"""Fixed stock (vertical supply): supply rises a little, demand rises a lot -> price rises.

Topic: Demand and supply: shifts
Use for: a fixed stock (taxi licences, land, flats, seats) whose quota is raised
  slightly while demand grows more, so the price still rises
  (CE2011 Q11(a), CE1992 Q1(d))

Marking-scheme points it shows:
  - vertical supply S1 -> S2 (small shift right) and demand D1 -> D2 (larger shift right)
  - equilibria E1, E2: price rises P1 -> P2, quantity rises Q1 -> Q2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    S1, S2 = Line.vertical(44), Line.vertical(54)
    D1 = Line((18, 80), m=-1.15)
    D2 = D1.shift(dx=26)
    draw(ax, S1, name=r"$S_1$", y0=O[1], y1=86, end="top")
    draw(ax, S2, name=r"$S_2$", y0=O[1], y1=86, end="top")
    draw(ax, D1, 18, 62, r"$D_1$", dy=-1.5)
    draw(ax, D2, 40, 84, r"$D_2$", dy=-1.5)
    arrow(ax, (S1.vx + 1.5, 82), (S2.vx - 1.5, 82))           # small supply shift
    arrow(ax, (D1.x(36) + 2, 36), (D2.x(36) - 2, 36))         # big demand shift

    (q1, p1), (q2, p2) = E1, E2 = meet(S1, D1), meet(S2, D2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 2.5, E[1] + 1, f"$E_{n}$", ha="left", va="bottom")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"15_vertical_supply_demand_shift_{lang}.png"))
