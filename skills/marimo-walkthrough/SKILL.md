---
name: marimo-walkthrough
description: Build marimo walkthrough notebooks with narrative story arcs, consistent visualization style, and branded CSS. Use when creating or editing marimo notebooks that present research findings as a story. Use together with marimo-pair for cell editing.
---

# Marimo Walkthrough Skill

Copy `style.py` and `custom.css` into the notebook directory.

## Story Structure (5-act arc)

```
Act 1 – Setup       : opening question + dataset size + filter result
Act 2 – Framework   : theory/taxonomy + classification method note
Act 3 – Main result : primary distribution → interpretation → breakdown → time trend
Act 4 – Secondary   : supporting dimensions (2-panel) + interpretation
Act 5 – Continuous  : embedding view → probability profiles → closing insight
```

## Notebook Layout: top = story, bottom = compute

Display cells live near their narrative; all wrangling + figure construction goes at the bottom.

- Every figure: **display cell** (top, one line: just `fig_quad`) + **compute cell** (bottom)
- Compute cells: `_private` variable names, grouped with `# === Section Name ===` headers
- All cells `hide_code=True`
- Data loads + shared constants near top (everything depends on them)

## Markdown Style

- Bold key finding in first sentence; N in italics: `**Choose** leads (36%, *N* = 8,858)`
- `>` blockquote for one-sentence closing summary
- Bold bullet lists for comparisons — no markdown tables
- `/// note | Title\n…\n///` for caveats and methodology asides
- Interpretation cell immediately follows its figure

## Explaining Complex Transformations

Before any figure with a non-obvious transform, add a `/// note | How this is computed`
callout with a **real example row** — pull from the actual dataframe, never invent:

```
/// note | How this is computed
**Paper:** *"Collaborative agents for code review"*

- Raw similarities → generate=0.41, choose=0.68, negotiate=0.12, execute=0.31
- After softmax (τ=0.05) → generate=0.02, **choose=0.96**, negotiate=0.00, execute=0.02
- Assigned label: **choose**
///
```

## Visualization

`style.py` provides `PALETTE`, `LAYOUT_DEFAULTS`, `apply_layout`. Always `fig.update_layout(**LAYOUT_DEFAULTS)`.

- **No bar charts** — point plots for distributions
- **No green+red together**
- White background, no grid, axis lines only

```python
PALETTE = {"generate": "#4C72B0", "choose": "#64B5F6", "negotiate": "#FFB74D", "execute": "#CE93D8"}
```

For non-semantic series: `MUTED` from `style.py`.

## CSS

First cell: `mo.Html(open("custom.css").read())`
Fira Code font, 20px body, warm brown `#45372b`, orange accent `#df7020`.

## Data Loading

```python
_data_path = Path(__file__).parent / "data.parquet" if "__file__" in dir() else Path("data.parquet")
df = pd.read_parquet(_data_path)
for col in df.columns:
    if col.endswith("_all") or col.endswith("_raw"):
        df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
```

## Checklist

- [ ] All cells `hide_code=True`
- [ ] CSS cell first; data load + constants before first figure
- [ ] Each figure: one-line display cell (top) + compute cell (bottom, `_` prefixed)
- [ ] Compute cells grouped by `# === Section ===`
- [ ] Interpretation `mo.md` immediately after each figure
- [ ] Complex transforms: worked-example note before figure
- [ ] Numbers verified against data; N formatted `f"{n:,}"`
- [ ] Act 5 summary as bold bullet list
