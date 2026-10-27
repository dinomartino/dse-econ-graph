"""Demand increases -> price and quantity rise.

Topic: Demand and supply: shifts
Use for: demand rises (more buyers, higher income for a normal good, a dearer
  substitute ...) and the question asks the effect on price and quantity
  (chat-only variant; same layout as 12 with the shift reversed)

Variant of: 12_demand_decrease

Marking-scheme points it shows:
  - rightward shift of demand D1 -> D2 (arrow), S unchanged
  - new equilibrium E2: price rises P1 -> P2, quantity rises Q1 -> Q2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    S = Line((20, 18), (80, 78))
    D1 = Line((16, 82), (60, 24))
    D2 = D1.shift(dx=26)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D1, 16, 53, r"$D_1$", dy=-1.5)
    draw(ax, D2, 40, 84, r"$D_2$", dy=-1.5)
    y = 70
    arrow(ax, (D1.x(y) + 2, y), (D2.x(y) - 2, y))

    (q1, p1), (q2, p2) = E1, E2 = meet(D1, S), meet(D2, S)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"12b_demand_increase_{lang}.png"))
