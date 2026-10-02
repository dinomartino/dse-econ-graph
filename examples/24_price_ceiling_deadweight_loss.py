"""Price ceiling BELOW equilibrium -> shortage and deadweight loss.

Topic: Price controls and efficiency
Use for: a price ceiling or controlled price below equilibrium when the question
  asks about efficiency / deadweight loss
  (DSEPP Q4(b)(ii), DSE2016 Q11(b), DSE2014)

Marking-scheme points it shows:
  - ceiling Pc below the equilibrium price; D = MB, S = MC
  - quantity transacted Qc read off S (the short side), solid line up to D
  - deadweight loss DL: triangle between D and S from Qc to Qe
  - shortage at Pc (Qc to Qd)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 84), (80, 24))
    S = Line((22, 18), (70, 82))
    draw(ax, D, 16, 80, "D = MB", dy=-1.5)
    draw(ax, S, 22, 70, "S = MC", end="top")

    Qe, Pe = meet(D, S)
    Pc = 34                                    # ceiling, below Pe
    Qc, Qd = S.x(Pc), D.x(Pc)
    region(ax, [(Qc, Pc), (Qc, D.y(Qc)), (Qe, Pe)], "////", border=True)
    sign(ax, (2 * Qc + Qe) / 3, (Pc + D.y(Qc) + Pe) / 3, "DL")
    line(ax, (Qc, O[1]), (Qc, D.y(Qc)))
    label(ax, Qc, O[1] - 1.8, r"$Q_c$", va="top")
    line(ax, (O[0], Pc), (86, Pc))
    label(ax, O[0] - 1.5, Pc, r"$P_c$", ha="right")
    dashed(ax, (Qd, O[1]), (Qd, Pc)); label(ax, Qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, Qc, Qd, Pc - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"24_price_ceiling_deadweight_loss_{lang}.png"))
