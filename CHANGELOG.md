# Changelog

All notable changes to the TYPO3 Development Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## 1.1.0 - 2026-01-17

### Added

- `/typo3:init` now performs a comprehensive project analysis, including:
  - Makefile detection and available custom commands
  - Docker Compose environment analysis (files, services, volumes)
  - Frontend toolchain detection (Webpack, Vite, TypeScript, CSS tooling)
  - Extension dependency analysis from local `composer.json` files
  - Git context (current branch, recent commits, uncommitted changes)
  - Composer configuration analysis (repositories, patches, scripts)

### Changed

- Expanded `CLAUDE.md` example to include all new analysis fields
- Documented strict preservation of existing `CLAUDE.md` content (update-only)
- README simplified to describe the `CLAUDE.md`-based configuration approach

---

## [1.0.2] - 2024-01-17

### Fixed

**Critical Bug Fixes** - Plugin no longer interferes with normal Claude Code usage

- **Removed blocking UserPromptSubmit hooks** that prevented commands from running
  - Commands like `/typo3:init` and `/typo3:test` were blocked by overly aggressive hooks
  - Normal conversation was interrupted by hooks matching common words (query, model, etc.)
  - Plugin now only runs hooks when actually writing code (PreToolUse/PostToolUse)

### Changed

**Architecture: Switched to CLAUDE.md approach**

- **No more separate JSON files** - Configuration now stored in `CLAUDE.md` (standard Claude Code approach)
- `/typo3:init` now writes to `CLAUDE.md` instead of `.claude/typo3-project.json`
- Simplified SessionStart hook - only loads TYPO3 Coding Guidelines
- **Restored complete coding guidelines** from in2code-de/claude-code-instructions
- Updated `docs/CONFIGURATION.md` with new CLAUDE.md-based documentation

### Migration

**For users upgrading from v1.0.0-1.0.1:**

1. Old `.claude/typo3-project.json` and `.claude/typo3-config.json` files are no longer used (safe to delete)
2. Run `/typo3:init` to create `CLAUDE.md` with project configuration
3. Plugin no longer blocks normal usage - works seamlessly with Claude Code

### Breaking Changes

- Configuration files changed from JSON to CLAUDE.md (but plugin works without any config)
- Old JSON files in `.claude/` directory are ignored

---

## [1.0.1] - 2024-01-17

### Fixed
- Wrapped `SessionStart` entries in `hooks` arrays to satisfy Claude Code hooks schema and prevent plugin load errors

---

## [1.0.0] - 2024-01-16

### Added

**Initial Stable Release** 🎉

This is the first stable release of the TYPO3 Development Plugin for Claude Code.

#### Commands (19 total)
- `/typo3:init` - Deep project analysis and configuration detection
- `/typo3:extension` - Complete extension structure scaffolding
- `/typo3:model` - Domain Model + Repository + TCA + SQL generation
- `/typo3:plugin` - Plugin creation with Controller, Templates, FlexForm
- `/typo3:controller` - Slim Extbase Controller with Dependency Injection
- `/typo3:viewhelper` - Custom Fluid ViewHelper generation
- `/typo3:middleware` - PSR-15 Middleware creation
- `/typo3:upgrade` - Version upgrade assistance
- `/typo3:test` - Unit and Functional test scaffolding
- `/typo3:migration` - Doctrine DBAL Migration creation
- `/typo3:scheduler` - Scheduler Task generation
- `/typo3:flexform` - FlexForm XML configuration generation
- `/typo3:event` - PSR-14 Event + EventListener creation
- `/typo3:command` - Symfony Console Command scaffolding
- `/typo3:docs` - Search TYPO3 official documentation
- `/typo3:changelog` - Get TYPO3 Core changelog entries
- `/typo3:ter` - Search TYPO3 Extension Repository
- `/typo3:api` - Get TYPO3 Core API reference with examples
- `/typo3:cgl` - Get TYPO3 Coding Guidelines reference
- `/typo3:test-browser` - Automated browser testing for TYPO3 frontend and backend

#### Skills (10 total)
- `typo3-coding-standards` - Enforces PSR-12 and TYPO3 CGL compliance
- `extbase-patterns` - Suggests modern Extbase patterns and slim controllers
- `fluid-best-practices` - Prevents business logic in Fluid templates
- `dependency-injection` - Promotes constructor-based Dependency Injection
- `security-awareness` - Identifies security vulnerabilities (XSS, SQL injection, CSRF)
- `doctrine-dbal` - Guides proper Doctrine DBAL and QueryBuilder usage
- `typo3-api` - Provides knowledge of TYPO3 Core APIs
- `content-blocks` - Guides TYPO3 v13+ Content Block creation
- `project-aware` - Dynamically adapts to detected TYPO3 version
- `browser-testing` - Knowledge for testing TYPO3 in Chrome browser

