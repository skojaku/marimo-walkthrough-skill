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
- All cells `hide_code=True` — including the compute cells, the import cell, and data loads
- Data loads + shared constants near top (everything depends on them)
- **A compute cell must not render its own output**, or the figure appears a second time
  below the story. Its last line must be an *assignment*, not a bare figure expression. End
  figure-building cells with `_ = None` (or assign the final call). marimo shows output only
  when the last line is an expression; `fig.update_xaxes(...)` returns the figure and *will*
  render. Verify: a compute cell's `output` should be `None`, only the display cell holds the `Figure`.

## Compression: the reader has an attention budget

Treat the reader's attention as a fixed budget. Every cell, figure, equation, and sentence spends
some of it; spend it only where it buys understanding. A walkthrough is read once, skimmed, by a
busy colleague — the goal is the most understanding per unit attention, not the most complete
record. When in doubt, cut. After a first draft, delete ~30%.

Before adding anything, ask: *does this earn its place in the attention budget?* If two cells make
the same point, merge them. If a figure needs three paragraphs to explain, the figure is wrong.

- **Consolidate near-duplicates.** If several items differ in only one thing (conditions, models,
  fields), present them together — one figure, one table, one shared form — instead of repeating
  the whole structure for each. Repetition spends attention without adding understanding.
- **One interpretation per figure**, ideally a short bold-led sentence plus a bullet list of
  the numbers. No second paragraph restating it.
- **No rhetorical flourishes.** Banned: "the signature", "the punchline", "in disguise", "a
  reminder that…", "textbook", "strikingly", "it turns out", "interestingly", "notably". State
  the fact.
- **No hedging chains** ("seems to roughly suggest that it might"). Say what the data shows, with
  its uncertainty.
- **Don't restate the conclusion** in the intro, the caption, and the summary. Pick one place.
- **Cut the obvious.** If a point is self-evident, it gets no section, figure, or sentence.
- The closing summary is a **bullet list**, 3–5 lines, numbers included. Not prose.

## Writing Principles

- **Plain, common English.** Short sentences, everyday words. Avoid em-dashes. Spell out Greek
  letters in prose (mu, sigma), even if figures use μ, σ.
- **Be specific; never vague.** Name the exact quantity: the statistic, what it is computed over,
  and its units — "Spearman ρ between the score and citations over the next 5 years", not "the
  number"/"the value"/"the signal". Vague nouns are a smell; pin them to a definition.
- **Explain the mechanism, not just the result.** After "X is negative", say *why*.
- **Define every element when first introduced** (see below).

## Accuracy: the prose must match the numbers

The fastest way to lose a reader's trust is a caption that overstates the figure. Check every
claim against the actual values *with their uncertainty* before writing it.

- **Don't generalize past the data.** "Every field shows the effect" is wrong if one field's
  estimate overlaps zero. Say "three of four; the fourth is borderline (X ± SE)".
- **Distinguish an effect from its absence.** A *sign flip* (clearly negative) is not the same as
  a *collapse to zero* (no effect). Name which one each case is.
- **Read the figure you are captioning.** If you write "flat across rows", confirm the rows are
  flat — they may rise in one and fall in another. Describe what is actually there.
- **Quote borderline / null results honestly**, with the ± so the reader sees they are borderline.

## Uncertainty is mandatory in every plot

A point or line with no uncertainty is an incomplete result. **Every figure shows uncertainty.**

- **Prefer a bootstrapped confidence interval over an analytic SE.** Resample the underlying units
  (papers, replicates) with replacement, recompute the statistic each time (1000+ resamples), and
  show the 2.5–97.5% percentile interval. This is the default because the statistics here —
  Spearman/partial correlations, count-weighted within-bin means, ratios — have no clean closed-form
  SE, and bootstrap makes no normality assumption. Reach for an analytic SE only when bootstrap is
  genuinely infeasible.
- **Means/points → error bars at the CI; lines → a shaded CI band** (use `band()` from `style.py`,
  passing the half-CI). Dumbbells and point plots get `error_x`/`error_y` set to the CI.
