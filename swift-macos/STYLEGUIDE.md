# Design System & Style Guide

> A comprehensive design system for native Swift macOS applications with an Apple-native aesthetic.

---

## Design Philosophy

**"Native & Intentional"** - The interface should feel like a first-party Apple application. Leverage system components, respect platform conventions, and only customize where it adds genuine value.

### Core Principles

1. **System-first** - Use SF Symbols, system colors, and native controls whenever possible
2. **Adaptive** - Respect light/dark mode, accessibility settings, and accent colors
3. **Density-aware** - Match the information density users expect from macOS
4. **Responsive feedback** - Every interaction should feel acknowledged
5. **Consistency** - Match Apple's Human Interface Guidelines

---

## Color System

### System Colors (Preferred)

Always prefer system semantic colors - they automatically adapt to light/dark mode:

```swift
// Backgrounds
Color.primary           // Main content
Color.secondary         // Secondary content
Color(nsColor: .windowBackgroundColor)
Color(nsColor: .controlBackgroundColor)
Color(nsColor: .textBackgroundColor)

// Text
Color.primary           // Main text (auto-adapts)
Color.secondary         // Secondary text
Color(nsColor: .labelColor)
Color(nsColor: .secondaryLabelColor)
Color(nsColor: .tertiaryLabelColor)
Color(nsColor: .quaternaryLabelColor)

// Semantic
Color.accentColor       // User's accent color
Color.red              // Errors, destructive
Color.green            // Success
Color.yellow           // Warnings
Color.blue             // Links, primary actions
```

### Custom Colors (When Needed)

If you must define custom colors, provide both appearances:

```swift
extension Color {
    static let bgPrimary = Color("BGPrimary")    // In Assets.xcassets
    static let bgSurface = Color("BGSurface")
    static let bgElevated = Color("BGElevated")
}
```

In Assets.xcassets, define both Any Appearance and Dark Appearance:

| Token | Light | Dark |
|-------|-------|------|
| bgPrimary | `#F5F5F7` | `#1A1D23` |
| bgSurface | `#FFFFFF` | `#242830` |
| bgElevated | `#FFFFFF` | `#2A2E38` |
| bgHover | `#EEEEF0` | `#2E3340` |

### Accent Colors

Respect the user's system accent color:

```swift
// Use system accent
Color.accentColor

// Or define your own that adapts
Button("Primary Action") { }
    .buttonStyle(.borderedProminent)  // Uses accent color automatically
```

---

## Typography

### System Fonts

Always use the system font for UI:

```swift
// Standard hierarchy
.font(.largeTitle)      // 26pt
.font(.title)           // 22pt
.font(.title2)          // 17pt
.font(.title3)          // 15pt
.font(.headline)        // 13pt semibold
.font(.body)            // 13pt
.font(.callout)         // 12pt
.font(.subheadline)     // 11pt
.font(.footnote)        // 10pt
.font(.caption)         // 10pt
.font(.caption2)        // 10pt light

// Monospace for code/commands
.font(.system(.body, design: .monospaced))
Font.custom("SF Mono", size: 12)
```

### Text Styles

```swift
// Primary content
Text("Action Name")
    .font(.body)
    .foregroundStyle(.primary)

// Secondary content
Text("Last run: 5 min ago")
    .font(.caption)
    .foregroundStyle(.secondary)

// Muted/hint
Text("⌘K to search")
    .font(.caption2)
    .foregroundStyle(.tertiary)

// Section headers (uppercase)
Text("SETTINGS")
    .font(.caption)
    .fontWeight(.medium)
    .foregroundStyle(.secondary)
    .textCase(.uppercase)
    .tracking(0.5)
```

---

## Spacing & Layout

### System Spacing

Use SwiftUI's built-in spacing:

