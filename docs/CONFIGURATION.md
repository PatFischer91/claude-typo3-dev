# Configuration Guide

The TYPO3 Development Plugin uses Claude Code's standard `CLAUDE.md` file for all project configuration.

## Philosophy

Unlike previous versions, the plugin now follows Claude Code's standard approach:
- **No separate JSON files** - Everything in CLAUDE.md (just like `/init`)
- **Standard Claude Code behavior** - Works exactly like other Claude projects
- **Simple and transparent** - Easy to read and edit manually

## How It Works

### 1. Session Start

When you open a TYPO3 project, the TYPO3 Coding Guidelines are **automatically loaded** into the session. This happens regardless of whether CLAUDE.md exists or not.

**You get:**
- PSR-12 coding standards
- TYPO3-specific conventions
- Modern patterns (DI, QueryBuilder, ResponseInterface)
- Security best practices

### 2. Project Initialization

When you run `/typo3:init`, the plugin analyzes your project and writes TYPO3-specific configuration to `CLAUDE.md`.

**The command detects:**
- TYPO3 version
- PHP version
- Project type (DDEV, Docker, Composer)
- Installed extensions
- Site configurations
- Development tools

**Everything is written to CLAUDE.md** (not separate files).

## CLAUDE.md Structure

After running `/typo3:init`, your CLAUDE.md might look like this:

```markdown
# Project: My TYPO3 Site

## TYPO3 Configuration

**TYPO3 Version**: 12.4.10 (LTS)
**PHP Version**: 8.2 (min: 8.1)
**Project Type**: DDEV + Composer Mode
**Public Path**: public/
**Config Path**: config/

### Project Structure
- Composer-based TYPO3 installation
- DDEV local development environment
- Modern TYPO3 v12 setup

### Local Extensions
- **my_shop** (MyVendor) v1.0.0
  - Location: packages/my_shop/

### Third-Party Extensions
- news (georgringer/news)
- powermail (in2code/powermail)

### Sites
- **main**: https://mysite.ddev.site/ (Languages: de, en)

### Development Tools
- ✅ PHP CS Fixer: vendor/bin/php-cs-fixer
- ❌ PHPStan: Not installed
- ✅ TYPO3 Testing Framework

### TYPO3 v12 Guidelines for This Project

Apply these version-specific best practices:

1. **Controllers**: All actions MUST return ResponseInterface
2. **Dependency Injection**: Constructor-based DI only (ObjectManager removed)
3. **TCA**: Use modern types (number, datetime, etc.)
4. **Events**: PSR-14 Events only (no legacy hooks)
5. **Request**: Use request attributes instead of $GLOBALS['TSFE']
6. **Database**: QueryBuilder with named parameters only
7. **Strict Types**: Always use `declare(strict_types=1);`
8. **Config Files**: Use `defined('TYPO3') || die();` (not `or die()`)

### Recommendations
- Install PHPStan: `composer require --dev phpstan/phpstan`
- Install Rector: `composer require --dev ssch/typo3-rector`
```

## Customization

You can **edit CLAUDE.md manually** to customize behavior:

### Add Custom Guidelines

```markdown
## Custom Development Guidelines

- Always use English for variable names
- Prefix all my extensions with "acme_"
- Use PSR-4 autoloading
```

### Override Detected Values

If the plugin detected wrong values, just edit CLAUDE.md:

```markdown
**TYPO3 Version**: 13.0 (not 12.4 - we're on edge branch)
```

### Add Extension-Specific Notes

```markdown
### my_shop Extension

- Main entry point: Classes/Controller/ShopController.php
- Uses custom payment provider: Stripe
- Database tables: tx_myshop_orders, tx_myshop_products
```

## Workflow

### First Time Setup

```bash
# In your TYPO3 project
claude

# Run init to analyze project
/typo3:init

# CLAUDE.md is created with TYPO3 config
```

### After Major Changes

Re-run `/typo3:init` after:
- TYPO3 version upgrade
- Adding new extensions
- Changing project structure
- Switching environments (DDEV ↔ Docker)

### Manual Editing

