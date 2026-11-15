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

Le classement de l'étape 2 n'a pas encore été lancé au moment où ces attentes
sont écrites.

## 4. Prochaine étape

Commiter les deux stratégies et leurs tests, puis seulement après lancer le
tournoi élargi et comparer son classement à celui de l'étape 1.
