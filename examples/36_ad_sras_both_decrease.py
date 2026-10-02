"""AD and SRAS both decrease -> real output falls; the price level is indeterminate.

Topic: AD-AS
Use for: one event that raises costs AND cuts spending (Brexit visa costs + less
  investment, a disaster that shuts factories + pessimism); only Y is certain
  (DSE2017 Q12(b), DSE2021 Q11(b))

Marking-scheme points it shows:
  - AD0 shifts left to AD1 (arrow)
  - SRAS0 shifts left to SRAS1 (arrow)
  - real output falls Y0 -> Y1; the price level is not labelled (may rise or fall)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD0 = Line((38, 80), (82, 26))
    AD1 = AD0.shift(dx=-20)
    S0 = Line((40, 26), (82, 72))
    S1 = S0.shift(dx=-20)
    draw(ax, AD0, 38, 80, r"$AD_0$", end="top")
    draw(ax, AD1, 18, 54, r"$AD_1$", end="top")
    draw(ax, S0, 40, 82, r"$SRAS_0$", end="top")
    draw(ax, S1, 20, 62, r"$SRAS_1$", end="top")
    for A, B, y in ((AD0, AD1, 72), (S0, S1, 66)):
        arrow(ax, (A.x(y) - 2, y), (B.x(y) + 2, y))

    E0, E1 = meet(AD0, S0), meet(AD1, S1)
    guide(ax, E0, O, xlab=r"$Y_0$", to_y=False)
    guide(ax, E1, O, xlab=r"$Y_1$", to_y=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0], E[1] + 4, n, va="bottom")
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"36_ad_sras_both_decrease_{lang}.png"))
