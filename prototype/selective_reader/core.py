from __future__ import annotations

import hashlib
import json
import re
import shutil
import tarfile
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Optional, Tuple

import duckdb

from .topics import topic_summary_for_query


SUPPORTED_SCHEMA_VERSIONS = {"1.0.0"}
CHUNK_SIZE = 1024 * 1024
MAX_MANIFEST_BYTES = 5 * 1024 * 1024
RECEIPT_FILENAME = ".validation-receipt.json"
RECEIPT_VERSION = 1
COORDINATE_PATTERN = re.compile(
    r"^(?:chr)?(?P<chrom>[0-9]+|X|Y|M):(?P<pos>[0-9]+)"
    r"(?::(?P<ref>[ACGT]+):(?P<alt>[ACGT]+))?$",
    re.IGNORECASE,
)
RSID_PATTERN = re.compile(r"^rs[0-9]+$", re.IGNORECASE)


@dataclass
class WorkspaceReport:
    archive: str
    workspace: str
    schema_version: str
    genome_build: str
    generated_at: str
    extracted_files: int
    extracted_bytes: int
    skipped_files: int
    skipped_bytes: int
    validated_entries: int
    elapsed_seconds: float
    reused_workspace: bool
    validation_mode: str
    validated_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SearchResult:
    query: str
    query_kind: str
    hits: List[Dict[str, Any]]
    elapsed_seconds: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _safe_relative_path(name: str, root_name: str) -> Optional[str]:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("archive contains an unsafe path: %s" % name)
    if not path.parts:
        return None
    if path.parts[0] != root_name:
        raise ValueError("archive contains more than one top-level directory")
    if len(path.parts) == 1:
        return None
    return PurePosixPath(*path.parts[1:]).as_posix()


def _should_extract(relative_path: str) -> bool:
    lower = relative_path.lower()
    return (
        lower.endswith(".json")
        or lower.endswith(".parquet")
        or ".parquet/" in lower
    )


def _read_manifest(archive: Path) -> Tuple[str, bytes, Dict[str, Any]]:
    with tarfile.open(str(archive), mode="r:gz") as bundle:
        root_name = None
        for member in bundle:
            path = PurePosixPath(member.name)
            if not path.parts:
                continue
            if root_name is None:
                root_name = path.parts[0]
            if path.parts[0] != root_name:
                raise ValueError("archive contains more than one top-level directory")
            if len(path.parts) == 2 and path.name == "manifest.json":
                if not member.isfile():
                    raise ValueError("manifest.json is not a regular file")
                if member.size > MAX_MANIFEST_BYTES:
                    raise ValueError("manifest.json is unexpectedly large")
                source = bundle.extractfile(member)
                if source is None:
                    raise ValueError("manifest.json could not be read")
                manifest_bytes = source.read()
                manifest = json.loads(manifest_bytes)
                return root_name, manifest_bytes, manifest
    raise ValueError("manifest.json was not found")


def _manifest_identity(manifest_bytes: bytes) -> str:
    return hashlib.sha256(manifest_bytes).hexdigest()[:20]


def _archive_fingerprint(archive: Path) -> Dict[str, Any]:
    metadata = archive.stat()
    return {
        "path": str(archive),
        "size": metadata.st_size,
        "mtime_ns": metadata.st_mtime_ns,
        "device": metadata.st_dev,
        "inode": metadata.st_ino,
    }


def _workspace_entry_size(path: Path) -> Optional[int]:
    if path.is_symlink():
        return None
    if path.is_file():
        return path.stat().st_size
    if not path.is_dir():
        return None
    total = 0
    for member in path.rglob("*"):
        if member.is_symlink():
            return None
        if member.is_file():
            total += member.stat().st_size
    return total


def _workspace_matches_receipt(workspace: Path, receipt: Dict[str, Any]) -> bool:
    if receipt.get("version") != RECEIPT_VERSION:
        return False
    if not (workspace / "manifest.json").is_file():
        return False
    if not (workspace / "schema.json").is_file():
        return False
    if not (workspace / "variants.parquet").is_dir():
        return False

    manifest_hasher = hashlib.sha256()
    with (workspace / "manifest.json").open("rb") as source:
        manifest_hasher.update(source.read())
    if manifest_hasher.hexdigest() != receipt.get("manifest_sha256"):
        return False

    stored_entries = receipt.get("stored_entries")
    if not isinstance(stored_entries, dict):
        return False
    for relative_path, expected_size in stored_entries.items():
        path = PurePosixPath(relative_path)
        if path.is_absolute() or ".." in path.parts:
            return False
        if _workspace_entry_size(workspace / relative_path) != expected_size:
            return False
    return True


