"""Price fixed ABOVE equilibrium; demand falls -> quantity sold and sales revenue fall.

Topic: Price fixed away from equilibrium
Use for: a price kept above equilibrium when demand falls: the quantity sold is
  Qd, so sales revenue falls by P x (Q1 - Q2); reverse the shift for a rise
  (CE2004 Q10(a), CE2002 Q11(b))

Marking-scheme points it shows:
  - fixed price P above equilibrium; leftward shift D1 -> D2 (arrow)
  - excess supply at P after the change (Q2 to Qs)
  - quantity sold (= Qd) falls from Q1 to Q2
  - fall in sales revenue = P x (Q1 - Q2), hatched with a key
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    P = 58                                     # fixed price, above equilibrium
    S = Line((20, 22), (74, P))
    D1 = Line((70, P), m=-1.6)
    D2 = D1.shift(dx=-30)
    draw(ax, S, 20, 82, "S", dy=1.5)
    draw(ax, D1, D1.x(86), 86, r"$D_1$", end="left")
    draw(ax, D2, D2.x(86), 60, r"$D_2$", end="left")
    arrow(ax, (D1.x(86) - 8, 86), (D2.x(86) + 2, 86))

    q1, q2, qs = D1.x(P), D2.x(P), S.x(P)
    hatch(ax, q2, O[1], q1, P)                 # fall in sales revenue
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    label(ax, q1, O[1] - 1.8, r"$Q_1$", va="top")
    label(ax, q2, O[1] - 1.8, r"$Q_2$", va="top")
    arrow(ax, (q1, 3), (q2, 3))                # quantity sold falls
    brace(ax, q2, qs, P + 1, side="above")
    label(ax, (q2 + q1) / 2 - 5, P + 7.5, T("excess supply", "超額供應"))   # left of D1
    key(ax, 58, 94, T("Fall in sales revenue", "銷售收入減少"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"22_fixed_price_surplus_revenue_fall_{lang}.png"))
