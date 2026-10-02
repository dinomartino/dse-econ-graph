"""Deflationary gap narrows: AD increases -> real output rises towards Yf.

Topic: AD-AS
Use for: showing a deflationary (output) gap and how a rise in AD (tax cut, more
  tourists, expansionary policy) narrows it; add the vertical LRAS yourself
  (DSE2019 Q10(b), DSE2021 Q11(a), DSE2023 Q7(a), DSE2023 Q7(b))

Marking-scheme points it shows:
  - vertical LRAS at Yf, right of E0 (Y0 < Yf): gap0 = Y0 to Yf
  - AD0 shifts right to AD1 (arrow); E0 -> E1, P0 -> P1, Y0 -> Y1
  - gap1 = Y1 to Yf, narrower than gap0; key: gap = deflationary gap
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((22, 24), m=1)
    L = Line.vertical(70)
    AD0 = Line((36, 38), m=-1.4)
    AD1 = AD0.shift(dx=20)
    draw(ax, S, 22, 78, "SRAS", dy=1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, AD0, 18, 44, r"$AD_0$", end="top")
    draw(ax, AD1, 38, 66, r"$AD_1$", end="top")
    y = 56
    arrow(ax, (AD0.x(y) + 2, y), (AD1.x(y) - 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, S)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    brace(ax, E1[0], L.vx, O[1] + 1.5, r"$gap_1$", side="above")
    brace(ax, E0[0], L.vx, O[1] - 8, r"$gap_0$", side="below")
    label(ax, 73, 44, T("gap =\ndeflationary gap", "gap =\n通縮缺口"), ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"39_deflationary_gap_{lang}.png"))
