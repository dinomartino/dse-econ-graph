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

import io
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


def _have(names):
    found = {f.name for f in font_manager.fontManager.ttflist}
    return [n for n in names if n in found]


def setup(lang: str = "en", size: float = SIZE):
    """Pick fonts for English ("en") or Traditional Chinese ("zh").

    Chinese text uses a Ming/Song serif like the HKEAA Chinese papers; the
    letters and numbers in the same label stay in the Times-style serif.
    No CJK font installed (e.g. Google Colab)?  Run
        !apt-get -qq install fonts-noto-cjk
    and restart the runtime."""
    global LANG, SIZE, _READY
    LANG, SIZE, _READY = lang, size, True
    latin = (_have(LATIN) or ["STIXGeneral"])[0]
    family = [latin]
    if lang == "zh":
        cjk = _have(CJK)
        if not cjk:
            warnings.warn("No Chinese font found; Chinese labels will show as boxes. "
                          "Install one, e.g. Colab/Ubuntu: apt-get install fonts-noto-cjk")
        family += cjk[:1]
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

def save(fig, path="diagram.png", aspect: float | None = None, show=False):
    """PNG (greyscale, 300 dpi) or .svg / .pdf by extension.  The canvas grows
    to fit every label, so nothing is ever clipped.  `aspect` (w/h)
    pads the PNG with white to an exact ratio, e.g. to replace a picture in
    Word without moving the layout.  show=True also displays it (notebooks)."""
    if show:
        try:
            from IPython.display import display
            display(fig)
        except ImportError:
            pass
    if not path.lower().endswith(".png"):
        fig.savefig(path, facecolor="white", bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
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
    return path
