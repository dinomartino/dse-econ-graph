---
name: dse-econ-graph
description: Draw HKDSE / HKCEE Economics diagrams as copy-paste Python code that reproduces the black-and-white HKEAA marking-scheme style, in English or Traditional Chinese — demand and supply, shortage / surplus, price ceilings and floors, minimum wage, total revenue and elasticity, unit tax incidence, consumer / producer surplus and deadweight loss, quotas, externalities, PPC. Use whenever someone asks to draw, redraw, recreate or clean up an economics graph or diagram for DSE (or any exam in that style), to replace a blurry scanned or AI-coloured graph, or to answer a "with the aid of a diagram" question.
---

# DSE Economics diagrams in code

Recreate exam-quality economics diagrams — the kind printed in HKEAA marking
schemes — by writing a short Python (matplotlib) script. The look is fixed:
black on white, Times-style serif (Chinese: Ming/Song serif), thin lines,
arrow-headed axes, dashed guide lines, `////` hatching and `....` dotted
fills, curly braces for shortages. No colour, no grid, no title box.

This file is self-contained. The whole drawing library, `dsegraph`, is at the
end ("The library"); any assistant — including a web chat with no files —
can paste it into the script it writes.

## What you give the user

The users are economics teachers in a **web chat**: Grok, ChatGPT, Claude,
Gemini or another AI that can run Python. They do not code. They paste a
**question and its marking scheme** — nothing else — and expect **the
finished picture back, straight away**. No code, no explanations, no
questions.

### In a web chat: the pasted question in, the picture out

Whenever the message contains an economics question or marking scheme
(with or without any other words), treat it as "draw the diagram(s) for
this":

1. **Decide everything yourself — never ask.** Which diagram, which curves
   shift, which areas, labels: all from the question and the marking
   scheme (see "Workflow"). If something is unclear, choose what the
   marking scheme rewards.
   - **Language** = the language of the pasted question: Chinese text →
     `zh`, English → `en`. Both only if the teacher asks for both.
   - **Several parts** that each need a diagram ((b)(i), (b)(ii) …, or
     "in separate diagrams") → one picture per part, in order.
2. Write ONE script: the library, then the diagram(s), saving
   `diagram_en.png` / `diagram_zh.png` (or `diagram_b_i_en.png` … for
   several parts). The library: if `dse-econ-graph.zip` was uploaded, unzip
   it once with your code tool and start the script with
   `import sys; sys.path.insert(0, "dse-econ-graph"); from dsegraph import *`
   (adjust the folder to where you unzipped it). Otherwise paste the whole
   library from "The library" below at the top, unchanged. Do not
   `pip install` or download anything — chat code tools (Grok's, ChatGPT's)
   usually have no internet.
3. **Run it with your code tool.** `save()` displays the finished picture,
   so it appears in the chat. Look at it; fix anything from the checklist
   and run again — silently.
4. **Reply with the picture(s) ONLY.** No code, no economics explanation,
   no "here is your diagram", no follow-up questions. With several
   pictures, put just the part label (e.g. "(b)(i)") above each. Attach or
   link the PNG files too if your chat can.
5. If the teacher then asks for a change in words ("make demand steeper",
   "Chinese too"), edit, run again and reply with the new picture only.

`save()` also tidies the picture: a label touching a line, arrow, brace or
another label is moved to a clear spot. A printed line
`dsegraph note: … crowded` means it could not — move that label yourself
and run again.

**Chinese.** `setup("zh")` uses any installed Chinese font, else a font
file the user uploaded, else downloads one. If it prints
`dsegraph: NO CHINESE FONT`, the Chinese labels are boxes □□ — do not show
that picture. Show the English one, and give the Chinese version as a
Colab script (below) with one line: "Your chat can't draw Chinese text —
for the 中文 version, open colab.new, paste this, press ▶." This and the
case below are the only times you show code or extra words.

**If the picture does not appear in the chat**, or you cannot run code at
all: say so in one line, and give the complete script (library + diagram)
in one code block with: "Open colab.new, paste this, press ▶ — the
picture appears below it and downloads." Colab has internet, so Chinese
works there too.

### In a coding tool (Claude Code, Codex, …)

Same script; save the PNGs where the user wants them, look at them, and
report the file paths.

### Using it again

Teachers upload `dse-econ-graph.zip` (this guide, the instructions text,
the library and every template) once: as a **Skill** in Claude, or into a
**Project** in Grok or ChatGPT together with the short instructions text.
Otherwise they attach the zip (or this file) again in a new chat.
If a teacher asks how to set this up, tell them these steps for their AI,
in plain words.

## Workflow

1. **Read the question and the marking scheme.** List every point the
   scheme says to "indicate / illustrate in the diagram" — each must be
   visible in the picture, labelled as the scheme names it.
2. **Decide the economics before any coordinate**: which market and axes,
   which curves, which one shifts and which way, whether demand / supply is
   elastic (flat) or inelastic (steep), which price is fixed, which areas
   are shaded and which must be bigger.
3. **Pick the template** from "Templates" that matches the diagram type
   (and, ideally, a scheme ID listed with it), and start from its code.
4. **Build with `Line` objects and compute every point.** `meet(D, S)` for
   an equilibrium, `D.x(P)` for the quantity demanded at price P,
   `S.shift(dx=10)` for an increase in supply, `S.shift(dy=t)` for a unit
   tax. Never type a coordinate for something that should sit on a curve.
5. **Lay it out** following the style rules, then **check** against the
   checklist at the end of this section.

### Economics that is easy to get wrong

- Increase in demand / supply = shift **right**; decrease = shift **left**.
  Label the old and new curves (D₀ → D₁ or D₁ → D₂, whatever the question
  uses) and put a short arrow between them pointing the way of the shift.
- Price ceiling / fixed price **below** equilibrium → shortage
  (excess demand) = Qd − Qs **on the fixed-price line**. Price floor /
  minimum wage **above** equilibrium → surplus (excess supply). Quantity
  transacted is the SMALLER of Qd and Qs.
- With a fixed price, a shift changes the size of the shortage, not the
  price: brace the old gap (a) and the new gap (b) on the same price line.
- Fixed stock (land, taxi licences, public housing units, tickets,
  seats) → **vertical** supply.
- Total revenue / expenditure diagrams show **only the CHANGE in TR** —
  never shade or label the whole old TR (P₁ × Q₁) or new TR rectangles.
  - P and Q move in opposite directions (a movement along D, or a supply
    shift): shade the gain and the loss. The price-change rectangle is
    |ΔP| × (the quantity that stays), the quantity-change rectangle is
    |ΔQ| × (the price that stays); mark them "+" and "−" (or "gain" /
    "loss"). Elastic demand → draw D **flat**, so the quantity rectangle is
    clearly bigger; inelastic → **steep**, so the price rectangle is
    clearly bigger. Make the stated inequality obvious (at least ~1.5×).
  - P and Q move the same way (a demand shift): shade the single L-shaped
    strip between the old and new P × Q corners and label it "increase in
    TR" / "decrease in TR" (a `key()` legend works well).
- Unit tax: supply shifts **up by t** (vertical distance), consumers pay
  Pc, producers receive Pc − t; tax revenue = t × new quantity.
- Labour market: y-axis wage rate, x-axis number of workers / quantity of
  labour; firms demand labour, workers supply it.
- Negative production externality: MSC above MPC; market output Qm (D ∩
  MPC) > efficient Q* (D ∩ MSC); deadweight loss = triangle between MSC
  and D from Q* to Qm.
- AD-AS: axes "Price level" / "Real output" (物價水平 / 實質產出). AD
  slopes down, SRAS up, LRAS is vertical at Y_f. A demand shock moves AD;
  a cost shock moves SRAS; growth moves LRAS (and usually AD) right.
  Deflationary gap = equilibrium LEFT of LRAS; inflationary gap = RIGHT.
  Self-adjustment moves SRAS only (AD stays) until the equilibrium is on
  LRAS. When AD and SRAS both shift left, only Y is certain: label Y only.
- Quota: supply becomes S up to the quota, then vertical. Subsidy: S shifts
  DOWN by s; buyers pay P₁, sellers get P₁ + s; MC > MB at the new Q.
  Price controls: quantity transacted is the short side (S for a ceiling,
  D for a floor); deadweight loss is the triangle from there to Qe.
- PPC is concave to the origin; a point inside = unemployment /
  inefficiency, outside = unattainable; growth = outward shift.

### Style rules (HKEAA marking-scheme look)

- `new(w, h)` at the size the picture will print (inches; default 3.2 × 2.6).
  Text is 10.5 pt at that size, the same as the papers. Do not shrink text
  to make things fit — make the picture bigger or move things.
- Axes with `axes()`: y title **above** the y-arrow, x title **right of**
  the x-arrow (split a long one with `\n`), `0` at the origin.
- Curves are straight thin lines, named at one end (`D`, `S`, `S₁`, `MSC`).
  Equilibrium points may get a `dot()` and a name (`E`, `E₁`) when the
  scheme mentions them.
- Guides to the axes are dashed (`guide()`), labelled `P₁`, `Q₁` on the axes.
- Gaps are curly braces (`brace()` horizontal, `vbrace()` vertical) with the
  word beyond the tip ("shortage", "excess supply", "a", "b", "t").
  No room at a crowded spot? Put the word nearby with `leader()` (text + thin
  arrow).
- Areas: `hatch()` `////`, `dots()` `....`, or `region()` for triangles —
  a different pattern for each area, labelled with `sign()` (white patch)
  or a small `key()` legend. Greyscale only: never colour.
- Subscripts with mathtext: `r"$P_1$"`, `r"$Q_{d}$"`, `r"$S'$"` → write a
  prime as `"S’"` (plain text) because mathtext lifts `'` too high.

### English and Chinese

- `setup("en")` or `setup("zh")` first; write every word as
  `T("English", "中文")` so one script makes both versions.
- **Never put Chinese inside `$...$`** (mathtext cannot draw it); put the
  Chinese as plain text beside the symbol.
- In Chinese papers the curve letters and symbols stay English
  (D, S, MPC, P₁, Q₂, E); only words are translated.
- Fonts are picked automatically: Times New Roman (fallback: the STIX
  font that ships with matplotlib) + the first Chinese serif found
  (PMingLiU / MingLiU on Windows, Songti TC on macOS, Noto Serif CJK TC on
  Linux), else an uploaded font file, else Noto Serif TC downloaded once.
- Use the HKEAA / EDB wording:

| English | 中文 | English | 中文 |
|---|---|---|---|
| Price | 價格 | Quantity | 數量 |
| Unit price | 單位價格 | Quantity transacted | 交易量 |
| Wage rate | 工資率 | Number of workers | 工人數目 |
| Demand / Supply | 需求 / 供應 | Equilibrium price | 均衡價格 |
| Shortage | 短缺 | Surplus | 盈餘 |
| Excess demand | 超額需求 | Excess supply | 超額供應 |
| Total revenue | 總收入 | Total expenditure | 總開支 |
| Price ceiling | 價格上限 | Price floor | 價格下限 |
| Minimum wage | 最低工資 | Quota | 配額 |
| Unit tax | 從量稅 | Tax revenue | 政府稅收 |
| Consumers' burden | 消費者負擔 | Producers' burden | 生產者負擔 |
| Consumer surplus | 消費者盈餘 | Producer surplus | 生產者盈餘 |
| Deadweight loss | 無謂損失 | Subsidy | 津貼 |
| Marginal private cost | 邊際私人成本 | Marginal social cost | 邊際社會成本 |
| Marginal private benefit | 邊際私人利益 | Marginal social benefit | 邊際社會利益 |
| Production possibilities curve | 生產可能曲線 | Capital goods / Consumer goods | 資本品 / 消費品 |
| Price level | 物價水平 | Real output | 實質產出 |
| Aggregate demand (AD) | 總需求 | Aggregate supply (SRAS / LRAS) | 總供應 |
| Deflationary gap | 通縮缺口 | Inflationary gap | 通脹缺口 |
| Full employment | 充分就業 | Total social surplus | 總社會盈餘 |
| Buyers' burden | 買家負擔 | Sellers' burden | 賣家負擔 |
| Consumer benefit | 消費者得益 | Producer benefit | 生產者得益 |
| Per-unit subsidy | 從量津貼 | Wage rate / Number of workers | 工資率 / 工人數目 |

### Checklist before you hand it over

- [ ] Every "indicate in the diagram" point from the marking scheme is there.
- [ ] Every labelled point is computed, and sits exactly on its curves.
- [ ] Shifts go the right way, the arrow says so, old and new are labelled.
- [ ] TR diagrams shade only the change in TR (gain / loss, or the
      L-shaped increase), not the old or new TR rectangles.
- [ ] Elastic = flat, inelastic = steep; the bigger area really is bigger.
- [ ] No label touches a line or another label; no dashed guide runs
      through text; nothing is cut off. Check the Chinese version
      separately — Chinese labels are wider.
- [ ] Black and white only; same fonts and line weights as the library.
- [ ] Both `en` and `zh` render if the user wants both.

## Templates

Every kind of supply-and-demand and AD-AS diagram found in the HKDSE /
HKCEE marking schemes has a tested template. **Always start from the
closest one:** find it in this index, copy its code from "Template code"
at the end of this guide under the library, then change only what the
question needs (labels, which curve shifts, steepness, words). Every
template makes an English and a Chinese version. The scheme IDs in
brackets are the questions each one mirrors.

<!-- BEGIN TEMPLATE LIST -->
**Demand and supply: shifts**

- `12_demand_decrease`: Demand decreases -> price and quantity fall. *Use for:* demand falls (fewer buyers, lower income, a cheaper substitute ...) and the question asks the effect on price and quantity (CE2000 Q9(b)(i), DSE2012 Q12(c)(i), CE1993 Q4(b)(ii))
- `13_supply_decrease`: Supply decreases -> price rises, quantity falls. *Use for:* supply falls (higher production cost, a unit tax, a higher tariff on imports, bad weather ...) and the question asks the effect on price and quantity; a demand increase or a supply increase is drawn the same way with the arrow reversed (CE1992 Q2(b)(i), CE1994 Q9(b)(i))
- `14_simultaneous_shifts`: Demand and supply both increase, demand by MORE -> price rises. *Use for:* "under what condition does the price rise?" when demand and supply both change; variants: both shift left with the supply shift bigger (CE2002 Q2) also raises the price; equal shifts leave the price unchanged (CE1995 Q11(a), CE2002 Q2, CE2003 Q10(b)(ii), DSE2015 Q11(d))
- `15_vertical_supply_demand_shift`: Fixed stock (vertical supply): supply rises a little, demand rises a lot -> price rises. *Use for:* a fixed stock (taxi licences, land, flats, seats) whose quota is raised slightly while demand grows more, so the price still rises (CE2011 Q11(a), CE1992 Q1(d))

**Labour market**

- `02_price_floor_surplus`: Minimum wage ABOVE equilibrium in a labour market -> unemployment. *Use for:* a minimum wage ABOVE the equilibrium wage causes unemployment (excess supply of labour); for its deadweight loss use template 25 (CE1990 Q1(b), DSE2018 Q10(c))
- `16_labour_imported_workers`: Imported workers: labour supply rises -> wage falls, LOCAL employment falls. *Use for:* importing workers (or more immigrants) adds to the local labour supply; the wage falls and fewer LOCAL workers are employed (read off the local S at W2) (CE1998 Q9(c)(i)(ii))

