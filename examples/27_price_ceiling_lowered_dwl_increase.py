"""A price ceiling is lowered further below equilibrium -> deadweight loss increases.

Topic: Price controls and efficiency
Use for: a price ceiling (or controlled price) lowered from Pc1 to Pc2, both below
  equilibrium, when the question asks for the change in deadweight loss
  (DSE2012 Q5(c))

Marking-scheme points it shows:
  - ceiling lowered Pc1 -> Pc2; quantity transacted falls Q1 -> Q2 along S
  - original deadweight loss: triangle between D and S from Q1 to Qe (dotted)
  - increase in deadweight loss: trapezoid between D and S from Q2 to Q1 (hatched)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((14, 86), m=-0.85)
    S = Line((20, 16), m=1.0)
    draw(ax, D, 14, 84, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", end="top")

    Qe, Pe = meet(D, S)
    P1, P2 = 40, 28                            # both ceilings below Pe
    Q1, Q2 = S.x(P1), S.x(P2)
    region(ax, [(Q1, P1), (Q1, D.y(Q1)), (Qe, Pe)], "....", border=True)
    region(ax, [(Q2, P2), (Q2, D.y(Q2)), (Q1, D.y(Q1)), (Q1, P1)], "////", border=True)
    dot(ax, Qe, Pe)
    guide(ax, (Qe, Pe), O, xlab=r"$Q_e$", to_y=False)
    for P, Q, n in ((P1, Q1, "1"), (P2, Q2, "2")):
        line(ax, (O[0], P), (86, P))
        label(ax, O[0] - 1.5, P, f"$P_{{c{n}}}$", ha="right")
        line(ax, (Q, O[1]), (Q, D.y(Q)))
        label(ax, Q, O[1] - 1.8, f"$Q_{n}$", va="top")
    arrow(ax, (2, P1), (2, P2))                # ceiling lowered
    arrow(ax, (Q1, 3), (Q2, 3))                # Q falls
    key(ax, 52, 92, T("Original deadweight loss", "原有無謂損失"), "....")
    key(ax, 52, 85.5, T("Increase in deadweight loss", "無謂損失增加"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"27_price_ceiling_lowered_dwl_increase_{lang}.png"))
