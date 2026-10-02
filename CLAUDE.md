# dse-econ-graph — working notes for Claude

Read this first. Then read `docs/ROADMAP.md` (what to do next) and
`docs/DECISIONS.md` (why things are the way they are). At the end of a
session, update both.

## Who this is for

- **End user: a Hong Kong secondary-school economics teacher.** Knows
  nothing about code, GitHub, Python or files beyond "download" and
  "copy & paste". Never ask them to install, run, clone or edit anything.
- **The only thing they touch:** the maintainer's own website, which has
  download buttons for the files in `download/`, plus their AI chat.
- **AIs, in the order we recommend them:** Grok (works in Hong Kong),
  then Claude, then ChatGPT (both need a VPN in HK). Gemini handled it
  poorly and is no longer offered to teachers, but don't break it. Keep
  SKILL.md and `instructions.txt` provider-neutral; per-AI setup steps live
  in `teacher/setup.json` (`providers`).
- **One download: `dse-econ-graph.zip`.** It holds SKILL.md,
  instructions.txt, dsegraph.py and every template (the claude.ai skill
  layout). Teachers upload it as-is: a Skill in Grok (Plugins ▸ Skills ▸ Add
  skill ▸ Upload skill file, checked on grok.com 2026-10-03) and in Claude;
  ChatGPT takes its own zip plus the instructions text in a project. The AI unzips it and imports the
  library from the folder (pasting the library is the fallback).
  **ChatGPT needs its own zip**, `dse-econ-graph-chatgpt.zip`: its Upload
  plugin rejects the claude.ai layout and wants `.codex-plugin/plugin.json`
  + `skills/dse-econ-graph/`. Claude needs `dse-econ-graph/SKILL.md` at the
  zip's top, so one zip can't serve both. The build makes both.
- **The maintainer** (repo owner) uses voice typing: "Germany" = Gemini,
  "grog" = Grok, "ship" = skill. They want short answers and few questions.
  They already have the website, so don't propose another one or a hosted
  draw page (declined 2026-10-02).

## The contract with the teacher

**The teacher pastes a question and its marking scheme. The AI replies with
the finished picture only:** no code, no explanation, no questions. The
language follows the question (中文 question → 中文 diagram), with one
picture per part. Every change must keep this true. Code appears only in
the colab.new fallback, when the AI can't show pictures or Chinese.

## How it works

```
teacher ──► Grok Skill / Claude Skill (dse-econ-graph.zip)
            · ChatGPT plugin + Project (instructions text)  · any chat (attach the zip)
              │  the AI writes ONE script = whole dsegraph library + diagram
              ▼  runs it in its offline sandbox ▸ picture shown in chat
           fallback: script for colab.new (no picture / no Chinese font)
```

| Path | What | Edit? |
|---|---|---|
| `dsegraph.py` | The drawing library (matplotlib + pillow). Source of truth. | yes |
| `examples/NN_*.py` | Templates: `diagram(lang)` makes EN and ZH. The docstring's `Topic:` / `Use for:` lines build the guide's index; all template code is pasted into SKILL.md. | yes |
| `SKILL.md` | The guide the AI follows. Prose is hand-written; blocks between `<!-- BEGIN x -->` / `<!-- END x -->` are generated. | prose only |
| `teacher/instructions.txt` | Text the teacher pastes into the Grok / ChatGPT project instructions. Provider-neutral, short (< 1600 chars). Also in the zip, in the manifest (`instructions_text`) and synced into README. | yes |
| `teacher/setup.json` | Setup steps shown on the website, EN + 繁中: one entry per AI in `providers`, plus `use`, `quick`, `updating`. | yes |
| `README.md` | Teacher-first page (EN + 繁中). The block between `<!-- BEGIN INSTRUCTIONS -->` markers is generated. | yes, except that block |
| `CHANGELOG.md` | Top entry = current version + "what's new" (`- en:` / `- zh:` lines). | yes |
| `download/` | Built files for the website + `manifest.json`. | **never by hand** |
| `gallery/` | PNGs rendered from `examples/`. | built |
| `tools/build.py` | Syncs SKILL.md, renders gallery, runs every template exactly as pasted from SKILL.md under the library (the "pasted test"), writes `download/`. | yes |
| `tools/release.py` | Pushes and creates the GitHub release. | yes |

## Where the diagrams come from

The templates mirror the diagrams in the maintainer's teaching materials,
**KP_ECON** (iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/KP_ECON`).
It is **read-only** for this project: never write there, and copy files out
before unzipping.
- `Reference/Diagram_Requirements/` lists what every diagram question must
  show (`00_ALL…md`, section 8 = checklist by diagram type).
- Answer images: `S4/R3/LQ/images_review/*_orig.*`, `S4/R4/LQ/images_review`,
  and `word/media` inside `LQ/<topic>/<topic>.docx` (English files).
- **Scope: supply & demand and AD-AS only** (maintainer, 2026-10-02).
  Monopoly, PPF, trade, exchange rate, money market and Lorenz are out.
  KP has no AD-AS images, so those templates follow the text requirements.

## Rules

1. **Download filenames are a public contract.** The website and old links
   use `releases/latest/download/<name>` and `raw…/main/download/<name>`
   for `SKILL.md`, `SKILL.txt`, `instructions.txt`, `dse-econ-graph.zip`,
   `dse-econ-graph-chatgpt.zip` and `manifest.json`. Never rename or remove one.
   Adding files or manifest fields is fine.
2. **Everything a teacher reads is bilingual** (English + Traditional
   Chinese, HK wording, EDB glossary terms), short, and free of code words.
3. **Diagrams:** black and white, HKEAA marking-scheme look, computed
   geometry (`meet`, `Line.x`, `shift`). Economics rules are in SKILL.md
   ("Economics that is easy to get wrong"). TR diagrams show only the
   change in TR.
4. **SKILL.md must stay self-contained:** Grok's and ChatGPT's sandboxes have no internet,
   so the AI pastes the whole library into its script. Keep the library
   lean, because every extra line is pasted on every request.
5. **Adding a template:** next free number, the docstring format of the
   others (`Topic:` must be one of `TOPICS` in `tools/build.py`; `Use for:`
   with the scheme IDs), under ~2.2 KB, and render and look at both PNGs.
6. **Adding an AI:** add an entry to `providers` in `teacher/setup.json`
   (check the real button names), a row in README's table, and a test in
   `docs/grok-test.md`. Don't put provider-only rules in SKILL.md unless
   that AI needs them; the same file must work everywhere.
7. After any change, run `python tools/build.py` and **look at the changed
   gallery PNGs** (Read them) before committing. Check both `_en` and `_zh`.

## Release (only when the maintainer asks)

1. Add a new top entry to `CHANGELOG.md` (`## X.Y.Z — YYYY-MM-DD`, then
   `- en:` / `- zh:` lines written for teachers).
2. `python tools/build.py` → check gallery → commit.
3. `python tools/release.py "short title"`. It checks, pushes and creates
   the GitHub release with every `download/` file attached.

The website picks up the new `manifest.json` within about 5 minutes.
