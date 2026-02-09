# Documentation Standards

> How to document the Actions codebase (and similar projects). Practical guidelines for maintainable docs.

---

## Core Documents

Every project should have these files at the root:

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | What it is, how to install, how to use | End users |
| `CLAUDE.md` | Session context for AI assistants | Claude/AI tools |
| `ARCHITECTURE.md` | System design, patterns, data flow | Developers |
| `ROADMAP.md` | Features, priorities, version history | Product/Dev team |
| `CHANGELOG.md` | What changed per version | Everyone |
| `STYLEGUIDE.md` | Visual design system | Designers/Devs |
| `CODING_STANDARDS.md` | Code conventions | Developers |

---

## CLAUDE.md (AI Session Context)

The most important file for AI-assisted development. Structure it for quick orientation:

### Template

```markdown
# Claude Code Instructions for [Project Name]

> **This file is for LLM sessions.** Quick context for working on this codebase.

## Session Start Checklist

1. Read `ROADMAP.md` - Current sprint and priorities
2. Read `ARCHITECTURE.md` - Patterns and structure
3. Check active tasks before making changes

## Quick Context

**[Project Name]** is a [one-sentence description]. Built with [tech stack].

### Key Files

| Purpose | File |
|---------|------|
| Entry point | `src/main/main.js` |
| State management | `src/renderer/App.jsx` |
| [Add 5-8 most important files] |

### Commands

\`\`\`bash
npm run dev    # Development
npm run build  # Production
\`\`\`

## Patterns to Follow

[List 3-5 most important patterns with brief examples]

## Coding Standards

[Link to or summarize key conventions]

## Critical Gotchas

[List known issues, quirks, "don't do this" items]

## Documentation Updates

When making changes:
- Update ROADMAP.md if adding/completing features
- Update ARCHITECTURE.md if changing patterns
- Update CHANGELOG.md for releases

## Session End Checklist

1. Ensure changes are tested
2. Update ROADMAP.md if tasks completed
3. Document new gotchas
4. Leave codebase working
```

### Key Principles

- **Front-load the important stuff** - AI context windows are limited
- **Be specific** - File paths, not vague descriptions
- **Include gotchas** - Save future sessions from repeating mistakes
- **Keep it current** - Update after each significant session

---

## ARCHITECTURE.md

Document the system design for developers who need to understand the codebase.

### Template

```markdown
# Architecture

## Overview

[2-3 sentences describing what the system does and its high-level design]

## Tech Stack

- **Runtime**: Electron 28+
- **UI**: React 18 (functional components)
- **Build**: Vite
- **State**: Context + useReducer
- [Add key dependencies]

## System Diagram

\`\`\`
┌─────────────────────────────────────────────────┐
│                  Main Process                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │  Store  │  │ Hotkeys │  │ Action Executor │ │
│  └────┬────┘  └────┬────┘  └────────┬────────┘ │
└───────┼────────────┼───────────────┼───────────┘
        │            │               │
        └────────────┼───────────────┘
                     │ IPC
        ┌────────────┴───────────────┐
        │      Renderer Process      │
        │  ┌──────────────────────┐  │
        │  │   React App (App.jsx) │  │
        │  └──────────────────────┘  │
        └────────────────────────────┘
\`\`\`

## Directory Structure

\`\`\`
src/
├── main/           # Electron main process
├── renderer/       # React application
├── shared-styles/  # CSS shared across windows
└── modal-apps/     # Standalone modal windows
\`\`\`

## Core Concepts

### [Concept 1: e.g., "Data Model"]

[Explain with examples]

### [Concept 2: e.g., "IPC Communication"]

[Explain with examples]

## Key Patterns

### [Pattern Name]

[When to use, how to implement, example code]

## Data Flow

[Describe how data moves through the system]

## Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `main.js` | Window lifecycle, app events |
| `store.js` | Data persistence |
| [etc.] |
```

### Key Principles

- **Diagrams over prose** - ASCII art is fine
- **Show, don't just tell** - Include code examples
- **Keep it high-level** - Implementation details belong in comments
- **Update incrementally** - Add sections as features are built

---

## ROADMAP.md

Track features, priorities, and project history.

### Template

```markdown
# Roadmap

## Current Sprint

### In Progress
- [ ] Feature being worked on

### Up Next
- [ ] Next priority item

## Backlog

### High Priority
- [ ] Important feature 1
- [ ] Important feature 2

### Medium Priority
- [ ] Nice-to-have 1

### Low Priority / Ideas
- [ ] Future consideration

## Completed

### v0.6.0 (2024-01-15)
- [x] Feature A
- [x] Feature B

### v0.5.0 (2024-01-01)
- [x] Feature C

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.6.0 | 2024-01-15 | Feature A, Feature B |
| 0.5.0 | 2024-01-01 | Feature C |

## Technical Debt & Refactoring

- [ ] Refactor X module
- [ ] Extract Y into separate file

## Known Issues

- Issue description (workaround if any)
```

### Key Principles

- **Current sprint at top** - Most important info first
- **Move, don't delete** - Completed items go to version sections
- **Date your completions** - Makes history searchable
- **Track tech debt** - Separate from features

---

## CHANGELOG.md

Record what changed for each release.

### Format

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature description

### Changed
- Modification to existing feature

