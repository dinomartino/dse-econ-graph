"""Phase-0 spike (DSEconMentor k-0241): dump a template's finished picture as a "scene".

    python tools/trace.py OUT_DIR 07 10 14 24 27 41

For every template and language this runs `diagram(lang)`, then the same label
declutter `save()` runs, and writes OUT_DIR/<id>_<lang>.scene.json: every line,
arrow, brace, area and text with resolved coordinates on the 0..100 canvas,
plus the figure size and the tight bounding box `save()` crops to. It also
saves OUT_DIR/<id>_<lang>.py.png, rendered here with the fonts this machine
has, so a TS painter can be compared against the scene it was given.

Text entries carry matplotlib's own measured extent (inches) so the painter's
text metrics can be checked too.  Not part of the build; throwaway.
"""
from __future__ import annotations

import glob
import importlib.util
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)

import dsegraph  # noqa: E402
from matplotlib.patches import FancyArrowPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.text import Annotation, Text  # noqa: E402

PAD_IN = 0.04


def load(num: str):
    path = glob.glob(os.path.join(ROOT, "examples", f"{num}_*.py"))[0]
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return name, mod


def dash(ln):
    off, seq = ln._unscaled_dash_pattern
    return list(seq) if seq else None


def scene(fig, ax):
    r = fig.canvas.get_renderer()
    w_in, h_in = fig.get_size_inches()
    items = []
    for ln in ax.lines:
        xy = ln.get_xydata().tolist()
        if ln.get_marker() not in (None, "None", "", " ") and len(xy) == 1:
            items.append({"t": "dot", "at": xy[0], "ms": ln.get_markersize(), "z": ln.get_zorder()})
        else:
            d = dash(ln)
            items.append({"t": "line", "pts": xy, "lw": ln.get_linewidth(), "dash": d,
                          "cap": ln.get_dash_capstyle() if d else ln.get_solid_capstyle(),
                          "join": ln.get_solid_joinstyle(), "z": ln.get_zorder()})
    for p in ax.patches:
        z = p.get_zorder()
        if isinstance(p, FancyArrowPatch):
            st = p.get_arrowstyle()
            items.append({"t": "arrow", "a": list(p._posA_posB[0]), "b": list(p._posA_posB[1]),
                          "head_length": st.head_length, "head_width": st.head_width,
                          "mutation": p.get_mutation_scale(), "lw": p.get_linewidth(), "z": z})
        elif isinstance(p, PathPatch):
            path = p.get_path()
            items.append({"t": "path", "verts": path.vertices.tolist(), "codes": path.codes.tolist(),
                          "lw": p.get_linewidth(), "z": z})
        elif isinstance(p, Rectangle):
            items.append({"t": "rect", "xy": list(p.get_xy()), "w": p.get_width(), "h": p.get_height(),
                          "hatch": p.get_hatch(), "lw": p.get_linewidth(), "z": z})
        elif isinstance(p, Polygon):
            items.append({"t": "poly", "pts": p.get_xy().tolist(), "hatch": p.get_hatch(),
                          "lw": p.get_linewidth(), "z": z})
        else:
            raise TypeError(f"unhandled patch {type(p).__name__}")
    for t in ax.texts:
        if isinstance(t, Annotation):
            raise TypeError("leader() not handled in the spike")
        ext = Text.get_window_extent(t, r)
        bb = t.get_bbox_patch()
        items.append({"t": "text", "s": t.get_text(), "at": list(t.get_position()),
                      "ha": t.get_ha(), "va": t.get_va(), "size": t.get_fontsize(),
                      "patch": bool(bb), "z": t.get_zorder(),
                      "ext_in": [ext.x0 / fig.dpi, ext.y0 / fig.dpi, ext.x1 / fig.dpi, ext.y1 / fig.dpi]})
    tb = fig.get_tightbbox(r)
    return {"fig_in": [float(w_in), float(h_in)], "dpi": fig.dpi,
            "tight_in": [tb.x0, tb.y0, tb.x1, tb.y1], "pad_in": PAD_IN,
            "font": dsegraph.plt.rcParams["font.family"], "items": items}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for num in sys.argv[2:]:
        name, mod = load(num)
        for lang in ("en", "zh"):
            fig = mod.diagram(lang)
            ax = fig.axes[0]
            stuck = dsegraph._declutter(fig, ax)
            fig.canvas.draw()
            sc = scene(fig, ax)
            sc.update({"id": name, "lang": lang, "stuck": stuck})
            with open(os.path.join(out, f"{name}_{lang}.scene.json"), "w") as f:
                json.dump(sc, f, ensure_ascii=False, indent=1)
            # the same PNG save() writes, labels already decluttered
            dsegraph.save(fig, os.path.join(out, f"{name}_{lang}.py.png"), tidy=False)
            print(name, lang, len(sc["items"]), "items", sc["font"])


if __name__ == "__main__":
    main()
