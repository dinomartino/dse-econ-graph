"""Inflationary gap closed by a fall in AD -> real output falls back to Yf.

Topic: AD-AS
Use for: output above full employment (Y0 > Yf) and a fall in AD (fewer tourists,
  contractionary fiscal or monetary policy) that brings it back to Yf (DSE2015 Q12(b))

Marking-scheme points it shows:
  - E0 right of the vertical LRAS: Y0 > Yf, inflationary gap from Yf to Y0
  - AD0 shifts left to AD1 (arrow); new E1 where AD1 meets SRAS on LRAS
  - real output falls Y0 -> Yf, price level falls P0 -> P1
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((20, 30), m=0.6)
    L = Line.vertical(42)
    AD0 = Line((64, S.y(64)), m=-1.5)
    AD1 = Line(meet(L, S), m=AD0.m)              # meets SRAS on LRAS
    draw(ax, S, 20, 84, "SRAS", dy=1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, AD0, 50, 78, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 26, 54, r"$AD_1$", end="top")
    y = 70
    arrow(ax, (AD0.x(y) - 2, y), (AD1.x(y) + 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, L)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", to_x=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1] - 3, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level falls
    arrow(ax, (E0[0], O[1] - 8), (L.vx, O[1] - 8))        # real output falls
    brace(ax, L.vx, E0[0], O[1] + 1.5, "gap", side="above")
    label(ax, 68, 24, T("gap =\ninflationary gap", "gap =\n通脹缺口"), ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"40_inflationary_gap_{lang}.png"))
