"""Aggregate demand decreases -> price level and real output both fall.

Topic: AD-AS
Use for: less investment, fewer tourists, a fall in exports, contractionary fiscal
  or monetary policy (chat-only variant: 34 with the shift reversed)

Variant of: 34_ad_increase

Marking-scheme points it shows:
  - AD0 shifts left to AD1 (arrow), SRAS unchanged
  - equilibrium moves E0 -> E1 down along the upward-sloping SRAS
  - price level falls P0 -> P1, real output falls Y0 -> Y1
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((22, 24), (76, 78))
    AD0 = Line((38, 78), (80, 22))
    AD1 = AD0.shift(dx=-22)
    draw(ax, S, 22, 76, "SRAS", dy=1.5)
    draw(ax, AD0, 38, 80, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 16, 58, r"$AD_1$", dy=-1.5)
    y = 70
    arrow(ax, (AD0.x(y) - 2, y), (AD1.x(y) + 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, S)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level falls
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"34b_ad_decrease_{lang}.png"))
