# Shared Design Methodology & Best Practices

> Universal principles that apply across all frameworks and platforms. Read this first, then dive into framework-specific guides.

---

## How This Repository Works

This repository contains design standards, coding conventions, and documentation templates organized by framework/platform:

```
design-standards/
├── SHARED.md              # You are here - universal principles
├── CODING_STANDARDS.md    # Universal coding standards (DRY, security, testing)
├── README.md              # Quick start and navigation
│
├── electron/              # Electron + React (JavaScript)
│   ├── CODING_STANDARDS.md
│   ├── STYLEGUIDE.md
│   ├── DOCUMENTATION_STANDARDS.md
│   └── templates/
│
├── swift-macos/           # Native Swift + SwiftUI
│   ├── CODING_STANDARDS.md
│   ├── STYLEGUIDE.md
│   ├── DOCUMENTATION_STANDARDS.md
│   └── templates/
│
└── self-preview/          # AI Agent Visual Feedback Pattern
    ├── SELF_PREVIEW.md
    ├── self_preview.py
    └── CLAUDE_SNIPPET.md
```

### Using in Your Project

**Option 1: Clone as submodule**
```bash
git submodule add git@github.com:avanrossum/design-standards.git docs/standards
```

**Option 2: Copy what you need**
```bash
# For an Electron project
cp -r design-standards/electron/* docs/

# For a Swift project
cp -r design-standards/swift-macos/* docs/
```

### Contributing Back

When you discover patterns worth standardizing:

```bash
cd docs/standards  # or wherever you cloned it
git add -A
git commit -m "Add: [pattern description]"
git push origin main
```

---

## Universal Design Principles

These principles apply regardless of framework or language.

### 1. Quiet Utility

The interface should feel purposeful, not decorative. Every element earns its place through function.

- **Density without clutter** - Pack information tightly but maintain breathing room
- **Immediate clarity** - State should be obvious at a glance
- **Responsive feedback** - Every interaction should feel acknowledged
- **Platform integration** - Look and feel native to the OS

### 2. Theme Adaptability

Both dark and light modes should feel intentional, not inverted.

- Dark mode is not just "invert colors"
- Light mode is not just "make everything white"
- Each theme should be designed as a first-class citizen
- Test both modes during development

### 3. Information Hierarchy

Use visual weight to guide attention:

1. **Primary** - Main content, actionable items
2. **Secondary** - Supporting information, labels
3. **Tertiary** - Hints, metadata, disabled states

This applies to both text and interactive elements.

---

## Universal Coding Principles

### Code for Humans First

```
# Bad - clever but unclear
const x = a ? b ? c : d : e;

# Good - explicit and readable
if (a) {
  return b ? c : d;
}
return e;
```

### Single Responsibility

Each function, class, or module should do one thing well.

```
# Bad - doing too much
async function loadAndValidateAndSaveUser(data) { }

# Good - focused
async function validateUser(data) { }
async function saveUser(data) { }
```

### Explicit Over Implicit

State your intentions clearly:

- Name functions with verbs that describe their action
- Name variables with nouns that describe their content
- Avoid abbreviations unless universally understood

### Error Handling is Not Optional

Every external operation can fail:

- Network requests
- File system operations
- User input parsing
- Database queries

Wrap them in try/catch (or equivalent) and handle failures gracefully.

### Comments Explain "Why", Not "What"

```
# Bad - restates the code
// Increment counter by 1
counter += 1;

# Good - explains the reasoning
// Counter starts at -1 to account for header row
counter += 1;
```

---

## Universal Documentation Standards

### Every Project Needs

| Document | Purpose | Primary Audience |
|----------|---------|------------------|
| `README.md` | What it is, how to use it | End users |
| `CLAUDE.md` | AI session context | Claude/AI tools |
| `ARCHITECTURE.md` | System design, patterns | Developers |
| `ROADMAP.md` | Features, priorities | Product/Dev team |
| `CHANGELOG.md` | What changed per version | Everyone |

### CLAUDE.md is Critical

For AI-assisted development, `CLAUDE.md` is the most important file:

- Front-load important information (context windows are limited)
- Be specific - use file paths, not vague descriptions
- Include gotchas - save future sessions from repeating mistakes
- Keep it current - update after significant sessions

### Documentation Style

1. **Be direct** - "Read this file" not "It might be helpful to consider reading this file"
2. **Use active voice** - "App saves data" not "Data is saved by the app"
3. **Prefer lists** - Scannable beats paragraphs
4. **Include examples** - Show, don't just tell

---

## Universal Git Conventions

### Commit Messages

```
<type>: <short description>

<optional body explaining why>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code change that neither fixes nor adds
- `docs` - Documentation only
- `style` - Formatting, no code change
- `test` - Adding tests
- `chore` - Build, tooling, dependencies

**Examples:**
```
feat: Add keyboard shortcut for quick search
fix: Prevent crash when file is missing
refactor: Extract validation into separate module
docs: Update installation instructions
```

### Branch Naming

```
feature/keyboard-shortcuts
fix/missing-file-crash
refactor/validation-module
```

---

## Platform-Agnostic Gotchas

### State Synchronization

After any mutation to persistent storage, refresh the UI state:

```javascript
// Electron/React
await electronAPI.saveData(data);
await refreshData();  // Re-sync React state
```

```swift
// Swift
await storage.save(data)
await viewModel.reload()  // Re-fetch from storage
```

### Theme Dual-Sync

When changing themes, update both:
1. The visual appearance (CSS variables, SwiftUI colorScheme)
2. The system-level setting (Electron nativeTheme, NSApp appearance)

### Window Close ≠ Quit

Menu bar apps should hide on close, not quit. Implement this intentionally.

### Debounced Persistence

Don't write to disk on every keystroke. Debounce saves (300ms is common).

---

## Adding a New Framework

When adding support for a new framework:

1. **Create directory**: `framework-name/`
2. **Adapt the three core docs**:
   - `CODING_STANDARDS.md` - Language idioms, patterns
   - `STYLEGUIDE.md` - UI conventions, native components
   - `DOCUMENTATION_STANDARDS.md` - Doc templates
3. **Create templates**: `templates/` with starter files
4. **Update this file**: Add to the directory structure above
5. **Update README.md**: Add to navigation

### Adaptation Guidelines

When adapting documents for a new framework:

- **Keep the structure** - Same sections, same order
- **Change the specifics** - Language syntax, framework patterns
- **Preserve the principles** - The "why" stays the same
- **Add platform gotchas** - Each platform has quirks

---

## Keeping Standards Fresh

### During Development

- Note patterns worth standardizing
- Document gotchas as you discover them
- Push improvements back to this repo

### Periodic Review

- **Weekly**: Check if project patterns should be upstream
- **Per release**: Review docs for accuracy
- **Quarterly**: Prune outdated patterns, add new ones

### When to Override Standards

Standards serve consistency, but aren't gospel. Override when:

- Platform conventions conflict (follow the platform)
- Performance requires it (document why)
- Team agreement exists (update the standard)

Never override silently - document the exception.

---

## Philosophy

> *"Consistency is a virtue, but not the only virtue."*

These standards exist to:
1. Reduce decision fatigue
2. Enable quick onboarding
3. Maintain quality across projects
4. Support AI-assisted development

They do NOT exist to:
1. Enforce rigid uniformity
2. Prevent innovation
3. Create bureaucracy
4. Slow down development

When standards get in the way of good work, update the standards.

---

*Standards evolve. Keep them fresh.*
