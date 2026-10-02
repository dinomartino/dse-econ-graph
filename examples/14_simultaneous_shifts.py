"""Demand and supply both increase, demand by MORE -> price rises.

Topic: Demand and supply: shifts
Use for: "under what condition does the price rise?" when demand and supply both
  change; variants: both shift left with the supply shift bigger (CE2002 Q2) also
  raises the price; equal shifts leave the price unchanged
  (CE1995 Q11(a), CE2002 Q2, CE2003 Q10(b)(ii), DSE2015 Q11(d))

Marking-scheme points it shows:
  - D shifts right D -> D' and S shifts right S -> S', each with its own arrow
  - the demand shift is clearly larger than the supply shift
  - new equilibrium E2: price rises P1 -> P2, quantity rises Q1 -> Q2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D, S = Line((16, 78), m=-1), Line((18, 20), m=1)
    D2, S2 = D.shift(dx=30), S.shift(dx=12)
    draw(ax, D, 16, 58, "D", dy=-1.5)
    draw(ax, D2, 42, 88, "D’", dy=-1.5)
    draw(ax, S, 18, 78, "S", end="top")
    draw(ax, S2, 30, 88, "S’", end="top")
    arrow(ax, (D.x(72) + 2, 72), (D2.x(72) - 2, 72))     # big demand shift
    arrow(ax, (S.x(28) + 2, 28), (S2.x(28) - 2, 28))     # small supply shift

    (q1, p1), (q2, p2) = E1, E2 = meet(D, S), meet(D2, S2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"14_simultaneous_shifts_{lang}.png"))
