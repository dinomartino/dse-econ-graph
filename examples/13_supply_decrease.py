"""Supply decreases -> price rises, quantity falls.

Topic: Demand and supply: shifts
Use for: supply falls (higher production cost, a unit tax, a higher tariff on
  imports, bad weather ...) and the question asks the effect on price and quantity;
  a demand increase or a supply increase is drawn the same way with the arrow reversed
  (CE1992 Q2(b)(i), CE1994 Q9(b)(i))

Marking-scheme points it shows:
  - leftward shift of supply S -> S' (arrow), D unchanged
  - new equilibrium E2: price rises P1 -> P2, quantity falls Q1 -> Q2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 78), (84, 22))
    S1 = Line((36, 18), (82, 78))
    S2 = S1.shift(dx=-22)
    draw(ax, D, 18, 84, "D", dy=-1.5)
    draw(ax, S1, 36, 82, "S", end="top")
    draw(ax, S2, 18, 60, "S’", end="top")
    y = 72
    arrow(ax, (S1.x(y) - 2, y), (S2.x(y) + 2, y))

    (q1, p1), (q2, p2) = E1, E2 = meet(D, S1), meet(D, S2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"13_supply_decrease_{lang}.png"))
