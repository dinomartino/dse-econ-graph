"""Price fixed BELOW equilibrium; demand increases -> shortage grows.

Topic: Price fixed away from equilibrium
Use for: price stays fixed below equilibrium while demand rises (or supply falls), so
  the shortage grows from a to b (DSE2022 Q10(e), CE2003 Q1(a))

Marking-scheme points it shows:
  - fixed price (P) below the equilibrium price
  - rightward shift of demand D0 to D1 (arrow)
  - shortage at P: a (before) enlarges to b (after)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (94, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D0 = Line((14, 82), (62, 34))
    D1 = D0.shift(dx=14)
    S = Line((20, 22), (74, 76))
    draw(ax, D0, 21, D0.x(24), r"$D_0$", end="top")
    draw(ax, D1, 35, D1.x(24), r"$D_1$", end="top")
    draw(ax, S, 20, 74, "S", dy=1.5)

    P = 34                                     # fixed price, below equilibrium
    qs, q0, q1 = S.x(P), D0.x(P), D1.x(P)
    line(ax, (O[0], P), (90, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    for q, name in ((qs, r"$Q_s$"), (q0, r"$Q_{d0}$"), (q1, r"$Q_{d1}$")):
        dashed(ax, (q, O[1]), (q, P)); label(ax, q, O[1] - 1.8, name, va="top")
    brace(ax, qs, q0, P - 1, "a", side="below")
    brace(ax, qs, q1, P + 1, side="above")
    label(ax, (qs + q0) / 2 + 2, P + 1 + 2.5 + 3, "b")   # left of the tip: D0 crosses the tip

    # shift arrow D0 -> D1 on the upper part of the curves
    y = 62
    arrow(ax, (D0.x(y) + 2, y), (D1.x(y) - 2, y))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"03_demand_increase_fixed_price_{lang}.png"))
