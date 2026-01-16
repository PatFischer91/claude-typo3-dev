---
description: Creates a complete TYPO3 Extbase plugin with controller, templates, TypoScript, and FlexForm configuration
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Create TYPO3 Extbase Plugin

Creates a complete frontend plugin setup following TYPO3 best practices.

## Usage

```
/typo3:plugin <PluginName> [description]
```

**Parameters:**
- `PluginName`: Plugin name in StudlyCase (e.g., `ProductList`, `NewsDisplay`)
- `description`: Optional plugin description

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

First, detect the current extension:
- Look for `ext_emconf.php` or `composer.json` in current directory or parent
- Extract extension key and vendor name
- If not in extension, ask user which extension to use

### 2. Parse Arguments

Extract plugin name from `$ARGUMENTS`. Convert to proper formats:
- PluginName: StudlyCase (e.g., `ProductList`)
- plugin_name: lowercase with underscores (e.g., `product_list`)
- pluginname: lowercase no separators (e.g., `productlist`)

### 3. Create Controller

**Path:** `Classes/Controller/<PluginName>Controller.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;

/**
 * <PluginName> Controller
 */
class <PluginName>Controller extends ActionController
{
    public function __construct(
        // Add your dependencies here via constructor injection
    ) {}

    /**
     * List action
     */
    public function listAction(): ResponseInterface
    {
        // Add your logic here
        return $this->htmlResponse();
    }

    /**
     * Show action
     */
    public function showAction(): ResponseInterface
    {
        // Add your logic here
        return $this->htmlResponse();
    }
}
```

### 4. Create Fluid Templates

**Path:** `Resources/Private/Templates/<PluginName>/List.html`

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="content">
    <div class="tx-<extensionkey>-<pluginname>">
        <h1><f:translate key="<pluginname>.list.title" /></h1>

        <f:comment>Add your template content here</f:comment>
    </div>
</f:section>

</html>
```

**Path:** `Resources/Private/Templates/<PluginName>/Show.html`

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="content">
    <div class="tx-<extensionkey>-<pluginname>">
        <h1><f:translate key="<pluginname>.show.title" /></h1>

        <f:comment>Add your template content here</f:comment>
    </div>
</f:section>

</html>
```

### 5. Create Default Layout

**Path:** `Resources/Private/Layouts/Default.html` (if not exists)

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:render section="content" />

</html>
```

### 6. Register Plugin in ext_localconf.php

Add to `ext_localconf.php`:

```php
\TYPO3\CMS\Extbase\Utility\ExtensionUtility::configurePlugin(
    '<ExtensionKeyStudlyCase>',
    '<PluginName>',
    [
        \<VendorName>\<ExtensionKeyStudlyCase>\Controller\<PluginName>Controller::class => 'list, show',
    ],
    // Non-cacheable actions
    [
        \<VendorName>\<ExtensionKeyStudlyCase>\Controller\<PluginName>Controller::class => '',
    ]
);
```

### 7. Register Plugin in ext_tables.php

Add to `ext_tables.php`:

```php
\TYPO3\CMS\Extbase\Utility\ExtensionUtility::registerPlugin(
    '<ExtensionKeyStudlyCase>',
    '<PluginName>',
    'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:plugin.<pluginname>.title',
    'extension-<extension_key>-<pluginname>',
    'plugins'
);
```

### 8. Create FlexForm

**Path:** `Configuration/FlexForms/<PluginName>.xml`

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<T3DataStructure>
    <sheets>
        <sDEF>
            <ROOT>
                <sheetTitle>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sheet.general</sheetTitle>
                <type>array</type>
                <el>
                    <settings.itemsPerPage>
                        <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.itemsPerPage</label>
                        <config>
                            <type>number</type>
                            <size>5</size>
                            <default>10</default>
                        </config>
                    </settings.itemsPerPage>
                </el>
            </ROOT>
        </sDEF>
    </sheets>
</T3DataStructure>
```

### 9. Register FlexForm in TCA/Overrides

**Path:** `Configuration/TCA/Overrides/tt_content.php`

Add or create:

```php
<?php

defined('TYPO3') || die();

$GLOBALS['TCA']['tt_content']['types']['list']['subtypes_addlist']['<extensionkey>_<pluginname>'] = 'pi_flexform';

\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addPiFlexFormValue(
    '<extensionkey>_<pluginname>',
    'FILE:EXT:<extension_key>/Configuration/FlexForms/<PluginName>.xml'
);
```

### 10. Add Language Labels

**Path:** `Resources/Private/Language/locallang_be.xlf`

```xml
<trans-unit id="plugin.<pluginname>.title">
    <source><PluginName></source>
</trans-unit>
<trans-unit id="flexform.sheet.general">
    <source>General Settings</source>
</trans-unit>
<trans-unit id="flexform.itemsPerPage">
    <source>Items per page</source>
</trans-unit>
```

**Path:** `Resources/Private/Language/locallang.xlf`

```xml
<trans-unit id="<pluginname>.list.title">
    <source><PluginName> List</source>
</trans-unit>
<trans-unit id="<pluginname>.show.title">
    <source><PluginName> Details</source>
</trans-unit>
```

### 11. Create Plugin Icon

Create SVG icon at `Resources/Public/Icons/Extension-<pluginname>.svg`

## Success Message

```
✓ Plugin '<PluginName>' created successfully!

Files created:
- Classes/Controller/<PluginName>Controller.php
- Resources/Private/Templates/<PluginName>/List.html
- Resources/Private/Templates/<PluginName>/Show.html
- Configuration/FlexForms/<PluginName>.xml
- Configuration/TCA/Overrides/tt_content.php (updated)
- ext_localconf.php (updated)
- ext_tables.php (updated)
- Resources/Private/Language/locallang_be.xlf (updated)

Next steps:
1. Clear cache: typo3 cache:flush
2. Add plugin to a page via backend
3. Inject dependencies in controller constructor
4. Add business logic to service classes
```

## Important Notes

- Controller must return `ResponseInterface`
- Use constructor injection for dependencies
- Keep controller slim - business logic in services
- No `$GLOBALS['TSFE']` - use `$this->request`
- FlexForm settings available via `$this->settings`
