# TYPO3 Development Plugin - Complete Feature Reference

## Overview

This plugin transforms Claude Code into a TYPO3-specialized development assistant with automatic version detection, code generation, validation, and best practices enforcement.

---

## Slash Commands (14)

All commands are prefixed with `/typo3:`. Arguments in `[]` are optional.

### `/typo3:init`

**Deep project analysis** - Performs comprehensive TYPO3 project analysis.

```
/typo3:init
```

**Note:** Basic auto-detection happens automatically for new projects. Use this command for detailed analysis including site configs, all extensions, and dev tools.

**Creates:** `.claude/typo3-project.json` with:
- TYPO3 version (11/12/13)
- PHP version
- Project type (DDEV, Composer, Legacy)
- Installed extensions
- Site configurations
- Available dev tools

---

### `/typo3:extension`

**Create new extension** with complete structure.

```
/typo3:extension [extension_key] [VendorName] [description]
```

**Example:**
```
/typo3:extension my_shop MyVendor "Online shop extension"
```

**Creates:**
- `ext_emconf.php` / `composer.json`
- `ext_localconf.php` / `ext_tables.php`
- `Configuration/` structure
- `Classes/` structure
- `Resources/` with templates
- `Services.yaml` for DI

---

### `/typo3:model`

**Generate Domain Model** with Repository, TCA, and SQL.

```
/typo3:model [ModelName] [fields]
```

**Example:**
```
/typo3:model Product "title:string,price:float,stock:int,active:bool,image:file"
```

**Creates:**
- `Classes/Domain/Model/Product.php`
- `Classes/Domain/Repository/ProductRepository.php`
- `Configuration/TCA/tx_myext_domain_model_product.php`
- `ext_tables.sql` entries

**Supported Field Types:**
| Type | TCA Type | PHP Type |
|------|----------|----------|
| `string` | input | string |
| `text` | text | string |
| `int` | number | int |
| `float` | number | float |
| `bool` | check | bool |
| `datetime` | datetime | \DateTime |
| `file` | file | FileReference |
| `relation` | select/group | ObjectStorage |

---

### `/typo3:plugin`

**Create Extbase Plugin** with Controller, Templates, and registration.

```
/typo3:plugin [PluginName] [description]
```

**Example:**
```
/typo3:plugin ProductList "Display products"
```

**Creates:**
- Controller with list/show actions
- Fluid templates (List.html, Show.html)
- Plugin registration in `ext_localconf.php`
- TypoScript setup
- Optional FlexForm

---

### `/typo3:controller`

**Create slim Extbase Controller** with DI.

```
/typo3:controller [ControllerName] [actions]
```

**Example:**
```
/typo3:controller Product "list,show,new,create,edit,update,delete"
```

**Features:**
- Constructor injection
- ResponseInterface return types
- Slim controller pattern

---

### `/typo3:viewhelper`

**Generate custom ViewHelper**.

```
/typo3:viewhelper [Name] [description]
```

**Example:**
```
/typo3:viewhelper FormatPrice "Formats price with currency"
```

**Creates:**
- `Classes/ViewHelpers/FormatPriceViewHelper.php`
- With `renderStatic()` for performance

---

### `/typo3:middleware`

**Create PSR-15 Middleware**.

```
/typo3:middleware [Name] [description]
```

**Example:**
```
/typo3:middleware ApiAuthentication "JWT token validation"
```

**Creates:**
- `Classes/Middleware/ApiAuthenticationMiddleware.php`
- `Configuration/RequestMiddlewares.php` registration

---

### `/typo3:test`

**Generate Unit/Functional Tests**.

```
/typo3:test [ClassName] [type]
```

**Example:**
```
/typo3:test ProductService functional
```

**Types:** `unit`, `functional`

---

### `/typo3:upgrade`

**TYPO3 Version Upgrade Assistant**.

```
/typo3:upgrade [from_version] [to_version]
```

**Example:**
```
/typo3:upgrade 11.5 12.4
```

**Provides:**
- Breaking changes checklist
- Deprecation warnings
- Code migration suggestions
- Rector commands

---

### `/typo3:migration`

**Create database migration**.

```
/typo3:migration [description]
```

**Example:**
```
/typo3:migration "Add slug field to products"
```

---

### `/typo3:scheduler`

