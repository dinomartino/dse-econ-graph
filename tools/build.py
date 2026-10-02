"""Rebuild everything that is generated from the sources.

    python tools/build.py            # sync SKILL.md, render the gallery, pack dist/
    python tools/build.py --check    # exit 1 if SKILL.md is out of date (for CI)

1. Pastes dsegraph.py, the template list and example 01 into SKILL.md, so
   SKILL.md stays a single self-contained file any chat assistant can use.
2. Runs every examples/NN_*.py (English + Chinese PNGs into gallery/).
3. Writes dist/dse-econ-graph.zip — the skill folder for claude.ai upload.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
EXAMPLES = sorted((ROOT / "examples").glob("[0-9][0-9]_*.py"))


def block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- BEGIN {re.escape(name)} -->\n).*?(<!-- END {re.escape(name)} -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"SKILL.md has no '{name}' markers")
    return pat.sub(lambda m: m.group(1) + body + m.group(2), text)


def doc_first_line(path: Path) -> str:
    doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    return doc.strip().splitlines()[0] if doc else ""


LOADER = (
    "# DSE graph library — downloads automatically, do not edit\n"
    "import os, urllib.request\n"
    "if not os.path.exists(\"dsegraph.py\"):\n"
    "    urllib.request.urlretrieve(\"https://raw.githubusercontent.com/dinomartino/dse-econ-graph/main/dsegraph.py\", \"dsegraph.py\")\n"
    "from dsegraph import *\n")


def standalone(path: Path) -> str:
    """An example as it would be pasted under the library: no sys.path dance,
    a plain __main__ that saves beside the script."""
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"import os, sys\nsys\.path\.insert\(0, .*?\)\nfrom dsegraph import \*\n",
                 LOADER, src)
    src = re.sub(r'if __name__ == "__main__":\n.*', (
        'if __name__ == "__main__":\n'
        '    for lang in ("en", "zh"):\n'
        '        save(diagram(lang), f"diagram_{lang}.png")\n'), src, flags=re.S)
    return src


def sync() -> str:
    text = SKILL.read_text(encoding="utf-8")
    lib = (ROOT / "dsegraph.py").read_text(encoding="utf-8")
    text = block(text, "dsegraph.py", f"```python\n{lib}```\n")
    rows = "\n".join(f"- `{p.name}` — {doc_first_line(p)}" for p in EXAMPLES)
    text = block(text, "TEMPLATE LIST", rows + "\n")
    first = ROOT / "examples" / "01_price_ceiling_shortage.py"
    text = block(text, "EXAMPLE 01", f"```python\n{standalone(first)}```\n")
    return text


def main() -> int:
    new = sync()
    if "--check" in sys.argv:
        if new != SKILL.read_text(encoding="utf-8"):
            print("SKILL.md is out of date — run: python tools/build.py")
            return 1
        print("SKILL.md is up to date")
        return 0
    SKILL.write_text(new, encoding="utf-8")
    print(f"synced {SKILL.name}: library + {len(EXAMPLES)} templates")

    failed = []
    for p in EXAMPLES:
        r = subprocess.run([sys.executable, str(p)], cwd=ROOT, capture_output=True, text=True)
        print(("ok    " if r.returncode == 0 else "FAIL  ") + p.name)
        if r.returncode:
            failed.append(p.name)
            print(r.stderr[-2000:])

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(dist / "dse-econ-graph.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in [SKILL, ROOT / "dsegraph.py", *EXAMPLES]:
            z.write(f, Path("dse-econ-graph") / f.relative_to(ROOT))
    print(f"packed dist/dse-econ-graph.zip")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
