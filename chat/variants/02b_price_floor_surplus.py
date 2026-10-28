"""Price floor ABOVE equilibrium in a goods market -> surplus (excess supply).

Topic: Price fixed away from equilibrium
Use for: a price floor / fixed price ABOVE equilibrium in a goods market causes a
  surplus; for a minimum wage use 02, for the deadweight loss use 25
  (chat-only variant of 02 with goods-market axes)

Variant of: 02_price_floor_surplus

Marking-scheme points it shows:
  - price floor (Pf) above the equilibrium price (Pe)
  - correct position of the surplus / excess supply (Qd to Qs at Pf)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$P_e$", to_x=False)

    P = 66                                     # price floor, above Pe
    qd, qs = D.x(P), S.x(P)
    line(ax, (O[0], P), (84, P))
    label(ax, O[0] - 1.5, P, r"$P_f$", ha="right")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    dashed(ax, (qs, O[1]), (qs, P)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    brace(ax, qd, qs, P + 1, T("surplus", "盈餘"), side="above")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"02b_price_floor_surplus_{lang}.png"))
