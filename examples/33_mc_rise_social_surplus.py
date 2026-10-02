"""Marginal cost rises -> supply shifts up -> total social surplus falls by area abE1E0.

Topic: Consumer and producer surplus
Use for: a rise in production cost (MC) and the change in total social surplus
  (DSE2023 Q5(a))

Marking-scheme points it shows:
  - S0 = MC0 shifts up to S1 = MC1 (arrow); D = MB
  - equilibrium E0 -> E1
  - a, b: where S0 and S1 meet the price axis
  - hatched band abE1E0 = decrease in total social surplus
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((12, 88), (80, 16))
    S0 = Line((12, 18), m=0.75)
    S1 = S0.shift(dy=18)
    draw(ax, D, 12, 74, "D = MB", dy=-1.5)
    draw(ax, S0, 12, 80, r"$S_0$ = $MC_0$")
    draw(ax, S1, 12, 72, r"$S_1$ = $MC_1$")
    arrow(ax, (68, S0.y(68) + 3), (68, S1.y(68) - 3))

    a, b = (O[0], S0.y(O[0])), (O[0], S1.y(O[0]))
    E0, E1 = meet(D, S0), meet(D, S1)
    region(ax, [a, b, E1, E0], "////")
    dot(ax, *E0); dot(ax, *E1)
    label(ax, E0[0] + 4, E0[1] - 1, r"$E_0$")
    label(ax, E1[0] + 1, E1[1] + 5, r"$E_1$")
    label(ax, O[0] - 1.5, a[1], "a", ha="right")
    label(ax, O[0] - 1.5, b[1], "b", ha="right")
    key(ax, 34, 92, T("Decrease in total social surplus", "總社會盈餘減少"))
    label(ax, 54, 86, T("= area", "= 面積"), ha="right")   # no Chinese inside $...$
    label(ax, 54.6, 86, r"ab$E_1E_0$", ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"33_mc_rise_social_surplus_{lang}.png"))
