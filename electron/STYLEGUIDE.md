# Design System & Style Guide

> A comprehensive design system for Electron + React macOS applications with a native, utilitarian aesthetic.

---

## Design Philosophy

**"Quiet Utility"** - The interface should feel native to macOS while being distinctly purposeful. Every element earns its place through function, not decoration.

### Core Principles

1. **Density without clutter** - Pack information tightly but maintain breathing room
2. **Immediate clarity** - State should be obvious at a glance (colors, badges, dots)
3. **Responsive feedback** - Every interaction should feel acknowledged (hover states, transitions, active states)
4. **System integration** - Look and feel like a first-party macOS utility
5. **Theme adaptability** - Dark and light modes should feel equally intentional, not inverted

---

## Color System

### Dark Theme (Primary)

```css
/* Backgrounds - Layer system from darkest to lightest */
--bg-primary: #1a1d23;     /* App background, deepest layer */
--bg-surface: #242830;     /* Cards, panels, elevated content */
--bg-elevated: #2a2e38;    /* Hover states on surfaces */
--bg-hover: #2e3340;       /* Interactive hover states */

/* Borders */
--border-color: #2e3340;   /* Subtle, same as hover for cohesion */

/* Text - Three-tier hierarchy */
--text-primary: #e8e8e8;   /* Main content, headings */
--text-secondary: #8890a0; /* Labels, metadata */
--text-muted: #5a6070;     /* Hints, timestamps, disabled */

/* Semantic Colors */
--success: #4caf50;        /* Green - success states */
--warning: #f59e0b;        /* Amber - caution, running states */
--error: #ef4444;          /* Red - errors, danger actions */
--danger: #ef4444;         /* Alias for destructive actions */

/* Accent - Configurable (default: blue) */
--accent: #3b82f6;
--accent-hover: #60a5fa;

/* Forms */
--input-bg: #1e2128;       /* Slightly darker than bg-primary */
--input-border: #363c4a;   /* Visible but not prominent */

/* UI Components */
--button-bg: #2e3340;
--button-hover: #363c4a;
--dropdown-bg: #242830;
--dropdown-hover: #2e3340;
--modal-overlay: rgba(0, 0, 0, 0.6);
--scrollbar-thumb: #3a3f4b;
```

### Light Theme

```css
--bg-primary: #f5f5f7;     /* Apple-style warm gray */
--bg-surface: #ffffff;     /* Pure white cards */
--bg-elevated: #ffffff;    /* Same as surface in light mode */
--bg-hover: #eeeef0;       /* Subtle gray hover */
--border-color: #e0e0e0;   /* Visible but soft */

--text-primary: #1a1d23;   /* Near-black */
--text-secondary: #6b7280;
--text-muted: #9ca3af;

--input-bg: #f0f0f2;
--input-border: #d1d5db;
```

### Accent Color Palette

Configurable accent colors with dark/light variants:

| Name | Dark | Light |
|------|------|-------|
| Blue | `#3b82f6` / `#60a5fa` | `#2563eb` / `#1d4ed8` |
| Purple | `#8b5cf6` / `#a78bfa` | `#7c3aed` / `#6d28d9` |
| Pink | `#ec4899` / `#f472b6` | `#db2777` / `#be185d` |
| Red | `#f43f5e` / `#fb7185` | `#e11d48` / `#be123c` |
| Orange | `#f97316` / `#fb923c` | `#ea580c` / `#c2410c` |
| Amber | `#f59e0b` / `#fbbf24` | `#d97706` / `#b45309` |
| Green | `#10b981` / `#34d399` | `#059669` / `#047857` |

---

## Typography

### Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Monospace (for code, commands, variables)

```css
font-family: 'SF Mono', 'Menlo', 'Monaco', Consolas, monospace;
```

### Scale

| Use Case | Size | Weight | Color |
|----------|------|--------|-------|
| Body text | 13px | 400 | `--text-primary` |
| Buttons | 12px | 500 | `--text-primary` |
| Labels (uppercase) | 12px | 500 | `--text-secondary` |
| Section titles | 11px | 600 | `--text-muted` |
| Hints/Metadata | 11px | 400 | `--text-muted` |
| Keyboard shortcuts | 11px | 400 | `--text-muted` |
| Modal titles | 14px | 600 | `--text-primary` |