#### Agents (6 total)
- `typo3-validator` - Validates code against TYPO3 CGL and best practices
- `typo3-migration-assistant` - Assists with major version upgrades (v11→v12→v13)
- `typo3-security-scanner` - Scans for security vulnerabilities (OWASP Top 10)
- `tca-validator` - Validates TCA configurations and column types
- `typoscript-analyzer` - Analyzes TypoScript for deprecated syntax
- `typo3-browser-tester` - Automated browser testing for frontend and backend

#### Hooks
- `SessionStart` - Loads TYPO3 CGL and detects project configuration
- `PreToolUse` - Validates code before writing (PHP, Fluid, TCA)
- `PostToolUse` - Runs PHP CS Fixer and other post-processing
- `UserPromptSubmit` - Provides context-aware suggestions

#### Chrome DevTools Integration
- Full browser automation for TYPO3 testing
- Screenshot capture (viewport and full page)
- DOM and accessibility tree inspection
- Network request and console message monitoring
- Automated form testing
- Backend module testing with authentication
- Performance analysis

#### Documentation
- Comprehensive installation guide
- Detailed configuration documentation
- Complete feature reference
- Architecture documentation
- Chrome DevTools setup guide
- Release process documentation

### Changed
- Plugin renamed from `typo3-development` to `typo3-dev`
- Repository moved to `claude-typo3-dev` for better discoverability
- Configuration system redesigned:
  - Auto-generated `.claude/typo3-project.json` for project detection
  - Optional `.claude/typo3-config.json` for manual overrides
- Improved marketplace integration with `@in2code` namespace
- Enhanced project detection (TYPO3 version, extensions, tools)

### Fixed
- Configuration file naming consistency
- Repository URL references across all documentation
- Installation command syntax in guides

### Documentation
- Added comprehensive `docs/CONFIGURATION.md`
- Added `RELEASE.md` with Git Flow workflow
- Added `CHANGELOG.md` (this file)
- Updated all documentation with new repository URLs
- Improved README with clearer configuration explanation

---

## [0.4.0] - 2024-01-10

### Added
- Chrome DevTools integration via MCP
- `/typo3:test-browser` command for browser testing
- `typo3-browser-tester` agent for automated testing
- `browser-testing` skill for testing knowledge
- Documentation for browser testing features

### Changed
- Removed custom TYPO3 Documentation MCP server
- Switched to Chrome DevTools for all browser-based testing
- Simplified MCP configuration

---

## [0.3.0] - 2024-01-05

### Added
- `/typo3:docs` command to search TYPO3 documentation
- `/typo3:changelog` command to get Core changelog
- `/typo3:ter` command to search Extension Repository
- `/typo3:api` command to get Core API reference
- `/typo3:cgl` command to get Coding Guidelines

### Changed
- Improved project detection in SessionStart hook
- Enhanced TYPO3 version detection

---

## [0.2.0] - 2024-01-01

### Added
- Complete command suite (14 commands)
- Skills system with 9 auto-activated skills
- Agents for validation and migration
- Hooks for automated quality checks
- Project configuration support

### Changed
- Improved extension scaffolding
- Better TCA generation
- Enhanced Fluid template generation

---

## [0.1.0] - 2023-12-20

### Added
- Initial plugin structure
- Basic commands: extension, model, plugin, controller
- TYPO3 Coding Guidelines integration
- SessionStart hook with CGL loading

---

## Versioning Policy

- **MAJOR** version for breaking changes (renamed commands, removed features)
- **MINOR** version for new features (new commands, skills, agents)
- **PATCH** version for bug fixes and documentation improvements

## Upgrade Guides

### Upgrading to 1.0.0 from 0.x

1. **Update Installation**
   ```bash
   # Remove old version
   /plugin uninstall typo3-development

   # Install new version
   /plugin marketplace add PatFischer91/claude-typo3-dev
   /plugin install typo3-dev@in2code
   ```

2. **Configuration Migration**
   - The plugin now auto-generates `.claude/typo3-project.json`
   - If you had custom settings, move them to `.claude/typo3-config.json`
   - See [Configuration Guide](./docs/CONFIGURATION.md) for details

3. **No Breaking Changes**
   - All commands work exactly as before
   - All skills and agents remain unchanged
   - Hook behavior is identical

---

## Links

- [GitHub Repository](https://github.com/PatFischer91/claude-typo3-dev)
- [Installation Guide](./docs/INSTALLATION.md)
- [Configuration Guide](./docs/CONFIGURATION.md)
- [Release Process](./RELEASE.md)

[1.0.0]: https://github.com/PatFischer91/claude-typo3-dev/releases/tag/v1.0.0
[0.4.0]: https://github.com/PatFischer91/claude-typo3-dev/releases/tag/v0.4.0
[0.3.0]: https://github.com/PatFischer91/claude-typo3-dev/releases/tag/v0.3.0
[0.2.0]: https://github.com/PatFischer91/claude-typo3-dev/releases/tag/v0.2.0
[0.1.0]: https://github.com/PatFischer91/claude-typo3-dev/releases/tag/v0.1.0
