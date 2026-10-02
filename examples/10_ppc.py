"""Production possibilities curve (PPC) and economic growth.

Topic: Other
Use for: production possibilities curve: efficiency, unemployment and growth

Marking-scheme points it shows:
  - PPC concave to the origin (increasing opportunity cost)
  - point on the curve (B): efficient; inside (A): unemployment / inefficiency;
    outside (C): unattainable with current resources
  - outward shift of the PPC (PPC1) = economic growth
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 98), T("Consumer goods", "消費品"), T("Capital goods", "資本品"))

    def pt(s, t):                      # point at angle t on the PPC scaled by s
        return (O[0] + s * 55 * math.cos(t), O[1] + s * 60 * math.sin(t))

    ts = [i * (math.pi / 2) / 80 for i in range(81)]
    for s, ls in ((1.0, "-"), (74 / 55, (0, (4, 3)))):
        pts = [pt(s, t) for t in ts]
        curve(ax, [p[0] for p in pts], [p[1] for p in pts], ls=ls)
    label(ax, 12 + 74, 12 - 1.8, r"PPC$_1$", va="top")
    q = pt(1.0, 0.0)
    label(ax, q[0], q[1] - 1.8, r"PPC$_0$", va="top")

    B, A, C = pt(1.0, math.radians(50)), pt(0.6, math.radians(50)), pt(1.17, math.radians(50))
    for p, n, dx, dy in ((A, "A", 2.5, -2.5), (B, "B", 2.5, 2.2), (C, "C", 2.5, 2.2)):
        dot(ax, *p); label(ax, p[0] + dx, p[1] + dy, n)

    g0, g1 = pt(1.0, math.radians(75)), pt(74 / 55, math.radians(75))
    arrow(ax, (g0[0] + 1, g0[1] + 1), (g1[0] - 0.5, g1[1] + 0.5), head=0.9)
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"10_ppc_{lang}.png"))
