# Marimo Walkthrough Skill

[Marimo](https://marimo.io/) is a Python notebook where cells are reactive — edit one cell and every downstream cell updates automatically. I use it for all my research notebooks.

## Why marimo

Three things keep me coming back.

**Reactive.** Marimo tracks which variables each cell defines and which it uses. Change a cell, and marimo reruns everything that depends on it — and only that. No more running cells out of order and getting confused about why the result changed. The notebook is always in a consistent state.

**Reproducible.** Marimo saves notebooks as plain `.py` files. There's no hidden kernel state. If a notebook runs top-to-bottom without error, it's reproducible. I can `git diff` it, review it, and run it on a server with `marimo run notebook.py`.

**AI-friendly.** This is underrated. Because marimo is just Python and the reactive graph is explicit, an AI agent can read the notebook, understand what each cell does, add a new cell that uses an existing variable, and the notebook just works. No hidden state to untangle. I work with AI assistants on notebooks constantly now, and marimo makes that surprisingly smooth.

## What is a walkthrough notebook

A walkthrough is a notebook that tells a story. Not a scratchpad, not a dashboard — a linear narrative from question to finding, with figures and interpretation cells woven together. The reader scrolls top to bottom and follows the argument.

I've found that the structure matters as much as the content. Which figures come first, how interpretations are worded, where caveats go — these shape how a reader understands the results. This skill captures the conventions I've settled on.

## Marimo-pair

[marimo-pair](https://github.com/marimo-team/marimo) is a Claude Code skill that gives the AI full access to the running notebook kernel. It can read cell code, create and edit cells, run them, and see outputs — all while the notebook is live in the browser.

The key API is `marimo._code_mode`:

```python
import marimo._code_mode as cm

async with cm.get_context() as ctx:
    cid = ctx.create_cell("fig_quad", hide_code=True)
    ctx.run_cell(cid)
```

Without marimo-pair, editing a running notebook from the outside is fragile — direct file writes are silently clobbered when the kernel saves. Marimo-pair is the right way to let an AI work inside a live session.

**This skill (marimo-walkthrough) handles story and style decisions. Marimo-pair handles the actual cell operations.** Load both when building or editing a walkthrough.

## Installation

### Using `npx skills` (works across agents)

```bash
npx skills add skojaku/marimo-walkthrough-skill --all

# Or target Claude Code specifically
npx skills add skojaku/marimo-walkthrough-skill -a claude-code
```

### Manual install

Copy `skills/marimo-walkthrough/` to `~/.claude/skills/marimo-walkthrough/`.

### Per-notebook files

Copy `style.py` and `custom.css` into the notebook directory:

```bash
cp skills/marimo-walkthrough/style.py notebooks/my-notebook/
cp skills/marimo-walkthrough/custom.css notebooks/my-notebook/
```

## What's in this skill

```
skills/marimo-walkthrough/
├── SKILL.md      # Story arc, layout, markdown style, visualization rules, checklist
├── style.py      # PALETTE, LAYOUT_DEFAULTS, apply_layout(), softmax_profile()
└── custom.css    # Fira Code font, 20px body, warm brown + orange accent
```

`SKILL.md` is what Claude Code loads as the skill prompt. It's intentionally short — around 90 lines — because it's used alongside marimo-pair and doesn't need to repeat what that skill already covers.

## My conventions

The notebooks I make follow a 5-act story arc: setup → framework → main result → secondary result → continuous/closing view. Each act opens with a heading and closes with an interpretation cell that states the finding in plain language.

Figures are split across two cells. A one-line display cell (`fig_quad`) sits near the story narrative at the top. The compute cell — data wrangling, figure construction — goes at the bottom, hidden, grouped with other compute cells for that section. Marimo's reactive graph makes this possible: define a variable anywhere and use it anywhere. Readers never see the code; they see outputs.

All intermediate variables in compute cells are prefixed `_` so they don't pollute the reactive namespace and don't trigger spurious reruns.

For any stat that involves a non-obvious transformation (softmax, co-occurrence, embedding similarity), I add a worked example using a real row from the data before the figure. Numbers that came from nowhere are the most common source of confusion when sharing notebooks.

## License

MIT
