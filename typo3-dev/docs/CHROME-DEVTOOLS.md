# Chrome DevTools Integration

This plugin includes integration with Chrome DevTools via MCP (Model Context Protocol), enabling browser automation and testing for TYPO3 frontend development.

## Features

- **Take Screenshots** - Capture viewport or full-page screenshots
- **DOM Inspection** - Analyze page structure and accessibility tree
- **Network Monitoring** - Track HTTP requests and responses
- **Console Logs** - Access browser console messages
- **Automated Testing** - Click, type, navigate programmatically
- **Performance Analysis** - Measure Core Web Vitals

## Setup

### Prerequisites

1. **Google Chrome** installed
2. **Node.js** 18+ installed
3. Chrome must be running with remote debugging enabled

### Start Chrome with Remote Debugging

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

### Enable in Plugin

The Chrome DevTools MCP is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-devtools-server"]
    }
  }
}
```

## Usage Examples

### Test TYPO3 Frontend

```
Please open my TYPO3 site at http://localhost:8000 and take a screenshot
```

```
Navigate to the contact page and check if the form is visible
```

```
Test the mobile navigation by resizing to 375px width
```

### Debug Layout Issues

```
Take a screenshot of the homepage and identify any layout issues
```

```
Check the accessibility tree for the main navigation
```

### Performance Testing

```
Analyze the page load performance and identify bottlenecks
```

```
Check Core Web Vitals for the homepage
```

### Form Testing

```
Fill out the contact form with test data and submit it
```

```
Test form validation by submitting empty required fields
```

### Network Analysis

```
List all network requests made when loading the product page
```

```
Check if there are any failed API requests
```

## Available Actions

| Action | Description |
|--------|-------------|
| `navigate_page` | Go to a URL |
| `take_screenshot` | Capture current viewport |
| `take_snapshot` | Get accessibility tree |
| `click` | Click an element |
| `fill` | Type into input fields |
| `hover` | Hover over element |
| `press_key` | Press keyboard keys |
| `list_network_requests` | Show HTTP requests |
| `list_console_messages` | Show console logs |
| `evaluate_script` | Run JavaScript |
| `resize_page` | Change viewport size |

## TYPO3-Specific Testing Scenarios

### Test Content Elements

```
Navigate to /content-examples and verify all content elements render correctly
```

### Test Responsive Design

```
Test the page at these breakpoints: 320px, 768px, 1024px, 1440px
Take screenshots at each size
```

### Test Backend Login

```
Navigate to /typo3 and test the login form with invalid credentials
Verify the error message appears
```

### Test Form Extensions (Powermail, etc.)

```
Navigate to the contact page
Fill the form with:
- Name: Test User
- Email: test@example.com
- Message: This is a test message
Submit and verify the success message
```

### Test News Extension

```
Navigate to /news
Click on the first news article
Verify the detail view loads correctly
Check for proper meta tags
```

## Tips

1. **Start Simple** - Begin with navigation and screenshots
2. **Use Selectors** - Reference elements by their accessibility labels
3. **Check Console** - Monitor for JavaScript errors
4. **Network Tab** - Verify API calls work correctly
5. **Responsive Testing** - Test multiple viewport sizes

## Troubleshooting

### "Cannot connect to Chrome"

Ensure Chrome is running with `--remote-debugging-port=9222`

### "Element not found"

- Wait for page to fully load
- Use `take_snapshot` to see available elements
- Check if element is in an iframe

### "Permission denied"

Ensure the MCP server has necessary permissions

## Security Notes

- Only use on development/staging environments
- Don't expose remote debugging port publicly
- Be careful with form submissions on production

## References

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [MCP Documentation](https://modelcontextprotocol.io/)
