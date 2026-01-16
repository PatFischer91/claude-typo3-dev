---
description: Test TYPO3 frontend and backend directly in Chrome browser - manual testing, visual checks, form submissions, backend module testing.
allowed-tools: mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__fill_form, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__new_page, mcp__chrome-devtools__list_network_requests, mcp__chrome-devtools__list_console_messages, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__wait_for, mcp__chrome-devtools__press_key, mcp__chrome-devtools__hover
---

# TYPO3 Browser Testing

Test TYPO3 frontend and backend directly in Chrome browser using Chrome DevTools integration.

## Usage

```
/typo3:test-browser <action> [url_or_description]
```

**Arguments:** $ARGUMENTS

### Actions

| Action | Description |
|--------|-------------|
| `frontend` | Test frontend page |
| `backend` | Test backend module |
| `form` | Test form submission |
| `login` | Test backend login |
| `content` | Test content element |
| `plugin` | Test plugin output |
| `check` | Visual check / screenshot |
| `console` | Check for JS errors |
| `network` | Check network requests |

### Examples

```
/typo3:test-browser frontend https://mysite.ddev.site/
/typo3:test-browser backend "List module"
/typo3:test-browser form "Contact form on /contact"
/typo3:test-browser login
/typo3:test-browser plugin "News list plugin"
/typo3:test-browser check "Homepage hero section"
```

## Testing Workflows

### Frontend Page Test

1. Navigate to the URL
2. Take a snapshot to understand page structure
3. Check for console errors
4. Take screenshot for visual verification
5. Report findings

```
Steps:
1. mcp__chrome-devtools__navigate_page → URL
2. mcp__chrome-devtools__take_snapshot → Get page structure
3. mcp__chrome-devtools__list_console_messages → Check errors
4. mcp__chrome-devtools__take_screenshot → Visual check
5. Report: "Page loaded, no errors, screenshot attached"
```

### Backend Login Test

1. Navigate to `/typo3`
2. Fill username and password
3. Click login button
4. Verify dashboard loads
5. Report success/failure

```
Steps:
1. mcp__chrome-devtools__navigate_page → /typo3
2. mcp__chrome-devtools__take_snapshot → Find login form
3. mcp__chrome-devtools__fill_form → username, password
4. mcp__chrome-devtools__click → Login button
5. mcp__chrome-devtools__wait_for → "Dashboard" or module name
6. mcp__chrome-devtools__take_screenshot → Verify logged in
```

### Backend Module Test

1. Login if needed
2. Navigate to module (via menu click or URL)
3. Take snapshot of module content
4. Interact with module (list, edit, etc.)
5. Verify expected behavior
6. Report findings

### Form Submission Test

1. Navigate to page with form
2. Take snapshot to find form fields
3. Fill form with test data
4. Submit form
5. Check for success message or redirect
6. Verify form finisher executed (email, DB, etc.)

```
Steps:
1. mcp__chrome-devtools__navigate_page → Form page URL
2. mcp__chrome-devtools__take_snapshot → Find form elements
3. mcp__chrome-devtools__fill_form → Fill all required fields
4. mcp__chrome-devtools__click → Submit button
5. mcp__chrome-devtools__wait_for → Success message
6. mcp__chrome-devtools__take_screenshot → Capture result
```

### Plugin Output Test

1. Navigate to page with plugin
2. Take snapshot to find plugin output
3. Verify expected elements exist
4. Test plugin interactions (pagination, filters, etc.)
5. Check for proper data display

### Console Error Check

1. Navigate to page
2. List console messages
3. Filter for errors/warnings
4. Report any JavaScript issues

```
Steps:
1. mcp__chrome-devtools__navigate_page → URL
2. mcp__chrome-devtools__list_console_messages → types: ["error", "warn"]
3. Report: List all errors with context
```

### Network Request Analysis

1. Navigate to page
2. List network requests
3. Check for failed requests (4xx, 5xx)
4. Analyze AJAX/API calls
5. Report issues

```
Steps:
1. mcp__chrome-devtools__navigate_page → URL
2. mcp__chrome-devtools__list_network_requests
3. Filter for failed requests
4. mcp__chrome-devtools__get_network_request → Details for problematic requests
```

## TYPO3-Specific Testing

### Backend Selectors (Common)

| Element | Typical Selector Pattern |
|---------|-------------------------|
| Module menu | `.scaffold-modulemenu` |
| Module content | `.module-body` |
| List records | `.recordlist` |
| Edit form | `.form-section` |
| Save button | `button[name="_savedok"]` |
| Docheader | `.module-docheader` |
| Flash messages | `.alert` |
| Page tree | `.scaffold-content-navigation-component` |

### Frontend Selectors (Common)

| Element | Typical Pattern |
|---------|----------------|
| Content elements | `.frame-type-*` |
| News list | `.news-list` |
| Powermail form | `.powermail_form` |
| Navigation | `nav`, `.main-navigation` |
| Footer | `footer`, `.footer` |

### Test Data Suggestions

For form testing, use:
- Email: `test@example.com`
- Name: `Test User`
- Phone: `+49 123 456789`
- Message: `This is an automated test submission.`

## Output Format

After testing, provide:

```markdown
## Browser Test Results

**Test:** <description>
**URL:** <tested URL>
**Status:** ✅ Passed / ❌ Failed / ⚠️ Warning

### Findings

1. <Finding 1>
2. <Finding 2>

### Console Errors
- <Error 1> (if any)

### Screenshots
[Screenshots attached]

### Recommendations
- <Recommendation 1>
```

## Important Notes

- Always take snapshots before interacting to understand page structure
- Use `wait_for` after navigation or form submission to ensure page is ready
- Check console messages for hidden errors
- Backend testing may require login first
- DDEV sites typically use `.ddev.site` domain
- For HTTPS warnings, the browser may need to accept the certificate first
