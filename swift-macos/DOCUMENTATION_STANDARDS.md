# Documentation Standards

> How to document native Swift macOS codebases. Practical guidelines for maintainable docs.

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

**[Project Name]** is a [one-sentence description]. Built with Swift/SwiftUI for macOS.

### Key Files

| Purpose | File |
|---------|------|
| App entry | `ProjectName/App/ProjectNameApp.swift` |
| Main view | `ProjectName/App/ContentView.swift` |
| Data layer | `ProjectName/Core/Services/StorageService.swift` |
| App delegate | `ProjectName/App/AppDelegate.swift` |

### Commands

\`\`\`bash
# Build
xcodebuild -scheme ProjectName -configuration Debug build

# Run tests
xcodebuild test -scheme ProjectName
\`\`\`

## Patterns to Follow

### State Management
\`\`\`swift
// Observable for shared state
@Observable class AppState {
    var actions: [Action] = []
}

// ViewModel for complex views
@MainActor
class ActionListViewModel: ObservableObject {
    @Published var items: [Action] = []
}
\`\`\`

### Async Operations
\`\`\`swift
// Always use async/await
func loadData() async throws -> [Action] { }

// Update UI on main actor
await MainActor.run { self.items = result }
\`\`\`

## Coding Standards

See `CODING_STANDARDS.md` for full conventions. Key points:

- **Swift 5.9+** - Modern Swift features
- **SwiftUI first** - AppKit when necessary
- **MVVM pattern** - ViewModels for complex views
- **Actors** - For thread-safe shared state

## Critical Gotchas

1. **@MainActor** - All UI updates must happen on main actor
2. **Sandboxing** - App Store requires sandbox; file access is restricted
3. **Hardened Runtime** - Required for notarization; affects script execution
4. **MenuBarExtra** - Requires macOS 13+ for SwiftUI-native menu bar apps

## Documentation Updates

When making changes:
- Update `ROADMAP.md` if adding/completing features
- Update `ARCHITECTURE.md` if changing patterns
- Update `CHANGELOG.md` for releases

## Session End Checklist

1. Ensure changes compile without warnings
2. Run tests
3. Update ROADMAP.md if tasks completed
4. Document new gotchas
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
# [PROJECT_NAME] - Architecture Guide

> **For LLM Sessions:** Read ROADMAP.md first for project overview.

---

## Directory Structure

\`\`\`
ProjectName/
├── App/
│   ├── ProjectNameApp.swift     # @main entry
│   ├── AppDelegate.swift        # NSApplicationDelegate
│   └── ContentView.swift        # Root view
│
├── Features/
│   ├── Actions/
│   │   ├── Views/               # SwiftUI views
│   │   ├── ViewModels/          # Observable view models
│   │   └── Models/              # Data models
│   └── Settings/
│
├── Core/
│   ├── Services/                # Business logic
│   ├── Extensions/              # Swift extensions
│   └── Utilities/               # Helper functions
│
└── Resources/
    ├── Assets.xcassets
    └── Localizable.strings
\`\`\`

---

## Architecture Layers

\`\`\`
┌─────────────────────────────────────┐
│             Views (SwiftUI)          │
│    ContentView, ActionListView       │
└──────────────────┬──────────────────┘
                   │ @StateObject / @ObservedObject
┌──────────────────┴──────────────────┐
│          ViewModels (MVVM)           │
│    ActionListViewModel, etc.         │
└──────────────────┬──────────────────┘
                   │ async/await
┌──────────────────┴──────────────────┐
│           Services (Actors)          │
│   StorageService, ExecutorService    │
└──────────────────┬──────────────────┘
                   │
┌──────────────────┴──────────────────┐
│          System (AppKit/Foundation)  │
│   FileManager, Process, Keychain     │
└─────────────────────────────────────┘
\`\`\`

---

## Data Flow

### State Management

\`\`\`swift
// App-wide state using @Observable (macOS 14+)
@Observable class AppState {
    var actions: [Action] = []
    var settings: Settings = .default
}

// Or ObservableObject for macOS 13
@MainActor
class AppState: ObservableObject {
    @Published var actions: [Action] = []
}
\`\`\`

### ViewModel Pattern

\`\`\`swift
@MainActor
final class ActionListViewModel: ObservableObject {
    @Published private(set) var actions: [Action] = []
    @Published var error: Error?

    private let storage: StorageService

    func loadActions() async {
        do {
            actions = try await storage.loadActions()
        } catch {
            self.error = error
        }
    }
}
\`\`\`

---

## Key Patterns

### Dependency Injection

\`\`\`swift
// Protocol for testability
protocol StorageProviding {
    func load<T: Decodable>(_ type: T.Type) async throws -> T
    func save<T: Encodable>(_ value: T) async throws
}

// Concrete implementation
actor StorageService: StorageProviding { }

// In ViewModel
init(storage: StorageProviding = StorageService.shared) {
    self.storage = storage
}
\`\`\`

### Actor Isolation

\`\`\`swift
// Thread-safe service
actor ExecutorService {
    func run(_ command: String) async throws -> String { }
}

// Access from main actor
let result = try await executorService.run(command)
\`\`\`

---

## Adding New Features

### New View + ViewModel

1. Create model in `Features/[Feature]/Models/`
2. Create ViewModel in `Features/[Feature]/ViewModels/`
3. Create View in `Features/[Feature]/Views/`
4. Wire up in parent view

### New Service

1. Create actor in `Core/Services/`
2. Define protocol if needed for testing
3. Inject into ViewModels that need it
```

