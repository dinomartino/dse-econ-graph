"""Long run: AD increases on a vertical LRAS -> price level rises, real output stays at Yf.

Topic: AD-AS
Use for: the LONG-RUN effect of a demand-side change (cash handout, more spending)
  when production capacity is unchanged (DSE2012 Q10(c))

Marking-scheme points it shows:
  - vertical LRAS at full-employment output Yf (no SRAS)
  - AD1 shifts right to AD2 (arrow)
  - price level rises P1 -> P2; real output unchanged at Yf
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    L = Line.vertical(50)
    AD1 = Line((18, 70), (70, 18))
    AD2 = AD1.shift(dx=22)
    draw(ax, L, y0=O[1], y1=82, name="LRAS", end="top")
    draw(ax, AD1, 18, 70, r"$AD_1$", dy=-1.5)
    draw(ax, AD2, 32, 82, r"$AD_2$", dy=-1.5)
    y = 32
    arrow(ax, (AD1.x(y) + 2, y), (AD2.x(y) - 2, y))

    E1, E2 = meet(AD1, L), meet(AD2, L)
    guide(ax, E1, O, r"$P_1$", to_x=False)
    guide(ax, E2, O, r"$P_2$", to_x=False)
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    for E, n in ((E1, r"$E_1$"), (E2, r"$E_2$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E1[1]), (O[0] - 9, E2[1]))       # price level rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"37_lras_ad_increase_{lang}.png"))
