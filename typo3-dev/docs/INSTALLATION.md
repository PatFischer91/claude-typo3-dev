# Installation Guide

## Quick Installation

### Option 1: Via Plugin Manager (Recommended)

```bash
# In Claude Code, open plugin manager
/plugin

# Then select "Discover" and search for "typo3"
# Or add the marketplace directly:
/plugin marketplace add PatFischer91/claude-typo3-dev
```

### Option 2: Direct Installation

```bash
# Install directly from GitHub
/plugin install typo3-dev@in2code
```

### Option 3: CLI Installation

```bash
# From your terminal
claude plugin marketplace add PatFischer91/claude-typo3-dev
claude plugin install typo3-dev@in2code
```

### Option 4: Manual Installation

```bash
# Clone to your plugins directory
git clone https://github.com/PatFischer91/claude-typo3-dev.git ~/.claude/plugins/in2code

# Or for project-specific installation
git clone https://github.com/PatFischer91/claude-typo3-dev.git .claude/plugins/in2code
```

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
# Via plugin manager
/plugin uninstall typo3-dev

# Or via CLI
claude plugin uninstall typo3-dev@in2code
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

### Plugin not found

Make sure the marketplace is added:
```bash
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
