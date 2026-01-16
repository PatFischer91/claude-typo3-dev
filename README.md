# TYPO3 Development Plugin for Claude Code

A comprehensive plugin for TYPO3 developers that automates workflows with specific tools, validations, and best practices enforcement.

## 🎯 Overview

This plugin extends Claude Code with TYPO3-specific functionality:
- **Slash Commands** for extension scaffolding and code generation
- **Skills** for automatic coding standards compliance
- **Agents** for code validation and migration assistance
- **Hooks** for automated quality checks
- **MCP Server** for TYPO3 documentation integration

## ✨ Features

### 📝 Slash Commands

| Command | Description |
|---------|-------------|
| `/typo3:extension` | Creates complete extension structure with best practices |
| `/typo3:model` | Generates Domain Model + Repository + TCA |
| `/typo3:plugin` | Creates plugin with Controller, Templates, and TypoScript |
| `/typo3:controller` | Creates slim Extbase Controller with DI |
| `/typo3:viewhelper` | Generates custom ViewHelper |
| `/typo3:middleware` | Creates PSR-15 Middleware |
| `/typo3:upgrade` | Assists with TYPO3 version upgrades |
| `/typo3:test` | Creates Unit/Functional Tests |
| `/typo3:migration` | Creates Doctrine DBAL Migration |
| `/typo3:scheduler` | Creates Scheduler Task |

### 🤖 Skills (auto-activated)

- **typo3-coding-standards** - Monitors TYPO3 CGL compliance
- **extbase-patterns** - Suggests modern Extbase patterns
- **fluid-best-practices** - Prevents business logic in templates
- **dependency-injection** - Prefers DI over static calls
- **security-awareness** - Warns about XSS, SQL injection, etc.
- **doctrine-dbal** - Uses QueryBuilder instead of deprecated methods
- **typo3-api** - Knows TYPO3 Core APIs and their usage

### 🔍 Agents

- **typo3-validator** - Validates code against TYPO3 CGL and best practices
- **typo3-migration-assistant** - Helps with major version upgrades
- **typo3-security-scanner** - Finds security vulnerabilities
- **tca-validator** - Validates TCA configurations
- **typoscript-analyzer** - Analyzes TypoScript code

### 🪝 Hooks

- **PreToolUse: Write/Edit** - Validates TYPO3 code before saving
- **PostToolUse: Write** - Runs PHP CS Fixer
- **SessionStart** - Loads TYPO3 Coding Guidelines
- **UserPromptSubmit** - Suggests TYPO3 best practices

### 🌐 MCP Server Integration

- **TYPO3 Documentation** - Direct access to docs.typo3.org
- **Extension Repository** - Search TER (TYPO3 Extension Repository)
- **Changelog Lookup** - Browse TYPO3 Core Changelog
- **API Reference** - TYPO3 Core API Reference

## 📦 Installation

```bash
# Install plugin (when public)
/plugin install typo3-development

# Or test locally
claude --plugin-dir ./typo3_development
```

## 🚀 Quick Start

1. **Create extension**:
   ```
   /typo3:extension my_extension "MyVendor"
   ```

2. **Generate model with repository and TCA**:
   ```
   /typo3:model Product "A product in the shop"
   ```

3. **Create controller**:
   ```
   /typo3:controller ProductController
   ```

4. **Write tests**:
   ```
   /typo3:test ProductControllerTest
   ```

## 🛠️ Configuration

The plugin automatically uses TYPO3 Coding Guidelines from:
- https://github.com/in2code-de/claude-code-instructions/blob/main/CLAUDE.md
- Official TYPO3 CGL: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/

### Optional Plugin Configuration

Create `.claude/typo3-config.json` in your project:

```json
{
  "typo3Version": "12.4",
  "extensionKey": "my_extension",
  "vendorName": "MyVendor",
  "guidelinesUrl": "https://github.com/in2code-de/claude-code-instructions/blob/main/CLAUDE.md",
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

- [Architecture](./docs/ARCHITECTURE.md) - Plugin architecture and concepts
- [Skills Guide](./docs/SKILLS.md) - All skills in detail
- [Commands Reference](./docs/COMMANDS.md) - All slash commands
- [Hooks Configuration](./docs/HOOKS.md) - Hook system
- [MCP Integration](./docs/MCP.md) - MCP Server setup
- [Development Guide](./docs/DEVELOPMENT.md) - Plugin development

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](./LICENSE)

## 🙏 Credits

- TYPO3 Community
- [in2code Claude Code Instructions](https://github.com/in2code-de/claude-code-instructions)
- Claude Code Team

## 🔗 Links

- [TYPO3 CMS](https://typo3.org)
- [TYPO3 Documentation](https://docs.typo3.org)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

**Status**: 🚧 In Development - v0.1.0 (Private Beta)
