# App Archetypes

> Quiet Utility apps share a common design system (see STYLEGUIDE.md) but diverge in layout and interaction patterns based on their information architecture. This document defines the two archetypes.

---

## Archetype: Command Palette

**Example**: Actions

An app whose primary purpose is selecting and executing discrete operations. The UI is optimized for fast visual scanning and one-shot interaction.

### Characteristics

| Trait | Implementation |
|-------|---------------|
| Primary navigation | Visual category grid (icon + label buttons, 64-80px wide) |
| Content structure | Single selected item at a time, details in modals |
| Item layout | Icon circle (28px) anchors left, title + meta right |
| Editing model | Modal windows with their own drag region (28px) |
| List density | Medium — items are taller to accommodate drag handles and icon circles |
| State display | Inline status dots and badges per item |
| Drag & drop | Core interaction for reordering |

### Layout Skeleton

```
┌─ drag region (28px) ──────────────────┐
│  [category grid: scrollable row]      │
├───────────────────────────────────────┤
│  [item list: icon + title + status]   │
│  [item list: ...]                     │
├───────────────────────────────────────┤
│  [footer: metadata + actions]         │
└───────────────────────────────────────┘
```

### Unique Components

- **Fast Category Switcher** — Horizontal scrollable grid of icon buttons with 2px accent border on selection, `scale(1.05)` hover
- **Drag Handle** — Left-anchored grip icon for reorder
- **Icon Circle** — 28px round container with `bg-surface` background, 1px border
- **Modal Editor** — Separate frameless window for complex editing

---

## Archetype: Data List

**Example**: Panorasana

An app whose primary purpose is monitoring and browsing a large set of items. The UI is optimized for scanning, filtering, and drilling into detail without leaving context.

### Characteristics

| Trait | Implementation |
|-------|---------------|
| Primary navigation | Text tab bar with underline indicator |
| Content structure | Scrollable list with inline expansion |
| Item layout | Title + metadata row, action buttons right-aligned |
| Editing model | None — read-only with links to external editor |
| List density | High — items are compact, metadata stacks below title |
| State display | Left-border highlight + background tint for attention |
| Search/Filter | Dedicated toolbar: search input + sort dropdown |

### Layout Skeleton

```
┌─ drag region (38px) + title + actions ┐
│  [tab bar: text tabs, underline]      │
│  [search bar: icon + input]           │
│  [sort bar: label + select]           │
├───────────────────────────────────────┤
│  [item: title + meta | buttons]       │
│    └─ [expandable: comments/detail]   │
│  [item: ...]                          │
├───────────────────────────────────────┤
│  [status bar: dot + count | version]  │
└───────────────────────────────────────┘
```

### Unique Components

#### Tab Bar

Text-only tabs with a 2px bottom border accent indicator. No background fill on active.

```css
.tab-bar {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  padding: 0 12px;
  gap: 0;
}

.tab {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  border-bottom: 2px solid transparent;
  background: none;
}

.tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
```

#### Search Bar

Full-width input with an absolutely positioned icon. Sits between tab bar and list content.

```css
.search-bar {
  padding: 6px 12px;
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-input {
  width: 100%;
  padding: 6px 10px 6px 30px;  /* left padding for icon */
}
```

#### Sort Bar

Compact inline control. Label + native `<select>` at 11px.

```css
.sort-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 2px 12px 6px;
}

.sort-label {
  font-size: 11px;
  color: var(--text-muted);
}

.sort-select {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 3px;
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  color: var(--text-secondary);
}
```

#### Activity Highlight

A left-border accent + translucent background tint. Used to draw attention to items with new or unread content.

```css
/* Add to shared variables */
--highlight-bg: rgba(59, 130, 246, 0.15);
--highlight-border: rgba(59, 130, 246, 0.3);

.item.highlighted {
  border-left: 3px solid var(--accent);
  background: var(--highlight-bg);
}
```

The highlight is **not animated** — it appears and disappears instantly. This avoids distraction in a dense list where multiple items may highlight simultaneously.

#### Inline Expansion

Expandable detail section inside a list item. Uses a chevron rotation (0 to 90deg) as affordance.

```css
.expand-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  font-size: 12px;
  color: var(--text-secondary);
  background: none;
  cursor: pointer;
}

.expand-toggle-icon {
  transition: transform 0.15s ease;
}

.expand-toggle-icon.expanded {
  transform: rotate(90deg);
}

.expand-section {
  padding: 4px 10px 8px;
  max-height: 200px;
  overflow-y: auto;
  border-top: 1px solid var(--border-color);
}
```

#### Status Bar

Persistent footer showing app connection state and item count.

```css
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 12px;
  border-top: 1px solid var(--border-color);
  min-height: 26px;
  font-size: 11px;
  color: var(--text-muted);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.connected { background: var(--success); }
.status-dot.disconnected { background: var(--text-muted); }
```

#### Notification Badge

Small inline badge appended to a toggle button label.

```css
.badge {
  font-size: 9px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  background: var(--accent);
  color: #ffffff;
  margin-left: 4px;
}
```

#### Empty State

Centered placeholder shown when a list has no content. Includes optional CTA button.

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-state-icon { color: var(--text-muted); margin-bottom: 12px; }
.empty-state-title { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.empty-state-text { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.empty-state-btn {
  margin-top: 12px;
  background: var(--accent);
  color: #ffffff;
}
```

#### Helper Hints

Small muted text with optional links, placed below inputs to guide the user.

```css
.hint {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 6px;
}

.hint a {
  color: var(--accent);
  text-decoration: none;
}

.hint a:hover {
  text-decoration: underline;
}
```

---

## Shared Patterns

Both archetypes share the full design system from STYLEGUIDE.md:

- Color system (dark/light themes, 7 accent colors)
- Typography scale (13px body, 12px buttons, 11px metadata)
- 4px spacing rhythm
- Button variants (default, primary, danger, ghost)
- Input styling and focus states
- Scrollbar styling (6px, rounded)
- Drag region with `-webkit-app-region`
- Theme switching via `data-theme` / `data-accent` attributes
- Transition timing (0.15s hover, 0.1s press, 0.2s toggles)

---

## Choosing an Archetype

| If your app... | Use |
|----------------|-----|
| Executes discrete actions/commands | Command Palette |
| Displays a browsable dataset | Data List |
| Has few items but complex per-item editing | Command Palette |
| Has many items with light per-item detail | Data List |
| Needs drag-and-drop reordering | Command Palette |
| Needs search, sort, and filter | Data List |
| Opens modal editors for item configuration | Command Palette |
| Shows inline detail expansion | Data List |

Most apps clearly fit one archetype. If an app needs both (e.g. a list of automations with inline editors), lean toward Data List for the primary view and use modals for the editing flow.

---

*This document complements STYLEGUIDE.md. The style guide defines the design tokens and base components; this document defines how they assemble into application layouts.*