**Total revenue and elasticity**

- `05_tr_price_change_elastic`: Price falls on ELASTIC (flat) demand -> total revenue rises. *Use for:* a price fall along one ELASTIC demand curve raises total revenue / expenditure; for a price rise on inelastic demand use 18 (CE1993 Q1(a), CE2003 Q9(a))
- `06_tr_supply_decrease_inelastic`: Supply decreases on INELASTIC (steep) demand -> total revenue rises. *Use for:* a supply shift (cost up, bad harvest; or reversed: subsidy, cost down) with inelastic or elastic demand changes total revenue (CE1994 Q11(b), CE1997 Q11(c), CE2009 Q9(b), DSEPP Q3, DSE2021 Q10(c), CE2000 Q11(b) wage bill)
- `11_tr_demand_increase`: Demand increases -> price and quantity both rise -> total revenue increases (shade the change only). *Use for:* demand increases, so P and Q both rise: shade only the increase in total revenue / expenditure (DSE2017 Q10(c), CE2010 Q1)
- `17_tr_demand_decrease`: Demand decreases -> price and quantity both fall -> total revenue falls (shade the change only). *Use for:* a fall in demand and its effect on sellers' total revenue, or the decrease in consumers' expenditure / sales revenue (CE1997 Q9(b), CE1999 Q9(b), CE2004 Q3)
- `18_tr_price_rise_inelastic`: Price rises on INELASTIC (steep) demand -> total revenue rises. *Use for:* a price rise along an inelastic demand curve raises total revenue / expenditure, e.g. the HK$ depreciates so the import price in HK$ rises and spending on the import rises; for a price fall on elastic demand use template 05 (DSE2013 Q9(a), CE2005 Q9(a), CE1993 Q1(a))
- `19_tr_vertical_supply_increase`: Fixed stock (vertical supply) increases on ELASTIC (flat) demand -> total value rises. *Use for:* more taxi licences (land, flats ...) are issued and demand is elastic, so the price falls but the total value of all licences rises (CE1992 Q1(d)(ii))

**Price fixed away from equilibrium**

- `01_price_ceiling_shortage`: Price set BELOW equilibrium (price ceiling / fixed low price) -> shortage. *Use for:* a price ceiling / fixed price BELOW equilibrium causes a shortage (CE1991 Q4(c)(i))
- `03_demand_increase_fixed_price`: Price fixed BELOW equilibrium; demand increases -> shortage grows. *Use for:* price stays fixed below equilibrium while demand rises (or supply falls), so the shortage grows from a to b (DSE2022 Q10(e), CE2003 Q1(a))
- `04_vertical_supply_shortage`: Perfectly inelastic (vertical) supply, price set BELOW equilibrium -> shortage. *Use for:* a fixed stock (tickets, seats, licences, flats, university places) sold at a price below equilibrium (DSE2020 Q11(b), DSEPP Q12(a)(i), DSE2023 Q11(a))
- `20_fixed_wage_supply_increase`: Wage fixed BELOW equilibrium; labour supply increases -> excess demand for labour shrinks. *Use for:* a wage or price fixed below equilibrium when supply rises; the same layout works for any fixed price when D or S shifts (DSE2021 Q12(c), CE1991 Q4(c)(ii))
- `21_vertical_supply_price_raised`: Vertical supply; the fixed price is raised but stays below equilibrium -> shortage shrinks. *Use for:* a fixed tuition fee or ticket price raised from P1 to P2 (e.g. $10 to $20) with a fixed number of places or seats; also the variant where vertical S shifts right at a fixed price (DSEPP Q12(a)(ii), CE2007 Q8(a), CE2005 Q9(b)(i))
- `22_fixed_price_surplus_revenue_fall`: Price fixed ABOVE equilibrium; demand falls -> quantity sold and sales revenue fall. *Use for:* a price kept above equilibrium when demand falls: the quantity sold is Qd, so sales revenue falls by P x (Q1 - Q2); reverse the shift for a rise (CE2004 Q10(a), CE2002 Q11(b))
- `23_fixed_price_rent_increase`: Vertical supply; the controlled rent is raised but stays below equilibrium -> total rental payment rises. *Use for:* a rent (or other controlled price) raised from P0 to P1 with a fixed number of units; also capital raised by a share issue at a fixed price, P̄ x Q̄ (hatch the whole rectangle under P̄ up to Q̄ there) (DSE2025 Q11(b)(i), CE2001 Q10(c)(i))

**Price controls and efficiency**

- `24_price_ceiling_deadweight_loss`: Price ceiling BELOW equilibrium -> shortage and deadweight loss. *Use for:* a price ceiling or controlled price below equilibrium when the question asks about efficiency / deadweight loss (DSEPP Q4(b)(ii), DSE2016 Q11(b), DSE2014)
- `25_price_floor_deadweight_loss`: Price (fare / price floor) set ABOVE equilibrium -> excess supply and deadweight loss. *Use for:* a fixed fare or price floor above equilibrium when the question asks about deadweight loss; a minimum wage with DWL (DSE2018 Q10(c): relabel the axes Wage rate / Quantity of labour); a raised price floor (DSE2014 Q3) (DSE2019 Q11(b), DSE2014 Q3, DSE2018 Q10(c))
- `26_price_ceiling_consumer_surplus_change`: Price ceiling BELOW equilibrium -> change in consumer surplus (gain "+" and loss "−"). *Use for:* how a price ceiling changes consumer surplus: buyers who still get the good pay less (+), the units no longer sold are lost (−) (DSEPP Q4(b)(i))
- `27_price_ceiling_lowered_dwl_increase`: A price ceiling is lowered further below equilibrium -> deadweight loss increases. *Use for:* a price ceiling (or controlled price) lowered from Pc1 to Pc2, both below equilibrium, when the question asks for the change in deadweight loss (DSE2012 Q5(c))

**Tax, subsidy and quota**

- `07_unit_tax_incidence`: Per-unit tax: incidence and tax revenue. *Use for:* per-unit tax: who pays it and the tax revenue; for burden labels and the deadweight-loss triangle use 31 (CE1993 Q4(c), DSE2016 Q10(c))
- `08_surplus_deadweight_quota`: A quota (Qq) set BELOW the equilibrium quantity (Qe): consumer surplus, producer surplus and deadweight loss. *Use for:* a quota below the equilibrium quantity: consumer surplus, producer surplus and deadweight loss (CE1997 Q10(b), CE1998 Q2)
- `28_unit_subsidy`: Per-unit subsidy: S shifts down, buyers pay less, sellers receive more, MC > MB. *Use for:* subsidy incidence; the less elastic side benefits more (draw D or S steeper to match) (DSE2017 Q11(b))
- `29_quota_increase`: A quota is raised -> price falls, quantity rises, deadweight loss shrinks. *Use for:* relaxing (raising) an effective quota and its effect on efficiency (DSE2015 Q3)
- `30_quota_demand_increase`: Demand rises under a quota -> quantity stays at the quota, deadweight loss grows. *Use for:* demand increases while a quota is in force; also an effective quota (P rises, Q falls to the quota), drawn with the same kinked S (DSE2024 Q3, CE1997 Q10(b))
- `31_unit_tax_burden_dwl`: Unit tax on a good with inelastic (steep) demand: buyers bear more, deadweight loss "a". *Use for:* who bears more of a unit tax (the less elastic side) and the deadweight loss; for tax-revenue shading see template 07 (DSE2014 Q9(b), DSE2016 Q10(c))

**Consumer and producer surplus**

- `32_consumer_producer_surplus`: Consumer surplus and producer surplus at the market equilibrium. *Use for:* show (or name) consumer surplus and producer surplus in a market (DSESP Q9(a))
- `33_mc_rise_social_surplus`: Marginal cost rises -> supply shifts up -> total social surplus falls by area abE1E0. *Use for:* a rise in production cost (MC) and the change in total social surplus (DSE2023 Q5(a))

**AD-AS**

- `34_ad_increase`: Aggregate demand increases -> price level and real output both rise. *Use for:* a cash handout, more investment, more tourists, expansionary fiscal or monetary policy; for a fall in AD, swap AD0/AD1 and reverse the arrows (DSE2013 Q12(c), DSE2014 Q12(c), DSE2016 Q12(b), DSE2024 Q12(a), DSE2025 Q10(c), DSEPP Q13(b))
- `35_sras_decrease`: Short-run aggregate supply decreases -> price level rises, real output falls. *Use for:* production costs rise (wages, rents, oil or raw-material prices), a natural disaster or strike cuts production; for an SRAS increase, reverse the arrows (supply-shock MCQs, DSE2017 Q12)
- `36_ad_sras_both_decrease`: AD and SRAS both decrease -> real output falls; the price level is indeterminate. *Use for:* one event that raises costs AND cuts spending (Brexit visa costs + less investment, a disaster that shuts factories + pessimism); only Y is certain (DSE2017 Q12(b), DSE2021 Q11(b))
- `37_lras_ad_increase`: Long run: AD increases on a vertical LRAS -> price level rises, real output stays at Yf. *Use for:* the LONG-RUN effect of a demand-side change (cash handout, more spending) when production capacity is unchanged (DSE2012 Q10(c))
- `38_economic_growth`: Economic growth: LRAS and AD both increase -> real output rises; P rises if AD grows more. *Use for:* better infrastructure, more labour or capital, R&D, new tourist attractions that raise both spending and production capacity (DSE2018 Q9, DSE2020 Q9(b))
- `39_deflationary_gap`: Deflationary gap narrows: AD increases -> real output rises towards Yf. *Use for:* showing a deflationary (output) gap and how a rise in AD (tax cut, more tourists, expansionary policy) narrows it; add the vertical LRAS yourself (DSE2019 Q10(b), DSE2021 Q11(a), DSE2023 Q7(a), DSE2023 Q7(b))
- `40_inflationary_gap`: Inflationary gap closed by a fall in AD -> real output falls back to Yf. *Use for:* output above full employment (Y0 > Yf) and a fall in AD (fewer tourists, contractionary fiscal or monetary policy) that brings it back to Yf (DSE2015 Q12(b))
- `41_self_adjust_deflationary`: Deflationary gap closed by market forces: SRAS increases -> price level falls, output rises to Yf. *Use for:* "how do market forces restore full-employment output" when Y < Yf: excess supply of labour -> wages and costs fall -> SRAS rises (DSEPP Q13(c), DSE2024 Q7(b))
- `42_self_adjust_inflationary`: Inflationary gap closed by market forces: SRAS decreases -> price level rises, output falls to Yf. *Use for:* "how do market forces restore full-employment output" when Y > Yf: excess demand for labour -> wages and costs rise -> SRAS falls (DSE2020 Q6)
- `43_supply_shock_recovery`: Temporary supply shock: SRAS falls (1), then recovers (2) -> P and Y return to P0 and Yf. *Use for:* raw-material prices rise for a while, then the economy adjusts back in the long run (excess labour supply -> wages fall -> SRAS rises again) (DSE2013 Q4(b))

**Other**

- `09_externality_overproduction`: Negative externality in production: overproduction and deadweight loss. *Use for:* negative externality: overproduction and deadweight loss (MSC above MPC)
- `10_ppc`: Production possibilities curve (PPC) and economic growth. *Use for:* production possibilities curve: efficiency, unemployment and growth
<!-- END TEMPLATE LIST -->

### Replacing a picture in Word

To drop a redraw into an existing Word document without moving the layout,
draw at the picture's frame size and save with the original's aspect ratio:
`save(fig, "new.png", aspect=orig_width / orig_height)` — the PNG is padded
with white to exactly that shape.

## The library

Paste this whole block at the top of every script (or save it as
`dsegraph.py` and `from dsegraph import *`). Needs `matplotlib >= 3.6` and
`pillow`.

