import json
import tempfile
import unittest
from pathlib import Path

import duckdb

from prototype.selective_reader.topics import (
    TOPIC_INDEX_FILENAME,
    topic_summary_for_query,
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
                SELECT
                    'variant-1'::VARCHAR AS variant_id,
                    struct_pack(
                        is_gwas_hit := true,
                        traits := ['cholesterol levels']::VARCHAR[],
                        effect_size := 0.2::DOUBLE,
                        effect_type := 'beta'::VARCHAR,
                        effect_allele := 'G'::VARCHAR,
                        ci_lower := 0.1::DOUBLE,
                        ci_upper := 0.3::DOUBLE,
                        p_value := 1e-9::DOUBLE,
                        sample_size := 100000::BIGINT,
                        study_pmids := ['12345']::VARCHAR[]
                    ) AS trait_associations
                UNION ALL
                SELECT
                    'variant-2'::VARCHAR AS variant_id,
                    struct_pack(
                        is_gwas_hit := false,
                        traits := []::VARCHAR[],
                        effect_size := NULL::DOUBLE,
                        effect_type := NULL::VARCHAR,
                        effect_allele := NULL::VARCHAR,
                        ci_lower := NULL::DOUBLE,
                        ci_upper := NULL::DOUBLE,
                        p_value := NULL::DOUBLE,
                        sample_size := NULL::BIGINT,
                        study_pmids := []::VARCHAR[]
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
                SELECT 'cholesterol levels'::VARCHAR AS trait,
                       'lipid measurement'::VARCHAR AS mapped_trait,
                       'cholesterol levels'::VARCHAR AS reported_trait
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "gwas_associations.parquet")],
        )
        connection.close()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_topic_index_exposes_recorded_values_and_personal_variant_counts(self):
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
        self.assertEqual(cholesterol["personal"]["trait_variant_count"], 1)
        self.assertEqual(
            cholesterol["personal"]["polygenic_scores"][0]["percentile"],
            81.5,
        )
        self.assertEqual(cholesterol["research_association_count"], 1)
        self.assertEqual(
            topic_summary_for_query(str(self.workspace), "cholesterol"),
            {
                "section": "trait_variant_summary",
                "trait": "Cholesterol levels",
                "variant_count": 1,
            },
        )

        cache = json.loads((self.workspace / TOPIC_INDEX_FILENAME).read_text())
        self.assertEqual(cache["topics"], topics)


if __name__ == "__main__":
    unittest.main()
