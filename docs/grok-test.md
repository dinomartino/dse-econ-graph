# AI test (about 5 minutes per AI)

For the maintainer. Run it on grok.com after any big change (and on
chatgpt.com, claude.ai and gemini.google.com when you can), and write the
results into `ROADMAP.md`.

## 1. Can Grok's sandbox show pictures and draw Chinese?

New chat (no project), paste:

> Run this Python with your code tool and show me the output, including any picture:
> ```python
> import subprocess, matplotlib, matplotlib.pyplot as plt
> print(matplotlib.__version__)
> print(subprocess.run(["fc-list", ":lang=zh", "family"], capture_output=True, text=True).stdout[:800] or "NO CHINESE FONTS")
> import os; print([p for p in ["/mnt/data", "/mnt/user-data/uploads", "/home/user", "/workspace", "/tmp"] if os.path.isdir(p)])
> fig, ax = plt.subplots(figsize=(3, 2)); ax.plot([0, 1], [1, 0]); ax.set_title("需求 demand")
> plt.savefig("t.png"); plt.show()
> ```

Write down: is a picture shown? Is 需求 drawn or are there boxes? Which font
names? Which folders exist?

## 2. The real thing

Set it up exactly as in `teacher/setup.json` for that AI (the steps the
teacher sees). Then, in a chat in that project, paste ONLY this (no
instruction, as a teacher would):

> The government sets a maximum price for face masks below the equilibrium
> price. With the aid of a diagram, explain the effect on the market.
> Marking scheme: Indicate in the diagram: price ceiling below equilibrium
> (1), the shortage (1).

Check: Does the reply contain ONLY the picture (no code, no explanation, no
question back)? Is it in English? Does it match
`gallery/01_price_ceiling_shortage_en.png`? How long did it take? Then
paste a Chinese question (e.g. from an `LQ/*_CHIN.docx`) and check that
the picture comes back in 中文. Finally ask for a change ("make demand
steeper") and check that it redraws, again picture only.
