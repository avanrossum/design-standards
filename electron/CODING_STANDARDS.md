# Coding Standards

> Conventions and patterns for Electron + React macOS applications. Follow these when contributing or starting new projects.

---

## Language & Framework

- **Plain JavaScript** - No TypeScript
- **React 18+** - Functional components only, no class components
- **ES Modules** - `import`/`export`, no CommonJS in renderer
- **Node.js** - CommonJS in main process is acceptable
- **Electron** - Context isolation enabled, preload bridge pattern

---

## File Organization

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `ActionItem.jsx` |
| Modules/utilities | kebab-case | `hotkey-manager.js` |
| CSS files | kebab-case | `global.css` |
| Constants files | kebab-case | `constants.js` |
| Test files | `*.test.js` | `utils.test.js` |

### Directory Structure

```
src/
├── main/                    # Electron main process
│   ├── main.js             # Entry point, window creation, lifecycle
│   ├── preload.js          # Context bridge
│   ├── ipc-handlers.js     # IPC handler registration
│   ├── store.js            # Data persistence
│   └── *-manager.js        # Stateful subsystems (classes)
│
├── renderer/               # React app
│   ├── App.jsx            # Root component, state management
│   ├── components/        # UI components
│   ├── context/           # React contexts
│   ├── hooks/             # Custom hooks
│   └── styles/            # CSS files
│
├── shared-styles/         # CSS shared across windows
│   └── variables.css      # Design tokens
│
└── modal-apps/            # Standalone modal windows
    └── [modal-name]/
        ├── index.html
        ├── App.jsx
        ├── preload.js
        └── styles.css
```

### One Component Per File

Each React component gets its own file, named after the component:

```jsx
// components/ActionItem.jsx
export default function ActionItem({ action, onRun }) {
  // ...
}
```

---

## JavaScript Conventions

### Variables & Functions

```javascript
// Variables: camelCase
const isLoading = false;
const actionList = [];

// Functions: camelCase, descriptive verbs
function handleClick() {}
function fetchActions() {}
async function saveToStore() {}

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const DEFAULT_WINDOW_WIDTH = 400;

// Private/internal: leading underscore (in classes)
_internalMethod() {}
```

### Destructuring

Always destructure props, context, and object returns:

```javascript
// Props
function ActionItem({ action, onRun, isManaging }) {

// Context
const { state, dispatch } = useAppContext();

// Object returns
const { data, error } = await fetchData();
```

### Async/Await

Prefer `async`/`await` over `.then()` chains:

```javascript
// Good
async function loadData() {
  try {
    const result = await window.electronAPI.getData();
    return result;
  } catch (err) {
    console.error('Failed to load:', err);
  }
}

// Avoid
function loadData() {
  return window.electronAPI.getData()
    .then(result => result)
    .catch(err => console.error(err));
}
```

### Error Handling

Wrap IPC calls and external operations in try/catch:

```javascript
async function saveAction(data) {
  try {
    await window.electronAPI.updateAction(data.id, data);
    await refreshData();
  } catch (err) {
    console.error('Save failed:', err);
    showError('Failed to save action');
  }
}
```

### Explicit Returns

Use explicit returns for multi-line JSX, implicit for simple expressions:

```javascript
// Explicit for multi-line JSX
function ActionItem({ action }) {
  return (
    <div className="action-item">
      <span>{action.name}</span>
    </div>
  );
}

// Implicit OK for simple transforms
const names = actions.map(a => a.name);
```

---

## React Patterns

### Functional Components Only

```javascript
// Good
export default function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null);
  return <div>{/* ... */}</div>;
}

// Never
class MyComponent extends React.Component { }
```

### State Management

- **Global state**: React Context + useReducer (see App.jsx pattern)
- **Local state**: useState for UI-only concerns (loading, form values)
- **Derived state**: Compute in render, don't store

```javascript
// Global state via context
const { state, dispatch } = useAppContext();

// Local UI state
const [isExpanded, setIsExpanded] = useState(false);
const [inputValue, setInputValue] = useState('');

// Derived - compute, don't store
const filteredActions = actions.filter(a => a.categoryId === selectedCategory);
```

