# Coding Standards

> Conventions and patterns for Electron + React macOS applications. Follow these when contributing or starting new projects.

---

## Language & Framework

- **TypeScript** - Strict mode (`strict: true`, `noUnusedLocals`, `noUnusedParameters`). Plain JavaScript acceptable for simpler projects
- **React 19+** - Functional components only, no class components
- **ES Modules** - `import`/`export`, no CommonJS in renderer
- **Node.js** - Main process source is ESM; `tsc` compiles to CJS for Electron
- **Electron** - Context isolation enabled, preload bridge pattern

---

## File Organization

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `ActionItem.tsx` |
| Modules/utilities | kebab-case | `hotkey-manager.ts` |
| CSS files | kebab-case | `global.css` |
| Constants files | kebab-case | `constants.ts` |
| Test files | `*.test.ts` | `utils.test.ts` |

### Directory Structure

```
src/
├── main/                    # Electron main process
│   ├── main.ts             # Entry point, window creation, lifecycle
│   ├── preload.ts          # Context bridge
│   ├── ipc-handlers.ts     # IPC handler registration
│   ├── store.ts            # Data persistence
│   └── *-manager.ts        # Stateful subsystems (classes)
│
├── renderer/               # React app
│   ├── App.tsx            # Root component, state management
│   ├── components/        # UI components
│   ├── context/           # React contexts
│   ├── hooks/             # Custom hooks
│   └── styles/            # CSS files
│
├── shared/                # Cross-boundary types and utilities
│   ├── types.ts           # Domain types, IPC contracts, preload API shapes
│   └── global.d.ts        # Window augmentation (declare global)
│
├── shared-styles/         # CSS shared across windows
│   └── variables.css      # Design tokens
│
└── modal-apps/            # Standalone modal windows
    └── [modal-name]/
        ├── index.html
        ├── App.tsx
        ├── preload.ts
        └── styles.css
```

### One Component Per File

Each React component gets its own file, named after the component:

```tsx
// components/ActionItem.tsx
interface ActionItemProps {
  action: Action;
  onRun: (id: string) => void;
}

export default function ActionItem({ action, onRun }: ActionItemProps) {
  // ...
}
```

---

## TypeScript Conventions

### Type Architecture

- **Shared types** (`src/shared/types.ts`): All types that cross the IPC boundary (Asana domain types, IPC channel maps, preload API interfaces, settings shape)
- **Window augmentation** (`src/shared/global.d.ts`): `declare global { interface Window { ... } }`
- **Component prop interfaces**: Defined inline above their component, not in shared types
- **Internal class state**: Stays inline, not shared
- **Constants**: Use `as const` assertions; let TypeScript infer the types

### Typing Patterns

```typescript
// Prop interfaces above components
interface TaskItemProps {
  task: AsanaTask;
  onComplete: (taskId: string) => Promise<void>;
}

// Typed useState
const [tasks, setTasks] = useState<AsanaTask[]>([]);
const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

// Event handlers
function handleClick(e: React.MouseEvent) { }
function handleChange(e: React.ChangeEvent<HTMLSelectElement>) { }

// Error narrowing in catch blocks
catch (err) {
  console.error('Failed:', (err as Error).message);
}

// String literal unions over enums
type SortBy = 'modified' | 'created' | 'alphabetical';
```

### tsconfig Structure

Use project references with a shared base config:

| File | Purpose | `module` | `outDir` | `noEmit` |
|------|---------|----------|----------|----------|
| `tsconfig.base.json` | Shared strict settings | - | - | - |
| `tsconfig.main.json` | Main process compilation | `commonjs` | `dist-main` | `false` |
| `tsconfig.renderer.json` | IDE + type checking (Vite builds) | `ESNext` | - | `true` |
| `tsconfig.json` | Root project references | - | - | - |

---

## Variables & Functions

