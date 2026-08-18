import json
import tempfile
import unittest
from pathlib import Path

import duckdb

from prototype.selective_reader.topics import (
    TOPIC_INDEX_FILENAME,
    topics_for_workspace,
)


class TopicIndexTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name)
        variants = self.workspace / "variants.parquet" / "chrom=chr1"
        variants.mkdir(parents=True)
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'variant-1'::VARCHAR AS variant_id,
                       struct_pack(
                           is_gwas_hit := true,
                           traits := ['cholesterol levels']::VARCHAR[]
                       ) AS trait_associations
            ) TO ? (FORMAT PARQUET)
            """,
            [str(variants / "part-0000.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'CYP2C19'::VARCHAR AS gene_symbol,
                       '*1/*17'::VARCHAR AS diplotype,
                       'Rapid Metabolizer'::VARCHAR AS phenotype,
                       ['clopidogrel']::VARCHAR[] AS affected_drugs
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "pharmacogenomics.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'cholesterol'::VARCHAR AS trait,
                       0.42::DOUBLE AS score_value,
                       81.5::DOUBLE AS percentile,
                       'Synthetic reference'::VARCHAR AS reference_population
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "prs.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'finding-1'::VARCHAR AS finding_id,
                       'variant-1'::VARCHAR AS variant_id,
                       'BRCA1'::VARCHAR AS gene_symbol,
                       'Breast cancer'::VARCHAR AS condition,
                       'variant_classification'::VARCHAR AS claim_type,
                       'Likely_pathogenic'::VARCHAR AS classification,
                       true AS clinical_grade,
                       ['evidence-1']::VARCHAR[] AS evidence_ids
                UNION ALL
                SELECT 'finding-2', 'variant-2', 'GENE2', 'Asthma',
                       'variant_classification', 'Uncertain_significance',
                       false, ['evidence-2']::VARCHAR[]
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "clinical_findings.parquet")],
        )
        connection.close()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_topic_index_exposes_recorded_values_and_person_linked_records(self):
        topics = topics_for_workspace(str(self.workspace))
        by_id = {topic["id"]: topic for topic in topics}

        clopidogrel = by_id["clopidogrel"]
        self.assertEqual(
            clopidogrel["personal"]["pharmacogenomics"],
            [
                {
                    "gene_symbol": "CYP2C19",
                    "diplotype": "*1/*17",
                    "phenotype": "Rapid Metabolizer",
                }
            ],
        )

        cholesterol = by_id["cholesterol"]
        self.assertEqual(
            cholesterol["personal"]["polygenic_scores"][0]["percentile"],
            81.5,
        )
        self.assertTrue(cholesterol["personal"]["has_person_linked_variants"])
        self.assertIn("trait_variants", cholesterol["record_sections"])

        breast_cancer = by_id["breast-cancer"]
        self.assertEqual(
            breast_cancer["personal"]["clinical_findings"],
            [
                {
                    "finding_id": "finding-1",
                    "condition": "Breast cancer",
                    "claim_type": "variant_classification",
                    "classification": "Likely_pathogenic",
                    "gene_symbol": "BRCA1",
                }
            ],
        )
        self.assertIn("clinical_findings", breast_cancer["record_sections"])
        self.assertEqual(
            by_id["clinical-findings"]["personal"]["clinical_findings"],
            breast_cancer["personal"]["clinical_findings"],
        )
        self.assertNotIn("clinical_findings", by_id["asthma"]["record_sections"])
        self.assertEqual(
            by_id["ehlers-danlos-syndrome"]["query"],
            "Ehlers-Danlos",
        )
        self.assertEqual(by_id["parkinsons-disease"]["query"], "Parkinson")
        self.assertEqual(
            by_id["primary-immunodeficiency"]["query"],
            "primary immunodeficiency",
        )

        cache = json.loads((self.workspace / TOPIC_INDEX_FILENAME).read_text())
        self.assertEqual(cache["topics"], topics)


if __name__ == "__main__":
    unittest.main()
