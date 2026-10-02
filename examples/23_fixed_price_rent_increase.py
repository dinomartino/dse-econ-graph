"""Vertical supply; the controlled rent is raised but stays below equilibrium -> total rental payment rises.

Topic: Price fixed away from equilibrium
Use for: a rent (or other controlled price) raised from P0 to P1 with a fixed
  number of units; also capital raised by a share issue at a fixed price,
  P̄ x Q̄ (hatch the whole rectangle under P̄ up to Q̄ there)
  (DSE2025 Q11(b)(i), CE2001 Q10(c)(i))

Marking-scheme points it shows:
  - vertical supply S at Q0; rent raised from P0 to P1, both below equilibrium
  - increase in total rental payment = (P1 - P0) x Q0, hatched with a key
  - excess demand (shortage) at P1, from Q0 to Qd
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Quantity", "數量"), T("Rental", "租金"))

    D = Line((20, 80), (84, 24))
    S = Line.vertical(44)
    draw(ax, D, 20, 84, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=84, end="top")
    label(ax, S.vx, O[1] - 1.8, r"$Q_0$", va="top")

    P0, P1 = 28, 38                            # both below equilibrium
    hatch(ax, O[0], P0, S.vx, P1)              # increase in total rental payment
    dashed(ax, (S.vx, P1), (D.x(P1), P1))
    label(ax, O[0] - 1.5, P0, r"$P_0$", ha="right")
    label(ax, O[0] - 1.5, P1, r"$P_1$", ha="right")
    arrow(ax, (3, P0), (3, P1))                # rent raised
    brace(ax, S.vx, D.x(P1), P1 - 1, T("Excess\ndemand", "超額需求"), side="below")
    key(ax, 58, 80, T("Increase in total\nrental payment", "總租金支出增加"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"23_fixed_price_rent_increase_{lang}.png"))
