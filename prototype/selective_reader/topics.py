from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Optional, Sequence, Set, Tuple

import duckdb


TOPIC_INDEX_FILENAME = ".topic-index.json"
TOPIC_INDEX_VERSION = 4

TOPICS: Tuple[Dict[str, str], ...] = (
    # Medications are matched only against recorded pharmacogenomic drug links.
    {"id": "clopidogrel", "kind": "medications", "label": "Clopidogrel", "query": "clopidogrel", "group": "Heart and circulation"},
    {"id": "warfarin", "kind": "medications", "label": "Warfarin", "query": "warfarin", "group": "Heart and circulation"},
    {"id": "simvastatin", "kind": "medications", "label": "Simvastatin", "query": "simvastatin", "group": "Heart and circulation"},
    {"id": "ibuprofen", "kind": "medications", "label": "Ibuprofen", "query": "ibuprofen", "group": "Pain and inflammation"},
    {"id": "celecoxib", "kind": "medications", "label": "Celecoxib", "query": "celecoxib", "group": "Pain and inflammation"},
    {"id": "codeine", "kind": "medications", "label": "Codeine", "query": "codeine", "group": "Pain and inflammation"},
    {"id": "omeprazole", "kind": "medications", "label": "Omeprazole", "query": "omeprazole", "group": "Digestion"},
    {"id": "sertraline", "kind": "medications", "label": "Sertraline", "query": "sertraline", "group": "Mental health"},
    {"id": "citalopram", "kind": "medications", "label": "Citalopram", "query": "citalopram", "group": "Mental health"},
    {"id": "amitriptyline", "kind": "medications", "label": "Amitriptyline", "query": "amitriptyline", "group": "Mental health"},
    {"id": "phenytoin", "kind": "medications", "label": "Phenytoin", "query": "phenytoin", "group": "Neurology"},
    {"id": "fluorouracil", "kind": "medications", "label": "Fluorouracil", "query": "fluorouracil", "group": "Cancer treatment"},
    {"id": "capecitabine", "kind": "medications", "label": "Capecitabine", "query": "capecitabine", "group": "Cancer treatment"},
    {"id": "azathioprine", "kind": "medications", "label": "Azathioprine", "query": "azathioprine", "group": "Immune conditions"},
    {"id": "voriconazole", "kind": "medications", "label": "Voriconazole", "query": "voriconazole", "group": "Infections"},
    # Conditions and traits are matched only against recorded PRS and GWAS text.
    {"id": "coronary-artery-disease", "kind": "conditions", "label": "Coronary artery disease", "query": "coronary artery disease", "group": "Heart and circulation"},
    {"id": "atrial-fibrillation", "kind": "conditions", "label": "Atrial fibrillation", "query": "atrial fibrillation", "group": "Heart and circulation"},
    {"id": "type-2-diabetes", "kind": "conditions", "label": "Type 2 diabetes", "query": "type 2 diabetes", "group": "Metabolism"},
    {"id": "breast-cancer", "kind": "conditions", "label": "Breast cancer", "query": "breast cancer", "group": "Cancer"},
    {"id": "prostate-cancer", "kind": "conditions", "label": "Prostate cancer", "query": "prostate cancer", "group": "Cancer"},
    {"id": "colorectal-cancer", "kind": "conditions", "label": "Colorectal cancer", "query": "colorectal cancer", "group": "Cancer"},
    {"id": "alzheimers-disease", "kind": "conditions", "label": "Alzheimer's disease", "query": "Alzheimer", "group": "Brain and nervous system"},
    {"id": "migraine", "kind": "conditions", "label": "Migraine", "query": "migraine", "group": "Brain and nervous system"},
    {"id": "asthma", "kind": "conditions", "label": "Asthma", "query": "asthma", "group": "Immune and respiratory"},
    {"id": "celiac-disease", "kind": "conditions", "label": "Celiac disease", "query": "celiac disease", "group": "Immune and respiratory"},
    {"id": "rheumatoid-arthritis", "kind": "conditions", "label": "Rheumatoid arthritis", "query": "rheumatoid arthritis", "group": "Immune and respiratory"},
    {"id": "pcos", "kind": "conditions", "label": "PCOS", "query": "pcos", "group": "Hormones and reproductive health"},
    {"id": "osteoporosis", "kind": "conditions", "label": "Osteoporosis", "query": "osteoporosis", "group": "Bones"},
    {"id": "depression", "kind": "conditions", "label": "Depression", "query": "depression", "group": "Mental health"},
    {"id": "chronic-kidney-disease", "kind": "conditions", "label": "Chronic kidney disease", "query": "chronic kidney disease", "group": "Kidney health"},
    {"id": "cholesterol", "kind": "traits", "label": "Cholesterol levels", "query": "cholesterol", "group": "Heart and metabolism"},
    {"id": "blood-pressure", "kind": "traits", "label": "Blood pressure", "query": "blood pressure", "group": "Heart and metabolism"},
    {"id": "body-mass-index", "kind": "traits", "label": "Body mass index", "query": "body mass index", "group": "Body measurements"},
    {"id": "height", "kind": "traits", "label": "Height", "query": "height", "group": "Body measurements"},
    {"id": "chronotype", "kind": "traits", "label": "Morning or evening preference", "query": "chronotype", "group": "Sleep"},
    {"id": "sleep-duration", "kind": "traits", "label": "Sleep duration", "query": "sleep duration", "group": "Sleep"},
    {"id": "caffeine", "kind": "traits", "label": "Caffeine consumption", "query": "caffeine", "group": "Everyday habits"},
    {"id": "alcohol", "kind": "traits", "label": "Alcohol consumption", "query": "alcohol consumption", "group": "Everyday habits"},
    {"id": "extraversion", "kind": "traits", "label": "Extraversion", "query": "extraversion", "group": "Behavior and preferences"},
    {"id": "neuroticism", "kind": "traits", "label": "Neuroticism", "query": "neuroticism", "group": "Behavior and preferences"},
    {"id": "handedness", "kind": "traits", "label": "Handedness", "query": "handedness", "group": "Behavior and preferences"},
    {"id": "lactose-intolerance", "kind": "traits", "label": "Lactose intolerance", "query": "lactose intolerance", "group": "Food and digestion"},
    {"id": "eye-color", "kind": "traits", "label": "Eye color", "query": "eye color", "group": "Appearance"},
    {"id": "hair-color", "kind": "traits", "label": "Hair color", "query": "hair color", "group": "Appearance"},
    {"id": "age-at-menopause", "kind": "traits", "label": "Age at menopause", "query": "age at menopause", "group": "Hormones and reproductive health"},
)


