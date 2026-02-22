# MCP Server Coding Standards

Standards for building Model Context Protocol (MCP) servers in JavaScript/Node.js.

## Language & Framework

- **Language**: Plain JavaScript (no TypeScript)
- **Runtime**: Node.js 18+
- **Protocol**: MCP via `@modelcontextprotocol/sdk`
- **Transport**: STDIO for Claude Desktop integration
- **Testing**: Vitest

## File Organization

```
mcp-project/
├── src/
│   ├── index.js              # Entry point (shebang, transport setup)
│   ├── server.js             # MCP server creation, request handlers
│   ├── tools/                # Tool implementations by domain
│   │   ├── index.js          # Aggregates all tools
│   │   ├── feature-a.js      # Tool definitions and handlers
│   │   └── feature-b.js
│   └── lib/                  # Pure logic modules (testable)
│       ├── client.js         # API client wrapper (singleton)
│       ├── validators.js     # Input validation
│       ├── formatters.js     # Response formatting
│       └── utils.js          # Shared utilities
├── test/
│   └── lib/                  # Unit tests for pure modules
├── CLAUDE.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── README.md
├── CHANGELOG.md
├── package.json
├── vitest.config.js
└── .gitignore
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | `kebab-case` | `date-utils.js` |
| Functions | `camelCase` | `validateDate()` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES` |
| Tool names | `snake_case` with prefix | `myapp_get_items` |

## Critical: Stdout is Reserved

**NEVER use `console.log()` in MCP servers.** The STDIO transport uses stdout for JSON-RPC protocol messages. Any extraneous output corrupts the protocol.

```javascript
// WRONG - breaks MCP protocol
console.log('Debug message');

// CORRECT - use stderr for all logging
console.error('Debug message');
```

## Tool Definition Pattern

Each tool file exports two things:

```javascript
// Tool definitions for MCP registration
const toolDefinitions = [
  {
    name: 'myapp_get_items',
    description: 'Get all items. Use this to list available items.',
    inputSchema: {
      type: 'object',
      properties: {
        search: {
          type: 'string',
          description: 'Optional search filter',
        },
        limit: {
          type: 'number',
          description: 'Maximum items to return (default: 50)',
        },
      },
    },
  },
  {
    name: 'myapp_create_item',
    description: 'Create a new item.',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Item name',
        },
      },
      required: ['name'],
    },
  },
];

// Handler functions (one per tool)
async function handleGetItems(params) { ... }
async function handleCreateItem(params) { ... }

const handlers = {
  'myapp_get_items': handleGetItems,
  'myapp_create_item': handleCreateItem,
};

module.exports = { toolDefinitions, handlers };
```

## Tool Handler Pattern

Every tool handler should follow this structure:

```javascript
async function handleCreateItem(params) {
  // 1. Validate inputs
  const validation = validateItemInput(params);
  if (!validation.valid) {
    return errorResponse(validation.error);
  }

  try {
    // 2. Get client and perform operation
    const client = await getClient();
    const result = await client.createItem(params);

    // 3. Format and return success response
    return successResponse({
      success: true,
      message: 'Item created',
      item: formatItemForResponse(result),
    });
  } catch (err) {
    // 4. Log to stderr and return error response
    console.error('Error creating item:', err);
    return errorResponse(`Failed to create item: ${err.message}`);
  }
}
```

## Response Helpers

Always use consistent response helpers:

```javascript
function successResponse(data) {
  return {
    content: [{
      type: 'text',
      text: JSON.stringify(data, null, 2),
    }],
  };
}

function errorResponse(message) {
  return {
    isError: true,
    content: [{
      type: 'text',
      text: message,
    }],
  };
}
```

**Key rules:**
- Return errors in result objects, not as protocol-level errors
- This allows Claude to see and handle errors gracefully
- Always include `isError: true` for error responses

## Singleton Client Pattern

External API clients should use lazy-initialized singletons:

```javascript
let clientInstance = null;
let connectionPromise = null;

async function getClient() {
  if (clientInstance) {
    return clientInstance;
  }

  if (connectionPromise) {
    return connectionPromise;
  }

  connectionPromise = (async () => {
    const email = process.env.MY_API_EMAIL;
    const password = process.env.MY_API_PASSWORD;

    if (!email || !password) {
      throw new Error('Credentials required');
    }

    const client = new MyAPIClient({ email, password });
    await client.connect();

    clientInstance = client;
    return client;
  })();

  return connectionPromise;
}
```

