# Configuration Guide

The TYPO3 Development Plugin uses a two-tier configuration system that balances automatic detection with manual control.

## Configuration Files Overview

| File | Purpose | Created By | Priority |
|------|---------|------------|----------|
| `.claude/typo3-project.json` | Auto-detected project settings | Plugin | Low |
| `.claude/typo3-config.json` | Manual overrides and preferences | User | High |

## Auto-Generated Configuration

### `.claude/typo3-project.json`

This file is automatically created by the plugin when:
- You run `/typo3:init` command
- The `SessionStart` hook detects a TYPO3 project
- Any command needs project information

**You should NOT edit this file manually.** The plugin regenerates it when needed.

#### Structure

```json
{
  "analyzedAt": "2024-01-16T12:00:00Z",
  "typo3": {
    "version": "12.4.10",
    "majorVersion": 12,
    "isLTS": true,
    "composerMode": true
  },
  "php": {
    "version": "8.2",
    "minVersion": "8.1"
  },
  "project": {
    "type": "ddev",
    "rootPath": "/var/www/html",
    "publicPath": "public",
    "configPath": "config"
  },
  "extensions": {
    "installed": [
      {
        "key": "my_extension",
        "vendor": "MyVendor",
        "path": "packages/my_extension"
      }
    ]
  },
  "sites": [
    {
      "identifier": "main",
      "base": "https://mysite.ddev.site/"
    }
  ],
  "tools": {
    "composer": true,
    "phpCSFixer": "vendor/bin/php-cs-fixer",
    "ddev": true,
    "docker": false
  },
  "guidelines": {
    "codingStandards": "PSR-12",
    "typo3Version": "12.4"
  }
}
```

#### What Gets Detected

**TYPO3 Version:**
- Reads from `composer.json` (typo3/cms-core version)
- Checks `typo3conf/ext/` vs `public/typo3conf/ext/` for composer mode
- Determines LTS status (v11, v12, v13)

**PHP Version:**
- From `composer.json` platform requirements
- From DDEV `.ddev/config.yaml`

**Project Type:**
- DDEV: Detects `.ddev/` directory
- Docker: Detects `docker-compose.yml`
- Native: Neither DDEV nor Docker

**Extensions:**
- Scans `packages/` and `typo3conf/ext/`
- Reads extension keys and vendor names
- Identifies active development extensions

**Tools:**
- PHP CS Fixer: Checks `vendor/bin/php-cs-fixer`
- Composer: Checks `composer.json`
- DDEV/Docker: Checks config files

#### Used By

This configuration is used by:
- `project-aware` skill - Adapts suggestions to your TYPO3 version
- All commands - Uses correct paths and versions
- Hooks - Validates against your project standards
- Agents - Knows which TYPO3 APIs are available

#### When to Regenerate

Run `/typo3:init` after:
- TYPO3 version upgrade
- Adding/removing extensions
- Changing project structure
- Switching environments (DDEV ↔ Docker)

## Manual Configuration

### `.claude/typo3-config.json`

Create this file to **override** auto-detected settings or set custom preferences.

This is optional - the plugin works without it.

#### Use Cases

1. **Force Specific TYPO3 Version Behavior**
   ```json
   {
     "typo3Version": "12.4"
   }
   ```
   Forces v12 patterns even if v11 is detected (useful during upgrades).

2. **Set Default Extension for Commands**
   ```json
   {
     "extensionKey": "my_shop",
     "vendorName": "MyVendor"
   }
   ```
   Pre-fills extension key in `/typo3:model`, `/typo3:plugin`, etc.

3. **Configure Coding Standards Enforcement**
   ```json
   {
     "autoEnforce": {
       "codingStandards": true,
       "dependencyInjection": true,
       "securityChecks": true,
       "fluidValidation": true
     }
   }
   ```
   Controls which PreToolUse hooks are active.

4. **Set Custom Tool Paths**
   ```json
   {
     "phpCSFixerPath": "vendor/bin/php-cs-fixer",
     "phpStanPath": "vendor/bin/phpstan"
   }
   ```
   Overrides auto-detected tool locations.

#### Full Example

