"""Point d'entrée : python -m dilemme etape1 [--graine N] [--contre-soi]"""

import argparse

from .strategies import STRATEGIES_COURS, fabriques
from .tournoi import ConfigTournoi, formater_resultats, lancer_tournoi

POPULATIONS = {
    "etape1": STRATEGIES_COURS,
}


def main() -> None:
    p = argparse.ArgumentParser(description="Tournoi du dilemme du prisonnier itéré")
    p.add_argument("etape", choices=sorted(POPULATIONS))
    p.add_argument("--graine", type=int, default=42)
    p.add_argument("--parties", type=int, default=5)
    p.add_argument("--tours", type=int, default=200)
    p.add_argument("--contre-soi", action="store_true",
                   help="chaque stratégie joue aussi contre son double")
    p.add_argument("--bruit", type=float, default=0.0,
                   help="probabilité d'inverser chaque coup, ex. 0.05")
    args = p.parse_args()
    if not 0 <= args.bruit <= 1:
        p.error("--bruit doit être entre 0 et 1")

    config = ConfigTournoi(nb_parties=args.parties, nb_tours=args.tours,
                           graine=args.graine, contre_soi=args.contre_soi,
                           bruit=args.bruit)
    res = lancer_tournoi(fabriques(POPULATIONS[args.etape]), config)
    print(formater_resultats(res))


if __name__ == "__main__":
    main()
