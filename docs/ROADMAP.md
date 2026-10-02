# Roadmap

What to do next, most important first. Move finished items to the bottom
with the date and version. Record why in `DECISIONS.md` when a choice is
made.

## Now: confirm Grok actually works (blocking)

- [ ] **ChatGPT:** does Plugins ▸ Upload plugin accept
      `dse-econ-graph-chatgpt.zip`? If it rejects a plugin.json field, the
      error names it; fix `plugin_json()` in `tools/build.py`. Does the
      plugin's skill trigger inside a project chat?

- [ ] **Does Grok accept `dse-econ-graph.zip` in project files, and can its
      code tool unzip it?** If not, tell teachers to upload SKILL.md
      instead (it's in every release) and change `teacher/setup.json`.

Nobody has run v1.5.0 on grok.com yet. These unknowns decide the next steps.
Run the test in [`grok-test.md`](grok-test.md) and record the answers here.

- [ ] **Does Grok show the matplotlib picture in the chat?** If not, the
      whole "picture in the chat" idea fails on Grok; the fallback is the
      colab.new script, which is much worse for teachers. Then rethink.
- [ ] **Does Grok's sandbox have a Chinese font?** (`fc-list :lang=zh`.)
      If not, can it read a font file uploaded to the chat or project? If
      both are no, 中文 always goes through Colab.
- [ ] **Does Grok paste the whole library faithfully** (about 20 KB), or
      does it shorten or "improve" it? If it drifts, make the library
      smaller or split it into a core part and an optional part.
- [ ] **Project feature:** check the real names of the Projects /
      Instructions / Files buttons on grok.com, the instruction length
      limit, and whether free accounts have Projects. Fix the wording in
      `teacher/setup.json` to match the screen exactly.
- [ ] **Other AIs:** run part 2 of `grok-test.md` in ChatGPT, Claude and
      Gemini too, and check each one's button names in `teacher/setup.json`
      (ChatGPT project Instructions, Claude Settings ▸ Capabilities ▸ Skills,
      Gemini New Gem ▸ Knowledge). Mark the best one `recommended`.
- [ ] Which Grok model and mode works best (auto / expert / fast)? Put it
      in the teacher steps if it matters.

## Next

- [ ] Test the new S&D and AD-AS templates against real questions in Grok:
      paste 5 LQs per topic from KP_ECON and compare with the scheme images.
- [ ] Watch SKILL.md size (~125 KB). If ChatGPT or Grok misses parts,
      strip docstrings/comments from the pasted library and template code.

- [ ] Run the 11 templates' typical questions through Grok and keep a
      small "Grok results" log (question → OK / what went wrong). Turn
      repeated mistakes into rules in SKILL.md.
- [ ] Chinese titles for the gallery (manifest `gallery[].title` is
      English only), e.g. a `zh:` line in each example's docstring.
- [ ] Screenshots of the Grok setup steps for the website (EN + 中文 UI).

## Later / ideas

- [ ] A GitHub Action running `python tools/build.py --check` on every push.
- [ ] Shrink the library for pasting (strip docstrings in the SKILL.md copy).

## Done

- 2026-10-02 v1.5.0: 32 new S&D and AD-AS templates mirroring the KP_ECON
  answers (43 in all), full template code and a topic index in SKILL.md,
  and a build step that runs every template as pasted from the guide.

- 2026-10-02 v1.5.0: Grok first, with ChatGPT / Claude / Gemini setups
  (`providers` in the manifest); provider-neutral `instructions.txt`;
  `download/` + `manifest.json` for the website; offline-safe Chinese font search; release script; these docs.
