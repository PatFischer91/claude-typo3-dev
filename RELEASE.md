# Release Process

This document describes the Git Flow workflow for creating releases of the TYPO3 Development Plugin.

## Version Numbering

Follow [Semantic Versioning](https://semver.org):

```
MAJOR.MINOR.PATCH (e.g., 1.0.0)
```

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Examples

- `1.0.0` → `1.0.1`: Bug fix (e.g., fixed typo in command)
- `1.0.0` → `1.1.0`: New feature (e.g., added new command `/typo3:backup`)
- `1.0.0` → `2.0.0`: Breaking change (e.g., renamed command from `/typo3:model` to `/typo3:domain-model`)

## Git Flow Workflow

### Branch Overview

- `main` - Production releases (tagged with versions)
- `develop` - Development branch (next release)
- `feature/*` - Feature branches
- `release/*` - Release preparation branches
- `hotfix/*` - Emergency fixes for production

### 1. Development Workflow

All development happens on `develop` branch or feature branches:

```bash
# Start working on develop
git checkout develop
git pull origin develop

# Create feature branch (optional)
git checkout -b feature/add-new-command

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "feat: Add /typo3:backup command"

# Push to remote
git push origin feature/add-new-command

# Merge back to develop when ready
git checkout develop
git merge feature/add-new-command --no-ff
git push origin develop
```

### 2. Prepare Release

When `develop` is ready for release:

```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Create release branch
git checkout -b release/v1.1.0
```

### 3. Update Version Numbers

Update version in these files:

1. **`typo3-dev/.claude-plugin/plugin.json`**
   ```json
   {
     "version": "1.1.0"
   }
   ```

2. **`.claude-plugin/marketplace.json`**
   ```json
   {
     "plugins": [
       {
         "name": "typo3-dev",
         "version": "1.1.0"
       }
     ]
   }
   ```

3. **`README.md`** (bottom of file)
   ```markdown
   **Version**: 1.1.0 | **Status**: Stable
   ```

4. **`CHANGELOG.md`** (add new version entry)

Commit version bump:

```bash
git add .
git commit -m "chore: Bump version to 1.1.0"
```

### 4. Final Testing

Test the release branch:

```bash
# Install plugin locally
claude --plugin-dir ./typo3-dev

# Test commands
/typo3:init
/typo3:extension test_ext TestVendor
# ... test all changes ...
```

### 5. Merge to Main and Tag

```bash
# Merge release to main
git checkout main
git pull origin main
git merge release/v1.1.0 --no-ff

# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0 - Add backup command and improve documentation"

# Push to remote
git push origin main
git push origin v1.1.0
```

### 6. Merge Back to Develop

```bash
# Merge release changes back to develop
git checkout develop
git merge release/v1.1.0 --no-ff
git push origin develop

# Delete release branch (locally and remotely)
git branch -d release/v1.1.0
git push origin --delete release/v1.1.0
```

## Hotfix Workflow

For urgent fixes to production:

```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/v1.0.1

# Fix the issue
# ... edit files ...

# Commit fix
git add .
git commit -m "fix: Resolve critical bug in model generator"

# Update version numbers (1.0.0 → 1.0.1)
# ... edit plugin.json, marketplace.json, README.md ...
git add .
git commit -m "chore: Bump version to 1.0.1"

# Merge to main and tag
git checkout main
git merge hotfix/v1.0.1 --no-ff
git tag -a v1.0.1 -m "Hotfix v1.0.1 - Fix model generator bug"
git push origin main
git push origin v1.0.1

# Merge to develop
git checkout develop
git merge hotfix/v1.0.1 --no-ff
git push origin develop

# Delete hotfix branch
git branch -d hotfix/v1.0.1
git push origin --delete hotfix/v1.0.1
```

## Pre-Release Checklist

Before creating a release, ensure:

- [ ] All tests pass
- [ ] Documentation is updated
  - [ ] README.md reflects new features
  - [ ] docs/ files are up to date
  - [ ] CHANGELOG.md has new version entry
- [ ] Version numbers updated in all files:
  - [ ] `typo3-dev/.claude-plugin/plugin.json`
  - [ ] `.claude-plugin/marketplace.json`
  - [ ] `README.md`
- [ ] Breaking changes documented in CHANGELOG.md
- [ ] Migration guide provided (if needed)
- [ ] All commands and skills tested
- [ ] MCP servers functional (Chrome DevTools)
- [ ] No sensitive data in commits

## Release Checklist

During release:

- [ ] Create release branch from develop
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Test all functionality
- [ ] Merge to main with `--no-ff`
- [ ] Create annotated tag with meaningful message
- [ ] Push main and tag to remote
- [ ] Merge back to develop
- [ ] Delete release branch
- [ ] Create GitHub release with notes
- [ ] Announce release (if applicable)

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (version bump, dependencies)

### Examples

```bash
feat(commands): Add /typo3:backup command for database backups
fix(model): Resolve incorrect TCA field type generation
docs(readme): Update installation instructions
chore: Bump version to 1.1.0
```

## Version History Example

```
v1.0.0 - 2024-01-16 - Initial stable release
v1.0.1 - 2024-01-20 - Fix model generator bug
v1.1.0 - 2024-02-01 - Add backup command and improve docs
v2.0.0 - 2024-03-15 - Rename commands for consistency (breaking)
```

## GitHub Release Notes

When creating a GitHub release, include:

1. **What's New** - New features
2. **Improvements** - Enhancements to existing features
3. **Bug Fixes** - Fixed issues
4. **Breaking Changes** - Incompatibilities (for major versions)
5. **Migration Guide** - How to upgrade (if needed)

### Example Release Notes

```markdown
## v1.1.0 - Enhanced Documentation & Backup Command

### What's New
- `/typo3:backup` command for database and file backups
- Comprehensive configuration guide (docs/CONFIGURATION.md)

### Improvements
- Improved auto-detection of TYPO3 version
- Better error messages in all commands
- Updated Chrome DevTools integration

### Bug Fixes
- Fixed incorrect namespace generation in models (#42)
- Resolved TCA field type detection bug (#45)

### Installation
```bash
claude plugin marketplace add PatFischer91/claude-typo3-dev
claude plugin install typo3-dev@in2code
```

Full Changelog: https://github.com/PatFischer91/claude-typo3-dev/compare/v1.0.0...v1.1.0
```

## Publishing to Marketplace

After releasing to GitHub:

1. GitHub release is automatically detected by Claude Code marketplace
2. Users can install the new version with:
   ```bash
   /plugin update typo3-dev@in2code
   ```

## Rollback Procedure

If a release has critical issues:

```bash
# Create hotfix branch from previous tag
git checkout -b hotfix/v1.1.1 v1.0.0

# Fix issues
# ... make fixes ...

# Follow hotfix workflow (see above)
```

Or revert the release:

```bash
# Revert merge commit on main
git checkout main
git revert -m 1 <merge-commit-sha>
git push origin main
```

## Support Branches

- Releases follow `main` branch
- Only latest version receives updates
- Critical security fixes may be backported to previous versions

## Questions?

For release process questions, open an issue at:
https://github.com/PatFischer91/claude-typo3-dev/issues