def _sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def _topic_values(topics: Sequence[Dict[str, str]]) -> Tuple[str, List[str]]:
    placeholders = ", ".join(["(?, ?)"] * len(topics))
    parameters: List[str] = []
    for topic in topics:
        parameters.extend([topic["id"], topic["query"]])
    return placeholders, parameters


def _topic_details() -> Dict[str, Dict[str, Any]]:
    return {
        topic["id"]: {
            "pharmacogenomics": [],
            "polygenic_scores": [],
            "has_person_linked_variants": False,
        }
        for topic in TOPICS
    }


def _scan_medications(
    connection: Any,
    workspace: Path,
    topics: Sequence[Dict[str, str]],
    matches: DefaultDict[str, Set[str]],
    details: Dict[str, Dict[str, Any]],
) -> None:
    path = workspace / "pharmacogenomics.parquet"
    if not path.is_file():
        return
    connection.execute(
        "CREATE VIEW topic_pharmacogenomics AS SELECT * FROM read_parquet('%s')"
        % _sql_path(path)
    )
    values, parameters = _topic_values(topics)
    cursor = connection.execute(
        """
        WITH topics(topic_id, term) AS (VALUES %s)
        SELECT DISTINCT topic_id, gene_symbol, diplotype, phenotype
        FROM topics, topic_pharmacogenomics AS pharmacogenomics
        WHERE EXISTS (
            SELECT 1
            FROM UNNEST(pharmacogenomics.affected_drugs) AS drug(value)
            WHERE lower(value) LIKE '%%' || lower(term) || '%%'
        )
        """ % values,
        parameters,
    )
    for topic_id, gene_symbol, diplotype, phenotype in cursor.fetchall():
        key = str(topic_id)
        matches[key].add("pharmacogenomics")
        details[key]["pharmacogenomics"].append(
            {
                "gene_symbol": gene_symbol,
                "diplotype": diplotype,
                "phenotype": phenotype,
            }
        )


