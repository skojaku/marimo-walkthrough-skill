# marimo-walkthrough-skill

Claude Code skill for writing marimo walkthrough notebooks: story structure, visualization preferences, CSS.

## Install

```bash
# Copy skill into your Claude skills directory
cp -r skills/marimo-walkthrough ~/.claude/skills/
```

Then in Claude Code settings, add:
```json
{ "skillsDirectory": "~/.claude/skills" }
```

## Files

```
skills/marimo-walkthrough/
├── SKILL.md      # Skill prompt (loaded by Claude Code)
├── style.py      # PALETTE, LAYOUT_DEFAULTS, apply_layout, softmax_profile
└── custom.css    # Fira Code font, warm color scheme, 20px body text
```

Copy `style.py` and `custom.css` into each notebook's directory.