**Key principles:**
- Lazy initialization on first tool use
- Single instance shared across all tool calls
- Credentials from environment variables only
- Disable real-time features (WebSocket) for stateless MCP tools

## Input Validation

Extract validation into pure functions for testability:

```javascript
function validateDate(dateString) {
  if (!dateString) {
    return { valid: false, error: 'Date is required' };
  }

  if (typeof dateString !== 'string') {
    return { valid: false, error: 'Date must be a string' };
  }

  const date = parseDate(dateString);
  if (!date) {
    return { valid: false, error: 'Invalid date format. Use YYYY-MM-DD' };
  }

  return { valid: true };
}
```

## Response Formatting

Extract formatting into pure functions:

```javascript
function formatItemForResponse(item) {
  return {
    id: item.identifier,
    name: item.name || '',
    createdAt: formatDateValue(item.createdAt),
    // Normalize null/undefined to consistent values
    description: item.description || null,
  };
}
```

**Key principles:**
- Use `id` not `identifier` in responses (cleaner for Claude)
- Normalize missing values (empty string for required, null for optional)
- Format dates consistently (YYYY-MM-DD)

## Server Entry Point

```javascript
#!/usr/bin/env node

const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { createServer } = require('./server.js');

async function main() {
  const server = createServer();
  const transport = new StdioServerTransport();

  await server.connect(transport);

  // Log to stderr only
  console.error('MCP server started');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

## Server Setup

```javascript
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const { getAllTools, getHandler } = require('./tools/index.js');

function createServer() {
  const server = new Server(
    { name: 'my-mcp-server', version: '1.0.0' },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: getAllTools() };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = getHandler(name);

    if (!handler) {
      return errorResponse(`Unknown tool: ${name}`);
    }

    try {
      return await handler(args || {});
    } catch (error) {
      console.error(`Error in tool ${name}:`, error);
      return errorResponse(`Tool error: ${error.message}`);
    }
  });

  return server;
}
```

## Testing Strategy

### What to Test

- **Pure functions** in `lib/` (validators, formatters, utils)
- **Edge cases** (null, undefined, empty, invalid input)
- **Boundary conditions** (date limits, string lengths)

### What NOT to Test

- Tool handlers directly (require mock client)
- Server setup (framework behavior)
- MCP protocol (SDK responsibility)

### Test Structure

```javascript
import { describe, it, expect } from 'vitest';
import { validateDate } from '../../src/lib/validators.js';

describe('validateDate', () => {
  it('accepts valid YYYY-MM-DD format', () => {
    expect(validateDate('2024-03-15')).toEqual({ valid: true });
  });

  it('rejects invalid format', () => {
    const result = validateDate('03/15/2024');
    expect(result.valid).toBe(false);
    expect(result.error).toContain('YYYY-MM-DD');
  });

  it('handles null input', () => {
    const result = validateDate(null);
    expect(result.valid).toBe(false);
    expect(result.error).toContain('required');
  });
});
```

## Package.json Configuration

```json
{
  "name": "mcp-myapp",
  "version": "1.0.0",
  "main": "src/index.js",
  "bin": {
    "mcp-myapp": "src/index.js"
  },
  "type": "commonjs",
  "scripts": {
    "start": "node src/index.js",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.0"
  },
  "devDependencies": {
    "vitest": "^3.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Common Gotchas

1. **No stdout** - Always use `console.error()` for logging
2. **Stateless tools** - No WebSocket connections; tools should be request-response
3. **Date format** - Use ISO format (YYYY-MM-DD) for consistency
4. **Error in results** - Return errors as result objects, not thrown exceptions
5. **Singleton client** - Initialize once, reuse across all tool calls
6. **Environment credentials** - Never hardcode credentials; use env vars

## Documentation Requirements

Every MCP project should include:

| Document | Purpose |
|----------|---------|
| `README.md` | Installation, configuration, tool reference |
| `CLAUDE.md` | AI session context (key files, patterns, gotchas) |
| `ARCHITECTURE.md` | Data flow, module responsibilities |
| `ROADMAP.md` | Current sprint, backlog, version history |
| `CHANGELOG.md` | Version changes (Keep a Changelog format) |
