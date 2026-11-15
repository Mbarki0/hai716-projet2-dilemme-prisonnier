import random
import unittest

from dilemme.jeu import C, D, jouer_partie
from dilemme.strategies import (STRATEGIES_COURS, AllD, Grim, Joss, Pavlov,
                                Tester, TitForTat, fabriques)
from dilemme.tournoi import ConfigTournoi, ResultatTournoi, lancer_tournoi


def partie(a, b, n=10, graine=0):
    return jouer_partie(a(), b(), n, random.Random(graine))


class TestPartie(unittest.TestCase):
    def test_tft_contre_alld_exemple_du_cours(self):
        # Cours : sur 10 tours, TFT fait 18 et ALL-D 23.
        r = partie(TitForTat, AllD)
        self.assertEqual(r.coups_a, [C] + [D] * 9)
        self.assertEqual((r.score_a, r.score_b), (18, 23))

    def test_tft_contre_tft_coopere(self):
        r = partie(TitForTat, TitForTat)
        self.assertEqual((r.score_a, r.score_b), (30, 30))

    def test_tester_exploite_un_naif(self):
        class AllC(TitForTat):
            def jouer(self, m, a):
                return C
        r = partie(Tester, AllC, n=7)
        self.assertEqual("".join(r.coups_a), "DCCDCCD")

    def test_tester_passe_en_tft_si_riposte(self):
        r = partie(Tester, TitForTat, n=6)
        # T1 : D/C, T2 : C/D (riposte) -> TESTER copie l'adversaire ensuite
        self.assertEqual("".join(r.coups_a), "DCDCDC")

    def test_joss_trahit_environ_une_fois_sur_dix(self):
        j = Joss()
        j.reinitialiser(random.Random(1))
        n = sum(j.jouer([], [C]) == D for _ in range(10000))
        self.assertTrue(900 < n < 1100)


class TestNouvellesStrategies(unittest.TestCase):
    def test_grim_ne_pardonne_pas_une_trahison(self):
        grim = Grim()
        self.assertEqual(grim.jouer([], []), C)
        self.assertEqual(grim.jouer([C, C], [C, C]), C)
        self.assertEqual(grim.jouer([C, C], [C, D]), D)
        self.assertEqual(grim.jouer([C, C, D], [C, D, C]), D)

    def test_pavlov_applique_win_stay_lose_shift(self):
        pavlov = Pavlov()
        self.assertEqual(pavlov.jouer([], []), C)
        self.assertEqual(pavlov.jouer([C], [C]), C)
        self.assertEqual(pavlov.jouer([C], [D]), D)
        self.assertEqual(pavlov.jouer([D], [C]), D)
        self.assertEqual(pavlov.jouer([D], [D]), C)


class TestBruit(unittest.TestCase):
    def test_bruit_inverse_environ_5_pourcent(self):
        r = jouer_partie(AllD(), AllD(), 20000, random.Random(3), bruit=0.05)
        n = r.coups_a.count(C)
        self.assertTrue(800 < n < 1200)

    def test_bruit_nul_ne_change_rien(self):
        # Les résultats de l'étape 1 (graine 42) ne doivent pas bouger.
        res = lancer_tournoi(fabriques(STRATEGIES_COURS), ConfigTournoi())
        self.assertEqual(res.total("ALL-D"), 9554)
        self.assertEqual(res.total("TIT-FOR-TAT"), 9084)


class TestTournoi(unittest.TestCase):
    def test_reproductible(self):
        cfg = ConfigTournoi(graine=7)
        r1 = lancer_tournoi(fabriques(STRATEGIES_COURS), cfg)
        r2 = lancer_tournoi(fabriques(STRATEGIES_COURS), cfg)
        self.assertEqual(r1.scores, r2.scores)

    def test_graine_change_resultat(self):
        r1 = lancer_tournoi(fabriques(STRATEGIES_COURS), ConfigTournoi(graine=1))
        r2 = lancer_tournoi(fabriques(STRATEGIES_COURS), ConfigTournoi(graine=2))
        self.assertNotEqual(r1.scores, r2.scores)


class TestHorizonInconnu(unittest.TestCase):
    def test_continuation_zero_arrete_apres_un_tour(self):
        r = jouer_partie(AllD(), AllD(), 200, random.Random(0),
                         continuation=0.0)
        self.assertEqual(r.nb_tours, 1)
        self.assertEqual((r.score_a, r.score_b), (2, 2))

    def test_probability_de_continuation_invalide(self):
        with self.assertRaisesRegex(ValueError, "continuation"):
            jouer_partie(AllD(), AllD(), 200, random.Random(0),
                         continuation=1.0)

    def test_horizon_inconnu_reproductible(self):
        cfg = ConfigTournoi(graine=7, continuation=0.9)
        r1 = lancer_tournoi(fabriques(STRATEGIES_COURS), cfg)
        r2 = lancer_tournoi(fabriques(STRATEGIES_COURS), cfg)
        self.assertEqual(r1.scores, r2.scores)
        self.assertEqual(r1.tours, r2.tours)

    def test_classement_utilise_la_moyenne_par_tour(self):
        cfg = ConfigTournoi(continuation=0.5)
        resultat = ResultatTournoi(
            config=cfg,
            noms=["A", "B"],
            scores={"A": {"A": 0, "B": 100},
                    "B": {"A": 30, "B": 0}},
            tours={"A": {"A": 0, "B": 100},
                   "B": {"A": 10, "B": 0}},
        )
        self.assertEqual(resultat.classement()[0][0], "B")


if __name__ == "__main__":
    unittest.main()
