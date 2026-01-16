# TYPO3 Development Plugin for Claude Code

A comprehensive plugin for TYPO3 developers that automates workflows with specific tools, validations, and best practices enforcement.

## 🎯 Overview

This plugin extends Claude Code with TYPO3-specific functionality:
- **Slash Commands** for extension scaffolding and code generation
- **Skills** for automatic coding standards compliance
- **Agents** for code validation and migration assistance
- **Hooks** for automated quality checks
- **MCP Servers** for TYPO3 documentation and browser testing

## ✨ Features

### 📝 Slash Commands

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

### 🤖 Skills (auto-activated)

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

### 🔍 Agents

| Agent | Description |
|-------|-------------|
| `typo3-validator` | Validates code against TYPO3 CGL and best practices |
| `typo3-migration-assistant` | Helps with major version upgrades (v11→v12→v13) |
| `typo3-security-scanner` | Finds security vulnerabilities (OWASP Top 10) |
| `tca-validator` | Validates TCA configurations and column types |
| `typoscript-analyzer` | Analyzes TypoScript for deprecated syntax |

### 🪝 Hooks

| Event | Action |
|-------|--------|
| `SessionStart` | Loads TYPO3 CGL + detects project config (.claude/typo3-project.json) |
| `PreToolUse: Write/Edit PHP` | Validates TYPO3 best practices before saving |
| `PreToolUse: Write/Edit HTML` | Checks Fluid templates for anti-patterns |
| `PreToolUse: Write/Edit TCA` | Validates TCA configuration |
| `PostToolUse: Write PHP` | Runs PHP CS Fixer (if available) |
| `PostToolUse: ext_tables.sql` | Reminds to run `extension:setup` |
| `UserPromptSubmit` | Context-aware suggestions (controller, model, query, etc.) |

### 🌐 MCP Server Integration

#### TYPO3 Documentation Server (with real TER API)
- **search_typo3_docs** - Search docs.typo3.org with curated links
- **get_typo3_changelog** - Browse TYPO3 Core Changelog (v11/v12/v13)
- **search_typo3_extensions** - Search TER with real API calls
- **get_extension_detail** - Get detailed extension info from TER
- **get_typo3_api_reference** - TYPO3 Core API Reference with examples
- **get_typo3_coding_guidelines** - Official CGL reference (PHP, DB, Fluid, Security)

#### Chrome DevTools Integration
Test TYPO3 frontend directly in the browser:
- Take viewport/full-page screenshots
- Inspect DOM and accessibility tree
- Monitor network requests
- Run automated tests (click, type, navigate)
- Analyze Core Web Vitals performance

See [Chrome DevTools Documentation](./docs/CHROME-DEVTOOLS.md)

## 📦 Installation

### Via Plugin Manager (Recommended)

```bash
# Open Claude Code plugin manager
/plugin

# Add marketplace and install
/plugin marketplace add PatFischer91/typo3_development
/plugin install typo3-development@typo3-development-marketplace
```

### Via CLI

```bash
claude plugin marketplace add PatFischer91/typo3_development
claude plugin install typo3-development@typo3-development-marketplace
```

### Manual Installation

```bash
git clone https://github.com/PatFischer91/typo3_development.git ~/.claude/plugins/typo3-development-marketplace
```

### MCP Server Requirements (Optional)

```bash
# For TYPO3 Docs Server
pip install mcp httpx

# For Chrome DevTools
npm install -g @anthropic-ai/mcp-devtools-server
```

See [Installation Guide](./docs/INSTALLATION.md) for detailed instructions.

## 🚀 Quick Start

**Auto-Detection:** When you open a TYPO3 project that hasn't been initialized yet (no `CLAUDE.md` in project root), the plugin automatically detects your TYPO3 version and configures itself. No manual setup needed!

For deeper analysis, you can optionally run:
```
/typo3:init
```

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

4. **Add tests**:
   ```
   /typo3:test ProductService functional
   ```

5. **Prepare for upgrade**:
   ```
   /typo3:upgrade 11.5 12.4
   ```

## 🛠️ Configuration

### Built-in Guidelines

The plugin includes **complete TYPO3 Coding Guidelines** loaded at session start:
- PSR-12 PHP Coding Standards
- TYPO3-specific conventions (`defined('TYPO3') || die();`)
- Modern patterns (DI, QueryBuilder, ResponseInterface)
- Security best practices

### Optional Project Configuration

Create `.claude/typo3-config.json`:

```json
{
  "typo3Version": "12.4",
  "extensionKey": "my_extension",
  "vendorName": "MyVendor",
  "autoEnforce": {
    "codingStandards": true,
    "dependencyInjection": true,
    "securityChecks": true,
    "fluidValidation": true
  },
  "phpCSFixerPath": "vendor/bin/php-cs-fixer"
}
```

## 📚 Documentation

- [Installation Guide](./docs/INSTALLATION.md) - How to install the plugin
- [Feature Reference](./docs/FEATURES.md) - Complete feature documentation
- [Chrome DevTools](./docs/CHROME-DEVTOOLS.md) - Browser testing setup

## 🔧 Directory Structure

```
typo3_development/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest
├── typo3-development/        # Plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json       # Plugin metadata
│   ├── commands/             # 14 Slash commands
│   │   ├── init.md           # Project initialization
│   │   ├── extension.md
│   │   ├── model.md
│   │   └── ...
│   ├── skills/               # 9 Auto-activated skills
│   │   ├── typo3-coding-standards/
│   │   ├── extbase-patterns/
│   │   └── ...
│   ├── agents/               # 5 Specialized agents
│   │   ├── typo3-validator/
│   │   ├── typo3-migration-assistant/
│   │   └── ...
│   ├── hooks/
│   │   └── hooks.json        # Event-driven automation
│   ├── mcp/
│   │   └── typo3-docs-server/  # TYPO3 Documentation MCP
│   └── .mcp.json             # MCP configuration
├── docs/                     # Documentation
└── README.md
```

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch
3. Follow TYPO3 CGL
4. Submit pull request

## 📄 License

MIT License

## 🔗 Links

- [TYPO3 CMS](https://typo3.org)
- [TYPO3 Documentation](https://docs.typo3.org)
- [TYPO3 Coding Guidelines](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

**Version**: 0.3.0 | **Status**: 🚧 Beta
