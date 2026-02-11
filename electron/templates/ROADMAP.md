# [PROJECT_NAME] - Project Roadmap

> **For LLM Sessions:** This document is the source of truth for the project. Start here to understand the application, then consult ARCHITECTURE.md for implementation details.

## Quick Start for New Sessions

1. **Read this file first** - Understand what the app does and current priorities
2. **Read ARCHITECTURE.md** - Understand the codebase structure and patterns
3. **Check the Current Sprint** section below for active work

---

## What is [PROJECT_NAME]?

**[PROJECT_NAME]** is a [description of what the app does].

### Core Features
- **Feature 1** - Description
- **Feature 2** - Description
- **Feature 3** - Description

---

## Current Sprint

### In Progress
- [ ] Current feature being worked on

### Up Next
- [ ] Next priority item

### Done
- [x] Recently completed item

---

## Feature Backlog

### High Priority
- [ ] Important feature 1
- [ ] Important feature 2

### Medium Priority
- [ ] Nice-to-have 1
- [ ] Nice-to-have 2

### Low Priority / Ideas
- [ ] Future consideration 1
- [ ] Future consideration 2

---

## Technical Debt & Refactoring

- [ ] Refactor X for clarity
- [ ] Extract Y into separate module

---

## Gotchas and Known Issues

### Critical

1. **[Issue Name]**
   - Description of the issue
   - Workaround if any

### Development

1. **[Dev gotcha]**
   - Description
   - How to handle

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Electron |
| Frontend | React |
| Build | Vite |
| State | React Context + useReducer |
| Storage | JSON file in userData |
| Styling | CSS Variables |

---

## Commands Reference

```bash
# Development
npm run dev              # Start dev server + Electron

# Build
npm run build            # Full production build
```

---

## Version History

### v0.1.0 (Current)
- Initial release
- Feature list

---

## Contributing

See ARCHITECTURE.md for codebase structure and patterns.
See the Gotchas section above before making changes.

When adding features:
1. Update this ROADMAP.md to reflect changes
2. Add entry to CHANGELOG.md
3. Keep components focused and single-purpose
4. Follow existing IPC patterns
5. Test on both dev and production builds
