---
name: dse-econ-graph
description: Draw HKDSE / HKCEE Economics diagrams as copy-paste Python code that reproduces the black-and-white HKEAA marking-scheme style, in English or Traditional Chinese — demand and supply, shortage / surplus, price ceilings and floors, minimum wage, total revenue and elasticity, unit tax incidence, consumer / producer surplus and deadweight loss, quotas, externalities, PPC. Use whenever someone asks to draw, redraw, recreate or clean up an economics graph or diagram for DSE (or any exam in that style), to replace a blurry scanned or AI-coloured graph, or to answer a "with the aid of a diagram" question.
---

# DSE Economics diagrams in code

Recreate exam-quality economics diagrams — the kind printed in HKEAA marking
schemes — by writing a short Python (matplotlib) script. The look is fixed:
black on white, Times-style serif (Chinese: Ming/Song serif), thin lines,
arrow-headed axes, dashed guide lines, `////` hatching and `....` dotted
fills, curly braces for shortages. No colour, no grid, no title box.

This file is self-contained. The whole drawing library, `dsegraph`, is at the
end ("The library"); any assistant — including a web chat with no files —
can paste it into the script it writes.

## What you give the user

Assume the user is a teacher or student who **does not code** — most of
them use **Gemini** in the browser. They want the picture, not the program.

### A. You cannot run code yourself (Gemini, most web chats)

Give **one short Python script in one code block**: the 5-line loader
below, then the diagram code. Do NOT paste the whole library — the loader
fetches it, and a short script is easier to copy and has nothing to mistype.

```python
# DSE graph library — downloads automatically, do not edit
import os, urllib.request
if not os.path.exists("dsegraph.py"):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/dinomartino/dse-econ-graph/main/dsegraph.py", "dsegraph.py")
from dsegraph import *
```

After the code block, give these steps in the user's language, exactly:

> **How to get the picture (no coding needed)**
> 1. Click **Export to Colab** under the code (Gemini: the share / ⋮ menu
>    of the code box). No such button? Copy the code, open
>    https://colab.research.google.com/github/dinomartino/dse-econ-graph/blob/main/DSE_Graph_Maker.ipynb
>    and paste it into **Step 2**.
> 2. Press **▶** (or **Runtime ▸ Run all**). Sign in with Google if asked;
>    if it says *"Run anyway?"*, click **Run anyway**.
> 3. The picture appears under the code and downloads to your computer.
>    The first run takes about a minute.

> **如何取得圖片（不需識寫程式）**
> 1. 按程式碼下方的 **Export to Colab（匯出至 Colab）**（Gemini：程式碼框的分享／⋮ 選單）。沒有這個按鈕？複製程式碼，打開
>    https://colab.research.google.com/github/dinomartino/dse-econ-graph/blob/main/DSE_Graph_Maker.ipynb
>    貼到 **Step 2**。
> 2. 按 **▶**（或 **執行階段 ▸ 全部執行**）。如要求登入 Google 請登入；見到「仍要執行」請按 **仍要執行**。
> 3. 圖片會在程式碼下方出現，並自動下載到你的電腦。第一次執行約需一分鐘。

If the user reports an error, ask them to copy the red error text to you,
fix the code, and give the whole corrected script again (never a partial
patch — they cannot merge code).

### B. You can run Python yourself (Claude with code execution, ChatGPT)

Write the script, RUN it, look at the PNG, fix every problem from the
checklist, then give the user **the PNG files** to download. Offer the code
only as an extra. Use the loader above if the sandbox has internet;
otherwise paste the full library from "The library" at the top of the
script. Chinese fonts are handled by `setup("zh")`: an installed Chinese
serif, else a font file the user uploaded, else Noto Serif TC downloaded
once. If there is no internet and no Chinese font, ask the user to upload
any Chinese `.ttf` / `.otf` and run again.

### Either way

- Both languages unless the user says otherwise: the script saves
  `diagram_en.png` and `diagram_zh.png` (300 dpi); `.svg` only if asked.