### Dispatch Pattern

```javascript
// Opening modals
dispatch({ type: 'OPEN_MODAL', payload: { modal: 'settings' } });
dispatch({ type: 'OPEN_MODAL', payload: { modal: 'editAction', actionId: 'act_123' } });

// Closing modals
dispatch({ type: 'CLOSE_MODAL' });

// State updates
dispatch({ type: 'SET_CATEGORIES', payload: categories });
```

### Refresh After Mutations

Always refresh React state after IPC mutations:

```javascript
await window.electronAPI.updateAction(id, data);
await refreshData();  // Re-fetch from store to sync state
```

### Event Handlers

Prefix with `handle`:

```javascript
function handleClick() {}
function handleSubmit(e) {}
function handleKeyDown(e) {}
```

---

## IPC Patterns

### Adding New IPC Methods

1. **Main process** - Add handler in `ipc-handlers.js` or dedicated module:

```javascript
// ipc-handlers.js
ipcMain.handle('feature:action', async (event, arg1, arg2) => {
  // Implementation
  return result;
});
```

2. **Preload** - Expose in `preload.js`:

```javascript
contextBridge.exposeInMainWorld('electronAPI', {
  featureAction: (arg1, arg2) => ipcRenderer.invoke('feature:action', arg1, arg2),
});
```

3. **Renderer** - Call via `window.electronAPI`:

```javascript
const result = await window.electronAPI.featureAction(arg1, arg2);
```

### IPC Naming

Use colon-separated namespaces:

```
store:get-data
action:run
hotkey:register
modal:submit
settings:update
```

### Promise-Based IPC for Windows

For windows that return data (like dialogs):

```javascript
// Main process
let resolvePromise;

function showInputWindow(data) {
  return new Promise((resolve) => {
    resolvePromise = resolve;
    createWindow(data);
  });
}

ipcMain.on('window:submit', (event, result) => {
  resolvePromise?.(result);
  resolvePromise = null;
});
```

---

## CSS Conventions

### Variables for Everything

Never hardcode colors, always use CSS variables:

```css
/* Good */
color: var(--text-primary);
background: var(--bg-surface);

/* Bad */
color: #e8e8e8;
background: #242830;
```

### Component Prefixes

Prefix classes with component abbreviation to avoid conflicts:

```css
/* Global Variables Manager */
.gvm-list { }
.gvm-variable { }
.gvm-preset-item { }

/* Action Variables Section */
.avs-header { }
.avs-content { }
.avs-variable { }
```

### No `!important`

Fix specificity properly instead:

```css
/* Bad */
.button { color: red !important; }

/* Good - increase specificity */
.modal .button { color: red; }
```

### Section Comments

Use section headers in long CSS files:

```css
/* ── Header ── */
.header { }

/* ── Action List ── */
.action-list { }

/* ── Modal Overlay ── */
.modal-overlay { }
```

### Class Naming

kebab-case with component context:

```css
.action-item { }
.action-item-name { }
.action-item-meta { }
.action-item-icon { }
```

---

## Module Patterns

### Stateful Subsystems as Classes

For features with internal state, use classes:

```javascript
// hotkey-manager.js
class HotkeyManager {
  constructor({ store, getMainWindow }) {
    this.store = store;
    this.getMainWindow = getMainWindow;
    this.registeredHotkeys = new Map();
  }

  registerIpcHandlers() {
    ipcMain.handle('hotkey:register', (_, id, combo) => this.register(id, combo));
    ipcMain.handle('hotkey:unregister', (_, id) => this.unregister(id));
  }

  register(id, combo) { /* ... */ }
  unregister(id) { /* ... */ }
}

module.exports = { HotkeyManager };
```

### Instantiation in main.js

```javascript
// main.js - app.whenReady()
hotkeyManager = new HotkeyManager({
  store,
  getMainWindow: () => mainWindow,
});
hotkeyManager.registerIpcHandlers();
```

### Stateless Utilities as Modules

For pure functions, use module exports:

```javascript
// utils.js
function escapeShellArg(arg) { /* ... */ }
function substituteVariables(template, vars) { /* ... */ }

module.exports = { escapeShellArg, substituteVariables };
```

