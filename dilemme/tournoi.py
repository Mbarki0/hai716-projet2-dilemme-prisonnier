"""Tournoi tous contre tous au format d'Axelrod."""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field

from .jeu import GAINS_DILEMME, jouer_partie


@dataclass
class ConfigTournoi:
    nb_parties: int = 5          # parties par paire de stratégies
    nb_tours: int = 200          # tours par partie
    graine: int = 42             # graine aléatoire globale
    contre_soi: bool = False     # chaque stratégie joue-t-elle contre son double ?
    bruit: float = 0.0           # probabilité d'inverser chaque coup (étape 3)
    gains: dict = field(default_factory=lambda: dict(GAINS_DILEMME))


@dataclass
class ResultatTournoi:
    config: ConfigTournoi
    noms: list[str]
    # scores[a][b] = total marqué par a contre b, sommé sur les parties
    scores: dict[str, dict[str, int]]

    def total(self, nom: str) -> int:
        return sum(self.scores[nom].values())

    def classement(self) -> list[tuple[str, int]]:
        return sorted(((n, self.total(n)) for n in self.noms),
                      key=lambda x: (-x[1], x[0]))


def lancer_tournoi(fabriques: dict, config: ConfigTournoi) -> ResultatTournoi:
    """`fabriques` : nom -> fonction sans argument qui crée une stratégie neuve.

    Chaque partie reçoit son propre générateur, dérivé de (graine, paire, n° de
    partie) : ajouter ou retirer une stratégie ne change pas les tirages des
    autres paires, et tout le tournoi se rejoue à l'identique.
    """
    noms = list(fabriques)
    scores = {a: {b: 0 for b in noms} for a in noms}

    paires = list(itertools.combinations(noms, 2))
    if config.contre_soi:
        paires += [(n, n) for n in noms]

    for a, b in paires:
        for k in range(config.nb_parties):
            rng = random.Random(f"{config.graine}|{a}|{b}|{k}")
            res = jouer_partie(fabriques[a](), fabriques[b](), config.nb_tours,
                               rng, config.gains, config.bruit)
            if a == b:
                # Contre son double : on ne compte qu'un des deux scores.
                scores[a][a] += res.score_a
            else:
                scores[a][b] += res.score_a
                scores[b][a] += res.score_b
    return ResultatTournoi(config, noms, scores)


def formater_resultats(res: ResultatTournoi) -> str:
    """Tableau texte : matrice des scores puis classement."""
    noms = res.noms
    larg = max(len(n) for n in noms) + 2
    lignes = []
    c = res.config
    lignes.append(f"Tournoi : {c.nb_parties} parties x {c.nb_tours} tours, "
                  f"graine={c.graine}, contre soi={c.contre_soi}, bruit={c.bruit}")
    lignes.append("")
    lignes.append("Score de la ligne contre la colonne (somme des parties)")
    lignes.append(" " * larg + "".join(n[:8].rjust(10) for n in noms))
    for a in noms:
        cells = "".join(
            ("-" if a == b and not c.contre_soi else str(res.scores[a][b])).rjust(10)
            for b in noms)
        lignes.append(a.ljust(larg) + cells)
    lignes.append("")
    lignes.append("Classement")
    nb_adv = len(noms) - (0 if c.contre_soi else 1)
    nb_tours_total = nb_adv * c.nb_parties * c.nb_tours
    for rang, (nom, total) in enumerate(res.classement(), 1):
        moy = total / nb_tours_total if nb_tours_total else 0
        lignes.append(f"{rang:>2}. {nom.ljust(larg)} {total:>7}   "
                      f"({moy:.3f} pt/tour)")
    return "\n".join(lignes)
