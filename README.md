# Design Standards

> Shared design systems, coding standards, and documentation templates for macOS applications.

---

## For AI Agents

**Read `SHARED.md` first** - Universal principles across all frameworks.

Then read the framework-specific guides:

| Framework | Files to Read |
|-----------|---------------|
| **Electron + React** | `electron/STYLEGUIDE.md`, `electron/CODING_STANDARDS.md` |
| **Swift + SwiftUI** | `swift-macos/STYLEGUIDE.md`, `swift-macos/CODING_STANDARDS.md` |

### Key Points (All Frameworks)

- **Theme adaptability** - Support light and dark modes as first-class citizens
- **Native feel** - Match platform conventions
- **State sync** - Refresh UI after data mutations
- **Error handling** - Every external operation can fail

### Contributing Back

If you discover patterns worth standardizing:

```bash
cd docs/standards && git add -A && git commit -m "Add: [pattern]" && git push
```

---

## Repository Structure

```
design-standards/
├── SHARED.md                  # Universal principles (READ FIRST)
├── README.md                  # This file
│
├── electron/                  # Electron + React (JavaScript)
│   ├── CODING_STANDARDS.md    # Code conventions, patterns
│   ├── STYLEGUIDE.md          # Visual design, CSS, components
│   ├── DOCUMENTATION_STANDARDS.md
│   └── templates/             # Starter doc templates
│       ├── ARCHITECTURE.md
│       ├── CLAUDE.md
│       ├── ROADMAP.md
│       └── CHANGELOG.md
│
└── swift-macos/               # Native Swift + SwiftUI
    ├── CODING_STANDARDS.md    # Swift conventions, patterns
    ├── STYLEGUIDE.md          # SwiftUI design, components
    ├── DOCUMENTATION_STANDARDS.md
    └── templates/             # Starter doc templates
        ├── ARCHITECTURE.md
        ├── CLAUDE.md
        ├── ROADMAP.md
        └── CHANGELOG.md
```

---

## Quick Start

### Option 1: Clone as Submodule (Recommended)

```bash
# From your project root
git submodule add git@github.com:avanrossum/design-standards.git docs/standards
```

### Option 2: Clone Directly

```bash
git clone git@github.com:avanrossum/design-standards.git docs/standards
```

### Option 3: Copy Individual Files

```bash
# For Electron project
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/electron/STYLEGUIDE.md > docs/STYLEGUIDE.md
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/electron/CODING_STANDARDS.md > docs/CODING_STANDARDS.md

# For Swift project
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/swift-macos/STYLEGUIDE.md > docs/STYLEGUIDE.md
curl -sL https://raw.githubusercontent.com/avanrossum/design-standards/main/swift-macos/CODING_STANDARDS.md > docs/CODING_STANDARDS.md
```

---

## What's Included

### Per Framework

| File | Purpose |
|------|---------|
| `CODING_STANDARDS.md` | Language conventions, patterns, file organization |
| `STYLEGUIDE.md` | Visual design - colors, typography, spacing, components |
| `DOCUMENTATION_STANDARDS.md` | How to document your project |
| `templates/` | Starter templates for CLAUDE.md, ARCHITECTURE.md, etc. |

### Shared

| File | Purpose |
|------|---------|
| `SHARED.md` | Universal principles across all frameworks |

---

## Framework Quick Reference

### Electron + React

- **Language**: JavaScript (no TypeScript)
- **UI**: React 18+ functional components
- **State**: Context + useReducer
- **Styling**: CSS variables for theming
- **IPC**: `ipcMain.handle` / `ipcRenderer.invoke`

### Swift + SwiftUI

- **Language**: Swift 5.9+
- **UI**: SwiftUI (AppKit fallback)
- **State**: @Observable / ObservableObject
- **Styling**: System colors, SF Symbols
- **Concurrency**: async/await, actors

---

## Keeping Standards in Sync

### Pushing Updates

When you discover patterns worth standardizing:

```bash
cd docs/standards
git add -A
git commit -m "Add: [description]"
git push origin main
```

### Pulling Updates

```bash
cd docs/standards
git pull origin main
```

### For Submodules

```bash
# Pull latest
git submodule update --remote docs/standards

# Commit the update
git add docs/standards
git commit -m "chore: Update design standards"
```

---

## Adding a New Framework

1. Create directory: `framework-name/`
2. Adapt the three core docs:
   - `CODING_STANDARDS.md`
   - `STYLEGUIDE.md`
   - `DOCUMENTATION_STANDARDS.md`
3. Create `templates/` with starter files
4. Update `SHARED.md` structure section
5. Update this README

See `SHARED.md` for detailed adaptation guidelines.

---

## Origins

Originally extracted from the [Actions](https://github.com/avanrossum/actions) macOS menu-bar app. Designed for:

- macOS-native aesthetic
- AI-assisted development (Claude Code)
- Consistent quality across projects

---

*Standards evolve. Keep them fresh.*
