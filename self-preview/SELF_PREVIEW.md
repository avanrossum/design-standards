# The Self-Preview Pattern

> A feedback loop for AI agents that produce visual artifacts.

---

## The Problem

AI coding agents are blind to visual output. They can write CSS but can't see the page. They can generate SVG but can't tell if it looks right. They can build a font but can't read it. They can produce a chart but can't verify the data is plotted correctly.

Without visual feedback, agents work in a "write and hope" mode — making changes based on code logic alone, with no way to verify the result.

## The Solution

Render the artifact to PNG. Read it back. Fix what's wrong. Repeat.

```
code change → build → render to PNG → read PNG → assess → fix → repeat
```

The agent uses its multimodal vision capability to inspect its own output, creating a tight feedback loop without requiring human review at every step. The agent becomes its own QA reviewer.

This turns "write and hope" into "write, look, fix" — the same iterative loop human designers use.

---

## When to Use This

Use the self-preview pattern when your project produces **visual output that can't be validated by code alone**:

| Domain | Artifact | Why code review isn't enough |
|--------|----------|------------------------------|
| Font design | .ttf / .otf | Glyph shapes are coordinates — you need to see them rendered |
| Web UI | HTML/CSS | Layout, spacing, and visual hierarchy only exist visually |
| Data visualization | Charts, plots | Data correctness requires seeing the rendered output |
| SVG / vector graphics | .svg files | Path data is opaque without rendering |
| PDF generation | .pdf files | Page layout, margins, text flow need visual check |
| Game assets | Sprites, tilesets | Alignment, animation frames need visual verification |
| LaTeX / typesetting | .tex → .pdf | Formatting, equations, page breaks are visual |
| 3D rendering | Scene files | Geometry, lighting, camera angles need visual check |
| Diagram generation | Flowcharts, ERDs | Node placement, edge routing, label overlap |
| Icon / logo design | Vector assets | Proportions, optical balance, pixel alignment |

---

## How It Works

### Step 1: Build the artifact

Your project already has a build step — compiling code, generating output, running a pipeline. No changes needed here.

### Step 2: Write a render script

A small script that converts your build output to PNG. This is the only new code the pattern requires.

The render script should support:
- **Targeted rendering** — render a specific item, not just the whole thing
- **Reference overlays** — grid lines, bounding boxes, metric markers
- **CLI control** — arguments for what to render, size, overlay toggles

### Step 3: Read and assess

The agent reads the PNG using its file-reading tool (which supports images in Claude Code, Cursor, etc.), sees the rendered output, and makes informed corrections.

### Step 4: Iterate

Fix what's wrong, rebuild, re-render, re-inspect. The loop is fast enough that the agent can do 5-10 iterations in the time a human would do one.

---

## Design Principles

These principles are what make the pattern effective vs. just "render to PNG."

### 1. Make it fast

The render step should take **< 2 seconds**. If it's slow, the agent will avoid using it and revert to guessing. Optimize for speed:
- Render individual items, not the whole project
- Use lightweight renderers (Pillow over headless browsers when possible)
- Cache what doesn't change between renders

### 2. Make it targeted

Support rendering **specific items** — a single glyph, a single component, a single page. The agent needs to zoom in on what it just changed, not wade through a full specimen sheet every time.

```bash
# Good: render just what changed
render --items button spinner --size 500

# Also good: full overview for periodic checks
render --overview-only
```

### 3. Add visual context

Raw output isn't enough. The agent can see shapes but needs **reference markers** to judge correctness:

| Context type | What it helps assess |
|-------------|---------------------|
| Grid lines | Alignment, spacing consistency |
| Metric lines | Vertical positioning (baseline, x-height, etc.) |
| Bounding boxes | Size, padding, overflow |
| Labels / annotations | Identity, expected values |
| Reference colors | Distinct zones, state indicators |
| Dimension markers | Width, height, margin values |

### 4. Use high contrast

The agent's vision works best with **clean, high-contrast images**:
- Dark backgrounds with light content (or vice versa)
- Distinct colors for different overlay types
- Large enough render size to catch subtle issues (400-600px per item)
- Avoid gradients or textures behind the content being inspected

### 5. Output to predictable paths

The agent needs to know where to find the PNG without guessing:

```
build/previews/              # fixed output directory
build/previews/button.png    # predictable filename per item
build/previews/overview.png  # full overview at known path
```

### 6. Support CLI control

