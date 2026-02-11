# Coding Standards

> Conventions and patterns for native Swift macOS applications. Follow these when contributing or starting new projects.

---

## Language & Framework

- **Swift 5.9+** - Modern Swift with concurrency features
- **SwiftUI** - Declarative UI (fallback to AppKit when needed)
- **Swift Concurrency** - async/await, actors for thread safety
- **Combine** - For reactive data flow where appropriate
- **macOS 13+** - Target recent macOS versions

---

## File Organization

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Views | PascalCase | `ActionItemView.swift` |
| Models | PascalCase | `Action.swift` |
| ViewModels | PascalCase + VM | `ActionListViewModel.swift` |
| Services | PascalCase + Service | `StorageService.swift` |
| Extensions | Type+Feature | `String+Validation.swift` |
| Protocols | PascalCase + -able/-ing | `Runnable.swift`, `ActionExecuting.swift` |
| Test files | Type+Tests | `ActionTests.swift` |

### Directory Structure

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
│   │   └── HotkeyService.swift
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

### One Type Per File

Each struct, class, or enum gets its own file:

```swift
// Views/ActionItemView.swift
struct ActionItemView: View {
    let action: Action

    var body: some View {
        // ...
    }
}
```

---

## Swift Conventions

### Properties & Variables

```swift
// Properties: camelCase
let isLoading = false
var actionList: [Action] = []

// Constants: camelCase (Swift convention)
let maxRetryCount = 3
let defaultWindowWidth: CGFloat = 400

// Type constants: static let
struct Constants {
    static let animationDuration: TimeInterval = 0.15
    static let cornerRadius: CGFloat = 8
}

// Private properties: leading underscore not needed, use access control
private var internalState: Int = 0
```

### Functions & Methods

```swift
// Methods: camelCase, descriptive verbs
func handleClick() { }
func fetchActions() async throws -> [Action] { }
func saveToStore(_ action: Action) async { }

// Boolean getters: use is/has/can prefix
var isRunning: Bool { }
var hasChanges: Bool { }
func canExecute() -> Bool { }
```

### Access Control

Be explicit about access levels:

```swift
// Public API
public struct ActionExecutor {
    // Internal by default (within module)
    let store: StorageService

    // Explicitly private
    private var cache: [String: Action] = [:]

    // File-private for implementation details
    fileprivate func internalHelper() { }
}
```

### Error Handling

```swift
// Define domain-specific errors
enum ActionError: LocalizedError {
    case notFound(id: String)
    case executionFailed(reason: String)
    case invalidCommand

    var errorDescription: String? {
        switch self {
        case .notFound(let id):
            return "Action not found: \(id)"
        case .executionFailed(let reason):
            return "Execution failed: \(reason)"
        case .invalidCommand:
            return "Invalid command"
        }
    }
}

// Use Result type for synchronous operations
func validateAction(_ action: Action) -> Result<Action, ActionError> {
    guard !action.command.isEmpty else {
        return .failure(.invalidCommand)
    }
    return .success(action)
}

// Use async throws for asynchronous operations
func runAction(_ action: Action) async throws -> ActionResult {
    guard let command = action.command else {
        throw ActionError.invalidCommand
    }
    return try await executor.run(command)
}
```

---

## SwiftUI Patterns

### View Structure

```swift
struct ActionItemView: View {
    // MARK: - Properties
    let action: Action
    let onRun: () -> Void

    // MARK: - State
    @State private var isHovered = false
    @State private var isExpanded = false

    // MARK: - Environment
    @Environment(\.colorScheme) private var colorScheme

    // MARK: - Body
    var body: some View {
        HStack {
            actionIcon
            actionDetails
            Spacer()
            runButton
        }
        .padding(8)
        .background(backgroundColor)
        .cornerRadius(6)
    }

    // MARK: - Subviews
    private var actionIcon: some View {
        Image(systemName: action.iconName)
            .foregroundStyle(.secondary)
    }

    private var actionDetails: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(action.name)
                .font(.body)
            Text(action.command)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }

    private var runButton: some View {
        Button("Run", action: onRun)
            .buttonStyle(.bordered)
    }

    // MARK: - Computed Properties
    private var backgroundColor: Color {
        isHovered ? Color.secondary.opacity(0.1) : .clear
    }
}
```

