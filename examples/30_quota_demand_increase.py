"""Demand rises under a quota -> quantity stays at the quota, deadweight loss grows.

Topic: Tax, subsidy and quota
Use for: demand increases while a quota is in force; also an effective quota
  (P rises, Q falls to the quota), drawn with the same kinked S
  (DSE2024 Q3, CE1997 Q10(b))

Marking-scheme points it shows:
  - kinked S_quota: S0 (= MC) up to the quota Q0, then vertical
  - D0 (= MB0) shifts right to D1 (= MB1); quantity stays at Q0
  - efficient quantity rises from Q1 to Q2 (D meets S0)
  - hatched: the increase in deadweight loss (key)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    S0 = Line((16, 20), (80, 76))
    D0 = Line((16, 80), (70, 20))
    D1 = D0.shift(dx=16)
    draw(ax, S0, 16, 80, r"$S_0$ = MC", dy=1)
    draw(ax, D0, 16, 66, r"$D_0$ = $MB_0$", end="bottom")
    draw(ax, D1, 26, 80, r"$D_1$ = $MB_1$", dy=-1.5)
    arrow(ax, (D0.x(30) + 2, 30), (D1.x(30) - 2, 30))

    Q0 = 30
    K = (Q0, S0.y(Q0))                          # the kink
    draw(ax, Line.vertical(Q0), y0=K[1], y1=90, name=r"$S_{quota}$", end="top")
    dashed(ax, (Q0, O[1]), K)
    E1, E2 = meet(D0, S0), meet(D1, S0)
    region(ax, [(Q0, D0.y(Q0)), (Q0, D1.y(Q0)), E2, E1], "////")
    guide(ax, E1, O, to_y=False)
    guide(ax, E2, O, to_y=False)
    for q, n in ((Q0, r"$Q_0$"), (E1[0], r"$Q_1$"), (E2[0], r"$Q_2$")):
        label(ax, q, O[1] - 1.8, n, va="top")
    arrow(ax, (E1[0], 3), (E2[0], 3))          # efficient quantity rises
    key(ax, 50, 92, T("Increase in deadweight loss", "無謂損失增加"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"30_quota_demand_increase_{lang}.png"))
