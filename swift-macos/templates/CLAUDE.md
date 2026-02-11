# Claude Code Instructions for [PROJECT_NAME]

> **This file is for LLM sessions.** Quick context for working on this codebase.

## Session Start Checklist

1. Read `ROADMAP.md` - Current sprint and priorities
2. Read `ARCHITECTURE.md` - Patterns and structure
3. Check active tasks before making changes

## Quick Context

**[PROJECT_NAME]** is a [one-sentence description]. Built with Swift/SwiftUI for macOS.

### Key Files

| Purpose | File |
|---------|------|
| App entry | `ProjectName/App/ProjectNameApp.swift` |
| Main view | `ProjectName/App/ContentView.swift` |
| App delegate | `ProjectName/App/AppDelegate.swift` |
| Data persistence | `ProjectName/Core/Services/StorageService.swift` |

### Commands

```bash
# Build (Xcode)
xcodebuild -scheme ProjectName -configuration Debug build

# Run tests
xcodebuild test -scheme ProjectName

# Build for release
xcodebuild -scheme ProjectName -configuration Release archive
```

## Patterns to Follow

### State Management
```swift
// ViewModel for complex views
@MainActor
final class FeatureViewModel: ObservableObject {
    @Published private(set) var items: [Item] = []

    func load() async {
        items = try await service.loadItems()
    }
}
```

### Async Operations
```swift
// Always use async/await
func loadData() async throws -> [Action] {
    try await storage.load([Action].self)
}

// Launch from sync context
Task {
    await viewModel.load()
}
```

### New Service
1. Create actor in `Core/Services/`
2. Define protocol for testability
3. Inject into ViewModels

## Coding Standards

See `CODING_STANDARDS.md` for full conventions. Key points:

- **Swift 5.9+** - Modern Swift features
- **SwiftUI first** - AppKit when necessary
- **MVVM pattern** - ViewModels for complex views
- **Actors** - Thread-safe shared state
- **SF Symbols** - All icons

## Critical Gotchas

1. **@MainActor** - All UI updates must be on main actor
2. **Sandboxing** - App Store requires entitlements for file access
3. **Hardened Runtime** - Required for notarization
4. **NSApplicationDelegate** - Still needed for menu bar apps, global hotkeys

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
5. Leave codebase working
