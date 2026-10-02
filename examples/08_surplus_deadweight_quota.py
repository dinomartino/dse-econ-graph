"""A quota (Qq) set BELOW the equilibrium quantity (Qe): consumer surplus,
producer surplus and deadweight loss.

Topic: Tax, subsidy and quota
Use for: a quota below the equilibrium quantity: consumer surplus, producer surplus and
  deadweight loss (CE1997 Q10(b), CE1998 Q2)

Marking-scheme points it shows:
  - quota line at Qq < Qe; price rises to Pq (on D at Qq)
  - consumer surplus: above Pq, under D, up to Qq
  - producer surplus: above S, below Pq, up to Qq
  - deadweight loss: triangle between D and S from Qq to Qe
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((12, 86), (80, 24))
    S = Line((12, 18), (80, 80))
    draw(ax, D, 12, 80, "D", dy=-1.5)
    draw(ax, S, 12, 72, "S", dy=1.5)

    Qe, Pe = meet(D, S)
    Qq = O[0] + 0.6 * (Qe - O[0])              # quota, below Qe
    Pq, Ps = D.y(Qq), S.y(Qq)
    Q = Line.vertical(Qq)
    draw(ax, Q, name=T("Quota", "配額"), y0=O[1], y1=88, end="top")

    # areas (exact vertices)
    region(ax, [(12, D.y(12)), (Qq, Pq), (12, Pq)], "....", border=True)      # CS
    region(ax, [(12, Pq), (Qq, Pq), (Qq, Ps), (12, S.y(12))], "////", border=True)  # PS
    region(ax, [(Qq, Pq), (Qq, Ps), (Qe, Pe)], "xxxx", border=True)           # DWL
    dot(ax, Qe, Pe)

    dashed(ax, (O[0], Pq), (12, Pq))
    label(ax, O[0] - 1.5, Pq, r"$P_q$", ha="right")
    label(ax, O[0] - 1.5, Ps, r"$P_s$", ha="right")
    dashed(ax, (O[0], Ps), (Qq, Ps))
    guide(ax, (Qe, Pe), O, r"$P_e$", r"$Q_e$")
    label(ax, Qq, O[1] - 1.8, r"$Q_q$", va="top")

    key(ax, 60, 92, T("Consumer surplus", "消費者盈餘"), "....")
    key(ax, 60, 85.5, T("Producer surplus", "生產者盈餘"), "////")
    key(ax, 60, 79, T("Deadweight loss", "無謂損失"), "xxxx")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"08_surplus_deadweight_quota_{lang}.png"))
