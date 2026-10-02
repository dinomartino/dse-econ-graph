"""Demand decreases -> price and quantity fall.

Topic: Demand and supply: shifts
Use for: demand falls (fewer buyers, lower income, a cheaper substitute ...) and
  the question asks the effect on price and quantity
  (CE2000 Q9(b)(i), DSE2012 Q12(c)(i), CE1993 Q4(b)(ii))

Marking-scheme points it shows:
  - leftward shift of demand D1 -> D2 (arrow), S unchanged
  - new equilibrium E2: price falls P1 -> P2, quantity falls Q1 -> Q2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    S = Line((20, 18), (80, 78))
    D1 = Line((40, 82), (84, 24))
    D2 = D1.shift(dx=-26)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D1, 40, 84, r"$D_1$", dy=-1.5)
    draw(ax, D2, 16, 50, r"$D_2$", dy=-1.5)
    y = 70
    arrow(ax, (D1.x(y) - 2, y), (D2.x(y) + 2, y))

    (q1, p1), (q2, p2) = E1, E2 = meet(D1, S), meet(D2, S)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"12_demand_decrease_{lang}.png"))
