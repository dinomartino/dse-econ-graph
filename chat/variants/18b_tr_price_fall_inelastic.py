"""Price falls on INELASTIC (steep) demand -> total revenue falls.

Topic: Total revenue and elasticity
Use for: a price fall along an inelastic demand curve lowers total revenue /
  expenditure, e.g. a bumper harvest lowers farmers' revenue (chat-only variant:
  18 with the price change reversed); for a price fall on elastic demand use 05

Variant of: 18_tr_price_rise_inelastic

Marking-scheme points it shows:
  - steep (inelastic) demand curve D, no supply curve needed
  - price falls from P1 to P2, quantity demanded rises from Q1 to Q2
  - loss (P2..P1 x 0..Q1) marked "-", gain (Q1..Q2 x 0..P2) marked "+"
  - loss > gain, so total revenue falls
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((30, 86), (66, 20))
    draw(ax, D, 30, 66, "D", dy=-1.5)

    P1, P2 = 62, 34
    Q1, Q2 = D.x(P1), D.x(P2)
    A, B = (Q1, P1), (Q2, P2)

    dots(ax, O[0], P2, Q1, P1)                 # loss
    hatch(ax, Q1, O[1], Q2, P2)                # gain
    guide(ax, A, O, r"$P_1$", r"$Q_1$")
    guide(ax, B, O, r"$P_2$", r"$Q_2$")
    dot(ax, *A); dot(ax, *B)
    sign(ax, (O[0] + Q1) / 2, (P1 + P2) / 2, "−", size=SIZE + 2)
    sign(ax, (Q1 + Q2) / 2, (P2 + O[1]) / 2, "+", size=SIZE + 2)

    arrow(ax, (O[0] - 9, P1), (O[0] - 9, P2))  # price falls
    arrow(ax, (Q1, O[1] - 9), (Q2, O[1] - 9))  # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"18b_tr_price_fall_inelastic_{lang}.png"))
