"""Rebuild everything that is generated from the sources.

    python tools/build.py              # sync SKILL.md, render the gallery, write download/
    python tools/build.py --check      # exit 1 if SKILL.md, README.md or download/ is out of date
    python tools/build.py --no-render  # as the first, but keep the PNGs already in gallery/
                                       # (a machine whose fonts differ from the committed gallery)

1. Pastes dsegraph.py, the template list and example 01 into SKILL.md, so
   SKILL.md stays a single self-contained file any chat assistant can use.
2. Runs every examples/NN_*.py (English + Chinese PNGs into gallery/) and
   every chat-only variant chat/variants/NNx_*.py (into gallery/chat/).
3. Writes download/ — the files teachers download, with fixed names (the
   website links to them, so never rename one) and manifest.json, which the
   website reads: version, what's new, setup steps, file links, gallery.
4. Writes download/chat-catalogue.json for DSEconMentor's chat tutor: every
   template and variant with the texts in chat/meta.json and its PNGs' size
   and sha256. Variants never go into SKILL.md, the zips or manifest.json.
5. Recipes for the chat tutor's renderer: re-traces recipes/golden/ (every
   template's picture as primitives, tools/trace.py) after rendering and checks
   recipes/ (tools/recipes.py): every catalogue id has a recipe that matches
   its golden scene. The catalogue lists each recipe and scene with its sha256.
   --check also runs both checks (the trace takes a few seconds).
"""
from __future__ import annotations

import ast
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
EXAMPLES = sorted((ROOT / "examples").glob("[0-9][0-9]_*.py"))
DOWNLOAD = ROOT / "download"
TEACHER = ROOT / "teacher"
GALLERY = ROOT / "gallery"
# Chat-only variants (DSEconMentor's chat tutor): rendered into gallery/chat/,
# never pasted into SKILL.md or put in the teacher zips or manifest.json.
VARIANTS = sorted((ROOT / "chat" / "variants").glob("[0-9][0-9][a-z]_*.py"))
CHAT_META = ROOT / "chat" / "meta.json"
CATALOGUE = "chat-catalogue.json"                                 # in download/, not in FILES
RECIPES = ROOT / "recipes"                                        # recipe per catalogue id + golden scenes

REPO = "dinomartino/dse-econ-graph"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"           # CORS-friendly, for fetch()
LATEST = f"https://github.com/{REPO}/releases/latest/download"    # for download buttons

# Teacher downloads: published name -> (title en, title zh, what it is en, zh)
FILES = {
    "dse-econ-graph.zip": ("dse-econ-graph (everything, .zip)", "dse-econ-graph（全部檔案，.zip）",
                           "The file to download for Grok or Claude (ChatGPT has its own version below). Do not unzip it.",
                           "Grok 或 Claude 用的下載檔案（ChatGPT 另有專用版本）。不用解壓。"),
    "dse-econ-graph-chatgpt.zip": ("dse-econ-graph for ChatGPT (.zip)", "dse-econ-graph（ChatGPT 版，.zip）",
                                   "The ChatGPT version: upload it with Plugins ▸ Upload plugin. Do not unzip it.",
                                   "ChatGPT 專用版本：在 Plugins ▸ Upload plugin 上載，不用解壓。"),
    "SKILL.md": ("Diagram guide", "畫圖指南",
                 "Only if your AI cannot open the .zip: the guide on its own (also inside the zip).",
                 "只在 AI 打不開 .zip 時使用：單獨的指南（.zip 內已包含）。"),
    "instructions.txt": ("Instructions", "指示",
                         "The text to paste into your Grok or ChatGPT project's Instructions (also inside the zip).",
                         "貼到 Grok 或 ChatGPT 專案 Instructions（指示）的文字（.zip 內已包含）。"),
    "SKILL.txt": ("Diagram guide (.txt)", "畫圖指南（.txt）",
                  "The same guide as a .txt file, for chats that do not accept .md.",
                  "同一份指南的 .txt 版本，供不接受 .md 的對話使用。"),
}


