---
description: Creates a slim TYPO3 Extbase Controller with constructor-based dependency injection and proper ResponseInterface returns
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Create TYPO3 Extbase Controller

Generates a slim Extbase Controller following TYPO3 best practices.

## Usage

```
/typo3:controller <ControllerName> [actions]
```

**Parameters:**
- `ControllerName`: Controller name (e.g., `Product`, `ProductController`)
- `actions`: Optional comma-separated action names (default: `list,show`)

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key and vendor name
- Determine namespace

### 2. Parse Arguments

- Extract controller name (remove "Controller" suffix if present)
- Parse action names if provided
- Default actions: `list`, `show`

### 3. Generate Controller Class

**Path:** `Classes/Controller/<ControllerName>Controller.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;

/**
 * <ControllerName> Controller
 *
 * Handles <ControllerName> related actions.
 */
class <ControllerName>Controller extends ActionController
{
    public function __construct(
        // Inject dependencies here:
        // private readonly <ControllerName>Repository $<controllerName>Repository,
        // private readonly <ControllerName>Service $<controllerName>Service,
    ) {}

    /**
     * List action - displays all items
     */
    public function listAction(): ResponseInterface
    {
        // Example:
        // $items = $this-><controllerName>Repository->findAll();
        // $this->view->assign('items', $items);

        return $this->htmlResponse();
    }

    /**
     * Show action - displays single item details
     *
     * @param int $<controllerName> The item UID
     */
    public function showAction(int $<controllerName>): ResponseInterface
    {
        // Example:
        // $item = $this-><controllerName>Repository->findByUid($<controllerName>);
        // $this->view->assign('item', $item);

        return $this->htmlResponse();
    }
}
```

### 4. Add More Actions (if specified)

For each additional action (e.g., `create`, `update`, `delete`):

```php
/**
 * <ActionName> action
 */
public function <actionName>Action(): ResponseInterface
{
    // Add your logic here
    return $this->htmlResponse();
}
```

**Common action patterns:**

**Create action:**
```php
public function createAction(<ControllerName> $new<ControllerName>): ResponseInterface
{
    $this-><controllerName>Repository->add($new<ControllerName>);
    $this->addFlashMessage('Item created successfully');
    return $this->redirect('list');
}
```

**Update action:**
```php
public function updateAction(<ControllerName> $<controllerName>): ResponseInterface
{
    $this-><controllerName>Repository->update($<controllerName>);
    $this->addFlashMessage('Item updated successfully');
    return $this->redirect('list');
}
```

**Delete action:**
```php
public function deleteAction(<ControllerName> $<controllerName>): ResponseInterface
{
    $this-><controllerName>Repository->remove($<controllerName>);
    $this->addFlashMessage('Item deleted successfully');
    return $this->redirect('list');
}
```

### 5. Create Corresponding Templates

Create template files for each action:

**Path:** `Resources/Private/Templates/<ControllerName>/<ActionName>.html`

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="content">
    <div class="tx-<extensionkey>">
        <f:comment>Template for <ActionName> action</f:comment>
    </div>
</f:section>

</html>
```

## Best Practices Applied

1. **Slim Controller Pattern**
   - No business logic in controller
   - Delegate to services for complex operations
   - Controller only handles request/response flow

2. **Constructor Injection**
   - All dependencies via `__construct()`
   - Use `private readonly` for immutability
   - No ObjectManager or makeInstance

3. **ResponseInterface Returns**
   - All actions return `ResponseInterface`
   - Use `$this->htmlResponse()` for HTML
   - Use `$this->jsonResponse()` for JSON/AJAX

4. **No Global Access**
   - No `$GLOBALS['TSFE']`
   - No direct `$_GET`, `$_POST`
   - Use `$this->request` for request data

5. **Type Declarations**
   - Strict types enabled
   - All parameters typed
   - All return types specified

## Success Message

```
✓ Controller '<ControllerName>Controller' created successfully!

Files created:
- Classes/Controller/<ControllerName>Controller.php
- Resources/Private/Templates/<ControllerName>/List.html
- Resources/Private/Templates/<ControllerName>/Show.html

Next steps:
1. Inject required dependencies (Repository, Service)
2. Register plugin with this controller in ext_localconf.php
3. Implement business logic in service classes
4. Customize templates

Remember: Keep the controller SLIM!
```
