"""Unit tax on a good with inelastic (steep) demand: buyers bear more, deadweight loss "a".

Topic: Tax, subsidy and quota
Use for: who bears more of a unit tax (the less elastic side) and the
  deadweight loss; for tax-revenue shading see template 07
  (DSE2014 Q9(b), DSE2016 Q10(c))

Marking-scheme points it shows:
  - steep D; S0 shifts up by the tax to S1 (arrow "tax")
  - buyers pay P1 (was P0); sellers receive P2 = P1 - t; Q0 -> Q1
  - buyers' burden P0..P1 > sellers' burden P2..P0 (braces)
  - deadweight loss: triangle "a" between D and S0 from Q1 to Q0
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    D = Line((32, 90), (62, 22))
    S0 = Line((12, 18), m=0.7)
    S1 = S0.shift(dy=28)
    draw(ax, D, 32, 62, "D", dy=-1.5)
    draw(ax, S0, 12, 80, r"$S_0$")
    draw(ax, S1, 20, 64, r"$S_1$")
    x = 72
    arrow(ax, (x, S0.y(x) + 4), (x, S0.y(x) + 14))
    label(ax, x + 1.5, S0.y(x) + 10, T("tax", "稅"), ha="left")

    E0, E1 = meet(D, S0), meet(D, S1)
    Q1, P1 = E1
    B = (Q1, S0.y(Q1))
    region(ax, [E1, B, E0], "////", border=True)
    sign(ax, (2 * Q1 + E0[0]) / 3, (P1 + B[1] + E0[1]) / 3, "a")
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, E0, O, r"$P_0$", r"$Q_0$")
    guide(ax, B, O, r"$P_2$", to_x=False)
    vbrace(ax, E0[1] + 0.5, P1, 5, T("Buyers' burden", "買家負擔"))
    vbrace(ax, B[1], E0[1] - 0.5, 5, T("Sellers' burden", "賣家負擔"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"31_unit_tax_burden_dwl_{lang}.png"))