def block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- BEGIN {re.escape(name)} -->\n).*?(<!-- END {re.escape(name)} -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"no '{name}' markers")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)


# Template groups, in the order the guide lists them (each example's "Topic:")
TOPICS = ["Demand and supply: shifts", "Labour market", "Total revenue and elasticity",
          "Price fixed away from equilibrium", "Price controls and efficiency",
          "Tax, subsidy and quota", "Consumer and producer surplus", "AD-AS", "Other"]


def meta(path: Path) -> dict:
    """title / topic / use from an example's docstring:
    first paragraph = title, then "Topic: ..." and "Use for: ..." lines."""
    doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    paras = doc.strip().split("\n\n")
    title = " ".join(l.strip() for l in paras[0].splitlines())
    topic = re.search(r"^Topic:\s*(.+)$", doc, re.M)
    use = re.search(r"^Use for:\s*(.+?)(?:\n\n|\Z)", doc, re.M | re.S)
    if not topic or topic.group(1).strip() not in TOPICS:
        raise SystemExit(f"{path.name}: needs a 'Topic:' line, one of {TOPICS}")
    shows = []                                     # "  - point" lines, continuations joined
    pts = re.search(r"^Marking-scheme points it shows:\n(.*?)(?:\n\n|\Z)", doc, re.M | re.S)
    for line in (pts.group(1).splitlines() if pts else []):
        s = line.strip()
        if s.startswith("- "):
            shows.append(" ".join(s[2:].split()))
        elif s and shows:
            shows[-1] += " " + " ".join(s.split())
    base = re.search(r"^Variant of:\s*(\S+)\s*$", doc, re.M)
    return {"title": title, "topic": topic.group(1).strip(),
            "use": " ".join(l.strip() for l in use.group(1).splitlines()) if use else "",
            "shows": shows, "variant_of": base.group(1) if base else None}


def doc_first_line(path: Path) -> str:
    return meta(path)["title"]


PASTE = '# (paste the whole dsegraph library from "The library" here)\n'


def standalone(path: Path) -> str:
    """An example as it is pasted under the library: its docstring as comments
    (a second docstring before the library's `from __future__` would be a
    SyntaxError), no sys.path dance, and a plain __main__ saving beside it."""
    src = path.read_text(encoding="utf-8")
    doc = ast.parse(src).body[0]
    if isinstance(doc, ast.Expr) and isinstance(doc.value, ast.Constant):
        lines = src.splitlines(keepends=True)
        text = ast.get_docstring(ast.parse(src))
        src = "".join(("# " + l).rstrip() + "\n" for l in text.splitlines()) + "".join(lines[doc.end_lineno:])
    m = re.search(r"import ([\w, ]+)\nsys\.path\.insert\(0, .*?\)\nfrom dsegraph import \*\n", src)
    if not m:
        raise SystemExit(f"{path.name}: header must be 'import os, sys / sys.path.insert(...) / from dsegraph import *'")
    extra = [x.strip() for x in m.group(1).split(",") if x.strip() not in ("os", "sys")]
    src = src[:m.start()] + PASTE + (f"import {', '.join(extra)}\n" if extra else "") + src[m.end():]
    src = re.sub(r'if __name__ == "__main__":\n.*', (
        'if __name__ == "__main__":\n'
        '    for lang in ("en", "zh"):\n'
        '        save(diagram(lang), f"diagram_{lang}.png")\n'), src, flags=re.S)
    return src


def pasted_test(lib: str) -> list[str]:
    """Run every template exactly as a chat AI would: library pasted in, in an
    empty folder. Returns the names that fail or print a 'crowded' note."""
    import tempfile
    failed = []
    for p in EXAMPLES:
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "s.py").write_text(standalone(p).replace(PASTE, lib), encoding="utf-8")
            r = subprocess.run([sys.executable, "s.py"], cwd=d, capture_output=True, text=True)
            made = sorted(f.name for f in Path(d).glob("*.png"))
            if r.returncode or made != ["diagram_en.png", "diagram_zh.png"] or "crowded" in r.stdout:
                failed.append(p.name)
                print(f"FAIL  {p.name} (pasted)\n{r.stdout[-500:]}{r.stderr[-1500:]}")
    return failed


