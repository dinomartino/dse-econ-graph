"""Fixed stock (vertical supply) increases on ELASTIC (flat) demand -> total value rises.

Topic: Total revenue and elasticity
Use for: more taxi licences (land, flats ...) are issued and demand is elastic, so
  the price falls but the total value of all licences rises
  (CE1992 Q1(d)(ii))

Marking-scheme points it shows:
  - vertical supply S shifts right to S' (arrow), flat (elastic) demand D
  - equilibria E1, E2: price falls P1 -> P2, quantity rises Q1 -> Q2
  - gain (Q1..Q2 x 0..P2) marked "+", loss (P2..P1 x 0..Q1) marked "-"
  - gain > loss, so the total value of licences rises
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.7)
    O = (12, 12)
    axes(ax, O, (86, 12), (12, 92), T("Quantity of\ntaxi licences", "的士牌照\n數量"),
         T("Price of a taxi licence", "的士牌照價格"))

    S1, S2 = Line.vertical(40), Line.vertical(62)
    D = Line((20, 70), m=-0.45)
    draw(ax, S1, name="S", y0=O[1], y1=84, end="top")
    draw(ax, S2, name="S’", y0=O[1], y1=84, end="top")
    draw(ax, D, 20, 76, "D", dy=-1.5)
    arrow(ax, (S1.vx + 2, 78), (S2.vx - 2, 78))

    (q1, p1), (q2, p2) = E1, E2 = meet(S1, D), meet(S2, D)
    hatch(ax, O[0], p2, q1, p1)                # loss
    dots(ax, q1, O[1], q2, p2)                 # gain
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 2, E[1] + 1.5, f"$E_{n}$", ha="left", va="bottom")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    sign(ax, (O[0] + q1) / 2, (p1 + p2) / 2, "−", size=SIZE + 2)
    sign(ax, (q1 + q2) / 2, (O[1] + p2) / 2, "+", size=SIZE + 2)
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))  # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))  # quantity rises
    return fig


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery")
    os.makedirs(out, exist_ok=True)
    for lang in ("en", "zh"):
        save(diagram(lang), os.path.join(out, f"19_tr_vertical_supply_increase_{lang}.png"))
