"""Economic growth: LRAS and AD both increase -> real output rises; P rises if AD grows more.

Topic: AD-AS
Use for: better infrastructure, more labour or capital, R&D, new tourist attractions
  that raise both spending and production capacity (DSE2018 Q9, DSE2020 Q9(b))

Marking-scheme points it shows:
  - LRAS0 shifts right to LRAS1 (arrow)
  - AD0 shifts right to AD1 (arrow), by MORE than LRAS
  - E0 -> E1: real output rises Y0 -> Y1, price level rises P0 -> P1
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    L0 = Line.vertical(46)
    L1 = L0.shift(dx=12)
    AD0 = Line((14, 80), m=-1)
    AD1 = AD0.shift(dx=28)                     # AD grows more than LRAS -> P rises
    draw(ax, L0, y0=O[1], y1=86)
    draw(ax, L1, y0=O[1], y1=86)
    label(ax, L0.vx + 1, 88, r"$LRAS_0$", ha="right", va="bottom")
    label(ax, L1.vx - 1, 88, r"$LRAS_1$", ha="left", va="bottom")
    draw(ax, AD0, 16, 70, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 40, 84, r"$AD_1$", dy=-1.5)
    arrow(ax, (L0.vx + 2, 82), (L1.vx - 2, 82))
    y = 78
    arrow(ax, (AD0.x(y) + 2, y), (AD1.x(y) - 2, y))

    E0, E1 = meet(AD0, L0), meet(AD1, L1)
    for E, p, n, Y in ((E0, r"$P_0$", r"$E_0$", r"$Y_0$"), (E1, r"$P_1$", r"$E_1$", r"$Y_1$")):
        guide(ax, E, O, p, to_x=False)
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
        label(ax, E[0], O[1] - 1.8, Y, va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"38_economic_growth_{lang}.png"))
