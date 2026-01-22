# TYPO3 Development Plugins for Claude Code

A comprehensive collection of plugins for TYPO3 developers that automates workflows with specific tools, validations, and the enforcement of best practices.

## Overview available Plugins

### Plugin: TYPO3-Dev
This plugin extends Claude Code with tailored capabilities for TYPO3 development and code generation:
- **Slash Commands** for extension scaffolding, code generation, and documentation access
- **Skills** for automatic coding standards compliance and browser testing
- **Agents** for code validation, migration assistance, and automated testing
- **Hooks** for automated quality checks
- **Chrome DevTools** for browser-based testing and debugging

#### Features

###### Slash Commands

| Command | Description |
|---------|-------------|
| `/typo3:init` | Deep project analysis (auto-runs on new projects, manual for detailed config) |
| `/typo3:extension` | Creates complete extension structure with best practices |
| `/typo3:model` | Generates Domain Model + Repository + TCA + SQL |
| `/typo3:plugin` | Creates plugin with Controller, Templates, FlexForm |
| `/typo3:controller` | Creates slim Extbase Controller with DI |
| `/typo3:viewhelper` | Generates custom Fluid ViewHelper |
| `/typo3:middleware` | Creates PSR-15 Middleware |
| `/typo3:upgrade` | Assists with TYPO3 version upgrades |
| `/typo3:test` | Creates Unit/Functional Tests |
| `/typo3:migration` | Creates Doctrine DBAL Migration |
| `/typo3:scheduler` | Creates Scheduler Task |
| `/typo3:flexform` | Generates FlexForm XML configuration |
| `/typo3:event` | Creates PSR-14 Event + Listener |
| `/typo3:command` | Creates Symfony Console Command |
| `/typo3:docs` | Search TYPO3 official documentation |
| `/typo3:changelog` | Get TYPO3 Core changelog for version upgrades |
| `/typo3:ter` | Search TYPO3 Extension Repository |
| `/typo3:api` | Get TYPO3 Core API reference with examples |
| `/typo3:cgl` | Get TYPO3 Coding Guidelines reference |
| `/typo3:test-browser` | Test TYPO3 frontend/backend in Chrome browser |
| `/typo3:code-simplify` | Automatically refactor and clean up TYPO3 code (behavior-preserving) |

###### Skills (auto-activated)

| Skill | Description |
|-------|-------------|
| `typo3-coding-standards` | Monitors PSR-12 and TYPO3 CGL compliance |
| `extbase-patterns` | Suggests modern Extbase patterns, slim controllers |
| `fluid-best-practices` | Prevents business logic in templates |
| `dependency-injection` | Prefers constructor DI over static calls |
| `security-awareness` | Warns about XSS, SQL injection, CSRF |
| `doctrine-dbal` | Uses QueryBuilder with named parameters |
| `typo3-api` | Knows TYPO3 Core APIs (Caching, Logging, FAL) |
| `content-blocks` | Guides TYPO3 v13+ Content Block creation |
| `project-aware` | Adapts to detected TYPO3 version (v11/v12/v13) |
| `browser-testing` | Knowledge for testing TYPO3 in Chrome browser |

###### Agents

| Agent | Description |
|-------|-------------|
| `typo3-validator` | Validates code against TYPO3 CGL and best practices |
| `typo3-migration-assistant` | Helps with major version upgrades (v11→v12→v13) |
| `typo3-security-scanner` | Finds security vulnerabilities (OWASP Top 10) |
| `tca-validator` | Validates TCA configurations and column types |
| `typoscript-analyzer` | Analyzes TypoScript for deprecated syntax |
| `typo3-browser-tester` | Automated browser testing for frontend and backend |

###### Hooks

| Event | Action |
|-------|--------|
| `SessionStart` | Loads TYPO3 CGL + detects project config (.claude/typo3-project.json) |
| `PreToolUse: Write/Edit PHP` | Validates TYPO3 best practices before saving |
| `PreToolUse: Write/Edit HTML` | Checks Fluid templates for anti-patterns |
| `PreToolUse: Write/Edit TCA` | Validates TCA configuration |
| `PreToolUse: Bash (git commit)` | **Intelligent code-simplify suggestions** (pre-commit + session-based) |
| `PreToolUse: Write/Edit (all)` | Tracks session activity for intelligent suggestions |
| `PostToolUse: Write PHP` | Runs PHP CS Fixer (if available) |
| `PostToolUse: ext_tables.sql` | Reminds to run `extension:setup` |

**Intelligent Hook Details:**

The code-simplify hook is **smart and non-intrusive** - it suggests running the simplifier at the right times:
- **Pre-commit:** Always shows gentle suggestion when committing changes
- **Session-based:** After 30+ minutes of active coding with significant changes
- **Smart cooldown:** Won't suggest again for 15 minutes after successful run
- **Context-aware:** Adapts suggestion strength based on changes and session duration
- **Never blocking:** All suggestions are optional, workflow continues normally

Philosophy: **Helpful, not annoying** - respects your workflow while encouraging code quality.

###### Chrome DevTools Integration

Browser automation and testing for TYPO3 development:
- Take viewport/full-page screenshots
- Inspect DOM and accessibility tree
- Monitor network requests and console messages
- Automated form testing and submissions
- Backend module testing with login
- Visual regression testing
- Performance analysis

See [Chrome DevTools Documentation](typo3-dev/docs/CHROME-DEVTOOLS.md)

#### Installation

###### Via Plugin Manager (Recommended)

```bash
# Open Claude Code plugin manager
/plugin

# Add marketplace and install
/plugin marketplace add PatFischer91/claude-typo3-dev
/plugin install typo3-dev@in2code
```

