# HAI716 — Projet 2

Tournoi du dilemme du prisonnier itéré.

## Auteurs

Mohammed M'BARKI — journal : [journal_mbarki.md](journal_mbarki.md)
Mohamed MESTI — journal : [journal_mesti.md](journal_mesti.md)

## Objectif

Construire un moteur de tournoi permettant de faire s'affronter différentes
stratégies du dilemme du prisonnier itéré, puis étudier l'effet de nouvelles
stratégies et de modifications du protocole expérimental.

## Organisation du code

```
dilemme/
  jeu.py         matrice des gains et moteur d'une partie
  strategies.py  stratégies (interface reinitialiser / jouer)
  tournoi.py     tournoi tous contre tous, classement, affichage
  __main__.py    ligne de commande
tests/           tests unitaires
resultats/       sorties des tournois
```

Python 3.10+ , aucune dépendance externe.

## Exécution

Étape 1 — tournoi de base (5 parties de 200 tours, graine 42) :

```
python -m dilemme etape1
```

Options : `--graine N`, `--parties N`, `--tours N`, `--contre-soi`
(chaque stratégie joue aussi contre son double).

Étape 3 — bruit (chaque coup inversé avec une probabilité de 5 %) :

```
python -m dilemme etape1 --bruit 0.05
```

## Tests

```
python -m unittest -v
```
