---
name: marimo-walkthrough
description: Build marimo walkthrough notebooks with narrative story arcs, consistent visualization style, and branded CSS. Use when creating or editing marimo notebooks that present research findings as a story.
---

# Marimo Walkthrough Skill

**Requires:** load the `marimo-pair` skill to edit the live notebook kernel.
Use `marimo-pair` for all cell creation/editing; use this skill for story, style, and content decisions.

Copy `style.py` into the notebook directory. Load CSS via `custom.css`.

## Story Structure

Every walkthrough is a **5-act arc**. Each act opens with a `mo.md` header and closes with an interpretation cell.

```
Act 1 – Setup       : opening question + dataset size + filter result
Act 2 – Framework   : theory/taxonomy table + classification method note
Act 3 – Main result : primary distribution → interpretation → finer breakdown → time trend
Act 4 – Secondary   : supporting dimensions (2-panel plots) + interpretation
Act 5 – Continuous  : embedding/continuous view → probability profiles → closing insight
```

**Cell order matters.** Define all data loads and variables before the first figure that uses them. Use marimo's reactive graph but write top-to-bottom for readers.

## Cell Conventions

- **All cells are hidden by default** — `hide_code=True` on every cell (narrative and figure alike)
- Readers see only output; code is accessible via expand but never shown upfront
- `mo.md` cells open each act with `##` heading, sub-sections with `###`
- Interpretation cells immediately follow their figure — never separate them
- No orphaned section headers (a `##` cell must be followed by content, not another `##`)

### Layout: top = story, bottom = compute

Marimo's reactive graph lets variables defined anywhere be used anywhere.
Use this to separate *what readers see* from *how it's computed*:

```
[TOP — visible story]
  mo.md intro
  fig_quad          ← one-liner: just "fig_quad" or mo.Html(fig_quad)
  mo.md interpretation
  fig_types
  mo.md interpretation
  ...

[BOTTOM — hidden compute, grouped by section]
  # === Act 3: McGrath ===
  _quad_counts = ...   # data wrangling for fig_quad
  fig_quad = go.Figure(...)

  # === Act 4: Steiner ===
  _struct_counts = ...
  fig_binary = make_subplots(...)
```

**Rules:**
- Every figure has exactly two cells: a **display cell** (top, one line) and a **compute cell** (bottom, all the wrangling + figure construction)
- Display cell: just the variable name, or `mo.vstack([fig, caption])` — nothing else
- Compute cell: all `_private` intermediate variables prefixed with `_` so they don't pollute the reactive graph
- Group compute cells by section with a `# === Section Name ===` comment header
- Data loads and shared constants (PALETTE, LAYOUT_DEFAULTS) stay near the top since everything depends on them

## Markdown Style

- Bold the key finding in the first sentence: `**Choose** is the plurality…`
- State N with italics: `(*N* = 8,858)`
- Use `>` blockquote for the one-sentence summary in the closing act
- Tables for framework comparisons (not prose lists)
- Callout boxes via `/// note | Title\n…\n///` for caveats or methodology asides

## Visualization Rules

See `style.py` for `PALETTE`, `LAYOUT_DEFAULTS`, `apply_layout`.

- **No bar charts** — use point plots (scatter with error bars) for distributions
- **No green+red together** — use palette below
- White background, no grid lines, axis lines only (`showline=True`, `showgrid=False`)
- Font: 14pt body, 16pt title (set via `LAYOUT_DEFAULTS`)
- All figures: `fig.update_layout(**LAYOUT_DEFAULTS)`
- Multi-panel: `make_subplots` with `horizontal_spacing=0.12`

## Color Palette

```python
PALETTE = {
    "generate":  "#4C72B0",   # deep blue
    "choose":    "#64B5F6",   # light blue
    "negotiate": "#FFB74D",   # amber
    "execute":   "#CE93D8",   # lavender
}
```

For non-semantic series use `px.colors.qualitative.Pastel` or muted seaborn palette.

## CSS

Load at top of notebook (first cell, `hide_code=True`):

```python
mo.Html(open("custom.css").read() if Path("custom.css").exists()
        else open(Path(__file__).parent / "custom.css").read())
```

See `custom.css`. Key rules:
- Font: Fira Code (monospace) for all text — sets a data-science aesthetic
- Body text: 20px, color `#45372b` (warm dark brown)
- Accent: `#df7020` (burnt orange) for links
- Headings scaled down (h1=1.5em, h2=1.3em, h3=1.15em)

## Data Loading Pattern

```python
from pathlib import Path
import pandas as pd, json

_data_path = (Path(__file__).parent / "data.parquet"
              if "__file__" in dir() else Path("data.parquet"))
df = pd.read_parquet(_data_path)
# JSON-string columns → python objects
for col in df.columns:
    if col.endswith("_all") or col.endswith("_raw"):
        df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
```

## Explaining Complex Transformations

When a stat involves non-obvious computation (softmax, co-occurrence pairs, embedding distances, multi-label expansion), show a worked example inline using a real row from the data.

Pattern: `mo.md` cell before the figure with a `/// note | How this is computed` callout:

```
/// note | How this is computed
We pick one paper and walk through the steps:

| Step | Value |
|---|---|
| Paper | *"Collaborative agents for code review"* |
| Raw similarities | generate=0.41, choose=0.68, negotiate=0.12, execute=0.31 |
| After softmax (τ=0.05) | generate=0.02, choose=0.96, negotiate=0.00, execute=0.02 |
| Assigned label | **choose** |

Each paper's reasoning text is embedded; cosine similarity to four anchor descriptions
gives the raw scores; softmax sharpens them into a probability profile.
///
```

Rules:
- Use an actual row (pull from the dataframe, don't invent numbers)
- Show every intermediate step in a table — input → transform → output
- One example is enough; don't generalize abstractly before showing the concrete case
- Place the note *before* the figure it explains, not after

## Checklist

- [ ] All cells have `hide_code=True`
- [ ] CSS cell is first
- [ ] Imports + constants cell (style.py helpers) near top
- [ ] Data load cell before first figure
- [ ] Each figure split: one-line display cell (top) + compute cell (bottom)
- [ ] Compute cells use `_private` variable names, grouped by `# === Section ===`
- [ ] Each figure display cell immediately followed by interpretation `mo.md`
- [ ] Numbers in md cells match actual data (run cells, verify)
- [ ] N values formatted with commas: `f"{n:,}"`
- [ ] Summary table in Act 5 with all key proportions
- [ ] Complex transforms have a worked example note before the figure
