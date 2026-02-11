# [PROJECT_NAME] - Project Roadmap

> **For LLM Sessions:** This is the source of truth. Start here, then check ARCHITECTURE.md.

---

## Quick Start for New Sessions

1. **Read this file first** - Understand the app and priorities
2. **Read ARCHITECTURE.md** - Understand code patterns
3. **Check Current Sprint** - See active work

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

- [ ] Add unit tests for services
- [ ] Refactor X for clarity

---

## Gotchas and Known Issues

### Platform

1. **Sandboxing**
   - App Store requires sandbox entitlements
   - File access needs explicit permissions

2. **Notarization**
   - Hardened runtime required
   - Some shell operations may be restricted

### Development

1. **SwiftUI Previews**
   - May fail with AppKit integrations
   - Use `#if DEBUG` for preview-specific code

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Swift 5.9+ |
| UI Framework | SwiftUI |
| Fallback UI | AppKit |
| Target | macOS 13+ |
| Build | Xcode 15+ |
| State | ObservableObject / @Observable |
| Persistence | JSON / UserDefaults |

---

## Commands Reference

```bash
# Development (Xcode)
# Open project and press ⌘R

# Build from command line
xcodebuild -scheme ProjectName -configuration Debug build

# Run tests
xcodebuild test -scheme ProjectName

# Archive for release
xcodebuild -scheme ProjectName -configuration Release archive
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- Core feature list

---

## Contributing

See ARCHITECTURE.md for codebase structure.
See CODING_STANDARDS.md for code conventions.

When adding features:
1. Update this ROADMAP.md
2. Add entry to CHANGELOG.md
3. Follow MVVM pattern
4. Add tests for business logic
5. Test on both Intel and Apple Silicon
