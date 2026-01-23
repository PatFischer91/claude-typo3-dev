# Getting Started with TYPO3-Dev Plugin

Welcome! This guide helps you get the most out of the TYPO3-Dev plugin with practical examples and workflows.

## 🚀 Quick Start (First 5 Minutes)

### 1. Installation
```bash
# Add the marketplace
claude plugin marketplace add PatFischer91/claude-typo3-dev

# Install the plugin
claude plugin install typo3-dev@in2code
```

### 2. Start a New Chat in Your TYPO3 Project
The plugin automatically:
- ✅ Loads TYPO3 coding guidelines
- ✅ Enables all commands, skills, and agents
- ✅ Starts session tracking

### 3. Try Your First Command
```
/typo3:help
```
See all available commands organized by category.

---

## 📋 Common Use Cases

### Use Case 1: Creating a New Extension

**Goal:** Scaffold a complete TYPO3 extension from scratch

**Command:**
```
/typo3:extension my_blog MyVendor
```

**What happens:**
- Creates extension structure (Classes/, Configuration/, Resources/, etc.)
- Generates composer.json, ext_emconf.php, ext_localconf.php
- Sets up proper namespacing
- Creates initial controller and repository

**Next steps:**
```
/typo3:model Post "title:string,content:text,author:string"
```
Creates domain model with TCA configuration.

---

### Use Case 2: Adding Features to Existing Extension

**Scenario:** You need to add a new domain model to your extension

**Step 1 - Create Model:**
```
/typo3:model Product "name:string,price:float,stock:int,active:bool"
```

**Step 2 - Add Controller Actions:**
```
/typo3:controller ProductController list,show,create,update,delete
```

**Step 3 - Check Configuration:**
```
/typo3:init
```
Reviews your extension and suggests improvements.

---

### Use Case 3: Finding TYPO3 Documentation

**When:** You need to know how to use a specific TYPO3 API

**Examples:**
```
/typo3:docs QueryBuilder 12.4
/typo3:docs Extbase Repository
/typo3:docs PSR-15 Middleware
/typo3:docs ContentObject Rendering
```

**What it does:**
- Searches official TYPO3 documentation
- Version-specific results (12.4, 13.0, etc.)
- Provides direct links to relevant pages

---

### Use Case 4: Refactoring and Code Quality

**Scenario:** Your code has grown and needs cleanup

**Step 1 - Analyze Issues:**
```
/typo3:code-simplify changed goal:full
```

**Options:**
- `scope:changed` - Only changed files
- `scope:staged` - Git staged files
- `scope:all` - Entire extension
- `goal:quick` - Quick fixes only
- `goal:full` - Deep refactoring

**Step 2 - Fix Specific Issues:**
```
/typo3:code-simplify scope:file file:Classes/Domain/Model/Product.php
```

**When to use:**
- Before committing (suggested automatically via hooks)
- After adding new features
- During code reviews
- Before releases

---

### Use Case 5: Working with TCA (Database Schema)

**Creating TCA for a Model:**
```
/typo3:tca products "name,description,price,category"
```

**Result:**
- Complete TCA configuration in `Configuration/TCA/tx_myext_domain_model_products.php`
- Proper field types (input, text, select, etc.)
- Language support (l10n fields)
- Enable fields (hidden, deleted, starttime, endtime)
- Searchable fields

**Modifying Existing Tables:**
```
/typo3:tca-extend pages "my_custom_field:string"
```

---

### Use Case 6: Creating ViewHelpers

**Scenario:** You need custom Fluid functionality

**Command:**
```
/typo3:viewhelper FormatCurrency namespace:Format
```

**What you get:**
- ViewHelper class in proper location
- Correct namespace and registration
- Example implementation
- PHPDoc comments

**Use in Fluid:**
```html
<my:format.formatCurrency amount="{product.price}" currency="EUR" />
```

---

### Use Case 7: Debugging and Testing

