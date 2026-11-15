"""Stratégies du dilemme du prisonnier itéré.

Interface : une stratégie est un objet avec
  - reinitialiser(rng) : appelé au début de chaque partie ;
  - jouer(mes_coups, coups_adv) -> "C" ou "D".
Tout l'aléa passe par self.rng pour que les tournois soient rejouables.
"""

from __future__ import annotations

import random

from .jeu import C, D


class Strategie:
    nom = "?"

    def __init__(self):
        self.rng = random.Random(0)

    def reinitialiser(self, rng: random.Random) -> None:
        self.rng = rng

    def jouer(self, mes_coups: list[str], coups_adv: list[str]) -> str:
        raise NotImplementedError


# --- Stratégies du cours (CM4, tournoi d'Axelrod) ---------------------------

class AllD(Strategie):
    """Toujours D."""
    nom = "ALL-D"

    def jouer(self, mes_coups, coups_adv):
        return D


class Random(Strategie):
    """C ou D au hasard, une chance sur deux (témoin)."""
    nom = "RANDOM"

    def jouer(self, mes_coups, coups_adv):
        return C if self.rng.random() < 0.5 else D


class TitForTat(Strategie):
    """C au premier tour, puis rejoue le coup précédent de l'adversaire."""
    nom = "TIT-FOR-TAT"

    def jouer(self, mes_coups, coups_adv):
        return coups_adv[-1] if coups_adv else C


class Joss(Strategie):
    """TIT-FOR-TAT, mais remplace C par D une fois sur dix."""
    nom = "JOSS"

    def jouer(self, mes_coups, coups_adv):
        coup = coups_adv[-1] if coups_adv else C
        if coup == C and self.rng.random() < 0.1:
            return D
        return coup


class Tester(Strategie):
    """D au premier tour. Si l'adversaire riposte, joue TIT-FOR-TAT ;
    sinon répète C, C, D.

    Interprétation retenue (le cours ne précise pas) : la riposte ne peut se
    voir qu'au tour 2 ou après. Dès que l'adversaire a joué D une fois, TESTER
    bascule définitivement en TIT-FOR-TAT. Tant que ce n'est pas le cas, il
    enchaîne le cycle C, C, D à partir du tour 2.
    """
    nom = "TESTER"

    def reinitialiser(self, rng):
        super().reinitialiser(rng)
        self.mode_tft = False

    def jouer(self, mes_coups, coups_adv):
        t = len(mes_coups)          # numéro du tour courant, à partir de 0
        if t == 0:
            return D
        if D in coups_adv:
            self.mode_tft = True
        if self.mode_tft:
            return coups_adv[-1]
        return (C, C, D)[(t - 1) % 3]


STRATEGIES_COURS = [AllD, Random, TitForTat, Tester, Joss]


def fabriques(classes) -> dict:
    """nom -> constructeur, pour lancer_tournoi."""
    return {cls.nom: cls for cls in classes}