### Fixed
- Bug fix description

### Removed
- Removed feature

## [0.6.0] - 2024-01-15

### Added
- Shortcuts.app integration with searchable picker
- Pop-out script editor with search/replace
- Delete action from context menu with confirmation

### Changed
- Type selector now uses visual icons instead of tabs
- Type is locked after action creation

### Fixed
- Child modal no longer closes parent modal
- Context menu delete confirmation now works correctly
```

### Categories

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Features to be removed in future
- **Removed** - Features removed in this release
- **Fixed** - Bug fixes
- **Security** - Vulnerability fixes

### Key Principles

- **User-focused** - Describe impact, not implementation
- **One line per change** - Brief but complete
- **Link to issues** - If using issue tracker
- **Unreleased section** - Accumulate changes during development

---

## Code Comments

### When to Comment

| Do Comment | Don't Comment |
|------------|---------------|
| Why something is done | What the code does (if clear) |
| Non-obvious gotchas | Every function |
| Complex algorithms | Simple operations |
| Workarounds and their reasons | Obvious variable names |
| External dependencies | Standard patterns |

### Comment Styles

```javascript
// Single line for brief notes

/*
 * Multi-line for longer explanations
 * that span multiple lines
 */

/**
 * JSDoc for public APIs and complex functions
 * @param {string} name - The action name
 * @returns {Object} The created action
 */

// ── Section Header ────────────────────────────────────
// Use for visual separation in long files

// TODO: Description of what needs to be done
// FIXME: Description of known issue
// HACK: Explanation of workaround
```

### JSDoc Usage

Use JSDoc for:
- Functions with non-obvious parameters
- Public APIs
- Complex return types

```javascript
/**
 * Executes an action with variable substitution
 * @param {Object} action - The action configuration
 * @param {string} action.type - Type: 'terminal', 'url', 'script', 'shortcut'
 * @param {string} action.command - The command/URL/script to execute
 * @param {Object.<string, string>} [variables={}] - Variables to substitute
 * @returns {Promise<{success: boolean, output?: string, error?: string}>}
 */
async function executeAction(action, variables = {}) { }
```

---

## README.md

For end users. Keep it practical.

### Template

```markdown
# Project Name

> One-line description

![Screenshot](screenshot.png)

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
# macOS
brew install project-name

# Or download from releases
\`\`\`

## Quick Start

1. Step one
2. Step two
3. Step three

## Usage

### Basic Usage

[Common use case with example]

### Advanced Usage

[Power user features]

## Configuration

[Settings and customization options]

## Development

\`\`\`bash
git clone [repo]
cd project-name
npm install
npm run dev
\`\`\`

## License

MIT
```

---

## Inline Documentation

### File Headers

Optional, but helpful for context:

```javascript
/**
 * HotkeyManager - Global keyboard shortcut registration
 *
 * Handles registering/unregistering Electron globalShortcuts,
 * conflict detection, and leader-key (listening mode) support.
 *
 * @module hotkey-manager
 */
```

### Complex Logic

Explain the algorithm, not line-by-line:

```javascript
// Luminance calculation for accessibility contrast checking
// Uses sRGB color space formula (WCAG 2.0)
// Returns value 0-1 where 0 is black, 1 is white
function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}
```

### Gotchas and Warnings

Make them obvious:

```javascript
// WARNING: globalShortcut.register() can throw if combo is invalid
// Always validate combo format before calling

// GOTCHA: Store writes are debounced (300ms). Don't rely on immediate persistence.

// NOTE: This runs in renderer process, not main. Use IPC for system operations.
```

---

## Keeping Docs Updated

### During Development

1. **Add to ROADMAP.md** when starting a feature
2. **Mark complete** when finishing
3. **Note gotchas** as you discover them
4. **Update ARCHITECTURE.md** for new patterns

### At Release

1. **Move Unreleased to version** in CHANGELOG.md
2. **Update version numbers** in package.json, ROADMAP.md
3. **Review CLAUDE.md** for accuracy
4. **Update README.md** screenshots if UI changed

### Periodic Review

- **Monthly**: Prune stale ROADMAP items
- **Per release**: Verify ARCHITECTURE.md accuracy
- **On breaking changes**: Update all docs comprehensively

---

## Writing Style

### Be Direct

```markdown
# Bad
It might be helpful to consider reading the architecture document before
attempting to make changes to the codebase.

# Good
Read ARCHITECTURE.md before making changes.
```

### Use Active Voice

```markdown
# Bad
The action is executed by the ActionExecutor.

# Good
ActionExecutor runs actions.
```

### Prefer Lists Over Paragraphs

```markdown
# Bad
The system supports four types of actions. Terminal actions run shell
commands. URL actions open links. Script actions execute multi-line
scripts. Shortcut actions run Apple Shortcuts.

# Good
Action types:
- **Terminal**: Shell commands
- **URL**: Open links
- **Script**: Multi-line scripts
- **Shortcut**: Apple Shortcuts
```

### Include Examples

```markdown
# Bad
Use the dispatch function to update state.

# Good
Update state via dispatch:
\`\`\`javascript
dispatch({ type: 'SET_CATEGORY', payload: categoryId });
\`\`\`
```

---

*Good documentation is invisible - it answers questions before they're asked.*
