"""Per-unit subsidy: S shifts down, buyers pay less, sellers receive more, MC > MB.

Topic: Tax, subsidy and quota
Use for: subsidy incidence; the less elastic side benefits more (draw D or S steeper to match)
  (DSE2017 Q11(b))

Marking-scheme points it shows:
  - S0 shifts down by the subsidy s to Ss (arrow); E0 -> E1, Q0 -> Q1
  - buyers pay P1 < P0; sellers receive P2 = P1 + s (point A on S0)
  - consumer benefit (P0-P1) x Q1 dotted, producer benefit (P2-P0) x Q1 hatched
  - at Q1, MC (A) > MB (E1): overproduction
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 88), (80, 18))
    S0 = Line((16, 40), (80, 80))
    Ss = S0.shift(dy=-22)
    draw(ax, D, 16, 80, "D", dy=-1.5)
    draw(ax, S0, 16, 80, r"$S_0$")
    draw(ax, Ss, 24, 80, r"$S_s$")
    arrow(ax, (76, S0.y(76) - 2), (76, Ss.y(76) + 2))

    E0, E1 = meet(D, S0), meet(D, Ss)
    Q1, P1 = E1
    A = (Q1, S0.y(Q1))
    dots(ax, O[0], P1, Q1, E0[1])               # consumer benefit
    hatch(ax, O[0], E0[1], Q1, A[1], "////")    # producer benefit
    guide(ax, E0, O, r"$P_0$", r"$Q_0$")
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, A, O, r"$P_2$", to_x=False)
    for p in (E0, E1, A):
        dot(ax, *p)
    sign(ax, E0[0] - 3.5, E0[1] - 8.5, r"$E_0$")
    label(ax, Q1 - 1, A[1] + 4, "A")
    label(ax, Q1 - 3.5, P1 - 7, r"$E_1$")
    leader(ax, (Q1 + 9, A[1] + 1), (Q1 + 1, A[1]), "MC", ha="left")
    leader(ax, (Q1 + 9, P1 + 1), (Q1 + 1.2, P1), "MB", ha="left")

    key(ax, 34, 93, T("Consumer benefit", "消費者得益"), "....")
    key(ax, 34, 87, T("Producer benefit", "生產者得益"), "////")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"28_unit_subsidy_{lang}.png"))
