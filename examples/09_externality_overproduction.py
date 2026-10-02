"""Negative externality in production: overproduction and deadweight loss.

Topic: Other
Use for: negative externality: overproduction and deadweight loss (MSC above MPC)

Marking-scheme points it shows:
  - MSC above MPC (external cost); D = MPB = MSB
  - market output Qm where D = MPC; efficient output Q* where D = MSC
  - Qm > Q*  (overproduction)
  - deadweight loss: triangle between MSC and D from Q* to Qm
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 94), T("Quantity", "數量"), T("Price / cost", "價格／成本"))

    D = Line((12, 86), (80, 24))
    MPC = Line((12, 16), (80, 70))
    MSC = MPC.shift(dy=16)
    draw(ax, D, 12, 80, "D = MPB = MSB", dy=-1.5)
    draw(ax, MPC, 12, 80, "MPC", dy=0)
    draw(ax, MSC, 12, 76, "MSC", dy=0)

    Qm, Pm = meet(D, MPC)
    Qs, Ps = meet(D, MSC)
    dot(ax, Qm, Pm); dot(ax, Qs, Ps)
    region(ax, [(Qs, Ps), (Qm, MSC.y(Qm)), (Qm, Pm)], "////", border=True)

    guide(ax, (Qm, Pm), O, r"$P_m$", r"$Q_m$")
    guide(ax, (Qs, Ps), O, r"$P^*$", r"$Q^*$")
    cx, cy = (Qs + 2 * Qm) / 3, (Ps + MSC.y(Qm) + Pm) / 3     # centroid
    leader(ax, (44, 84), (cx, cy + 1), T("Deadweight\nloss", "無謂損失"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"09_externality_overproduction_{lang}.png"))
