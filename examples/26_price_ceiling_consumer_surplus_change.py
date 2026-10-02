"""Price ceiling BELOW equilibrium -> change in consumer surplus (gain "+" and loss "−").

Topic: Price controls and efficiency
Use for: how a price ceiling changes consumer surplus: buyers who still get the
  good pay less (+), the units no longer sold are lost (−)
  (DSEPP Q4(b)(i))

Marking-scheme points it shows:
  - ceiling Pc below the equilibrium price Pe; quantity transacted Qs (on S)
  - gain "+": rectangle (Pe - Pc) x Qs
  - loss "−": triangle between D and the Pe line, from Qs to Qe
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 86), (80, 24))
    S = Line((22, 16), (76, 82))
    draw(ax, D, 16, 84, "D", dy=-1.5)
    draw(ax, S, 22, 76, "S", end="top")

    Qe, Pe = meet(D, S)
    Pc = 26                                    # ceiling, below Pe
    Qs = S.x(Pc)
    region(ax, [(O[0], Pc), (Qs, Pc), (Qs, Pe), (O[0], Pe)], "////", border=True)
    region(ax, [(Qs, Pe), (Qs, D.y(Qs)), (Qe, Pe)], "////", border=True)
    sign(ax, (O[0] + Qs) / 2, (Pc + Pe) / 2, "+", size=SIZE + 2)
    sign(ax, (2 * Qs + Qe) / 3, (2 * Pe + D.y(Qs)) / 3, "−", size=SIZE + 2)
    dot(ax, Qe, Pe)
    line(ax, (Qs, O[1]), (Qs, D.y(Qs)))
    label(ax, Qs, O[1] - 1.8, r"$Q_s$", va="top")
    line(ax, (O[0], Pc), (86, Pc))
    label(ax, O[0] - 1.5, Pc, r"$P_c$", ha="right")
    label(ax, O[0] - 1.5, Pe, r"$P_e$", ha="right")
    guide(ax, (Qe, Pe), O, xlab=r"$Q_e$", to_y=False)
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"26_price_ceiling_consumer_surplus_change_{lang}.png"))
