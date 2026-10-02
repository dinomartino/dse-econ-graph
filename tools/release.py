"""Publish the current version as a GitHub release.

    python tools/release.py "short title"

Takes the version and notes from the top entry of CHANGELOG.md, checks that
everything is built and committed, pushes main, then creates release
vX.Y.Z with every file in download/ attached — so the website's
`releases/latest/download/<name>` links serve the new files.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from build import FILES, changelog  # noqa: E402


def run(*cmd: str, check: bool = True) -> str:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"{' '.join(cmd)} failed:\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    title = sys.argv[1]
    log = changelog()
    tag = f"v{log['version']}"

    run(sys.executable, "tools/build.py", "--check")
    if run("git", "status", "--porcelain"):
        raise SystemExit("uncommitted changes — commit them first")
    if run("git", "branch", "--show-current") != "main":
        raise SystemExit("not on main")
    if run("git", "tag", "--list", tag):
        raise SystemExit(f"{tag} already exists — add a new entry at the top of CHANGELOG.md")

    notes = "\n".join(f"- {line}" for lang in ("en", "zh") for line in log["whats_new"][lang])
    run("git", "push", "origin", "main")
    run("gh", "release", "create", tag, "--target", "main", "--title", f"{tag} — {title}",
        "--notes", notes, *[f"download/{name}" for name in FILES], "download/manifest.json")
    print(f"released {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
