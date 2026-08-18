import tempfile
import unittest
from pathlib import Path

import duckdb

from prototype.selective_reader.genome_map import genome_map_for_workspace


class GenomeMapTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name)
        chromosome_one = self.workspace / "variants.parquet" / "chrom=chr1"
        chromosome_two = self.workspace / "variants.parquet" / "chrom=chr2"
        chromosome_one.mkdir(parents=True)
        chromosome_two.mkdir(parents=True)
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1:1:A:G'::VARCHAR AS variant_id,
                       'rs1'::VARCHAR AS rsid,
                       'chr1'::VARCHAR AS chrom,
                       1::BIGINT AS pos
                UNION ALL
                SELECT 'chr1:248956422:C:T', 'rs2', 'chr1', 248956422
            ) TO ? (FORMAT PARQUET)
            """,
            [str(chromosome_one / "part-0000.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'chr2:10:G:A'::VARCHAR AS variant_id,
                       NULL::VARCHAR AS rsid,
                       'chr2'::VARCHAR AS chrom,
                       10::BIGINT AS pos
            ) TO ? (FORMAT PARQUET)
            """,
            [str(chromosome_two / "part-0000.parquet")],
        )
        connection.close()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_builds_bounded_variant_density_and_drill_down_queries(self):
        result = genome_map_for_workspace(str(self.workspace), "GRCh38")

        self.assertTrue(result["supported"])
        self.assertEqual(result["bin_count"], 24)
        self.assertEqual(result["total_variant_records"], 3)
        self.assertEqual(len(result["chromosomes"]), 25)
        chromosome_one = result["chromosomes"][0]
        self.assertEqual(chromosome_one["chrom"], "chr1")
        self.assertEqual(chromosome_one["variant_count"], 2)
        self.assertEqual(len(chromosome_one["bins"]), 24)
        self.assertEqual(chromosome_one["bins"][0]["variant_count"], 1)
        self.assertEqual(chromosome_one["bins"][0]["example_query"], "rs1")
        self.assertEqual(chromosome_one["bins"][-1]["variant_count"], 1)
        self.assertEqual(chromosome_one["bins"][-1]["example_query"], "rs2")
        chromosome_two = result["chromosomes"][1]
        self.assertEqual(chromosome_two["bins"][0]["example_query"], "chr2:10:G:A")
        self.assertEqual(result["callability"]["state"], "not_included")

    def test_reports_site_callability_records_without_treating_them_as_coverage(self):
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1'::VARCHAR AS chrom, true AS callable
                UNION ALL SELECT 'chr1', false
                UNION ALL SELECT 'chr2', true
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callability.parquet")],
        )
        connection.close()

        result = genome_map_for_workspace(str(self.workspace), "GRCh38")

        self.assertEqual(result["callability"]["state"], "available")
        self.assertEqual(result["callability"]["kind"], "site_records")
        self.assertEqual(result["callability"]["record_count"], 3)
        self.assertEqual(result["chromosomes"][0]["callability_records"], 2)
        self.assertEqual(result["chromosomes"][1]["callability_records"], 1)

    def test_reports_an_included_but_empty_callability_table(self):
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT NULL::VARCHAR AS chrom, NULL::BOOLEAN AS callable
                WHERE false
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callability.parquet")],
        )
        connection.close()

        result = genome_map_for_workspace(str(self.workspace), "GRCh38")

        self.assertEqual(result["callability"]["state"], "included_empty")
        self.assertEqual(result["callability"]["kind"], "site_records")
        self.assertEqual(result["callability"]["record_count"], 0)

    def test_prefers_interval_callability_when_both_sources_exist(self):
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1'::VARCHAR AS chrom, true AS callable
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callability.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'chr1'::VARCHAR AS chrom, 1::BIGINT AS start_pos,
                       100::BIGINT AS end_pos, true AS callable
                UNION ALL SELECT 'chr2', 1, 50, true
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callable_regions.parquet")],
        )
        connection.close()

        result = genome_map_for_workspace(str(self.workspace), "GRCh38")

        self.assertEqual(result["callability"]["state"], "available")
        self.assertEqual(result["callability"]["kind"], "interval_records")
        self.assertEqual(result["callability"]["source"], "callable_regions.parquet")
        self.assertEqual(result["callability"]["record_count"], 2)

    def test_does_not_infer_a_map_for_an_unsupported_genome_build(self):
        result = genome_map_for_workspace(str(self.workspace), "GRCh37")

        self.assertFalse(result["supported"])
        self.assertEqual(result["reason"], "genome_build_not_supported")
        self.assertEqual(result["chromosomes"], [])


if __name__ == "__main__":
    unittest.main()
