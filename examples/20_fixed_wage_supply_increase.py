"""Wage fixed BELOW equilibrium; labour supply increases -> excess demand for labour shrinks.

Topic: Price fixed away from equilibrium
Use for: a wage or price fixed below equilibrium when supply rises; the same
  layout works for any fixed price when D or S shifts
  (DSE2021 Q12(c), CE1991 Q4(c)(ii))

Marking-scheme points it shows:
  - fixed wage W0 below the equilibrium wage
  - rightward shift of labour supply S0 -> S1 (arrow)
  - excess demand at W0 shrinks: ex dd0 (Q0 to Qd) -> ex dd1 (Q1 to Qd)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def sub(ax, x, y, word, n):            # word + subscript; mathtext cannot draw Chinese
    label(ax, x, y, word, ha="right"); label(ax, x, y - 1.6, n, ha="left", size=SIZE * .7)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.5, 2.7)
    O = (12, 12)
    axes(ax, O, (94, 12), (12, 92), T("Number of workers", "工人數目"), T("Wage rate", "工資率"))

    W = 36                                     # fixed wage, below equilibrium
    D = Line((84, W), m=-0.45)
    S0 = Line((20, W), m=1.6)
    S1 = S0.shift(dx=36)
    draw(ax, D, 20, 90, r"$D_0$", dy=-1.5)
    draw(ax, S0, S0.x(20), S0.x(84), r"$S_0$", end="top")
    draw(ax, S1, 46, S1.x(84), r"$S_1$", end="top")
    y = 74
    arrow(ax, (S0.x(y) + 5, y), (S1.x(y) - 5, y))

    q0, q1, qd = S0.x(W), S1.x(W), D.x(W)
    line(ax, (O[0], W), (92, W))
    label(ax, O[0] - 1.5, W, r"$W_0$", ha="right")
    for q, n in ((q0, r"$Q_0$"), (q1, r"$Q_1$"), (qd, r"$Q_d$")):
        line(ax, (q, O[1]), (q, W)); label(ax, q, O[1] - 1.8, n, va="top")
    brace(ax, q0, qd, W + 1, side="above")
    brace(ax, q1, qd, W - 1, side="below")
    sub(ax, (q0 + q1) / 2 + T(7, 10), W + 7, T("ex dd", "超額需求"), "0")
    sub(ax, (q1 + qd) / 2 + T(5, 8.5), W - 7, T("ex dd", "超額需求"), "1")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"20_fixed_wage_supply_increase_{lang}.png"))
