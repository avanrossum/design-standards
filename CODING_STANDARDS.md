# Coding Standards

> Universal coding standards that apply across all frameworks, languages, and platforms. Read this alongside `SHARED.md`, then consult the framework-specific standards for implementation details.

---

## DRY — Don't Repeat Yourself

### The Rule

Every piece of knowledge should have a single, authoritative source. Duplication breeds inconsistency — when logic exists in two places, one will eventually drift.

### Apply It

- **Extract shared logic** into reusable modules. If two components compute the same derived value, extract a function both can import.
- **Constants belong in one place.** Magic numbers, configuration defaults, and string literals used in multiple locations must live in a constants file or config object.
- **Shared types live in shared files.** Cross-boundary types (API contracts, domain models, IPC definitions) belong in a shared module, not duplicated per consumer.
- **Reusable UI patterns become components.** When the same layout, interaction, or display logic appears in multiple views, extract it into a named component.

### Don't Over-Apply It

DRY is about *knowledge*, not *code that looks similar*. Two functions with similar structure but different purposes are not duplication — they represent different concepts that happen to share syntax.

```
# Bad — premature abstraction hides intent
def handle_entity(entity, entity_type):
    if entity_type == 'user': ...
    elif entity_type == 'project': ...

# Good — separate functions for separate concerns
def handle_user(user): ...
def handle_project(project): ...
```

Extract when you see the same *decision* being made in multiple places. Leave it alone when two blocks of code merely *look* alike but serve different purposes.

---

## Separation of Concerns

### Principle

Each module, function, or layer should own exactly one responsibility. When a module handles multiple concerns, changes to one concern risk breaking the other.

### Layered Architecture

Organize code into clear layers with defined responsibilities:

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **Data** | Storage, retrieval, persistence | Database clients, file I/O, cache managers |
| **Logic** | Business rules, transformations, validation | Pure functions, domain models, formatters |
| **Transport** | Communication between processes or services | IPC handlers, API clients, message brokers |
| **Presentation** | Display, interaction, user-facing behavior | Components, views, CLI output formatters |

Rules:
- **Data layer** never imports from presentation
- **Logic layer** is pure — no side effects, no I/O, no framework dependencies
- **Transport layer** validates input, delegates to logic, returns results
- **Presentation layer** renders state and dispatches user actions

### Function-Level Separation

Each function does one thing:

```
# Bad — fetching, validating, AND saving in one function
async function processUserData(raw):
    response = await fetch(url)
    if not response.ok: throw Error
    validated = validate(response.data)
    await database.save(validated)
    return validated

# Good — each step is a focused function
async function fetchUser(url): ...
function validateUser(data): ...
async function saveUser(validated): ...
```

### File-Level Separation

One module, one purpose:

```
# Bad
utils.ts          (1200 lines of everything)

# Good
formatters.ts     (date/time/string formatting)
validators.ts     (input validation rules)
filters.ts        (filtering, sorting, partitioning)
csv.ts            (export utilities)
```

When a file grows beyond ~300 lines, look for natural seams to split along.

---

## Slim Entry Points and Controllers

### The Problem

Entry points (`main.ts`, `app.ts`, `index.ts`) and controller files tend to accumulate logic over time. They start as thin orchestrators and end as 2000-line monoliths that are impossible to test or reason about.

### The Standard

Entry points should do three things and nothing else:

1. **Initialize** — Create instances, load configuration, establish connections
2. **Wire** — Connect modules to each other (dependency injection, event binding, handler registration)
3. **Start** — Begin the application lifecycle (listen, serve, run)

```
# Bad — main.ts does everything
function main():
    # 50 lines of config parsing
    # 100 lines of database setup
    # 200 lines of route handlers
    # 80 lines of middleware logic
    # 40 lines of error handling
    app.listen(port)

# Good — main.ts orchestrates
function main():
    config = loadConfig()
    db = createDatabase(config.db)
    store = Store(db)
    api = ApiClient(config.api)

    registerHandlers(store, api)
    registerMiddleware(app)

    app.listen(config.port)
```

### Delegation Pattern

When a controller or handler file grows, extract logic into focused modules:

| Keep in controller | Extract to module |
|-------------------|-------------------|
| Route/handler registration | Business logic |
| Input validation (basic type checks) | Complex validation rules |
| Error response formatting | Data transformations |
| Calling the right module | The actual work |

The controller's job is to receive a request, validate it minimally, call the right module, and return the result. If a handler function exceeds ~30 lines, it's probably doing too much.

---

## Best Practices

### Naming

Names should reveal intent without requiring comments:

