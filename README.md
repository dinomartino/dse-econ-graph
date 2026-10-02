# dse-econ-graph

**Draw HKDSE Economics diagrams in code — in the black-and-white HKEAA
marking-scheme style, in English and Traditional Chinese.**

An AI skill plus a tiny Python library. Attach it to any AI chat (Gemini,
ChatGPT, Claude, …), paste a question and its marking scheme, and the AI
draws the diagram exactly like the official papers — Times-style serif
(Chinese: Ming/Song serif), thin lines, arrow axes, dashed guides, `////`
hatching, curly braces — and shows you the picture. No colour, no blurry
scans, no AI-art look.

| English | 中文 |
|---|---|
| ![](gallery/01_price_ceiling_shortage_en.png) | ![](gallery/01_price_ceiling_shortage_zh.png) |
| ![](gallery/05_tr_price_change_elastic_en.png) | ![](gallery/05_tr_price_change_elastic_zh.png) |
| ![](gallery/09_externality_overproduction_en.png) | ![](gallery/09_externality_overproduction_zh.png) |

More in [`gallery/`](gallery/).

## For teachers — no coding needed

1. Download **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)** (one click).
2. Open Gemini (or ChatGPT, Claude, any AI chat), attach `SKILL.md`, and
   paste the question and its marking scheme. Say English, Chinese or both.
3. The AI draws the diagram and **shows the picture in the chat**.
   Right-click it ▸ *Save image as…* and put it in your worksheet.

Not quite right? Say so in words — *"make demand steeper"*, *"move
'shortage' lower"*, *"Chinese only"* — and it draws it again.

> Draw the diagram for this DSE question in English and Chinese.
> Question: … Marking scheme: "Indicate in the diagram: price below
> equilibrium (1), rightward shift of demand (1), shortage increases from
> a to b (1)."

### 老師使用說明（不需識寫程式）

1. 下載 **[`SKILL.md`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/SKILL.md)**（按一下即可）。
2. 打開 Gemini（或 ChatGPT、Claude 等任何 AI），附加 `SKILL.md`，貼上題目和評卷參考，註明要中文、英文或兩者。
3. AI 會畫好圖並**直接在對話中顯示圖片**。在圖片上按右鍵 ▸「另存圖片」即可使用。

要修改？直接用文字告訴它，例如「需求曲線畫斜一點」、「只要中文版」，它會重畫。

## For developers

| Where | How |
|---|---|
| **Claude Code** | `git clone https://github.com/dinomartino/dse-econ-graph ~/.claude/skills/dse-econ-graph` |
| **Claude.ai Skills** | upload [`dse-econ-graph.zip`](https://github.com/dinomartino/dse-econ-graph/releases/latest/download/dse-econ-graph.zip) |
| **Your own Python** | `pip install matplotlib pillow`, put `dsegraph.py` beside your script |

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
file you upload, otherwise it downloads the free Noto Serif TC once
(about 17 MB).

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
