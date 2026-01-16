---
name: browser-testing
description: Knowledge about testing TYPO3 frontend and backend in Chrome browser using DevTools MCP. Use when testing pages, forms, plugins, or backend modules.
---

# TYPO3 Browser Testing Skill

Knowledge and best practices for testing TYPO3 applications directly in Chrome browser using Chrome DevTools MCP integration.

## When to Use Browser Testing

Use browser testing for:
- **Visual verification** of frontend changes
- **Form testing** with real submissions
- **Backend module** functionality testing
- **JavaScript error** detection
- **Network request** analysis
- **Plugin output** verification
- **Content element** rendering checks

## Available Chrome DevTools Tools

### Navigation & Pages
- `mcp__chrome-devtools__navigate_page` - Navigate to URL
- `mcp__chrome-devtools__new_page` - Open new tab
- `mcp__chrome-devtools__list_pages` - List open tabs
- `mcp__chrome-devtools__select_page` - Switch tabs

### Page Analysis
- `mcp__chrome-devtools__take_snapshot` - Get page structure (accessibility tree)
- `mcp__chrome-devtools__take_screenshot` - Capture visual state
- `mcp__chrome-devtools__wait_for` - Wait for text to appear

### Interaction
- `mcp__chrome-devtools__click` - Click element
- `mcp__chrome-devtools__fill` - Fill single input
- `mcp__chrome-devtools__fill_form` - Fill multiple inputs
- `mcp__chrome-devtools__hover` - Hover over element
- `mcp__chrome-devtools__press_key` - Keyboard input

### Debugging
- `mcp__chrome-devtools__list_console_messages` - Get JS console output
- `mcp__chrome-devtools__list_network_requests` - Get HTTP requests
- `mcp__chrome-devtools__evaluate_script` - Run JavaScript

## TYPO3-Specific Testing Patterns

### Frontend Page Testing
```
1. Navigate to page URL
2. Take snapshot to analyze structure
3. Check console for JS errors
4. Take screenshot for visual verification
5. Report findings
```

### Backend Login
```
1. Navigate to /typo3
2. Take snapshot to find login form
3. Fill username and password fields
4. Click login button
5. Wait for dashboard to load
6. Verify with screenshot
```

### Form Submission
```
1. Navigate to page with form
2. Take snapshot to identify form fields
3. Fill form with test data
4. Click submit button
5. Wait for success message
6. Verify submission result
```

### Plugin Testing
```
1. Navigate to page with plugin
2. Take snapshot to find plugin output
3. Interact with plugin (pagination, filters, etc.)
4. Verify data displays correctly
5. Check for AJAX errors in network/console
```

## TYPO3 Backend Selectors

| Element | Selector Pattern |
|---------|-----------------|
| Module menu | `.scaffold-modulemenu` |
| Page tree | `.scaffold-content-navigation` |
| Content area | `.module-body` |
| Docheader | `.module-docheader` |
| Save button | `button[name="_savedok"]` |
| Record list | `.recordlist` |
| Flash messages | `.alert`, `.typo3-message` |

## TYPO3 Frontend Selectors

| Element | Selector Pattern |
|---------|-----------------|
| Content elements | `.frame-type-*` |
| News list | `.news-list-view` |
| News detail | `.news-detail` |
| Powermail form | `.powermail_form` |
| Form framework | `.form-element` |
| Navigation | `nav`, `.main-navigation` |

## Test Data Defaults

When testing forms, use these defaults:
- **Name:** Test User
- **Email:** test@example.com
- **Phone:** +49 123 456789
- **Address:** Test Street 123, 12345 Test City
- **Message:** Automated test submission

## Best Practices

### Always Do
1. **Take snapshots first** - Understand page structure before interacting
2. **Use wait_for** - Ensure pages/elements are loaded
3. **Check console messages** - Catch JavaScript errors
4. **Capture screenshots** - Document test results
5. **Verify network requests** - Find failed API calls

### Avoid
1. **Clicking without snapshot** - May click wrong element
2. **Skipping wait_for** - May interact before page ready
3. **Ignoring console errors** - May miss important issues
4. **Missing screenshots** - No visual proof of results

## Common Testing Scenarios

### Smoke Test
Quick health check:
1. Load homepage
2. Check for JS errors
3. Verify key content
4. Test navigation

### Form Validation Test
1. Submit empty form → Expect validation errors
2. Submit invalid data → Expect specific errors
3. Submit valid data → Expect success

### Content Verification
1. Navigate to page
2. Verify expected elements exist
3. Check content structure
4. Take screenshots

### Performance Check
1. Navigate to page
2. Check network requests for failures
3. Look for slow requests
4. Analyze resource loading

## Integration with Development Workflow

When developing TYPO3 features:
1. Make code changes
2. Use `/typo3:test-browser` to verify in browser
3. Check for regressions
4. Document with screenshots

For automated testing, use the `typo3-browser-tester` agent to run comprehensive test suites.

## Related Commands

- `/typo3:test-browser` - Manual browser testing command
- `typo3-browser-tester` agent - Automated testing agent