---

## Comments

### When to Comment

Comment the **why**, not the **what**:

```javascript
// Good - explains why
// Detach process so it survives app quit (fire-and-forget pattern)
child.unref();

// Bad - just restates the code
// Unref the child process
child.unref();
```

### Section Headers

For long files, use visual separators:

```javascript
// ── Window Management ──────────────────────────────────

function createWindow() { }
function showWindow() { }

// ── IPC Handlers ───────────────────────────────────────

function registerHandlers() { }
```

### JSDoc for Complex Functions

Use JSDoc for functions with non-obvious parameters:

```javascript
/**
 * Runs an action with variable substitution
 * @param {Object} action - The action configuration
 * @param {Object} variables - Key-value pairs for substitution
 * @param {boolean} [detached=false] - Run without tracking output
 * @returns {Promise<{success: boolean, output?: string, error?: string}>}
 */
async function runAction(action, variables, detached = false) { }
```

### Don't Comment Obvious Code

```javascript
// Bad - unnecessary
// Set loading to true
setLoading(true);

// Good - no comment needed, code is clear
setLoading(true);
```

---

## Import Order

Group imports logically (no strict enforcement, but prefer this order):

```javascript
// 1. React and core libraries
import { useState, useEffect } from 'react';

// 2. Third-party libraries
import CodeMirror from '@uiw/react-codemirror';

// 3. Local components
import ActionItem from './components/ActionItem';
import Modal from './components/Modal';

// 4. Hooks and context
import { useAppContext } from './context/AppContext';

// 5. Utilities and constants
import { formatDate } from './utils';
import { MODAL_CONFIG } from './constants';

// 6. Styles (at end)
import './styles/global.css';
```

---

## Avoid Over-Engineering

### Don't Add Unnecessary Abstraction

```javascript
// Bad - premature abstraction for one use
function createActionHandler(type) {
  return (action) => {
    if (type === 'run') runAction(action);
    if (type === 'edit') editAction(action);
  };
}

// Good - direct and clear
function handleRun(action) { runAction(action); }
function handleEdit(action) { editAction(action); }
```

### Don't Add Unused Features

Only implement what's needed now:

```javascript
// Bad - adding options "for later"
function saveAction(action, { validate = true, backup = false, notify = true }) { }

// Good - implement when actually needed
function saveAction(action) { }
```

### Keep Functions Focused

```javascript
// Bad - doing too much
async function loadAndValidateAndSaveAction(data) { }

// Good - single responsibility
async function validateAction(data) { }
async function saveAction(data) { }
```

---

## Security Considerations

### Input Validation

Validate at system boundaries:

```javascript
// Good - validate before execution
function runCommand(cmd) {
  if (!cmd || typeof cmd !== 'string') {
    return { success: false, error: 'Invalid command' };
  }
  // proceed...
}
```

### Shell Escaping

Always escape user input in shell commands:

```javascript
const { escapeShellArg } = require('./utils');
const safeArg = escapeShellArg(userInput);
spawn('sh', ['-c', `echo ${safeArg}`]);
```

### No Eval

Never eval user-provided strings:

```javascript
// Never
eval(userScript);
new Function(userCode)();

// If scripts are needed, execute in controlled environment
spawn('node', [scriptPath]);
```

---

## Testing Patterns

### File Naming

```
src/
├── utils.js
└── utils.test.js
```

### Test Structure

```javascript
describe('escapeShellArg', () => {
  it('escapes single quotes', () => {
    expect(escapeShellArg("it's")).toBe("'it'\\''s'");
  });

  it('handles empty string', () => {
    expect(escapeShellArg('')).toBe("''");
  });
});
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
feat: Add shortcut picker with search
fix: Prevent child modal from closing parent
refactor: Extract hotkey logic to HotkeyManager class
docs: Update ARCHITECTURE.md with child modal pattern
```

### Branch Naming

```
feature/shortcut-picker
fix/modal-close-bug
refactor/extract-hotkey-manager
```

---

*Keep code simple, direct, and purposeful. When in doubt, choose clarity over cleverness.*
