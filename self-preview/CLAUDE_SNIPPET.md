# CLAUDE.md Snippet — Self-Preview Pattern

> Copy the section below into your project's CLAUDE.md to teach the agent the visual feedback loop. Replace the placeholder values with your actual commands and paths.

---

```markdown
## Self-Preview (Visual Feedback Loop)

This project uses the **self-preview pattern**: after making changes that affect visual output, render to PNG and inspect the result before moving on.

### The loop

1. Make code changes
2. Build: `<your-build-command>`
3. Render what you changed: `python3 -m scripts.preview --items <changed-items> --size 500`
4. Read the output PNG(s) from `build/previews/` — visually verify the result
5. If something looks wrong, fix it and go back to step 2
6. Periodically render the full overview: `python3 -m scripts.preview --overview-only`

### Rules

- **Always render after visual changes.** Don't guess — look.
- **Prefer targeted renders.** Render just the items you changed, not everything.
- **Use the overview for consistency checks.** Individual items can look fine alone but break in context.
- **Large renders for detail.** Use `--size 500` or higher when checking fine details.
- **Reference overlays help.** The colored lines/boxes show alignment, bounds, and metrics — use them.

### Output paths

- `build/previews/<item>.png` — individual item renders
- `build/previews/overview.png` — full grid of all items
```
