# TYPO3 Development Plugin - Architecture

## Overview

This document describes the technical architecture and design decisions for the TYPO3 Development Plugin for Claude Code.

## Plugin Components

### 1. Slash Commands (`/commands/`)

Slash commands provide explicit, user-invoked workflows for common TYPO3 development tasks.

**Design Principles:**
- Each command is self-contained and focused on a single task
- Commands use `$ARGUMENTS` for dynamic parameters
- Pre-execution validation ensures correct context
- Commands follow TYPO3 CGL and best practices

**Implemented Commands:**

#### `/typo3:extension`
Creates a complete TYPO3 extension structure including:
- `composer.json` with proper dependencies
- `ext_emconf.php` with metadata
- Directory structure (`Classes/`, `Resources/`, `Configuration/`)
- `ext_tables.sql` for database schema
- TCA configuration files
- Automatically includes `defined('TYPO3') || die();` guards

**Parameters:** `extension_key` `vendor_name`

#### `/typo3:model`
Generates a complete Domain Model setup:
- Extbase Domain Model class with properties, getters, setters
- Repository class with custom queries
- TCA configuration
- Database schema in `ext_tables.sql`
- Doctrine DBAL migration (optional)

**Parameters:** `ModelName` `description`

#### `/typo3:plugin`
Creates a frontend plugin:
- Slim Controller with Dependency Injection
- Fluid template structure (Templates, Partials, Layouts)
- TypoScript configuration (setup.typoscript)
- FlexForm for plugin configuration
- Registration in `ext_localconf.php`

**Parameters:** `PluginName`

#### `/typo3:controller`
Generates an Extbase Controller following best practices:
- Slim controller (minimal business logic)
- Constructor-based Dependency Injection
- Proper action methods
- ViewHelper registration
- No `$GLOBALS['TSFE']` usage

**Parameters:** `ControllerName`

#### `/typo3:viewhelper`
Creates a custom Fluid ViewHelper:
- Proper namespace and class structure
- Type-hinted arguments
- Render method implementation
- Documentation comments
- Registration in `ext_localconf.php`

**Parameters:** `ViewHelperName`

#### `/typo3:middleware`
Generates PSR-15 Middleware:
- Proper interface implementation
- Request/Response handling
- Registration in `Configuration/RequestMiddlewares.php`
- Dependency Injection support

**Parameters:** `MiddlewareName`

#### `/typo3:upgrade`
Assists with TYPO3 version upgrades:
- Scans codebase for deprecated code
- Suggests migration paths
- Identifies breaking changes
- Proposes refactoring (e.g., `getUrl()` → `RequestFactory`)
- Checks `$GLOBALS['TSFE']` usage

**Parameters:** `from_version` `to_version`

#### `/typo3:test`
Creates test files:
- Unit tests with TYPO3 Testing Framework
- Functional tests with database fixtures
- Proper test class structure
- Mocking setup for repositories/services

**Parameters:** `TestClassName`

#### `/typo3:migration`
Creates Doctrine DBAL migration:
- Migration class with up/down methods
- Schema modifications
- Data migrations
- Proper naming convention

**Parameters:** `MigrationDescription`

#### `/typo3:scheduler`
Creates a Scheduler Task:
- Scheduler Task class
- Registration in `ext_localconf.php`
- Task fields definition
- Execute method implementation

**Parameters:** `TaskName`

---

### 2. Skills (`/skills/`)

Skills are automatically invoked by Claude when their description matches the task context. They provide continuous guidance without explicit user invocation.

**Design Principles:**
- Descriptions must be precise (Claude uses these to match tasks)
- Skills should be contextual and non-invasive
- Each skill focuses on a specific aspect of TYPO3 development
- Skills can include executable scripts for validation

**Implemented Skills:**

#### `typo3-coding-standards/`
**Description:** "Enforces TYPO3 Coding Guidelines (CGL) including PSR-12 compliance, proper namespacing, and TYPO3-specific conventions. Use when writing or reviewing PHP code for TYPO3."

**Behavior:**
- Validates PSR-12 compliance
- Checks for `defined('TYPO3') || die();` in configuration files
- Ensures proper vendor/extension namespacing
- Validates class naming conventions
- Checks file structure and organization

**Files:**
- `SKILL.md` - Instructions for Claude
- `validate.sh` - Optional PHP_CodeSniffer integration

#### `extbase-patterns/`
**Description:** "Suggests modern Extbase framework patterns including slim controllers, proper repository usage, and Doctrine DBAL queries. Use when developing Extbase extensions or refactoring legacy code."