def sync() -> str:
    text = SKILL.read_text(encoding="utf-8")
    lib = (ROOT / "dsegraph.py").read_text(encoding="utf-8")
    text = block(text, "dsegraph.py", f"```python\n{lib}```\n")
    groups = []
    for topic in TOPICS:
        rows = [(p, meta(p)) for p in EXAMPLES if meta(p)["topic"] == topic]
        if rows:
            groups.append(f"**{topic}**\n\n" + "\n".join(
                f"- `{p.stem}`: {m['title']}" + (f" *Use for:* {m['use']}" if m["use"] else "")
                for p, m in rows))
    text = block(text, "TEMPLATE LIST", "\n\n".join(groups) + "\n")
    code = "\n".join(f"### {p.stem}\n\n```python\n{standalone(p)}```\n" for p in EXAMPLES)
    text = block(text, "TEMPLATES", code)
    return text


README = ROOT / "README.md"


def readme() -> str:
    """README.md with the current instructions text pasted in (teachers copy it)."""
    text = (TEACHER / "instructions.txt").read_text(encoding="utf-8")
    return block(README.read_text(encoding="utf-8"), "INSTRUCTIONS", f"\n```text\n{text}```\n\n")


def changelog() -> dict:
    """The top entry of CHANGELOG.md: version, date and en / zh lines."""
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"^## (\S+) — (\d{4}-\d{2}-\d{2})\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit("CHANGELOG.md has no '## X.Y.Z — YYYY-MM-DD' entry")
    news = {"en": [], "zh": []}
    for lang, line in re.findall(r"^- (en|zh): (.+)$", m.group(3), re.M):
        news[lang].append(line.strip())
    return {"version": m.group(1), "released": m.group(2), "whats_new": news}