```
# Bad — requires mental mapping
const d = new Date();
const t = items.filter(i => i.s === 'a');
function proc(x) { }

# Good — self-documenting
const now = new Date();
const activeItems = items.filter(item => item.status === 'active');
function processPayment(invoice) { }
```

Conventions:
- **Functions**: verbs describing their action (`fetchUser`, `validateInput`, `formatDate`)
- **Variables**: nouns describing their content (`userList`, `isLoading`, `errorMessage`)
- **Booleans**: question form (`isVisible`, `hasPermission`, `shouldRetry`)
- **Constants**: SCREAMING_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private/internal**: leading underscore in languages that lack access modifiers (`_internalState`)

### Error Handling

Every external operation can fail. Handle it explicitly.

```
# Bad — unhandled failures
data = await fetchData()
save(data)

# Good — failures are anticipated
try:
    data = await fetchData()
    save(data)
catch error:
    log.error('Fetch failed:', error.message)
    showUserError('Unable to load data. Please retry.')
```

Principles:
- **Catch at the boundary** — Handle errors where you can do something useful (retry, show feedback, fall back)
- **Don't swallow errors silently** — At minimum, log them. Silent catch blocks hide bugs
- **Provide context** — "Failed to save user preferences" is more useful than "An error occurred"
- **Fail fast** — Validate inputs early. Don't let bad data travel deep into the system
- **Separate expected from unexpected** — A 404 is expected; an unhandled null is a bug. Handle them differently

### Async/Await Over Callbacks

Prefer `async`/`await` (or language-equivalent) over callback chains or deeply nested `.then()`:

```
# Avoid — callback pyramid
fetchUser(id, function(user) {
    fetchPosts(user.id, function(posts) {
        renderProfile(user, posts, function() {
            // ...
        })
    })
})

# Prefer — linear and readable
const user = await fetchUser(id)
const posts = await fetchPosts(user.id)
await renderProfile(user, posts)
```

### Immutability by Default

Prefer creating new values over mutating existing ones:

```
# Avoid — mutation
items.push(newItem)
user.name = 'Updated'

# Prefer — new values
const updated = [...items, newItem]
const updatedUser = { ...user, name: 'Updated' }
```

Mutation is acceptable when performance requires it or the language idiom expects it — but it should be the conscious exception, not the default.

### Guard Clauses Over Deep Nesting

Return early to keep the main logic path at the top indentation level:

```
# Bad — nested conditions
function processOrder(order):
    if order != null:
        if order.isValid:
            if order.items.length > 0:
                # actual logic buried 3 levels deep
                ...

# Good — guard clauses
function processOrder(order):
    if order == null: return
    if !order.isValid: return
    if order.items.length == 0: return

    # main logic at top level
    ...
```

### Avoid Over-Engineering

Only build what's needed now:

- **No speculative parameters** — Don't add `options` objects "for later"
- **No premature abstraction** — Two similar functions don't need a factory. Wait for the third
- **No unused indirection** — If a wrapper adds no behavior, remove it
- **No generic frameworks for specific problems** — Solve the problem at hand

```
# Over-engineered
class DataProcessorFactory:
    def create(type, strategy, options): ...

# Right-sized
def process_users(users): ...
def process_orders(orders): ...
```

---

## Documentation

### Comments Explain "Why", Not "What"

The code tells you *what* happens. Comments tell you *why* it happens that way.

```
# Bad — restates the code
// Increment retry count
retryCount += 1

# Good — explains the reasoning
// Retry count starts at -1 to account for the initial attempt
retryCount += 1

# Good — explains a non-obvious constraint
// Asana search API doesn't support standard offset pagination;
// must paginate manually via created_at.after sorted ascending
```

### When to Comment

- **Non-obvious business rules** — Why this threshold? Why this order?
- **Workarounds** — What bug or limitation does this work around?
- **Performance decisions** — Why this approach over the obvious one?
- **External dependencies** — What API behavior or system constraint drives this?

### When Not to Comment

- **Self-documenting code** — Good names eliminate the need for most comments
- **Restating the code** — `// Set loading to true` above `setLoading(true)` adds nothing
- **Commented-out code** — Delete it. Version control remembers

### Section Headers

In longer files, use visual separators to create scannable structure:

```
// ── Window Management ──────────────────────────────────

function createWindow() { }
function showWindow() { }

// ── Event Handlers ─────────────────────────────────────

function handleClick() { }
function handleSubmit() { }
```

### JSDoc / Docstrings

Use documentation comments for functions whose purpose isn't obvious from the signature. In typed languages, skip `@param` and `@returns` type annotations — the types already convey that:

```
/**
 * Spawns a detached process that survives app quit.
 * Used for fire-and-forget background tasks.
 */
async function spawnDetached(command: string, args: string[]): Promise<void>
```