### Text Rendering

```css
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

---

## Spacing & Layout

### Base Unit: 4px

All spacing derives from multiples of 4:

| Token | Value | Use |
|-------|-------|-----|
| `xs` | 4px | Icon gaps, tight padding |
| `sm` | 6px | Form element padding |
| `md` | 8px | Component gaps, section spacing |
| `lg` | 12px | Panel padding |
| `xl` | 16px | Modal padding |
| `xxl` | 24px | Major section breaks |

### Border Radius

```css
/* Tiered system */
border-radius: 3px;   /* Tiny: tags, badges */
border-radius: 4px;   /* Small: buttons, inputs */
border-radius: 6px;   /* Medium: cards, dropdowns */
border-radius: 8px;   /* Large: modals, panels */
```

---

## Components

### Buttons

```css
/* Base button */
button {
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  transition: background 0.15s ease, color 0.15s ease, transform 0.1s ease;
}

button:active {
  transform: scale(0.98);  /* Subtle press feedback */
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### Button Variants

| Variant | Background | Text |
|---------|------------|------|
| Default | `--button-bg` | `--text-primary` |
| Primary | `--accent` | `#ffffff` |
| Danger | `--danger` | `#ffffff` |
| Ghost | `transparent` | `--text-secondary` |

### Icon Buttons

```css
.icon-btn {
  background: none;
  padding: 4px;
  width: 26-28px;
  height: 26-28px;
  border-radius: 4px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.icon-btn.delete:hover {
  color: var(--error);
}
```

### Inputs

```css
input, textarea, select {
  font-size: 13px;
  padding: 6px 10px;
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: 4px;
  color: var(--text-primary);
  transition: border-color 0.15s ease;
}

input:focus {
  border-color: var(--accent);
  outline: none;
}

input::placeholder {
  color: var(--text-muted);
}
```

### Form Labels

```css
.form-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 5px;
}
```

### Cards / List Items

```css
.card {
  padding: 8px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  transition: background 0.15s ease;
}

.card:hover {
  background: var(--bg-elevated);
}
```

### Dropdowns

```css
.dropdown {
  background: var(--dropdown-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  max-height: 250px;
  overflow-y: auto;
}

.dropdown-option {
  padding: 8px 12px;
  font-size: 13px;
}

.dropdown-option:hover {
  background: var(--dropdown-hover);
}

.dropdown-option.active {
  color: var(--accent);
  font-weight: 500;
}
```

### Modals

```css
.modal-overlay {
  background: var(--modal-overlay);
  /* Dark: rgba(0,0,0,0.6), Light: rgba(0,0,0,0.3) */
}

.modal {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}
```

### Segmented Controls

```css
.segmented-control {
  display: flex;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.segmented-option {
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 500;
  background: var(--bg-primary);
  color: var(--text-secondary);
}

.segmented-option:not(:last-child) {
  border-right: 1px solid var(--border-color);
}

.segmented-option.active {
  background: var(--accent);
  color: #ffffff;
}
```

### Toggle Switches

```css
.toggle {
  width: 40px;
  height: 22px;
}

.toggle-slider {
  background: var(--button-bg);
  border-radius: 11px;
}

.toggle-slider::before {
  /* Knob */
  width: 18px;
  height: 18px;
  background: var(--text-secondary);
  border-radius: 50%;
  transition: transform 0.2s ease;
}

.toggle input:checked + .toggle-slider {
  background: var(--accent);
}

.toggle input:checked + .toggle-slider::before {
  transform: translateX(18px);
  background: #ffffff;
}
```

---

## Status Indicators

### Status Dots

Small colored circles for state indication:

```css
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.success { background: var(--success); }
.status-dot.fail { background: var(--error); }
.status-dot.running {
  background: var(--warning);
  animation: pulse-dot 1.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
```

### Badges

```css
.badge {
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 6px;
  border-radius: 3px;
  background: var(--accent);
  color: #ffffff;
}
```

### Keyboard Hints

```css
.kbd {
  padding: 2px 5px;
  font-size: 11px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 3px;
  color: var(--text-muted);
}
```

---

## Animations

### Timing

| Duration | Use Case |
|----------|----------|
| 0.1s | Button press, micro-interactions |
| 0.15s | Hover states, focus rings |
| 0.2s | Toggle switches, color changes |
| 1.5s | Pulsing animations (running states) |

### Easing

```css
transition-timing-function: ease;  /* Default */
/* Use ease-out for entrances, ease-in for exits */
```

### Common Patterns

```css
/* Hover transitions */
transition: background 0.15s ease, color 0.15s ease;

/* Button press */
button:active { transform: scale(0.98); }

/* Expansion arrow rotation */
.expand-icon {
  transition: transform 0.15s ease;
}
.expand-icon.expanded {
  transform: rotate(90deg);
}

/* Pulsing text (for "running" states) */
@keyframes pulse-text {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

---

## Icons

### Source

Material Design Icons (MDI) via inline SVG paths.

### Standard Size

```css
svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

/* In buttons/headers */
width: 18-20px;
height: 18-20px;
```

### Icon Component Pattern

```jsx
function Icon({ path, size = 16 }) {
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} fill="currentColor">
      <path d={path} />
    </svg>
  );
}
```

### Themed Icon Circles

```css
.icon-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## Scrollbars