```swift
VStack(spacing: 8) { }    // Standard
VStack(spacing: 4) { }    // Tight
VStack(spacing: 12) { }   // Relaxed
VStack(spacing: 16) { }   // Section breaks

HStack(spacing: 6) { }    // Icon + text
HStack(spacing: 8) { }    // Standard
HStack(spacing: 12) { }   // Button groups
```

### Padding

```swift
.padding(4)      // Tight (icons)
.padding(6)      // Form elements
.padding(8)      // Standard
.padding(12)     // Cards
.padding(16)     // Modal content
.padding(20)     // Window margins

// Directional
.padding(.horizontal, 12)
.padding(.vertical, 8)
.padding(.leading, 16)
```

### Safe Areas

Always respect safe areas and toolbar space:

```swift
ScrollView {
    content
}
.safeAreaInset(edge: .bottom) {
    toolbar
}
```

---

## Components

### Buttons

Use system button styles:

```swift
// Primary action
Button("Save") { }
    .buttonStyle(.borderedProminent)

// Secondary action
Button("Cancel") { }
    .buttonStyle(.bordered)

// Tertiary/text
Button("Learn More") { }
    .buttonStyle(.plain)
    .foregroundStyle(.secondary)

// Destructive
Button("Delete", role: .destructive) { }
    .buttonStyle(.bordered)

// Icon button
Button { } label: {
    Image(systemName: "gear")
}
.buttonStyle(.borderless)
```

### Custom Icon Buttons

```swift
struct IconButton: View {
    let systemName: String
    let action: () -> Void

    @State private var isHovered = false

    var body: some View {
        Button(action: action) {
            Image(systemName: systemName)
                .font(.system(size: 14))
                .foregroundStyle(isHovered ? .primary : .secondary)
                .frame(width: 26, height: 26)
                .background(
                    RoundedRectangle(cornerRadius: 4)
                        .fill(isHovered ? Color.secondary.opacity(0.1) : .clear)
                )
        }
        .buttonStyle(.plain)
        .onHover { isHovered = $0 }
    }
}
```

### Text Fields

```swift
// Standard
TextField("Name", text: $name)
    .textFieldStyle(.roundedBorder)

// With prompt
TextField("Enter command", text: $command, prompt: Text("echo 'hello'"))

// Secure
SecureField("Password", text: $password)

// Multiline
TextEditor(text: $script)
    .font(.system(.body, design: .monospaced))
    .scrollContentBackground(.hidden)
    .background(Color(nsColor: .textBackgroundColor))
    .cornerRadius(4)
    .overlay(
        RoundedRectangle(cornerRadius: 4)
            .stroke(Color(nsColor: .separatorColor), lineWidth: 1)
    )
```

### Form Controls

```swift
Form {
    Section("General") {
        TextField("Name", text: $name)

        Picker("Type", selection: $type) {
            ForEach(ActionType.allCases) { type in
                Text(type.displayName).tag(type)
            }
        }

        Toggle("Run in background", isOn: $runInBackground)
    }

    Section("Schedule") {
        DatePicker("Run at", selection: $runDate)
    }
}
.formStyle(.grouped)
```

### Lists

```swift
List(selection: $selectedId) {
    ForEach(actions) { action in
        ActionRowView(action: action)
    }
}
.listStyle(.sidebar)          // Sidebar navigation
.listStyle(.inset)            // Content list
.listStyle(.plain)            // No background

// Custom row
struct ActionRowView: View {
    let action: Action
    @State private var isHovered = false

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: action.iconName)
                .foregroundStyle(.secondary)

            VStack(alignment: .leading, spacing: 2) {
                Text(action.name)
                    .font(.body)
                Text(action.command)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }

            Spacer()

            if action.isRunning {
                ProgressView()
                    .scaleEffect(0.6)
            }
        }
        .padding(.vertical, 4)
        .padding(.horizontal, 8)
        .background(
            RoundedRectangle(cornerRadius: 6)
                .fill(isHovered ? Color.secondary.opacity(0.1) : .clear)
        )
        .onHover { isHovered = $0 }
    }
}
```