### Inline Documentation Standards

Every project should maintain living documentation (see `SHARED.md` for the full list). At minimum:

| Document | Purpose |
|----------|---------|
| `README.md` | What it is, how to run it |
| `CLAUDE.md` | AI session context — front-loaded, specific, current |
| `ARCHITECTURE.md` | System design, data flow, key decisions |

Keep `CLAUDE.md` ruthlessly current. It is the most-read file in AI-assisted development.

---

## Security Posture

Security is not a feature — it's a property of how you write all code.

### Validate at Boundaries

Every input from an external source is untrusted until validated:

- **User input** — Form fields, URL parameters, command-line arguments
- **API responses** — External services can return unexpected shapes
- **File contents** — Files on disk may be corrupted or tampered with
- **IPC messages** — Even internal communication should validate types
- **Environment variables** — May be missing, empty, or malformed

```
# Bad — trusts external input
function handleRequest(data):
    database.query(data.sql)

# Good — validates and constrains
function handleRequest(data):
    if typeof data.id != 'string': throw InvalidInput
    if data.id.length > 100: throw InvalidInput
    database.findById(sanitize(data.id))
```

### Never Trust, Always Verify

- **Don't trust client-side validation alone** — Always re-validate on the server/main process
- **Don't trust file extensions** — Verify content type when it matters
- **Don't trust environment** — Check that required values exist before using them

### Secrets Management

- **Never hardcode secrets** — No API keys, tokens, or passwords in source code
- **Never log secrets** — Mask or omit sensitive values in log output
- **Never send secrets to the renderer** — In Electron: IPC returns masked values, never raw keys
- **Use platform facilities** — OS Keychain, encrypted storage, environment-injected secrets

```
# Bad
const API_KEY = 'sk-abc123...'

# Good
const API_KEY = process.env.API_KEY
if (!API_KEY) throw new Error('API_KEY environment variable required')
```

### Shell Injection Prevention

User input must never be interpolated directly into shell commands:

```
# Dangerous
exec(`rm -rf ${userInput}`)

# Safe — use parameterized execution
spawn('rm', ['-rf', sanitizedPath])
```

### Principle of Least Privilege

- Request only the permissions your code needs
- Expose only the APIs your consumers need
- Store only the data your features need
- Grant only the access your users need

### Dependency Hygiene

- **Audit dependencies** — Fewer dependencies means fewer attack vectors
- **Pin versions** — Lock files prevent supply-chain surprises
- **Review updates** — Don't blindly upgrade. Read changelogs
- **Prefer well-maintained libraries** — Check commit activity, issue response time, and download counts before adopting

### No `eval`

Never execute dynamically constructed code from user input:

```
# Never
eval(userString)
new Function(userCode)()

# If dynamic execution is truly needed, sandbox it
spawn('node', ['--experimental-vm-modules', scriptPath])
```

---

## Testing

### Tests Are Required

All new logic requires tests. Extract pure functions into testable modules and co-locate tests alongside the source:

```
src/
  formatters.ts
  formatters.test.ts
  validators.ts
  validators.test.ts
```

### What to Test

- **Pure functions** — Formatters, validators, transformations, filters
- **Edge cases** — Null, undefined, empty strings, boundary values
- **Error paths** — What happens when things fail?
- **Regressions** — Every bug fix gets a test that would have caught it

### What Not to Test

- **Framework internals** — Don't test that React renders or Electron opens a window
- **Trivial code** — A one-line getter doesn't need a test
- **Implementation details** — Test behavior, not internal state

### Test Structure

```
describe('formatDate', () => {
    it('returns "Today" for today\'s date', () => { ... })
    it('returns "Tomorrow" for tomorrow\'s date', () => { ... })
    it('returns null for null input', () => { ... })
    it('detects overdue dates', () => { ... })
})
```

Use descriptive `it` strings that read as specifications. A failing test name should tell you what broke without reading the test body.

### Run Before Committing

Typecheck and tests must pass before every commit. CI should gate on both:

```bash
npm run typecheck && npm test   # or equivalent
```

---

## Git Conventions

### Commit Messages

```
<type>: <short description>

<optional body explaining why>
```

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code change that neither fixes nor adds
- `docs` — Documentation only
- `style` — Formatting, no code change
- `test` — Adding or updating tests
- `chore` — Build, tooling, dependencies

**Examples:**
```
feat: Add keyboard shortcut for quick search
fix: Prevent crash when config file is missing
refactor: Extract validation into separate module
docs: Update installation instructions
```

### Branch Naming

```
feature/keyboard-shortcuts
fix/missing-config-crash
refactor/validation-module
```

---

*Standards serve consistency, not rigidity. When they get in the way of good work, update the standards.*