def _scan_traits(
    connection: Any,
    workspace: Path,
    topics: Sequence[Dict[str, str]],
    matches: DefaultDict[str, Set[str]],
    details: Dict[str, Dict[str, Any]],
) -> None:
    values, parameters = _topic_values(topics)
    prs_path = workspace / "prs.parquet"
    if prs_path.is_file():
        connection.execute(
            "CREATE VIEW topic_prs AS SELECT * FROM read_parquet('%s')"
            % _sql_path(prs_path)
        )
        cursor = connection.execute(
            """
            WITH topics(topic_id, term) AS (VALUES %s)
            SELECT DISTINCT topic_id, prs.trait, prs.score_value,
                            prs.percentile, prs.reference_population
            FROM topics, topic_prs AS prs
            WHERE lower(prs.trait) LIKE '%%' || lower(term) || '%%'
            """ % values,
            parameters,
        )
        for (
            topic_id,
            trait,
            score_value,
            percentile,
            reference_population,
        ) in cursor.fetchall():
            key = str(topic_id)
            matches[key].add("polygenic_scores")
            details[key]["polygenic_scores"].append(
                {
                    "trait": trait,
                    "score_value": score_value,
                    "percentile": percentile,
                    "reference_population": reference_population,
                }
            )

    variants_path = workspace / "variants.parquet"
    if variants_path.is_dir():
        connection.execute(
            "CREATE VIEW topic_variants AS SELECT * FROM read_parquet("
            "'%s/**/*.parquet', hive_partitioning=true)" % _sql_path(variants_path)
        )
        try:
            connection.execute(
                "SELECT trait_associations.is_gwas_hit, "
                "trait_associations.traits FROM topic_variants LIMIT 0"
            )
        except duckdb.Error:
            pass
        else:
            cursor = connection.execute(
                """
                WITH topics(topic_id, term) AS (VALUES %s)
                SELECT DISTINCT topics.topic_id
                FROM topic_variants AS variants
                CROSS JOIN UNNEST(variants.trait_associations.traits) AS annotation(value)
                JOIN topics
                  ON lower(annotation.value) LIKE '%%' || lower(topics.term) || '%%'
                WHERE variants.trait_associations.is_gwas_hit
                """ % values,
                parameters,
            )
            for (topic_id,) in cursor.fetchall():
                key = str(topic_id)
                matches[key].add("trait_variants")
                details[key]["has_person_linked_variants"] = True


def _catalog_signature() -> str:
    serialized = json.dumps(TOPICS, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _load_topic_index(workspace: Path) -> Optional[Dict[str, Any]]:
    path = workspace / TOPIC_INDEX_FILENAME
    try:
        payload = json.loads(path.read_text())
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return None
    if payload.get("version") != TOPIC_INDEX_VERSION:
        return None
    if payload.get("catalog_signature") != _catalog_signature():
        return None
    if not isinstance(payload.get("topics"), list):
        return None
    return payload


def _store_topic_index(workspace: Path, topics: List[Dict[str, Any]]) -> None:
    path = workspace / TOPIC_INDEX_FILENAME
    temporary_path = workspace / (TOPIC_INDEX_FILENAME + ".tmp")
    payload = {
        "version": TOPIC_INDEX_VERSION,
        "catalog_signature": _catalog_signature(),
        "topics": topics,
    }
    try:
        temporary_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        temporary_path.replace(path)
    except OSError:
        temporary_path.unlink(missing_ok=True)


def topics_for_workspace(workspace_path: str) -> List[Dict[str, Any]]:
    workspace = Path(workspace_path).resolve()
    cached = _load_topic_index(workspace)
    if cached is not None:
        return cached["topics"]

    matches: DefaultDict[str, Set[str]] = defaultdict(set)
    details = _topic_details()
    medications = [topic for topic in TOPICS if topic["kind"] == "medications"]
    traits = [topic for topic in TOPICS if topic["kind"] != "medications"]

    connection = duckdb.connect()
    try:
        connection.execute("SET threads = 2")
        connection.execute("SET enable_progress_bar = false")
        _scan_medications(connection, workspace, medications, matches, details)
        _scan_traits(connection, workspace, traits, matches, details)
    finally:
        connection.close()

    section_order = {
        "pharmacogenomics": 0,
        "polygenic_scores": 1,
        "trait_variants": 2,
    }
    result = [
        {
            **topic,
            "recorded": bool(matches[topic["id"]]),
            "record_sections": sorted(
                matches[topic["id"]], key=lambda section: section_order[section]
            ),
            "personal": {
                "pharmacogenomics": details[topic["id"]]["pharmacogenomics"],
                "polygenic_scores": details[topic["id"]]["polygenic_scores"],
                "has_person_linked_variants": details[topic["id"]][
                    "has_person_linked_variants"
                ],
            },
        }
        for topic in TOPICS
    ]
    _store_topic_index(workspace, result)
    return result