```typescript
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

```typescript
// Props
function ActionItem({ action, onRun, isManaging }) {

// Context
const { state, dispatch } = useAppContext();

// Object returns
const { data, error } = await fetchData();
```

### Async/Await

Prefer `async`/`await` over `.then()` chains:

```typescript
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

```typescript
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

```typescript
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

```tsx
// Good
interface MyComponentProps {
  prop1: string;
  prop2: number;
}

export default function MyComponent({ prop1, prop2 }: MyComponentProps) {
  const [state, setState] = useState<string | null>(null);
  return <div>{/* ... */}</div>;
}

// Never
class MyComponent extends React.Component { }
```

### State Management

- **Global state**: React Context + useReducer (see App.jsx pattern)
- **Local state**: useState for UI-only concerns (loading, form values)
- **Derived state**: Compute in render, don't store

```typescript
// Global state via context
const { state, dispatch } = useAppContext();

// Local UI state
const [isExpanded, setIsExpanded] = useState(false);
const [inputValue, setInputValue] = useState('');

// Derived - compute, don't store
const filteredActions = actions.filter(a => a.categoryId === selectedCategory);
```

### Dispatch Pattern

```typescript
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

```typescript
await window.electronAPI.updateAction(id, data);
await refreshData();  // Re-fetch from store to sync state
```

### Event Handlers

Prefix with `handle`:

```typescript
function handleClick() {}
function handleSubmit(e) {}
function handleKeyDown(e) {}
```

---

## IPC Patterns

### Adding New IPC Methods

1. **Shared types** - Define channel contract in `src/shared/types.ts`:

```typescript
// In IpcInvokeChannelMap
'feature:action': { args: [arg1: string, arg2: number]; result: FeatureResult };
```

2. **Main process** - Add handler in `ipc-handlers.ts`:

```typescript
ipcMain.handle('feature:action', async (_event, arg1: string, arg2: number) => {
  return result;
});
```

3. **Preload** - Expose in `preload.ts`:

```typescript
contextBridge.exposeInMainWorld('electronAPI', {
  featureAction: (arg1: string, arg2: number) =>
    ipcRenderer.invoke('feature:action', arg1, arg2),
});
```

4. **Renderer** - Call via `window.electronAPI`:

```typescript
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

```typescript
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

```typescript
// hotkey-manager.ts
import { ipcMain } from 'electron';
import type { Store } from './store';
import type { BrowserWindow } from 'electron';

class HotkeyManager {
  private store: Store;
  private getMainWindow: () => BrowserWindow | null;
  private registeredHotkeys = new Map<string, string>();

  constructor({ store, getMainWindow }: {
    store: Store;
    getMainWindow: () => BrowserWindow | null;
  }) {
    this.store = store;
    this.getMainWindow = getMainWindow;
  }

  registerIpcHandlers(): void {
    ipcMain.handle('hotkey:register', (_, id: string, combo: string) =>
      this.register(id, combo));
    ipcMain.handle('hotkey:unregister', (_, id: string) =>
      this.unregister(id));
  }

  register(id: string, combo: string): void { /* ... */ }
  unregister(id: string): void { /* ... */ }
}

export { HotkeyManager };
```

### Instantiation in main.ts

```typescript
// main.ts - app.whenReady()
const hotkeyManager = new HotkeyManager({
  store,
  getMainWindow: () => mainWindow,
});
hotkeyManager.registerIpcHandlers();
```

### Stateless Utilities as Modules

For pure functions, use named exports:

```typescript
// utils.ts
export function escapeShellArg(arg: string): string { /* ... */ }
export function substituteVariables(template: string, vars: Record<string, string>): string { /* ... */ }
```

---

## Comments

### When to Comment

Comment the **why**, not the **what**:

```typescript
// Good - explains why
// Detach process so it survives app quit (fire-and-forget pattern)
child.unref();

// Bad - just restates the code
// Unref the child process
child.unref();
```

### Section Headers

For long files, use visual separators:

```typescript
// ── Window Management ──────────────────────────────────

function createWindow() { }
function showWindow() { }

// ── IPC Handlers ───────────────────────────────────────

function registerHandlers() { }
```

### JSDoc for Complex Functions

With TypeScript, `@param` and `@returns` type annotations are redundant. Use JSDoc only when the **purpose** needs explanation beyond what the type signature conveys:

```typescript
/**
 * Runs an action with variable substitution.
 * Spawns a detached child process that survives app quit when detached=true.
 */
async function runAction(
  action: ActionConfig,
  variables: Record<string, string>,
  detached = false
): Promise<ActionResult> { }
```

### Don't Comment Obvious Code

```typescript
// Bad - unnecessary
// Set loading to true
setLoading(true);

// Good - no comment needed, code is clear
setLoading(true);
```

---

## Import Order

Group imports logically (no strict enforcement, but prefer this order):

```typescript
// 1. React and core libraries
import { useState, useEffect } from 'react';

// 2. Third-party libraries
import CodeMirror from '@uiw/react-codemirror';

// 3. Type imports (grouped with or after their source)
import type { ActionConfig, ActionResult } from '../shared/types';

// 4. Local components
import ActionItem from './components/ActionItem';
import Modal from './components/Modal';

// 5. Hooks and context
import { useAppContext } from './context/AppContext';

// 6. Utilities and constants
import { formatDate } from './utils';
import { MODAL_CONFIG } from './constants';

// 7. Styles (at end)
import './styles/global.css';
```

---

## Avoid Over-Engineering

### Don't Add Unnecessary Abstraction

```typescript
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

```typescript
// Bad - adding options "for later"
function saveAction(action, { validate = true, backup = false, notify = true }) { }

// Good - implement when actually needed
function saveAction(action) { }
```

### Keep Functions Focused

```typescript
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

```typescript
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

```typescript
const { escapeShellArg } = require('./utils');
const safeArg = escapeShellArg(userInput);
spawn('sh', ['-c', `echo ${safeArg}`]);
```

### No Eval

Never eval user-provided strings:

```typescript
// Never
eval(userScript);
new Function(userCode)();

// If scripts are needed, execute in controlled environment
spawn('node', [scriptPath]);
```

---

## Testing Patterns

**Tests are required for all new logic.** Any new pure function, data transformation, or business logic must have corresponding tests before it ships. Extract testable logic from components into shared modules (see TESTING_STANDARDS.md for the full methodology).

### File Naming

```
src/
├── utils.ts
└── utils.test.ts
```

### Test Structure

```typescript
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
