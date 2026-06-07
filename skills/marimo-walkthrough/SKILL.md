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

## Writing Principles

These matter as much as the layout. Readers (and reviewers) judge the prose.

- **Plain, common English.** Short sentences, everyday words. Avoid em-dashes and
  ornate diction ("signature", "confound", "manufacture", "hugs zero"). Spell out
  Greek letters in prose (mu, sigma), even if the figures use μ, σ.
- **Be specific; never vague.** Name the exact quantity: the statistic, what it is
  computed over, and its units. Write "Spearman ρ between the score and citations
  over the next 5 years," not "the number" or "the value." Replace "the score
  works" with the measured quantity. Vague nouns ("number", "value", "signal") are
  a smell — pin them to a definition.
- **Explain the mechanism, not just the result.** After "X is negative," say *why*
  it is negative. A result without a cause reads as unexplained.
- **Cut the obvious.** If a point is self-evident, do not give it its own section,
  figure, or paragraph. Less text beats more.
- **Define every element when first introduced** (see below).

## Show the Math

State models and methods as equations — math makes a claim specific. Define every
symbol in prose right after the equation.

- marimo renders LaTeX with MathJax. Inline: `$\mu_i$`. A display block `$$ … $$`
  **must sit on its own line with a blank line before and after** — otherwise it
  nests and renders broken.
- Annotate terms with `\underbrace{(k_j+1)}_{\text{preferential attachment}}`.
- Give the actual generative/statistical model (citation weight, aging kernel,
  link probability), not a verbal sketch. Pull the exact form from the source code
  so it is correct.

## Define Every Figure Element

Before (or at) a figure, define every label the reader meets for the first time:
each series, axis, abbreviation, and condition name. A short bold-bullet glossary
works well. Readers cannot infer "bw", "neutral aging", or "PSO" from the axis
alone — name and explain each one.

## Concept Schematic & Mechanism Evidence

- Open the body with **one simple schematic** that defines the core quantity (e.g.
  a small labeled network). Keep it minimal: one panel, a few labels. Resist a
  second panel or extra annotations — an overloaded schematic does not land.
- When you claim a mechanism, the strongest evidence is a **controlled/synthetic
  test showing which ingredients are necessary**. A dumbbell (two quantities per
  condition, with a zero reference) reads well for an ablation.

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

- **Mean is half-story** — always show spread alongside central tendency: error bars (±1 SD or 95% CI), strip plots, violin, or a distribution panel. A single point with no spread is incomplete.
- **Spread ≠ uncertainty of the mean.** SD/IQR say how variable individual cases
  are; SE/CI say how well the *mean* is pinned down. If the claim is about a mean
  ("significantly negative"), show **SE or CI, not SD** — a large SD can hide a
  well-resolved mean and make a real effect look like noise. **Always label which
  the bars are.** For small/noisy replicates, average within each independent
  replicate first, then show SE across replicates (and note when a paired
  difference is more stable than either endpoint).
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

Keep the notebook self-contained: save a small **processed** CSV into the
notebook's `data/` dir (e.g. per-condition means + SE) rather than loading a
multi-MB raw file at render time.

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
- [ ] Every mean/proportion accompanied by spread (SD, CI, or distribution)
- [ ] Error bars labeled; SE/CI (not SD) when the claim is about a mean
- [ ] Numbers verified against data; N formatted `f"{n:,}"`
- [ ] Act 5 summary as bold bullet list
- [ ] Plain English; no em-dashes or jargon; Greek spelled out in prose
- [ ] Every quantity named precisely (statistic + what it is over + units); no vague "number/value"
- [ ] Mechanism explained (the why), not just the result
- [ ] Every figure element (series, axis, abbreviation, condition) defined when first introduced
- [ ] Models/methods shown as equations (`$$` on its own line, blank line around it)
- [ ] Obvious points cut; concept schematic kept minimal
