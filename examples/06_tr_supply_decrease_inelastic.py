"""Supply decreases on INELASTIC (steep) demand -> total revenue rises.

Topic: Total revenue and elasticity
Use for: a supply shift (cost up, bad harvest; or reversed: subsidy, cost down) with
  inelastic or elastic demand changes total revenue (CE1994 Q11(b), CE1997 Q11(c),
  CE2009 Q9(b), DSEPP Q3, DSE2021 Q10(c), CE2000 Q11(b) wage bill)

Marking-scheme points it shows:
  - steep (inelastic) demand curve D
  - supply decreases: S1 shifts left to S2 (shift arrow)
  - price rises P1 -> P2, quantity falls Q1 -> Q2
  - gain (P1..P2 x 0..Q2) marked "+", loss (Q2..Q1 x 0..P1) marked "-"
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

    D = Line((34, 84), (62, 20))
    S1 = Line((20, 24), (84, 72))
    S2 = S1.shift(dx=-30)
    draw(ax, D, 34, 62, "D", dy=-1.5)
    draw(ax, S1, 20, 84, r"$S_1$", dy=1.0)
    draw(ax, S2, 20, 60, r"$S_2$", end="top", dx=0)

    E1, E2 = meet(D, S1), meet(D, S2)
    (Q1, P1), (Q2, P2) = E1, E2

    dots(ax, O[0], P1, Q2, P2)                 # gain
    hatch(ax, Q2, O[1], Q1, P1)                # loss
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, E2, O, r"$P_2$", r"$Q_2$")
    dot(ax, *E1); dot(ax, *E2)
    sign(ax, O[0] + 0.3 * (Q2 - O[0]), P2 - 5, "+", size=SIZE + 2)
    sign(ax, (Q1 + Q2) / 2, (O[1] + P1) / 2, "−", size=SIZE + 2)

    ym = P2 + 5
    arrow(ax, (S1.x(ym) - 2, ym), (S2.x(ym) + 1, ym))   # supply decreases
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"06_tr_supply_decrease_inelastic_{lang}.png"))