### Segmented Controls

```swift
Picker("View", selection: $viewMode) {
    Text("List").tag(ViewMode.list)
    Text("Grid").tag(ViewMode.grid)
    Text("Compact").tag(ViewMode.compact)
}
.pickerStyle(.segmented)
.frame(width: 200)
```

### Toggle Switches

```swift
Toggle("Enable feature", isOn: $isEnabled)
    .toggleStyle(.switch)      // macOS switch style

// Custom toggle
Toggle(isOn: $isEnabled) {
    Label("Notifications", systemImage: "bell")
}
```

---

## Status Indicators

### Progress

```swift
// Indeterminate
ProgressView()
    .scaleEffect(0.8)

// Determinate
ProgressView(value: progress, total: 1.0)
    .progressViewStyle(.linear)

// With label
ProgressView("Loading...", value: progress, total: 1.0)
```

### Badges

```swift
Text("PRO")
    .font(.caption2)
    .fontWeight(.semibold)
    .textCase(.uppercase)
    .padding(.horizontal, 6)
    .padding(.vertical, 2)
    .background(Color.accentColor)
    .foregroundStyle(.white)
    .clipShape(Capsule())
```

### Status Dots

```swift
Circle()
    .fill(status.color)
    .frame(width: 6, height: 6)

// Animated for running state
Circle()
    .fill(Color.yellow)
    .frame(width: 6, height: 6)
    .opacity(isPulsing ? 0.4 : 1.0)
    .animation(.easeInOut(duration: 0.8).repeatForever(), value: isPulsing)
```

### Keyboard Hints

```swift
Text("⌘K")
    .font(.caption)
    .foregroundStyle(.secondary)
    .padding(.horizontal, 4)
    .padding(.vertical, 2)
    .background(Color(nsColor: .quaternaryLabelColor).opacity(0.5))
    .cornerRadius(3)
```

---

## Animations

### Timing

```swift
.animation(.easeInOut(duration: 0.15), value: state)  // Hover
.animation(.easeInOut(duration: 0.2), value: state)   // Transitions
.animation(.spring(response: 0.3), value: state)       // Interactive
```

### Common Patterns

```swift
// Hover effect
.scaleEffect(isHovered ? 1.02 : 1.0)
.animation(.easeInOut(duration: 0.1), value: isHovered)

// Button press
.scaleEffect(isPressed ? 0.98 : 1.0)

// Rotation (expand icon)
Image(systemName: "chevron.right")
    .rotationEffect(.degrees(isExpanded ? 90 : 0))
    .animation(.easeInOut(duration: 0.15), value: isExpanded)

// Opacity transition
.opacity(isVisible ? 1 : 0)
.animation(.easeInOut(duration: 0.2), value: isVisible)
```

### Transitions

```swift
if isShowing {
    ContentView()
        .transition(.opacity)
        .transition(.move(edge: .bottom))
        .transition(.scale.combined(with: .opacity))
}
```

---

## Icons

### SF Symbols (Required)

Always use SF Symbols for icons:

```swift
Image(systemName: "play.fill")
Image(systemName: "gear")
Image(systemName: "terminal")
Image(systemName: "link")
Image(systemName: "clock")

// With rendering mode
Image(systemName: "checkmark.circle.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.green)

// Variable symbols
Image(systemName: "speaker.wave.3.fill", variableValue: volume)
```

### Icon Sizes

```swift
.font(.system(size: 12))   // Small inline
.font(.system(size: 14))   // Standard
.font(.system(size: 16))   // Emphasized
.font(.system(size: 20))   // Headers
.font(.system(size: 32))   // Feature icons
```

### Icon + Text

```swift
Label("Settings", systemImage: "gear")
    .labelStyle(.titleAndIcon)

// Or manual for more control
HStack(spacing: 6) {
    Image(systemName: "gear")
        .foregroundStyle(.secondary)
    Text("Settings")
}
```