**Behavior:**
- Promotes slim controllers (no business logic)
- Suggests service classes for complex logic
- Recommends repository patterns
- Guides proper QueryBuilder usage
- Warns against `$GLOBALS['TSFE']` access

#### `fluid-best-practices/`
**Description:** "Prevents business logic in Fluid templates and promotes proper ViewHelper usage. Use when working with Fluid templates, ViewHelpers, or frontend rendering."

**Behavior:**
- Detects business logic in templates
- Suggests ViewHelper creation for complex logic
- Validates Fluid syntax
- Recommends Partials/Layouts for reusability
- Checks for XSS vulnerabilities in unescaped output

#### `dependency-injection/`
**Description:** "Promotes constructor-based Dependency Injection over static utility calls and ObjectManager usage. Use when creating classes, controllers, or services."

**Behavior:**
- Detects `GeneralUtility::makeInstance()`
- Suggests constructor injection
- Guides proper service configuration
- Warns against ObjectManager usage (deprecated)
- Recommends autowiring in `Services.yaml`

#### `security-awareness/`
**Description:** "Identifies security vulnerabilities in TYPO3 code including XSS, SQL injection, and insecure data handling. Use when handling user input, database queries, or rendering output."

**Behavior:**
- Detects direct `$_GET`, `$_POST`, `$_SESSION` access
- Warns about unsanitized output in Fluid
- Validates QueryBuilder parameter binding
- Checks for `htmlspecialchars()` usage
- Identifies potential CSRF issues

#### `doctrine-dbal/`
**Description:** "Guides proper Doctrine DBAL and QueryBuilder usage instead of deprecated database methods. Use when writing database queries or migrations."

**Behavior:**
- Detects deprecated `$GLOBALS['TYPO3_DB']`
- Suggests QueryBuilder patterns
- Validates parameter binding
- Recommends Repository methods
- Guides Connection usage from ConnectionPool

#### `typo3-api/`
**Description:** "Provides knowledge of TYPO3 Core APIs, their proper usage, and common patterns. Use when working with TYPO3 Core functionality like caching, logging, or file handling."

**Behavior:**
- Suggests proper API usage (CacheManager, Logger, FAL)
- Recommends `RequestFactory` over `getUrl()`
- Guides Event Dispatcher usage
- Validates PSR-7 Request/Response handling
- Suggests modern replacements for deprecated APIs

---

### 3. Agents (`/agents/`)

Agents are specialized sub-processes with isolated context and specific tool access. They handle complex, multi-step validation and analysis tasks.

**Design Principles:**
- Each agent has a focused expertise area
- Agents operate independently with isolated context
- Results are returned to main Claude session
- Agents can run in parallel for efficiency

**Implemented Agents:**

#### `typo3-validator/`
**Purpose:** Comprehensive code validation against TYPO3 CGL and best practices

**Process:**
1. Scans provided files or entire extension
2. Validates PSR-12 compliance
3. Checks TYPO3-specific conventions
4. Validates TCA structure and syntax
5. Returns detailed violation report with line numbers

**Tools:** Glob, Grep, Read, custom validation scripts

#### `typo3-migration-assistant/`
**Purpose:** Assists with major TYPO3 version upgrades

**Process:**
1. Identifies current TYPO3 version usage
2. Analyzes changelog for breaking changes
3. Scans codebase for deprecated methods
4. Generates migration recommendations
5. Proposes code refactoring steps
6. Creates migration checklist

**Tools:** WebFetch (for changelog), Grep, Read

#### `typo3-security-scanner/`
**Purpose:** Identifies security vulnerabilities in TYPO3 code

**Process:**
1. Scans for common vulnerability patterns
2. Checks SQL injection risks in queries
3. Identifies XSS vulnerabilities in templates
4. Validates input sanitization
5. Checks authentication/authorization patterns
6. Returns security report with severity levels

**Tools:** Grep, Read, custom security rules

#### `tca-validator/`
**Purpose:** Validates TCA (Table Configuration Array) syntax and completeness

**Process:**
1. Reads TCA configuration files
2. Validates PHP array syntax
3. Checks required TCA keys
4. Validates field types and configurations
5. Ensures consistency with database schema
6. Returns validation errors and warnings

**Tools:** Read, Bash (php -l for syntax check)

#### `typoscript-analyzer/`
**Purpose:** Analyzes TypoScript code quality and performance

**Process:**
1. Parses TypoScript files
2. Identifies deprecated TypoScript
3. Suggests performance optimizations
4. Validates syntax
5. Checks for common anti-patterns
6. Returns analysis report

**Tools:** Read, Grep, custom TypoScript parser

---

