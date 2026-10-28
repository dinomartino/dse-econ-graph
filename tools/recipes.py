"""Checks recipes/: every catalogue diagram has a recipe, and each recipe is right.

    python tools/recipes.py              # all; exit 1 with every problem found
    python tools/recipes.py 07 24        # only these ids
    python tools/recipes.py --no-fit     # skip the recipes/fit.json coverage check (while writing recipes)

A recipe (recipes/schema.json) says what a diagram contains in economics terms;
the stored ones also carry `geom`, the template's own numbers. Checked here:
1. shape: the JSON Schema (a small validator for the keywords schema.json uses;
   the repo needs only matplotlib and pillow);
2. references: ids exist and are unique, roles fit the family, glossary keys exist;
3. the picture: `geom` against the template's golden scene (recipes/golden/,
   tools/trace.py): every curve drawn where geom says, shifts and the tax as
   offsets of their base curve, lines at their level, every name, label, note and
   axis title present in that language's scene;
4. economics with the template's numbers: shift arrows point the way `dir` says,
   ceilings below / floors above / quotas left of equilibrium, vertical curves
   where `at` says, `onto` shifts land on that curve, `biggerThan` holds, and
   `expect` matches the computed first and last equilibria.
build.py --check runs this. Throwaway-free: no recipe is ever rendered here.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
GOLDEN = RECIPES / "golden"
SCHEMA = json.loads((RECIPES / "schema.json").read_text(encoding="utf-8"))
GLOSSARY = json.loads((RECIPES / "glossary.json").read_text(encoding="utf-8"))["terms"]
IDS = [p.stem for p in sorted((ROOT / "examples").glob("[0-9][0-9]_*.py"))] + \
      [p.stem for p in sorted((ROOT / "chat" / "variants").glob("[0-9][0-9][a-z]_*.py"))]
AXES = {"goods": ("quantity", "price"), "labour": ("number_of_workers", "wage_rate"),
        "adas": ("real_output", "price_level"), "ppc": ("consumer_goods", "capital_goods")}
FAMILY_AXES = {"market": "goods", "externality": "goods", "adas": "adas", "ppc": "ppc"}
FAMILY_ROLES = {"market": {"demand", "supply"}, "externality": {"demand", "supply", "mpc", "msc", "mpb", "msb"},
                "adas": {"ad", "sras", "lras"}, "ppc": {"ppc"}}
SUPPLY_LIKE = {"supply", "sras", "mpc", "msc"}
DEMAND_LIKE = {"demand", "ad", "mpb", "msb"}
TOL = 1e-4


# ---------------------------------------------------------------- 1. schema

def _ref(path):
    node = SCHEMA
    for part in path.lstrip("#/").split("/"):
        node = node[part]
    return node


def validate(v, s, where="$") -> list[str]:
    """The JSON Schema keywords recipes/schema.json uses, nothing more."""
    if "$ref" in s:
        return validate(v, _ref(s["$ref"]), where)
    errs = []
    if "oneOf" in s:
        ok = [o for o in s["oneOf"] if not validate(v, o, where)]
        if len(ok) != 1:
            return [f"{where}: matches {len(ok)} of the allowed forms (needs exactly 1)"]
    if "const" in s and v != s["const"]:
        errs.append(f"{where}: must be {s['const']!r}")
    if "enum" in s and v not in s["enum"]:
        errs.append(f"{where}: {v!r} not one of {s['enum']}")
    t = s.get("type")
    kinds = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    if t == "number":
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return errs + [f"{where}: must be a number"]
    elif t and not isinstance(v, kinds[t]):
        return errs + [f"{where}: must be {t}"]
    if isinstance(v, str):
        if "pattern" in s and not re.search(s["pattern"], v):
            errs.append(f"{where}: {v!r} has characters or a form not allowed")
        if len(v) < s.get("minLength", 0) or len(v) > s.get("maxLength", 10 ** 9):
            errs.append(f"{where}: length {len(v)} out of range")
    if isinstance(v, list):
        if len(v) < s.get("minItems", 0) or len(v) > s.get("maxItems", 10 ** 9):
            errs.append(f"{where}: {len(v)} items, out of range")
        pre = s.get("prefixItems", [])
        for i, x in enumerate(v):
            sub = pre[i] if i < len(pre) else s.get("items")
            if sub:
                errs += validate(x, sub, f"{where}[{i}]")
    if isinstance(v, dict):
        props = s.get("properties", {})
        errs += [f"{where}: needs {k!r}" for k in s.get("required", []) if k not in v]
        for k, x in v.items():
            if k in props:
                errs += validate(x, props[k], f"{where}.{k}")
            elif s.get("additionalProperties") is False:
                errs.append(f"{where}: unknown key {k!r}")
            elif isinstance(s.get("additionalProperties"), dict):
                errs += validate(x, s["additionalProperties"], f"{where}.{k}")
    return errs


# ---------------------------------------------------------------- helpers

class L:
    """A straight curve like dsegraph.Line: y = m x + c, or vertical at vx."""

    def __init__(self, m=None, c=None, vx=None):
        self.m, self.c, self.vx = m, c, vx

    @classmethod
    def of(cls, g):
        if "x" in g:
            return cls(vx=g["x"])
        if "p" in g and "q" in g:
            (x1, y1), (x2, y2) = g["p"], g["q"]
            m = (y2 - y1) / (x2 - x1)
            return cls(m, y1 - m * x1)
        if "p" in g and "m" in g:
            return cls(g["m"], g["p"][1] - g["m"] * g["p"][0])
        return None

    def y(self, x):
        return self.m * x + self.c

    def x(self, y):
        return self.vx if self.vx is not None else (y - self.c) / self.m

    def shift(self, dx=0.0, dy=0.0):
        if self.vx is not None:
            return L(vx=self.vx + dx)
        return L(self.m, self.c + dy - self.m * dx)

    def same(self, o):
        if (self.vx is None) != (o.vx is None):
            return False
        if self.vx is not None:
            return abs(self.vx - o.vx) < TOL
        return abs(self.m - o.m) < TOL and abs(self.c - o.c) < 1e-3

    def hshift(self, o):
        """Horizontal distance from self to o (o's x minus self's x at the same price)."""
        if self.vx is not None:
            return o.vx - self.vx
        return o.x(50) - self.x(50)


def meet(a: L, b: L):
    if a.vx is not None and b.vx is not None:
        return None
    if a.vx is not None:
        return (a.vx, b.y(a.vx))
    if b.vx is not None:
        return (b.vx, a.y(b.vx))
    if abs(a.m - b.m) < 1e-12:
        return None
    x = (b.c - a.c) / (a.m - b.m)
    return (x, a.y(x))


def norm(s: str) -> str:
    """A scene text or a recipe label, compared: no $, no braces around one character, spaces collapsed."""
    s = re.sub(r"(?<=[\u3400-\u9fff])\n(?=[\u3400-\u9fff])", "", s)   # 的士牌照\n數量 = 的士牌照數量
    s = s.replace("$", "").replace("\n", " ")
    s = re.sub(r"_\{(.)\}", r"_\1", s)
    return re.sub(r"\s+", " ", s).strip()


def words(t, lang):
    if isinstance(t, str):
        return t
    if "key" in t:
        return GLOSSARY[t["key"]][lang]
    return t[lang]


def texts(scene):
    return [norm(i["s"]) for i in scene["items"] if i["t"] in ("text", "leader")]


def has_text(scene, s):
    want = norm(s)
    return any(t == want or t.startswith(want + " ") or t.startswith(want + "（") or t.startswith(want + "(")
               for t in texts(scene))


def has_word(scene, s):
    """A word may share a label with a prefix or other words ("A: consumers' burden"). A one- or two-letter word
    must be a whole label ("Q"); "ex dd_0" may be the word and its subscript drawn as two texts (sub())."""
    want = norm(s).lower()
    ts = [t.lower() for t in texts(scene)]
    if len(want) <= 2 and want.isascii():
        return want in ts
    if any(want in t for t in ts):
        return True
    if "_" in want:
        word, sub = want.rsplit("_", 1)
        return any(word.strip() and word.strip() in t for t in ts) and any(t in (sub, "_" + sub) for t in ts)
    return False


def scene_lines(scene):
    return [i["pts"] for i in scene["items"] if i["t"] == "line"]


def segment_drawn(scene, p, q):
    for pts in scene_lines(scene):
        if len(pts) == 2:
            a, b = pts
            if (math.dist(a, p) < 1e-3 and math.dist(b, q) < 1e-3) or (math.dist(a, q) < 1e-3 and math.dist(b, p) < 1e-3):
                return True
    return False


def line_drawn_on(scene, ln: L):
    """Some drawn piece lies on this line (any extent)."""
    for pts in scene_lines(scene):
        if len(pts) == 2 and all(abs((ln.vx - x) if ln.vx is not None else (ln.y(x) - y)) < 1e-3 for x, y in pts) \
                and math.dist(*pts) > 1:
            return True
    return False


# ---------------------------------------------------------------- 2-4. one recipe

def check_recipe(rid: str, r: dict) -> list[str]:
    errs = validate(r, SCHEMA)
    if errs:
        return errs
    e = []
    if r.get("base") != rid:
        e.append(f"base must be its own id {rid!r}")
    if "geom" not in r:
        e.append("stored recipes need geom")
    fam = r["family"]
    # references
    curves = {c["id"]: c for c in r["curves"]}
    role = {c["id"]: c["role"] for c in r["curves"]}
    names = {c["id"]: c["name"] for c in r["curves"]}
    seen = set()

    def new_id(i):
        if i in seen:
            e.append(f"id {i!r} used twice")
        seen.add(i)

    for c in r["curves"]:
        new_id(c["id"])
        if c["role"] not in FAMILY_ROLES[fam]:
            e.append(f"curve {c['id']}: role {c['role']} not in a {fam} diagram")
    shift_of = {}
    for s in r.get("shifts", []):
        if s["of"] not in role:
            e.append(f"shift {s['id']}: unknown curve {s['of']!r}")
            continue
        new_id(s["id"])
        role[s["id"]], names[s["id"]], shift_of[s["id"]] = role[s["of"]], s["name"], s["of"]
        if s["dir"] in ("up", "down") and role[s["of"]] not in SUPPLY_LIKE | {"msb", "mpb"}:
            e.append(f"shift {s['id']}: {s['dir']} only for cost or benefit curves")
        size = s.get("size")
        if isinstance(size, dict):
            ref = next(iter(size.values()))
            if "onto" in size:
                if ref not in role or role[ref] not in ("lras",) and not curves.get(ref, {}).get("slope") == "vertical":
                    e.append(f"shift {s['id']}: onto {ref!r} must be a vertical curve")
            elif ref not in {x["id"] for x in r.get("shifts", [])}:
                e.append(f"shift {s['id']}: size refers to unknown shift {ref!r}")
    tax = r.get("tax")
    if tax:
        if tax["on"] not in role:
            e.append(f"tax: unknown curve {tax['on']!r}")
        elif role[tax["on"]] not in SUPPLY_LIKE:
            e.append("tax: must move a supply curve")
        if "id" in tax:
            new_id(tax["id"])
            role[tax["id"]] = role.get(tax["on"], "supply")
            names[tax["id"]] = tax.get("name", "")
    line_ids = set()
    for ln in r.get("lines", []):
        new_id(ln["id"])
        line_ids.add(ln["id"])
    for ln in r.get("lines", []):
        for k in ("below", "above", "leftOf", "rightOf", "from"):
            if k in ln and ln[k] not in line_ids:
                e.append(f"line {ln['id']}: {k} {ln[k]!r} is not a line")
        for c in ln.get("of", []):
            if c not in role:
                e.append(f"line {ln['id']}: unknown curve {c!r}")
        if ln["kind"] == "price_ceiling" and ln.get("level", "below_eq") != "below_eq":
            e.append(f"line {ln['id']}: a ceiling sits below equilibrium (fixed at equilibrium = fixed_price at_eq)")
        if ln["kind"] in ("price_floor", "minimum_wage") and ln.get("level", "above_eq") != "above_eq":
            e.append(f"line {ln['id']}: a floor sits above equilibrium")
    for c in r["curves"]:
        if "kinked" in c and c["kinked"] not in line_ids:
            e.append(f"curve {c['id']}: kinked at unknown line {c['kinked']!r}")
        for k, pair in (c.get("at") or {}).items():
            for x in pair:
                if x not in role:
                    e.append(f"curve {c['id']}: at.{k} unknown curve {x!r}")
        if c["role"] == "lras" and c.get("slope", "vertical") != "vertical":
            e.append(f"curve {c['id']}: LRAS is vertical")
    point_names = {p[k] for p in r.get("points", []) for k in ("name", "id") if k in p}

    def ref_ok(at, where):
        if isinstance(at, list):
            for x in at:
                if x not in role:
                    e.append(f"{where}: unknown curve {x!r}")
        elif "line" in at:
            if at["curve"] not in role or at["line"] not in line_ids:
                e.append(f"{where}: unknown curve or line in {at}")
        elif "axis" in at:
            if at["curve"] not in role:
                e.append(f"{where}: unknown curve {at['curve']!r}")
        elif "atQuantityOf" in at or "atPriceOf" in at:
            other = at.get("atQuantityOf", at.get("atPriceOf"))
            if at["curve"] not in role:
                e.append(f"{where}: unknown curve {at['curve']!r}")
            if other not in point_names:
                e.append(f"{where}: unknown point {other!r}")
        elif at.get("ppc") not in role:
            e.append(f"{where}: unknown PPC {at.get('ppc')!r}")

    for i, p in enumerate(r.get("points", [])):
        ref_ok(p["at"], f"points[{i}]")
    for k, v in (r.get("moves") or {}).items():
        if isinstance(v, list) and not all(x in point_names for x in v):
            e.append(f"moves.{k}: {v} are not named points")
    for s in r.get("shifts", []):
        if "returnsTo" in s and s["returnsTo"] not in {c["id"] for c in r["curves"]} | set(shift_of):
            e.append(f"shift {s['id']}: returnsTo {s['returnsTo']!r} is not an earlier curve")
    for kind in ("areas", "gaps"):
        for i, a in enumerate(r.get(kind, [])):
            if "at" in a and a["at"] not in line_ids | point_names | set(role):
                e.append(f"{kind}[{i}] ({a['kind']}): at {a['at']!r} is not a line, point or curve")
            for x in a.get("between", []):
                if x not in (point_names if kind == "areas" else set(role)):
                    e.append(f"{kind}[{i}] ({a['kind']}): between {x!r} is not a named {'point' if kind == 'areas' else 'curve'}")
    distortion = any(ln["kind"] in ("price_ceiling", "price_floor", "minimum_wage", "quota", "fixed_price")
                     for ln in r.get("lines", [])) or tax or fam == "externality"
    if any(a["kind"] in ("dwl", "dwl_change") for a in r.get("areas", [])) and not distortion:
        e.append("deadweight loss needs a ceiling, floor, quota, tax, subsidy or externality")
    if any(a["kind"] in ("tax_revenue", "consumers_burden", "producers_burden") for a in r.get("areas", [])) \
            and not (tax and tax["kind"] == "unit_tax"):
        e.append("tax revenue / burdens need a unit tax")
    for t in _all_texts(r):
        if isinstance(t, dict) and "key" in t and t["key"] not in GLOSSARY:
            e.append(f"glossary has no key {t['key']!r}")
    if e or "geom" not in r:
        return e
    return e + check_geom(rid, r, role, names, shift_of)


def _all_texts(r):
    out = list(r.get("notes", []))
    if isinstance(r.get("axes"), dict):
        out += [r["axes"]["x"], r["axes"]["y"]]
    for c in r["curves"] + r.get("shifts", []):
        out += [c["note"]] if "note" in c else []
        out += [c["arrowLabel"]] if "arrowLabel" in c else []
    for k in ("areas", "gaps"):
        out += [a["label"] for a in r.get(k, []) if "label" in a]
    if r.get("tax", {}).get("arrowLabel"):
        out.append(r["tax"]["arrowLabel"])
    return out


def check_geom(rid, r, role, names, shift_of) -> list[str]:
    e = []
    g = r["geom"]
    scenes = {}
    for lang in ("en", "zh"):
        f = GOLDEN / f"{rid}_{lang}.scene.json"
        if not f.exists():
            return [f"no golden scene {f.name} (run tools/trace.py)"]
        scenes[lang] = json.loads(f.read_text(encoding="utf-8"))
    sc = scenes["en"]
    if any(abs(a - b) > 1e-9 for a, b in zip(g["size"], sc["fig_in"])):
        e.append(f"geom.size {g['size']} ≠ the template's {sc['fig_in']}")
    arrows = [(i["a"], i["b"]) for i in sc["items"] if i["t"] == "arrow"]
    for end in ("xEnd", "yEnd"):
        if not any(math.dist(a, g["origin"]) < 1e-6 and math.dist(b, g[end]) < 1e-6 for a, b in arrows):
            e.append(f"no axis arrow from origin {g['origin']} to {end} {g[end]}")
    # lines of every curve: own geometry, or the base curve moved by the shift / tax
    lines: dict[str, L] = {}
    for cid, gc in g["curves"].items():
        if cid not in role:
            e.append(f"geom.curves.{cid}: no curve, shift or tax with that id")
    for c in r["curves"]:
        gc = g["curves"].get(c["id"], {})
        ln = L.of(gc)
        if ln is None and "ellipse" not in gc:
            e.append(f"geom.curves.{c['id']}: needs p+q, p+m, x or ellipse")
        if ln:
            lines[c["id"]] = ln
    order = [s["id"] for s in r.get("shifts", [])]
    for s in r.get("shifts", []):
        gs = g.get("shifts", {}).get(s["id"])
        base = lines.get(s["of"])
        own = L.of(g["curves"].get(s["id"], {}))
        if base is None:
            b_el, n_el = g["curves"].get(s["of"], {}).get("ellipse"), g["curves"].get(s["id"], {}).get("ellipse")
            if not (b_el and n_el):
                e.append(f"shift {s['id']}: base {s['of']} has no line (a PPC shift needs both ellipses)")
            elif not ({"right": n_el["rx"] > b_el["rx"], "left": n_el["rx"] < b_el["rx"]}.get(s["dir"], False)):
                e.append(f"shift {s['id']}: PPC dir {s['dir']} but its ellipse goes the other way")
            continue
        if gs is None and own is None:
            e.append(f"geom.shifts.{s['id']}: needs dx / dy (or the shifted curve's own line)")
            continue
        moved = base.shift(gs.get("dx", 0.0), gs.get("dy", 0.0)) if gs else own
        if own and not own.same(moved):
            e.append(f"shift {s['id']}: geom line ≠ {s['of']} moved by {gs}")
        if "returnsTo" in s and s["returnsTo"] in lines and not moved.same(lines[s["returnsTo"]]):
            e.append(f"shift {s['id']}: does not end on {s['returnsTo']}")
        lines[s["id"]] = moved
        h = base.hshift(moved)
        v = 0.0 if base.vx is not None else (moved.c - base.c)
        want = {"right": h > 1e-6, "left": h < -1e-6, "up": v > 1e-6, "down": v < -1e-6}[s["dir"]]
        if not want:
            e.append(f"shift {s['id']}: dir {s['dir']} but the template moves it {'right' if h > 0 else 'left'} / {'up' if v > 0 else 'down'}")
    tax = r.get("tax")
    if tax and tax.get("id") and tax["on"] in lines:
        if "tax" not in g:
            e.append("geom.tax needed")
        else:
            t = g["tax"]
            lines[tax["id"]] = lines[tax["on"]].shift(dy=t if tax["kind"] == "unit_tax" else -t)
            if t <= 0:
                e.append("geom.tax must be positive (direction comes from kind)")
    # drawn where geom says
    for cid, gc in g["curves"].items():
        ln = lines.get(cid)
        if "ellipse" in gc:
            el = gc["ellipse"]
            ok = any(len(pts) > 10 and all(abs(((x - el["center"][0]) / el["rx"]) ** 2 + ((y - el["center"][1]) / el["ry"]) ** 2 - 1) < 1e-3
                                           for x, y in pts) for pts in scene_lines(sc))
            if not ok:
                e.append(f"geom.curves.{cid}: no drawn curve on that ellipse")
            continue
        if ln is None:
            continue
        if "draw" in gc:
            a, b = gc["draw"]
            p, q = ((ln.vx, a), (ln.vx, b)) if ln.vx is not None else ((a, ln.y(a)), (b, ln.y(b)))
            if not segment_drawn(sc, p, q):
                e.append(f"geom.curves.{cid}: no line drawn from {r6(p)} to {r6(q)}")
        elif not line_drawn_on(sc, ln):
            e.append(f"geom.curves.{cid}: nothing drawn on that line")
    dots = [i["at"] for i in sc["items"] if i["t"] == "dot"]
    for name, xy in g.get("points", {}).items():
        if name not in {p.get("name") for p in r.get("points", [])} | {p.get("id") for p in r.get("points", [])}:
            e.append(f"geom.points.{name}: no point with that name or id")
        if not any(math.dist(xy, d) < 1e-3 for d in dots):
            e.append(f"geom.points.{name}: no dot drawn at {xy}")
    # levels
    for ln in r.get("lines", []):
        val = g.get("lines", {}).get(ln["id"])
        if val is None:
            e.append(f"geom.lines.{ln['id']}: needs a value")
            continue
        vertical = ln["kind"] == "quota"
        drawn = any(len(pts) == 2 and all(abs((x if vertical else y) - val) < 1e-3 for x, y in pts) for pts in scene_lines(sc))
        labelled = any(norm(i["s"]) == norm(ln["name"]) and abs(i["at"][0 if vertical else 1] - val) < 3
                       for i in sc["items"] if i["t"] == "text")
        if not (drawn or labelled):
            e.append(f"line {ln['id']}: nothing drawn or labelled at {val}")
    # words and names in each language's picture
    for lang, s in scenes.items():
        x_t, y_t = (r["axes"]["x"], r["axes"]["y"]) if isinstance(r.get("axes"), dict) else \
            tuple({"key": k} for k in AXES[r.get("axes", FAMILY_AXES[r["family"]])])
        for t in (x_t, y_t):
            if not has_word(s, words(t, lang)):
                e.append(f"{lang}: axis title {words(t, lang)!r} not in the picture")
        for t in r.get("notes", []):
            if not has_word(s, words(t, lang)):
                e.append(f"{lang}: note {words(t, lang)!r} not in the picture")
        for k in ("areas", "gaps"):
            for a in r.get(k, []):
                if "label" in a and not has_word(s, words(a["label"], lang)):
                    e.append(f"{lang}: {a['kind']} label {words(a['label'], lang)!r} not in the picture")
        for ln in r.get("lines", []):
            if "note" in ln and not has_word(s, words(ln["note"], lang)):
                e.append(f"{lang}: note of line {ln['id']} {words(ln['note'], lang)!r} not in the picture")
        for p in r.get("points", []):
            if "leader" in p and not has_word(s, words(p["leader"], lang)):
                e.append(f"{lang}: leader {words(p['leader'], lang)!r} not in the picture")
        for a in r.get("areas", []):
            if "corners" in a and not (has_text(s, a["corners"]) and has_word(s, GLOSSARY["equals_area"][lang])):
                e.append(f"{lang}: '= area {a['corners']}' not in the picture")
        for c in r["curves"] + r.get("shifts", []):
            if "note" in c and not has_word(s, words(c["note"], lang)):
                e.append(f"{lang}: note of {c['id']} {words(c['note'], lang)!r} not in the picture")
            if "arrowLabel" in c and not has_word(s, words(c["arrowLabel"], lang)):
                e.append(f"{lang}: arrow label of {c['id']} not in the picture")
        if lang == "en":
            for cid, nm in names.items():
                if nm and not has_text(s, nm):
                    e.append(f"name {nm!r} of {cid} not in the picture")
            for ln in r.get("lines", []):
                if not has_text(s, ln["name"]):
                    e.append(f"line name {ln['name']!r} not in the picture")
            for p in r.get("points", []):
                for nm in [p.get("name")] + list(p.get("guides") or []):
                    if nm and not has_text(s, nm):
                        e.append(f"point label {nm!r} not in the picture")
    e += points_drawn(r, g, lines, sc)
    e += economics(r, g, lines, role, shift_of, order)
    return e


def point_xy(r, g, lines, at, named):
    """Where a point reference lands with the template's numbers (None if it can't be computed)."""
    o = g["origin"]
    if isinstance(at, list):
        return meet(lines[at[0]], lines[at[1]]) if all(x in lines for x in at) else None
    c = lines.get(at.get("curve")) if "curve" in at else None
    if "line" in at:
        val = g.get("lines", {}).get(at["line"])
        kind = next((ln["kind"] for ln in r.get("lines", []) if ln["id"] == at["line"]), None)
        if c is None or val is None:
            return None
        return (val, c.y(val)) if kind == "quota" else (c.x(val), val)
    if "axis" in at:
        if c is None:
            return None
        return (o[0], c.y(o[0])) if at["axis"] == "price" else (c.x(o[1]), o[1])
    if "atQuantityOf" in at or "atPriceOf" in at:
        q = named.get(at.get("atQuantityOf", at.get("atPriceOf")))
        if c is None or q is None:
            return None
        return (q[0], c.y(q[0])) if "atQuantityOf" in at else (c.x(q[1]), q[1])
    return None


def points_drawn(r, g, lines, sc) -> list[str]:
    """Each point's dot and guides as the template draws them: dot or not, and each guide dashed, solid or absent."""
    e, named = [], {}
    o = g["origin"]
    dots = [i["at"] for i in sc["items"] if i["t"] == "dot"]
    segs = [(i["pts"], i["dash"]) for i in sc["items"] if i["t"] == "line" and len(i["pts"]) == 2]

    def guide_style(a, b, vertical):
        """Style of a drawn line covering a..b (axis to point); 'none' if nothing covers it."""
        k = 0 if vertical else 1
        for pts, d in segs:
            (x1, y1), (x2, y2) = pts
            if vertical and abs(x1 - x2) < 1e-6 and abs(x1 - a[0]) < 1e-3:
                lo, hi = min(y1, y2), max(y1, y2)
            elif not vertical and abs(y1 - y2) < 1e-6 and abs(y1 - a[1]) < 1e-3:
                lo, hi = min(x1, x2), max(x1, x2)
            else:
                continue
            if lo <= min(a[1 - k], b[1 - k]) + 1e-3 and hi >= max(a[1 - k], b[1 - k]) - 1e-3:
                return "dashed" if d else "solid"
        return "none"

    for i, p in enumerate(r.get("points", [])):
        xy = point_xy(r, g, lines, p["at"], named) if not (isinstance(p["at"], dict) and "ppc" in p["at"]) \
            else g.get("points", {}).get(p.get("name") or p.get("id"))
        if xy is None:
            continue
        for k in ("name", "id"):
            if k in p:
                named[p[k]] = xy
        where = p.get("name") or p.get("id") or f"points[{i}]"
        want_dot = p.get("dot", "name" in p)
        has_dot = any(math.dist(xy, d) < 1e-3 for d in dots)
        if want_dot != has_dot:
            e.append(f"point {where}: dot {'expected' if want_dot else 'not expected'} at {r6(xy)} but the template "
                     f"{'has none' if want_dot else 'draws one'}")
        style = p.get("guideStyle", "dashed")
        styles = style if isinstance(style, list) else [style, style]
        # a guide that runs along a vertical curve, a quota or a full price line is that line: no style of its own
        on_vertical = any(ln.vx is not None and abs(ln.vx - xy[0]) < 1e-6 for ln in lines.values()) or \
            any(ln["kind"] == "quota" and abs(g.get("lines", {}).get(ln["id"], 1e9) - xy[0]) < 1e-6 for ln in r.get("lines", []))
        on_price_line = any(ln["kind"] != "quota" and ln.get("full") and abs(g.get("lines", {}).get(ln["id"], 1e9) - xy[1]) < 1e-6
                            for ln in r.get("lines", []))
        for axis, label in enumerate(p.get("guides") or [None, None]):
            if label is None or (axis == 1 and on_vertical) or (axis == 0 and on_price_line):
                continue
            vertical = axis == 1
            a = (xy[0], o[1]) if vertical else (o[0], xy[1])
            got = guide_style(a, xy, vertical)
            if got != styles[axis]:
                e.append(f"point {where}: {'quantity' if vertical else 'price'} guide {label!r} is {got} in the template, "
                         f"recipe says {styles[axis]}")
    return e


