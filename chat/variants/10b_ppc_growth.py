"""Economic growth: the production possibilities curve (PPC) shifts outward.

Topic: Other
Use for: economic growth (more labour or capital, better technology) shown on a PPC
  (chat-only variant: 10 without the points)

Variant of: 10_ppc

Marking-scheme points it shows:
  - PPC0 concave to the origin
  - outward shift PPC0 -> PPC1 (arrow) = economic growth
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 98), T("Consumer goods", "消費品"), T("Capital goods", "資本品"))

    def pt(s, t):                      # point at angle t on the PPC scaled by s
        return (O[0] + s * 55 * math.cos(t), O[1] + s * 60 * math.sin(t))

    k = 74 / 55
    ts = [i * (math.pi / 2) / 80 for i in range(81)]
    for s, n in ((1.0, "0"), (k, "1")):
        pts = [pt(s, t) for t in ts]
        curve(ax, [p[0] for p in pts], [p[1] for p in pts])
        q = pt(s, 0.0)
        label(ax, q[0], q[1] - 1.8, f"PPC$_{n}$", va="top")

    g0, g1 = pt(1.0, math.radians(45)), pt(k, math.radians(45))
    arrow(ax, (g0[0] + 1.5, g0[1] + 1.5), (g1[0] - 1.5, g1[1] - 1.5), head=0.9)
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"10b_ppc_growth_{lang}.png"))