<!-- BEGIN dsegraph.py -->
```python
"""dsegraph — HKDSE / HKCEE Economics diagrams in the HKEAA marking-scheme style.

Black on white, Times-style serif (Chinese: Ming/Song serif), thin lines,
arrow-headed axes, dashed guide lines, "////" hatching and "...." dotted
fills, curly braces for shortages and surpluses.  English and Chinese.

Only needs matplotlib (>= 3.6).  Every diagram is drawn on a 0..100 x 0..100
canvas; the economic axes go wherever you put them with `axes()`.

    from dsegraph import *
    setup("en")                                   # or setup("zh")
    fig, ax = new(3.2, 2.6)                       # printed size, inches
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))
    D = Line((20, 85), (80, 25)); S = Line((20, 25), (80, 85))
    draw(ax, D, 20, 80, "D"); draw(ax, S, 20, 80, "S")
    E = meet(D, S); dot(ax, *E); guide(ax, E, O, r"$P_e$", r"$Q_e$")
    save(fig, "market.png")
"""
from __future__ import annotations

import glob
import io
import os
import warnings

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path

__all__ = ["setup", "T", "new", "axes", "Line", "meet", "draw", "line",
           "dashed", "guide", "label", "arrow", "hatch", "dots", "region",
           "brace", "vbrace", "dot", "sign", "key", "leader", "curve", "save",
           "SIZE", "LW"]

SIZE = 10.5          # pt at printed size — matches the exam papers
LW = 0.8             # pt, curves and axes
GUIDE_LW = 0.7       # pt, dashed guides and area borders
LANG = "en"
_READY = False

LATIN = ["Times New Roman", "Times", "Liberation Serif", "Nimbus Roman",
         "TeX Gyre Termes", "STIXGeneral"]            # STIX ships with matplotlib
CJK = ["PMingLiU", "MingLiU", "新細明體", "Songti TC", "LiSong Pro",
       "Noto Serif CJK TC", "Noto Serif TC", "Source Han Serif TC",
       "AR PL UMing TW", "AR PL UMing HK",
       "Noto Serif CJK SC", "Songti SC", "SimSun",           # simplified-only fallbacks
       "Microsoft JhengHei", "PingFang TC", "Heiti TC", "Noto Sans CJK TC"]


# Free Chinese serif (SIL Open Font Licence), fetched once when no Chinese
# font is installed — e.g. inside ChatGPT's or Claude's code sandbox.
# Grok's sandbox has no internet: there it relies on an installed font.
CJK_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
           "notoseriftc/NotoSerifTC%5Bwght%5D.ttf")
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "dsegraph")
# cwd, then where chat assistants put uploaded files, then the download cache
FONT_DIRS = [".", "/mnt/data", "/mnt/user-data/uploads", "/mnt/user-data", "/home/user",
             "/workspace", "/tmp", os.path.expanduser("~"), CACHE]


def _add_font(path):
    """Register a font file; return its family name (None if unusable)."""
    try:
        font_manager.fontManager.addfont(path)
        return font_manager.FontProperties(fname=path).get_name()
    except Exception:
        return None


def _has_chinese(path):
    """True if the font file can draw Chinese (checks the glyph for 數)."""
    try:
        from matplotlib.ft2font import FT2Font
        return FT2Font(path).get_char_index(ord("數")) > 0
    except Exception:
        return False


def _cjk_from_files():
    for d in FONT_DIRS:
        for f in sorted(glob.glob(os.path.join(d, "*.[tToO][tT][fFcC]"))):
            if _has_chinese(f):
                name = _add_font(f)
                if name:
                    return name
    return None


def _cjk_installed_any():
    """Any installed font that can draw Chinese, even one not in CJK —
    serif first.  For unknown sandboxes (e.g. Grok's) with odd font names."""
    fonts = sorted(font_manager.fontManager.ttflist,
                   key=lambda f: not any(k in f.name for k in ("Serif", "Ming", "Song", "宋", "明")))
    for f in fonts:
        if _has_chinese(f.fname):
            return f.name
    return None


def _cjk_download():
    path = os.path.join(CACHE, "NotoSerifTC.ttf")
    if not os.path.exists(path):
        try:
            import urllib.request
            os.makedirs(CACHE, exist_ok=True)
            print("dsegraph: downloading a Chinese font (Noto Serif TC, ~17 MB) - once only ...")
            with urllib.request.urlopen(CJK_URL, timeout=20) as r, open(path + ".part", "wb") as f:
                f.write(r.read())                  # timeout: offline sandboxes fail fast
            os.replace(path + ".part", path)
        except Exception:
            return None
    return _add_font(path)


def _have(names):
    found = {f.name for f in font_manager.fontManager.ttflist}
    return [n for n in names if n in found]


def setup(lang: str = "en", size: float = SIZE, font: str | None = None):
    """Pick fonts for English ("en") or Traditional Chinese ("zh").

    Chinese text uses a Ming/Song serif like the HKEAA Chinese papers; the
    letters and numbers in the same label stay in the Times-style serif.
    Chinese font, in order: `font=` (path to a .ttf/.otf file) -> an
    installed one (PMingLiU, Songti TC, Noto Serif CJK TC ...) -> a font file
    uploaded next to the script / into the chat -> any installed font that
    has Chinese -> Noto Serif TC, downloaded once.  Works in Colab, ChatGPT
    and Claude sandboxes without setup; Grok's (offline) needs an installed
    or uploaded font."""
    global LANG, SIZE, _READY
    LANG, SIZE, _READY = lang, size, True
    latin = (_have(LATIN) or ["STIXGeneral"])[0]
    family = [latin]
    if lang == "zh":
        cjk = (_add_font(font) if font else None) or (_have(CJK) or [None])[0] \
            or _cjk_from_files() or _cjk_installed_any() or _cjk_download()
        if cjk:
            family.append(cjk)
        else:
            print("dsegraph: NO CHINESE FONT - Chinese labels will show as boxes. "
                  "Show the English picture and give the Chinese version as a Colab script "
                  "(see 'Chinese' in the guide).")
    plt.rcParams.update({
        "font.family": family,                 # per-glyph fallback: Latin first, then CJK
        "font.size": size,
        "axes.unicode_minus": False,
        "hatch.linewidth": 0.6, "hatch.color": "black",
        "svg.fonttype": "none",
    })
    if latin == "STIXGeneral":
        plt.rcParams["mathtext.fontset"] = "stix"
    else:
        plt.rcParams.update({"mathtext.fontset": "custom", "mathtext.rm": latin,
                             "mathtext.it": f"{latin}:italic", "mathtext.bf": f"{latin}:bold"})
    plt.rcParams["mathtext.default"] = "rm"    # upright P₁, Q₂ like the papers


def T(en: str, zh: str) -> str:
    """The label for the current language: T("Quantity", "數量")."""
    return zh if LANG == "zh" else en


# --------------------------------------------------------------------------
# canvas
# --------------------------------------------------------------------------

def new(w_in: float = 3.2, h_in: float = 2.6):
    """A figure at its printed size (inches) with an invisible 0..100 canvas."""
    if not _READY:
        setup(LANG)
    fig = plt.figure(figsize=(w_in, h_in), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    return fig, ax


def arrow(ax, p, q, lw=LW, head=1.0):
    """Arrow from p to q: shift arrows, "price rises" arrows, axis heads."""
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={0.45*head},head_width={0.18*head}",
                                 mutation_scale=10, lw=lw, color="black",
                                 shrinkA=0, shrinkB=0, zorder=4))


def axes(ax, origin, x_end, y_end, xlabel="Quantity", ylabel="Price", zero="0"):
    """Arrow-headed axes.  The y title sits ABOVE the y-arrow, the x title to
    the RIGHT of the x-arrow, "0" below-left of the origin (exam layout).
    A long x title can be split with "\\n"."""
    arrow(ax, origin, x_end); arrow(ax, origin, y_end)
    if xlabel:
        ax.text(x_end[0] + 1.5, x_end[1], xlabel, ha="left", va="center", fontsize=SIZE)
    if ylabel:
        ax.text(y_end[0], y_end[1] + 2, ylabel, ha="center", va="bottom", fontsize=SIZE)
    if zero:
        ax.text(origin[0] - 1.5, origin[1] - 1.5, zero, ha="right", va="top", fontsize=SIZE)


# --------------------------------------------------------------------------
# exact geometry — compute every intersection, never eyeball it
# --------------------------------------------------------------------------

class Line:
    """A straight curve through p with slope m:  Line(p, q)  or  Line(p, m=-1.2).
    Vertical lines: Line.vertical(x)."""

    def __init__(self, p, q=None, m=None, x=None):
        self.vx = x
        if x is not None:
            return
        if q is not None:
            m = (q[1] - p[1]) / (q[0] - p[0])
        self.m, self.c = m, p[1] - m * p[0]

    @classmethod
    def vertical(cls, x):
        return cls(None, x=x)

    def y(self, x):
        if self.vx is not None:
            raise ValueError("vertical line has no y(x)")
        return self.m * x + self.c

    def x(self, y):
        if self.vx is not None:
            return self.vx
        return (y - self.c) / self.m

    def shift(self, dx=0.0, dy=0.0):
        """Parallel shift: dx>0 right (increase in D or S), dy>0 up (e.g. a unit tax)."""
        if self.vx is not None:
            return Line.vertical(self.vx + dx)
        return Line((0, self.c + dy - self.m * dx), m=self.m)


def meet(a: Line, b: Line):
    """Intersection point of two Lines."""
    if a.vx is not None:
        return (a.vx, b.y(a.vx))
    if b.vx is not None:
        return (b.vx, a.y(b.vx))
    x = (b.c - a.c) / (a.m - b.m)
    return (x, a.y(x))


def draw(ax, L: Line, x0=None, x1=None, name="", end="right", lw=LW, ls="-",
         y0=None, y1=None, dx=1.2, dy=0.0):
    """Draw Line L from x0 to x1 (vertical: from y0 to y1) and write its name
    just beyond one end ("right"/"left"/"top"/"bottom")."""
    if L.vx is not None:
        p, q = (L.vx, y0), (L.vx, y1)
    else:
        p, q = (x0, L.y(x0)), (x1, L.y(x1))
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=ls,
            solid_capstyle="butt", zorder=3)
    if name:
        if end == "top":
            hi = max(p, q, key=lambda t: t[1]); label(ax, hi[0] + dx * 0, hi[1] + 1.5 + dy, name, va="bottom")
        elif end == "bottom":
            lo = min(p, q, key=lambda t: t[1]); label(ax, lo[0], lo[1] - 1.5 + dy, name, va="top")
        elif end == "left":
            label(ax, p[0] - dx, p[1] + dy, name, ha="right")
        else:
            label(ax, q[0] + dx, q[1] + dy, name, ha="left")


def line(ax, p, q, lw=LW, ls="-"):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=ls,
            solid_capstyle="butt", zorder=3)


def curve(ax, xs, ys, lw=LW, ls="-"):
    """Any smooth curve (PPC, cost curves): pass the sampled points."""
    ax.plot(xs, ys, color="black", lw=lw, ls=ls, zorder=3)


def dashed(ax, p, q, lw=GUIDE_LW):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=lw, ls=(0, (4, 3)), zorder=2)


def guide(ax, pt, origin, ylab="", xlab="", to_y=True, to_x=True):
    """Dashed lines from a point to both axes, with its price / quantity labels."""
    x, y = pt
    if to_y:
        dashed(ax, (origin[0], y), (x, y))
        if ylab:
            label(ax, origin[0] - 1.5, y, ylab, ha="right")
    if to_x:
        dashed(ax, (x, origin[1]), (x, y))
        if xlab:
            label(ax, x, origin[1] - 1.8, xlab, va="top")


def label(ax, x, y, text, ha="center", va="center", size=None, **kw):
    """Text.  Subscripts with mathtext: r"$P_1$", r"$Q_{D0}$".  NEVER put
    Chinese inside $...$ — write it as plain text next to it."""
    ax.text(x, y, text, ha=ha, va=va, fontsize=size or SIZE, zorder=6, **kw)


def dot(ax, x, y, size=2.6):
    ax.plot([x], [y], "o", ms=size, color="black", zorder=7)


# --------------------------------------------------------------------------
# areas
# --------------------------------------------------------------------------

def hatch(ax, x0, y0, x1, y1, pattern="////", border=True):
    """Hatched rectangle (revenue gain/loss, tax revenue ...)."""
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, hatch=pattern,
                           lw=GUIDE_LW if border else 0, ec="black", zorder=1))


def dots(ax, x0, y0, x1, y1, border=True):
    hatch(ax, x0, y0, x1, y1, "....", border)


def region(ax, pts, pattern="////", border=False):
    """Any polygon (consumer / producer surplus, deadweight-loss triangle)."""
    ax.add_patch(Polygon(pts, closed=True, fill=False, hatch=pattern,
                         lw=GUIDE_LW if border else 0, ec="black", zorder=1))


def sign(ax, x, y, text, size=None):
    """A label on a small white patch so it reads over hatching: "+", "−", "A"."""
    ax.text(x, y, text, ha="center", va="center", fontsize=size or SIZE, zorder=8,
            bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))


def key(ax, x, y, text, pattern="////", w=8, h=4):
    """A small legend: a hatched swatch followed by its meaning."""
    hatch(ax, x, y - h / 2, x + w, y + h / 2, pattern)
    label(ax, x + w + 1.5, y, text, ha="left")


def leader(ax, text_xy, target_xy, text, ha="center", va="center"):
    """A label away from a crowded spot with a thin arrow to what it names
    ("deadweight loss" -> its triangle, "smaller shortage" -> a brace).
    The arrow starts at the edge of the text."""
    ax.annotate(text, xy=target_xy, xytext=text_xy, ha=ha, va=va, fontsize=SIZE, zorder=6,
                arrowprops=dict(arrowstyle="-|>,head_length=0.36,head_width=0.14",
                                mutation_scale=10, lw=GUIDE_LW, color="black",
                                shrinkA=2, shrinkB=0))


# --------------------------------------------------------------------------
# braces
# --------------------------------------------------------------------------

def _brace_path(a, b, k, depth, horizontal):
    s = 1 if depth > 0 else -1
    d = abs(depth)
    q = min(3.0, abs(b - a) / 4)
    m, h, t = (a + b) / 2, k + s * d / 2, k + s * d
    P = [(a, k), (a, h), (a + q, h), (m - q, h), (m, h), (m, t),
         (m, t), (m, h), (m + q, h), (b - q, h), (b, h), (b, k)]
    if not horizontal:
        P = [(y, x) for x, y in P]
    C = Path.CURVE3
    return Path(P, [Path.MOVETO, C, C, Path.LINETO, C, C, Path.MOVETO, C, C, Path.LINETO, C, C])


def brace(ax, x0, x1, y, text="", side="below", depth=2.5, gap=1.0):
    """Horizontal curly brace over [x0, x1] at height y, tip pointing to
    `side` ("below" / "above"), text beyond the tip (shortage, surplus ...)."""
    d = -depth if side == "below" else depth
    ax.add_patch(PathPatch(_brace_path(x0, x1, y, d, True), fill=False, lw=GUIDE_LW, ec="black", zorder=4))
    if text:
        label(ax, (x0 + x1) / 2, y + d + (-gap if d < 0 else gap), text,
              va="top" if d < 0 else "bottom")


def vbrace(ax, y0, y1, x, text="", side="left", depth=2.5, gap=1.0):
    """Vertical curly brace over [y0, y1] at x (a tax per unit, a price gap)."""
    d = -depth if side == "left" else depth
    ax.add_patch(PathPatch(_brace_path(y0, y1, x, d, False), fill=False, lw=GUIDE_LW, ec="black", zorder=4))
    if text:
        label(ax, x + d + (-gap if d < 0 else gap), (y0 + y1) / 2, text,
              ha="right" if d < 0 else "left")


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def _declutter(fig, ax, step=2.0, max_pts=14.0):
    """Move any label that touches a line, arrow, brace, dot or another label
    to the nearest clear spot (at most `max_pts` away).  The assistant that
    wrote the script usually cannot see the picture, so the library checks
    for it.  Returns the labels that could not be freed."""
    import math
    from matplotlib.text import Text
    from matplotlib.transforms import Bbox
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    px = fig.dpi / 72.0                                 # pixels per point
    paths, boxes = [], []
    for ln in ax.lines:
        xy = ln.get_xydata()
        if len(xy) == 1:                                # a dot
            x, y = ax.transData.transform(xy[0])
            d = ln.get_markersize() * px / 2 + 1
            boxes.append(Bbox([[x - d, y - d], [x + d, y + d]]))
        else:
            paths.append(ln.get_transform().transform_path(ln.get_path()))
    for p in ax.patches:
        if isinstance(p, (PathPatch, FancyArrowPatch)):
            paths.append(p.get_transform().transform_path(p.get_path()))
    # plain polylines: closed shapes (arrow heads) confuse intersects_bbox
    paths = [Path(poly) for q in paths for poly in q.to_polygons(closed_only=False)
             if len(poly) > 1]

    def clash(bb):
        inner = bb.padded(-2.0 * px)       # text vs text: only a real overlap counts
        return any(q.intersects_bbox(bb, filled=False) for q in paths) or \
            any(inner.overlaps(o) for o in boxes)

    stuck, moved = [], []
    for t in ax.texts:
        ext = lambda: Text.get_window_extent(t, r)     # text only (a leader's arrow excluded)
        bb = ext().padded(0.5 * px)
        if clash(bb):
            home = ax.transData.transform(t.get_position())
            best = None
            rad = step
            while best is None and rad <= max_pts:
                for k in range(16):
                    a = 2 * math.pi * k / 16
                    off = (rad * px * math.cos(a), rad * px * math.sin(a))
                    t.set_position(ax.transData.inverted().transform(home + off))
                    nb = ext().padded(0.5 * px)
                    if not clash(nb):
                        best, bb = off, nb
                        break
                rad += step
            if best is None:
                t.set_position(ax.transData.inverted().transform(home))
                bb = ext().padded(0.5 * px)
                stuck.append(t.get_text())
            else:
                moved.append(t.get_text())
        boxes.append(bb)
    if os.environ.get("DSEGRAPH_DEBUG") and moved:
        print("dsegraph: moved labels", moved)
    return stuck


def _present(path):
    """Show the finished picture where the script runs, so the user sees it
    without opening a file: under a notebook cell (and downloaded, in Colab),
    or in a chat assistant's code tool, which captures plt.show().  Desktop
    windows are skipped so a local script never blocks."""
    try:
        from IPython import get_ipython
        shell = get_ipython()
    except Exception:
        shell = None
    if shell is not None:
        try:
            from IPython.display import SVG, Image, display
            display(Image(path, width=420) if path.lower().endswith(".png") else SVG(path))
        except Exception:
            pass
        try:
            from google.colab import files
            files.download(path)
        except Exception:
            pass
        return
    backend = matplotlib.get_backend().lower()
    if any(g in backend for g in ("macosx", "tk", "qt", "gtk", "wx")) or not path.lower().endswith(".png"):
        return
    img = plt.imread(path)
    h, w = img.shape[:2]
    f = plt.figure(figsize=(w / 150, h / 150), dpi=150)
    a = f.add_axes([0, 0, 1, 1])
    a.imshow(img, cmap="gray", vmin=0, vmax=1)
    a.axis("off")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.show()


def save(fig, path="diagram.png", aspect: float | None = None, tidy: bool = True):
    """PNG (greyscale, 300 dpi) or .svg / .pdf by extension.  The canvas grows
    to fit every label, so nothing is ever clipped.  `aspect` (w/h) pads the
    PNG with white to an exact ratio, e.g. to replace a picture in Word
    without moving the layout.  The picture is also shown: in a chat
    assistant's code tool, under a notebook cell (downloaded, in Colab).  tidy=True first nudges any label that
    touches a line or another label into a clear spot."""
    if tidy and fig.axes:
        stuck = _declutter(fig, fig.axes[0])
        if stuck:
            print(f"dsegraph note ({path}): these labels are crowded — ask the AI to move them: "
                  + ", ".join(repr(s) for s in stuck))
    if not path.lower().endswith(".png"):
        fig.savefig(path, facecolor="white", bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)
        _present(path)
        return path
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    im = Image.open(buf).convert("L")
    if aspect:
        w, h = im.size
        if abs(w / h - aspect) > 0.002:
            W, H = (w, round(w / aspect)) if w / h > aspect else (round(h * aspect), h)
            c = Image.new("L", (W, H), 255)
            c.paste(im, ((W - w) // 2, (H - h) // 2))
            im = c
    im.save(path, optimize=True)
    _present(path)
    return path
```
<!-- END dsegraph.py -->