---

## ROADMAP.md

Track features, priorities, and project history.

### Template

```markdown
# [PROJECT_NAME] - Project Roadmap

> **For LLM Sessions:** Start here. Understand what the app does, then check ARCHITECTURE.md.

---

## What is [PROJECT_NAME]?

**[PROJECT_NAME]** is a [description].

### Core Features
- **Feature 1** - Description
- **Feature 2** - Description

---

## Current Sprint

### In Progress
- [ ] Current feature

### Up Next
- [ ] Next priority

### Done
- [x] Recently completed

---

## Feature Backlog

### High Priority
- [ ] Important feature 1

### Medium Priority
- [ ] Nice-to-have 1

### Low Priority / Ideas
- [ ] Future consideration

---

## Technical Debt

- [ ] Refactor X
- [ ] Add tests for Y

---

## Gotchas

### Platform
1. **Sandboxing** - File access requires entitlements
2. **Notarization** - Hardened runtime required

### Development
1. **SwiftUI previews** - May fail with certain AppKit integrations

---

## Version History

### v1.0.0 (Current)
- Initial release

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Swift 5.9+ |
| UI | SwiftUI |
| Fallback | AppKit |
| Target | macOS 13+ |
| Build | Xcode 15+ |
```

---

## CHANGELOG.md

Use [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature

### Changed
- Modification

### Fixed
- Bug fix

---

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Feature list
```

---

## Code Comments

### Swift Documentation Comments

```swift
/// Executes an action with optional variable substitution.
///
/// This method runs the action's command in a shell environment.
///
/// - Parameters:
///   - action: The action to execute.
///   - variables: Key-value pairs for substitution.
/// - Returns: The execution result.
/// - Throws: `ActionError.executionFailed` if the command fails.
/// - Note: Commands run in the user's default shell.
/// - Warning: Long-running commands may block.
func execute(
    _ action: Action,
    variables: [String: String] = [:]
) async throws -> ActionResult
```

### MARK Comments

```swift
struct ActionListView: View {
    // MARK: - Properties

    // MARK: - State

    // MARK: - Body

    // MARK: - Subviews

    // MARK: - Private Methods
}
```

### Warning Comments

```swift
// FIXME: This crashes on macOS 12
// TODO: Add caching
// MARK: - Deprecated
// WARNING: Not thread-safe, use actor instead
```

---

## README.md Template

```markdown
# Project Name

> One-line description

![Screenshot](screenshot.png)

## Features

- Feature 1
- Feature 2

## Requirements

- macOS 13+
- Xcode 15+ (for building)

## Installation

### Download
Download the latest release from [Releases](link).

### Homebrew (if applicable)
\`\`\`bash
brew install --cask project-name
\`\`\`

## Quick Start

1. Launch the app
2. Step two
3. Step three

## Development

\`\`\`bash
git clone [repo]
cd project-name
open ProjectName.xcodeproj
\`\`\`

### Building

\`\`\`bash
xcodebuild -scheme ProjectName -configuration Release build
\`\`\`

### Testing

\`\`\`bash
xcodebuild test -scheme ProjectName
\`\`\`

## License

MIT
```

---

## Writing Style

### Be Direct

```markdown
# Bad
It might be helpful to consider using actors for thread safety.

# Good
Use actors for thread safety.
```

### Use Active Voice

```markdown
# Bad
The action is executed by the ExecutorService.

# Good
ExecutorService runs actions.
```

### Prefer Lists

```markdown
# Bad
The system supports three action types. Terminal runs shell commands.
URL opens links. Script executes multi-line scripts.

# Good
Action types:
- **Terminal** - Shell commands
- **URL** - Open links
- **Script** - Multi-line scripts
```

### Include Examples

```markdown
# Bad
Use async/await for asynchronous operations.

# Good
Use async/await:
\`\`\`swift
func loadActions() async throws -> [Action] {
    try await storage.load([Action].self)
}
\`\`\`
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
2. **Update version** in project settings
3. **Review CLAUDE.md** for accuracy
4. **Update screenshots** if UI changed

### Periodic Review

- **Monthly**: Prune stale ROADMAP items
- **Per release**: Verify ARCHITECTURE.md accuracy
- **On breaking changes**: Update all docs

---

*Good documentation is invisible - it answers questions before they're asked.*
