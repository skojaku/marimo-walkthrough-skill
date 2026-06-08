"""Visualization defaults for marimo walkthrough notebooks.

Copy this file into the notebook directory and import:
    from style import PALETTE, MUTED, LAYOUT_DEFAULTS, apply_layout, band, softmax_profile
"""

import numpy as np

# ── Text / reference colors ─────────────────────────────────────────────────
INK       = "#222222"   # body text, titles, axis labels (near-black grey, NOT brown)
MUTED_INK = "#555555"   # secondary text / annotations
ACCENT    = "#c75d12"   # muted burnt orange — one highlight series, used sparingly
CONNECTOR = "#cccccc"   # dumbbell connector lines, faint links
ZERO_REF  = "#999999"   # zero / reference lines

# Two-series comparison (e.g. aggregate vs within-bin, condition A vs B). Avoid brown.
PAIR = ["#2c7fb8", "#c75d12"]   # blue, orange

# ── Color palette ──────────────────────────────────────────────────────────
# Semantic quadrant colors (McGrath circumplex)
PALETTE = {
    "generate":  "#4C72B0",   # deep blue
    "choose":    "#64B5F6",   # light blue
    "negotiate": "#FFB74D",   # amber
    "execute":   "#CE93D8",   # lavender
}

# General-purpose muted sequence (colorblind-safe, no green+red adjacent, no brown)
MUTED = ["#4C72B0", "#64B5F6", "#FFB74D", "#CE93D8", "#A0A0A0", "#6E7B8B"]

# ── Plot layout ────────────────────────────────────────────────────────────
FONT_SIZE  = 14
TITLE_SIZE = 16

_axis = dict(
    showgrid=False,
    showline=True,
    linewidth=1,
    linecolor=INK,
    mirror=False,
    title_font=dict(size=FONT_SIZE, color=INK),
    tickfont=dict(size=FONT_SIZE - 1, color=INK),
)

LAYOUT_DEFAULTS = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=FONT_SIZE, color=INK),          # global text color: grey, never brown
    title_font=dict(size=TITLE_SIZE, color=INK),
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


def band(fig, x, y, se, color="#2c7fb8", opacity=0.18, row=None, col=None):
    """Add a +/-1 SE shaded band around a line (uncertainty is mandatory — see SKILL.md).

    x, y, se are 1-D arrays of equal length. Draws a filled polygon y +/- se.
    Pair this with the line trace itself. Add the band BEFORE the line so the
    line sits on top. For subplots pass row/col.
    """
    import plotly.graph_objects as go
    x = np.asarray(x, float); y = np.asarray(y, float); se = np.asarray(se, float)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fill = f"rgba({r},{g},{b},{opacity})"
    tr = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y + se, (y - se)[::-1]]),
        fill="toself", fillcolor=fill, line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    )
    if row is not None:
        fig.add_trace(tr, row=row, col=col)
    else:
        fig.add_trace(tr)
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
