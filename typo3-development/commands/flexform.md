---
description: Creates a FlexForm XML configuration for TYPO3 plugins with sheets, fields, and proper structure
allowed-tools: Read, Write, Edit, Glob
---

# Create TYPO3 FlexForm

Generates FlexForm XML configuration for plugin settings.

## Usage

```
/typo3:flexform <PluginName> [fields]
```

**Parameters:**
- `PluginName`: Plugin name to create FlexForm for
- `fields`: Optional comma-separated field definitions (e.g., `itemsPerPage:int,showImages:bool`)

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Find extension key and vendor name
- Determine plugin identifier

### 2. Generate FlexForm XML

**Path:** `Configuration/FlexForms/<PluginName>.xml`

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<T3DataStructure>
    <meta>
        <langChildren>0</langChildren>
    </meta>
    <sheets>
        <sDEF>
            <ROOT>
                <sheetTitle>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sheet.general</sheetTitle>
                <type>array</type>
                <el>
                    <!-- Settings fields -->
                    <settings.itemsPerPage>
                        <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.itemsPerPage</label>
                        <config>
                            <type>number</type>
                            <size>5</size>
                            <default>10</default>
                        </config>
                    </settings.itemsPerPage>

                    <settings.showImages>
                        <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.showImages</label>
                        <config>
                            <type>check</type>
                            <renderType>checkboxToggle</renderType>
                            <default>1</default>
                        </config>
                    </settings.showImages>

                    <settings.sortOrder>
                        <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sortOrder</label>
                        <config>
                            <type>select</type>
                            <renderType>selectSingle</renderType>
                            <items>
                                <numIndex index="0">
                                    <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sortOrder.asc</label>
                                    <value>ASC</value>
                                </numIndex>
                                <numIndex index="1">
                                    <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sortOrder.desc</label>
                                    <value>DESC</value>
                                </numIndex>
                            </items>
                            <default>ASC</default>
                        </config>
                    </settings.sortOrder>
                </el>
            </ROOT>
        </sDEF>

        <sDisplay>
            <ROOT>
                <sheetTitle>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.sheet.display</sheetTitle>
                <type>array</type>
                <el>
                    <settings.template>
                        <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.template</label>
                        <config>
                            <type>select</type>
                            <renderType>selectSingle</renderType>
                            <items>
                                <numIndex index="0">
                                    <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.template.default</label>
                                    <value>Default</value>
                                </numIndex>
                                <numIndex index="1">
                                    <label>LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:flexform.template.grid</label>
                                    <value>Grid</value>
                                </numIndex>
                            </items>
                        </config>
                    </settings.template>
                </el>
            </ROOT>
        </sDisplay>
    </sheets>
</T3DataStructure>
```

### 3. Field Type Mappings

| Type | FlexForm Config |
|------|-----------------|
| `string` | `<type>input</type>` |
| `text` | `<type>text</type><rows>5</rows>` |
| `int` | `<type>number</type>` |
| `bool` | `<type>check</type><renderType>checkboxToggle</renderType>` |
| `select` | `<type>select</type><renderType>selectSingle</renderType>` |
| `link` | `<type>link</type>` |
| `file` | `<type>file</type>` |
| `page` | `<type>group</type><allowed>pages</allowed>` |
| `folder` | `<type>folder</type>` |
| `color` | `<type>color</type>` |
| `datetime` | `<type>datetime</type>` |

### 4. Register FlexForm

Update `Configuration/TCA/Overrides/tt_content.php`:

```php
<?php

defined('TYPO3') || die();

// Add FlexForm
$GLOBALS['TCA']['tt_content']['types']['list']['subtypes_addlist']['<extensionkey>_<pluginname>'] = 'pi_flexform';

\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addPiFlexFormValue(
    '<extensionkey>_<pluginname>',
    'FILE:EXT:<extension_key>/Configuration/FlexForms/<PluginName>.xml'
);

// Remove default fields (optional)
$GLOBALS['TCA']['tt_content']['types']['list']['subtypes_excludelist']['<extensionkey>_<pluginname>'] = 'recursive,select_key,pages';
```

### 5. Access in Controller

```php
// FlexForm settings are available via $this->settings
$itemsPerPage = (int)($this->settings['itemsPerPage'] ?? 10);
$showImages = (bool)($this->settings['showImages'] ?? true);
```

## Success Message

```
✓ FlexForm for '<PluginName>' created!

Files created/updated:
- Configuration/FlexForms/<PluginName>.xml
- Configuration/TCA/Overrides/tt_content.php

Access settings in controller:
$this->settings['fieldName']

Next steps:
1. Add language labels to locallang_be.xlf
2. Clear cache: typo3 cache:flush
3. Edit plugin in backend to see FlexForm
```
