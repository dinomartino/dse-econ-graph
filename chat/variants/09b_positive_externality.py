"""Positive externality in consumption: under-consumption and deadweight loss.

Topic: Other
Use for: positive externality in consumption (education, vaccination, public
  transport ...): MSB above MPB, so the market consumes too little; no
  marking-scheme ID yet (chat-only variant, drawn from the syllabus)

Variant of: 09_externality_overproduction

Marking-scheme points it shows:
  - MSB above MPB (external benefit); D = MPB; S = MPC = MSC
  - market output Qm where D = S; efficient output Q* where MSB = S
  - Qm < Q*  (under-consumption)
  - deadweight loss: triangle between MSB and S from Qm to Q*
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 94), T("Quantity", "數量"), T("Price / cost", "價格／成本"))

    S = Line((12, 18), (80, 72))
    D = Line((12, 72), m=-0.75)
    MSB = D.shift(dy=22)
    draw(ax, S, 12, 80, "S = MPC = MSC", dy=0)
    draw(ax, D, 12, 70, "D = MPB", dy=-1.5)
    draw(ax, MSB, 16, 80, "MSB", dy=-1.5)

    Qm, Pm = meet(D, S)
    Qs, Ps = meet(MSB, S)
    dot(ax, Qm, Pm); dot(ax, Qs, Ps)
    region(ax, [(Qm, Pm), (Qm, MSB.y(Qm)), (Qs, Ps)], "////", border=True)

    guide(ax, (Qm, Pm), O, r"$P_m$", r"$Q_m$")
    guide(ax, (Qs, Ps), O, xlab=r"$Q^*$", to_y=False)
    cx, cy = (2 * Qm + Qs) / 3, (Pm + MSB.y(Qm) + Ps) / 3     # centroid
    leader(ax, (44, 88), (cx, cy + 1), T("Deadweight\nloss", "無謂損失"))
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"09b_positive_externality_{lang}.png"))