```bash
# Edit CLAUDE.md with your favorite editor
vim CLAUDE.md

# Or ask Claude to update it
"Please add a note to CLAUDE.md that all new models should use UUID primary keys"
```

## Comparison: Old vs New Approach

| Aspect | Old (v1.0.0-1.0.1) | New (v1.0.2+) |
|--------|-------------------|---------------|
| **Config Location** | `.claude/typo3-project.json` | `CLAUDE.md` |
| **Manual Overrides** | `.claude/typo3-config.json` | Edit `CLAUDE.md` |
| **How to Update** | Re-run `/typo3:init` | Edit CLAUDE.md or re-run `/typo3:init` |
| **Visibility** | Hidden in .claude/ | Visible in project root |
| **Editability** | JSON (error-prone) | Markdown (easy to read/edit) |
| **Claude Code Standard** | ❌ Custom approach | ✅ Standard /init approach |

## Benefits of CLAUDE.md Approach

**Simpler:**
- One file instead of two
- Standard Claude Code behavior
- No special plugin-specific files

**More Transparent:**
- CLAUDE.md is in project root (visible)
- Easy to read and understand
- Easy to edit manually

**Better Integration:**
- Works like `/init`
- Consistent with other Claude projects
- Other team members understand it immediately

**Version Control Friendly:**
- Commit CLAUDE.md to Git
- Team shares same configuration
- Easy to review changes

## Troubleshooting

### Plugin Not Working

**Check:** Is the plugin enabled?
```bash
/plugin installed
```

### Guidelines Not Applied

**Solution:** The TYPO3 Coding Guidelines are loaded automatically at session start. You don't need CLAUDE.md for basic guidelines.

For project-specific adaptations, run `/typo3:init`.

### CLAUDE.md Not Created

**Check:** Did you run `/typo3:init`?
```bash
/typo3:init
```

### Wrong TYPO3 Version Detected

**Solution:** Edit CLAUDE.md manually and change the version:
```markdown
**TYPO3 Version**: 12.4 (manually set)
```

### Old JSON Files Present

If you upgraded from v1.0.0-1.0.1, you might have old JSON files:

```bash
# Remove old files (optional, they're ignored now)
rm .claude/typo3-project.json
rm .claude/typo3-config.json
```

The plugin no longer uses or creates these files.

## Migration from v1.0.0-1.0.1

If you're upgrading from an older version with JSON files:

1. **Remove old JSON files** (optional):
   ```bash
   rm .claude/typo3-project.json
   rm .claude/typo3-config.json
   ```

2. **Run `/typo3:init`** to create CLAUDE.md:
   ```bash
   /typo3:init
   ```

3. **Check CLAUDE.md** was created:
   ```bash
   cat CLAUDE.md
   ```

4. **Manually add custom preferences** from old `.claude/typo3-config.json` to CLAUDE.md if needed

## Example CLAUDE.md Templates

### Minimal CLAUDE.md

```markdown
# TYPO3 Project

**TYPO3 Version**: 12.4
**Project Type**: Composer

Use TYPO3 v12 best practices.
```

### Detailed CLAUDE.md

See full example in "CLAUDE.md Structure" section above.

### Multi-Project CLAUDE.md

```markdown
# TYPO3 Multi-Site Project

## Main Site (www.example.com)
**TYPO3 Version**: 12.4
**Site Identifier**: main

## Shop (shop.example.com)
**TYPO3 Version**: 12.4
**Site Identifier**: shop
**Extensions**: tx_myshop

## Blog (blog.example.com)
**TYPO3 Version**: 11.5 (legacy)
**Site Identifier**: blog
```

## Best Practices

1. **Commit CLAUDE.md to Git** - Share configuration with your team
2. **Update after major changes** - Keep CLAUDE.md current
3. **Document custom decisions** - Add notes about your architecture
4. **Use markdown formatting** - Make it readable
5. **Keep it concise** - Only include relevant information

## Related Documentation

- [Installation Guide](./INSTALLATION.md) - How to install the plugin
- [Feature Reference](./FEATURES.md) - Available commands and skills
- [TYPO3 Init Command](../typo3-dev/commands/init.md) - Detailed init documentation