def _cached_workspace_report(
    archive: Path, workspace_root: Path, started: float
) -> Optional[WorkspaceReport]:
    if not workspace_root.is_dir():
        return None
    fingerprint = _archive_fingerprint(archive)
    for workspace in workspace_root.iterdir():
        if not workspace.is_dir() or ".partial-" in workspace.name:
            continue
        receipt_path = workspace / RECEIPT_FILENAME
        if not receipt_path.is_file():
            continue
        try:
            receipt = json.loads(receipt_path.read_text())
            if receipt.get("archive") != fingerprint:
                continue
            if not _workspace_matches_receipt(workspace, receipt):
                continue
            report = receipt["report"]
            return WorkspaceReport(
                archive=str(archive),
                workspace=str(workspace),
                schema_version=report["schema_version"],
                genome_build=report["genome_build"],
                generated_at=report["generated_at"],
                extracted_files=report["extracted_files"],
                extracted_bytes=report["extracted_bytes"],
                skipped_files=report["skipped_files"],
                skipped_bytes=report["skipped_bytes"],
                validated_entries=report["validated_entries"],
                elapsed_seconds=round(time.monotonic() - started, 3),
                reused_workspace=True,
                validation_mode="cached",
                validated_at=receipt["validated_at"],
            )
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
            continue
    return None


def _ancestor_manifest_directories(
    relative_path: str, manifest_paths: Iterable[str]
) -> List[str]:
    return [
        candidate
        for candidate in manifest_paths
        if relative_path.startswith(candidate.rstrip("/") + "/")
    ]


