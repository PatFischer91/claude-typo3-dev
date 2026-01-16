---
description: Creates complete TYPO3 extension structure with best practices, composer.json, TCA configuration, and proper directory layout
---

# Create TYPO3 Extension

Creates a complete TYPO3 extension structure following best practices and TYPO3 CGL.

## Usage

```
/typo3:extension <extension_key> <vendor_name> [description]
```

**Parameters:**
- `extension_key`: Extension key (e.g., `blog_extension`, `my_shop`)
- `vendor_name`: Vendor name in StudlyCase (e.g., `MyCompany`)
- `description`: Optional extension description

## What This Command Does

1. Creates complete directory structure
2. Generates `composer.json` with proper dependencies
3. Creates `ext_emconf.php` with metadata
4. Sets up `ext_localconf.php` and `ext_tables.php`
5. Creates directory structure for Classes, Resources, Configuration
6. Adds `.gitignore` and basic documentation

## Steps

### 1. Parse Arguments

Extract the extension key, vendor name, and optional description from `$ARGUMENTS`.

**Format expected:**
```
extension_key VendorName "Optional description"
```

### 2. Validate Input

- Extension key must be lowercase with underscores
- Vendor name must be StudlyCase
- No spaces in extension key or vendor

### 3. Create Directory Structure

Create the following structure:

```
<extension_key>/
├── .gitignore
├── composer.json
├── ext_emconf.php
├── ext_localconf.php
├── ext_tables.php
├── ext_tables.sql
├── README.md
├── Classes/
│   ├── Controller/
│   ├── Domain/
│   │   ├── Model/
│   │   ├── Repository/
│   │   └── Validator/
│   ├── Service/
│   ├── Utility/
│   └── ViewHelpers/
├── Configuration/
│   ├── TCA/
│   ├── TypoScript/
│   │   ├── setup.typoscript
│   │   └── constants.typoscript
│   ├── Services.yaml
│   └── RequestMiddlewares.php
└── Resources/
    ├── Private/
    │   ├── Language/
    │   │   └── locallang.xlf
    │   ├── Layouts/
    │   ├── Partials/
    │   └── Templates/
    └── Public/
        ├── Css/
        ├── JavaScript/
        └── Icons/
            └── Extension.svg
```

### 4. Generate composer.json

```json
{
    "name": "<vendor_name_lowercase>/<extension_key_with_dashes>",
    "type": "typo3-cms-extension",
    "description": "<description or default>",
    "license": "GPL-2.0-or-later",
    "require": {
        "typo3/cms-core": "^12.4",
        "typo3/cms-extbase": "^12.4",
        "typo3/cms-fluid": "^12.4"
    },
    "autoload": {
        "psr-4": {
            "<VendorName>\\<ExtensionKeyStudlyCase>\\": "Classes/"
        }
    },
    "extra": {
        "typo3/cms": {
            "extension-key": "<extension_key>"
        }
    }
}
```

**Note:** Convert extension_key to StudlyCase for PSR-4 namespace (e.g., `blog_extension` → `BlogExtension`)

### 5. Generate ext_emconf.php

```php
<?php

$EM_CONF[$_EXTKEY] = [
    'title' => '<Extension Title>',
    'description' => '<description>',
    'category' => 'plugin',
    'author' => '',
    'author_email' => '',
    'state' => 'alpha',
    'clearCacheOnLoad' => true,
    'version' => '1.0.0',
    'constraints' => [
        'depends' => [
            'typo3' => '12.4.0-12.4.99',
        ],
        'conflicts' => [],
        'suggests' => [],
    ],
];
```

### 6. Generate ext_localconf.php

```php
<?php

defined('TYPO3') || die();

(function () {
    // Register icons
    $iconRegistry = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
        \TYPO3\CMS\Core\Imaging\IconRegistry::class
    );
    $iconRegistry->registerIcon(
        'extension-<extension_key>',
        \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        ['source' => 'EXT:<extension_key>/Resources/Public/Icons/Extension.svg']
    );

    // Configure plugins here when needed
    // \TYPO3\CMS\Extbase\Utility\ExtensionUtility::configurePlugin(
    //     '<ExtensionKeyStudlyCase>',
    //     'PluginName',
    //     [
    //         \<VendorName>\<ExtensionKeyStudlyCase>\Controller\MyController::class => 'list, show',
    //     ],
    //     // Non-cacheable actions
    //     [
    //         \<VendorName>\<ExtensionKeyStudlyCase>\Controller\MyController::class => 'create, update, delete',
    //     ]
    // );
})();
```