**Create Scheduler Task**.

```
/typo3:scheduler [Name] [description]
```

**Example:**
```
/typo3:scheduler ImportProducts "Import products from API"
```

---

### `/typo3:flexform`

**Generate FlexForm XML**.

```
/typo3:flexform [plugin_name] [fields]
```

**Example:**
```
/typo3:flexform ProductList "itemsPerPage:int,sortOrder:select"
```

---

### `/typo3:event`

**Create PSR-14 Event + Listener**.

```
/typo3:event [EventName]
```

**Example:**
```
/typo3:event ProductCreated
```

**Creates:**
- `Classes/Event/ProductCreatedEvent.php`
- `Classes/EventListener/ProductCreatedEventListener.php`
- `Services.yaml` listener registration

---

### `/typo3:command`

**Create Symfony Console Command**.

```
/typo3:command [name] [description]
```

**Example:**
```
/typo3:command product:import "Import products from CSV"
```

---

## Skills (9)

Skills are automatically activated based on context. Claude uses them without explicit invocation.

### `typo3-coding-standards`

Monitors and enforces:
- PSR-12 compliance
- TYPO3 CGL conventions
- `defined('TYPO3') || die();` guards
- Proper namespacing

### `extbase-patterns`

Suggests modern Extbase patterns:
- Slim controllers
- Service layer architecture
- Proper DI usage
- ResponseInterface returns

### `fluid-best-practices`

Prevents anti-patterns in Fluid:
- No business logic in templates
- Proper ViewHelper usage
- XSS prevention (`f:format.raw` warnings)

### `dependency-injection`

Enforces DI best practices:
- Constructor injection
- No ObjectManager
- No `GeneralUtility::makeInstance()` for services
- `private readonly` properties

### `security-awareness`

Warns about security issues:
- SQL injection (QueryBuilder enforcement)
- XSS vulnerabilities
- CSRF protection
- Input validation

### `doctrine-dbal`

Ensures proper database access:
- QueryBuilder usage
- Named parameters
- No raw SQL
- Proper PDO types

### `typo3-api`

Knows TYPO3 Core APIs:
- Caching Framework
- Logging API
- FAL (File Abstraction Layer)
- Site Configuration
- Context API

### `content-blocks`

Guides TYPO3 v13+ Content Block creation:
- YAML configuration
- Frontend/EditorPreview templates
- Field types and validation

### `project-aware`

Adapts to detected TYPO3 version:

| TYPO3 | Adaptations |
|-------|-------------|
| v11 | Allows deprecated patterns, warns about future removal |
| v12 | Enforces ResponseInterface, constructor DI, modern TCA |
| v13 | Suggests Content Blocks, Site Sets, PHP 8.2+ features |

---

## Agents (5)

Specialized AI agents for complex tasks.

### `typo3-validator`

Validates code against TYPO3 CGL and best practices.

**Checks:**
- File structure
- Naming conventions
- DI usage
- Security patterns
- TCA configuration

### `typo3-migration-assistant`

Helps with major version upgrades.

**Capabilities:**
- Identifies deprecated code
- Suggests replacements
- Generates Rector config
- Creates migration checklist

### `typo3-security-scanner`

Finds security vulnerabilities.

**Scans for:**
- SQL injection
- XSS vulnerabilities
- CSRF issues
- Insecure file handling
- Sensitive data exposure

### `tca-validator`

Validates TCA configurations.

**Checks:**
- Required fields
- Type configurations
- Deprecated options
- Version compatibility

### `typoscript-analyzer`

Analyzes TypoScript for issues.

**Detects:**
- Deprecated syntax
- Performance issues
- Configuration errors
- Migration needs

---

## Hooks

Event-driven automation that runs at specific points.

### SessionStart

**Triggers:** When Claude Code session begins

**Actions:**
1. Checks for `CLAUDE.md` in project root
2. If new project + TYPO3 detected → Auto-initializes
3. Loads `.claude/typo3-project.json` configuration
4. Applies TYPO3 Coding Guidelines

### PreToolUse

**Triggers:** Before writing/editing files

| File Type | Checks |
|-----------|--------|
| `*.php` | PSR-12, DI, type declarations, security |
| `*.html` | Fluid best practices, no business logic |
| `TCA/*.php` | TCA validation, modern types |

