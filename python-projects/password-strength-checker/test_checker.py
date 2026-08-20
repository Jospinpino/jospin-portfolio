"""Unit tests for the password strength analyzer."""

import unittest

from checker import analyze, has_repeated_run, has_sequence


class AnalyzeTests(unittest.TestCase):
    def test_empty_password(self):
        result = analyze("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["label"], "Empty")

    def test_common_password_scores_zero(self):
        result = analyze("password1")
        self.assertEqual(result["score"], 0)
        self.assertIn(
            "This is one of the most common passwords in use, avoid it entirely.",
            result["issues"],
        )

    def test_short_password_flagged(self):
        result = analyze("aB1!")
        self.assertIn("Shorter than 8 characters.", result["issues"])

    def test_missing_character_classes_flagged(self):
        result = analyze("alllowercase")
        self.assertIn("No uppercase letters.", result["issues"])
        self.assertIn("No digits.", result["issues"])
        self.assertIn("No symbols.", result["issues"])

    def test_strong_password_scores_high(self):
        result = analyze("Tr@ns!tGiraffe94Kite")
        self.assertGreaterEqual(result["score"], 5)
        self.assertEqual(result["issues"], [])

    def test_sequence_detected(self):
        self.assertTrue(has_sequence("myqwerty99"))
        self.assertFalse(has_sequence("Tr@ns!tGiraffe94"))

    def test_repeated_run_detected(self):
        self.assertTrue(has_repeated_run("aaaa1234"))
        self.assertFalse(has_repeated_run("abab1234"))

    def test_sequence_password_is_penalized(self):
        result = analyze("Abcdef1234!!")
        self.assertTrue(any("sequence" in issue for issue in result["issues"]))


if __name__ == "__main__":
    unittest.main()
