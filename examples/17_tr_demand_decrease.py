"""Demand decreases -> price and quantity both fall -> total revenue falls (shade the change only).

Topic: Total revenue and elasticity
Use for: a fall in demand and its effect on sellers' total revenue, or the decrease
  in consumers' expenditure / sales revenue
  (CE1997 Q9(b), CE1999 Q9(b), CE2004 Q3)

Marking-scheme points it shows:
  - leftward shift of demand D1 -> D2 (arrow), S unchanged
  - lower price and quantity (P1 -> P2, Q1 -> Q2)
  - decrease in total revenue = the L-shaped strip between the old and new
    P x Q corners (never the whole old or new TR rectangle)
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
    D1 = Line((38, 80), (84, 20))
    D2 = D1.shift(dx=-22)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D1, 38, 84, r"$D_1$", dy=-1.5)
    draw(ax, D2, 16, 62, r"$D_2$", dy=-1.5)
    y = 70
    arrow(ax, (D1.x(y) - 2, y), (D2.x(y) + 2, y))

    q1, p1 = meet(D1, S)
    q2, p2 = meet(D2, S)
    # the change in TR only: old rectangle minus new rectangle
    region(ax, [(O[0], p2), (q2, p2), (q2, O[1]), (q1, O[1]), (q1, p1), (O[0], p1)],
           "////", border=True)
    guide(ax, (q1, p1), O, r"$P_1$", r"$Q_1$")
    guide(ax, (q2, p2), O, r"$P_2$", r"$Q_2$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    key(ax, 48, 90, T("Decrease in total revenue", "總收入減少"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"17_tr_demand_decrease_{lang}.png"))
