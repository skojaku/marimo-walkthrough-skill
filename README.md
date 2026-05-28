# Marimo Walkthrough Skill

[Marimo](https://marimo.io/) is a Python notebook alternative to Jupyter. While I've been using Jupyter time to time, two things push me to use marimo notebook: 

1. Reproducibility - Jupyter notebook does not ensure reproducibility. Cells are, by default, executed sequentially from the top to the bottom (run-all-cell). But users can run specific cells in any order. This harms the reproducibility. 
2. Git & AI friendly - Jupyter notebook is essentially a mix of text and binary packed into a json file. Not editable and not git friendly. Marimo is just a python script without binary. An AI agent can read the notebook, understand what each cell does, add a new cell that uses an existing variable, and the notebook just works. It does not overload git.

## What is a walkthrough notebook

A walkthrough is a notebook that presents the results with a narrative, i.e., it is a linear narrative from question to finding, with figures and interpretation cells woven together. I find it very helpful for communicating with my collaborators. I've found that the structure matters as much as the content. Which figures come first, how interpretations are worded, where caveats go. These shape how they the results. This skill captures the conventions I've settled on.

## Marimo-pair

[[marimo-pair](https://github.com/marimo-team/marimo)](https://github.com/marimo-team/marimo-pair) is a AI skill that gives the AI full access to the running notebook kernel. It can read cell code, create and edit cells, run them, and see outputs.

**This skill (marimo-walkthrough) handles story and style decisions. Marimo-pair handles the actual cell operations.** Install marimo pair skill as well when using this walkthrough skill. 

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

`SKILL.md` is what AI loads as the skill prompt. I keep it intentionally short for maintainability and readability.

## My conventions

The notebooks I make follow a 5-act story arc: setup, framework, main result, secondary result, continuous/closing view. Each act opens with a heading and closes with an interpretation cell that states the finding in plain language.

Figures are split across two cells. A one-line display cell (`fig_quad`) sits near the story narrative at the top. The compute cell---data wrangling, figure construction---goes at the bottom, hidden, grouped with other compute cells for that section. Readers never see the code. This is intentional because we care about results more than code at exploration stage. Later on, thorough reviews on code are needed when the analysis pipeline is formed. 

For any stat that involves a non-obvious transformation (softmax, co-occurrence, embedding similarity), I add a worked example using a real row from the data before the figure. Numbers that came from nowhere are the most common source of confusion when sharing notebooks.

## License

MIT