**Browser Testing with Chrome DevTools:**

The plugin includes Chrome DevTools integration for testing TYPO3 frontend/backend.

**Access:**
1. Open Chrome browser via MCP integration
2. Navigate to your TYPO3 instance
3. Inspect elements, check console, monitor network

**Useful for:**
- Testing Fluid templates
- Debugging JavaScript
- Checking API responses
- Validating frontend rendering

---

### Use Case 8: Upgrading TYPO3 Version

**Scenario:** Updating from TYPO3 11 to 12

**Step 1 - Check Compatibility:**
```
/typo3:init
```
Analyzes your extension for version-specific issues.

**Step 2 - Review Breaking Changes:**
```
/typo3:docs "TYPO3 12 breaking changes"
```

**Step 3 - Update Code:**
Ask Claude: "Update my extension for TYPO3 12 compatibility"
- The plugin's guidelines ensure generated code follows TYPO3 v12 standards
- Removes deprecated APIs (ObjectManager, etc.)
- Updates to PSR-14 events
- Uses modern Extbase patterns

---

## 🎯 Recommended Workflows

### Workflow A: Starting a New Extension (15 min)

1. **Scaffold Structure**
   ```
   /typo3:extension my_extension MyVendor
   ```

2. **Create Domain Models**
   ```
   /typo3:model Product "title:string,price:float"
   /typo3:model Category "name:string,description:text"
   ```

3. **Add Controllers**
   ```
   /typo3:controller ProductController list,show,new,create,edit,update,delete
   /typo3:controller CategoryController list,show
   ```

4. **Generate Repositories**
   ```
   /typo3:repository ProductRepository
   /typo3:repository CategoryRepository
   ```

5. **Review & Optimize**
   ```
   /typo3:init
   /typo3:code-simplify scope:all goal:quick
   ```

---

### Workflow B: Daily Development Session

1. **Start Coding** - Guidelines load automatically
2. **Add Features** - Use `/typo3:*` commands as needed
3. **Check Quality** - Plugin suggests code-simplify when needed
4. **Commit** - Hooks remind you to run quality checks
5. **Document** - Use `/typo3:docs` to verify API usage

---

### Workflow C: Code Review Preparation

1. **Check Changed Files**
   ```
   /typo3:code-simplify scope:changed goal:full
   ```

2. **Review Coding Standards**
   - PHP-CS-Fixer runs automatically (PostToolUse hook)
   - Guidelines are always loaded

3. **Verify Documentation**
   ```
   /typo3:docs [topic relevant to your changes]
   ```

4. **Test in Browser** (if frontend changes)
   - Use Chrome DevTools integration

---

## 🎨 Best Practices

### When to Use Commands vs. Natural Language

**Use Commands when:**
- ✅ Scaffolding (extension, model, controller)
- ✅ Searching documentation
- ✅ Refactoring code
- ✅ Creating specific components (ViewHelper, Repository)

**Use Natural Language when:**
- ✅ Explaining complex logic
- ✅ Debugging issues
- ✅ Understanding existing code
- ✅ Custom implementations

**Example:**
```
# Command for scaffolding
/typo3:model User "username:string,email:string"

# Natural language for custom logic
"Add a method to UserRepository that finds users by domain from email address,
considering only active users with verified email"
```

---

### Combining Multiple Commands

**Example: Complete Blog Extension**

```
# 1. Create extension
/typo3:extension blog MyCompany

# 2. Create models
/typo3:model Post "title:string,content:text,published:datetime"
/typo3:model Comment "author:string,text:text,post:Post"

# 3. Create controllers
/typo3:controller PostController list,show,new,create
/typo3:controller CommentController create,delete

# 4. Add ViewHelper
/typo3:viewhelper TruncateText namespace:Format

# 5. Review
/typo3:init
```

---

### Code Quality Pipeline

The plugin helps maintain quality automatically:

1. **During Coding:**
   - Guidelines loaded at session start
   - Pre-write checks for PHP/Fluid/TCA files

2. **Before Commit:**
   - Automatic suggestion to run code-simplify
   - PHP-CS-Fixer runs on PHP files

3. **After Commit:**
   - Session tracking for intelligent suggestions

**To disable suggestions temporarily:**
The hooks have built-in cooldown (15 minutes) and smart triggers (minimum 5 changed files).

---

## 🔧 Advanced Features

### Custom TYPO3 Documentation Version

Set custom branch for documentation:
```
DOC_BRANCH=13.4 /typo3:docs Middleware
```

### Scope-Based Refactoring

```
# Only changed files
/typo3:code-simplify scope:changed

# Only staged files
/typo3:code-simplify scope:staged

# Specific file
/typo3:code-simplify scope:file file:Classes/Controller/MyController.php

# Entire directory
/typo3:code-simplify scope:dir dir:Classes/Domain/Model/

# Everything
/typo3:code-simplify scope:all
```

### Fine-Grained Goals

```
# Quick fixes only (simple improvements)
goal:quick

# Moderate refactoring
goal:moderate

# Deep refactoring (extract methods, simplify logic)
goal:full
```

---

## 💡 Tips & Tricks

### Tip 1: Use Tab Completion
Type `/typo3:` and press Tab to see all available commands.

### Tip 2: Check Session Tracking
```bash
# See when your session started
date -d @$(cat .git/.code-simplify-session-start) '+%Y-%m-%d %H:%M:%S'

# See session duration
echo $(( ($(date +%s) - $(cat .git/.code-simplify-session-start)) / 60 )) minutes
```

### Tip 3: Combine Init + Docs
```
/typo3:init
# Then follow up with:
/typo3:docs [topic suggested by init]
```

### Tip 4: Quick Reference
Keep the command reference handy:
```
/typo3:help
```

### Tip 5: Version-Specific Help
Always specify TYPO3 version when searching docs:
```
/typo3:docs QueryBuilder 12.4
```

---

## 🆘 Common Questions

### "Which command should I use for...?"

| Task | Command | Notes |
|------|---------|-------|
| New extension | `/typo3:extension` | Complete scaffold |
| New model | `/typo3:model` | Includes TCA |
| New controller | `/typo3:controller` | Slim controllers |
| Search API docs | `/typo3:docs` | Version-aware |
| Refactor code | `/typo3:code-simplify` | Multiple scopes |
| Check extension | `/typo3:init` | Comprehensive review |
| Custom ViewHelper | `/typo3:viewhelper` | Fluid component |
| Repository | `/typo3:repository` | Data access |
| TCA configuration | `/typo3:tca` | Database schema |

### "The plugin suggests code-simplify too often"

The plugin is smart about suggestions:
- Only after 5+ file changes
- 15-minute cooldown between suggestions
- Stronger suggestions during long sessions (30+ min)

If it's still too frequent, the cooldown prevents spam.

### "How do I know what the plugin is doing?"

Check loaded features:
```
# In Claude Code UI
Plugins → Installed → typo3-dev → Components
```

Or check session tracking:
```bash
ls -la .git/.code-simplify-*
```

### "Should I use commands or agents?"

**Commands** = Quick, specific tasks (scaffolding, searching)
**Agents** = Complex, multi-step tasks (automatically triggered)

The plugin chooses agents automatically when appropriate. You typically just use commands.

---

## 📚 Next Steps

1. **Try the Workflows Above** - Pick one that matches your task
2. **Explore Commands** - `/typo3:help` shows everything
3. **Read Feature Docs** - See `docs/FEATURES.md` for details
4. **Check Examples** - Real-world patterns in each command

**Need Help?**
- GitHub Issues: https://github.com/PatFischer91/claude-typo3-dev/issues
- Command Reference: `/typo3:help`
- Full Documentation: `docs/` directory

---

**Happy TYPO3 Development! 🚀**