Give the agent knobs to control what it sees:

```bash
render --items A B C        # which items to render
render --size 500           # output size in pixels
render --no-overlays        # clean render without reference markers
render --overview-only      # just the grid/specimen view
render --overlays-only      # just the reference markers (no content)
```

---

## Reference Implementation

See `self_preview.py` in this directory — a working template you can adapt for any project.

The template provides:
- A `PreviewRenderer` base class with the core loop
- CLI argument parsing for targeted rendering
- Configurable overlays (grid, labels, bounding boxes)
- Predictable output paths
- Both single-item and overview rendering

### Adapting the template

1. **Copy `self_preview.py`** into your project's `scripts/` directory
2. **Subclass `PreviewRenderer`** and implement three methods:
   - `load_artifact()` — load your build output
   - `render_item(item, size)` — render one item to a Pillow Image
   - `get_items()` — list all renderable items
3. **Add overlay drawing** in `render_item()` using the provided helpers
4. **Wire it into your build cycle** (see CLAUDE.md snippet below)

---

## CLAUDE.md Integration

Add this to your project's `CLAUDE.md` to teach the agent the feedback loop:

```markdown
## Self-Preview (Visual Feedback Loop)

After making visual changes, use the render script to inspect your work:

\```bash
# 1. Build the project
<your build command>

# 2. Render what you changed (targeted, fast)
python3 -m scripts.preview --items <what-you-changed> --size 500

# 3. Read the PNG output → assess → fix → repeat

# 4. Periodic full overview check
python3 -m scripts.preview --overview-only
\```

Output goes to `build/previews/`. Read the PNGs to visually verify your changes.
Prefer targeted renders (specific items) over full overviews for speed.
```

---

## Render Approach by Domain

Quick reference for how to render common artifact types:

| Domain | Build output | Render to PNG with | Dependencies |
|--------|-------------|-------------------|-------------|
| **Font design** | .ttf / .otf | Pillow `ImageFont` | `Pillow`, `fonttools` |
| **Web UI** | HTML/CSS | Playwright / Puppeteer screenshot | `playwright` |
| **React components** | JSX | Storybook screenshot or `react-screenshot-test` | varies |
| **Data viz** | Code | `matplotlib.savefig()` / `plotly.write_image()` | `matplotlib` or `plotly` |
| **SVG graphics** | .svg | `cairosvg.svg2png()` | `cairosvg` |
| **PDF** | .pdf | `pdf2image.convert_from_path()` | `pdf2image`, `poppler` |
| **LaTeX** | .tex | `pdflatex` → `pdf2image` | `texlive`, `pdf2image` |
| **Game sprites** | Sprite sheet | Pillow direct load + grid overlay | `Pillow` |
| **Diagrams** | DOT / Mermaid | `graphviz` render or mermaid CLI | `graphviz` or `@mermaid-js/mermaid-cli` |
| **3D models** | Scene file | Blender CLI render / `trimesh` | varies |
| **Icons** | SVG/PNG | Pillow at multiple sizes + pixel grid | `Pillow`, `cairosvg` |

---

## What Makes This Different from Screenshots

Taking a screenshot is one thing. The self-preview pattern is specifically designed for **AI agent feedback loops**, which means:

1. **Reference overlays** — not just "what it looks like" but "what it should look like" (grid lines, metrics, bounding boxes give the agent a spec to compare against)
2. **Targeted rendering** — the agent renders just what it changed, not a full page, keeping the loop fast and focused
3. **CLI-driven** — the agent controls what to render and at what detail level, rather than always getting the same output
4. **Predictable output** — fixed paths mean the agent doesn't need to search for files or parse command output
5. **High contrast by default** — optimized for AI vision, not human aesthetics

---

## Origin

Developed during the [Cairn Mono](https://github.com/avanrossum/can-claude-make-a-font) project — building an ADHD-optimized monospaced font entirely with an AI agent. The agent needed to see what it was drawing to make informed corrections. The render script (`render_glyphs.py`) became the most critical tool in the workflow, enabling 5-10 iteration cycles per glyph where the agent would build, render, inspect the PNG, spot issues, and fix them autonomously.

Without it, the agent was guessing. With it, the agent was designing.

---

*Pattern by [Cairn Mono](https://github.com/avanrossum/can-claude-make-a-font). Contribute improvements back to [design-standards](https://github.com/avanrossum/design-standards).*
