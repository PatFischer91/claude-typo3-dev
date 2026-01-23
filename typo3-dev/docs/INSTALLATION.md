# Installation Guide

## Quick Installation (2 Steps)

### Step 1: Add the Marketplace

```bash
# In Claude Code
/plugin marketplace add PatFischer91/claude-typo3-dev

# Or via CLI
claude plugin marketplace add PatFischer91/claude-typo3-dev
```

### Step 2: Install the Plugin

```bash
# In Claude Code
/plugin install typo3-dev@in2code

# Or via CLI
claude plugin install typo3-dev@in2code
```

The plugin will be installed globally and available in all your Claude Code projects.

## Requirements

### For MCP Servers (Optional)

The plugin includes MCP servers for enhanced functionality:

```bash
# TYPO3 Documentation Server
pip install mcp httpx

# Chrome DevTools (for browser testing)
npm install -g @anthropic-ai/mcp-devtools-server
```

### Chrome DevTools Setup

To use browser testing features, start Chrome with remote debugging:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug

# Linux
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir=C:\temp\chrome-debug
```

## Verification

After installation, verify the plugin is active:

```bash
# List installed plugins
/plugin installed

# Test a command
/typo3:init
```

## Uninstallation

```bash
# Via CLI
claude plugin uninstall typo3-dev

# Or via plugin manager in Claude Code
/plugin uninstall typo3-dev
```

## Updating

```bash
# Update marketplace index
/plugin marketplace update

# Reinstall plugin for latest version
/plugin uninstall typo3-dev
/plugin install typo3-dev@in2code
```

## Troubleshooting

### "Plugin not found" error

**Problem:** You forgot to add the marketplace first.

**Solution:**
```bash
# Step 1: Add marketplace
claude plugin marketplace add PatFischer91/claude-typo3-dev

# Step 2: Install plugin
claude plugin install typo3-dev@in2code
```

### "Marketplace not found" error

**Problem:** The marketplace URL is incorrect or not accessible.

**Solution:** Verify the marketplace was added correctly:
```bash
# List configured marketplaces
/plugin marketplace list

# Re-add if needed
/plugin marketplace add PatFischer91/claude-typo3-dev
```

### MCP Server errors

Check Python dependencies:
```bash
pip install --upgrade mcp httpx
```

### Commands not working

Verify plugin is installed:
```bash
/plugin installed
```

## Project vs Global Installation

| Scope | Location | Use Case |
|-------|----------|----------|
| Global | `~/.claude/plugins/` | Available in all projects |
| Project | `.claude/plugins/` | Only for specific project |

For TYPO3 development, **global installation** is recommended since you'll use it across multiple projects.
