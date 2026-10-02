"""Minimum wage ABOVE equilibrium in a labour market -> unemployment.

Marking-scheme points it shows:
  - minimum wage (W_min) above the equilibrium wage (W_e)
  - correct position of the excess supply of labour / unemployment (Qd to Qs at W_min)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Number of workers", "工人數目"), T("Wage rate", "工資率"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$W_e$", to_x=False)

    W = 66                                     # minimum wage, above We
    qd, qs = D.x(W), S.x(W)
    line(ax, (O[0], W), (84, W))
    label(ax, O[0] - 1.5, W, r"$W_{min}$", ha="right")
    dashed(ax, (qd, O[1]), (qd, W)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    dashed(ax, (qs, O[1]), (qs, W)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    brace(ax, qd, qs, W + 1, T("excess supply", "超額供應"), side="above")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"02_price_floor_surplus_{lang}.png"))