## Template code

The library goes where each template says
`# (paste the whole dsegraph library from "The library" here)`.

<!-- BEGIN TEMPLATES -->
### 01_price_ceiling_shortage

```python
# Price set BELOW equilibrium (price ceiling / fixed low price) -> shortage.
#
# Topic: Price fixed away from equilibrium
# Use for: a price ceiling / fixed price BELOW equilibrium causes a shortage
#   (CE1991 Q4(c)(i))
#
# Marking-scheme points it shows:
#   - price (P) below the equilibrium price (Pe)
#   - correct position of the shortage / excess demand (Qs to Qd at P)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$P_e$", to_x=False)

    P = 34                                     # the fixed price, below Pe
    qs, qd = S.x(P), D.x(P)
    line(ax, (O[0], P), (84, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    dashed(ax, (qs, O[1]), (qs, P)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, qs, qd, P - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 02_price_floor_surplus

```python
# Minimum wage ABOVE equilibrium in a labour market -> unemployment.
#
# Topic: Labour market
# Use for: a minimum wage ABOVE the equilibrium wage causes unemployment (excess supply
#   of labour); for its deadweight loss use template 25 (CE1990 Q1(b), DSE2018 Q10(c))
#
# Marking-scheme points it shows:
#   - minimum wage (W_min) above the equilibrium wage (W_e)
#   - correct position of the excess supply of labour / unemployment (Qd to Qs at W_min)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Number of workers", "工人數目"), T("Wage rate", "工資率"))

    D = Line((20, 82), (78, 22))
    S = Line((20, 22), (78, 82))
    draw(ax, D, 20, 78, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", dy=1.5)

    E = meet(D, S)
    guide(ax, E, O, r"$W_e$", to_x=False)

    W = 66                                     # minimum wage, above We
    qd, qs = D.x(W), S.x(W)
    line(ax, (O[0], W), (84, W))
    label(ax, O[0] - 1.5, W, r"$W_{min}$", ha="right")
    dashed(ax, (qd, O[1]), (qd, W)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    dashed(ax, (qs, O[1]), (qs, W)); label(ax, qs, O[1] - 1.8, r"$Q_s$", va="top")
    brace(ax, qd, qs, W + 1, T("excess supply", "超額供應"), side="above")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 03_demand_increase_fixed_price

```python
# Price fixed BELOW equilibrium; demand increases -> shortage grows.
#
# Topic: Price fixed away from equilibrium
# Use for: price stays fixed below equilibrium while demand rises (or supply falls), so
#   the shortage grows from a to b (DSE2022 Q10(e), CE2003 Q1(a))
#
# Marking-scheme points it shows:
#   - fixed price (P) below the equilibrium price
#   - rightward shift of demand D0 to D1 (arrow)
#   - shortage at P: a (before) enlarges to b (after)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (94, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D0 = Line((14, 82), (62, 34))
    D1 = D0.shift(dx=14)
    S = Line((20, 22), (74, 76))
    draw(ax, D0, 21, D0.x(24), r"$D_0$", end="top")
    draw(ax, D1, 35, D1.x(24), r"$D_1$", end="top")
    draw(ax, S, 20, 74, "S", dy=1.5)

    P = 34                                     # fixed price, below equilibrium
    qs, q0, q1 = S.x(P), D0.x(P), D1.x(P)
    line(ax, (O[0], P), (90, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    for q, name in ((qs, r"$Q_s$"), (q0, r"$Q_{d0}$"), (q1, r"$Q_{d1}$")):
        dashed(ax, (q, O[1]), (q, P)); label(ax, q, O[1] - 1.8, name, va="top")
    brace(ax, qs, q0, P - 1, "a", side="below")
    brace(ax, qs, q1, P + 1, side="above")
    label(ax, (qs + q0) / 2 + 2, P + 1 + 2.5 + 3, "b")   # left of the tip: D0 crosses the tip

    # shift arrow D0 -> D1 on the upper part of the curves
    y = 62
    arrow(ax, (D0.x(y) + 2, y), (D1.x(y) - 2, y))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 04_vertical_supply_shortage

```python
# Perfectly inelastic (vertical) supply, price set BELOW equilibrium -> shortage.
#
# Topic: Price fixed away from equilibrium
# Use for: a fixed stock (tickets, seats, licences, flats, university places) sold at a
#   price below equilibrium (DSE2020 Q11(b), DSEPP Q12(a)(i), DSE2023 Q11(a))
#
# Marking-scheme points it shows:
#   - vertical supply at fixed quantity Q0
#   - controlled price (P) below the equilibrium price (Pe)
#   - shortage / excess demand from Q0 to Qd at P
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 84), (82, 24))
    S = Line.vertical(46)
    draw(ax, D, 18, 82, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=82, end="top")

    E = meet(S, D)
    dot(ax, *E)
    guide(ax, E, O, r"$P_e$", r"$Q_0$")

    P = 32                                     # controlled price, below Pe
    qd = D.x(P)
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    dashed(ax, (qd, O[1]), (qd, P)); label(ax, qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, S.vx, qd, P - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 05_tr_price_change_elastic

```python
# Price falls on ELASTIC (flat) demand -> total revenue rises.
#
# Topic: Total revenue and elasticity
# Use for: a price fall along one ELASTIC demand curve raises total revenue / expenditure;
#   for a price rise on inelastic demand use 18 (CE1993 Q1(a), CE2003 Q9(a))
#
# Marking-scheme points it shows:
#   - flat (elastic) demand curve D
#   - price falls from P1 to P2, quantity demanded rises from Q1 to Q2
#   - loss of revenue (P2..P1 x 0..Q1) marked "-", gain (Q1..Q2 x 0..P2) marked "+"
#   - gain > loss, so total revenue rises
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((20, 66), (84, 38))
    draw(ax, D, 20, 84, "D", dy=-1.5)

    P1, P2 = 58, 46
    Q1, Q2 = D.x(P1), D.x(P2)
    A, B = (Q1, P1), (Q2, P2)

    dots(ax, Q1, O[1], Q2, P2)                 # gain
    hatch(ax, O[0], P2, Q1, P1)                # loss
    guide(ax, A, O, r"$P_1$", r"$Q_1$")
    guide(ax, B, O, r"$P_2$", r"$Q_2$")
    dot(ax, *A); dot(ax, *B)
    sign(ax, (Q1 + Q2) / 2, P2 / 2 + O[1] / 2, "+", size=SIZE + 2)
    sign(ax, (O[0] + Q1) / 2, (P1 + P2) / 2, "−", size=SIZE + 2)

    arrow(ax, (4, P1), (4, P2))                # price falls
    arrow(ax, (Q1, 3), (Q2, 3))                # quantity rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 06_tr_supply_decrease_inelastic

```python
# Supply decreases on INELASTIC (steep) demand -> total revenue rises.
#
# Topic: Total revenue and elasticity
# Use for: a supply shift (cost up, bad harvest; or reversed: subsidy, cost down) with
#   inelastic or elastic demand changes total revenue (CE1994 Q11(b), CE1997 Q11(c),
#   CE2009 Q9(b), DSEPP Q3, DSE2021 Q10(c), CE2000 Q11(b) wage bill)
#
# Marking-scheme points it shows:
#   - steep (inelastic) demand curve D
#   - supply decreases: S1 shifts left to S2 (shift arrow)
#   - price rises P1 -> P2, quantity falls Q1 -> Q2
#   - gain (P1..P2 x 0..Q2) marked "+", loss (Q2..Q1 x 0..P1) marked "-"
#   - gain > loss, so total revenue rises
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((34, 84), (62, 20))
    S1 = Line((20, 24), (84, 72))
    S2 = S1.shift(dx=-30)
    draw(ax, D, 34, 62, "D", dy=-1.5)
    draw(ax, S1, 20, 84, r"$S_1$", dy=1.0)
    draw(ax, S2, 20, 60, r"$S_2$", end="top", dx=0)

    E1, E2 = meet(D, S1), meet(D, S2)
    (Q1, P1), (Q2, P2) = E1, E2

    dots(ax, O[0], P1, Q2, P2)                 # gain
    hatch(ax, Q2, O[1], Q1, P1)                # loss
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, E2, O, r"$P_2$", r"$Q_2$")
    dot(ax, *E1); dot(ax, *E2)
    sign(ax, O[0] + 0.3 * (Q2 - O[0]), P2 - 5, "+", size=SIZE + 2)
    sign(ax, (Q1 + Q2) / 2, (O[1] + P1) / 2, "−", size=SIZE + 2)

    ym = P2 + 5
    arrow(ax, (S1.x(ym) - 2, ym), (S2.x(ym) + 1, ym))   # supply decreases
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 07_unit_tax_incidence

```python
# Per-unit tax: incidence and tax revenue.
#
# Topic: Tax, subsidy and quota
# Use for: per-unit tax: who pays it and the tax revenue; for burden labels and the
#   deadweight-loss triangle use 31 (CE1993 Q4(c), DSE2016 Q10(c))
#
# Marking-scheme points it shows:
#   - S shifts up (vertically) by the tax t to S+t
#   - consumers pay Pc, producers receive Pp = Pc - t, quantity falls Q0 -> Q1
#   - brace for the tax per unit t
#   - hatched tax revenue (Pp..Pc x 0..Q1), split into consumers' and producers' burden
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (14, 12)
    axes(ax, O, (92, 12), (14, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((22, 84), (84, 26))
    S = Line((22, 26), (84, 72))
    t = 20
    St = S.shift(dy=t)
    draw(ax, D, 22, 72, "D", dy=-1.5)
    draw(ax, S, 22, 84, "S", dy=1.0)

    E0, E1 = meet(D, S), meet(D, St)
    draw(ax, St, E1[0], 74, "S+t", dy=1.5)      # starts at E1 so it stays out of the hatch
    Q0, Pe = E0
    Q1, Pc = E1
    Pp = S.y(Q1)
    assert abs((Pc - Pp) - t) < 1e-9

    hatch(ax, O[0], Pp, Q1, Pc)
    dashed(ax, (O[0], Pe), (Q1, Pe))
    guide(ax, E1, O, r"$P_c$", r"$Q_1$")
    dashed(ax, (O[0], Pp), (Q1, Pp)); label(ax, O[0] - 1.5, Pp, r"$P_p$", ha="right")
    dashed(ax, (O[0], Pe), (Q0, Pe)); label(ax, O[0] - 1.5, Pe, r"$P_e$", ha="right")
    dashed(ax, (Q0, O[1]), (Q0, Pe)); label(ax, Q0, O[1] - 1.8, r"$Q_0$", va="top")
    dot(ax, *E0); dot(ax, *E1); dot(ax, Q1, Pp)

    sign(ax, (O[0] + Q1) / 2, (Pe + Pc) / 2, "A")
    sign(ax, (O[0] + Q1) / 2, (Pp + Pe) / 2, "B")
    vbrace(ax, Pp, Pc, 4, r"$t$", side="left")

    kx, ky = 62, 22
    label(ax, kx, ky + 5, T("A: consumers' burden", "A：消費者負擔"), ha="left")
    label(ax, kx, ky, T("B: producers' burden", "B：生產者負擔"), ha="left")
    label(ax, kx, ky - 5, T("A + B: tax revenue", "A + B：政府稅收"), ha="left")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 08_surplus_deadweight_quota

```python
# A quota (Qq) set BELOW the equilibrium quantity (Qe): consumer surplus,
# producer surplus and deadweight loss.
#
# Topic: Tax, subsidy and quota
# Use for: a quota below the equilibrium quantity: consumer surplus, producer surplus and
#   deadweight loss (CE1997 Q10(b), CE1998 Q2)
#
# Marking-scheme points it shows:
#   - quota line at Qq < Qe; price rises to Pq (on D at Qq)
#   - consumer surplus: above Pq, under D, up to Qq
#   - producer surplus: above S, below Pq, up to Qq
#   - deadweight loss: triangle between D and S from Qq to Qe
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((12, 86), (80, 24))
    S = Line((12, 18), (80, 80))
    draw(ax, D, 12, 80, "D", dy=-1.5)
    draw(ax, S, 12, 72, "S", dy=1.5)

    Qe, Pe = meet(D, S)
    Qq = O[0] + 0.6 * (Qe - O[0])              # quota, below Qe
    Pq, Ps = D.y(Qq), S.y(Qq)
    Q = Line.vertical(Qq)
    draw(ax, Q, name=T("Quota", "配額"), y0=O[1], y1=88, end="top")

    # areas (exact vertices)
    region(ax, [(12, D.y(12)), (Qq, Pq), (12, Pq)], "....", border=True)      # CS
    region(ax, [(12, Pq), (Qq, Pq), (Qq, Ps), (12, S.y(12))], "////", border=True)  # PS
    region(ax, [(Qq, Pq), (Qq, Ps), (Qe, Pe)], "xxxx", border=True)           # DWL
    dot(ax, Qe, Pe)

    dashed(ax, (O[0], Pq), (12, Pq))
    label(ax, O[0] - 1.5, Pq, r"$P_q$", ha="right")
    label(ax, O[0] - 1.5, Ps, r"$P_s$", ha="right")
    dashed(ax, (O[0], Ps), (Qq, Ps))
    guide(ax, (Qe, Pe), O, r"$P_e$", r"$Q_e$")
    label(ax, Qq, O[1] - 1.8, r"$Q_q$", va="top")

    key(ax, 60, 92, T("Consumer surplus", "消費者盈餘"), "....")
    key(ax, 60, 85.5, T("Producer surplus", "生產者盈餘"), "////")
    key(ax, 60, 79, T("Deadweight loss", "無謂損失"), "xxxx")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 09_externality_overproduction

