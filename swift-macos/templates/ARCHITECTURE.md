# [PROJECT_NAME] - Architecture Guide

> **For LLM Sessions:** Read ROADMAP.md first for project overview. This document covers implementation details.

---

## Directory Structure

```
ProjectName/
├── App/
│   ├── ProjectNameApp.swift     # @main entry point
│   ├── AppDelegate.swift        # NSApplicationDelegate (if needed)
│   └── ContentView.swift        # Root view
│
├── Features/                    # Feature-based organization
│   ├── Actions/
│   │   ├── Views/
│   │   │   ├── ActionListView.swift
│   │   │   └── ActionItemView.swift
│   │   ├── ViewModels/
│   │   │   └── ActionListViewModel.swift
│   │   └── Models/
│   │       └── Action.swift
│   │
│   └── Settings/
│       ├── Views/
│       └── ViewModels/
│
├── Core/                        # Shared infrastructure
│   ├── Services/
│   │   ├── StorageService.swift
│   │   └── ExecutorService.swift
│   ├── Extensions/
│   │   └── View+Extensions.swift
│   └── Utilities/
│       └── ShellExecutor.swift
│
├── Resources/
│   ├── Assets.xcassets
│   └── Localizable.strings
│
└── Tests/
    └── ProjectNameTests/
```

---

## Architecture Layers

```
┌─────────────────────────────────────┐
│             Views (SwiftUI)          │
│    ContentView, FeatureView          │
└──────────────────┬──────────────────┘
                   │ @StateObject / @ObservedObject
┌──────────────────┴──────────────────┐
│          ViewModels (@MainActor)     │
│    FeatureViewModel                  │
└──────────────────┬──────────────────┘
                   │ async/await
┌──────────────────┴──────────────────┐
│           Services (Actors)          │
│   StorageService, ExecutorService    │
└──────────────────┬──────────────────┘
                   │
┌──────────────────┴──────────────────┐
│        System (Foundation/AppKit)    │
│   FileManager, Process, Keychain     │
└─────────────────────────────────────┘
```

---

## Data Flow

### State Management

```swift
// ViewModel pattern with ObservableObject
@MainActor
final class FeatureViewModel: ObservableObject {
    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false
    @Published var error: Error?

    private let storage: StorageService

    init(storage: StorageService = .shared) {
        self.storage = storage
    }

    func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await storage.load([Item].self)
        } catch {
            self.error = error
        }
    }
}
```

### View Integration

```swift
struct FeatureView: View {
    @StateObject private var viewModel = FeatureViewModel()

    var body: some View {
        List(viewModel.items) { item in
            ItemRow(item: item)
        }
        .task {
            await viewModel.load()
        }
    }
}
```

---

## Data Structures

### Models

```swift
struct Item: Identifiable, Codable {
    let id: String
    var name: String
    var createdAt: Date

    init(id: String = UUID().uuidString, name: String) {
        self.id = id
        self.name = name
        self.createdAt = Date()
    }
}
```

### Settings

```swift
struct Settings: Codable {
    var theme: Theme = .system
    var showInDock: Bool = false

    enum Theme: String, Codable {
        case light, dark, system
    }
}
```

---

## Key Patterns

### Actor for Thread Safety

```swift
actor StorageService {
    static let shared = StorageService()

    private var storageURL: URL {
        FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("ProjectName")
            .appendingPathComponent("data.json")
    }

    func load<T: Decodable>(_ type: T.Type) async throws -> T {
        let data = try Data(contentsOf: storageURL)
        return try JSONDecoder().decode(type, from: data)
    }

    func save<T: Encodable>(_ value: T) async throws {
        let data = try JSONEncoder().encode(value)
        try data.write(to: storageURL, options: .atomic)
    }
}
```

### Dependency Injection

```swift
// Protocol for testing
protocol StorageProviding {
    func load<T: Decodable>(_ type: T.Type) async throws -> T
    func save<T: Encodable>(_ value: T) async throws
}

// ViewModel accepts protocol
init(storage: StorageProviding = StorageService.shared) {
    self.storage = storage
}
```

---

## Adding New Features

### New View + ViewModel

1. Create model in `Features/[Feature]/Models/`
2. Create ViewModel in `Features/[Feature]/ViewModels/`
3. Create View in `Features/[Feature]/Views/`
4. Wire up in parent view with `@StateObject`

### New Service

1. Create actor in `Core/Services/`
2. Define protocol if testing needed
3. Add `static let shared` singleton
4. Inject into ViewModels

### New Setting

1. Add property to `Settings` struct
2. Add UI in SettingsView
3. Persist via StorageService

---

## Testing Checklist

Before shipping:

- [ ] Builds without warnings
- [ ] All tests pass
- [ ] Works in both light and dark mode
- [ ] Accessibility labels present
- [ ] Data persists across launches
- [ ] Memory: no leaks or retain cycles
