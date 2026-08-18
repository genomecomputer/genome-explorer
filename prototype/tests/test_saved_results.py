import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from prototype.selective_reader.saved_results import SavedResultsStore


class SavedResultsStoreTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary_directory.name) / "saved-results.json"
        self.store = SavedResultsStore(self.path)
        self.bundle = {
            "bundle_id": "bundle-1",
            "nickname": "Synthetic sample",
            "schema_version": "1.1.0",
            "genome_build": "GRCh38",
            "generated_at": "2026-08-14T10:27:30+00:00",
        }
        self.record = {
            "section": "pharmacogenomics",
            "gene_symbol": "CYP2C19",
            "diplotype": "*1/*17",
            "phenotype": "Rapid Metabolizer",
            "affected_drugs": ["clopidogrel", "omeprazole"],
            "_record_key": "application-only",
        }

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_saves_deduplicates_removes_and_separates_bundles(self):
        first = self.store.add("bundle-1", "clopidogrel", self.record)
        duplicate = self.store.add("bundle-1", "CYP2C19", self.record)

        self.assertEqual(first["saved_id"], duplicate["saved_id"])
        self.assertEqual(len(self.store.entries("bundle-1")), 1)
        self.assertNotIn("_record_key", first["record"])
        self.assertEqual(self.store.entries("bundle-2"), [])

        reloaded = SavedResultsStore(self.path)
        self.assertEqual(reloaded.entries("bundle-1")[0]["record"], first["record"])
        self.assertTrue(reloaded.remove("bundle-1", first["saved_id"]))
        self.assertEqual(reloaded.entries("bundle-1"), [])
        self.assertFalse(reloaded.remove("bundle-1", first["saved_id"]))

    def test_exports_stable_json_and_csv_from_recorded_fields(self):
        saved = self.store.add("bundle-1", "clopidogrel", self.record)

        json_export = self.store.export("bundle-1", self.bundle, "json")
        self.assertEqual(json_export["file_name"], "synthetic-sample-saved-results.json")
        payload = json.loads(json_export["content"])
        self.assertEqual(payload["bundle"]["schema_version"], "1.1.0")
        self.assertEqual(payload["records"][0]["saved_id"], saved["saved_id"])
        self.assertEqual(payload["records"][0]["record"]["gene_symbol"], "CYP2C19")
        self.assertEqual(
            json_export["content"],
            self.store.export("bundle-1", self.bundle, "json")["content"],
        )

        csv_export = self.store.export("bundle-1", self.bundle, "csv")
        self.assertEqual(csv_export["file_name"], "synthetic-sample-saved-results.csv")
        rows = list(csv.DictReader(io.StringIO(csv_export["content"])))
        self.assertEqual(rows[0]["section"], "pharmacogenomics")
        self.assertEqual(rows[0]["record.gene_symbol"], "CYP2C19")
        self.assertEqual(
            rows[0]["record.affected_drugs"],
            '["clopidogrel","omeprazole"]',
        )

    def test_rejects_unsupported_sections(self):
        with self.assertRaisesRegex(ValueError, "unsupported record section"):
            self.store.add(
                "bundle-1",
                "anything",
                {"section": "generated_interpretation", "text": "not from bundle"},
            )

    def test_ignores_a_corrupt_local_store(self):
        self.path.write_text("[]", encoding="utf-8")

        self.assertEqual(self.store.entries("bundle-1"), [])


if __name__ == "__main__":
    unittest.main()
