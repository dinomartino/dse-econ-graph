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

### With Gemini (gemini.google.com)

**Once:** download **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)**
— it teaches Gemini how to draw DSE diagrams. (Your department can also
make a shared Gem so nobody needs the file: see
[`gemini/GEM_SETUP.md`](gemini/GEM_SETUP.md).)

**Each diagram:**
1. Open Gemini, attach `SKILL.md` with **＋**, and ask — paste the question
   and the marking scheme, say English and/or Chinese.
2. Gemini replies with a block of code. Click **Export to Colab** under it
   (in the code box's share / ⋮ menu).
3. Colab opens: press **▶**. Sign in with Google if asked, and click
   **Run anyway** if asked.
4. The picture appears and downloads to your computer. (First run: about
   a minute.)

No *Export to Colab* button? Copy the code, click
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dinomartino/dse-econ-graph/blob/main/DSE_Graph_Maker.ipynb),
paste it into *Step 2*, then **Runtime ▸ Run all**.

**What to type:**

> Draw the diagram for this DSE question in English and Chinese.
> Question: … Marking scheme: "Indicate in the diagram: price below
> equilibrium (1), rightward shift of demand (1), shortage increases from
> a to b (1)."

Not quite right? Tell Gemini in words — *"put 'shortage' lower"*, *"make
demand steeper"*, *"Chinese only"* — and export the new code again. Got
a red error in Colab? Copy it to Gemini: *"I got this error, please give me
the whole corrected code."*

### 老師使用說明（Gemini，不需識寫程式）

**只需一次：** 下載 **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)**，這個檔案教 Gemini 如何畫 DSE 經濟圖。（科組亦可建立一個共用 Gem，大家打開連結即可用，不用附加檔案，見 [`gemini/GEM_SETUP.md`](gemini/GEM_SETUP.md)。）

**每次畫圖：**
1. 打開 Gemini，用 **＋** 附加 `SKILL.md`，貼上題目和評卷參考，註明要中文、英文或兩者。
2. Gemini 會給你一段程式碼。按程式碼下方的 **Export to Colab（匯出至 Colab）**（在程式碼框的分享／⋮ 選單）。
3. Colab 打開後按 **▶**。如要求登入 Google 請登入；見到「仍要執行」請按 **仍要執行**。
4. 圖片會出現並自動下載到你的電腦（第一次約需一分鐘）。

找不到 *Export to Colab*？複製程式碼，按上面的 **Open in Colab**，貼到 *Step 2*，再按 **執行階段 ▸ 全部執行**。

**可以這樣問：**

> 請按這題 DSE 題目及評卷參考，畫中英文版本的圖。
> 題目：…… 評卷參考：「在圖中標示：價格低於均衡價格 (1)、需求曲線右移 (1)、短缺由 a 增至 b (1)。」

不滿意？直接用文字告訴 Gemini，例如「把『短缺』移低一點」、「需求曲線畫斜一點」、「只要中文版」，再匯出新的程式碼。Colab 出現紅色錯誤？複製給 Gemini：「出現這個錯誤，請給我完整修正後的程式碼。」

### With Claude or ChatGPT

These can run the code themselves and hand you the picture directly.

- **Claude (claude.ai):** Settings ▸ Capabilities — turn on *Code execution
  and file creation*; under *Skills* upload
  [`dse-econ-graph.zip`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/dse-econ-graph.zip)
  (once). Then just ask.
- **ChatGPT:** attach `SKILL.md`, ask, and add *"Run the code and give me
  the PNG files."*

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
