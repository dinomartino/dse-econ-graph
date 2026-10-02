# dse-econ-graph

**Draw HKDSE Economics diagrams in code — in the black-and-white HKEAA
marking-scheme style, in English and Traditional Chinese.**

An AI skill plus a tiny Python library. Give it to any AI assistant
(Gemini, ChatGPT, Claude, …), describe a question or paste a marking scheme,
and you get back one Python script that draws the diagram exactly like the
official papers: Times-style serif (Chinese: Ming/Song serif), thin lines,
arrow axes, dashed guides, `////` hatching, curly braces. No colour, no
blurry scans, no AI-art look. Copy it, run it, paste the PNG into your notes.

| English | 中文 |
|---|---|
| ![](gallery/01_price_ceiling_shortage_en.png) | ![](gallery/01_price_ceiling_shortage_zh.png) |
| ![](gallery/05_tr_price_change_elastic_en.png) | ![](gallery/05_tr_price_change_elastic_zh.png) |
| ![](gallery/09_externality_overproduction_en.png) | ![](gallery/09_externality_overproduction_zh.png) |

More in [`gallery/`](gallery/).

## For teachers — no coding needed

### 👉 Start here: **[dinomartino.github.io/dse-econ-graph](https://dinomartino.github.io/dse-econ-graph/)**

One page, in 中文 and English, with a big **Copy** button. Nothing to
download, no GitHub.

**With Gemini (recommended):**
1. On the start page click **Copy the instructions**.
2. gemini.google.com ▸ **Explore Gems** ▸ **New Gem** ▸ name it
   `DSE Econ Graph 經濟圖表` ▸ paste into **Instructions** ▸ **Save**.
   (Once only. Share the Gem's link and colleagues skip this step.)
3. Open the Gem, paste a question and its marking scheme, say English
   and/or Chinese.
4. Under Gemini's code click **Export to Colab**, press **▶** — the
   picture appears and downloads.

Not quite right? Tell Gemini in words ("make demand steeper", "Chinese
only") and do step 4 again.

### 老師使用說明

👉 **由這裏開始：[dinomartino.github.io/dse-econ-graph](https://dinomartino.github.io/dse-econ-graph/)**（中英對照，有「複製」按鈕，不用下載，不用 GitHub）

1. 在網頁按 **複製指示**。
2. 到 gemini.google.com ▸ **探索 Gem** ▸ **新增 Gem**，名稱 `DSE Econ Graph 經濟圖表`，把指示貼到 **指示** 欄，按 **儲存**（只需一次；把 Gem 連結分享給同事，他們連這步也不用做）。
3. 打開 Gem，貼上題目和評卷參考，註明要中文／英文。
4. 按 Gemini 程式碼下方的 **Export to Colab**，再按 **▶**，圖片會出現並自動下載。

### With Claude or ChatGPT

These can run the code themselves and hand you the picture directly.

- **Claude (claude.ai):** Settings ▸ Capabilities — turn on *Code execution
  and file creation*; under *Skills* upload
  [`dse-econ-graph.zip`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/dse-econ-graph.zip)
  (once). Then just ask.
- **ChatGPT / any chat:** paste the instructions from the start page as
  the first message (or make a GPT with them). ChatGPT can usually run the
  code itself — add *"Run the code and give me the PNG files."*

## For other AI tools and developers

| Where | How |
|---|---|
| **Claude Code** | `git clone https://github.com/dinomartino/dse-econ-graph ~/.claude/skills/dse-econ-graph` — then just ask "draw the shortage diagram for …" |
| **Custom GPT / Gem / Project** | add `SKILL.md` as knowledge, so every chat can draw without attaching it |
| **Your own Python** | `pip install matplotlib pillow`, put `dsegraph.py` beside your script (below) |

## Use the library directly

```python
from dsegraph import *

setup("zh")                                   # or "en"
fig, ax = new(3.2, 2.6)                       # printed size in inches
O = (12, 12)
axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))
D = Line((20, 82), (78, 22)); S = Line((20, 22), (78, 82))
draw(ax, D, 20, 78, "D"); draw(ax, S, 20, 78, "S")
P = 34
line(ax, (O[0], P), (84, P)); label(ax, 10.5, P, "P", ha="right")
brace(ax, S.x(P), D.x(P), P - 1, T("shortage", "短缺"))
save(fig, "shortage.png")
```

Every point comes from exact geometry (`meet(D, S)`, `D.x(P)`,
`S.shift(dx=10)`, `S.shift(dy=tax)`), so curves always meet where the
labels say. See the [templates](examples/) for price floors, shifting
demand at a fixed price, total revenue and elasticity, unit tax incidence,
consumer / producer surplus and deadweight loss, externalities and the PPC.

## Fonts

English uses Times New Roman, or the Times-like STIX font that ships with
matplotlib. Chinese uses the first serif it finds: PMingLiU / MingLiU
(Windows), Songti TC (macOS), Noto Serif CJK TC (Linux); otherwise a font
file you upload next to the script, otherwise it downloads the free Noto
Serif TC once (about 17 MB) — so Colab, ChatGPT and Claude work with no
setup.

## Contributing

Add a template as `examples/NN_name.py` (copy an existing one: a
`diagram(lang)` function that makes both languages), then run

```bash
python tools/build.py
```

which re-renders the gallery, pastes the current library and template list
into `SKILL.md`, and packs `dist/dse-econ-graph.zip`.

## Notes

- The style imitates the diagrams in HKEAA marking schemes; this project is
  not affiliated with or endorsed by the HKEAA.
- Chinese terms follow the EDB *English-Chinese Glossary of Terms Commonly
  Used in the Teaching of Economics in Secondary Schools* (2020).
- MIT licence.
