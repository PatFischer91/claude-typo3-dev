# Contributing to TYPO3 Development Plugin

Thank you for your interest in contributing to the TYPO3 Development Plugin for Claude Code!

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Provide clear description and steps to reproduce
- Include Claude Code version and environment details

### Suggesting Features

- Open an issue with `[Feature Request]` prefix
- Describe the use case and expected behavior
- Explain how it benefits TYPO3 developers

### Contributing Code

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code structure
   - Test your changes thoroughly
   - Update documentation if needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe what your PR does
   - Reference any related issues
   - Wait for review

## Development Guidelines

### Adding a New Skill

1. Create directory: `skills/skill-name/`
2. Create `SKILL.md` with YAML frontmatter
3. Write clear, concise description (200 chars max)
4. Add skill instructions and examples
5. Test by triggering matching context
6. Document in `docs/SKILLS.md`

### Adding a New Command

1. Create `commands/command-name.md`
2. Add YAML frontmatter with description
3. Write clear instructions for Claude
4. Include parameter documentation
5. Add examples and expected output
6. Document in `docs/COMMANDS.md`

### Adding a New Hook

1. Edit `hooks/hooks.json`
2. Choose appropriate event type
3. Add matcher pattern (regex)
4. Define hook action (command or prompt)
5. Test hook triggering
6. Document in `docs/HOOKS.md`

### Modifying the MCP Server

1. Edit `mcp/typo3-docs-server/server.py`
2. Follow MCP SDK conventions
3. Add proper type hints
4. Update tool schemas if needed
5. Test with MCP inspector
6. Update `mcp/typo3-docs-server/README.md`

## Code Style

### Python (MCP Server)

- Follow PEP 8
- Use type hints
- Add docstrings for functions
- Keep functions focused and small

### Markdown (Skills, Commands)

- Use clear headings
- Include code examples
- Follow TYPO3 CGL in code snippets
- Keep descriptions concise

### JSON (Hooks, Config)

- Proper indentation (2 spaces)
- No trailing commas
- Validate JSON syntax

## Testing

### Manual Testing

```bash
# Test plugin locally
claude --plugin-dir ./typo3_development

# Test specific command
/typo3:extension test_ext TestVendor

# Test MCP server
cd mcp/typo3-docs-server
python server.py
```

### Validation

- Ensure all JSON files are valid
- Test skills activation with relevant prompts
- Verify commands work with various parameters
- Check hooks trigger correctly

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add examples for new features
- Keep docs in sync with code

## Community Guidelines

- Be respectful and constructive
- Help others learn
- Share knowledge and best practices
- Focus on improving TYPO3 development experience

## Questions?

- Open an issue for questions
- Check existing documentation
- Join TYPO3 Slack #claude-code (if exists)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making TYPO3 development with Claude Code better! 🚀
