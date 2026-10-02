"""Vertical supply; the fixed price is raised but stays below equilibrium -> shortage shrinks.

Topic: Price fixed away from equilibrium
Use for: a fixed tuition fee or ticket price raised from P1 to P2 (e.g. $10 to
  $20) with a fixed number of places or seats; also the variant where vertical
  S shifts right at a fixed price
  (DSEPP Q12(a)(ii), CE2007 Q8(a), CE2005 Q9(b)(i))

Marking-scheme points it shows:
  - vertical supply S at Q0; both prices below the equilibrium price
  - price raised from P1 to P2 (arrow between the labels)
  - shortage shrinks: Ex. D1 (wide, at P1) -> Ex. D2 (narrow, at P2)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def sub(ax, x, y, word, n):            # word + subscript; mathtext cannot draw Chinese
    label(ax, x, y, word, ha="right"); label(ax, x, y - 1.6, n, ha="left", size=SIZE * .7)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (14, 12)
    axes(ax, O, (90, 12), (14, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((22, 84), (86, 24))
    S = Line.vertical(34)
    draw(ax, D, 22, 86, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=84, end="top")
    label(ax, S.vx, O[1] - 1.8, r"$Q_0$", va="top")

    P1, P2 = 28, 48                            # both below equilibrium
    for P, n in ((P1, "1"), (P2, "2")):
        q = D.x(P)
        line(ax, (O[0], P), (88, P))
        label(ax, O[0] - 1.5, P, f"$P_{n}$", ha="right")
        brace(ax, S.vx, q, P - 1, side="below")
        sub(ax, (S.vx + q) / 2 + T(5, 8.5), P - 7, T("Ex. D", "超額需求"), n)
    arrow(ax, (5, P1 + 3), (5, P2 - 3))        # price raised
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"21_vertical_supply_price_raised_{lang}.png"))
