# dse-econ-graph

**Draw HKDSE Economics diagrams in code — in the black-and-white HKEAA
marking-scheme style, in English and Traditional Chinese.**

An AI skill plus a tiny Python library. Give it to any AI assistant
(Claude, ChatGPT, Gemini, …), describe a question or paste a marking scheme,
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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dinomartino/dse-econ-graph/blob/main/DSE_Graph_Maker.ipynb)

First download **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)**
(one click). That file teaches the AI how to draw DSE diagrams. Then pick
the AI you already use:

**A. Claude (claude.ai)** — easiest
1. Settings ▸ Capabilities: turn on *Code execution and file creation*.
   Under *Skills*, upload [`dse-econ-graph.zip`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/dse-econ-graph.zip). (Once only.)
2. In any chat, ask for the diagram. Claude draws it and gives you the
   picture to download.

**B. ChatGPT**
1. Start a chat, attach `SKILL.md` (📎).
2. Ask for the diagram and add: *"Run the code and give me the PNG files."*
3. Download the pictures it returns.

**C. Any other AI** (Gemini, DeepSeek, Poe, Copilot …)
1. Attach or paste `SKILL.md`, ask for the diagram. It replies with code.
2. Click **Open in Colab** above, paste the code into *Step 2*, then
   **Runtime ▸ Run all**. The pictures download by themselves.

**What to type** — paste the question and the marking scheme, say which
language:

> Draw the diagram for this DSE question in English and Chinese.
> Question: … Marking scheme: "Indicate in the diagram: price below
> equilibrium (1), rightward shift of demand (1), shortage increases from
> a to b (1)."

Not quite right? Just say so in words — *"put 'shortage' lower"*, *"make
demand steeper"*, *"Chinese only"* — and ask for the picture again.

### 老師使用說明（不需識寫程式）

先下載 **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)**（按一下即可）。這個檔案教 AI 如何畫 DSE 經濟圖。然後選擇你平日用的 AI：

**A. Claude（claude.ai）** — 最簡單
1. 設定 ▸ Capabilities：開啟 *Code execution and file creation*；在 *Skills* 上載 [`dse-econ-graph.zip`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/dse-econ-graph.zip)（只需做一次）。
2. 在任何對話中請它畫圖，Claude 會直接給你圖片下載。

**B. ChatGPT**
1. 開新對話，用 📎 附加 `SKILL.md`。
2. 請它畫圖，並加一句：「請執行程式碼，把 PNG 圖片給我。」
3. 下載它給你的圖片。

**C. 其他 AI**（Gemini、DeepSeek、Poe、Copilot 等）
1. 附加或貼上 `SKILL.md`，請它畫圖，它會給你一段程式碼。
2. 按上面的 **Open in Colab**，把程式碼貼到 *Step 2*，再按 **執行階段 ▸ 全部執行**，圖片會自動下載。

**可以這樣問：** 貼上題目和評卷參考，並註明語言：

> 請按這題 DSE 題目及評卷參考，畫中英文版本的圖。
> 題目：…… 評卷參考：「在圖中標示：價格低於均衡價格 (1)、需求曲線右移 (1)、短缺由 a 增至 b (1)。」

不滿意？直接用文字告訴它，例如「把『短缺』移低一點」、「需求曲線畫斜一點」、「只要中文版」，再請它重新給你圖片。

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
