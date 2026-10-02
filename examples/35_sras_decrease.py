"""Short-run aggregate supply decreases -> price level rises, real output falls.

Topic: AD-AS
Use for: production costs rise (wages, rents, oil or raw-material prices), a natural
  disaster or strike cuts production; for an SRAS increase, reverse the arrows
  (supply-shock MCQs, DSE2017 Q12)

Marking-scheme points it shows:
  - SRAS0 shifts left to SRAS1 (arrow), AD unchanged
  - equilibrium moves E0 -> E1 up along AD
  - price level rises P0 -> P1, real output falls Y0 -> Y1
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((18, 80), (76, 22))
    S0 = Line((34, 22), (82, 70))
    S1 = S0.shift(dx=-22)
    draw(ax, AD, 18, 76, "AD", dy=-1.5)
    draw(ax, S0, 34, 82, r"$SRAS_0$", end="top")
    draw(ax, S1, 16, 64, r"$SRAS_1$", end="top")
    y = 60
    arrow(ax, (S0.x(y) - 2, y), (S1.x(y) + 2, y))

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output falls
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"35_sras_decrease_{lang}.png"))