```python
# Negative externality in production: overproduction and deadweight loss.
#
# Topic: Other
# Use for: negative externality: overproduction and deadweight loss (MSC above MPC)
#
# Marking-scheme points it shows:
#   - MSC above MPC (external cost); D = MPB = MSB
#   - market output Qm where D = MPC; efficient output Q* where D = MSC
#   - Qm > Q*  (overproduction)
#   - deadweight loss: triangle between MSC and D from Q* to Qm
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 94), T("Quantity", "數量"), T("Price / cost", "價格／成本"))

    D = Line((12, 86), (80, 24))
    MPC = Line((12, 16), (80, 70))
    MSC = MPC.shift(dy=16)
    draw(ax, D, 12, 80, "D = MPB = MSB", dy=-1.5)
    draw(ax, MPC, 12, 80, "MPC", dy=0)
    draw(ax, MSC, 12, 76, "MSC", dy=0)

    Qm, Pm = meet(D, MPC)
    Qs, Ps = meet(D, MSC)
    dot(ax, Qm, Pm); dot(ax, Qs, Ps)
    region(ax, [(Qs, Ps), (Qm, MSC.y(Qm)), (Qm, Pm)], "////", border=True)

    guide(ax, (Qm, Pm), O, r"$P_m$", r"$Q_m$")
    guide(ax, (Qs, Ps), O, r"$P^*$", r"$Q^*$")
    cx, cy = (Qs + 2 * Qm) / 3, (Ps + MSC.y(Qm) + Pm) / 3     # centroid
    leader(ax, (44, 84), (cx, cy + 1), T("Deadweight\nloss", "無謂損失"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 10_ppc

```python
# Production possibilities curve (PPC) and economic growth.
#
# Topic: Other
# Use for: production possibilities curve: efficiency, unemployment and growth
#
# Marking-scheme points it shows:
#   - PPC concave to the origin (increasing opportunity cost)
#   - point on the curve (B): efficient; inside (A): unemployment / inefficiency;
#     outside (C): unattainable with current resources
#   - outward shift of the PPC (PPC1) = economic growth
# (paste the whole dsegraph library from "The library" here)
import math


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 98), T("Consumer goods", "消費品"), T("Capital goods", "資本品"))

    def pt(s, t):                      # point at angle t on the PPC scaled by s
        return (O[0] + s * 55 * math.cos(t), O[1] + s * 60 * math.sin(t))

    ts = [i * (math.pi / 2) / 80 for i in range(81)]
    for s, ls in ((1.0, "-"), (74 / 55, (0, (4, 3)))):
        pts = [pt(s, t) for t in ts]
        curve(ax, [p[0] for p in pts], [p[1] for p in pts], ls=ls)
    label(ax, 12 + 74, 12 - 1.8, r"PPC$_1$", va="top")
    q = pt(1.0, 0.0)
    label(ax, q[0], q[1] - 1.8, r"PPC$_0$", va="top")

    B, A, C = pt(1.0, math.radians(50)), pt(0.6, math.radians(50)), pt(1.17, math.radians(50))
    for p, n, dx, dy in ((A, "A", 2.5, -2.5), (B, "B", 2.5, 2.2), (C, "C", 2.5, 2.2)):
        dot(ax, *p); label(ax, p[0] + dx, p[1] + dy, n)

    g0, g1 = pt(1.0, math.radians(75)), pt(74 / 55, math.radians(75))
    arrow(ax, (g0[0] + 1, g0[1] + 1), (g1[0] - 0.5, g1[1] + 0.5), head=0.9)
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 11_tr_demand_increase

```python
# Demand increases -> price and quantity both rise -> total revenue increases (shade the change only).
#
# Topic: Total revenue and elasticity
# Use for: demand increases, so P and Q both rise: shade only the increase in total revenue
#   / expenditure (DSE2017 Q10(c), CE2010 Q1)
#
# Marking-scheme points it shows:
#   - rightward shift of the demand curve (D0 -> D1)
#   - higher price and quantity (P0 -> P1, Q0 -> Q1)
#   - increase in total revenue = the L-shaped strip between the old and new
#     P x Q corners (never the whole old or new TR rectangle)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), "Q", "P")

    S = Line((20, 18), (80, 78))
    D0 = Line((16, 80), (62, 20))
    D1 = D0.shift(dx=22)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D0, 16, 62, r"$D_0$", dy=-1.5)
    draw(ax, D1, 38, 82, r"$D_1$", dy=-1.5)
    y = 70
    arrow(ax, (D0.x(y) + 2, y), (D1.x(y) - 2, y))

    q0, p0 = meet(D0, S)
    q1, p1 = meet(D1, S)
    # the change in TR only: new rectangle minus old rectangle
    region(ax, [(O[0], p0), (q0, p0), (q0, O[1]), (q1, O[1]), (q1, p1), (O[0], p1)],
           "////", border=True)
    guide(ax, (q0, p0), O, r"$P_0$", r"$Q_0$")
    guide(ax, (q1, p1), O, r"$P_1$", r"$Q_1$")
    arrow(ax, (O[0] - 9, p0), (O[0] - 9, p1))                 # price rises
    arrow(ax, (q0, O[1] - 8), (q1, O[1] - 8))             # quantity rises
    key(ax, 60, 86, T("Increase in TR", "總收入增加"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 12_demand_decrease

```python
# Demand decreases -> price and quantity fall.
#
# Topic: Demand and supply: shifts
# Use for: demand falls (fewer buyers, lower income, a cheaper substitute ...) and
#   the question asks the effect on price and quantity
#   (CE2000 Q9(b)(i), DSE2012 Q12(c)(i), CE1993 Q4(b)(ii))
#
# Marking-scheme points it shows:
#   - leftward shift of demand D1 -> D2 (arrow), S unchanged
#   - new equilibrium E2: price falls P1 -> P2, quantity falls Q1 -> Q2
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    S = Line((20, 18), (80, 78))
    D1 = Line((40, 82), (84, 24))
    D2 = D1.shift(dx=-26)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D1, 40, 84, r"$D_1$", dy=-1.5)
    draw(ax, D2, 16, 50, r"$D_2$", dy=-1.5)
    y = 70
    arrow(ax, (D1.x(y) - 2, y), (D2.x(y) + 2, y))

    (q1, p1), (q2, p2) = E1, E2 = meet(D1, S), meet(D2, S)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 13_supply_decrease

```python
# Supply decreases -> price rises, quantity falls.
#
# Topic: Demand and supply: shifts
# Use for: supply falls (higher production cost, a unit tax, a higher tariff on
#   imports, bad weather ...) and the question asks the effect on price and quantity;
#   a demand increase or a supply increase is drawn the same way with the arrow reversed
#   (CE1992 Q2(b)(i), CE1994 Q9(b)(i))
#
# Marking-scheme points it shows:
#   - leftward shift of supply S -> S' (arrow), D unchanged
#   - new equilibrium E2: price rises P1 -> P2, quantity falls Q1 -> Q2
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 78), (84, 22))
    S1 = Line((36, 18), (82, 78))
    S2 = S1.shift(dx=-22)
    draw(ax, D, 18, 84, "D", dy=-1.5)
    draw(ax, S1, 36, 82, "S", end="top")
    draw(ax, S2, 18, 60, "S’", end="top")
    y = 72
    arrow(ax, (S1.x(y) - 2, y), (S2.x(y) + 2, y))

    (q1, p1), (q2, p2) = E1, E2 = meet(D, S1), meet(D, S2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 14_simultaneous_shifts

```python
# Demand and supply both increase, demand by MORE -> price rises.
#
# Topic: Demand and supply: shifts
# Use for: "under what condition does the price rise?" when demand and supply both
#   change; variants: both shift left with the supply shift bigger (CE2002 Q2) also
#   raises the price; equal shifts leave the price unchanged
#   (CE1995 Q11(a), CE2002 Q2, CE2003 Q10(b)(ii), DSE2015 Q11(d))
#
# Marking-scheme points it shows:
#   - D shifts right D -> D' and S shifts right S -> S', each with its own arrow
#   - the demand shift is clearly larger than the supply shift
#   - new equilibrium E2: price rises P1 -> P2, quantity rises Q1 -> Q2
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D, S = Line((16, 78), m=-1), Line((18, 20), m=1)
    D2, S2 = D.shift(dx=30), S.shift(dx=12)
    draw(ax, D, 16, 58, "D", dy=-1.5)
    draw(ax, D2, 42, 88, "D’", dy=-1.5)
    draw(ax, S, 18, 78, "S", end="top")
    draw(ax, S2, 30, 88, "S’", end="top")
    arrow(ax, (D.x(72) + 2, 72), (D2.x(72) - 2, 72))     # big demand shift
    arrow(ax, (S.x(28) + 2, 28), (S2.x(28) - 2, 28))     # small supply shift

    (q1, p1), (q2, p2) = E1, E2 = meet(D, S), meet(D2, S2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 4, E[1], f"$E_{n}$", ha="left")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 15_vertical_supply_demand_shift

```python
# Fixed stock (vertical supply): supply rises a little, demand rises a lot -> price rises.
#
# Topic: Demand and supply: shifts
# Use for: a fixed stock (taxi licences, land, flats, seats) whose quota is raised
#   slightly while demand grows more, so the price still rises
#   (CE2011 Q11(a), CE1992 Q1(d))
#
# Marking-scheme points it shows:
#   - vertical supply S1 -> S2 (small shift right) and demand D1 -> D2 (larger shift right)
#   - equilibria E1, E2: price rises P1 -> P2, quantity rises Q1 -> Q2
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    S1, S2 = Line.vertical(44), Line.vertical(54)
    D1 = Line((18, 80), m=-1.15)
    D2 = D1.shift(dx=26)
    draw(ax, S1, name=r"$S_1$", y0=O[1], y1=86, end="top")
    draw(ax, S2, name=r"$S_2$", y0=O[1], y1=86, end="top")
    draw(ax, D1, 18, 62, r"$D_1$", dy=-1.5)
    draw(ax, D2, 40, 84, r"$D_2$", dy=-1.5)
    arrow(ax, (S1.vx + 1.5, 82), (S2.vx - 1.5, 82))           # small supply shift
    arrow(ax, (D1.x(36) + 2, 36), (D2.x(36) - 2, 36))         # big demand shift

    (q1, p1), (q2, p2) = E1, E2 = meet(S1, D1), meet(S2, D2)
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 2.5, E[1] + 1, f"$E_{n}$", ha="left", va="bottom")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price rises
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 16_labour_imported_workers

```python
# Imported workers: labour supply rises -> wage falls, LOCAL employment falls.
#
# Topic: Labour market
# Use for: importing workers (or more immigrants) adds to the local labour supply;
#   the wage falls and fewer LOCAL workers are employed (read off the local S at W2)
#   (CE1998 Q9(c)(i)(ii))
#
# Marking-scheme points it shows:
#   - S (Local) and S' (Local + imported) to its right, labour demand D
#   - wage rate falls W1 -> W2
#   - local employment falls Q1 -> Q2, Q2 read off S (Local) at W2
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Number of\nworkers", "工人數目"), T("Wage rate", "工資率"))

    D = Line((24, 84), m=-1)
    S = Line((16, 20), m=1)
    S2 = S.shift(dx=26)
    draw(ax, D, 24, 80, "D", dy=-1.5)
    draw(ax, S, 16, 74, T("S (Local)", "S（本地）"), dy=1.5)
    draw(ax, S2, 38, 84, T("S’ (Local + imported)", "S’（本地＋輸入）"), dy=1.5)

    q1, w1 = meet(D, S)
    w2 = meet(D, S2)[1]
    q2 = S.x(w2)                                   # local workers at the new wage
    guide(ax, (q1, w1), O, r"$W_1$", to_x=False)
    guide(ax, meet(D, S2), O, r"$W_2$", to_x=False)
    for q, w, n in ((q1, w1, "1"), (q2, w2, "2")):
        line(ax, (q, O[1]), (q, w))
        label(ax, q, O[1] - 1.8, f"$Q_{n}$", va="top")
    arrow(ax, (q1 - 3, O[1] - 4.3), (q2 + 3, O[1] - 4.3))   # Q2 <- Q1
    arrow(ax, (O[0] - 9, w1), (O[0] - 9, w2))               # wage falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 17_tr_demand_decrease

```python
# Demand decreases -> price and quantity both fall -> total revenue falls (shade the change only).
#
# Topic: Total revenue and elasticity
# Use for: a fall in demand and its effect on sellers' total revenue, or the decrease
#   in consumers' expenditure / sales revenue
#   (CE1997 Q9(b), CE1999 Q9(b), CE2004 Q3)
#
# Marking-scheme points it shows:
#   - leftward shift of demand D1 -> D2 (arrow), S unchanged
#   - lower price and quantity (P1 -> P2, Q1 -> Q2)
#   - decrease in total revenue = the L-shaped strip between the old and new
#     P x Q corners (never the whole old or new TR rectangle)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    S = Line((20, 18), (80, 78))
    D1 = Line((38, 80), (84, 20))
    D2 = D1.shift(dx=-22)
    draw(ax, S, 20, 80, "S", dy=1.5)
    draw(ax, D1, 38, 84, r"$D_1$", dy=-1.5)
    draw(ax, D2, 16, 62, r"$D_2$", dy=-1.5)
    y = 70
    arrow(ax, (D1.x(y) - 2, y), (D2.x(y) + 2, y))

    q1, p1 = meet(D1, S)
    q2, p2 = meet(D2, S)
    # the change in TR only: old rectangle minus new rectangle
    region(ax, [(O[0], p2), (q2, p2), (q2, O[1]), (q1, O[1]), (q1, p1), (O[0], p1)],
           "////", border=True)
    guide(ax, (q1, p1), O, r"$P_1$", r"$Q_1$")
    guide(ax, (q2, p2), O, r"$P_2$", r"$Q_2$")
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))      # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))      # quantity falls
    key(ax, 48, 90, T("Decrease in total revenue", "總收入減少"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 18_tr_price_rise_inelastic

```python
# Price rises on INELASTIC (steep) demand -> total revenue rises.
#
# Topic: Total revenue and elasticity
# Use for: a price rise along an inelastic demand curve raises total revenue /
#   expenditure, e.g. the HK$ depreciates so the import price in HK$ rises and
#   spending on the import rises; for a price fall on elastic demand use template 05
#   (DSE2013 Q9(a), CE2005 Q9(a), CE1993 Q1(a))
#
# Marking-scheme points it shows:
#   - steep (inelastic) demand curve D, no supply curve needed
#   - price rises from P1 to P2, quantity demanded falls from Q1 to Q2
#   - gain (P1..P2 x 0..Q2) marked "+", loss (Q2..Q1 x 0..P1) marked "-"
#   - gain > loss, so total revenue rises
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((30, 86), (66, 20))
    draw(ax, D, 30, 66, "D", dy=-1.5)

    P1, P2 = 34, 62
    Q1, Q2 = D.x(P1), D.x(P2)
    A, B = (Q1, P1), (Q2, P2)

    dots(ax, O[0], P1, Q2, P2)                 # gain
    hatch(ax, Q2, O[1], Q1, P1)                # loss
    guide(ax, A, O, r"$P_1$", r"$Q_1$")
    guide(ax, B, O, r"$P_2$", r"$Q_2$")
    dot(ax, *A); dot(ax, *B)
    sign(ax, (O[0] + Q2) / 2, (P1 + P2) / 2, "+", size=SIZE + 2)
    sign(ax, (Q1 + Q2) / 2, (P1 + O[1]) / 2, "−", size=SIZE + 2)

    arrow(ax, (O[0] - 9, P1), (O[0] - 9, P2))  # price rises
    arrow(ax, (Q1, O[1] - 9), (Q2, O[1] - 9))  # quantity falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 19_tr_vertical_supply_increase

