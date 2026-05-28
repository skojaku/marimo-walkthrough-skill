"""Visualization defaults for marimo walkthrough notebooks.

Copy this file into the notebook directory and import:
    from style import PALETTE, LAYOUT_DEFAULTS, apply_layout, softmax_profile
"""

import numpy as np

# ── Color palette ──────────────────────────────────────────────────────────
# Semantic quadrant colors (McGrath circumplex)
PALETTE = {
    "generate":  "#4C72B0",   # deep blue
    "choose":    "#64B5F6",   # light blue
    "negotiate": "#FFB74D",   # amber
    "execute":   "#CE93D8",   # lavender
}

# General-purpose muted sequence (safe for colorblind, no green+red adjacent)
MUTED = ["#4C72B0", "#64B5F6", "#FFB74D", "#CE93D8", "#A0A0A0", "#8C7A6B"]

# ── Plot layout ────────────────────────────────────────────────────────────
FONT_SIZE  = 14
TITLE_SIZE = 16

_axis = dict(
    showgrid=False,
    showline=True,
    linewidth=1,
    linecolor="black",
    mirror=False,
    title_font=dict(size=FONT_SIZE),
    tickfont=dict(size=FONT_SIZE - 1),
)

LAYOUT_DEFAULTS = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=FONT_SIZE),
    title_font=dict(size=TITLE_SIZE),
    xaxis=_axis,
    yaxis=_axis,
    margin=dict(l=60, r=30, t=50, b=60),
)


def apply_layout(fig, **overrides):
    """Apply LAYOUT_DEFAULTS to a plotly figure, with optional overrides."""
    fig.update_layout(**{**LAYOUT_DEFAULTS, **overrides})
    # Propagate axis style to all subplots
    for ax in [k for k in fig.layout if k.startswith(("xaxis", "yaxis"))]:
        fig.layout[ax].update(_axis)
    return fig


# ── Softmax probability profile ───────────────────────────────────────────
def softmax_profile(raw_dict: dict, temperature: float = 0.05) -> dict:
    """Convert cosine similarities to a probability profile via softmax.

    Args:
        raw_dict: {label: similarity_score}
        temperature: lower = sharper (default 0.05)

    Returns:
        {label: probability}
    """
    keys = list(raw_dict.keys())
    vals = np.array([raw_dict[k] for k in keys], dtype=float)
    exp_vals = np.exp((vals - vals.max()) / temperature)
    probs = exp_vals / exp_vals.sum()
    return {k: float(p) for k, p in zip(keys, probs)}