###### Via CLI

```bash
claude plugin marketplace add PatFischer91/claude-typo3-dev
claude plugin install typo3-dev@in2code
```

###### Manual Installation

```bash
git clone https://github.com/PatFischer91/claude-typo3-dev.git ~/.claude/plugins/in2code
```

###### Requirements

- **Chrome DevTools**: Requires `npx` (comes with Node.js) for browser testing features

See [Installation Guide](typo3-dev/docs/INSTALLATION.md) for detailed instructions.

#### Quick Start

**Auto-Detection:** When you open a TYPO3 project that hasn't been initialized yet (no `CLAUDE.md` in project root), the plugin automatically detects your TYPO3 version and configures itself. No manual setup needed!

For deeper analysis, you can optionally run:
```
/typo3:init
```

#### Code Simplifier

Automatically refactor and clean up TYPO3 code following best practices:

**Quick Start:**
```bash
/typo3:code-simplify
```

**Features:**
- ✅ **Behavior-preserving** refactoring (outputs, APIs, security unchanged)
- ✅ PSR-12 formatting and code style
- ✅ TYPO3 best practices (DI, QueryBuilder, Extbase patterns)
- ✅ Security review (XSS, SQL injection prevention)
- ✅ Version-aware (TYPO3 11/12/13)
- ✅ Respects existing project tooling (PHP CS Fixer, PHPStan, Rector)
- ✅ Intelligent hook system (suggests before commits, non-intrusive)
- ✅ Smart defaults (auto-detects changed files)

**What It Does:**
- Formatting & consistency (PSR-12, imports, whitespace)
- Readability improvements (extract methods, reduce nesting)
- TYPO3 patterns (DI, QueryBuilder, slim controllers)
- Security hardening (escaping, SQL injection prevention)
- Generates detailed reports with "What was NOT changed" section

**What It Does NOT Do:**
- ❌ Does NOT change functionality or behavior
- ❌ Does NOT modify public APIs
- ❌ Does NOT weaken security
- ❌ Uncertain changes become proposals (you decide)

**Intelligent Hook:**
- Pre-commit suggestions (gentle reminders)
- Session-based triggers (after 30+ min of coding)
- Smart cooldown (15-min after run)
- Never annoying, always helpful

See: [Code Simplifier Guide](typo3-dev/docs/CODE-SIMPLIFIER.md)

#### Common Workflows

1. **Create new extension**:
   ```
   /typo3:extension my_shop MyVendor "Online shop extension"
   ```

2. **Generate domain model**:
   ```
   /typo3:model Product "title:string,price:float,stock:int,active:bool"
   ```

3. **Create plugin**:
   ```
   /typo3:plugin ProductList "List products"
   ```

4. **Search documentation**:
   ```
   /typo3:docs QueryBuilder 12.4
   ```

5. **Test in browser**:
   ```
   /typo3:test-browser frontend https://mysite.ddev.site/
   ```

6. **Prepare for upgrade**:
   ```
   /typo3:upgrade 11.5 12.4
   ```

#### Configuration

###### Built-in Guidelines

The plugin includes **complete TYPO3 Coding Guidelines** loaded at session start:
- PSR-12 PHP Coding Standards
- TYPO3-specific conventions (`defined('TYPO3') || die();`)
- Modern patterns (DI, QueryBuilder, ResponseInterface)
- Security best practices
``
###### Project Configuration

Run `/typo3:init` to analyze your TYPO3 project and write comprehensive configuration to `CLAUDE.md`:
- Auto-detects TYPO3 version, extensions, project type (DDEV/Docker/Composer)
- Discovers development tools (PHP CS Fixer, PHPStan, Rector)
- Identifies site configurations and languages
- Applies version-specific guidelines

The plugin uses standard Claude Code `CLAUDE.md` approach - no separate JSON files needed.

For detailed information, see the [Configuration Guide](typo3-dev/docs/CONFIGURATION.md).``

#### Documentation

- [Installation Guide](./typo3-dev/docs/INSTALLATION.md) - How to install the plugin
- [Configuration Guide](typo3-dev/docs/CONFIGURATION.md) - Project configuration options
- [Feature Reference](typo3-dev/docs/FEATURES.md) - Complete feature documentation
- [Chrome DevTools](typo3-dev/docs/CHROME-DEVTOOLS.md) - Browser testing setup

#### Directory Structure

```
typo3_development/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest
├── typo3-dev/                # Plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json       # Plugin metadata
│   ├── commands/             # 20 Slash commands
│   │   ├── init.md           # Project initialization
│   │   ├── extension.md      # Extension scaffolding
│   │   ├── model.md          # Domain model generation
│   │   ├── docs.md           # Documentation search
│   │   ├── test-browser.md   # Browser testing
│   │   └── ...
│   ├── skills/               # 10 Auto-activated skills
│   │   ├── typo3-coding-standards/
│   │   ├── browser-testing/
│   │   └── ...
│   ├── agents/               # 6 Specialized agents
│   │   ├── typo3-validator/
│   │   ├── typo3-browser-tester/
│   │   └── ...
│   ├── hooks/
│   │   └── hooks.json        # Event-driven automation
│   └── .mcp.json             # MCP configuration (Chrome DevTools)
├── docs/                     # Documentation
└── README.md
```

## License

MIT License

## Links

- [TYPO3 CMS](https://typo3.org)
- [TYPO3 Documentation](https://docs.typo3.org)
- [TYPO3 Coding Guidelines](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

**Version**: 1.1.0 | **Status**: Stable
