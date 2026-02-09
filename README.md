# Design Standards

> Shared design system, coding standards, and documentation templates for Electron + React macOS apps.

---

## For AI Agents

**Read these files before writing code:**

| File | When to Read |
|------|--------------|
| `STYLEGUIDE.md` | Before writing CSS or designing UI components |
| `CODING_STANDARDS.md` | Before writing any code |
| `DOCUMENTATION_STANDARDS.md` | Before creating or updating docs |
| `templates/CLAUDE.md` | Template for your project's AI context file |

### Key Points

- **Colors**: Use CSS variables (`--bg-primary`, `--text-secondary`, etc.)
- **Spacing**: 4px base unit
- **Components**: Functional React only, no TypeScript
- **IPC**: Use `ipcMain.handle`/`ipcRenderer.invoke` pattern
- **State**: React Context + useReducer

### Contributing Back

If you discover patterns that should be standardized, push them to this repo:

```bash
cd docs/standards && git add -A && git commit -m "Add: [pattern]" && git push
```

---

## Quick Start

### Option 1: Clone into your project

```bash
# From your project root
git clone git@github.com:avanrossum/design-standards.git docs/standards

# Or as a submodule (recommended for versioning)
git submodule add git@github.com:avanrossum/design-standards.git docs/standards
```

### Option 2: Copy individual files

```bash
# Copy what you need
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/STYLEGUIDE.md > docs/STYLEGUIDE.md
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/CODING_STANDARDS.md > docs/CODING_STANDARDS.md
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/DOCUMENTATION_STANDARDS.md > docs/DOCUMENTATION_STANDARDS.md
```

---

## What's Included

| File | Purpose |
|------|---------|
| `STYLEGUIDE.md` | Visual design system - colors, typography, spacing, components, animations |
| `CODING_STANDARDS.md` | Code conventions - JS/React patterns, naming, file organization |
| `DOCUMENTATION_STANDARDS.md` | Doc templates - CLAUDE.md, ARCHITECTURE.md, ROADMAP.md, CHANGELOG.md |
| `templates/` | Starter templates for common docs |

---

## Keeping Standards in Sync

**This is a living document.** As you work on projects, you'll discover new patterns, gotchas, and improvements. Push them back here so all projects benefit.

### Pushing Updates

When you discover something that should be standardized:

```bash
cd docs/standards  # or wherever you cloned it
git add -A
git commit -m "Add: [what you learned]"
git push origin main
```

### Pulling Updates

Regularly sync to get improvements from other projects:

```bash
cd docs/standards
git pull origin main
```

### For Submodules

```bash
# Pull latest standards
git submodule update --remote docs/standards

# Commit the update to your project
git add docs/standards
git commit -m "chore: Update design standards"
```

---

## Workflow

### Starting a New Project

1. Clone/copy the standards into your project
2. Copy templates for your doc files (CLAUDE.md, etc.)
3. Customize for your specific project

### During Development

1. **Follow the standards** - They exist for consistency
2. **Note exceptions** - If something doesn't fit, document why
3. **Contribute back** - Found a better pattern? Push it upstream

### Periodic Review

- **Weekly**: Check if any project-specific patterns should be standardized
- **Per release**: Review and update docs based on learnings
- **Quarterly**: Prune outdated patterns, add new ones

---

## Project Origins

Originally extracted from the [Actions](https://github.com/avanrossum/actions) macOS menu-bar app. Designed for:

- Electron 28+ applications
- React 18+ (functional components)
- macOS-native aesthetic
- AI-assisted development (Claude Code)

---

*Standards evolve. Keep them fresh.*
