"""Perfectly inelastic (vertical) supply, price set BELOW equilibrium -> shortage.

Marking-scheme points it shows:
  - vertical supply at fixed quantity Q0
  - controlled price (P) below the equilibrium price (Pe)
  - shortage / excess demand from Q0 to Qd at P
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 84), (82, 24))
    S = Line.vertical(46)
    draw(ax, D, 18, 82, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=82, end="top")

    E = meet(S, D)
    dot(ax, *E)
    guide(ax, E, O, r"$P_e$", r"$Q_0$")

    P = 32                                     # controlled price, below Pe
    qd = D.x(P)
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, S.vx, qd, P - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"04_vertical_supply_shortage_{lang}.png"))