```css
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
```

---

## macOS Integration

### Window Chrome

```css
/* Drag region for frameless windows */
.drag-region {
  -webkit-app-region: drag;
  height: 28px;
}

/* Exclude interactive elements */
.drag-region button,
.drag-region input {
  -webkit-app-region: no-drag;
}
```

### Text Selection

```css
body {
  user-select: none;  /* Disable by default */
}

/* Allow selection in content areas */
.selectable,
.output-content {
  user-select: text;
}
```

### System Font Features

```css
/* Use native font rendering */
-webkit-font-smoothing: antialiased;

/* Disable ligatures if needed */
font-variant-ligatures: none;
```

---

## Theme Implementation

### HTML Structure

```html
<html data-theme="dark" data-accent="blue">
```

### CSS Variables Approach

All colors use CSS custom properties, enabling theme switching by changing the `data-theme` attribute.

### Instant Theme Switch

Disable transitions during theme change to prevent flash:

```css
.theme-transitioning,
.theme-transitioning *,
.theme-transitioning *::before,
.theme-transitioning *::after {
  transition: none !important;
}
```

```javascript
// In JS
document.documentElement.classList.add('theme-transitioning');
document.documentElement.dataset.theme = newTheme;
requestAnimationFrame(() => {
  document.documentElement.classList.remove('theme-transitioning');
});
```

---

## File Structure

```
src/
├── shared-styles/
│   └── variables.css      # Design tokens (single source of truth)
│
├── renderer/
│   └── styles/
│       ├── variables.css  # @import '../shared-styles/variables.css'
│       ├── global.css     # Base styles, resets
│       └── components.css # Component styles
│
└── modal-apps/
    └── */
        └── styles.css     # Modal-specific styles
```

---

## Quick Start Template

```css
/* Base reset */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #root {
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 13px;
  background: var(--bg-primary);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  user-select: none;
}
```

---

## Do's and Don'ts

### Do

- Use the 3-tier text color system consistently
- Add hover states to all interactive elements
- Use subtle transitions (0.15s ease)
- Keep buttons compact (6px 12px padding)
- Use uppercase labels sparingly and only for form sections
- Maintain 4px spacing rhythm

### Don't

- Add gradients (except for type-specific icons)
- Use drop shadows on flat elements
- Mix rounded corners (pick 4px, 6px, or 8px per component)
- Use pure black or pure white in dark mode
- Add animations longer than 0.2s for state changes
- Use outline focus rings (use border-color instead)

---

## Electron-Specific Notes

### Window Backgrounds

Match Electron's native window background to prevent flash:

```javascript
// main.js
const window = new BrowserWindow({
  backgroundColor: theme === 'dark' ? '#1a1d23' : '#f5f5f7',
  // ...
});
```

### Vibrancy (if using)

```javascript
vibrancy: 'under-window',  // or 'sidebar', 'content'
visualEffectState: 'active',
```

---

*Keep this document updated as the design system evolves.*
