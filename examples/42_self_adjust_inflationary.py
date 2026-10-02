"""Inflationary gap closed by market forces: SRAS decreases -> price level rises, output falls to Yf.

Topic: AD-AS
Use for: "how do market forces restore full-employment output" when Y > Yf:
  excess demand for labour -> wages and costs rise -> SRAS falls (DSE2020 Q6)

Marking-scheme points it shows:
  - AD unchanged; E0 right of the vertical LRAS (Y0 > Yf)
  - SRAS0 shifts left to SRAS1 (arrow) until AD meets SRAS1 on LRAS
  - E0 -> E1: price level rises P0 -> P1, real output falls Y0 -> Yf
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((16, 80), m=-0.7)
    L = Line.vertical(44)
    S0 = Line((64, AD.y(64)), m=1.5)
    S1 = Line(meet(AD, L), m=S0.m)               # meets AD on LRAS
    draw(ax, AD, 16, 84, "AD", dy=-1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, S0, 52, 80, r"$SRAS_0$", end="top")
    draw(ax, S1, 30, 60, r"$SRAS_1$", end="top")
    y = 66
    arrow(ax, (S0.x(y) - 2, y), (S1.x(y) + 2, y))

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", to_x=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 2, E[1] + 4, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (L.vx, O[1] - 8))        # real output falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"42_self_adjust_inflationary_{lang}.png"))