def _hash_directory(path: Path) -> Tuple[str, int]:
    hasher = hashlib.sha256()
    total_bytes = 0
    for member in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        hasher.update(member.relative_to(path).as_posix().encode("utf-8"))
        hasher.update(b"\0")
        with member.open("rb") as source:
            while True:
                chunk = source.read(CHUNK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
                total_bytes += len(chunk)
    return hasher.hexdigest(), total_bytes


def open_bundle(
    archive_path: str, workspace_root: Path, force_validate: bool = False
) -> WorkspaceReport:
    started = time.monotonic()
    archive = Path(archive_path).expanduser().resolve()
    if not archive.is_file():
        raise ValueError("archive does not exist: %s" % archive)

    if not force_validate:
        cached_report = _cached_workspace_report(archive, workspace_root, started)
        if cached_report is not None:
            return cached_report

    archive_fingerprint = _archive_fingerprint(archive)

    root_name, manifest_bytes, manifest = _read_manifest(archive)
    schema_version = manifest.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("unsupported schema version: %r" % schema_version)

    declared = manifest.get("files")
    if not isinstance(declared, dict):
        raise ValueError("manifest files field is missing or invalid")

    workspace_root.mkdir(parents=True, exist_ok=True)
    final_workspace = workspace_root / _manifest_identity(manifest_bytes)
    temporary_workspace = Path(
        tempfile.mkdtemp(
            prefix=final_workspace.name + ".partial-", dir=str(workspace_root)
        )
    )
    validation_workspace = Path(
        tempfile.mkdtemp(
            prefix=final_workspace.name + ".validation-", dir=str(workspace_root)
        )
    )

    exact_hashes: Dict[str, str] = {}
    exact_sizes: Dict[str, int] = {}
    observed_directories = set()
    manifest_paths = tuple(declared.keys())
    extracted_files = 0
    extracted_bytes = 0
    skipped_files = 0
    skipped_bytes = 0

    try:
        with tarfile.open(str(archive), mode="r|gz") as bundle:
            for member in bundle:
                relative_path = _safe_relative_path(member.name, root_name)
                if member.issym() or member.islnk():
                    raise ValueError("archive links are not supported: %s" % member.name)
                if member.isdir() or relative_path is None:
                    continue
                if not member.isfile():
                    raise ValueError(
                        "archive contains a non-regular entry: %s" % member.name
                    )

                source = bundle.extractfile(member)
                if source is None:
                    raise ValueError("archive member could not be read: %s" % member.name)

                ancestors = _ancestor_manifest_directories(
                    relative_path, manifest_paths
                )
                observed_directories.update(ancestors)
                should_extract = (
                    any(directory.lower().endswith(".parquet") for directory in ancestors)
                    if ancestors
                    else _should_extract(relative_path)
                )

                destination_path = None
                if should_extract:
                    destination_path = temporary_workspace / relative_path
                elif ancestors:
                    destination_path = validation_workspace / relative_path

                destination = None
                if destination_path is not None:
                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    destination = destination_path.open("wb")

                file_hasher = hashlib.sha256()
                try:
                    while True:
                        chunk = source.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        file_hasher.update(chunk)
                        if destination is not None:
                            destination.write(chunk)
                finally:
                    if destination is not None:
                        destination.close()

                exact_hashes[relative_path] = file_hasher.hexdigest()
                exact_sizes[relative_path] = member.size
                if should_extract:
                    extracted_files += 1
                    extracted_bytes += member.size
                else:
                    skipped_files += 1
                    skipped_bytes += member.size

        failures = []
        for relative_path, metadata in declared.items():
            if relative_path in observed_directories:
                extracted_directory = temporary_workspace / relative_path
                validation_directory = validation_workspace / relative_path
                directory_path = (
                    extracted_directory
                    if extracted_directory.is_dir()
                    else validation_directory
                )
                actual_hash, actual_size = _hash_directory(directory_path)
            else:
                actual_hash = exact_hashes.get(relative_path)
                actual_size = exact_sizes.get(relative_path)

            if actual_hash is None:
                failures.append("missing declared entry: %s" % relative_path)
                continue
            if actual_hash != metadata.get("sha256"):
                failures.append("hash mismatch: %s" % relative_path)
            expected_size = metadata.get("bytes")
            if expected_size is not None and actual_size != expected_size:
                failures.append("byte count mismatch: %s" % relative_path)

        if "schema.json" not in exact_hashes:
            failures.append("missing required entry: schema.json")
        if not any(path.startswith("variants.parquet/") for path in exact_hashes):
            failures.append("missing required directory: variants.parquet")
        if failures:
            raise ValueError("bundle validation failed:\n  - " + "\n  - ".join(failures))

        if _archive_fingerprint(archive) != archive_fingerprint:
            raise ValueError("archive changed during validation")

        shutil.rmtree(validation_workspace)
        validated_at = datetime.now(timezone.utc).isoformat()
        stored_entries = {
            relative_path: metadata.get("bytes")
            for relative_path, metadata in declared.items()
            if _should_extract(relative_path) and metadata.get("bytes") is not None
        }
        receipt = {
            "version": RECEIPT_VERSION,
            "validated_at": validated_at,
            "archive": archive_fingerprint,
            "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "stored_entries": stored_entries,
            "report": {
                "schema_version": str(schema_version),
                "genome_build": str(manifest.get("genome_build")),
                "generated_at": str(manifest.get("generated_at")),
                "extracted_files": extracted_files,
                "extracted_bytes": extracted_bytes,
                "skipped_files": skipped_files,
                "skipped_bytes": skipped_bytes,
                "validated_entries": len(declared),
            },
        }
        receipt_path = temporary_workspace / RECEIPT_FILENAME
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

        if final_workspace.is_symlink() or final_workspace.is_file():
            final_workspace.unlink()
        elif final_workspace.is_dir():
            shutil.rmtree(final_workspace)
        temporary_workspace.replace(final_workspace)

        return WorkspaceReport(
            archive=str(archive),
            workspace=str(final_workspace),
            schema_version=str(schema_version),
            genome_build=str(manifest.get("genome_build")),
            generated_at=str(manifest.get("generated_at")),
            extracted_files=extracted_files,
            extracted_bytes=extracted_bytes,
            skipped_files=skipped_files,
            skipped_bytes=skipped_bytes,
            validated_entries=len(declared),
            elapsed_seconds=round(time.monotonic() - started, 3),
            reused_workspace=False,
            validation_mode="full",
            validated_at=validated_at,
        )
    except Exception:
        shutil.rmtree(temporary_workspace, ignore_errors=True)
        shutil.rmtree(validation_workspace, ignore_errors=True)
        raise


def _sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def _rows(cursor: Any, section: str) -> List[Dict[str, Any]]:
    columns = [description[0] for description in cursor.description]
    return [
        {"section": section, **dict(zip(columns, row))}
        for row in cursor.fetchall()
    ]


def _variant_projection() -> str:
    return """
        variant_id,
        rsid,
        chrom,
        pos,
        ref,
        alt,
        genotype.gt AS genotype,
        genotype.zygosity AS zygosity,
        quality.call_confidence AS call_confidence,
        gene.symbol AS gene,
        consequence.hgvsp AS hgvsp,
        pathogenicity.clinvar_significance AS clinvar_significance,
        pathogenicity.clinvar_review_stars AS clinvar_review_stars,
        pathogenicity.clinvar_id AS clinvar_id,
        clinical_grade
    """


def search_workspace(workspace_path: str, query: str) -> SearchResult:
    started = time.monotonic()
    workspace = Path(workspace_path).resolve()
    variants = workspace / "variants.parquet"
    if not variants.is_dir():
        raise ValueError("workspace does not contain variants.parquet")

    connection = duckdb.connect()
    connection.execute(
        "CREATE VIEW variants AS SELECT * FROM read_parquet("
        "'%s/**/*.parquet', hive_partitioning=true)" % _sql_path(variants)
    )

    table_files = {
        "pharmacogenomics": workspace / "pharmacogenomics.parquet",
        "prs": workspace / "prs.parquet",
        "gwas_associations": workspace / "gwas_associations.parquet",
        "gene_index": workspace / "gene_index.parquet",
    }
    available = set()
    for table, path in table_files.items():
        if path.is_file():
            connection.execute(
                "CREATE VIEW %s AS SELECT * FROM read_parquet('%s')"
                % (table, _sql_path(path))
            )
            available.add(table)

    normalized_query = query.strip()
    if not normalized_query:
        raise ValueError("search query cannot be empty")

    hits: List[Dict[str, Any]] = []
    coordinate = COORDINATE_PATTERN.fullmatch(normalized_query)
    if RSID_PATTERN.fullmatch(normalized_query):
        query_kind = "rsid"
        cursor = connection.execute(
            "SELECT %s FROM variants WHERE lower(rsid) = lower(?) LIMIT 25"
            % _variant_projection(),
            [normalized_query],
        )
        hits.extend(_rows(cursor, "variants"))
    elif coordinate:
        query_kind = "coordinate"
        chrom = "chr" + coordinate.group("chrom").upper()
        parameters: List[Any] = [chrom, int(coordinate.group("pos"))]
        predicate = "chrom = ? AND pos = ?"
        if coordinate.group("ref") and coordinate.group("alt"):
            predicate += " AND ref = ? AND alt = ?"
            parameters.extend(
                [coordinate.group("ref").upper(), coordinate.group("alt").upper()]
            )
        cursor = connection.execute(
            "SELECT %s FROM variants WHERE %s LIMIT 25"
            % (_variant_projection(), predicate),
            parameters,
        )
        hits.extend(_rows(cursor, "variants"))
    else:
        query_kind = "term"
        cursor = connection.execute(
            "SELECT %s FROM variants WHERE upper(gene.symbol) = upper(?) LIMIT 25"
            % _variant_projection(),
            [normalized_query],
        )
        hits.extend(_rows(cursor, "variants"))

        if "gene_index" in available:
            cursor = connection.execute(
                """
                SELECT gene_symbol, chrom, start_pos, end_pos,
                       variant_count, actionable_count
                FROM gene_index
                WHERE upper(gene_symbol) = upper(?)
                LIMIT 25
                """,
                [normalized_query],
            )
            hits.extend(_rows(cursor, "genes"))

        if "pharmacogenomics" in available:
            cursor = connection.execute(
                """
                SELECT gene_symbol, diplotype, phenotype, activity_score,
                       copy_number, cpic_level, affected_drugs, guideline_url
                FROM pharmacogenomics
                WHERE upper(gene_symbol) = upper(?)
                   OR EXISTS (
                       SELECT 1
                       FROM UNNEST(affected_drugs) AS drug(value)
                       WHERE lower(value) LIKE '%' || lower(?) || '%'
                   )
                LIMIT 25
                """,
                [normalized_query, normalized_query],
            )
            hits.extend(_rows(cursor, "pharmacogenomics"))

        if "prs" in available:
            cursor = connection.execute(
                """
                SELECT trait, score_value, percentile, reference_population,
                       training_source, training_date
                FROM prs
                WHERE lower(trait) LIKE '%' || lower(?) || '%'
                LIMIT 25
                """,
                [normalized_query],
            )
            hits.extend(_rows(cursor, "polygenic_scores"))

        topic_summary = topic_summary_for_query(str(workspace), normalized_query)
        if topic_summary is not None:
            hits.append(topic_summary)

        if "gwas_associations" in available:
            cursor = connection.execute(
                """
                SELECT variant_id, rsid, gene, chrom, pos, ref, alt, trait,
                       effect_allele, effect_size, effect_type, p_value,
                       source, pubmed_id, study_accession, catalog_version
                FROM gwas_associations
                WHERE lower(trait) LIKE '%' || lower(?) || '%'
                   OR lower(COALESCE(mapped_trait, '')) LIKE '%' || lower(?) || '%'
                   OR lower(COALESCE(reported_trait, '')) LIKE '%' || lower(?) || '%'
                LIMIT 25
                """,
                [normalized_query, normalized_query, normalized_query],
            )
            hits.extend(_rows(cursor, "gwas"))

    connection.close()
    return SearchResult(
        query=normalized_query,
        query_kind=query_kind,
        hits=hits,
        elapsed_seconds=round(time.monotonic() - started, 3),
    )


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
