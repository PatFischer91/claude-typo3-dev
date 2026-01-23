# TYPO3-Dev Plugin - Quick Reference Card

> **Quick access to the most important commands and workflows**

## 🎯 Most Used Commands

```bash
# Create new extension
/typo3:extension <extkey> <vendor>

# Create domain model
/typo3:model <ModelName> "field1:type,field2:type"

# Create controller
/typo3:controller <ControllerName> action1,action2

# Search documentation
/typo3:docs <topic> [version]

# Refactor code
/typo3:code-simplify scope:changed goal:quick

# Analyze extension
/typo3:init

# Analyze project
/typo3:init
```

---

## ⚡ Quick Workflows

### New Extension (5 min)
```
/typo3:extension blog MyVendor
/typo3:model Post "title:string,content:text"
/typo3:controller PostController list,show
/typo3:init
```

### Add Feature (3 min)
```
/typo3:model Comment "author:string,text:text"
/typo3:controller CommentController create,delete
/typo3:code-simplify scope:changed
```

### Before Commit
```
/typo3:code-simplify scope:staged goal:full
```

---

## 📖 Documentation Search

```bash
# By topic
/typo3:docs QueryBuilder
/typo3:docs Fluid ViewHelpers
/typo3:docs PSR-15 Middleware

# By version
/typo3:docs Extbase 12.4
/typo3:docs TCA 13.0
```

---

## 🔍 Code Simplify Scopes

| Scope | Command | Use When |
|-------|---------|----------|
| Changed files | `scope:changed` | Daily work |
| Staged files | `scope:staged` | Before commit |
| All files | `scope:all` | Major cleanup |
| One file | `scope:file file:path/to/file.php` | Specific fix |
| Directory | `scope:dir dir:Classes/Domain/` | Specific area |

## 🎨 Code Simplify Goals

| Goal | Description | Time |
|------|-------------|------|
| `goal:quick` | Simple fixes only | ~1 min |
| `goal:moderate` | Medium refactoring | ~3 min |
| `goal:full` | Deep refactoring | ~5 min |

---

## 🏗️ Component Creation

| Component | Command | Example |
|-----------|---------|---------|
| Extension | `/typo3:extension` | `blog MyCompany` |
| Model | `/typo3:model` | `Post "title:string,text:text"` |
| Controller | `/typo3:controller` | `PostController list,show` |
| Repository | `/typo3:repository` | `PostRepository` |
| ViewHelper | `/typo3:viewhelper` | `FormatDate namespace:Format` |
| TCA | `/typo3:tca` | `posts "title,content,author"` |
| Middleware | `/typo3:middleware` | `AuthMiddleware` |
| Command | `/typo3:command` | `ImportCommand` |

---

## 📁 File Structure

After `/typo3:extension myext MyVendor`:

```
my_ext/
├── Classes/
│   ├── Controller/      # Slim controllers
│   ├── Domain/
│   │   ├── Model/       # Domain models
│   │   └── Repository/  # Data access
│   └── ViewHelpers/     # Custom Fluid tags
├── Configuration/
│   ├── TCA/            # Database config
│   └── TypoScript/     # TS setup/constants
├── Resources/
│   ├── Private/
│   │   ├── Templates/
│   │   ├── Partials/
│   │   └── Layouts/
│   └── Public/         # CSS, JS, Images
├── composer.json
├── ext_emconf.php
└── ext_localconf.php
```

---

## 🎓 TYPO3 Model Field Types

```bash
# String fields
"name:string"           → VARCHAR(255)
"email:string"          → VARCHAR(255)

# Text fields
"description:text"      → TEXT

# Numbers
"price:float"           → DECIMAL
"quantity:int"          → INTEGER
"stock:int"             → INTEGER

# Boolean
"active:bool"           → TINYINT(1)
"published:bool"        → TINYINT(1)

# Date/Time
"created:datetime"      → DATETIME
"updated:datetime"      → DATETIME

# Relations
"category:Category"     → Foreign key
"tags:Tag"             → M:N relation
```

---

## 🚦 Coding Guidelines (Auto-Loaded)

**Always:**
- ✅ `declare(strict_types=1);` after `<?php`
- ✅ Constructor injection with `private readonly`
- ✅ Type declarations on all parameters/returns
- ✅ QueryBuilder with named parameters
- ✅ PSR-12 formatting

**Never:**
- ❌ `GeneralUtility::makeInstance()` for services
- ❌ `$GLOBALS['TSFE']` (use request attributes)
- ❌ Direct `$_GET`, `$_POST`, `$_SESSION` access
- ❌ SQL concatenation (use named parameters)
- ❌ `@` error suppression

---

## 🔧 Hooks & Automation

**Auto-Triggered:**
- ✅ Guidelines loaded on session start
- ✅ Session tracking initialized
- ✅ PHP-CS-Fixer runs on PHP file writes
- ✅ Code-simplify suggested before commits (smart)

**Tracking Files:**
```bash
# Session info stored in:
.git/.code-simplify-session-start
.git/.code-simplify-last-activity
.git/.code-simplify-last-run
```

---

## 💡 Pro Tips

1. **Browse Commands:** Type `/typo3:` to see command list
2. **Version-Specific:** Always specify version in docs search
3. **Combine Init + Docs:** `/typo3:init` then search suggested topics
4. **Scope Changed:** Use `scope:changed` for daily work
5. **Browse Commands:** Type `/typo3:` to see command list (no Tab needed)

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| SessionStart error | Check plugin installed correctly |
| No tracking files | Ensure you're in a git repo |
| Too many suggestions | Built-in 15min cooldown |
| Command not found | Type `/typo3:` to see available commands |
| Guidelines not loading | Restart Claude session |

---

## 📞 Getting Help

```bash
# Available commands
Type /typo3: to see all commands (command list appears automatically)

# Documentation
docs/GETTING-STARTED.md        # Detailed guide
docs/FEATURES.md               # All features
docs/INSTALLATION.md           # Setup
docs/CONFIGURATION.md          # Config options
```

---

**Quick Start:** `/typo3:extension myext MyVendor` → Start coding!
