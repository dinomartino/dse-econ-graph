"""Price rises on ELASTIC (flat) demand -> total revenue falls.

Topic: Total revenue and elasticity
Use for: a price rise along one ELASTIC demand curve lowers total revenue /
  expenditure (chat-only variant: 05 with the price change reversed); for a price
  rise on inelastic demand use 18

Variant of: 05_tr_price_change_elastic

Marking-scheme points it shows:
  - flat (elastic) demand curve D
  - price rises from P1 to P2, quantity demanded falls from Q1 to Q2
  - gain of revenue (P1..P2 x 0..Q2) marked "+", loss (Q2..Q1 x 0..P1) marked "-"
  - loss > gain, so total revenue falls
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 66), (84, 38))
    draw(ax, D, 20, 84, "D", dy=-1.5)

    P1, P2 = 46, 58
    Q1, Q2 = D.x(P1), D.x(P2)
    A, B = (Q1, P1), (Q2, P2)

    hatch(ax, O[0], P1, Q2, P2)                # gain
    dots(ax, Q2, O[1], Q1, P1)                 # loss
    guide(ax, A, O, r"$P_1$", r"$Q_1$")
    guide(ax, B, O, r"$P_2$", r"$Q_2$")
    dot(ax, *A); dot(ax, *B)
    sign(ax, (O[0] + Q2) / 2, (P1 + P2) / 2, "+", size=SIZE + 2)
    sign(ax, (Q1 + Q2) / 2, (P1 + O[1]) / 2, "−", size=SIZE + 2)

    arrow(ax, (4, P1), (4, P2))                # price rises
    arrow(ax, (Q1, 3), (Q2, 3))                # quantity falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"05b_tr_price_rise_elastic_{lang}.png"))
