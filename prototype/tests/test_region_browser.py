import tempfile
import unittest
from pathlib import Path

import duckdb

from prototype.selective_reader.region_browser import region_browser_for_workspace


class RegionBrowserTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name)
        variants = self.workspace / "variants.parquet" / "chrom=chr1"
        variants.mkdir(parents=True)
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1:' || cast(100 + index AS VARCHAR) || ':A:G' AS variant_id,
                       'rs' || cast(100 + index AS VARCHAR) AS rsid,
                       'chr1'::VARCHAR AS chrom,
                       (100 + index)::BIGINT AS pos,
                       'A'::VARCHAR AS ref,
                       'G'::VARCHAR AS alt,
                       struct_pack(gt := [0, 1]::INTEGER[], zygosity := 'het') AS genotype,
                       struct_pack(call_confidence := 'high') AS quality,
                       struct_pack(symbol := 'GENE1') AS gene,
                       struct_pack(hgvsp := NULL::VARCHAR) AS consequence,
                       struct_pack(
                           clinvar_significance := CASE WHEN index = 1 THEN 'Likely_pathogenic' ELSE NULL END,
                           clinvar_has_conflicts := false,
                           clinvar_conflict_summary := NULL::VARCHAR,
                           clinvar_review_stars := CASE WHEN index = 1 THEN 2 ELSE NULL END,
                           clinvar_submitters_count := NULL::INTEGER,
                           clinvar_id := CASE WHEN index = 1 THEN 'VCV1' ELSE NULL END
                       ) AS pathogenicity,
                       struct_pack(is_gwas_hit := index = 2) AS trait_associations,
                       struct_pack(is_pgx := index = 3) AS pharmacogenomics,
                       (index = 1) AS clinical_grade
                FROM range(1, 31) AS generated(index)
            ) TO ? (FORMAT PARQUET)
            """,
            [str(variants / "part-0000.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'GENE1'::VARCHAR AS gene_symbol,
                       'chr1'::VARCHAR AS chrom,
                       50::BIGINT AS start_pos,
                       250::BIGINT AS end_pos,
                       30::BIGINT AS variant_count,
                       1::BIGINT AS actionable_count
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "gene_index.parquet")],
        )
        connection.execute(
            """
            COPY (
                SELECT 'chr1'::VARCHAR AS chrom,
                       1::BIGINT AS start_pos,
                       175::BIGINT AS end_pos,
                       true AS callable
                UNION ALL SELECT 'chr1', 150, 225, true
                UNION ALL SELECT 'chr1', 226, 300, false
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callable_regions.parquet")],
        )
        connection.close()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_gene_query_builds_contextual_tracks_and_record_pages(self):
        payload = region_browser_for_workspace(
            str(self.workspace), "GRCh38", query="GENE1"
        )

        self.assertEqual(payload["target"]["kind"], "gene")
        self.assertEqual(payload["target"]["gene_start"], 50)
        self.assertEqual(payload["target"]["gene_end"], 250)
        self.assertEqual(payload["genes"]["genes"][0]["gene_symbol"], "GENE1")
        self.assertEqual(payload["variants"]["total"], 30)
        self.assertEqual(payload["annotations"]["total"], 3)
        self.assertEqual(payload["callability"]["kind"], "interval_records")
        self.assertEqual(payload["callability"]["callable_bases"], 225)
        self.assertEqual(payload["records"]["page"], 1)
        self.assertEqual(payload["records"]["page_count"], 2)
        self.assertEqual(len(payload["records"]["hits"]), 25)

        second_page = region_browser_for_workspace(
            str(self.workspace),
            "GRCh38",
            chrom=payload["region"]["chrom"],
            start=payload["region"]["start"],
            end=payload["region"]["end"],
            page=2,
        )
        self.assertEqual(len(second_page["records"]["hits"]), 5)

    def test_resolves_rsid_and_exact_coordinate_range(self):
        rsid = region_browser_for_workspace(
            str(self.workspace), "GRCh38", query="rs101"
        )
        coordinate = region_browser_for_workspace(
            str(self.workspace), "GRCh38", query="chr1:100-120"
        )
        formatted_coordinate = region_browser_for_workspace(
            str(self.workspace), "GRCh38", query="chr1:1,000-1,020"
        )

        self.assertEqual(rsid["target"]["kind"], "rsid")
        self.assertEqual(rsid["target"]["position"], 101)
        self.assertEqual(coordinate["region"]["start"], 100)
        self.assertEqual(coordinate["region"]["end"], 120)
        self.assertEqual(coordinate["region"]["chromosome_length"], 248956422)
        self.assertEqual(coordinate["variants"]["total"], 20)
        self.assertEqual(coordinate["callability"]["coverage_percent"], 100.0)
        self.assertEqual(formatted_coordinate["region"]["start"], 1000)

    def test_site_callability_is_not_reported_as_coverage(self):
        (self.workspace / "callable_regions.parquet").unlink()
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1'::VARCHAR AS chrom, 110::BIGINT AS pos, true AS callable
                UNION ALL SELECT 'chr1', 115, false
            ) TO ? (FORMAT PARQUET)
            """,
            [str(self.workspace / "callability.parquet")],
        )
        connection.close()

        payload = region_browser_for_workspace(
            str(self.workspace), "GRCh38", query="chr1:100-120"
        )

        self.assertEqual(payload["callability"]["kind"], "site_records")
        self.assertEqual(payload["callability"]["site_count"], 1)
        self.assertIsNone(payload["callability"]["coverage_percent"])

    def test_rejects_unknown_terms_and_oversized_regions(self):
        with self.assertRaisesRegex(ValueError, "gene is not recorded"):
            region_browser_for_workspace(
                str(self.workspace), "GRCh38", query="NOTAGENE"
            )
        with self.assertRaisesRegex(ValueError, "up to 25 Mb"):
            region_browser_for_workspace(
                str(self.workspace), "GRCh38", query="chr1:1-30000000"
            )


if __name__ == "__main__":
    unittest.main()
