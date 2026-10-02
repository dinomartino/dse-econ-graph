"""Consumer surplus and producer surplus at the market equilibrium.

Topic: Consumer and producer surplus
Use for: show (or name) consumer surplus and producer surplus in a market
  (DSESP Q9(a))

Marking-scheme points it shows:
  - D and S, a price line from the equilibrium to the price axis
  - C.S.: the triangle under D and above the price
  - P.S.: the triangle above S and below the price
  - a text legend: C.S. = consumer surplus, P.S. = producer surplus
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.6, 2.6)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 92), T("Quantity", "數量"), T("Price ($)", "價格 ($)"))

    D = Line((12, 86), (70, 20))
    S = Line((12, 34), (76, 80))
    draw(ax, D, 12, 70, "D", dy=-1.5)
    draw(ax, S, 12, 76, "S", dy=1.5)

    q, p = meet(D, S)
    line(ax, (O[0], p), (q, p))
    label(ax, O[0] + (q - O[0]) / 3, (D.y(12) + 2 * p) / 3, "C.S.")
    label(ax, O[0] + (q - O[0]) / 3, (S.y(12) + 2 * p) / 3, "P.S.")

    label(ax, 58, 46, T("C.S. = Consumer surplus", "C.S. = 消費者盈餘"), ha="left")
    label(ax, 58, 39, T("P.S. = Producer surplus", "P.S. = 生產者盈餘"), ha="left")
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"32_consumer_producer_surplus_{lang}.png"))
