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

Étape 2 — tournoi avec GRIM et PAVLOV :

```
python -m dilemme etape2
```

Options générales : `--graine N`, `--parties N`, `--tours N`,
`--contre-soi` (chaque stratégie joue aussi contre son double) et
`--bruit P` (probabilité d'inverser chaque coup).

Étape 3 — bruit (chaque coup inversé avec une probabilité de 5 %) :

```
python -m dilemme etape1 --bruit 0.05
```

Étape 3 — horizon inconnu (durée moyenne de 200 tours) :

```
python -m dilemme etape2 --continuation 0.995
```

L'option `--continuation W` remplace la durée fixe par une probabilité `W`
de poursuivre la partie après chaque tour. Le classement est alors établi
sur la moyenne de points par tour.

## Tests

```
python -m unittest -v
```