### PostToolUse

**Triggers:** After writing files

| File Type | Action |
|-----------|--------|
| `*.php` | Runs PHP CS Fixer (if available) |
| `ext_tables.sql` | Reminds to run `extension:setup` |

### UserPromptSubmit

**Triggers:** When user mentions specific keywords

| Keywords | Guidance Applied |
|----------|------------------|
| `controller`, `action` | Slim controller, DI, ResponseInterface |
| `model`, `repository` | Domain model patterns |
| `query`, `database` | QueryBuilder, named parameters |
| `viewhelper`, `fluid` | ViewHelper patterns, security |
| `upgrade`, `migration` | Version-specific changes |
| `security`, `xss` | Security best practices |

---

## MCP Servers (2)

### TYPO3 Documentation Server

**Tools:**

| Tool | Description |
|------|-------------|
| `search_typo3_docs` | Search docs.typo3.org |
| `get_typo3_changelog` | Browse changelog (v11/v12/v13) |
| `search_typo3_extensions` | Search TER (real API) |
| `get_extension_detail` | Get extension info from TER |
| `get_typo3_api_reference` | Core API reference with examples |
| `get_typo3_coding_guidelines` | CGL for PHP, DB, Fluid, Security |

### Chrome DevTools Server

**Features:**
- Take screenshots
- Inspect DOM and accessibility tree
- Monitor network requests
- Automated testing (click, type, navigate)
- Core Web Vitals analysis

See [Chrome DevTools Documentation](./CHROME-DEVTOOLS.md) for setup.

---

## Auto-Detection Flow

```
Session Start
     │
     ▼
┌─────────────────────┐
│ CLAUDE.md exists?   │
└─────────────────────┘
     │
     ├── YES ──► Load existing config
     │
     └── NO ──► Check for TYPO3
                    │
                    ├── composer.json has typo3/cms-core?
                    │         │
                    │         ├── YES ──► Auto-analyze:
                    │         │           - TYPO3 version
                    │         │           - PHP version
                    │         │           - Project type
                    │         │           - Extensions
                    │         │           ──► Create typo3-project.json
                    │         │
                    │         └── NO ──► Not a TYPO3 project
                    │
                    └── Apply TYPO3 CGL guidelines
```

---

## Version-Specific Behavior

### TYPO3 11.5

```php
// Allowed (deprecated)
$this->objectManager->get(Repository::class);
GeneralUtility::getUrl('https://...');

// TCA
'config' => ['type' => 'input', 'eval' => 'int']
```

### TYPO3 12.4

```php
// Required
public function __construct(
    private readonly ProductRepository $productRepository
) {}

public function listAction(): ResponseInterface
{
    return $this->htmlResponse();
}

// TCA
'config' => ['type' => 'number']
```

### TYPO3 13.x

```php
// New features
// - Content Blocks
// - Site Sets
// - PHP 8.2+ features
// - Composer-only mode
```

---

## File Structure

```
typo3-dev/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── commands/                     # 14 slash commands
│   ├── init.md
│   ├── extension.md
│   ├── model.md
│   ├── plugin.md
│   ├── controller.md
│   ├── viewhelper.md
│   ├── middleware.md
│   ├── test.md
│   ├── upgrade.md
│   ├── migration.md
│   ├── scheduler.md
│   ├── flexform.md
│   ├── event.md
│   └── command.md
├── skills/                       # 9 auto-activated skills
│   ├── typo3-coding-standards/
│   ├── extbase-patterns/
│   ├── fluid-best-practices/
│   ├── dependency-injection/
│   ├── security-awareness/
│   ├── doctrine-dbal/
│   ├── typo3-api/
│   ├── content-blocks/
│   └── project-aware/
├── agents/                       # 5 specialized agents
│   ├── typo3-validator/
│   ├── typo3-migration-assistant/
│   ├── typo3-security-scanner/
│   ├── tca-validator/
│   └── typoscript-analyzer/
├── hooks/
│   └── hooks.json               # Event automation
├── mcp/
│   └── typo3-docs-server/       # TYPO3 Documentation MCP
├── .mcp.json                     # MCP configuration
└── docs/                         # Documentation
    ├── INSTALLATION.md
    ├── FEATURES.md
    └── CHROME-DEVTOOLS.md
```
