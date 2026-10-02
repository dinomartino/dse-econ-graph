"""Price (fare / price floor) set ABOVE equilibrium -> excess supply and deadweight loss.

Topic: Price controls and efficiency
Use for: a fixed fare or price floor above equilibrium when the question asks
  about deadweight loss; a minimum wage with DWL (DSE2018 Q10(c): relabel the
  axes Wage rate / Quantity of labour); a raised price floor (DSE2014 Q3)
  (DSE2019 Q11(b), DSE2014 Q3, DSE2018 Q10(c))

Marking-scheme points it shows:
  - price P above the equilibrium price
  - quantity transacted Q read off D (the short side), solid line from Q up to P
  - deadweight loss DL: triangle between D and S from Q to Qe
  - excess supply at P (Q to Qs)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 74), (78, 20))
    S = Line((18, 22), (74, 84))
    draw(ax, D, 18, 78, "D", dy=-1.5)
    draw(ax, S, 18, 74, "S", end="top")

    Qe, Pe = meet(D, S)
    P = 64                                     # set above Pe
    Q, Qs = D.x(P), S.x(P)
    region(ax, [(Q, P), (Q, S.y(Q)), (Qe, Pe)], "xxxx", border=True)
    sign(ax, (2 * Q + Qe) / 3, (P + S.y(Q) + Pe) / 3, "DL")
    line(ax, (Q, O[1]), (Q, P))
    label(ax, Q, O[1] - 1.8, "Q", va="top")
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    brace(ax, Q, Qs, P + 1, T("excess supply", "超額供應"), side="above")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"25_price_floor_deadweight_loss_{lang}.png"))
