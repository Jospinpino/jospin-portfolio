"""Tests unitaires pour l'analyseur de robustesse des mots de passe."""

import unittest

from checker import analyze, charset_size, has_repeated_run, has_sequence


class TestsAnalyse(unittest.TestCase):

    def test_mot_de_passe_vide(self):
        resultat = analyze("")
        self.assertEqual(resultat["score"], 0)
        self.assertEqual(resultat["label"], "Empty")

    def test_mot_de_passe_courant_score_zero(self):
        resultat = analyze("password1")
        self.assertEqual(resultat["score"], 0)
        self.assertIn(
            "This is one of the most common passwords in use, avoid it entirely.",
            resultat["issues"],
        )

    def test_mot_de_passe_court_signale(self):
        resultat = analyze("aB1!")
        self.assertIn("Shorter than 8 characters.", resultat["issues"])

    def test_absence_de_categories_de_caracteres(self):
        resultat = analyze("alllowercase")
        self.assertIn("No uppercase letters.", resultat["issues"])
        self.assertIn("No digits.", resultat["issues"])
        self.assertIn("No symbols.", resultat["issues"])

    def test_mot_de_passe_robuste_obtient_un_bon_score(self):
        resultat = analyze("Tr@ns!tGiraffe94Kite")
        self.assertGreaterEqual(resultat["score"], 5)
        self.assertEqual(resultat["issues"], [])

    def test_detection_de_sequence(self):
        self.assertTrue(has_sequence("myqwerty99"))
        self.assertFalse(has_sequence("Tr@ns!tGiraffe94"))

    def test_detection_de_caracteres_repetes(self):
        self.assertTrue(has_repeated_run("aaaa1234"))
        self.assertFalse(has_repeated_run("abab1234"))

    def test_mot_de_passe_avec_sequence_est_penalise(self):
        resultat = analyze("Abcdef1234!!")
        self.assertTrue(any("sequence" in probleme for probleme in resultat["issues"]))

    def test_calcul_taille_ensemble_caracteres(self):
        self.assertEqual(charset_size("abc"), 26)
        self.assertEqual(charset_size("ABC"), 26)
        self.assertEqual(charset_size("123"), 10)
        self.assertEqual(charset_size("!@#"), 33)
        self.assertEqual(charset_size("aB1!"), 26 + 26 + 10 + 33)
        self.assertEqual(charset_size(""), 1)


if __name__ == "__main__":
    unittest.main()
