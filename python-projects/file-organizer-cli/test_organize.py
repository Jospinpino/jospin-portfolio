"""Unit tests for the file organizer, using a temporary directory of dummy files."""

import tempfile
import unittest
from pathlib import Path

from organize import category_for, organize, unique_destination


class CategoryForTests(unittest.TestCase):
    def test_known_extensions(self):
        self.assertEqual(category_for(".jpg"), "Images")
        self.assertEqual(category_for(".PDF"), "Documents")
        self.assertEqual(category_for(".py"), "Code")

    def test_unknown_extension_is_others(self):
        self.assertEqual(category_for(".xyz"), "Others")


class OrganizeTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp_dir.name)
        (self.root / "photo.jpg").write_text("fake image")
        (self.root / "report.pdf").write_text("fake pdf")
        (self.root / "notes.txt").write_text("fake notes")
        (self.root / "script.py").write_text("print('hi')")
        (self.root / "mystery.xyz").write_text("unknown type")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_dry_run_does_not_move_files(self):
        moved, plan = organize(self.root, dry_run=True)
        self.assertEqual(len(plan), 5)
        self.assertTrue((self.root / "photo.jpg").exists())
        self.assertFalse((self.root / "Images").exists())

    def test_real_run_moves_files_into_categories(self):
        moved, plan = organize(self.root)
        self.assertTrue((self.root / "Images" / "photo.jpg").exists())
        self.assertTrue((self.root / "Documents" / "report.pdf").exists())
        self.assertTrue((self.root / "Documents" / "notes.txt").exists())
        self.assertTrue((self.root / "Code" / "script.py").exists())
        self.assertTrue((self.root / "Others" / "mystery.xyz").exists())
        self.assertFalse((self.root / "photo.jpg").exists())

    def test_skip_others_leaves_unknown_files_in_place(self):
        organize(self.root, include_others=False)
        self.assertTrue((self.root / "mystery.xyz").exists())
        self.assertFalse((self.root / "Others").exists())

    def test_running_twice_does_not_lose_or_overwrite_files(self):
        organize(self.root)
        (self.root / "photo.jpg").write_text("a second image")
        organize(self.root)
        self.assertTrue((self.root / "Images" / "photo.jpg").exists())
        self.assertTrue((self.root / "Images" / "photo (1).jpg").exists())

    def test_unique_destination_avoids_overwrite(self):
        existing = self.root / "file.txt"
        existing.write_text("original")
        result = unique_destination(existing)
        self.assertEqual(result.name, "file (1).txt")


if __name__ == "__main__":
    unittest.main()
