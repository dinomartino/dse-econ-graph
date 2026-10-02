"""Imported workers: labour supply rises -> wage falls, LOCAL employment falls.

Topic: Labour market
Use for: importing workers (or more immigrants) adds to the local labour supply;
  the wage falls and fewer LOCAL workers are employed (read off the local S at W2)
  (CE1998 Q9(c)(i)(ii))

Marking-scheme points it shows:
  - S (Local) and S' (Local + imported) to its right, labour demand D
  - wage rate falls W1 -> W2
  - local employment falls Q1 -> Q2, Q2 read off S (Local) at W2
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Number of\nworkers", "工人數目"), T("Wage rate", "工資率"))

    D = Line((24, 84), m=-1)
    S = Line((16, 20), m=1)
    S2 = S.shift(dx=26)
    draw(ax, D, 24, 80, "D", dy=-1.5)
    draw(ax, S, 16, 74, T("S (Local)", "S（本地）"), dy=1.5)
    draw(ax, S2, 38, 84, T("S’ (Local + imported)", "S’（本地＋輸入）"), dy=1.5)

    q1, w1 = meet(D, S)
    w2 = meet(D, S2)[1]
    q2 = S.x(w2)                                   # local workers at the new wage
    guide(ax, (q1, w1), O, r"$W_1$", to_x=False)
    guide(ax, meet(D, S2), O, r"$W_2$", to_x=False)
    for q, w, n in ((q1, w1, "1"), (q2, w2, "2")):
        line(ax, (q, O[1]), (q, w))
        label(ax, q, O[1] - 1.8, f"$Q_{n}$", va="top")
    arrow(ax, (q1 - 3, O[1] - 4.3), (q2 + 3, O[1] - 4.3))   # Q2 <- Q1
    arrow(ax, (O[0] - 9, w1), (O[0] - 9, w2))               # wage falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"16_labour_imported_workers_{lang}.png"))