### State Management

Use the appropriate property wrapper:

```swift
// Local view state
@State private var isLoading = false

// Binding from parent
@Binding var selectedId: String?

// Observable object (ViewModel)
@StateObject private var viewModel = ActionListViewModel()

// Observed object passed from parent
@ObservedObject var viewModel: ActionListViewModel

// Environment values
@Environment(\.dismiss) private var dismiss
@Environment(\.colorScheme) private var colorScheme

// App-wide state (iOS 17+ / macOS 14+)
@Observable class AppState {
    var actions: [Action] = []
    var settings: Settings = .default
}
```

### ViewModel Pattern

```swift
@MainActor
final class ActionListViewModel: ObservableObject {
    // MARK: - Published Properties
    @Published private(set) var actions: [Action] = []
    @Published private(set) var isLoading = false
    @Published var error: Error?

    // MARK: - Dependencies
    private let storageService: StorageService
    private let executor: ActionExecutor

    // MARK: - Init
    init(storageService: StorageService = .shared,
         executor: ActionExecutor = .shared) {
        self.storageService = storageService
        self.executor = executor
    }

    // MARK: - Actions
    func loadActions() async {
        isLoading = true
        defer { isLoading = false }

        do {
            actions = try await storageService.loadActions()
        } catch {
            self.error = error
        }
    }

    func runAction(_ action: Action) async {
        do {
            _ = try await executor.run(action)
        } catch {
            self.error = error
        }
    }
}
```

---

## AppKit Integration

When SwiftUI isn't sufficient, use AppKit:

### NSViewRepresentable

```swift
struct TerminalView: NSViewRepresentable {
    let output: String

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSScrollView()
        let textView = NSTextView()

        textView.isEditable = false
        textView.font = .monospacedSystemFont(ofSize: 12, weight: .regular)
        textView.backgroundColor = NSColor(Color.bgPrimary)

        scrollView.documentView = textView
        return scrollView
    }

    func updateNSView(_ scrollView: NSScrollView, context: Context) {
        guard let textView = scrollView.documentView as? NSTextView else { return }
        textView.string = output
    }
}
```

### Menu Bar Apps (NSStatusItem)

```swift
@main
struct MenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        Settings {
            SettingsView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?
    private var popover: NSPopover?

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusItem()
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)

        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "bolt.fill", accessibilityDescription: "Actions")
            button.action = #selector(togglePopover)
        }

        popover = NSPopover()
        popover?.contentViewController = NSHostingController(rootView: MainView())
        popover?.behavior = .transient
    }

    @objc private func togglePopover(_ sender: AnyObject?) {
        guard let button = statusItem?.button else { return }

        if let popover = popover, popover.isShown {
            popover.performClose(sender)
        } else {
            popover?.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
        }
    }
}
```

---

## Concurrency Patterns

### Async/Await

```swift
// Prefer async/await over completion handlers
func loadActions() async throws -> [Action] {
    let url = storageURL
    let data = try Data(contentsOf: url)
    return try JSONDecoder().decode([Action].self, from: data)
}

// Task for launching async work from sync context
func handleButtonTap() {
    Task {
        do {
            let actions = try await loadActions()
            self.actions = actions
        } catch {
            self.error = error
        }
    }
}
```

### Actors for Thread Safety

```swift
actor StorageActor {
    private var cache: [String: Action] = [:]

    func getAction(id: String) -> Action? {
        cache[id]
    }

    func setAction(_ action: Action) {
        cache[action.id] = action
    }

    func loadFromDisk() async throws {
        // File I/O happens on actor's executor
        let data = try Data(contentsOf: storageURL)
        let actions = try JSONDecoder().decode([Action].self, from: data)
        cache = Dictionary(uniqueKeysWithValues: actions.map { ($0.id, $0) })
    }
}
```

