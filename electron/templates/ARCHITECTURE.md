# [PROJECT_NAME] - Architecture Guide

> **For LLM Sessions:** Read ROADMAP.md first for project overview. This document covers implementation details and code patterns.

---

## Directory Structure

```
project/
├── src/
│   ├── main/                    # Electron main process
│   │   ├── main.js              # Entry point, window creation, app lifecycle
│   │   ├── store.js             # Data persistence
│   │   ├── ipc-handlers.js      # IPC message handlers
│   │   ├── preload.js           # Context bridge API
│   │   └── *-manager.js         # Stateful subsystems (classes)
│   │
│   ├── renderer/                # React frontend
│   │   ├── index.html           # HTML entry point
│   │   ├── index.jsx            # React root mount
│   │   ├── App.jsx              # Main app, context provider, reducer
│   │   ├── components/          # React components
│   │   └── styles/              # CSS files
│   │
│   └── shared-styles/           # Shared CSS across windows
│       └── variables.css        # CSS custom properties (themes)
│
├── build/                       # App resources
│   ├── icon.icns               # macOS app icon
│   └── trayIconTemplate.png    # Tray icon
│
├── package.json
├── vite.config.js
└── electron-builder.config.js
```

---

## Process Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Process                             │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐             │
│  │  Store   │  │  Tray    │  │  [Feature]    │             │
│  │ (JSON)   │  │  Menu    │  │   Manager     │             │
│  └────┬─────┘  └────┬─────┘  └───────┬───────┘             │
│       │             │                │                      │
│       └─────────────┼────────────────┘                      │
│                     │                                        │
│              ┌──────┴──────┐                                │
│              │ IPC Handlers│                                │
│              └──────┬──────┘                                │
└─────────────────────┼───────────────────────────────────────┘
                      │ contextBridge
              ┌───────┴───────┐
              │  preload.js   │
              │ (electronAPI) │
              └───────┬───────┘
                      │
┌─────────────────────┼───────────────────────────────────────┐
│                     │      Renderer Process                  │
│              ┌──────┴──────┐                                │
│              │   App.jsx   │                                │
│              │  (Context)  │                                │
│              └──────┬──────┘                                │
│                     │                                        │
│    ┌────────────────┼────────────────┐                      │
│    │                │                │                      │
│ ┌──┴───┐     ┌──────┴─────┐    ┌────┴────┐                 │
│ │Header│     │  Content   │    │ Modals  │                 │
│ └──────┘     └────────────┘    └─────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### State Management

React Context + useReducer pattern in `App.jsx`:

```javascript
// State shape
{
  items: [],
  settings: {},
  selectedId: null,
  activeModal: null,
  loaded: false
}

// Key actions
'INIT'              - Load initial data
'SET_ITEMS'         - Update items array
'SET_SETTINGS'      - Merge settings
'OPEN_MODAL'        - Open modal with optional payload
'CLOSE_MODAL'       - Close current modal
```

### IPC Communication

All renderer-to-main communication uses `window.electronAPI`:

```javascript
// Request-response (invoke/handle)
window.electronAPI.getData()
window.electronAPI.saveItem(itemData)

// Events (send/on)
window.electronAPI.onSomeEvent(callback)  // Returns unsubscribe fn
```

**Pattern:** After any mutation via IPC, call `refreshData()` to sync React state.

---

## Data Structures

### Settings

```javascript
{
  theme: 'dark' | 'light' | 'system',
  windowBounds: { width, height, x, y }
}
```

---

## Component Patterns

### Component Structure

```jsx
import { useAppContext } from '../App';

export default function MyComponent({ prop }) {
  const { state, dispatch, refreshData } = useAppContext();

  // Local state for UI concerns only
  const [loading, setLoading] = useState(false);

  // Handlers call IPC then refresh
  const handleAction = async () => {
    await window.electronAPI.doSomething();
    await refreshData();
  };

  return (/* JSX */);
}
```

---

## Store Persistence

### File Location

```
macOS: ~/Library/Application Support/[app-name]/data.json
```

### Write Strategy

- Debounced writes (300ms) to reduce I/O
- Synchronous write on initial load
- Merges with defaults on load to handle schema changes

---

## Adding New Features

### New IPC Channel

1. Add handler in `src/main/ipc-handlers.js`
2. Expose in `src/main/preload.js`
3. Call via `window.electronAPI.newMethod()`

### New Setting

1. Add to `DEFAULT_DATA.settings` in `store.js`
2. Add IPC handler if main process needs to react
3. Add UI in Settings component
4. Update reducer in `App.jsx` if needed

---

## Testing Checklist

Before shipping changes:

- [ ] Test in dev mode (`npm run dev`)
- [ ] Test production build (`npm run build`)
- [ ] Verify data persists across restarts
- [ ] Check both dark and light themes
- [ ] Test window bounds persistence
- [ ] Verify tray icon works
