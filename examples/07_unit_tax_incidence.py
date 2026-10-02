"""Per-unit tax: incidence and tax revenue.

Marking-scheme points it shows:
  - S shifts up (vertically) by the tax t to S+t
  - consumers pay Pc, producers receive Pp = Pc - t, quantity falls Q0 -> Q1
  - brace for the tax per unit t
  - hatched tax revenue (Pp..Pc x 0..Q1), split into consumers' and producers' burden
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (14, 12)
    axes(ax, O, (92, 12), (14, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((22, 84), (84, 26))
    S = Line((22, 26), (84, 72))
    t = 20
    St = S.shift(dy=t)
    draw(ax, D, 22, 72, "D", dy=-1.5)
    draw(ax, S, 22, 84, "S", dy=1.0)

    E0, E1 = meet(D, S), meet(D, St)
    draw(ax, St, E1[0], 74, "S+t", dy=1.5)      # starts at E1 so it stays out of the hatch
    Q0, Pe = E0
    Q1, Pc = E1
    Pp = S.y(Q1)
    assert abs((Pc - Pp) - t) < 1e-9

    hatch(ax, O[0], Pp, Q1, Pc)
    dashed(ax, (O[0], Pe), (Q1, Pe))
    guide(ax, E1, O, r"$P_c$", r"$Q_1$")
    dashed(ax, (O[0], Pp), (Q1, Pp)); label(ax, O[0] - 1.5, Pp, r"$P_p$", ha="right")
    dashed(ax, (O[0], Pe), (Q0, Pe)); label(ax, O[0] - 1.5, Pe, r"$P_e$", ha="right")
    dashed(ax, (Q0, O[1]), (Q0, Pe)); label(ax, Q0, O[1] - 1.8, r"$Q_0$", va="top")
    dot(ax, *E0); dot(ax, *E1); dot(ax, Q1, Pp)

    sign(ax, (O[0] + Q1) / 2, (Pe + Pc) / 2, "A")
    sign(ax, (O[0] + Q1) / 2, (Pp + Pe) / 2, "B")
    vbrace(ax, Pp, Pc, 4, r"$t$", side="left")

    kx, ky = 62, 22
    label(ax, kx, ky + 5, T("A: consumers' burden", "A：消費者負擔"), ha="left")
    label(ax, kx, ky, T("B: producers' burden", "B：生產者負擔"), ha="left")
    label(ax, kx, ky - 5, T("A + B: tax revenue", "A + B：政府稅收"), ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"07_unit_tax_incidence_{lang}.png"))
