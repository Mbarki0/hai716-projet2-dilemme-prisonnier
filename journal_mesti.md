# Journal de bord

## Informations générales

- Module : HAI716
- Projet : tournoi du dilemme du prisonnier itéré
- Auteur : Mohamed Mesti
- Langage envisagé : Python
- Date de début : 13 novembre 2026

---

## 1. Protocole

| Paramètre | Valeur | Raison du choix |
|---|---|---|
| Tours par partie | 200 | format d'Axelrod du cours |
| Parties par paire | 5 | format d'Axelrod du cours |
| Gains (CC, CD, DC, DD) | (3,3), (0,5), (5,0), (2,2) | matrice imposée par l'énoncé |
| Graine | 42 | fixée pour rejouer le tournoi à l'identique |
| Contre son double | non (par défaut) | l'énoncé dit « chaque stratégie affronte chaque autre » ; testé aussi avec `--contre-soi` |
| Modifications (étape 3) | bruit 5 % (moi) + sélection (M’BARKI) | regarde ce que les trahisons de JOSS font à TFT |

Reproductibilité : chaque partie a son propre générateur aléatoire, dérivé de
(graine, paire de stratégies, numéro de partie). Ajouter une stratégie ne
change donc pas les tirages des autres paires.

---

## 2. Stratégies

### Population de base (cours 4)

| Stratégie | Règle | Origine | Devrait bien jouer contre | Devrait mal jouer contre |
|---|---|---|---|---|
| ALL-D | toujours D | stratégie « rationnelle » par récurrence à rebours | les naïfs, RANDOM | elle-même, TFT (gain 2 au lieu de 3) |
| RANDOM | C ou D à 50 % | témoin | _à compléter_ | _à compléter_ |
| TIT-FOR-TAT | C au tour 1, puis copie le dernier coup adverse | Rapoport, vainqueur d'Axelrod 1980 | _à compléter_ | _à compléter_ |
| TESTER | D au tour 1 ; si l'adversaire riposte → TFT, sinon cycle C, C, D | cours 4 | _à compléter_ | _à compléter_ |
| JOSS | TFT, mais remplace C par D une fois sur dix | cours 4 | _à compléter_ | _à compléter_ |

**Choix d'interprétation pour TESTER** : le cours ne dit pas quand on vérifie
la riposte. J'ai retenu : dès que l'adversaire joue D une fois, TESTER passe
définitivement en TIT-FOR-TAT ; sinon il enchaîne C, C, D à partir du tour 2.

### Nouvelles stratégies (étape 2)

_à compléter_

---

## 3. Étape 1 — tournoi de base

Commande : `python -m dilemme etape1`

Sortie (graine 42, fichier `resultats/etape1.txt`) :

```
Score de la ligne contre la colonne (somme des parties)
                  ALL-D    RANDOM  TIT-FOR-    TESTER      JOSS
ALL-D                 -      3527      2015      2000      2012
RANDOM              982         -      2516      2464      2338
TIT-FOR-TAT        1990      2506         -      2500      2088
TESTER             2000      2474      2500         -      2017
JOSS               1992      2583      2113      2017         -

Classement
 1. ALL-D            9554   (2.389 pt/tour)
 2. TIT-FOR-TAT      9084   (2.271 pt/tour)
 3. TESTER           8991   (2.248 pt/tour)
 4. JOSS             8705   (2.176 pt/tour)
 5. RANDOM           8300   (2.075 pt/tour)
```

Avec les graines 1, 2 et 3 : ALL-D reste 1er, TESTER et TFT s'échangent les places 2 et 3.

Variante `--contre-soi` (fichier `resultats/etape1_contre_soi.txt`) :
TIT-FOR-TAT passe 1er (12084) devant ALL-D (11554).
Matchs contre son double : TFT/TFT = 3000, ALL-D/ALL-D = 2000,
TESTER/TESTER = 2000, JOSS/JOSS = 2037, RANDOM/RANDOM = 2574.

Tests unitaires : `python -m unittest -v` → 7 tests OK.

![Classement étape 1](captures/etape1.png)

### Question : TIT-FOR-TAT gagne-t-il ?

Non. Le classement montre que ALL-D est le gagnant (9554 points) et que TFT
est au 2e rang (9084 points).

ALL-D marque le plus contre RANDOM (3527 points, environ 3,5 points par tour).

TFT ne coopère pas vraiment avec TESTER et JOSS : 2500 et 2088 points, soit
moins de 3 points par tour.

Quand chaque stratégie joue aussi contre elle-même (`--contre-soi`), TFT
gagne : TFT contre TFT = 3000, ALL-D contre ALL-D = 2000, donc TFT passe à
12084 et ALL-D à 11554.

---

## 4. Étape 2 — nouvelles stratégies

Partie réalisée par Mohammed M'BARKI (voir son journal et sa branche `mbarki`).

---

## 5. Étape 3 — modifications du tournoi

Pour chaque modification : prédiction écrite **avant** de lancer, puis résultat, puis explication de l'écart.

### Modification 1 : _…_

- Justification du choix :
- Prédiction (avant exécution) :
- Résultat :
- Écart et explication :

### Modification 2 : _…_

- Justification du choix :
- Prédiction (avant exécution) :
- Résultat :
- Écart et explication :

---

## 6. Impasses

- La découverte des tests (`python -m unittest discover -s tests`) échouait :
  le dossier `tests` n'était pas un paquet. Ajout de `tests/__init__.py`.