```python
# Fixed stock (vertical supply) increases on ELASTIC (flat) demand -> total value rises.
#
# Topic: Total revenue and elasticity
# Use for: more taxi licences (land, flats ...) are issued and demand is elastic, so
#   the price falls but the total value of all licences rises
#   (CE1992 Q1(d)(ii))
#
# Marking-scheme points it shows:
#   - vertical supply S shifts right to S' (arrow), flat (elastic) demand D
#   - equilibria E1, E2: price falls P1 -> P2, quantity rises Q1 -> Q2
#   - gain (Q1..Q2 x 0..P2) marked "+", loss (P2..P1 x 0..Q1) marked "-"
#   - gain > loss, so the total value of licences rises
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.7)
    O = (12, 12)
    axes(ax, O, (86, 12), (12, 92), T("Quantity of\ntaxi licences", "的士牌照\n數量"),
         T("Price of a taxi licence", "的士牌照價格"))

    S1, S2 = Line.vertical(40), Line.vertical(62)
    D = Line((20, 70), m=-0.45)
    draw(ax, S1, name="S", y0=O[1], y1=84, end="top")
    draw(ax, S2, name="S’", y0=O[1], y1=84, end="top")
    draw(ax, D, 20, 76, "D", dy=-1.5)
    arrow(ax, (S1.vx + 2, 78), (S2.vx - 2, 78))

    (q1, p1), (q2, p2) = E1, E2 = meet(S1, D), meet(S2, D)
    hatch(ax, O[0], p2, q1, p1)                # loss
    dots(ax, q1, O[1], q2, p2)                 # gain
    for n, E in (("1", E1), ("2", E2)):
        dot(ax, *E)
        label(ax, E[0] + 2, E[1] + 1.5, f"$E_{n}$", ha="left", va="bottom")
        guide(ax, E, O, f"$P_{n}$", f"$Q_{n}$")
    sign(ax, (O[0] + q1) / 2, (p1 + p2) / 2, "−", size=SIZE + 2)
    sign(ax, (q1 + q2) / 2, (O[1] + p2) / 2, "+", size=SIZE + 2)
    arrow(ax, (O[0] - 9, p1), (O[0] - 9, p2))  # price falls
    arrow(ax, (q1, O[1] - 9), (q2, O[1] - 9))  # quantity rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 20_fixed_wage_supply_increase

```python
# Wage fixed BELOW equilibrium; labour supply increases -> excess demand for labour shrinks.
#
# Topic: Price fixed away from equilibrium
# Use for: a wage or price fixed below equilibrium when supply rises; the same
#   layout works for any fixed price when D or S shifts
#   (DSE2021 Q12(c), CE1991 Q4(c)(ii))
#
# Marking-scheme points it shows:
#   - fixed wage W0 below the equilibrium wage
#   - rightward shift of labour supply S0 -> S1 (arrow)
#   - excess demand at W0 shrinks: ex dd0 (Q0 to Qd) -> ex dd1 (Q1 to Qd)
# (paste the whole dsegraph library from "The library" here)


def sub(ax, x, y, word, n):            # word + subscript; mathtext cannot draw Chinese
    label(ax, x, y, word, ha="right"); label(ax, x, y - 1.6, n, ha="left", size=SIZE * .7)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.5, 2.7)
    O = (12, 12)
    axes(ax, O, (94, 12), (12, 92), T("Number of workers", "工人數目"), T("Wage rate", "工資率"))

    W = 36                                     # fixed wage, below equilibrium
    D = Line((84, W), m=-0.45)
    S0 = Line((20, W), m=1.6)
    S1 = S0.shift(dx=36)
    draw(ax, D, 20, 90, r"$D_0$", dy=-1.5)
    draw(ax, S0, S0.x(20), S0.x(84), r"$S_0$", end="top")
    draw(ax, S1, 46, S1.x(84), r"$S_1$", end="top")
    y = 74
    arrow(ax, (S0.x(y) + 5, y), (S1.x(y) - 5, y))

    q0, q1, qd = S0.x(W), S1.x(W), D.x(W)
    line(ax, (O[0], W), (92, W))
    label(ax, O[0] - 1.5, W, r"$W_0$", ha="right")
    for q, n in ((q0, r"$Q_0$"), (q1, r"$Q_1$"), (qd, r"$Q_d$")):
        line(ax, (q, O[1]), (q, W)); label(ax, q, O[1] - 1.8, n, va="top")
    brace(ax, q0, qd, W + 1, side="above")
    brace(ax, q1, qd, W - 1, side="below")
    sub(ax, (q0 + q1) / 2 + T(7, 10), W + 7, T("ex dd", "超額需求"), "0")
    sub(ax, (q1 + qd) / 2 + T(5, 8.5), W - 7, T("ex dd", "超額需求"), "1")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 21_vertical_supply_price_raised

```python
# Vertical supply; the fixed price is raised but stays below equilibrium -> shortage shrinks.
#
# Topic: Price fixed away from equilibrium
# Use for: a fixed tuition fee or ticket price raised from P1 to P2 (e.g. $10 to
#   $20) with a fixed number of places or seats; also the variant where vertical
#   S shifts right at a fixed price
#   (DSEPP Q12(a)(ii), CE2007 Q8(a), CE2005 Q9(b)(i))
#
# Marking-scheme points it shows:
#   - vertical supply S at Q0; both prices below the equilibrium price
#   - price raised from P1 to P2 (arrow between the labels)
#   - shortage shrinks: Ex. D1 (wide, at P1) -> Ex. D2 (narrow, at P2)
# (paste the whole dsegraph library from "The library" here)


def sub(ax, x, y, word, n):            # word + subscript; mathtext cannot draw Chinese
    label(ax, x, y, word, ha="right"); label(ax, x, y - 1.6, n, ha="left", size=SIZE * .7)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (14, 12)
    axes(ax, O, (90, 12), (14, 90), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((22, 84), (86, 24))
    S = Line.vertical(34)
    draw(ax, D, 22, 86, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=84, end="top")
    label(ax, S.vx, O[1] - 1.8, r"$Q_0$", va="top")

    P1, P2 = 28, 48                            # both below equilibrium
    for P, n in ((P1, "1"), (P2, "2")):
        q = D.x(P)
        line(ax, (O[0], P), (88, P))
        label(ax, O[0] - 1.5, P, f"$P_{n}$", ha="right")
        brace(ax, S.vx, q, P - 1, side="below")
        sub(ax, (S.vx + q) / 2 + T(5, 8.5), P - 7, T("Ex. D", "超額需求"), n)
    arrow(ax, (5, P1 + 3), (5, P2 - 3))        # price raised
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 22_fixed_price_surplus_revenue_fall

```python
# Price fixed ABOVE equilibrium; demand falls -> quantity sold and sales revenue fall.
#
# Topic: Price fixed away from equilibrium
# Use for: a price kept above equilibrium when demand falls: the quantity sold is
#   Qd, so sales revenue falls by P x (Q1 - Q2); reverse the shift for a rise
#   (CE2004 Q10(a), CE2002 Q11(b))
#
# Marking-scheme points it shows:
#   - fixed price P above equilibrium; leftward shift D1 -> D2 (arrow)
#   - excess supply at P after the change (Q2 to Qs)
#   - quantity sold (= Qd) falls from Q1 to Q2
#   - fall in sales revenue = P x (Q1 - Q2), hatched with a key
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    P = 58                                     # fixed price, above equilibrium
    S = Line((20, 22), (74, P))
    D1 = Line((70, P), m=-1.6)
    D2 = D1.shift(dx=-30)
    draw(ax, S, 20, 82, "S", dy=1.5)
    draw(ax, D1, D1.x(86), 86, r"$D_1$", end="left")
    draw(ax, D2, D2.x(86), 60, r"$D_2$", end="left")
    arrow(ax, (D1.x(86) - 8, 86), (D2.x(86) + 2, 86))

    q1, q2, qs = D1.x(P), D2.x(P), S.x(P)
    hatch(ax, q2, O[1], q1, P)                 # fall in sales revenue
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    label(ax, q1, O[1] - 1.8, r"$Q_1$", va="top")
    label(ax, q2, O[1] - 1.8, r"$Q_2$", va="top")
    arrow(ax, (q1, 3), (q2, 3))                # quantity sold falls
    brace(ax, q2, qs, P + 1, side="above")
    label(ax, (q2 + q1) / 2 - 5, P + 7.5, T("excess supply", "超額供應"))   # left of D1
    key(ax, 58, 94, T("Fall in sales revenue", "銷售收入減少"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 23_fixed_price_rent_increase

```python
# Vertical supply; the controlled rent is raised but stays below equilibrium -> total rental payment rises.
#
# Topic: Price fixed away from equilibrium
# Use for: a rent (or other controlled price) raised from P0 to P1 with a fixed
#   number of units; also capital raised by a share issue at a fixed price,
#   P̄ x Q̄ (hatch the whole rectangle under P̄ up to Q̄ there)
#   (DSE2025 Q11(b)(i), CE2001 Q10(c)(i))
#
# Marking-scheme points it shows:
#   - vertical supply S at Q0; rent raised from P0 to P1, both below equilibrium
#   - increase in total rental payment = (P1 - P0) x Q0, hatched with a key
#   - excess demand (shortage) at P1, from Q0 to Qd
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 92), T("Quantity", "數量"), T("Rental", "租金"))

    D = Line((20, 80), (84, 24))
    S = Line.vertical(44)
    draw(ax, D, 20, 84, "D", dy=-1.5)
    draw(ax, S, name="S", y0=O[1], y1=84, end="top")
    label(ax, S.vx, O[1] - 1.8, r"$Q_0$", va="top")

    P0, P1 = 28, 38                            # both below equilibrium
    hatch(ax, O[0], P0, S.vx, P1)              # increase in total rental payment
    dashed(ax, (S.vx, P1), (D.x(P1), P1))
    label(ax, O[0] - 1.5, P0, r"$P_0$", ha="right")
    label(ax, O[0] - 1.5, P1, r"$P_1$", ha="right")
    arrow(ax, (3, P0), (3, P1))                # rent raised
    brace(ax, S.vx, D.x(P1), P1 - 1, T("Excess\ndemand", "超額需求"), side="below")
    key(ax, 58, 80, T("Increase in total\nrental payment", "總租金支出增加"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 24_price_ceiling_deadweight_loss

```python
# Price ceiling BELOW equilibrium -> shortage and deadweight loss.
#
# Topic: Price controls and efficiency
# Use for: a price ceiling or controlled price below equilibrium when the question
#   asks about efficiency / deadweight loss
#   (DSEPP Q4(b)(ii), DSE2016 Q11(b), DSE2014)
#
# Marking-scheme points it shows:
#   - ceiling Pc below the equilibrium price; D = MB, S = MC
#   - quantity transacted Qc read off S (the short side), solid line up to D
#   - deadweight loss DL: triangle between D and S from Qc to Qe
#   - shortage at Pc (Qc to Qd)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 84), (80, 24))
    S = Line((22, 18), (70, 82))
    draw(ax, D, 16, 80, "D = MB", dy=-1.5)
    draw(ax, S, 22, 70, "S = MC", end="top")

    Qe, Pe = meet(D, S)
    Pc = 34                                    # ceiling, below Pe
    Qc, Qd = S.x(Pc), D.x(Pc)
    region(ax, [(Qc, Pc), (Qc, D.y(Qc)), (Qe, Pe)], "////", border=True)
    sign(ax, (2 * Qc + Qe) / 3, (Pc + D.y(Qc) + Pe) / 3, "DL")
    line(ax, (Qc, O[1]), (Qc, D.y(Qc)))
    label(ax, Qc, O[1] - 1.8, r"$Q_c$", va="top")
    line(ax, (O[0], Pc), (86, Pc))
    label(ax, O[0] - 1.5, Pc, r"$P_c$", ha="right")
    dashed(ax, (Qd, O[1]), (Qd, Pc)); label(ax, Qd, O[1] - 1.8, r"$Q_d$", va="top")
    brace(ax, Qc, Qd, Pc - 1, T("shortage", "短缺"), side="below")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 25_price_floor_deadweight_loss

```python
# Price (fare / price floor) set ABOVE equilibrium -> excess supply and deadweight loss.
#
# Topic: Price controls and efficiency
# Use for: a fixed fare or price floor above equilibrium when the question asks
#   about deadweight loss; a minimum wage with DWL (DSE2018 Q10(c): relabel the
#   axes Wage rate / Quantity of labour); a raised price floor (DSE2014 Q3)
#   (DSE2019 Q11(b), DSE2014 Q3, DSE2018 Q10(c))
#
# Marking-scheme points it shows:
#   - price P above the equilibrium price
#   - quantity transacted Q read off D (the short side), solid line from Q up to P
#   - deadweight loss DL: triangle between D and S from Q to Qe
#   - excess supply at P (Q to Qs)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((18, 74), (78, 20))
    S = Line((18, 22), (74, 84))
    draw(ax, D, 18, 78, "D", dy=-1.5)
    draw(ax, S, 18, 74, "S", end="top")

    Qe, Pe = meet(D, S)
    P = 64                                     # set above Pe
    Q, Qs = D.x(P), S.x(P)
    region(ax, [(Q, P), (Q, S.y(Q)), (Qe, Pe)], "xxxx", border=True)
    sign(ax, (2 * Q + Qe) / 3, (P + S.y(Q) + Pe) / 3, "DL")
    line(ax, (Q, O[1]), (Q, P))
    label(ax, Q, O[1] - 1.8, "Q", va="top")
    line(ax, (O[0], P), (86, P))
    label(ax, O[0] - 1.5, P, "P", ha="right")
    brace(ax, Q, Qs, P + 1, T("excess supply", "超額供應"), side="above")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 26_price_ceiling_consumer_surplus_change

```python
# Price ceiling BELOW equilibrium -> change in consumer surplus (gain "+" and loss "−").
#
# Topic: Price controls and efficiency
# Use for: how a price ceiling changes consumer surplus: buyers who still get the
#   good pay less (+), the units no longer sold are lost (−)
#   (DSEPP Q4(b)(i))
#
# Marking-scheme points it shows:
#   - ceiling Pc below the equilibrium price Pe; quantity transacted Qs (on S)
#   - gain "+": rectangle (Pe - Pc) x Qs
#   - loss "−": triangle between D and the Pe line, from Qs to Qe
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 86), (80, 24))
    S = Line((22, 16), (76, 82))
    draw(ax, D, 16, 84, "D", dy=-1.5)
    draw(ax, S, 22, 76, "S", end="top")

    Qe, Pe = meet(D, S)
    Pc = 26                                    # ceiling, below Pe
    Qs = S.x(Pc)
    region(ax, [(O[0], Pc), (Qs, Pc), (Qs, Pe), (O[0], Pe)], "////", border=True)
    region(ax, [(Qs, Pe), (Qs, D.y(Qs)), (Qe, Pe)], "////", border=True)
    sign(ax, (O[0] + Qs) / 2, (Pc + Pe) / 2, "+", size=SIZE + 2)
    sign(ax, (2 * Qs + Qe) / 3, (2 * Pe + D.y(Qs)) / 3, "−", size=SIZE + 2)
    dot(ax, Qe, Pe)
    line(ax, (Qs, O[1]), (Qs, D.y(Qs)))
    label(ax, Qs, O[1] - 1.8, r"$Q_s$", va="top")
    line(ax, (O[0], Pc), (86, Pc))
    label(ax, O[0] - 1.5, Pc, r"$P_c$", ha="right")
    label(ax, O[0] - 1.5, Pe, r"$P_e$", ha="right")
    guide(ax, (Qe, Pe), O, xlab=r"$Q_e$", to_y=False)
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 27_price_ceiling_lowered_dwl_increase