def r6(p):
    return [round(v, 3) for v in p]


def economics(r, g, lines, role, shift_of, order) -> list[str]:
    e = []
    fam = r["family"]

    def first(roles):
        return next((c["id"] for c in r["curves"] if c["role"] in roles and c["id"] in lines), None)

    def last(cid):
        """The last curve in cid's chain of shifts."""
        out = cid
        for sid in order:
            if shift_of.get(sid) == out:
                out = sid
        return out

    d0, s0 = first(DEMAND_LIKE - {"msb"}), first(SUPPLY_LIKE - {"msc"})
    if fam == "adas":
        d0, s0 = first({"ad"}), first({"sras"}) or first({"lras"})
    # vertical placements
    for c in r["curves"]:
        for k, pair in (c.get("at") or {}).items():
            if c["id"] in lines and all(x in lines for x in pair):
                pt = meet(lines[pair[0]], lines[pair[1]])
                x = lines[c["id"]].vx
                if pt is None or x is None:
                    e.append(f"curve {c['id']}: at needs a vertical curve and a real intersection")
                    continue
                ok = {"through": abs(x - pt[0]) < 1e-6, "leftOf": x < pt[0] - 1e-6, "rightOf": x > pt[0] + 1e-6}[k]
                if not ok:
                    e.append(f"curve {c['id']}: not {k} {pair} in the template (x {x:.2f} vs {pt[0]:.2f})")
    # policy levels
    for ln in r.get("lines", []):
        val = g.get("lines", {}).get(ln["id"])
        pair = ln.get("of") or [d0, s0]
        if val is None or not all(p in lines for p in pair):
            continue
        eq = meet(lines[pair[0]], lines[pair[1]])
        if eq is None:
            continue
        lvl = ln.get("level") or {"price_ceiling": "below_eq", "price_floor": "above_eq",
                                   "minimum_wage": "above_eq", "quota": "below_eq"}.get(ln["kind"])
        ref = eq[0] if ln["kind"] == "quota" else eq[1]
        ok = {"below_eq": val < ref - 1e-6, "above_eq": val > ref + 1e-6, "at_eq": abs(val - ref) < 1e-6, None: True}[lvl]
        if not ok:
            e.append(f"line {ln['id']}: {lvl} but the template has {val:.2f} vs equilibrium {ref:.2f}")
    for ln in r.get("lines", []):
        val = g.get("lines", {})
        for k, cmp in (("below", lambda a, b: a < b), ("above", lambda a, b: a > b),
                       ("leftOf", lambda a, b: a < b), ("rightOf", lambda a, b: a > b)):
            if k in ln and ln["id"] in val and ln[k] in val and not cmp(val[ln["id"]], val[ln[k]]):
                e.append(f"line {ln['id']}: not {k} {ln[k]} in the template")
    # shift sizes
    for s in r.get("shifts", []):
        size = s.get("size")
        if isinstance(size, dict) and s["id"] in lines:
            mag = abs(lines[s["of"]].hshift(lines[s["id"]]))
            (k, ref), = size.items()
            if k == "onto":
                other = s0 if role[s["id"]] in DEMAND_LIKE else d0
                other = last(other) if other else None
                pt = meet(lines[s["id"]], lines[other]) if other in lines else None
                if pt is None or ref not in lines or abs(pt[0] - lines[ref].x(pt[1])) > 1e-3:
                    e.append(f"shift {s['id']}: the new equilibrium is not on {ref}")
            elif ref in lines:
                om = abs(lines[shift_of[ref]].hshift(lines[ref]))
                ok = {"biggerThan": mag > om + 1e-6, "smallerThan": mag < om - 1e-6, "equalTo": abs(mag - om) < 1e-6}[k]
                if not ok:
                    e.append(f"shift {s['id']}: not {k} {ref} in the template ({mag:.2f} vs {om:.2f})")
    x = r.get("expect", {})
    lras = first({"lras"})
    if fam == "adas" and "gap" in x and lras and d0 and first({"sras"}):
        e0 = meet(lines[d0], lines[first({"sras"})])
        lx = lines[lras].vx
        got = "deflationary" if e0[0] < lx - 1e-6 else "inflationary" if e0[0] > lx + 1e-6 else "none"
        if got != x["gap"]:
            e.append(f"expect.gap {x['gap']} but the first equilibrium gives {got}")
    # expect: first vs last equilibrium, no policy lines or tax
    policy = r.get("lines") or r.get("tax")
    if x and d0 and s0 and not policy:
        e0 = meet(lines[d0], lines[s0])
        d1, s1 = last(d0), last(s0)
        if fam == "adas" and not first({"sras"}):
            s1 = last(s0)
        e1 = meet(lines[d1], lines[s1]) if d1 in lines and s1 in lines else None
        if e0 and e1:
            dy, dx = e1[1] - e0[1], e1[0] - e0[0]
            got = {"price": dy, "price_level": dy, "quantity": dx, "output": dx}
            for k, want in x.items():
                if k in got and want != "unknown":
                    v = got[k]
                    actual = "up" if v > 1e-6 else "down" if v < -1e-6 else "same"
                    if actual != want:
                        e.append(f"expect.{k} {want} but the template's equilibria give {actual}")
    return e


