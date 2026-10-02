"""Price set BELOW equilibrium (price ceiling / fixed low price) -> shortage.

Topic: Price fixed away from equilibrium
Use for: a price ceiling / fixed price BELOW equilibrium causes a shortage
  (CE1991 Q4(c)(i))

Marking-scheme points it shows:
  - price (P) below the equilibrium price (Pe)
  - correct position of the shortage / excess demand (Qs to Qd at P)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$P_e$", to_x=False)

    P = 34                                     # the fixed price, below Pe
    qs, qd = S.x(P), D.x(P)
    line(ax, (O[0], P), (84, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    dashed(ax, (qs, O[1]), (qs, P)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, qs, qd, P - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"01_price_ceiling_shortage_{lang}.png"))
