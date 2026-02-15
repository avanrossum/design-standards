# Testing Standards

> Guidelines for writing effective, maintainable tests in Electron + React applications. Tests exist to catch regressions, document intent, and give confidence during refactors.

---

## Philosophy

Tests are not bureaucracy. They are a design tool. Good tests:

- **Catch regressions** before users do
- **Document behavior** — a test suite is living documentation of what the code actually does
- **Enable refactoring** — you can restructure code confidently when tests verify the output hasn't changed
- **Surface edge cases** — writing tests forces you to think about null inputs, empty arrays, timezone issues, and other real-world scenarios

Bad tests (testing implementation details, duplicating code, or testing framework behavior) are worse than no tests — they create maintenance burden without catching real bugs.

**All new logic requires tests.** Any new pure function, data transformation, filter, formatter, or business logic must ship with corresponding tests. Code that introduces untested logic should not pass review.

---

## What to Test

### Always Test

- **Pure functions** — filters, formatters, parsers, validators, transformers. These are the highest-value tests: easy to write, fast to run, and they cover the logic most likely to break.
- **Data transformations** — any function that takes data in one shape and returns it in another.
- **Edge cases** — null inputs, empty arrays, missing fields, boundary values (today/tomorrow, exactly 60 minutes, empty strings).
- **Business logic** — inclusion/exclusion filters, sorting, search matching, permission checks.

### Test When Valuable

- **IPC handlers** — test the logic they wrap, not the IPC mechanism itself.
- **State transitions** — if a component has a state machine (idle -> confirming -> completing), test the transition logic.
- **API response parsing** — mock the HTTP layer, test that your code correctly handles the response shape.

### Don't Test

- **Framework behavior** — don't test that React renders a div, or that Electron opens a window.
- **Implementation details** — don't assert on internal variable values or function call counts unless that's the actual contract.
- **CSS/layout** — visual testing belongs in manual QA or visual regression tools, not unit tests.
- **Simple pass-throughs** — a function that just calls another function with the same args needs no test.

---

## Architecture for Testability

The most important testing decision happens before you write any tests: **structure your code so the important parts are testable.**

### Extract Pure Logic from Components

UI components mix rendering with logic. Extract the logic:

```javascript
// Bad — logic buried in component, untestable without React
function TaskList({ tasks, searchQuery }) {
  const filtered = useMemo(() => {
    // 30 lines of filter/sort logic
  }, [tasks, searchQuery]);
  return <div>{filtered.map(...)}</div>;
}

// Good — logic extracted, component just renders
// shared/filters.js
export function filterAndSortTasks(tasks, { searchQuery, sortBy }) {
  // Same 30 lines, now testable without React
}

// TaskList.jsx
function TaskList({ tasks, searchQuery, sortBy }) {
  const filtered = useMemo(
    () => filterAndSortTasks(tasks, { searchQuery, sortBy }),
    [tasks, searchQuery, sortBy]
  );
  return <div>{filtered.map(...)}</div>;
}
```

### Inject Dependencies for Time-Sensitive Code

Date/time functions are inherently flaky if they use `new Date()` internally. Make the reference time injectable:

```javascript
// Bad — non-deterministic, will randomly fail at midnight
export function formatDueDate(dueOn) {
  const now = new Date();
  // ...
}

// Good — deterministic, testable
export function formatDueDate(dueOn, now = new Date()) {
  // ...
}
```

### Separate Side Effects from Decisions

If a function both decides what to do and does it, split it:

```javascript
// Bad — decision and side effect coupled
function handleUpdate(task) {
  if (task.modified_at > lastSeen) {
    showNotification(task.name);
    updateBadgeCount(count + 1);
  }
}

// Good — decision is testable, side effect is trivial
function hasNewActivity(task, lastSeen) {
  return task.modified_at > lastSeen;
}
```

---

## Test Structure

### File Placement

Co-locate test files with the code they test:

```
src/
├── shared/
│   ├── filters.js
│   ├── filters.test.js
│   ├── formatters.js
│   └── formatters.test.js
```

### Naming

```
describe('[function/module name]', () => {
  it('[does specific thing in specific scenario]', () => {
```

Test descriptions should read as plain English documentation:

```javascript
// Good — clear, specific, documents behavior
describe('applyItemFilters', () => {
  it('excludes items by GID', () => { ... });
  it('applies inclusion filter — items must match at least one pattern', () => { ... });
  it('handles empty pattern strings gracefully', () => { ... });
});

// Bad — vague, tests implementation
describe('filter function', () => {
  it('works correctly', () => { ... });
  it('calls filter method', () => { ... });
});
```

### Test Data Factories

Use factory functions for test data. Don't repeat object literals:

```javascript
const makeTasks = () => [
  { gid: '1', name: 'Fix bug', assignee: { name: 'Alice', gid: 'u1' } },
  { gid: '2', name: 'Write docs', assignee: { name: 'Bob', gid: 'u2' } },
];
```

### Arrange-Act-Assert

Every test should have three clear sections:

```javascript
it('filters tasks by project GID', () => {
  // Arrange
  const tasks = makeTasks();

  // Act
  const result = filterAndSortTasks(tasks, { selectedProjectGid: 'p1' });

  // Assert
  expect(result).toHaveLength(2);
  expect(result.every(t => t.projects.some(p => p.gid === 'p1'))).toBe(true);
});
```

---

## Test Quality Checklist

When writing tests, verify:

- [ ] **Happy path** — does it work with normal input?
- [ ] **Empty input** — null, undefined, empty array, empty string
- [ ] **Boundary values** — zero, one, max, off-by-one
- [ ] **Case sensitivity** — if search/matching is involved
- [ ] **Missing fields** — objects with optional properties omitted
- [ ] **No mutation** — does the function modify its input array/object?
- [ ] **Determinism** — will this test pass at any time of day, in any timezone?

---

## Tooling

### Framework

- **Vitest** — fast, Vite-native, compatible with Jest assertions
- Config: `vitest.config.js` at project root
- Tests run via `npm test` (CI) or `npm run test:watch` (development)

### Commands

```bash
npm test           # Run all tests once (CI mode)
npm run test:watch # Watch mode for development
npm run lint       # ESLint check
```

### CI Integration

Tests and lint run on every push and pull request via GitHub Actions. The release script also gates on passing lint and tests before building.

---

## Anti-Patterns

### Don't Test the Framework

```javascript
// Bad — testing that React renders
it('renders a div', () => {
  render(<TaskList tasks={[]} />);
  expect(screen.getByRole('list')).toBeInTheDocument();
});
```

### Don't Mirror Implementation

```javascript
// Bad — if the implementation changes, the test breaks even though behavior is identical
it('uses Array.filter', () => {
  const spy = vi.spyOn(Array.prototype, 'filter');
  applyFilters(items, 'task', settings);
  expect(spy).toHaveBeenCalled();
});
```

### Don't Write Fragile Snapshots

```javascript
// Bad — breaks on any formatting change
it('matches snapshot', () => {
  expect(formatDueDate('2026-01-15')).toMatchSnapshot();
});

// Good — asserts on specific behavior
it('formats today as "Today"', () => {
  expect(formatDueDate('2026-01-15', now).text).toBe('Today');
});
```

### Don't Ignore Test Failures

A failing test is either:
1. **A real bug** — fix the code
2. **An outdated test** — update the test to match new intended behavior
3. **A flaky test** — fix the test (usually a time dependency or ordering issue)

Never skip, disable, or `xdescribe` a test without a comment explaining why and a plan to fix it.

---

*Write tests that protect you. If a test wouldn't catch a real bug, it's not earning its keep.*