- When the user asks for a change in words ("move 'shortage' lower", "make
  demand steeper", "Chinese only"), change the code and deliver again the
  same way. Never ask them to edit code.
- "The library" section below is the reference for every function you
  may call — read it; don't invent functions that are not there.

## Workflow

1. **Read the question and the marking scheme.** List every point the
   scheme says to "indicate / illustrate in the diagram" — each must be
   visible in the picture, labelled as the scheme names it.
2. **Decide the economics before any coordinate**: which market and axes,
   which curves, which one shifts and which way, whether demand / supply is
   elastic (flat) or inelastic (steep), which price is fixed, which areas
   are shaded and which must be bigger.
3. **Build with `Line` objects and compute every point.** `meet(D, S)` for
   an equilibrium, `D.x(P)` for the quantity demanded at price P,
   `S.shift(dx=10)` for an increase in supply, `S.shift(dy=t)` for a unit
   tax. Never type a coordinate for something that should sit on a curve.
4. **Lay it out** following the style rules, then **check** against the
   checklist at the end of this section.

### Economics that is easy to get wrong

- Increase in demand / supply = shift **right**; decrease = shift **left**.
  Label the old and new curves (D₀ → D₁ or D₁ → D₂, whatever the question
  uses) and put a short arrow between them pointing the way of the shift.
- Price ceiling / fixed price **below** equilibrium → shortage
  (excess demand) = Qd − Qs **on the fixed-price line**. Price floor /
  minimum wage **above** equilibrium → surplus (excess supply). Quantity
  transacted is the SMALLER of Qd and Qs.
- With a fixed price, a shift changes the size of the shortage, not the
  price: brace the old gap (a) and the new gap (b) on the same price line.
- Fixed stock (land, taxi licences, public housing units, tickets,
  seats) → **vertical** supply.
- Total revenue / expenditure diagrams: the price-change rectangle is
  |ΔP| × (the quantity that stays), the quantity-change rectangle is
  |ΔQ| × (the price that stays). Elastic demand → draw D **flat**, so the
  quantity rectangle is clearly bigger; inelastic → **steep**, so the price
  rectangle is clearly bigger. Make the stated inequality obvious (at least
  ~1.5×), and mark the areas "+" and "−" (or "gain" / "loss").
- Unit tax: supply shifts **up by t** (vertical distance), consumers pay
  Pc, producers receive Pc − t; tax revenue = t × new quantity.
- Labour market: y-axis wage rate, x-axis number of workers / quantity of
  labour; firms demand labour, workers supply it.
- Negative production externality: MSC above MPC; market output Qm (D ∩
  MPC) > efficient Q* (D ∩ MSC); deadweight loss = triangle between MSC
  and D from Q* to Qm.
- PPC is concave to the origin; a point inside = unemployment /
  inefficiency, outside = unattainable; growth = outward shift.

### Style rules (HKEAA marking-scheme look)

- `new(w, h)` at the size the picture will print (inches; default 3.2 × 2.6).
  Text is 10.5 pt at that size, the same as the papers. Do not shrink text
  to make things fit — make the picture bigger or move things.
- Axes with `axes()`: y title **above** the y-arrow, x title **right of**
  the x-arrow (split a long one with `\n`), `0` at the origin.
- Curves are straight thin lines, named at one end (`D`, `S`, `S₁`, `MSC`).
  Equilibrium points may get a `dot()` and a name (`E`, `E₁`) when the
  scheme mentions them.
- Guides to the axes are dashed (`guide()`), labelled `P₁`, `Q₁` on the axes.
- Gaps are curly braces (`brace()` horizontal, `vbrace()` vertical) with the
  word beyond the tip ("shortage", "excess supply", "a", "b", "t").
  No room at a crowded spot? Put the word nearby with `leader()` (text + thin
  arrow).
- Areas: `hatch()` `////`, `dots()` `....`, or `region()` for triangles —
  a different pattern for each area, labelled with `sign()` (white patch)
  or a small `key()` legend. Greyscale only: never colour.
- Subscripts with mathtext: `r"$P_1$"`, `r"$Q_{d}$"`, `r"$S'$"` → write a
  prime as `"S’"` (plain text) because mathtext lifts `'` too high.

### English and Chinese

- `setup("en")` or `setup("zh")` first; write every word as
  `T("English", "中文")` so one script makes both versions.
- **Never put Chinese inside `$...$`** (mathtext cannot draw it); put the
  Chinese as plain text beside the symbol.
- In Chinese papers the curve letters and symbols stay English
  (D, S, MPC, P₁, Q₂, E); only words are translated.
- Fonts are picked automatically: Times New Roman (fallback: the STIX
  font that ships with matplotlib) + the first Chinese serif found
  (PMingLiU / MingLiU on Windows, Songti TC on macOS, Noto Serif CJK TC on
  Linux), else an uploaded font file, else Noto Serif TC downloaded once.
- Use the HKEAA / EDB wording:

| English | 中文 | English | 中文 |
|---|---|---|---|
| Price | 價格 | Quantity | 數量 |
| Unit price | 單位價格 | Quantity transacted | 交易量 |
| Wage rate | 工資率 | Number of workers | 工人數目 |
| Demand / Supply | 需求 / 供應 | Equilibrium price | 均衡價格 |
| Shortage | 短缺 | Surplus | 盈餘 |
| Excess demand | 超額需求 | Excess supply | 超額供應 |
| Total revenue | 總收入 | Total expenditure | 總開支 |
| Price ceiling | 價格上限 | Price floor | 價格下限 |
| Minimum wage | 最低工資 | Quota | 配額 |
| Unit tax | 從量稅 | Tax revenue | 政府稅收 |
| Consumers' burden | 消費者負擔 | Producers' burden | 生產者負擔 |
| Consumer surplus | 消費者盈餘 | Producer surplus | 生產者盈餘 |
| Deadweight loss | 無謂損失 | Subsidy | 津貼 |
| Marginal private cost | 邊際私人成本 | Marginal social cost | 邊際社會成本 |
| Marginal private benefit | 邊際私人利益 | Marginal social benefit | 邊際社會利益 |
| Production possibilities curve | 生產可能曲線 | Capital goods / Consumer goods | 資本品 / 消費品 |

### Checklist before you hand it over

- [ ] Every "indicate in the diagram" point from the marking scheme is there.
- [ ] Every labelled point is computed, and sits exactly on its curves.
- [ ] Shifts go the right way, the arrow says so, old and new are labelled.
- [ ] Elastic = flat, inelastic = steep; the bigger area really is bigger.
- [ ] No label touches a line or another label; no dashed guide runs
      through text; nothing is cut off. Check the Chinese version
      separately — Chinese labels are wider.
- [ ] Black and white only; same fonts and line weights as the library.
- [ ] Both `en` and `zh` render if the user wants both.

## Templates

Tested starting points, in `examples/` of the repository (PNG output in
`gallery/`). Pick the closest, then adapt it to the question. Every one
makes an English and a Chinese version.

<!-- BEGIN TEMPLATE LIST -->
- `01_price_ceiling_shortage.py` — Price set BELOW equilibrium (price ceiling / fixed low price) -> shortage.
- `02_price_floor_surplus.py` — Minimum wage ABOVE equilibrium in a labour market -> unemployment.
- `03_demand_increase_fixed_price.py` — Price fixed BELOW equilibrium; demand increases -> shortage grows.
- `04_vertical_supply_shortage.py` — Perfectly inelastic (vertical) supply, price set BELOW equilibrium -> shortage.
- `05_tr_price_change_elastic.py` — Price falls on ELASTIC (flat) demand -> total revenue rises.
- `06_tr_supply_decrease_inelastic.py` — Supply decreases on INELASTIC (steep) demand -> total revenue rises.
- `07_unit_tax_incidence.py` — Per-unit tax: incidence and tax revenue.
- `08_surplus_deadweight_quota.py` — A quota (Qq) set BELOW the equilibrium quantity (Qe): consumer surplus,
- `09_externality_overproduction.py` — Negative externality in production: overproduction and deadweight loss.
- `10_ppc.py` — Production possibilities curve (PPC) and economic growth.
<!-- END TEMPLATE LIST -->

A complete template, to show the pattern (for a web chat, this is the
whole script you hand over):

<!-- BEGIN EXAMPLE 01 -->
```python
"""Price set BELOW equilibrium (price ceiling / fixed low price) -> shortage.

Marking-scheme points it shows:
  - price (P) below the equilibrium price (Pe)
  - correct position of the shortage / excess demand (Qs to Qd at P)
"""
# DSE graph library — downloads automatically, do not edit
import os, urllib.request
if not os.path.exists("dsegraph.py"):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/dinomartino/dse-econ-graph/main/dsegraph.py", "dsegraph.py")
from dsegraph import *


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$P_e$", to_x=False)

    P = 34                                     # the fixed price, below Pe
    qs, qd = S.x(P), D.x(P)
    line(ax, (O[0], P), (84, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    dashed(ax, (qs, O[1]), (qs, P)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, qs, qd, P - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```
<!-- END EXAMPLE 01 -->

### Replacing a picture in Word

To drop a redraw into an existing Word document without moving the layout,
draw at the picture's frame size and save with the original's aspect ratio:
`save(fig, "new.png", aspect=orig_width / orig_height)` — the PNG is padded
with white to exactly that shape.

## The library

Paste this whole block at the top of every script (or save it as
`dsegraph.py` and `from dsegraph import *`). Needs `matplotlib >= 3.6` and
`pillow`.

<!-- BEGIN dsegraph.py -->
```python
"""dsegraph — HKDSE / HKCEE Economics diagrams in the HKEAA marking-scheme style.

Black on white, Times-style serif (Chinese: Ming/Song serif), thin lines,
arrow-headed axes, dashed guide lines, "////" hatching and "...." dotted
fills, curly braces for shortages and surpluses.  English and Chinese.

Only needs matplotlib (>= 3.6).  Every diagram is drawn on a 0..100 x 0..100
canvas; the economic axes go wherever you put them with `axes()`.

    from dsegraph import *
    setup("en")                                   # or setup("zh")
    fig, ax = new(3.2, 2.6)                       # printed size, inches
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))
    D = Line((20, 85), (80, 25)); S = Line((20, 25), (80, 85))
    draw(ax, D, 20, 80, "D"); draw(ax, S, 20, 80, "S")
    E = meet(D, S); dot(ax, *E); guide(ax, E, O, r"$P_e$", r"$Q_e$")
    save(fig, "market.png")
"""
from __future__ import annotations

import glob
import io
import os
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path

__all__ = ["setup", "T", "new", "axes", "Line", "meet", "draw", "line",
           "dashed", "guide", "label", "arrow", "hatch", "dots", "region",
           "brace", "vbrace", "dot", "sign", "key", "leader", "curve", "save",
           "SIZE", "LW"]

SIZE = 10.5          # pt at printed size — matches the exam papers
LW = 0.8             # pt, curves and axes
GUIDE_LW = 0.7       # pt, dashed guides and area borders
LANG = "en"
_READY = False

LATIN = ["Times New Roman", "Times", "Liberation Serif", "Nimbus Roman",
         "TeX Gyre Termes", "STIXGeneral"]            # STIX ships with matplotlib
CJK = ["PMingLiU", "MingLiU", "新細明體", "Songti TC", "LiSong Pro",
       "Noto Serif CJK TC", "Noto Serif TC", "Source Han Serif TC",
       "AR PL UMing TW", "AR PL UMing HK",
       "Noto Serif CJK SC", "Songti SC", "SimSun",           # simplified-only fallbacks
       "Microsoft JhengHei", "PingFang TC", "Heiti TC", "Noto Sans CJK TC"]


# Free Chinese serif (SIL Open Font Licence), fetched once when no Chinese
# font is installed — e.g. inside ChatGPT's or Claude's code sandbox.
CJK_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
           "notoseriftc/NotoSerifTC%5Bwght%5D.ttf")
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "dsegraph")
FONT_DIRS = [".", "/mnt/data", "/mnt/user-data/uploads", CACHE]   # cwd, chat uploads, cache


def _add_font(path):
    """Register a font file; return its family name (None if unusable)."""
    try:
        font_manager.fontManager.addfont(path)
        return font_manager.FontProperties(fname=path).get_name()
    except Exception:
        return None


def _cjk_from_files():
    for d in FONT_DIRS:
        for f in sorted(glob.glob(os.path.join(d, "*.[tToO][tT][fFcC]"))):
            name = _add_font(f)
            if name and any(k in name for k in ("CJK", "TC", "SC", "Ming", "Song", "Hei", "Kai", "宋", "明")):
                return name
    return None


def _cjk_download():
    path = os.path.join(CACHE, "NotoSerifTC.ttf")
    if not os.path.exists(path):
        try:
            import urllib.request
            os.makedirs(CACHE, exist_ok=True)
            print("dsegraph: downloading a Chinese font (Noto Serif TC, ~17 MB) - once only ...")
            urllib.request.urlretrieve(CJK_URL, path + ".part")
            os.replace(path + ".part", path)
        except Exception:
            return None
    return _add_font(path)


def _have(names):
    found = {f.name for f in font_manager.fontManager.ttflist}
    return [n for n in names if n in found]


def setup(lang: str = "en", size: float = SIZE, font: str | None = None):
    """Pick fonts for English ("en") or Traditional Chinese ("zh").

    Chinese text uses a Ming/Song serif like the HKEAA Chinese papers; the
    letters and numbers in the same label stay in the Times-style serif.
    Chinese font, in order: `font=` (path to a .ttf/.otf file) -> an
    installed one (PMingLiU, Songti TC, Noto Serif CJK TC ...) -> a font file
    uploaded next to the script / into the chat -> Noto Serif TC, downloaded
    once.  Works in Colab, ChatGPT and Claude sandboxes without setup."""
    global LANG, SIZE, _READY
    LANG, SIZE, _READY = lang, size, True
    latin = (_have(LATIN) or ["STIXGeneral"])[0]
    family = [latin]
    if lang == "zh":
        cjk = (_add_font(font) if font else None) or (_have(CJK) or [None])[0] \
            or _cjk_from_files() or _cjk_download()
        if cjk:
            family.append(cjk)
        else:
            warnings.warn("No Chinese font found and none could be downloaded; Chinese "
                          "labels will show as boxes. Upload a Chinese .ttf/.otf font "
                          "(e.g. Noto Serif TC from fonts.google.com) and run again.")
    plt.rcParams.update({
        "font.family": family,                 # per-glyph fallback: Latin first, then CJK
        "font.size": size,
        "axes.unicode_minus": False,
        "hatch.linewidth": 0.6, "hatch.color": "black",
        "svg.fonttype": "none",
    })
    if latin == "STIXGeneral":
        plt.rcParams["mathtext.fontset"] = "stix"
    else:
        plt.rcParams.update({"mathtext.fontset": "custom", "mathtext.rm": latin,
                             "mathtext.it": f"{latin}:italic", "mathtext.bf": f"{latin}:bold"})
    plt.rcParams["mathtext.default"] = "rm"    # upright P₁, Q₂ like the papers


def T(en: str, zh: str) -> str:
    """The label for the current language: T("Quantity", "數量")."""
    return zh if LANG == "zh" else en


# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------

def new(w_in: float = 3.2, h_in: float = 2.6):
    """A figure at its printed size (inches) with an invisible 0..100 canvas."""
    if not _READY:
        setup(LANG)
    fig = plt.figure(figsize=(w_in, h_in), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    return fig, ax


def arrow(ax, p, q, lw=LW, head=1.0):
    """Arrow from p to q: shift arrows, "price rises" arrows, axis heads."""
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={0.45*head},head_width={0.18*head}",
                                 mutation_scale=10, lw=lw, color="black",
                                 shrinkA=0, shrinkB=0, zorder=4))


def axes(ax, origin, x_end, y_end, xlabel="Quantity", ylabel="Price", zero="0"):
    """Arrow-headed axes.  The y title sits ABOVE the y-arrow, the x title to
    the RIGHT of the x-arrow, "0" below-left of the origin (exam layout).
    A long x title can be split with "\\n"."""
    arrow(ax, origin, x_end); arrow(ax, origin, y_end)
    if xlabel:
        ax.text(x_end[0] + 1.5, x_end[1], xlabel, ha="left", va="center", fontsize=SIZE)
    if ylabel:
        ax.text(y_end[0], y_end[1] + 2, ylabel, ha="center", va="bottom", fontsize=SIZE)
    if zero:
        ax.text(origin[0] - 1.5, origin[1] - 1.5, zero, ha="right", va="top", fontsize=SIZE)


# --------------------------------------------------------------------------
# exact geometry — compute every intersection, never eyeball it
# --------------------------------------------------------------------------

class Line:
    """A straight curve through p with slope m:  Line(p, q)  or  Line(p, m=-1.2).
    Vertical lines: Line.vertical(x)."""

    def __init__(self, p, q=None, m=None, x=None):
        self.vx = x
        if x is not None:
            return
        if q is not None:
            m = (q[1] - p[1]) / (q[0] - p[0])
        self.m, self.c = m, p[1] - m * p[0]

    @classmethod
    def vertical(cls, x):
        return cls(None, x=x)

    def y(self, x):
        if self.vx is not None:
            raise ValueError("vertical line has no y(x)")
        return self.m * x + self.c

    def x(self, y):
        if self.vx is not None:
            return self.vx
        return (y - self.c) / self.m

    def shift(self, dx=0.0, dy=0.0):
        """Parallel shift: dx>0 right (increase in D or S), dy>0 up (e.g. a unit tax)."""
        if self.vx is not None:
            return Line.vertical(self.vx + dx)
        return Line((0, self.c + dy - self.m * dx), m=self.m)


def meet(a: Line, b: Line):
    """Intersection point of two Lines."""
    if a.vx is not None:
        return (a.vx, b.y(a.vx))
    if b.vx is not None:
        return (b.vx, a.y(b.vx))
    x = (b.c - a.c) / (a.m - b.m)
    return (x, a.y(x))


def draw(ax, L: Line, x0=None, x1=None, name="", end="right", lw=LW, ls="-",
         y0=None, y1=None, dx=1.2, dy=0.0):
    """Draw Line L from x0 to x1 (vertical: from y0 to y1) and write its name
    just beyond one end ("right"/"left"/"top"/"bottom")."""
    if L.vx is not None:
        p, q = (L.vx, y0), (L.vx, y1)
    else:
        p, q = (x0, L.y(x0)), (x1, L.y(x1))
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=ls,
            solid_capstyle="butt", zorder=3)
    if name:
        if end == "top":
            hi = max(p, q, key=lambda t: t[1]); label(ax, hi[0] + dx * 0, hi[1] + 1.5 + dy, name, va="bottom")
        elif end == "bottom":
            lo = min(p, q, key=lambda t: t[1]); label(ax, lo[0], lo[1] - 1.5 + dy, name, va="top")
        elif end == "left":
            label(ax, p[0] - dx, p[1] + dy, name, ha="right")
        else:
            label(ax, q[0] + dx, q[1] + dy, name, ha="left")


def line(ax, p, q, lw=LW, ls="-"):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=ls,
            solid_capstyle="butt", zorder=3)


def curve(ax, xs, ys, lw=LW, ls="-"):
    """Any smooth curve (PPC, cost curves): pass the sampled points."""
    ax.plot(xs, ys, color="black", lw=lw, ls=ls, zorder=3)


def dashed(ax, p, q, lw=GUIDE_LW):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=(0, (4, 3)), zorder=2)


def guide(ax, pt, origin, ylab="", xlab="", to_y=True, to_x=True):
    """Dashed lines from a point to both axes, with its price / quantity labels."""
    x, y = pt
    if to_y:
        dashed(ax, (origin[0], y), (x, y))
        if ylab:
            label(ax, origin[0] - 1.5, y, ylab, ha="right")
    if to_x:
        dashed(ax, (x, origin[1]), (x, y))
        if xlab:
            label(ax, x, origin[1] - 1.8, xlab, va="top")


def label(ax, x, y, text, ha="center", va="center", size=None, **kw):
    """Text.  Subscripts with mathtext: r"$P_1$", r"$Q_{D0}$".  NEVER put
    Chinese inside $...$ — write it as plain text next to it."""
    ax.text(x, y, text, ha=ha, va=va, fontsize=size or SIZE, zorder=6, **kw)


def dot(ax, x, y, size=2.6):
    ax.plot([x], [y], "o", ms=size, color="black", zorder=7)


# --------------------------------------------------------------------------
# areas
# --------------------------------------------------------------------------

def hatch(ax, x0, y0, x1, y1, pattern="////", border=True):
    """Hatched rectangle (revenue gain/loss, tax revenue ...)."""
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, hatch=pattern,
                           lw=GUIDE_LW if border else 0, ec="black", zorder=1))


def dots(ax, x0, y0, x1, y1, border=True):
    hatch(ax, x0, y0, x1, y1, "....", border)


def region(ax, pts, pattern="////", border=False):
    """Any polygon (consumer / producer surplus, deadweight-loss triangle)."""
    ax.add_patch(Polygon(pts, closed=True, fill=False, hatch=pattern,
                         lw=GUIDE_LW if border else 0, ec="black", zorder=1))


def sign(ax, x, y, text, size=None):
    """A label on a small white patch so it reads over hatching: "+", "−", "A"."""
    ax.text(x, y, text, ha="center", va="center", fontsize=size or SIZE, zorder=8,
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))


def key(ax, x, y, text, pattern="////", w=8, h=4):
    """A small legend: a hatched swatch followed by its meaning."""
    hatch(ax, x, y - h / 2, x + w, y + h / 2, pattern)
    label(ax, x + w + 1.5, y, text, ha="left")


def leader(ax, text_xy, target_xy, text, ha="center", va="center"):
    """A label away from a crowded spot with a thin arrow to what it names
    ("deadweight loss" -> its triangle, "smaller shortage" -> a brace)."""
    label(ax, *text_xy, text, ha=ha, va=va)
    arrow(ax, text_xy, target_xy, lw=GUIDE_LW, head=0.8)


# --------------------------------------------------------------------------
# braces
# --------------------------------------------------------------------------

def _brace_path(a, b, k, depth, horizontal):
    s = 1 if depth > 0 else -1
    d = abs(depth)
    q = min(3.0, abs(b - a) / 4)
    m, h, t = (a + b) / 2, k + s * d / 2, k + s * d
    P = [(a, k), (a, h), (a + q, h), (m - q, h), (m, h), (m, t),
         (m, t), (m, h), (m + q, h), (b - q, h), (b, h), (b, k)]
    if not horizontal:
        P = [(y, x) for x, y in P]
    C = Path.CURVE3
    return Path(P, [Path.MOVETO, C, C, Path.LINETO, C, C, Path.MOVETO, C, C, Path.LINETO, C, C])


def brace(ax, x0, x1, y, text="", side="below", depth=2.5, gap=1.0):
    """Horizontal curly brace over [x0, x1] at height y, tip pointing to
    `side` ("below" / "above"), text beyond the tip (shortage, surplus ...)."""
    d = -depth if side == "below" else depth
    ax.add_patch(PathPatch(_brace_path(x0, x1, y, d, True), fill=False, lw=GUIDE_LW, ec="black", zorder=4))
    if text:
        label(ax, (x0 + x1) / 2, y + d + (-gap if d < 0 else gap), text,
              va="top" if d < 0 else "bottom")


def vbrace(ax, y0, y1, x, text="", side="left", depth=2.5, gap=1.0):
    """Vertical curly brace over [y0, y1] at x (a tax per unit, a price gap)."""
    d = -depth if side == "left" else depth
    ax.add_patch(PathPatch(_brace_path(y0, y1, x, d, False), fill=False, lw=GUIDE_LW, ec="black", zorder=4))
    if text:
        label(ax, x + d + (-gap if d < 0 else gap), (y0 + y1) / 2, text,
              ha="right" if d < 0 else "left")


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def _notebook(path):
    """In Colab / Jupyter: show the picture under the cell, and in Colab also
    download it — so "Export to Colab -> Run" is all a teacher has to do."""
    try:
        from IPython import get_ipython
        if get_ipython() is None:
            return
        from IPython.display import SVG, Image, display
        print(path)
        display(Image(path, width=420) if path.lower().endswith(".png") else SVG(path))
    except Exception:
        return
    try:
        from google.colab import files
        files.download(path)
    except Exception:
        pass


def save(fig, path="diagram.png", aspect: float | None = None):
    """PNG (greyscale, 300 dpi) or .svg / .pdf by extension.  The canvas grows
    to fit every label, so nothing is ever clipped.  `aspect` (w/h) pads the
    PNG with white to an exact ratio, e.g. to replace a picture in Word
    without moving the layout.  In a notebook the picture is also shown
    (and downloaded, in Colab)."""
    if not path.lower().endswith(".png"):
        fig.savefig(path, facecolor="white", bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
        _notebook(path)
        return path
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    im = Image.open(buf).convert("L")
    if aspect:
        w, h = im.size
        if abs(w / h - aspect) > 0.002:
            W, H = (w, round(w / aspect)) if w / h > aspect else (round(h * aspect), h)
            c = Image.new("L", (W, H), 255)
            c.paste(im, ((W - w) // 2, (H - h) // 2))
            im = c
    im.save(path, optimize=True)
    _notebook(path)
    return path
```
<!-- END dsegraph.py -->