### 4. Hooks (`/hooks/hooks.json`)

Hooks provide event-driven automation that runs at specific lifecycle points.

**Design Principles:**
- Hooks should be fast and non-intrusive
- Use shell commands for performance
- Use LLM-based hooks only when necessary
- Fail gracefully without blocking user workflow

**Implemented Hooks:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "prompt",
        "prompt": "Load TYPO3 Coding Guidelines from https://github.com/in2code-de/claude-code-instructions/blob/main/CLAUDE.md and apply them throughout this session."
      }
    ],

    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Before writing PHP code, ensure it follows TYPO3 CGL: PSR-12 compliance, proper namespacing, defined('TYPO3') || die(); in config files, and no deprecated methods."
          }
        ]
      }
    ],

    "PostToolUse": [
      {
        "matcher": "Write.*\\.php$",
        "hooks": [
          {
            "type": "command",
            "command": "[ -f vendor/bin/php-cs-fixer ] && vendor/bin/php-cs-fixer fix $FILE --rules=@PSR12 || true"
          }
        ]
      }
    ],

    "UserPromptSubmit": [
      {
        "matcher": "controller|model|repository",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Consider suggesting TYPO3 best practices: slim controllers, dependency injection, proper repository patterns, and avoiding $GLOBALS['TSFE']."
          }
        ]
      }
    ]
  }
}
```

**Hook Events:**

- **SessionStart**: Load TYPO3 guidelines at session start
- **PreToolUse**: Validate before writing code
- **PostToolUse**: Run PHP CS Fixer after file creation
- **UserPromptSubmit**: Provide contextual suggestions based on user input

---

### 5. MCP Server (`/mcp/`)

MCP (Model Context Protocol) servers provide external tool integration for TYPO3-specific resources.

**Design Principles:**
- Servers should be stateless and fast
- Cache responses where appropriate
- Provide clear error messages
- Follow MCP specification

**Implemented MCP Server:**

#### `typo3-docs-server/`

**Purpose:** Provides access to TYPO3 documentation and resources

**Tools Exposed:**

1. **`search_docs`** - Search docs.typo3.org
   - Parameters: `query`, `version`
   - Returns: Relevant documentation pages with excerpts

2. **`get_changelog`** - Fetch TYPO3 Core changelog entries
   - Parameters: `version`, `type` (Breaking|Feature|Deprecation)
   - Returns: Changelog entries with details

3. **`search_ter`** - Search TYPO3 Extension Repository
   - Parameters: `query`, `typo3_version`
   - Returns: Extension list with ratings, compatibility

4. **`get_api_reference`** - Get TYPO3 Core API documentation
   - Parameters: `class_name` or `api_endpoint`
   - Returns: API reference with parameters and examples

**Implementation:** Python-based MCP server using `mcp` SDK

**Configuration (`.mcp.json`):**
```json
{
  "mcpServers": {
    "typo3-docs": {
      "command": "python",
      "args": ["mcp/typo3-docs-server/server.py"]
    }
  }
}
```

---

## Integration with TYPO3 Coding Guidelines

The plugin automatically integrates with the in2code Claude Code Instructions:
https://github.com/in2code-de/claude-code-instructions/blob/main/CLAUDE.md

**Key Guidelines Enforced:**

1. **PHP Coding Standards**
   - PSR-12 compliance
   - `defined('TYPO3') || die();` in config files (not `or die()`)
   - Proper namespacing (Vendor\ExtensionKey\)

2. **Framework Usage**
   - Modern Extbase/Fluid patterns
   - Doctrine DBAL instead of deprecated queries
   - Slim controllers (no business logic)
   - Dependency Injection via `__construct()`

3. **Security**
   - No direct `$_GET`, `$_POST`, `$_SESSION` access
   - RequestFactory instead of `curl_setopt()` or `getUrl()`
   - SQL queries only in Repositories
   - Avoid `$GLOBALS['TSFE']`

4. **Database Schema**
   - Don't define fields in `ext_tables.sql` if already in TCA
   - Use Doctrine migrations for schema changes
   - Proper indexing in SQL

5. **Architecture**
   - PHP logic in `Classes/Domain/`
   - No business logic in Fluid templates
   - Use Repository pattern for data access
   - Service classes for complex operations

---

## File Structure

```
typo3_development/
├── .claude-plugin/
│   └── plugin.json                    # Plugin metadata
│
├── commands/                           # Slash commands
│   ├── extension.md                   # /typo3:extension
│   ├── model.md                       # /typo3:model
│   ├── plugin.md                      # /typo3:plugin
│   ├── controller.md                  # /typo3:controller
│   ├── viewhelper.md                  # /typo3:viewhelper
│   ├── middleware.md                  # /typo3:middleware
│   ├── upgrade.md                     # /typo3:upgrade
│   ├── test.md                        # /typo3:test
│   ├── migration.md                   # /typo3:migration
│   └── scheduler.md                   # /typo3:scheduler
│
├── skills/                             # Auto-activated skills
│   ├── typo3-coding-standards/
│   │   ├── SKILL.md
│   │   └── validate.sh
│   ├── extbase-patterns/
│   │   └── SKILL.md
│   ├── fluid-best-practices/
│   │   └── SKILL.md
│   ├── dependency-injection/
│   │   └── SKILL.md
│   ├── security-awareness/
│   │   └── SKILL.md
│   ├── doctrine-dbal/
│   │   └── SKILL.md
│   └── typo3-api/
│       └── SKILL.md
│
├── agents/                             # Specialized validators
│   ├── typo3-validator/
│   │   └── agent.json
│   ├── typo3-migration-assistant/
│   │   └── agent.json
│   ├── typo3-security-scanner/
│   │   └── agent.json
│   ├── tca-validator/
│   │   └── agent.json
│   └── typoscript-analyzer/
│       └── agent.json
│
├── hooks/                              # Event handlers
│   └── hooks.json
│
├── mcp/                                # MCP servers
│   └── typo3-docs-server/
│       ├── server.py
│       ├── requirements.txt
│       └── README.md
│
├── .mcp.json                           # MCP configuration
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                # This file
│   ├── COMMANDS.md                    # Command reference
│   ├── SKILLS.md                      # Skills guide
│   ├── HOOKS.md                       # Hooks configuration
│   ├── MCP.md                         # MCP integration
│   └── DEVELOPMENT.md                 # Development guide
│
├── examples/                           # Example usage
│   ├── extension-scaffold/
│   ├── model-generation/
│   └── plugin-creation/
│
├── tests/                              # Plugin tests
│   ├── commands/
│   ├── skills/
│   └── integration/
│
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

