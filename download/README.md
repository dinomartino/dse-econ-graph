# download/ — for the website

Everything a teacher downloads, plus `manifest.json` describing it. Made by
`python tools/build.py`; do not edit these files by hand. The names never
change, so links to them keep working.

| File | What the teacher does with it |
|---|---|
| `dse-econ-graph.zip` | **The one download.** Uploads it to Grok / ChatGPT project files, or as a Skill in Claude. Holds everything below plus the library and templates. |
| `instructions.txt` | Text pasted into the Grok / ChatGPT project's Instructions (also in the manifest as `instructions_text`, to show in a copy box) |
| `SKILL.md`, `SKILL.txt` | The guide alone, only for an AI that can't open the zip |
| `manifest.json` | (for the website) version, what's new, setup steps, links, gallery |

## Reading it from the website

```js
const M = "https://raw.githubusercontent.com/dinomartino/dse-econ-graph/main/download/manifest.json";
const m = await (await fetch(M, { cache: "no-cache" })).json();
// m.version, m.released            "1.5.0", "2026-10-02"
// m.whats_new.en / .zh             string[]
// m.files[]                        { name, title{en,zh}, description{en,zh}, bytes, sha256, url, download_url }
// m.instructions_text              the text teachers paste into Grok / ChatGPT project Instructions
// m.providers[]                    in recommended order: { id: "grok"|"claude"|"chatgpt", name, url,
//                                    recommended, needs_vpn_in_hk, files: [names of m.files to offer],
//                                    title{en,zh}, steps{en[],zh[]} }
// m.use / m.quick / m.updating     { title{en,zh}, steps{en: string[], zh: string[]} }
//   use      = how to draw once set up (same for every AI)
//   quick    = no setup: attach the zip to any chat
//   updating = what to do when a new version is out
// m.gallery[]                      { id, title, en: png url, zh: png url }
```

- **Page idea:** an AI picker (tabs from `providers`, the `recommended`
  one first). Each tab shows its `files` as buttons, its `steps`, then `use`.
- **Download buttons:** use `download_url` (the latest GitHub release). It
  makes the browser save the file. `url` opens it as text instead.
- **Reading with `fetch()`:** use `url` or the manifest URL above.
  `raw.githubusercontent.com` allows cross-site reads; GitHub release links
  do not.
- `raw.githubusercontent.com` caches for about 5 minutes, so a new version
  shows up a few minutes after it is pushed.
- Fields may be added in later versions; existing fields keep their meaning.
