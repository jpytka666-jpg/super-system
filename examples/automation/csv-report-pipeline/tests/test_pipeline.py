"""Tests for the CSV report pipeline. Run: python -m unittest discover -s tests"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import pipeline  # noqa: E402
import validate  # noqa: E402


class PipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp())
        (self.base / "input").mkdir()
        for src in (HERE / "sample_data").glob("*.csv"):
            shutil.copy(src, self.base / "input" / src.name)

    def tearDown(self) -> None:
        shutil.rmtree(self.base)

    def test_dedupe_counts(self) -> None:
        result = pipeline.run_once(self.base)
        by_name = {f.name: f for f in result.files}
        jan, feb, inv = by_name["sales_jan.csv"], by_name["sales_feb.csv"], by_name["inventory.csv"]
        # files run in name order: sales_feb < sales_jan, so feb keeps the shared Gizmo row
        self.assertEqual((feb.rows_in, feb.rows_out, feb.duplicates_in_file), (4, 3, 1))
        self.assertEqual((jan.rows_in, jan.rows_out, jan.duplicates_in_file,
                          jan.duplicates_cross_file), (6, 3, 2, 1))
        self.assertEqual((inv.rows_in, inv.rows_out, inv.duplicates_in_file), (3, 2, 1))
        self.assertEqual((result.total_in, result.total_out), (13, 8))

    def test_validator_passes_and_originals_archived(self) -> None:
        result = pipeline.run_once(self.base)
        self.assertEqual(validate.check(self.base), [])
        archived = list((self.base / "input" / "processed" / result.run_id).glob("*.csv"))
        self.assertEqual(len(archived), 3)
        self.assertEqual(list((self.base / "input").glob("*.csv")), [])

    def test_validator_detects_tampering(self) -> None:
        pipeline.run_once(self.base)
        clean = self.base / "output" / "clean" / "inventory_clean.csv"
        clean.write_text(clean.read_text() + "W-1,A,10\n")
        problems = validate.check(self.base)
        self.assertTrue(any("checksum mismatch" in p for p in problems))

    def test_idle_when_no_input(self) -> None:
        for p in (self.base / "input").glob("*.csv"):
            p.unlink()
        self.assertIsNone(pipeline.run_once(self.base))

    def test_symlink_skipped(self) -> None:
        (self.base / "input" / "link.csv").symlink_to(HERE / "sample_data" / "inventory.csv")
        result = pipeline.run_once(self.base)
        self.assertTrue(any(s.startswith("link.csv") for s in result.skipped))
        self.assertTrue((HERE / "sample_data" / "inventory.csv").exists())

    def test_watch_iterations_capped(self) -> None:
        pipeline.main(["--base", str(self.base), "--watch", "--interval", "0",
                       "--iterations", "999"])
        # 1 processing run + idle polls; cap means exactly one manifest and no hang
        self.assertEqual(len(list((self.base / "output" / "reports").glob("manifest_*.json"))), 1)


if __name__ == "__main__":
    unittest.main()