```python
# A price ceiling is lowered further below equilibrium -> deadweight loss increases.
#
# Topic: Price controls and efficiency
# Use for: a price ceiling (or controlled price) lowered from Pc1 to Pc2, both below
#   equilibrium, when the question asks for the change in deadweight loss
#   (DSE2012 Q5(c))
#
# Marking-scheme points it shows:
#   - ceiling lowered Pc1 -> Pc2; quantity transacted falls Q1 -> Q2 along S
#   - original deadweight loss: triangle between D and S from Q1 to Qe (dotted)
#   - increase in deadweight loss: trapezoid between D and S from Q2 to Q1 (hatched)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.7)
    O = (12, 12)
    axes(ax, O, (90, 12), (12, 92), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((14, 86), m=-0.85)
    S = Line((20, 16), m=1.0)
    draw(ax, D, 14, 84, "D", dy=-1.5)
    draw(ax, S, 20, 78, "S", end="top")

    Qe, Pe = meet(D, S)
    P1, P2 = 40, 28                            # both ceilings below Pe
    Q1, Q2 = S.x(P1), S.x(P2)
    region(ax, [(Q1, P1), (Q1, D.y(Q1)), (Qe, Pe)], "....", border=True)
    region(ax, [(Q2, P2), (Q2, D.y(Q2)), (Q1, D.y(Q1)), (Q1, P1)], "////", border=True)
    dot(ax, Qe, Pe)
    guide(ax, (Qe, Pe), O, xlab=r"$Q_e$", to_y=False)
    for P, Q, n in ((P1, Q1, "1"), (P2, Q2, "2")):
        line(ax, (O[0], P), (86, P))
        label(ax, O[0] - 1.5, P, f"$P_{{c{n}}}$", ha="right")
        line(ax, (Q, O[1]), (Q, D.y(Q)))
        label(ax, Q, O[1] - 1.8, f"$Q_{n}$", va="top")
    arrow(ax, (2, P1), (2, P2))                # ceiling lowered
    arrow(ax, (Q1, 3), (Q2, 3))                # Q falls
    key(ax, 52, 92, T("Original deadweight loss", "原有無謂損失"), "....")
    key(ax, 52, 85.5, T("Increase in deadweight loss", "無謂損失增加"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 28_unit_subsidy

```python
# Per-unit subsidy: S shifts down, buyers pay less, sellers receive more, MC > MB.
#
# Topic: Tax, subsidy and quota
# Use for: subsidy incidence; the less elastic side benefits more (draw D or S steeper to match)
#   (DSE2017 Q11(b))
#
# Marking-scheme points it shows:
#   - S0 shifts down by the subsidy s to Ss (arrow); E0 -> E1, Q0 -> Q1
#   - buyers pay P1 < P0; sellers receive P2 = P1 + s (point A on S0)
#   - consumer benefit (P0-P1) x Q1 dotted, producer benefit (P2-P0) x Q1 hatched
#   - at Q1, MC (A) > MB (E1): overproduction
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((16, 88), (80, 18))
    S0 = Line((16, 40), (80, 80))
    Ss = S0.shift(dy=-22)
    draw(ax, D, 16, 80, "D", dy=-1.5)
    draw(ax, S0, 16, 80, r"$S_0$")
    draw(ax, Ss, 24, 80, r"$S_s$")
    arrow(ax, (76, S0.y(76) - 2), (76, Ss.y(76) + 2))

    E0, E1 = meet(D, S0), meet(D, Ss)
    Q1, P1 = E1
    A = (Q1, S0.y(Q1))
    dots(ax, O[0], P1, Q1, E0[1])               # consumer benefit
    hatch(ax, O[0], E0[1], Q1, A[1], "////")    # producer benefit
    guide(ax, E0, O, r"$P_0$", r"$Q_0$")
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, A, O, r"$P_2$", to_x=False)
    for p in (E0, E1, A):
        dot(ax, *p)
    sign(ax, E0[0] - 3.5, E0[1] - 8.5, r"$E_0$")
    label(ax, Q1 - 1, A[1] + 4, "A")
    label(ax, Q1 - 3.5, P1 - 7, r"$E_1$")
    leader(ax, (Q1 + 9, A[1] + 1), (Q1 + 1, A[1]), "MC", ha="left")
    leader(ax, (Q1 + 9, P1 + 1), (Q1 + 1.2, P1), "MB", ha="left")

    key(ax, 34, 93, T("Consumer benefit", "消費者得益"), "....")
    key(ax, 34, 87, T("Producer benefit", "生產者得益"), "////")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 29_quota_increase

```python
# A quota is raised -> price falls, quantity rises, deadweight loss shrinks.
#
# Topic: Tax, subsidy and quota
# Use for: relaxing (raising) an effective quota and its effect on efficiency
#   (DSE2015 Q3)
#
# Marking-scheme points it shows:
#   - S0 (= MC) and D (= MB); the quota moves right from S1 to S2 (arrow)
#   - P falls P1 -> P2 and Q rises Q1 -> Q2 (axis arrows)
#   - W, X on D and Z, Y on S0; area WXYZ = reduction in deadweight loss (hatched, key)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    D = Line((18, 84), (80, 22))
    S0 = Line((20, 18), (80, 78))
    draw(ax, D, 18, 80, "D = MB", dy=-1.5)
    draw(ax, S0, 20, 80, r"$S_0$ = MC", dy=1)

    Q1, Q2 = 28, 40
    W, X = (Q1, D.y(Q1)), (Q2, D.y(Q2))
    Y, Z = (Q2, S0.y(Q2)), (Q1, S0.y(Q1))
    draw(ax, Line.vertical(Q1), y0=O[1], y1=88, name=r"$S_1$", end="top")
    draw(ax, Line.vertical(Q2), y0=O[1], y1=88, name=r"$S_2$", end="top")
    arrow(ax, (Q1 + 2, 85), (Q2 - 2, 85))

    region(ax, [W, X, Y, Z], "////")
    for p in (W, X, Y, Z):
        dot(ax, *p)
    label(ax, Q1 + 3, W[1] + 3.5, "W")
    label(ax, Q2 + 3, X[1] + 3.5, "X")
    label(ax, Q2 + 3, Y[1] - 3.5, "Y")
    label(ax, Q1 - 3, Z[1] + 3.5, "Z")
    guide(ax, W, O, r"$P_1$", to_x=False)
    guide(ax, X, O, r"$P_2$", to_x=False)
    label(ax, Q1, O[1] - 1.8, r"$Q_1$", va="top")
    label(ax, Q2, O[1] - 1.8, r"$Q_2$", va="top")
    arrow(ax, (4, W[1]), (4, X[1]))             # price falls
    arrow(ax, (Q1, 3), (Q2, 3))                 # quantity rises
    key(ax, 50, 91, T("Reduction in deadweight loss", "無謂損失減少"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 30_quota_demand_increase

```python
# Demand rises under a quota -> quantity stays at the quota, deadweight loss grows.
#
# Topic: Tax, subsidy and quota
# Use for: demand increases while a quota is in force; also an effective quota
#   (P rises, Q falls to the quota), drawn with the same kinked S
#   (DSE2024 Q3, CE1997 Q10(b))
#
# Marking-scheme points it shows:
#   - kinked S_quota: S0 (= MC) up to the quota Q0, then vertical
#   - D0 (= MB0) shifts right to D1 (= MB1); quantity stays at Q0
#   - efficient quantity rises from Q1 to Q2 (D meets S0)
#   - hatched: the increase in deadweight loss (key)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    S0 = Line((16, 20), (80, 76))
    D0 = Line((16, 80), (70, 20))
    D1 = D0.shift(dx=16)
    draw(ax, S0, 16, 80, r"$S_0$ = MC", dy=1)
    draw(ax, D0, 16, 66, r"$D_0$ = $MB_0$", end="bottom")
    draw(ax, D1, 26, 80, r"$D_1$ = $MB_1$", dy=-1.5)
    arrow(ax, (D0.x(30) + 2, 30), (D1.x(30) - 2, 30))

    Q0 = 30
    K = (Q0, S0.y(Q0))                          # the kink
    draw(ax, Line.vertical(Q0), y0=K[1], y1=90, name=r"$S_{quota}$", end="top")
    dashed(ax, (Q0, O[1]), K)
    E1, E2 = meet(D0, S0), meet(D1, S0)
    region(ax, [(Q0, D0.y(Q0)), (Q0, D1.y(Q0)), E2, E1], "////")
    guide(ax, E1, O, to_y=False)
    guide(ax, E2, O, to_y=False)
    for q, n in ((Q0, r"$Q_0$"), (E1[0], r"$Q_1$"), (E2[0], r"$Q_2$")):
        label(ax, q, O[1] - 1.8, n, va="top")
    arrow(ax, (E1[0], 3), (E2[0], 3))          # efficient quantity rises
    key(ax, 50, 92, T("Increase in deadweight loss", "無謂損失增加"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 31_unit_tax_burden_dwl

```python
# Unit tax on a good with inelastic (steep) demand: buyers bear more, deadweight loss "a".
#
# Topic: Tax, subsidy and quota
# Use for: who bears more of a unit tax (the less elastic side) and the
#   deadweight loss; for tax-revenue shading see template 07
#   (DSE2014 Q9(b), DSE2016 Q10(c))
#
# Marking-scheme points it shows:
#   - steep D; S0 shifts up by the tax to S1 (arrow "tax")
#   - buyers pay P1 (was P0); sellers receive P2 = P1 - t; Q0 -> Q1
#   - buyers' burden P0..P1 > sellers' burden P2..P0 (braces)
#   - deadweight loss: triangle "a" between D and S0 from Q1 to Q0
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), "Q", "P")

    D = Line((32, 90), (62, 22))
    S0 = Line((12, 18), m=0.7)
    S1 = S0.shift(dy=28)
    draw(ax, D, 32, 62, "D", dy=-1.5)
    draw(ax, S0, 12, 80, r"$S_0$")
    draw(ax, S1, 20, 64, r"$S_1$")
    x = 72
    arrow(ax, (x, S0.y(x) + 4), (x, S0.y(x) + 14))
    label(ax, x + 1.5, S0.y(x) + 10, T("tax", "稅"), ha="left")

    E0, E1 = meet(D, S0), meet(D, S1)
    Q1, P1 = E1
    B = (Q1, S0.y(Q1))
    region(ax, [E1, B, E0], "////", border=True)
    sign(ax, (2 * Q1 + E0[0]) / 3, (P1 + B[1] + E0[1]) / 3, "a")
    guide(ax, E1, O, r"$P_1$", r"$Q_1$")
    guide(ax, E0, O, r"$P_0$", r"$Q_0$")
    guide(ax, B, O, r"$P_2$", to_x=False)
    vbrace(ax, E0[1] + 0.5, P1, 5, T("Buyers' burden", "買家負擔"))
    vbrace(ax, B[1], E0[1] - 0.5, 5, T("Sellers' burden", "賣家負擔"))
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 32_consumer_producer_surplus

```python
# Consumer surplus and producer surplus at the market equilibrium.
#
# Topic: Consumer and producer surplus
# Use for: show (or name) consumer surplus and producer surplus in a market
#   (DSESP Q9(a))
#
# Marking-scheme points it shows:
#   - D and S, a price line from the equilibrium to the price axis
#   - C.S.: the triangle under D and above the price
#   - P.S.: the triangle above S and below the price
#   - a text legend: C.S. = consumer surplus, P.S. = producer surplus
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.6, 2.6)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 92), T("Quantity", "數量"), T("Price ($)", "價格 ($)"))

    D = Line((12, 86), (70, 20))
    S = Line((12, 34), (76, 80))
    draw(ax, D, 12, 70, "D", dy=-1.5)
    draw(ax, S, 12, 76, "S", dy=1.5)

    q, p = meet(D, S)
    line(ax, (O[0], p), (q, p))
    label(ax, O[0] + (q - O[0]) / 3, (D.y(12) + 2 * p) / 3, "C.S.")
    label(ax, O[0] + (q - O[0]) / 3, (S.y(12) + 2 * p) / 3, "P.S.")

    label(ax, 58, 46, T("C.S. = Consumer surplus", "C.S. = 消費者盈餘"), ha="left")
    label(ax, 58, 39, T("P.S. = Producer surplus", "P.S. = 生產者盈餘"), ha="left")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 33_mc_rise_social_surplus

