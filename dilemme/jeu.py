"""Moteur d'une partie de dilemme du prisonnier itéré entre deux stratégies."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

C, D = "C", "D"

# Matrice du cours : GAINS[(coup_i, coup_j)] = (gain_i, gain_j)
GAINS_DILEMME: dict[tuple[str, str], tuple[int, int]] = {
    (C, C): (3, 3),
    (C, D): (0, 5),
    (D, C): (5, 0),
    (D, D): (2, 2),
}


@dataclass
class ResultatPartie:
    """Trace complète d'une partie : coups joués et scores cumulés."""

    coups_a: list[str] = field(default_factory=list)
    coups_b: list[str] = field(default_factory=list)
    score_a: int = 0
    score_b: int = 0

    @property
    def nb_tours(self) -> int:
        return len(self.coups_a)


def jouer_partie(strat_a, strat_b, nb_tours: int, rng: random.Random,
                 gains: dict = GAINS_DILEMME) -> ResultatPartie:
    """Fait jouer `nb_tours` tours entre deux stratégies.

    Les deux joueurs choisissent simultanément : chacun ne reçoit que
    l'historique des tours précédents (le sien et celui de l'adversaire).
    `rng` est la seule source d'aléa de la partie, ce qui la rend rejouable.
    """
    strat_a.reinitialiser(random.Random(rng.random()))
    strat_b.reinitialiser(random.Random(rng.random()))
    res = ResultatPartie()
    for _ in range(nb_tours):
        # Copies : une stratégie ne peut pas modifier l'historique.
        coup_a = strat_a.jouer(list(res.coups_a), list(res.coups_b))
        coup_b = strat_b.jouer(list(res.coups_b), list(res.coups_a))
        if coup_a not in (C, D) or coup_b not in (C, D):
            raise ValueError(f"coup invalide : {coup_a!r} / {coup_b!r}")
        g_a, g_b = gains[(coup_a, coup_b)]
        res.coups_a.append(coup_a)
        res.coups_b.append(coup_b)
        res.score_a += g_a
        res.score_b += g_b
    return res
