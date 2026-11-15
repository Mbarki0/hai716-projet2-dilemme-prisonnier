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
    continuation: float | None = None  # probabilité w de continuer la partie
    gains: dict = field(default_factory=lambda: dict(GAINS_DILEMME))


@dataclass
class ResultatTournoi:
    config: ConfigTournoi
    noms: list[str]
    # scores[a][b] = total marqué par a contre b, sommé sur les parties
    scores: dict[str, dict[str, int]]
    # tours[a][b] = nombre de tours joués par a contre b
    tours: dict[str, dict[str, int]]

    def total(self, nom: str) -> int:
        return sum(self.scores[nom].values())

    def total_tours(self, nom: str) -> int:
        return sum(self.tours[nom].values())

    def moyenne(self, nom: str) -> float:
        total_tours = self.total_tours(nom)
        return self.total(nom) / total_tours if total_tours else 0.0

    def classement(self) -> list[tuple[str, int]]:
        return sorted(((n, self.total(n)) for n in self.noms),
                      key=lambda x: (-self.moyenne(x[0]), -x[1], x[0]))


def lancer_tournoi(fabriques: dict, config: ConfigTournoi) -> ResultatTournoi:
    """`fabriques` : nom -> fonction sans argument qui crée une stratégie neuve.

    Chaque partie reçoit son propre générateur, dérivé de (graine, paire, n° de
    partie) : ajouter ou retirer une stratégie ne change pas les tirages des
    autres paires, et tout le tournoi se rejoue à l'identique.
    """
    noms = list(fabriques)
    scores = {a: {b: 0 for b in noms} for a in noms}
    tours = {a: {b: 0 for b in noms} for a in noms}

    paires = list(itertools.combinations(noms, 2))
    if config.contre_soi:
        paires += [(n, n) for n in noms]

    for a, b in paires:
        for k in range(config.nb_parties):
            rng = random.Random(f"{config.graine}|{a}|{b}|{k}")
            res = jouer_partie(fabriques[a](), fabriques[b](), config.nb_tours,
                               rng, gains=config.gains, bruit=config.bruit,
                               continuation=config.continuation)
            if a == b:
                # Contre son double : on ne compte qu'un des deux scores.
                scores[a][a] += res.score_a
                tours[a][a] += res.nb_tours
            else:
                scores[a][b] += res.score_a
                scores[b][a] += res.score_b
                tours[a][b] += res.nb_tours
                tours[b][a] += res.nb_tours
    return ResultatTournoi(config, noms, scores, tours)


def formater_resultats(res: ResultatTournoi) -> str:
    """Tableau texte : matrice des scores puis classement."""
    noms = res.noms
    larg = max(len(n) for n in noms) + 2
    lignes = []
    c = res.config
    if c.continuation is None:
        horizon = f"{c.nb_parties} parties x {c.nb_tours} tours"
    else:
        horizon = (f"{c.nb_parties} parties, horizon inconnu "
                   f"w={c.continuation}")
    lignes.append(f"Tournoi : {horizon}, graine={c.graine}, "
                  f"contre soi={c.contre_soi}, bruit={c.bruit}")
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
    for rang, (nom, total) in enumerate(res.classement(), 1):
        moy = res.moyenne(nom)
        if c.continuation is None:
            detail = f"{moy:.3f} pt/tour"
        else:
            detail = f"{moy:.3f} pt/tour, {res.total_tours(nom)} tours"
        lignes.append(f"{rang:>2}. {nom.ljust(larg)} {total:>7}   ({detail})")
    return "\n".join(lignes)