```json
{
  "typo3Version": "12.4",
  "extensionKey": "my_shop",
  "vendorName": "Acme",
  "autoEnforce": {
    "codingStandards": true,
    "dependencyInjection": true,
    "securityChecks": true,
    "fluidValidation": true
  },
  "phpCSFixerPath": "vendor/bin/php-cs-fixer",
  "defaultNamespace": "Acme\\MyShop",
  "testFramework": "phpunit"
}
```

#### Available Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `typo3Version` | string | Auto-detected | Force TYPO3 version (e.g., "12.4") |
| `extensionKey` | string | - | Default extension key for commands |
| `vendorName` | string | - | Default vendor name (e.g., "MyVendor") |
| `autoEnforce.codingStandards` | boolean | true | Enable PSR-12/CGL validation |
| `autoEnforce.dependencyInjection` | boolean | true | Prefer DI over static calls |
| `autoEnforce.securityChecks` | boolean | true | Check for XSS/SQL injection |
| `autoEnforce.fluidValidation` | boolean | true | Validate Fluid templates |
| `phpCSFixerPath` | string | Auto-detected | Path to PHP CS Fixer |
| `phpStanPath` | string | - | Path to PHPStan |
| `defaultNamespace` | string | Auto-generated | Default PHP namespace |
| `testFramework` | string | "phpunit" | Test framework to use |

## Configuration Priority

When both files exist, values are merged with this priority:

1. **Manual config** (`.claude/typo3-config.json`) - Highest priority
2. **Auto-detected** (`.claude/typo3-project.json`) - Fallback
3. **Plugin defaults** - Last resort

### Example Merge

**Auto-detected** (`.claude/typo3-project.json`):
```json
{
  "typo3": {
    "version": "11.5.30",
    "majorVersion": 11
  },
  "extensionKey": null
}
```

**Manual override** (`.claude/typo3-config.json`):
```json
{
  "typo3Version": "12.4",
  "extensionKey": "my_shop"
}
```

**Merged result:**
```json
{
  "typo3": {
    "version": "12.4",     // From manual config
    "majorVersion": 12     // Updated based on manual version
  },
  "extensionKey": "my_shop" // From manual config
}
```

## Working Without Configuration

The plugin is designed to work without any configuration files:

- Commands prompt for required information (extension key, vendor name)
- Skills use generic TYPO3 best practices
- Hooks apply universal coding standards
- Agents validate against common patterns

Configuration just makes the experience smoother by pre-filling values and adapting to your specific setup.

## Best Practices

### For Development

Create `.claude/typo3-config.json` with your preferences:
```json
{
  "extensionKey": "my_extension",
  "vendorName": "MyVendor",
  "autoEnforce": {
    "codingStandards": true,
    "securityChecks": true
  }
}
```

### For CI/CD

Commit `.claude/typo3-project.json` to version control so all developers have the same detected configuration.

### During Upgrades

1. Set target version in `.claude/typo3-config.json`:
   ```json
   {
     "typo3Version": "12.4"
   }
   ```
2. Run `/typo3:upgrade 11.5 12.4`
3. After upgrade completes, remove manual override
4. Run `/typo3:init` to detect new version

## Troubleshooting

### Configuration Not Applied

1. Check file location (must be in `.claude/` at project root)
2. Validate JSON syntax (use a JSON linter)
3. Run `/typo3:init` to regenerate auto-detected config
4. Restart Claude Code session

### Wrong TYPO3 Version Detected

Override in `.claude/typo3-config.json`:
```json
{
  "typo3Version": "12.4"
}
```

### Commands Ask for Extension Key Every Time

Set default in `.claude/typo3-config.json`:
```json
{
  "extensionKey": "my_extension",
  "vendorName": "MyVendor"
}
```

### PHP CS Fixer Not Found

Specify path in `.claude/typo3-config.json`:
```json
{
  "phpCSFixerPath": "vendor/bin/php-cs-fixer"
}
```

## Related Documentation

- [Installation Guide](./INSTALLATION.md) - How to install the plugin
- [Feature Reference](./FEATURES.md) - Available commands and skills
- [Architecture](./ARCHITECTURE.md) - How the plugin works internally