```python
# Marginal cost rises -> supply shifts up -> total social surplus falls by area abE1E0.
#
# Topic: Consumer and producer surplus
# Use for: a rise in production cost (MC) and the change in total social surplus
#   (DSE2023 Q5(a))
#
# Marking-scheme points it shows:
#   - S0 = MC0 shifts up to S1 = MC1 (arrow); D = MB
#   - equilibrium E0 -> E1
#   - a, b: where S0 and S1 meet the price axis
#   - hatched band abE1E0 = decrease in total social surplus
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.4, 2.8)
    O = (12, 12)
    axes(ax, O, (92, 12), (12, 94), T("Quantity", "數量"), T("Price", "價格"))

    D = Line((12, 88), (80, 16))
    S0 = Line((12, 18), m=0.75)
    S1 = S0.shift(dy=18)
    draw(ax, D, 12, 74, "D = MB", dy=-1.5)
    draw(ax, S0, 12, 80, r"$S_0$ = $MC_0$")
    draw(ax, S1, 12, 72, r"$S_1$ = $MC_1$")
    arrow(ax, (68, S0.y(68) + 3), (68, S1.y(68) - 3))

    a, b = (O[0], S0.y(O[0])), (O[0], S1.y(O[0]))
    E0, E1 = meet(D, S0), meet(D, S1)
    region(ax, [a, b, E1, E0], "////")
    dot(ax, *E0); dot(ax, *E1)
    label(ax, E0[0] + 4, E0[1] - 1, r"$E_0$")
    label(ax, E1[0] + 1, E1[1] + 5, r"$E_1$")
    label(ax, O[0] - 1.5, a[1], "a", ha="right")
    label(ax, O[0] - 1.5, b[1], "b", ha="right")
    key(ax, 34, 92, T("Decrease in total social surplus", "總社會盈餘減少"))
    label(ax, 54, 86, T("= area", "= 面積"), ha="right")   # no Chinese inside $...$
    label(ax, 54.6, 86, r"ab$E_1E_0$", ha="left")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 34_ad_increase

```python
# Aggregate demand increases -> price level and real output both rise.
#
# Topic: AD-AS
# Use for: a cash handout, more investment, more tourists, expansionary fiscal or
#   monetary policy; for a fall in AD, swap AD0/AD1 and reverse the arrows
#   (DSE2013 Q12(c), DSE2014 Q12(c), DSE2016 Q12(b), DSE2024 Q12(a), DSE2025 Q10(c), DSEPP Q13(b))
#
# Marking-scheme points it shows:
#   - AD0 shifts right to AD1 (arrow), SRAS unchanged
#   - equilibrium moves E0 -> E1 along the upward-sloping SRAS
#   - price level rises P0 -> P1, real output rises Y0 -> Y1
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((22, 24), (76, 78))
    AD0 = Line((16, 78), (58, 22))
    AD1 = AD0.shift(dx=22)
    draw(ax, S, 22, 76, "SRAS", dy=1.5)
    draw(ax, AD0, 16, 58, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 38, 80, r"$AD_1$", dy=-1.5)
    y = 70
    arrow(ax, (AD0.x(y) + 2, y), (AD1.x(y) - 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, S)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 35_sras_decrease

```python
# Short-run aggregate supply decreases -> price level rises, real output falls.
#
# Topic: AD-AS
# Use for: production costs rise (wages, rents, oil or raw-material prices), a natural
#   disaster or strike cuts production; for an SRAS increase, reverse the arrows
#   (supply-shock MCQs, DSE2017 Q12)
#
# Marking-scheme points it shows:
#   - SRAS0 shifts left to SRAS1 (arrow), AD unchanged
#   - equilibrium moves E0 -> E1 up along AD
#   - price level rises P0 -> P1, real output falls Y0 -> Y1
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((18, 80), (76, 22))
    S0 = Line((34, 22), (82, 70))
    S1 = S0.shift(dx=-22)
    draw(ax, AD, 18, 76, "AD", dy=-1.5)
    draw(ax, S0, 34, 82, r"$SRAS_0$", end="top")
    draw(ax, S1, 16, 64, r"$SRAS_1$", end="top")
    y = 60
    arrow(ax, (S0.x(y) - 2, y), (S1.x(y) + 2, y))

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 36_ad_sras_both_decrease

```python
# AD and SRAS both decrease -> real output falls; the price level is indeterminate.
#
# Topic: AD-AS
# Use for: one event that raises costs AND cuts spending (Brexit visa costs + less
#   investment, a disaster that shuts factories + pessimism); only Y is certain
#   (DSE2017 Q12(b), DSE2021 Q11(b))
#
# Marking-scheme points it shows:
#   - AD0 shifts left to AD1 (arrow)
#   - SRAS0 shifts left to SRAS1 (arrow)
#   - real output falls Y0 -> Y1; the price level is not labelled (may rise or fall)
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD0 = Line((38, 80), (82, 26))
    AD1 = AD0.shift(dx=-20)
    S0 = Line((40, 26), (82, 72))
    S1 = S0.shift(dx=-20)
    draw(ax, AD0, 38, 80, r"$AD_0$", end="top")
    draw(ax, AD1, 18, 54, r"$AD_1$", end="top")
    draw(ax, S0, 40, 82, r"$SRAS_0$", end="top")
    draw(ax, S1, 20, 62, r"$SRAS_1$", end="top")
    for A, B, y in ((AD0, AD1, 72), (S0, S1, 66)):
        arrow(ax, (A.x(y) - 2, y), (B.x(y) + 2, y))

    E0, E1 = meet(AD0, S0), meet(AD1, S1)
    guide(ax, E0, O, xlab=r"$Y_0$", to_y=False)
    guide(ax, E1, O, xlab=r"$Y_1$", to_y=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0], E[1] + 4, n, va="bottom")
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 37_lras_ad_increase

```python
# Long run: AD increases on a vertical LRAS -> price level rises, real output stays at Yf.
#
# Topic: AD-AS
# Use for: the LONG-RUN effect of a demand-side change (cash handout, more spending)
#   when production capacity is unchanged (DSE2012 Q10(c))
#
# Marking-scheme points it shows:
#   - vertical LRAS at full-employment output Yf (no SRAS)
#   - AD1 shifts right to AD2 (arrow)
#   - price level rises P1 -> P2; real output unchanged at Yf
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    L = Line.vertical(50)
    AD1 = Line((18, 70), (70, 18))
    AD2 = AD1.shift(dx=22)
    draw(ax, L, y0=O[1], y1=82, name="LRAS", end="top")
    draw(ax, AD1, 18, 70, r"$AD_1$", dy=-1.5)
    draw(ax, AD2, 32, 82, r"$AD_2$", dy=-1.5)
    y = 32
    arrow(ax, (AD1.x(y) + 2, y), (AD2.x(y) - 2, y))

    E1, E2 = meet(AD1, L), meet(AD2, L)
    guide(ax, E1, O, r"$P_1$", to_x=False)
    guide(ax, E2, O, r"$P_2$", to_x=False)
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    for E, n in ((E1, r"$E_1$"), (E2, r"$E_2$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    arrow(ax, (O[0] - 9, E1[1]), (O[0] - 9, E2[1]))       # price level rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 38_economic_growth

```python
# Economic growth: LRAS and AD both increase -> real output rises; P rises if AD grows more.
#
# Topic: AD-AS
# Use for: better infrastructure, more labour or capital, R&D, new tourist attractions
#   that raise both spending and production capacity (DSE2018 Q9, DSE2020 Q9(b))
#
# Marking-scheme points it shows:
#   - LRAS0 shifts right to LRAS1 (arrow)
#   - AD0 shifts right to AD1 (arrow), by MORE than LRAS
#   - E0 -> E1: real output rises Y0 -> Y1, price level rises P0 -> P1
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    L0 = Line.vertical(46)
    L1 = L0.shift(dx=12)
    AD0 = Line((14, 80), m=-1)
    AD1 = AD0.shift(dx=28)                     # AD grows more than LRAS -> P rises
    draw(ax, L0, y0=O[1], y1=86)
    draw(ax, L1, y0=O[1], y1=86)
    label(ax, L0.vx + 1, 88, r"$LRAS_0$", ha="right", va="bottom")
    label(ax, L1.vx - 1, 88, r"$LRAS_1$", ha="left", va="bottom")
    draw(ax, AD0, 16, 70, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 40, 84, r"$AD_1$", dy=-1.5)
    arrow(ax, (L0.vx + 2, 82), (L1.vx - 2, 82))
    y = 78
    arrow(ax, (AD0.x(y) + 2, y), (AD1.x(y) - 2, y))

    E0, E1 = meet(AD0, L0), meet(AD1, L1)
    for E, p, n, Y in ((E0, r"$P_0$", r"$E_0$", r"$Y_0$"), (E1, r"$P_1$", r"$E_1$", r"$Y_1$")):
        guide(ax, E, O, p, to_x=False)
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
        label(ax, E[0], O[1] - 1.8, Y, va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (E1[0], O[1] - 8))       # real output rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 39_deflationary_gap

```python
# Deflationary gap narrows: AD increases -> real output rises towards Yf.
#
# Topic: AD-AS
# Use for: showing a deflationary (output) gap and how a rise in AD (tax cut, more
#   tourists, expansionary policy) narrows it; add the vertical LRAS yourself
#   (DSE2019 Q10(b), DSE2021 Q11(a), DSE2023 Q7(a), DSE2023 Q7(b))
#
# Marking-scheme points it shows:
#   - vertical LRAS at Yf, right of E0 (Y0 < Yf): gap0 = Y0 to Yf
#   - AD0 shifts right to AD1 (arrow); E0 -> E1, P0 -> P1, Y0 -> Y1
#   - gap1 = Y1 to Yf, narrower than gap0; key: gap = deflationary gap
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((22, 24), m=1)
    L = Line.vertical(70)
    AD0 = Line((36, 38), m=-1.4)
    AD1 = AD0.shift(dx=20)
    draw(ax, S, 22, 78, "SRAS", dy=1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, AD0, 18, 44, r"$AD_0$", end="top")
    draw(ax, AD1, 38, 66, r"$AD_1$", end="top")
    y = 56
    arrow(ax, (AD0.x(y) + 2, y), (AD1.x(y) - 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, S)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1], n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    brace(ax, E1[0], L.vx, O[1] + 1.5, r"$gap_1$", side="above")
    brace(ax, E0[0], L.vx, O[1] - 8, r"$gap_0$", side="below")
    label(ax, 73, 44, T("gap =\ndeflationary gap", "gap =\n通縮缺口"), ha="left")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 40_inflationary_gap

```python
# Inflationary gap closed by a fall in AD -> real output falls back to Yf.
#
# Topic: AD-AS
# Use for: output above full employment (Y0 > Yf) and a fall in AD (fewer tourists,
#   contractionary fiscal or monetary policy) that brings it back to Yf (DSE2015 Q12(b))
#
# Marking-scheme points it shows:
#   - E0 right of the vertical LRAS: Y0 > Yf, inflationary gap from Yf to Y0
#   - AD0 shifts left to AD1 (arrow); new E1 where AD1 meets SRAS on LRAS
#   - real output falls Y0 -> Yf, price level falls P0 -> P1
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    S = Line((20, 30), m=0.6)
    L = Line.vertical(42)
    AD0 = Line((64, S.y(64)), m=-1.5)
    AD1 = Line(meet(L, S), m=AD0.m)              # meets SRAS on LRAS
    draw(ax, S, 20, 84, "SRAS", dy=1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, AD0, 50, 78, r"$AD_0$", dy=-1.5)
    draw(ax, AD1, 26, 54, r"$AD_1$", end="top")
    y = 70
    arrow(ax, (AD0.x(y) - 2, y), (AD1.x(y) + 2, y))

    E0, E1 = meet(AD0, S), meet(AD1, L)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", to_x=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 3, E[1] - 3, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level falls
    arrow(ax, (E0[0], O[1] - 8), (L.vx, O[1] - 8))        # real output falls
    brace(ax, L.vx, E0[0], O[1] + 1.5, "gap", side="above")
    label(ax, 68, 24, T("gap =\ninflationary gap", "gap =\n通脹缺口"), ha="left")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 41_self_adjust_deflationary

```python
# Deflationary gap closed by market forces: SRAS increases -> price level falls, output rises to Yf.
#
# Topic: AD-AS
# Use for: "how do market forces restore full-employment output" when Y < Yf:
#   excess supply of labour -> wages and costs fall -> SRAS rises (DSEPP Q13(c), DSE2024 Q7(b))
#
# Marking-scheme points it shows:
#   - AD unchanged; E0 left of the vertical LRAS (Y0 < Yf)
#   - SRAS0 shifts right to SRAS1 (arrow) until AD meets SRAS1 on LRAS
#   - E0 -> E1: price level falls P0 -> P1, real output rises Y0 -> Yf
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((16, 74), m=-0.7)
    L = Line.vertical(60)
    S0 = Line((36, AD.y(36)), m=1.5)
    S1 = Line(meet(AD, L), m=S0.m)               # meets AD on LRAS
    draw(ax, AD, 16, 84, "AD", dy=-1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, S0, 22, 47, r"$SRAS_0$", end="top")
    draw(ax, S1, 46, 81, r"$SRAS_1$", end="top")
    y = 72
    arrow(ax, (S0.x(y) + 2, y), (S1.x(y) - 2, y))

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", to_x=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 2, E[1] + 4, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level falls
    arrow(ax, (E0[0], O[1] - 8), (L.vx, O[1] - 8))        # real output rises
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 42_self_adjust_inflationary

```python
# Inflationary gap closed by market forces: SRAS decreases -> price level rises, output falls to Yf.
#
# Topic: AD-AS
# Use for: "how do market forces restore full-employment output" when Y > Yf:
#   excess demand for labour -> wages and costs rise -> SRAS falls (DSE2020 Q6)
#
# Marking-scheme points it shows:
#   - AD unchanged; E0 right of the vertical LRAS (Y0 > Yf)
#   - SRAS0 shifts left to SRAS1 (arrow) until AD meets SRAS1 on LRAS
#   - E0 -> E1: price level rises P0 -> P1, real output falls Y0 -> Yf
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((16, 80), m=-0.7)
    L = Line.vertical(44)
    S0 = Line((64, AD.y(64)), m=1.5)
    S1 = Line(meet(AD, L), m=S0.m)               # meets AD on LRAS
    draw(ax, AD, 16, 84, "AD", dy=-1.5)
    draw(ax, L, y0=O[1], y1=86, name="LRAS", end="top")
    draw(ax, S0, 52, 80, r"$SRAS_0$", end="top")
    draw(ax, S1, 30, 60, r"$SRAS_1$", end="top")
    y = 66
    arrow(ax, (S0.x(y) - 2, y), (S1.x(y) + 2, y))

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", r"$Y_0$")
    guide(ax, E1, O, r"$P_1$", to_x=False)
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 2, E[1] + 4, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    arrow(ax, (O[0] - 9, E0[1]), (O[0] - 9, E1[1]))       # price level rises
    arrow(ax, (E0[0], O[1] - 8), (L.vx, O[1] - 8))        # real output falls
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```

### 43_supply_shock_recovery

```python
# Temporary supply shock: SRAS falls (1), then recovers (2) -> P and Y return to P0 and Yf.
#
# Topic: AD-AS
# Use for: raw-material prices rise for a while, then the economy adjusts back in the
#   long run (excess labour supply -> wages fall -> SRAS rises again) (DSE2013 Q4(b))
#
# Marking-scheme points it shows:
#   - AD, SRAS0 and vertical LRAS all through E0 at (Yf, P0)
#   - arrow 1: SRAS0 shifts left to SRAS1; E0 -> E1, P rises to P1, Y falls to Y1
#   - arrow 2: SRAS1 shifts back right to SRAS0; E1 -> E0, P back to P0, Y back to Yf
# (paste the whole dsegraph library from "The library" here)


def diagram(lang="en"):
    setup(lang)
    fig, ax = new(3.2, 2.6)
    O = (12, 12)
    axes(ax, O, (88, 12), (12, 90), T("Real output", "實質產出"), T("Price level", "物價水平"))

    AD = Line((16, 78), m=-0.9)
    L = Line.vertical(56)
    S0 = Line(meet(AD, L), m=1.2)
    S1 = S0.shift(dx=-20)
    draw(ax, AD, 16, 76, "AD", dy=-1.5)
    draw(ax, L, y0=O[1], y1=88, name="LRAS", end="top")
    draw(ax, S0, 36, 87.7, r"$SRAS_0$", end="top")
    draw(ax, S1, 16, 67.7, r"$SRAS_1$", end="top")
    for A, B, y, n in ((S0, S1, 66, "1"), (S1, S0, 22, "2")):
        arrow(ax, (A.x(y) + (2 if n == "2" else -2), y), (B.x(y) + (-2 if n == "2" else 2), y))
        label(ax, (A.x(y) + B.x(y)) / 2, y + 3, n)

    E0, E1 = meet(AD, S0), meet(AD, S1)
    guide(ax, E0, O, r"$P_0$", to_x=False)
    guide(ax, E1, O, r"$P_1$", r"$Y_1$")
    for E, n in ((E0, r"$E_0$"), (E1, r"$E_1$")):
        dot(ax, *E); label(ax, E[0] + 2, E[1] + 4, n, ha="left")
    label(ax, L.vx, O[1] - 1.8, r"$Y_f$", va="top")
    return fig


if __name__ == "__main__":
    for lang in ("en", "zh"):
        save(diagram(lang), f"diagram_{lang}.png")
```
<!-- END TEMPLATES -->
