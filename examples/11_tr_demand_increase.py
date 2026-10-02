"""Demand increases -> price and quantity both rise -> total revenue increases (shade the change only).

Marking-scheme points it shows:
  - rightward shift of the demand curve (D0 -> D1)
  - higher price and quantity (P0 -> P1, Q0 -> Q1)
  - increase in total revenue = the L-shaped strip between the old and new
    P x Q corners (never the whole old or new TR rectangle)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), "Q", "P")

    S = Line((20, 18), (80, 78))
    D0 = Line((16, 80), (62, 20))
    D1 = D0.shift(dx=22)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D0, 16, 62, r"$D_0$", dy=-1.5)
    draw(ax, D1, 38, 82, r"$D_1$", dy=-1.5)
    y = 70
    arrow(ax, (D0.x(y) + 2, y), (D1.x(y) - 2, y))

    q0, p0 = meet(D0, S)
    q1, p1 = meet(D1, S)
    # the change in TR only: new rectangle minus old rectangle
    region(ax, [(O[0], p0), (q0, p0), (q0, O[1]), (q1, O[1]), (q1, p1), (O[0], p1)],
           "////", border=True)
    guide(ax, (q0, p0), O, r"$P_0$", r"$Q_0$")
    guide(ax, (q1, p1), O, r"$P_1$", r"$Q_1$")
    arrow(ax, (O[0] - 9, p0), (O[0] - 9, p1))                 # price rises
    arrow(ax, (q0, O[1] - 8), (q1, O[1] - 8))             # quantity rises
    key(ax, 60, 86, T("Increase in TR", "總收入增加"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"11_tr_demand_increase_{lang}.png"))
