# Recipes

A recipe says what a diagram contains in economics terms: the curves and their roles, which one shifts and which
way, price or quantity lines (a ceiling, a floor, a quota), marked points, shaded areas, braces, labels and the
language. It has **no coordinates**. DSEconMentor's chat tutor writes recipes and draws them with its own renderer,
in this library's look (plan: DSEconMentor `docs/DIAGRAM_RECIPE_PLAN.md`). Teachers never see this folder; it is not
in SKILL.md, the zips or `manifest.json`.

| File | What |
|---|---|
| `schema.json` | The recipe format, v1 (JSON Schema). Adding optional fields is fine; renaming or removing one needs v2. |
| `glossary.json` | Words a recipe uses by key, English and Traditional Chinese (HK wording, the SKILL.md table). Keys are a contract. |
| `<id>.json` | One recipe per catalogue id (every template and chat variant), the starting points the chat model edits. Each also has `geom`: the template's own numbers, so the renderer reproduces the template exactly. |
| `fit.json` | Per id: `full`, or `partial` with what the picture shows that the schema cannot say yet. |
| `golden/<id>_<lang>.scene.json` | The template's finished picture as primitives (`tools/trace.py`), traced with Liberation Serif and Noto Serif CJK TC, the fonts the renderer bundles. DSEconMentor's tests compare its renderer against these. |

## Checks

- `python tools/recipes.py` checks every recipe: the schema; references (ids, roles for the family, glossary keys);
  `geom` against the golden scene (each curve drawn where geom says, shifts and the tax as offsets of their base
  curve, lines at their level, every name, label, note and axis title in the EN and 中 pictures); and the economics
  with the template's numbers (shift directions, ceilings below / floors above / quotas left of equilibrium,
  vertical curves where `at` says, `onto` and `biggerThan` sizes, `expect` against the first and last equilibria).
- `python tools/trace.py --check` re-traces every template and compares with `golden/`.
- `python tools/build.py --check` runs both; a full build re-traces `golden/` after rendering.

## Changing a template

Change its recipe in the same commit (curve names, levels, `geom`), run `python tools/build.py`, and make sure
`tools/recipes.py` passes. A new template or variant needs a recipe and a `fit.json` entry, like its `chat/meta.json`
entry. Recipe ids are catalogue ids: never rename or remove one.