def zipped(skill: str) -> bytes:
    """The one file teachers download and upload to Grok / Claude / ChatGPT:
    a dse-econ-graph/ folder (the claude.ai skill layout) with the guide, the
    instructions text, the library and every template. Byte-for-byte
    reproducible (fixed dates)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [SKILL, TEACHER / "instructions.txt", ROOT / "dsegraph.py", *EXAMPLES]:
            rel = Path(f.name) if f.parent == TEACHER else f.relative_to(ROOT)
            info = zipfile.ZipInfo(str(Path("dse-econ-graph") / rel), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, skill.encode("utf-8") if f == SKILL else f.read_bytes())
    return buf.getvalue()


def plugin_json() -> dict:
    """ChatGPT's "Upload plugin" wants a plugin archive (.codex-plugin/plugin.json
    + skills/<name>/SKILL.md), not a claude.ai skill folder."""
    log = changelog()
    return {
        "name": "dse-econ-graph",
        "version": log["version"],
        "description": "Draw HKDSE Economics diagrams (supply and demand, AD-AS) in the HKEAA "
                       "marking-scheme style, in English or Traditional Chinese, from a pasted "
                       "question and marking scheme.",
        "author": {"name": "dinomartino", "url": f"https://github.com/{REPO}"},
        "homepage": f"https://github.com/{REPO}",
        "repository": f"https://github.com/{REPO}",
        "license": "MIT",
        "keywords": ["economics", "hkdse", "diagrams", "education", "supply-and-demand"],
        "skills": "./skills/",
        "interface": {
            "displayName": "DSE Economics Diagrams",
            "shortDescription": "Paste a DSE Economics question, get the marking-scheme diagram",
            "longDescription": "Paste an HKDSE Economics question and its marking scheme; the diagram "
                               "comes back as a black-and-white picture in the HKEAA marking-scheme "
                               "style, in English or Chinese. Covers every supply-and-demand and "
                               "AD-AS diagram type in the marking schemes.",
            "developerName": "dinomartino",
            "category": "Education",
            "capabilities": ["Interactive", "Write"],
            "websiteURL": f"https://github.com/{REPO}",
            "defaultPrompt": ["Draw the diagram for this DSE Economics question and marking scheme"],
        },
    }


def plugin_zip(skill: str) -> bytes:
    """The ChatGPT version of the download: the same files as the main zip,
    laid out as a plugin."""
    buf = io.BytesIO()
    stamp = (2026, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        def put(name, data):
            info = zipfile.ZipInfo(name, stamp); info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
        put(".codex-plugin/plugin.json", json.dumps(plugin_json(), ensure_ascii=False, indent=2) + "\n")
        for f in [SKILL, TEACHER / "instructions.txt", ROOT / "dsegraph.py", *EXAMPLES]:
            rel = Path(f.name) if f.parent == TEACHER else f.relative_to(ROOT)
            put(str(Path("skills/dse-econ-graph") / rel), skill.encode("utf-8") if f == SKILL else f.read_bytes())
    return buf.getvalue()


def downloads(skill: str) -> dict[str, bytes]:
    """Every file in download/, by name."""
    out = {
        "SKILL.md": skill.encode("utf-8"),
        "SKILL.txt": skill.encode("utf-8"),
        "instructions.txt": (TEACHER / "instructions.txt").read_bytes(),
        "dse-econ-graph.zip": zipped(skill),
        "dse-econ-graph-chatgpt.zip": plugin_zip(skill),
    }
    names = {"skill": "SKILL.md", "skill_txt": "SKILL.txt", "instructions": "instructions.txt",
             "zip": "dse-econ-graph.zip", "chatgpt_zip": "dse-econ-graph-chatgpt.zip"}

    def fill(x):                                   # "{skill}" -> "SKILL.md", everywhere
        if isinstance(x, str):
            return x.format(**names)
        if isinstance(x, list):
            return [fill(v) for v in x]
        if isinstance(x, dict):
            return {k: fill(v) for k, v in x.items()}
        return x

    setup = json.loads((TEACHER / "setup.json").read_text(encoding="utf-8"))
    setup.pop("_comment", None)
    setup = fill(setup)
    unknown = {f for prov in setup["providers"] for f in prov["files"]} - set(FILES)
    if unknown:
        raise SystemExit(f"teacher/setup.json names files that are not built: {unknown}")
    texts = chat_meta()
    gallery = []
    for p in EXAMPLES:                             # templates only: variants are chat-only
        stem = p.stem
        gallery.append({"id": stem, "title": doc_first_line(p),
                        "title_zh": texts[stem]["caption"]["zh"], "topic": meta(p)["topic"],
                        "en": f"{RAW}/gallery/{stem}_en.png", "zh": f"{RAW}/gallery/{stem}_zh.png"})
    manifest = {
        "name": "dse-econ-graph",
        "about": {"en": "Paste a DSE Economics question and its marking scheme into Grok, Claude or ChatGPT and get the diagram in the HKEAA marking-scheme style, in English or Chinese.",
                  "zh": "把 DSE 經濟題目和評卷參考貼到 Grok、Claude 或 ChatGPT，即可得到 HKEAA 評卷參考風格的圖，中英文皆可。"},
        **changelog(),
        "files": [{
            "name": name,
            "title": {"en": t_en, "zh": t_zh},
            "description": {"en": d_en, "zh": d_zh},
            "bytes": len(out[name]),
            "sha256": hashlib.sha256(out[name]).hexdigest(),
            "url": f"{RAW}/download/{name}",
            "download_url": f"{LATEST}/{name}",
        } for name, (t_en, t_zh, d_en, d_zh) in FILES.items()],
        "instructions_text": (TEACHER / "instructions.txt").read_text(encoding="utf-8"),
        **setup,                                   # providers, use, quick, updating
        "gallery": gallery,
    }
    out["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    out[CATALOGUE] = catalogue(texts)
    return out


def chat_meta() -> dict:
    """chat/meta.json, checked: a complete entry for every template and
    variant (caption, alt, shows_zh, labels; en and zh), and every variant's
    "Variant of:" names a template. Stops the build with every problem found."""
    texts = json.loads(CHAT_META.read_text(encoding="utf-8"))
    bases = {p.stem for p in EXAMPLES}
    ids = [p.stem for p in EXAMPLES + VARIANTS]
    bad = [f"{i}: no entry" for i in ids if i not in texts]
    bad += [f"{i}: in meta.json but no such template or variant" for i in texts if i not in ids]

    def text(v):
        return isinstance(v, str) and v.strip() != ""

    for p in EXAMPLES + VARIANTS:
        e, m = texts.get(p.stem), meta(p)
        if e is None:
            continue
        for k in ("caption", "alt"):
            if not (isinstance(e.get(k), dict) and text(e[k].get("en")) and text(e[k].get("zh"))):
                bad.append(f"{p.stem}: needs {k} {{en, zh}}")
        lab = e.get("labels")
        if not (isinstance(lab, dict) and all(isinstance(lab.get(l), list) and lab[l]
                                              and all(map(text, lab[l])) for l in ("en", "zh"))):
            bad.append(f"{p.stem}: needs labels {{en: [...], zh: [...]}}")
        zh = e.get("shows_zh")
        if not m["shows"]:
            bad.append(f"{p.stem}: docstring has no 'Marking-scheme points it shows:' list")
        elif not (isinstance(zh, list) and len(zh) == len(m["shows"]) and all(map(text, zh))):
            bad.append(f"{p.stem}: shows_zh needs {len(m['shows'])} points, like the docstring")
        if p in VARIANTS and m["variant_of"] not in bases:
            bad.append(f"{p.name}: 'Variant of: {m['variant_of']}' is not a template in examples/")
        if p in EXAMPLES and m["variant_of"]:
            bad.append(f"{p.name}: templates in examples/ must not have a 'Variant of:' line")
    if bad:
        raise SystemExit("chat/meta.json / chat variants:\n  " + "\n  ".join(bad))
    return texts


def catalogue(texts: dict) -> bytes:
    """download/chat-catalogue.json, read by DSEconMentor's chat tutor through a
    pinned sync: the 43 templates in order, then the chat-only variants. Ids are
    a contract (saved in chat messages): never rename or remove one. size and
    sha256 describe the PNGs in gallery/ as they are now."""
    from PIL import Image
    diagrams = []
    for p in EXAMPLES + VARIANTS:
        m, e = meta(p), texts[p.stem]
        png, size, sha = {}, {}, {}
        for lang in ("en", "zh"):
            f = (GALLERY / "chat" if p in VARIANTS else GALLERY) / f"{p.stem}_{lang}.png"
            if not f.exists():
                raise SystemExit(f"{f.relative_to(ROOT)} is missing — run: python tools/build.py")
            png[lang] = f.relative_to(ROOT).as_posix()
            with Image.open(f) as im:
                size[lang] = list(im.size)
            sha[lang] = hashlib.sha256(f.read_bytes()).hexdigest()
        recipe = RECIPES / f"{p.stem}.json"
        golden = {lang: RECIPES / "golden" / f"{p.stem}_{lang}.scene.json" for lang in ("en", "zh")}
        for f in (recipe, *golden.values()):
            if not f.exists():
                raise SystemExit(f"{f.relative_to(ROOT)} is missing — write the recipe / run: python tools/trace.py")
        diagrams.append({
            "id": p.stem, "variant_of": m["variant_of"], "topic": m["topic"],
            "title": {"en": m["title"], "zh": e["caption"]["zh"]},
            "caption": e["caption"], "use": m["use"],
            "shows": {"en": m["shows"], "zh": e["shows_zh"]},
            "labels": e["labels"], "alt": e["alt"],
            "png": png, "size": size, "sha256": sha,
            "recipe": {"path": recipe.relative_to(ROOT).as_posix(),
                       "sha256": hashlib.sha256(recipe.read_bytes()).hexdigest()},
            "golden": {lang: {"path": f.relative_to(ROOT).as_posix(),
                              "sha256": hashlib.sha256(f.read_bytes()).hexdigest()} for lang, f in golden.items()}})
    cat = {"schema": 1, "version": changelog()["version"],
           "recipes": {"schema": "recipes/schema.json", "glossary": "recipes/glossary.json",
                       "fit": "recipes/fit.json", "recipe_version": 1},
           "diagrams": diagrams}
    return (json.dumps(cat, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def recipe_problems() -> list[str]:
    """tools/recipes.py: a recipe for every catalogue id, each matching its golden scene."""
    sys.path.insert(0, str(ROOT / "tools"))
    import recipes
    return recipes.check()


def main() -> int:
    new = sync()
    chat_meta()                                    # fail fast, before the long render
    if "--check" in sys.argv:
        files = downloads(new)
        stale = [] if new == SKILL.read_text(encoding="utf-8") else ["SKILL.md"]
        stale += [] if readme() == README.read_text(encoding="utf-8") else ["README.md"]
        stale += [f"download/{n}" for n, b in files.items()
                  if not (DOWNLOAD / n).exists() or (DOWNLOAD / n).read_bytes() != b]
        traced = subprocess.run([sys.executable, str(ROOT / "tools" / "trace.py"), "--check"], cwd=ROOT,
                                capture_output=True, text=True)
        stale += [] if traced.returncode == 0 else ["recipes/golden/"]
        bad = recipe_problems()
        if stale or bad:
            if stale:
                print("out of date: " + ", ".join(stale) + " — run: python tools/build.py")
            if traced.returncode:
                print(traced.stdout[-1500:].rstrip())
            if bad:
                print(f"recipes: {len(bad)} problem(s)\n  " + "\n  ".join(bad))
            return 1
        print("SKILL.md, README.md, download/ and recipes/golden/ are up to date; "
              f"{len(EXAMPLES) + len(VARIANTS)} recipes check out")
        return 0
    SKILL.write_text(new, encoding="utf-8")
    README.write_text(readme(), encoding="utf-8")
    print(f"synced {SKILL.name}: library + {len(EXAMPLES)} templates")

    failed = []
    for p in ([] if "--no-render" in sys.argv else EXAMPLES + VARIANTS):
        r = subprocess.run([sys.executable, str(p)], cwd=ROOT, capture_output=True, text=True)
        bad = r.returncode or (p in VARIANTS and "crowded" in r.stdout)
        print(("FAIL  " if bad else "ok    ") + str(p.relative_to(ROOT)))
        if bad:
            failed.append(p.name)
            print(r.stdout[-500:] + r.stderr[-2000:])

    # SKILL.md's templates only: the chat variants are not in the guide
    failed += pasted_test((ROOT / "dsegraph.py").read_text(encoding="utf-8"))
    print(f"pasted test: {len(EXAMPLES)} templates run as a chat AI would paste them")

    traced = subprocess.run([sys.executable, str(ROOT / "tools" / "trace.py")], cwd=ROOT,
                            capture_output=True, text=True)
    print(traced.stdout.strip().splitlines()[-1] if traced.stdout.strip() else traced.stderr[-800:])
    if traced.returncode:
        failed.append("tools/trace.py")
    bad = recipe_problems()
    print(f"recipes: {len(EXAMPLES) + len(VARIANTS)} catalogue ids, " + (f"{len(bad)} problem(s)" if bad else "all check out"))
    if bad:
        print("  " + "\n  ".join(bad))
        failed.append("recipes/")

    files = downloads(new)                         # after rendering: the catalogue hashes gallery/ and recipes/
    DOWNLOAD.mkdir(exist_ok=True)
    for name, data in files.items():
        (DOWNLOAD / name).write_bytes(data)
    print(f"wrote download/: {', '.join(files)}  (version {changelog()['version']})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