### MainActor for UI Updates

```swift
// Annotate entire class
@MainActor
final class ActionListViewModel: ObservableObject {
    @Published var actions: [Action] = []
}

// Or specific methods
func updateUI() async {
    let result = try await fetchData()
    await MainActor.run {
        self.data = result
    }
}
```

---

## Data Persistence

### UserDefaults for Settings

```swift
@propertyWrapper
struct UserDefault<Value> {
    let key: String
    let defaultValue: Value
    let container: UserDefaults = .standard

    var wrappedValue: Value {
        get {
            container.object(forKey: key) as? Value ?? defaultValue
        }
        set {
            container.set(newValue, forKey: key)
        }
    }
}

struct Settings {
    @UserDefault(key: "theme", defaultValue: "system")
    static var theme: String

    @UserDefault(key: "showInDock", defaultValue: false)
    static var showInDock: Bool
}
```

### File-Based Storage

```swift
actor StorageService {
    static let shared = StorageService()

    private var storageURL: URL {
        FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("AppName")
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

### Keychain for Secrets

```swift
import Security

struct KeychainService {
    static func save(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]

        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }

    static func load(key: String) throws -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess else {
            if status == errSecItemNotFound { return nil }
            throw KeychainError.loadFailed(status)
        }

        return result as? Data
    }
}
```

---

## Comments

### MARK Comments

Use MARK for code organization:

```swift
struct ActionItemView: View {
    // MARK: - Properties

    // MARK: - State

    // MARK: - Body

    // MARK: - Subviews

    // MARK: - Actions

    // MARK: - Private Methods
}
```

### Documentation Comments

```swift
/// Executes an action with optional variable substitution.
///
/// This method runs the action's command in a shell environment,
/// substituting any variables defined in the action.
///
/// - Parameters:
///   - action: The action configuration to execute.
///   - variables: Optional key-value pairs for variable substitution.
/// - Returns: The result of the action execution.
/// - Throws: `ActionError.executionFailed` if the command fails.
func execute(
    _ action: Action,
    variables: [String: String] = [:]
) async throws -> ActionResult {
    // Implementation
}
```

---

## Testing

### Unit Tests

```swift
import XCTest
@testable import ProjectName

final class ActionTests: XCTestCase {
    var sut: Action!

    override func setUp() {
        super.setUp()
        sut = Action(id: "test", name: "Test", command: "echo hello")
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func test_action_hasValidCommand() {
        XCTAssertFalse(sut.command.isEmpty)
    }

    func test_action_whenCommandEmpty_isInvalid() {
        sut = Action(id: "test", name: "Test", command: "")
        XCTAssertFalse(sut.isValid)
    }
}
```

### Async Tests

```swift
func test_loadActions_returnsStoredActions() async throws {
    // Given
    let mockStorage = MockStorageService()
    mockStorage.mockActions = [.sample]
    let viewModel = ActionListViewModel(storageService: mockStorage)

    // When
    await viewModel.loadActions()

    // Then
    XCTAssertEqual(viewModel.actions.count, 1)
    XCTAssertEqual(viewModel.actions.first?.id, Action.sample.id)
}
```

---

## Git Conventions

### Commit Messages

```
<type>: <short description>

<optional body explaining why>
```

Types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`

Examples:
```
feat: Add keyboard shortcut for running actions
fix: Prevent crash when action command is nil
refactor: Extract shell execution to dedicated service
docs: Update README with installation instructions
```

### Branch Naming

```
feature/keyboard-shortcuts
fix/nil-command-crash
refactor/shell-service
```

---

*Keep code simple, direct, and Swift-idiomatic. When in doubt, follow Apple's API Design Guidelines.*
