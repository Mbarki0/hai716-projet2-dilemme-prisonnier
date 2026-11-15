# Journal de bord

## Informations générales

- Module : HAI716
- Projet : tournoi du dilemme du prisonnier itéré
- Auteur : Mohammed M'BARKI
- Langage envisagé : Python
- Date de début : 13 novembre 2026

---

## 1. Protocole

| Paramètre | Valeur | Justification |
|---|---|---|
| Tours par partie | 200 | format imposé par l'énoncé |
| Parties par paire | 5 | format imposé par l'énoncé |
| Gains CC, CD, DC, DD | (3,3), (0,5), (5,0), (2,2) | matrice du cours |
| Graine | 42 | obtenir des résultats reproductibles |
| Contre son double | non par défaut | l'énoncé demande d'affronter chaque autre stratégie |
| Modifications | bruit 5 % et horizon inconnu | bruit réalisé par MESTI ; horizon inconnu pour ma partie |

Le moteur, les stratégies du cours et le tournoi ont été développés par
MESTI. J'ai récupéré cette base, relu les fichiers et relancé les tests : les
9 tests présents passent. J'ai aussi reproduit les classements sans bruit et
avec un bruit de 5 %.

## 2. Compréhension de la population de base

| Stratégie | Règle |
|---|---|
| ALL-D | joue toujours D |
| RANDOM | choisit C ou D avec la même probabilité |
| TIT-FOR-TAT | commence par C puis copie le dernier coup adverse |
| TESTER | commence par D ; passe à TIT-FOR-TAT si l'adversaire riposte, sinon répète C, C, D |
| JOSS | suit TIT-FOR-TAT, mais remplace parfois C par D avec une probabilité de 10 % |

Avec la population de base et sans confrontation contre soi, ALL-D termine
premier et TIT-FOR-TAT deuxième. Ce résultat diffère du tournoi historique
d'Axelrod parce que la population est ici très petite et contient peu de
stratégies capables de maintenir une coopération durable.

## 3. Étape 2 - nouvelles stratégies

### GRIM

GRIM commence par coopérer. Elle continue tant que l'adversaire n'a jamais
trahi. Dès qu'un D apparaît dans l'historique adverse, elle joue D jusqu'à la
fin de la partie. C'est une stratégie de déclenchement classique des jeux
répétés, souvent associée aux travaux de James Friedman sur les superjeux
(1971).

Source : https://doi.org/10.2307/2296617

Attentes avant le tournoi :

- elle devrait coopérer parfaitement avec TIT-FOR-TAT et avec elle-même ;
- elle devrait limiter rapidement les gains d'ALL-D après avoir subi une
  première exploitation ;
- elle devrait mal réagir aux trahisons occasionnelles de JOSS, car elle ne
  pardonne jamais.

### PAVLOV

PAVLOV, ou Win-Stay Lose-Shift, commence par C. Après CC ou DD, elle joue C ;
après CD ou DC, elle joue D. Elle peut donc retrouver la coopération après
une trahison mutuelle. Nowak et Sigmund ont étudié cette stratégie dans le
dilemme du prisonnier en 1993.

Source : https://doi.org/10.1038/364056a0

Attentes avant le tournoi :

- elle devrait coopérer durablement avec TIT-FOR-TAT et avec elle-même ;
- elle devrait mieux récupérer que TIT-FOR-TAT après une séquence DD ;
- elle devrait être exploitée par ALL-D pendant un tour sur deux, car elle
  revient à C après chaque DD ;
- son comportement contre RANDOM devrait être irrégulier.

Le classement de l'étape 2 n'avait pas encore été lancé au moment où ces
attentes ont été écrites et commitées.

### Résultats du tournoi élargi

Commande : `python -m dilemme etape2`

| Rang | Stratégie | Score | Moyenne par tour |
|---:|---|---:|---:|
| 1 | GRIM | 15645 | 2,607 |
| 2 | TIT-FOR-TAT | 15084 | 2,514 |
| 3 | ALL-D | 15069 | 2,511 |
| 4 | PAVLOV | 14205 | 2,368 |
| 5 | TESTER | 13331 | 2,222 |
| 6 | JOSS | 13284 | 2,214 |
| 7 | RANDOM | 11796 | 1,966 |

La sortie complète est conservée dans `resultats/etape2.txt`.

![Classement de l'étape 2](captures/etape2.png)

### Comparaison avec l'étape 1

Dans la population de base, ALL-D était première et TIT-FOR-TAT deuxième.
Après l'ajout de GRIM et PAVLOV, GRIM termine première, TIT-FOR-TAT reste
deuxième et ALL-D descend à la troisième place. Les scores totaux des deux
tournois ne sont pas directement comparables, car chaque stratégie rencontre
deux adversaires supplémentaires à l'étape 2. Les rangs et les moyennes par
tour sont donc plus utiles pour l'analyse.

GRIM obtient 3000 points contre TIT-FOR-TAT et 3000 contre PAVLOV : les trois
stratégies maintiennent la coopération pendant les cinq parties. Contre
ALL-D, GRIM marque 1990 points et ALL-D 2015. Elle subit la première trahison,
puis répond par D jusqu'à la fin, ce qui limite l'exploitation. Contre JOSS,
GRIM ne marque que 2133 points : une trahison occasionnelle de JOSS suffit à
déclencher une punition définitive. Ces observations correspondent aux
attentes écrites avant le tournoi.

PAVLOV coopère parfaitement avec TIT-FOR-TAT et GRIM, avec 3000 points dans
chaque confrontation. En revanche, elle ne marque que 1000 points contre
ALL-D, qui en obtient 3500. Leur partie alterne entre CD et DD : après DD,
PAVLOV revient à C et se fait de nouveau exploiter. Cette faiblesse explique
sa quatrième place malgré ses bonnes coopérations.

L'arrivée de deux stratégies coopératives profite également à TIT-FOR-TAT,
qui obtient 3000 points contre chacune. Le passage d'ALL-D de la première à
la troisième place confirme que le vainqueur dépend fortement de la
population du tournoi.

Les 11 tests passent après l'ajout des deux stratégies.

## 4. Prochaine étape

Écrire et commiter la prédiction concernant l'horizon inconnu avant de
modifier le moteur ou de lancer cette expérience.
