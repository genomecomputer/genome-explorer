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

        cache = json.loads((self.workspace / TOPIC_INDEX_FILENAME).read_text())
        self.assertEqual(cache["topics"], topics)


if __name__ == "__main__":
    unittest.main()