### 7. Generate ext_tables.php

```php
<?php

defined('TYPO3') || die();

(function () {
    // Add static TypoScript
    \TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addStaticFile(
        '<extension_key>',
        'Configuration/TypoScript',
        '<Extension Title>'
    );
})();
```

### 8. Generate Configuration/Services.yaml

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  <VendorName>\<ExtensionKeyStudlyCase>\:
    resource: '../Classes/*'

  # Exclude Domain Models from autowiring
  <VendorName>\<ExtensionKeyStudlyCase>\Domain\Model\:
    resource: '../Classes/Domain/Model/*'
    autowire: false
    autoconfigure: false
```

### 9. Generate TypoScript Files

**Configuration/TypoScript/setup.typoscript:**

```typoscript
plugin.tx_<extension_key_no_underscores> {
    view {
        templateRootPaths {
            0 = EXT:<extension_key>/Resources/Private/Templates/
        }
        partialRootPaths {
            0 = EXT:<extension_key>/Resources/Private/Partials/
        }
        layoutRootPaths {
            0 = EXT:<extension_key>/Resources/Private/Layouts/
        }
    }
    persistence {
        storagePid =
    }
    settings {
    }
}
```

**Configuration/TypoScript/constants.typoscript:**

```typoscript
plugin.tx_<extension_key_no_underscores> {
    view {
        # Path to template root (FE)
        templateRootPath = EXT:<extension_key>/Resources/Private/Templates/
        # Path to template partials (FE)
        partialRootPath = EXT:<extension_key>/Resources/Private/Partials/
        # Path to template layouts (FE)
        layoutRootPath = EXT:<extension_key>/Resources/Private/Layouts/
    }
    persistence {
        # Storage PID for records
        # cat=plugin.<extension_key>//a; type=int+; label=Default storage PID
        storagePid =
    }
}
```

### 10. Generate locallang.xlf

**Resources/Private/Language/locallang.xlf:**

```xml
<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<xliff version="1.0">
    <file source-language="en" datatype="plaintext" original="messages" date="2024-01-16T12:00:00Z" product-name="<extension_key>">
        <header/>
        <body>
            <trans-unit id="extension.title">
                <source><Extension Title></source>
            </trans-unit>
            <trans-unit id="extension.description">
                <source><Extension Description></source>
            </trans-unit>
        </body>
    </file>
</xliff>
```

### 11. Generate .gitignore

```
.Build/
.idea/
.vscode/
composer.lock
vendor/
*.log
.DS_Store
```

### 12. Generate README.md

```markdown
# <Extension Title>

<Description>

## Installation

Install via composer:

```bash
composer require <vendor_name_lowercase>/<extension_key_with_dashes>
```

## Configuration

1. Include the static TypoScript template
2. Configure the storage PID in TypoScript constants

## Usage

<Add usage instructions here>

## Development

### Requirements

- TYPO3 12.4 or higher
- PHP 8.1 or higher

### Setup

```bash
composer install
```

## License

GPL-2.0-or-later
```

### 13. Create Icon Placeholder

Create a simple SVG icon at `Resources/Public/Icons/Extension.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
    <rect width="16" height="16" fill="#FF8700"/>
    <text x="8" y="12" font-family="Arial" font-size="10" fill="white" text-anchor="middle">EXT</text>
</svg>
```

## Success Message

Display a success message with:
- Extension location
- Next steps (activate in Extension Manager, add TCA, create models)
- Command suggestions for next steps

Example:
```
✓ Extension '<extension_key>' created successfully!

Location: ./<extension_key>/

Next steps:
1. Activate extension in Extension Manager or via: typo3 extension:activate <extension_key>
2. Create domain model: /typo3:model Product "A product entity"
3. Create controller: /typo3:controller ProductController
4. Include static TypoScript in your site template

Happy coding!
```

## Important Notes

- Ensure `defined('TYPO3') || die();` is used in all PHP config files (NOT `or die()`)
- Use proper PSR-4 namespacing: `<VendorName>\<ExtensionKeyStudlyCase>\`
- All PHP files must have `declare(strict_types=1);`
- Follow TYPO3 CGL and PSR-12
- Extension key uses underscores, but namespace uses StudlyCase
