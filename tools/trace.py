"""Golden scenes: every template and chat variant, as the finished picture's primitives.

    python tools/trace.py                 # write recipes/golden/<id>_<lang>.scene.json for all 53 ids
    python tools/trace.py --check         # exit 1 if a committed scene differs from a fresh trace
    python tools/trace.py 07 24 --png DIR # only these ids; also save the PNGs (to compare a renderer)

A scene is what `save()` would draw, after the library's label declutter:
every line, arrow, brace path, hatched area, dot and text with resolved
coordinates on the 0..100 canvas, the printed size and the tight bounding
box the PNG is cropped to. Texts also carry matplotlib's measured extent
(inches). DSEconMentor's TS renderer is tested against these files (its
painter must draw the same picture, its compiler must turn recipes/<id>.json
into the same scene), so they are made with fixed fonts, the ones the
renderer bundles: Liberation Serif and Noto Serif CJK TC. Install them
(Debian: fonts-liberation fonts-noto-cjk) or the trace stops; a machine's
own Times New Roman would move the labels.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import dsegraph  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.text import Annotation, Text  # noqa: E402

GOLDEN = ROOT / "recipes" / "golden"
LATIN, CJK = "Liberation Serif", "Noto Serif CJK TC"
PAD_IN = 0.04                       # save(): pad_inches
SOURCES = sorted((ROOT / "examples").glob("[0-9][0-9]_*.py")) + \
    sorted((ROOT / "chat" / "variants").glob("[0-9][0-9][a-z]_*.py"))


def pin_fonts():
    have = {f.name for f in font_manager.fontManager.ttflist}
    missing = [f for f in (LATIN, CJK) if f not in have]
    if missing:
        raise SystemExit(f"trace: fonts missing: {', '.join(missing)} (Debian: apt install fonts-liberation fonts-noto-cjk)")
    dsegraph.LATIN, dsegraph.CJK = [LATIN], [CJK]


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def r6(v):
    """Floats rounded to 6 places (stable files across runs); recursive."""
    if isinstance(v, float):
        return 0.0 if v == 0 else round(v, 6)
    if isinstance(v, (list, tuple)):
        return [r6(x) for x in v]
    if isinstance(v, dict):
        return {k: r6(x) for k, x in v.items()}
    if hasattr(v, "tolist"):
        return r6(v.tolist())
    return v


def dash(ln):
    _, seq = ln._unscaled_dash_pattern
    return list(seq) if seq else None


def scene(fig, ax) -> dict:
    r = fig.canvas.get_renderer()
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
        ext = Text.get_window_extent(t, r)
        item = {"t": "text", "s": t.get_text(), "at": list(t.get_position()), "ha": t.get_ha(),
                "va": t.get_va(), "size": t.get_fontsize(), "patch": bool(t.get_bbox_patch()),
                "z": t.get_zorder(),
                "ext_in": [ext.x0 / fig.dpi, ext.y0 / fig.dpi, ext.x1 / fig.dpi, ext.y1 / fig.dpi]}
        if isinstance(t, Annotation):              # leader(): text with a thin arrow to its target
            st = t.arrow_patch.get_arrowstyle()
            item.update({"t": "leader", "target": list(t.xy), "head_length": st.head_length,
                         "head_width": st.head_width, "mutation": t.arrow_patch.get_mutation_scale(),
                         "lw": t.arrow_patch.get_linewidth(), "shrinkA": t.arrow_patch.shrinkA})
        items.append(item)
    tb = fig.get_tightbbox(r)
    w, h = fig.get_size_inches()
    return {"fig_in": [float(w), float(h)], "dpi": fig.dpi, "tight_in": [tb.x0, tb.y0, tb.x1, tb.y1],
            "pad_in": PAD_IN, "items": items}


def trace(path: Path, lang: str, png_dir: Path | None = None) -> dict:
    mod = load(path)
    fig = mod.diagram(lang)
    ax = fig.axes[0]
    stuck = dsegraph._declutter(fig, ax)
    fig.canvas.draw()
    sc = {"id": path.stem, "lang": lang, "matplotlib": matplotlib.__version__,
          "fonts": list(matplotlib.rcParams["font.family"]), "stuck": stuck, **scene(fig, ax)}
    if png_dir:
        png_dir.mkdir(parents=True, exist_ok=True)
        dsegraph.save(fig, str(png_dir / f"{path.stem}_{lang}.png"), tidy=False)
    else:
        dsegraph.plt.close(fig)
    return r6(sc)


def dumps(sc: dict) -> str:
    """One item per line: readable diffs, small files."""
    head = {k: v for k, v in sc.items() if k != "items"}
    body = ",\n".join("  " + json.dumps(it, ensure_ascii=False, separators=(",", ":")) for it in sc["items"])
    return json.dumps(head, ensure_ascii=False)[:-1] + ',\n "items": [\n' + body + "\n ]}\n"


def same(a, b, tol=1e-6) -> bool:
    if isinstance(a, float) or isinstance(b, float):
        return isinstance(a, (int, float)) and isinstance(b, (int, float)) and math.isclose(a, b, abs_tol=tol)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k], tol) for k in a)
    return a == b


def main() -> int:
    args = sys.argv[1:]
    check = "--check" in args
    png = Path(args[args.index("--png") + 1]) if "--png" in args else None
    nums = [a for a in args if not a.startswith("--") and (png is None or a != str(png))]
    paths = [p for p in SOURCES if not nums or p.stem.split("_")[0] in nums]
    pin_fonts()
    GOLDEN.mkdir(parents=True, exist_ok=True)
    bad = []
    for p in paths:
        for lang in ("en", "zh"):
            sc = trace(p, lang, png)
            f = GOLDEN / f"{p.stem}_{lang}.scene.json"
            if check:
                if not f.exists():
                    bad.append(f"{f.name}: missing")
                elif not same(json.loads(f.read_text(encoding="utf-8")), json.loads(dumps(sc))):
                    bad.append(f"{f.name}: differs from a fresh trace")
            else:
                f.write_text(dumps(sc), encoding="utf-8")
            if sc["stuck"]:
                print(f"note: {p.stem} {lang}: crowded labels {sc['stuck']}")
    if check:
        if not nums:
            expected = {f"{p.stem}_{lang}.scene.json" for p in SOURCES for lang in ("en", "zh")}
            bad += [f"{n}: no such template or variant"
                    for n in sorted({f.name for f in GOLDEN.glob("*.scene.json")} - expected)]
        if bad:
            print("golden scenes out of date — run: python tools/trace.py\n  " + "\n  ".join(bad))
            return 1
        print(f"golden scenes up to date ({len(paths) * 2})")
        return 0
    print(f"wrote {len(paths) * 2} golden scenes to {GOLDEN.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
