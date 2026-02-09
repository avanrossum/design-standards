# Claude Code Instructions for [PROJECT_NAME]

> **This file is for LLM sessions.** Quick context for working on this codebase.

## Session Start Checklist

1. Read `ROADMAP.md` - Current sprint and priorities
2. Read `ARCHITECTURE.md` - Patterns and structure
3. Check active tasks before making changes

## Quick Context

**[PROJECT_NAME]** is a [one-sentence description]. Built with Electron + React.

### Key Files

| Purpose | File |
|---------|------|
| App entry & window management | `src/main/main.js` |
| State management | `src/renderer/App.jsx` |
| Data persistence | `src/main/store.js` |
| IPC bridge | `src/main/preload.js` + `src/main/ipc-handlers.js` |
| Theming | `src/renderer/styles/variables.css` |

### Commands

```bash
npm run dev    # Development
npm run build  # Production build
```

## Patterns to Follow

### State Changes
```javascript
// Always refresh after mutations
await window.electronAPI.updateSomething(id, data);
await refreshData();  // Sync React state with store
```

### New IPC Methods
1. Add handler in `ipc-handlers.js`
2. Expose in `preload.js`
3. Call via `window.electronAPI.methodName()`

### Component Creation
- Keep components focused and single-purpose
- Use `useAppContext()` for state access
- Local state only for UI concerns (loading states, form values)

## Coding Standards

See `CODING_STANDARDS.md` for full conventions. Key points:

- **No TypeScript** - Plain JavaScript with JSDoc where helpful
- **Functional components** - Use hooks, no class components
- **async/await** - Over `.then()` chains
- **CSS Variables** - All colors from `variables.css`

## Critical Gotchas

1. **Sandbox disabled** - Required for script execution, security tradeoff
2. **Store debounce** - 300ms delay on writes, don't rely on immediate persistence
3. **Theme dual-sync** - Both CSS `data-theme` and Electron `nativeTheme` must match
4. **Close = hide** - Window close hides to tray, doesn't quit

## Documentation Updates

When making changes:
- Update `ROADMAP.md` if adding/completing features
- Update `ARCHITECTURE.md` if changing patterns
- Update `CHANGELOG.md` for releases

## Session End Checklist

1. Ensure changes are tested
2. Update ROADMAP.md if tasks completed
3. Document new gotchas
4. Leave codebase working
