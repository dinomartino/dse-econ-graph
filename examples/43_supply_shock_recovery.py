"""Temporary supply shock: SRAS falls (1), then recovers (2) -> P and Y return to P0 and Yf.

Topic: AD-AS
Use for: raw-material prices rise for a while, then the economy adjusts back in the
  long run (excess labour supply -> wages fall -> SRAS rises again) (DSE2013 Q4(b))

Marking-scheme points it shows:
  - AD, SRAS0 and vertical LRAS all through E0 at (Yf, P0)
  - arrow 1: SRAS0 shifts left to SRAS1; E0 -> E1, P rises to P1, Y falls to Y1
  - arrow 2: SRAS1 shifts back right to SRAS0; E1 -> E0, P back to P0, Y back to Yf
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((16, 78), m=-0.9)
    L = Line.vertical(56)
    S0 = Line(meet(AD, L), m=1.2)
    S1 = S0.shift(dx=-20)
    draw(ax, AD, 16, 76, "AD", dy=-1.5)
    draw(ax, L, y0=O[1], y1=88, name="LRAS", end="top")
    draw(ax, S0, 36, 87.7, r"$SRAS_0$", end="top")
    draw(ax, S1, 16, 67.7, r"$SRAS_1$", end="top")
    for A, B, y, n in ((S0, S1, 66, "1"), (S1, S0, 22, "2")):
        arrow(ax, (A.x(y) + (2 if n == "2" else -2), y), (B.x(y) + (-2 if n == "2" else 2), y))
        label(ax, (A.x(y) + B.x(y)) / 2, y + 3, n)

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", to_x=False)
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 2, E[1] + 4, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"43_supply_shock_recovery_{lang}.png"))
