"""A quota is raised -> price falls, quantity rises, deadweight loss shrinks.

Topic: Tax, subsidy and quota
Use for: relaxing (raising) an effective quota and its effect on efficiency
  (DSE2015 Q3)

Marking-scheme points it shows:
  - S0 (= MC) and D (= MB); the quota moves right from S1 to S2 (arrow)
  - P falls P1 -> P2 and Q rises Q1 -> Q2 (axis arrows)
  - W, X on D and Z, Y on S0; area WXYZ = reduction in deadweight loss (hatched, key)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    D = Line((18, 84), (80, 22))
    S0 = Line((20, 18), (80, 78))
    draw(ax, D, 18, 80, "D = MB", dy=-1.5)
    draw(ax, S0, 20, 80, r"$S_0$ = MC", dy=1)

    Q1, Q2 = 28, 40
    W, X = (Q1, D.y(Q1)), (Q2, D.y(Q2))
    Y, Z = (Q2, S0.y(Q2)), (Q1, S0.y(Q1))
    draw(ax, Line.vertical(Q1), y0=O[1], y1=88, name=r"$S_1$", end="top")
    draw(ax, Line.vertical(Q2), y0=O[1], y1=88, name=r"$S_2$", end="top")
    arrow(ax, (Q1 + 2, 85), (Q2 - 2, 85))

    region(ax, [W, X, Y, Z], "////")
    for p in (W, X, Y, Z):
        dot(ax, *p)
    label(ax, Q1 + 3, W[1] + 3.5, "W")
    label(ax, Q2 + 3, X[1] + 3.5, "X")
    label(ax, Q2 + 3, Y[1] - 3.5, "Y")
    label(ax, Q1 - 3, Z[1] + 3.5, "Z")
    guide(ax, W, O, r"$P_1$", to_x=False)
    guide(ax, X, O, r"$P_2$", to_x=False)
    label(ax, Q1, O[1] - 1.8, r"$Q_1$", va="top")
    label(ax, Q2, O[1] - 1.8, r"$Q_2$", va="top")
    arrow(ax, (4, W[1]), (4, X[1]))             # price falls
    arrow(ax, (Q1, 3), (Q2, 3))                 # quantity rises
    key(ax, 50, 91, T("Reduction in deadweight loss", "無謂損失減少"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"29_quota_increase_{lang}.png"))
