# Decisions

Why things are the way they are. Newest first. One entry per decision:
what was decided, why, and what we rejected.

## 2026-10-02 — One zip; Grok, then Claude, then ChatGPT

- **Decided:** teachers download only `dse-econ-graph.zip` (guide,
  instructions text, library, all templates) and upload it as-is, even in
  the web versions: a Skill in Claude, project files in Grok and ChatGPT
  plus the instructions text. The AI unzips it and imports the library.
- **Order:** Grok first (works in Hong Kong), then Claude and ChatGPT
  (both need a VPN in HK). Gemini is no longer offered.
- **Risk to test:** whether Grok's project files accept a .zip and let its
  code tool open it. SKILL.md / SKILL.txt stay in the release as the
  fallback.

## 2026-10-02 — Mirror the KP_ECON answer diagrams (S&D and AD-AS)

- **Decided:** one template per distinct S&D / AD-AS diagram type found in
  the KP_ECON marking schemes (catalogued from 181 unique answer images and
  `Reference/Diagram_Requirements`). Every template's full code is pasted
  into SKILL.md, because chat AIs only see that one file. The guide gets a
  topic index with the scheme IDs each template mirrors.
- **Scope:** S&D and AD-AS only, as the maintainer asked. Other diagram
  families are out.
- **Conflicts in the schemes, resolved:** TR shown as whole rectangles
  (CE1997, CE1999) → we still show only the change (rule since v1.4.1).
  Hatch patterns differ across scans, so the pattern carries no meaning;
  the sign or legend does.
- **Cost:** SKILL.md grows to ~125 KB. Fine for Grok, Claude and Gemini;
  ChatGPT may read large project files only in parts (watch in tests).

## 2026-10-02 — Paste the question, get the picture

- **Decided:** the teacher pastes only the question and marking scheme. The
  AI replies with the picture(s) only, in the question's language, one per
  part, never asking questions or showing code (except the colab.new
  fallback).
- **Why:** the maintainer's requirement: teachers must not need to write
  any instruction.

## 2026-10-02 — Works with every major AI, not only Grok (v1.5.0)

- **Decided:** one provider-neutral guide (`SKILL.md`) and one
  `instructions.txt` for all AIs. Only the setup steps differ, one entry per
  AI in `teacher/setup.json` → `providers` in the manifest. Claude gets
  the `.zip` skill; Grok, ChatGPT and Gemini get instructions + SKILL.md
  in a Project or Gem.
- **Why:** the maintainer asked for it to work with other providers too;
  teachers use whichever AI their school allows.
- **Rejected:** a separate guide per AI. It would drift apart and double
  the upkeep.

## 2026-10-02 — Grok is the main AI (v1.5.0)

- **Decided:** write and test for Grok first. Teachers set it up once in a
  Grok Project (instructions text + SKILL.md in the files).
- **Why:** in the maintainer's words, Gemini couldn't really handle it.
- **How:** Grok runs the whole library plus the diagram in its own sandbox
  and shows the picture in the chat. Its sandbox has no internet, so the
  library never downloads at run time. If there's no Chinese font, or no
  picture, Grok gives a colab.new script as the fallback.
- **Rejected:** a "Draw" web page that runs the code in the browser
  (Pyodide) while Grok only writes the recipe. It would be more reliable,
  but the maintainer didn't want another web page. Reconsider only if
  `grok-test.md` shows Grok can't display pictures.

## 2026-10-02 — Files for the maintainer's website

- **Decided:** a committed `download/` folder with fixed filenames and a
  `manifest.json` (version, what's new, setup steps EN/繁中, links,
  gallery). The website reads the manifest from `raw.githubusercontent.com`
  (allows cross-site reads) and uses `releases/latest/download/<name>`
  links for the buttons (they make the browser save the file).
- **Why:** the maintainer already has a website and only needs the files to
  be easy to fetch. The teacher never sees GitHub.
- Version and what's new come from `CHANGELOG.md`, so there's one place to
  edit.

## 2026-10-02 — One self-contained SKILL.md (v1.0–1.4)

- The library is pasted inside SKILL.md (generated blocks) so one file
  works in any chat, with no installs or downloads.
- Picture shown in the chat, no code shown, changes asked for in words.
- TR diagrams show only the change in TR (v1.4.1).