# ---------------------------------------------------------------- all

def check(ids=None, fit=True) -> list[str]:
    bad = []
    want = [i for i in IDS if not ids or i.split("_")[0] in ids]
    for rid in want:
        f = RECIPES / f"{rid}.json"
        if not f.exists():
            bad.append(f"{rid}: no recipe recipes/{rid}.json")
            continue
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            bad.append(f"{rid}: not JSON ({err})")
            continue
        bad += [f"{rid}: {m}" for m in check_recipe(rid, r)]
    stray = {f.stem for f in RECIPES.glob("*.json")} - set(IDS) - {"schema", "glossary", "fit"}
    bad += [f"recipes/{s}.json: no such template or variant" for s in sorted(stray)]
    if fit:
        fitf = RECIPES / "fit.json"
        table = json.loads(fitf.read_text(encoding="utf-8")) if fitf.exists() else {}
        diagrams = table.get("diagrams", {})
        for rid in want:
            entry = diagrams.get(rid)
            if not entry or entry.get("fit") not in ("full", "partial") or \
                    (entry["fit"] == "partial" and not entry.get("missing")):
                bad.append(f"{rid}: recipes/fit.json needs {{fit: full}} or {{fit: partial, missing: [...]}}")
    return bad


def main() -> int:
    args = sys.argv[1:]
    ids = [a for a in args if not a.startswith("--")]
    bad = check(ids, fit="--no-fit" not in args)
    if bad:
        print(f"recipes: {len(bad)} problem(s)\n  " + "\n  ".join(bad))
        return 1
    n = len([i for i in IDS if not ids or i.split('_')[0] in ids])
    print(f"recipes: {n} checked, all right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
