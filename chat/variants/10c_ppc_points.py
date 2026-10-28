"""Production possibilities curve (PPC): points inside, on and outside the curve.

Topic: Other
Use for: what a point inside, on or outside the PPC means (unemployment /
  inefficiency, efficiency, unattainable) with no shift (chat-only variant of 10)

Variant of: 10_ppc

Marking-scheme points it shows:
  - PPC concave to the origin (increasing opportunity cost)
  - point on the curve (B): efficient; inside (A): unemployment / inefficiency;
    outside (C): unattainable with current resources
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 98), T("Consumer goods", "消費品"), T("Capital goods", "資本品"))

    def pt(s, t):                      # point at angle t on the PPC scaled by s
        return (O[0] + s * 55 * math.cos(t), O[1] + s * 60 * math.sin(t))

    ts = [i * (math.pi / 2) / 80 for i in range(81)]
    pts = [pt(1.0, t) for t in ts]
    curve(ax, [p[0] for p in pts], [p[1] for p in pts])
    q = pt(1.0, 0.0)
    label(ax, q[0], q[1] - 1.8, "PPC", va="top")

    a = math.radians(50)
    B, A, C = pt(1.0, a), pt(0.6, a), pt(1.25, a)
    for p, n, dx, dy in ((A, "A", 2.5, -2.5), (B, "B", 2.5, 2.2), (C, "C", 2.5, 2.2)):
        dot(ax, *p); label(ax, p[0] + dx, p[1] + dy, n)

    kx = 66
    label(ax, kx, 90, T("A: unemployment / inefficiency", "A：失業／沒有效率"), ha="left")
    label(ax, kx, 84, T("B: efficient", "B：有效率"), ha="left")
    label(ax, kx, 78, T("C: unattainable", "C：無法達到"), ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gallery", "chat")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"10c_ppc_points_{lang}.png"))