---

## Windows & Sheets

### Window Styling

```swift
WindowGroup {
    ContentView()
}
.windowStyle(.hiddenTitleBar)              // Minimal chrome
.windowToolbarStyle(.unified)               // Modern toolbar
.windowToolbarStyle(.unifiedCompact)        // Compact toolbar
```

### Sheets & Popovers

```swift
.sheet(isPresented: $showSettings) {
    SettingsView()
        .frame(width: 400, height: 300)
}

.popover(isPresented: $showPopover) {
    PopoverContent()
        .padding()
}

// Confirmation dialog
.confirmationDialog("Delete Action?", isPresented: $showDelete) {
    Button("Delete", role: .destructive) { deleteAction() }
    Button("Cancel", role: .cancel) { }
}
```

### Alerts

```swift
.alert("Error", isPresented: $showError) {
    Button("OK", role: .cancel) { }
} message: {
    Text(errorMessage)
}
```

---

## Menu Bar Apps

### Popover Sizing

```swift
struct MenuBarPopover: View {
    var body: some View {
        VStack(spacing: 0) {
            header
            Divider()
            content
            Divider()
            footer
        }
        .frame(width: 300, height: 400)
    }
}
```

### MenuBarExtra (macOS 13+)

```swift
@main
struct MenuBarApp: App {
    var body: some Scene {
        MenuBarExtra("Actions", systemImage: "bolt.fill") {
            MenuBarView()
        }
        .menuBarExtraStyle(.window)  // Popover style
    }
}
```

---

## Scrollbars

```swift
ScrollView {
    content
}
.scrollIndicators(.visible, axes: .vertical)
.scrollIndicators(.hidden)   // Hide scrollbars
```

---

## Accessibility

### Always Include

```swift
Image(systemName: "play.fill")
    .accessibilityLabel("Run action")

Button { } label: {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete action")
.accessibilityHint("Permanently removes this action")
```

### Dynamic Type

```swift
// Use system fonts - they scale automatically
.font(.body)

// If using fixed sizes, allow scaling
@ScaledMetric var iconSize: CGFloat = 16
```

### High Contrast

System colors automatically adapt to high contrast settings.

---

## Window Backgrounds

### Matching AppKit

```swift
// Main window background
Color(nsColor: .windowBackgroundColor)

// Sidebar
Color(nsColor: .controlBackgroundColor)

// Content area
Color(nsColor: .textBackgroundColor)
```

### Vibrancy

```swift
.background(.ultraThinMaterial)
.background(.regularMaterial)
.background(.thickMaterial)
```

---

## Do's and Don'ts

### Do

- Use SF Symbols for all icons
- Respect system accent color
- Support both light and dark mode
- Use semantic colors (`.primary`, `.secondary`)
- Follow Apple's Human Interface Guidelines
- Test with accessibility settings (VoiceOver, high contrast)
- Use native controls when available

### Don't

- Create custom icons when SF Symbols exist
- Hardcode colors - use system colors
- Ignore safe areas
- Skip accessibility labels
- Use overly long animations (keep under 0.3s)
- Reinvent standard controls
- Mix design languages (iOS patterns on macOS)

---

## Quick Reference

### Color Hierarchy

1. `Color.accentColor` - Primary action
2. `Color.primary` - Main content
3. `Color.secondary` - Secondary content
4. `Color.tertiary` - Hints, disabled

### Font Hierarchy

1. `.title` / `.title2` - Section headers
2. `.headline` - Emphasized content
3. `.body` - Main content
4. `.caption` / `.caption2` - Metadata, hints

### Spacing Hierarchy

1. `4` - Tight (icon gaps)
2. `8` - Standard
3. `12` - Relaxed (sections)
4. `16`+ - Major breaks, window margins

---

*When in doubt, reference Apple's apps. Native feels familiar.*