- **Spread ≠ uncertainty of the estimate.** SD/IQR say how variable individual cases are; a CI says
  how well the *estimate* is pinned down. If the claim is about an estimate ("significantly
  negative"), show the **CI, not SD**. **Always label what the interval is** (e.g. "95% bootstrap CI
  over papers", or "±1 SE across degree bins" if you fall back to SE).
- **Simulated / synthetic results need real uncertainty too.** Run the model over several seeds and
  bootstrap / take the interval across seeds — do not report a single run, and do not fake a tiny
  analytic SE (1/√n is meaningless when the variation that matters is between runs).
- A figure where uncertainty would change the conclusion (an estimate that may overlap zero) must
  make that visible — that is the whole point.

## Show the Math

State models and methods as equations — math makes a claim specific. Define every symbol right
after the equation.

- marimo renders LaTeX with MathJax. Inline `$\mu_i$`. A display block `$$ … $$` **must sit on its
  own line with a blank line before and after**, or it renders broken.
- Annotate terms with `\underbrace{(k_j+1)}_{\text{preferential attachment}}`.
- Give the actual generative/statistical model, not a verbal sketch. Pull the exact form from the
  source code so it is correct.
- **Define each symbol once, at its point of use.** Do not introduce notation the shown equation
  does not use, and do not define the same symbol twice (once in prose, again in a glossary).

## Define Every Figure Element

Before (or at) a figure, define every label the reader meets for the first time: each series,
axis, abbreviation, and condition name. A short bold-bullet glossary works well. Readers cannot
infer "bw", "neutral aging", or "PSO" from the axis alone.

## Concept Schematic & Mechanism Evidence

- Open the body with **one simple schematic** that defines the core quantity (e.g. a small labeled
  network). One panel, a few labels. An overloaded schematic does not land.
- When you claim a mechanism, the strongest evidence is a **controlled/synthetic test showing
  which ingredients are necessary**. A dumbbell (two quantities per condition, with a zero
  reference, error bars on each) reads well for an ablation.

## Explaining Complex Transformations

Before any figure with a non-obvious transform, add a `/// note | How this is computed` callout
with a **real example row** — pull from the actual dataframe, never invent:

```
/// note | How this is computed
**Paper:** *"Collaborative agents for code review"*

- Raw similarities → generate=0.41, choose=0.68, negotiate=0.12, execute=0.31
- After softmax (τ=0.05) → generate=0.02, **choose=0.96**, negotiate=0.00, execute=0.02
- Assigned label: **choose**
///
```

For a statistical method (partial correlation, residualization), a tiny worked table (≤4 rows of
ranks + the resulting number) makes the recipe concrete.

## Tables

Default to bold bullet lists for comparisons. A **small markdown table is fine** for two cases: a
model × switch on/off matrix, and a short worked-example table (≤5 rows). Keep them tiny; large
tables belong in an appendix, not the narrative.

## Markdown Style

- Bold key finding in first sentence; N in italics: `**Choose** leads (36%, *N* = 8,858)`
- `/// note | Title\n…\n///` for caveats and methodology asides
- Interpretation cell immediately follows its figure

## Visualization

`style.py` provides `INK`, `ACCENT`, `MUTED`, `PAIR`, `CONNECTOR`, `ZERO_REF`, `PALETTE`,
`LAYOUT_DEFAULTS`, `apply_layout`, `band`. Always `apply_layout(fig, ...)`.

- **Text is grey/near-black (`INK = #222`), never brown.** `apply_layout` sets the global font
  color; do not override figure text to a warm tone. Reference/zero lines `ZERO_REF`; dumbbell
  connectors `CONNECTOR` (neutral grey, not tan).
- **Two-series comparisons** use `PAIR` (blue / muted-orange). The accent orange is for one
  highlight series or links — use it sparingly, not as a fill across the figure.
- **No bar charts** — point plots for distributions.
- **No green+red together.**
- White background, no grid, axis lines only.

```python
PALETTE = {"generate": "#4C72B0", "choose": "#64B5F6", "negotiate": "#FFB74D", "execute": "#CE93D8"}
```

For non-semantic series: `MUTED` from `style.py`.

## CSS

First cell: `mo.Html(open("custom.css").read())`
Fira Code font, 20px body, **grey ink `#222` (not brown)**, muted orange accent `#c75d12` for
links/highlights only, neutral grey admonition boxes.

## Data Loading

Keep the notebook self-contained: save a small **processed** CSV into the notebook's `data/` dir
(per-condition means + SE, including any seed-to-seed SE you computed) rather than loading a
multi-MB raw file at render time.

```python
_data_path = Path(__file__).parent / "data.parquet" if "__file__" in dir() else Path("data.parquet")
df = pd.read_parquet(_data_path)
for col in df.columns:
    if col.endswith("_all") or col.endswith("_raw"):
        df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
```

## Checklist

- [ ] All cells `hide_code=True` (including compute/import/data cells)
- [ ] Compute cells render nothing (last line is an assignment; figure shows only in its display cell)
- [ ] CSS cell first; data load + constants before first figure
- [ ] Each figure: one-line display cell (top) + compute cell (bottom, `_` prefixed)
- [ ] **Every figure shows uncertainty** (bootstrap CI preferred over SE); interval labeled (what it is over)
- [ ] Simulated results use real across-seed uncertainty (multiple runs), not a single run or analytic 1/√n
- [ ] Every claim matches the numbers *with* uncertainty; borderline/null cases stated honestly
- [ ] Sign-flip vs collapse-to-zero named correctly; no over-generalization past the data
- [ ] Compression pass done (~30% cut); near-duplicates consolidated; no banned flourishes; conclusion stated once
- [ ] Numbers verified against data; N formatted `f"{n:,}"`
- [ ] Closing summary as a bold bullet list with numbers
- [ ] Plain English; no em-dashes; Greek spelled out in prose
- [ ] Every quantity named precisely (statistic + what it is over + units); no vague "number/value"
- [ ] Mechanism explained (the why), not just the result
- [ ] Every figure element (series, axis, abbreviation, condition) defined when first introduced
- [ ] Symbols defined once, at point of use; no unused notation
- [ ] Models/methods shown as equations (`$$` on its own line, blank line around it)
- [ ] Text grey/near-black, not brown; accent orange used sparingly
- [ ] Obvious points cut; concept schematic kept minimal
