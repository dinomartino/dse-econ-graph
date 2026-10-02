"""Price falls on ELASTIC (flat) demand -> total revenue rises.

Marking-scheme points it shows:
  - flat (elastic) demand curve D
  - price falls from P1 to P2, quantity demanded rises from Q1 to Q2
  - loss of revenue (P2..P1 x 0..Q1) marked "-", gain (Q1..Q2 x 0..P2) marked "+"
  - gain > loss, so total revenue rises
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 66), (84, 38))
    draw(ax, D, 20, 84, "D", dy=-1.5)

    P1, P2 = 58, 46
    Q1, Q2 = D.x(P1), D.x(P2)
    A, B = (Q1, P1), (Q2, P2)

    dots(ax, Q1, O[1], Q2, P2)                 # gain
    hatch(ax, O[0], P2, Q1, P1)                # loss
    guide(ax, A, O, r"$P_1$", r"$Q_1$")
    guide(ax, B, O, r"$P_2$", r"$Q_2$")
    dot(ax, *A); dot(ax, *B)
    sign(ax, (Q1 + Q2) / 2, P2 / 2 + O[1] / 2, "+", size=SIZE + 2)
    sign(ax, (O[0] + Q1) / 2, (P1 + P2) / 2, "−", size=SIZE + 2)

    arrow(ax, (4, P1), (4, P2))                # price falls
    arrow(ax, (Q1, 3), (Q2, 3))                # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"05_tr_price_change_elastic_{lang}.png"))