---

## Development Workflow

### Adding a New Command

1. Create `commands/new-command.md`
2. Add YAML frontmatter with `description`
3. Write command instructions
4. Test with `/typo3:new-command`
5. Document in `docs/COMMANDS.md`

### Adding a New Skill

1. Create `skills/skill-name/` directory
2. Create `SKILL.md` with YAML frontmatter
3. Write precise description (200 chars max)
4. Add skill instructions
5. Optional: Add validation scripts
6. Test by triggering matching context
7. Document in `docs/SKILLS.md`

### Adding a New Agent

1. Create `agents/agent-name/` directory
2. Create `agent.json` with configuration
3. Define agent's tools and capabilities
4. Test agent execution
5. Document in agent-specific docs

### Adding a New Hook

1. Edit `hooks/hooks.json`
2. Choose appropriate event type
3. Add matcher pattern (optional)
4. Define hook action (command or prompt)
5. Test hook triggering
6. Document in `docs/HOOKS.md`

---

## Testing Strategy

### Command Testing
- Manual testing with various parameters
- Edge case handling
- Error message clarity

### Skill Testing
- Trigger contexts that should activate skill
- Verify skill provides correct guidance
- Ensure non-interference when not relevant

### Agent Testing
- Run agents on sample codebases
- Verify output accuracy
- Check performance and timeout handling

### Hook Testing
- Trigger hook events manually
- Verify hook execution
- Ensure graceful failure

### Integration Testing
- Test complete workflows (e.g., extension creation)
- Verify component interactions
- Test with real TYPO3 projects

---

## Performance Considerations

1. **Skills**: Keep descriptions concise for fast matching
2. **Hooks**: Prefer shell commands over LLM prompts
3. **MCP Server**: Cache documentation responses (15min TTL)
4. **Agents**: Use isolated context to prevent pollution
5. **Commands**: Minimize tool calls, maximize efficiency

---

## Future Enhancements

- [ ] LSP server integration for TYPO3 code intelligence
- [ ] Fluid template linting and validation
- [ ] TypoScript IntelliSense
- [ ] Automatic deprecation detection on save
- [ ] Integration with TYPO3 Rector rules
- [ ] Extension compatibility checker
- [ ] Performance profiling tools
- [ ] Database query analyzer
- [ ] TCA visual editor integration

---

## References

- [Claude Code Plugin Documentation](https://code.claude.com/docs/en/plugins)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [TYPO3 Coding Guidelines](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/)
- [in2code Claude Instructions](https://github.com/in2code-de/claude-code-instructions)
