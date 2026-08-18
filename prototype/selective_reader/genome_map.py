from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

import duckdb


BIN_COUNT = 24
GRCH38_CHROMOSOMES: Tuple[Tuple[str, str, int], ...] = (
    ("chr1", "1", 248956422),
    ("chr2", "2", 242193529),
    ("chr3", "3", 198295559),
    ("chr4", "4", 190214555),
    ("chr5", "5", 181538259),
    ("chr6", "6", 170805979),
    ("chr7", "7", 159345973),
    ("chr8", "8", 145138636),
    ("chr9", "9", 138394717),
    ("chr10", "10", 133797422),
    ("chr11", "11", 135086622),
    ("chr12", "12", 133275309),
    ("chr13", "13", 114364328),
    ("chr14", "14", 107043718),
    ("chr15", "15", 101991189),
    ("chr16", "16", 90338345),
    ("chr17", "17", 83257441),
    ("chr18", "18", 80373285),
    ("chr19", "19", 58617616),
    ("chr20", "20", 64444167),
    ("chr21", "21", 46709983),
    ("chr22", "22", 50818468),
    ("chrX", "X", 156040895),
    ("chrY", "Y", 57227415),
    ("chrM", "MT", 16569),
)


def _canonical_chromosome(value: Any) -> str:
    normalized = str(value or "").strip().upper()
    if normalized.startswith("CHR"):
        normalized = normalized[3:]
    if normalized == "MT":
        normalized = "M"
    return "chr" + normalized if normalized else ""


def _chromosome_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for chrom, label, length in GRCH38_CHROMOSOMES:
        bins = []
        for index in range(BIN_COUNT):
            bins.append(
                {
                    "index": index,
                    "start": math.floor(length * index / BIN_COUNT) + 1,
                    "end": math.floor(length * (index + 1) / BIN_COUNT),
                    "variant_count": 0,
                    "example_query": None,
                }
            )
        rows.append(
            {
                "chrom": chrom,
                "label": label,
                "length": length,
                "variant_count": 0,
                "callability_records": 0,
                "bins": bins,
            }
        )
    return rows


def _callability_summary(
    connection: duckdb.DuckDBPyConnection,
    workspace: Path,
) -> Tuple[Dict[str, Any], Dict[str, int]]:
    candidates = (
        (workspace / "callable_regions.parquet", "interval_records"),
        (workspace / "callability.parquet", "site_records"),
    )
    selected = next(
        ((path, kind) for path, kind in candidates if path.is_file()),
        None,
    )
    if selected is None:
        return (
            {
                "state": "not_included",
                "kind": None,
                "source": None,
                "record_count": 0,
            },
            {},
        )

    path, kind = selected
    try:
        rows = connection.execute(
            """
            SELECT chrom, count(*)::BIGINT AS record_count
            FROM read_parquet(?)
            WHERE chrom IS NOT NULL
            GROUP BY chrom
            """,
            [str(path)],
        ).fetchall()
    except duckdb.Error:
        return (
            {
                "state": "summary_unavailable",
                "kind": kind,
                "source": path.name,
                "record_count": 0,
            },
            {},
        )

    counts = {
        _canonical_chromosome(chrom): int(record_count)
        for chrom, record_count in rows
        if _canonical_chromosome(chrom)
    }
    total = sum(counts.values())
    return (
        {
            "state": "available" if total else "included_empty",
            "kind": kind,
            "source": path.name,
            "record_count": total,
        },
        counts,
    )


def genome_map_for_workspace(workspace_path: str, genome_build: str) -> Dict[str, Any]:
    if genome_build != "GRCh38":
        return {
            "supported": False,
            "reason": "genome_build_not_supported",
            "genome_build": genome_build,
            "bin_count": BIN_COUNT,
            "total_variant_records": 0,
            "callability": {
                "state": "not_evaluated",
                "kind": None,
                "source": None,
                "record_count": 0,
            },
            "chromosomes": [],
        }

    workspace = Path(workspace_path).resolve()
    variants = workspace / "variants.parquet"
    if not variants.is_dir():
        raise ValueError("workspace does not contain variants.parquet")

    chromosome_rows = _chromosome_rows()
    by_chromosome = {row["chrom"]: row for row in chromosome_rows}
    connection = duckdb.connect()
    try:
        connection.execute("PRAGMA threads=2")
        connection.execute(
            "CREATE TEMP TABLE genome_chromosomes "
            "(chrom VARCHAR, sort_order INTEGER, length BIGINT)"
        )
        connection.executemany(
            "INSERT INTO genome_chromosomes VALUES (?, ?, ?)",
            [
                (chrom, index, length)
                for index, (chrom, _label, length) in enumerate(GRCH38_CHROMOSOMES)
            ],
        )
        variant_rows = connection.execute(
            """
            SELECT chromosomes.chrom,
                   least(?, greatest(0, cast(floor(
                       (variants.pos - 1) * ?::DOUBLE / chromosomes.length
                   ) AS INTEGER))) AS bin_index,
                   count(*)::BIGINT AS variant_count,
                   arg_min(
                       coalesce(nullif(variants.rsid, ''), variants.variant_id),
                       variants.pos
                   ) AS example_query
            FROM read_parquet(?, hive_partitioning=true) AS variants
            JOIN genome_chromosomes AS chromosomes
              ON CASE
                   WHEN replace(lower(variants.chrom), 'chr', '') = 'mt' THEN 'm'
                   ELSE replace(lower(variants.chrom), 'chr', '')
                 END = replace(lower(chromosomes.chrom), 'chr', '')
            WHERE variants.pos BETWEEN 1 AND chromosomes.length
            GROUP BY chromosomes.chrom, bin_index
            """,
            [BIN_COUNT - 1, BIN_COUNT, str(variants / "**" / "*.parquet")],
        ).fetchall()

        for chrom, bin_index, variant_count, example_query in variant_rows:
            row = by_chromosome.get(_canonical_chromosome(chrom))
            if row is None:
                continue
            index = int(bin_index)
            count = int(variant_count)
            row["variant_count"] += count
            row["bins"][index]["variant_count"] = count
            row["bins"][index]["example_query"] = example_query

        callability, callability_counts = _callability_summary(connection, workspace)
        for chrom, count in callability_counts.items():
            row = by_chromosome.get(chrom)
            if row is not None:
                row["callability_records"] = count
    finally:
        connection.close()

    return {
        "supported": True,
        "reason": None,
        "genome_build": genome_build,
        "bin_count": BIN_COUNT,
        "total_variant_records": sum(
            row["variant_count"] for row in chromosome_rows
        ),
        "callability": callability,
        "chromosomes": chromosome_rows,
    }
