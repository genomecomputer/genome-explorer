import json
import tempfile
import unittest
from pathlib import Path

import duckdb

from prototype.selective_reader.core import search_workspace


class AnswerabilityTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary_directory.name)
        variants = self.workspace / "variants.parquet" / "chrom=chr1"
        variants.mkdir(parents=True)
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'chr1:100:A:G'::VARCHAR AS variant_id,
                       'rs100'::VARCHAR AS rsid,
                       'chr1'::VARCHAR AS chrom,
                       100::INTEGER AS pos,
                       'A'::VARCHAR AS ref,
                       'G'::VARCHAR AS alt,
                       struct_pack(gt := [0, 1]::INTEGER[], zygosity := 'het') AS genotype,
                       struct_pack(call_confidence := 'high') AS quality,
                       struct_pack(symbol := 'GENE1') AS gene,
                       struct_pack(hgvsp := NULL::VARCHAR) AS consequence,
                       struct_pack(
                           clinvar_significance := NULL::VARCHAR,
                           clinvar_has_conflicts := false,
                           clinvar_conflict_summary := NULL::VARCHAR,
                           clinvar_review_stars := NULL::INTEGER,
                           clinvar_submitters_count := NULL::INTEGER,
                           clinvar_id := NULL::VARCHAR
                       ) AS pathogenicity,
                       false AS clinical_grade
            ) TO ? (FORMAT PARQUET)
            """,
            [str(variants / "part-0000.parquet")],
        )
        connection.close()
        self._write_manifest("1.1.0", ["variants.parquet"])

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _write_manifest(self, version, files):
        payload = {
            "schema_version": version,
            "files": {path: {"sha256": "0" * 64} for path in files},
        }
        (self.workspace / "manifest.json").write_text(json.dumps(payload))

    def _write_callability(self, callable_value, include_row=True):
        value = "true" if callable_value else "false"
        predicate = "" if include_row else " WHERE false"
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'call-1'::VARCHAR AS callability_id,
                       NULL::VARCHAR AS variant_id,
                       NULL::VARCHAR AS gene_symbol,
                       'chr1'::VARCHAR AS chrom,
                       200::INTEGER AS pos,
                       false AS reference_observed,
                       %s AS callable,
                       'high'::VARCHAR AS call_confidence,
                       'site'::VARCHAR AS evidence_scope,
                       'synthetic'::VARCHAR AS assay_scope
                %s
            ) TO ? (FORMAT PARQUET)
            """ % (value, predicate),
            [str(self.workspace / "callability.parquet")],
        )
        connection.close()
        self._write_manifest(
            "1.1.0", ["variants.parquet", "callability.parquet"]
        )

    def _write_callable_region(self, callable_value):
        value = "true" if callable_value else "false"
        connection = duckdb.connect()
        connection.execute(
            """
            COPY (
                SELECT 'region-1'::VARCHAR AS region_id,
                       'chr1'::VARCHAR AS chrom,
                       150::INTEGER AS start_pos,
                       250::INTEGER AS end_pos,
                       %s AS callable,
                       20::INTEGER AS minimum_depth,
                       'synthetic'::VARCHAR AS assay_scope,
                       'synthetic interval'::VARCHAR AS derivation
            ) TO ? (FORMAT PARQUET)
            """ % value,
            [str(self.workspace / "callable_regions.parquet")],
        )
        connection.close()
        self._write_manifest(
            "1.1.0", ["variants.parquet", "callable_regions.parquet"]
        )

    def test_matching_variant_is_recorded(self):
        result = search_workspace(str(self.workspace), "rs100")

        self.assertEqual(result.answerability["state"], "recorded")
        self.assertEqual(result.answerability["basis"], "bundle_records")
        self.assertEqual(result.answerability["sections"], ["variants"])

    def test_callable_position_without_matching_alternate_is_explicit(self):
        self._write_callability(True)

        result = search_workspace(str(self.workspace), "chr1:200:A:T")

        self.assertEqual(
            result.answerability["state"],
            "callable_no_matching_alternate",
        )
        self.assertEqual(
            result.answerability["reason"],
            "callable_position_without_matching_variant",
        )
        self.assertTrue(result.answerability["callability"]["callable"])

    def test_not_callable_position_is_explicit(self):
        self._write_callability(False)

        result = search_workspace(str(self.workspace), "chr1:200")

        self.assertEqual(result.answerability["state"], "not_callable")
        self.assertFalse(result.answerability["callability"]["callable"])

    def test_callable_interval_can_answer_a_missing_position(self):
        self._write_callable_region(True)

        result = search_workspace(str(self.workspace), "chr1:200")

        self.assertEqual(
            result.answerability["state"],
            "callable_no_matching_alternate",
        )
        self.assertEqual(
            result.answerability["callability"]["source"],
            "callable_regions.parquet",
        )

    def test_missing_v11_callability_is_not_reported_as_a_negative_result(self):
        result = search_workspace(str(self.workspace), "chr1:200")

        self.assertEqual(result.answerability["state"], "analysis_not_included")
        self.assertEqual(
            result.answerability["reason"], "site_callability_not_included"
        )

    def test_empty_callability_table_leaves_the_position_unresolved(self):
        self._write_callability(True, include_row=False)

        result = search_workspace(str(self.workspace), "chr1:200")

        self.assertEqual(
            result.answerability["state"], "insufficient_bundle_data"
        )
        self.assertEqual(
            result.answerability["reason"], "no_site_level_callability_record"
        )

    def test_v10_bundle_cannot_interpret_a_missing_coordinate(self):
        self._write_manifest("1.0.0", ["variants.parquet"])

        result = search_workspace(str(self.workspace), "chr1:200")

        self.assertEqual(
            result.answerability["state"], "unsupported_bundle_version"
        )
        self.assertEqual(result.answerability["schema_version"], "1.0.0")

    def test_missing_rsid_without_offline_mapping_remains_unresolved(self):
        result = search_workspace(str(self.workspace), "rs999")

        self.assertEqual(
            result.answerability["state"], "insufficient_bundle_data"
        )
        self.assertEqual(
            result.answerability["reason"],
            "rsid_has_no_offline_coordinate_mapping",
        )


if __name__ == "__main__":
    unittest.main()
