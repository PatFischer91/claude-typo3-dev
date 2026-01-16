---
description: Generates complete Domain Model with Repository, TCA configuration, and database schema for TYPO3 Extbase
---

# Create TYPO3 Domain Model

Generates a complete Domain Model setup including:
- Extbase Domain Model class
- Repository class
- TCA (Table Configuration Array)
- Database schema in ext_tables.sql

## Usage

```
/typo3:model <ModelName> [properties] [description]
```

**Parameters:**
- `ModelName`: Model name in StudlyCase (e.g., `Product`, `BlogPost`)
- `properties`: Optional comma-separated properties with types (e.g., `title:string,price:float,stock:int`)
- `description`: Optional model description for TCA

**Examples:**
```
/typo3:model Product "A product in the shop"
/typo3:model Product "title:string,price:float,stock:int,active:bool" "Shop product"
/typo3:model BlogPost "title:string,content:text,author:string,publishedAt:datetime"
```

## Steps

### 1. Detect Extension Context

- Check if we're in an extension directory (look for `ext_emconf.php`)
- Extract extension key and vendor name from `composer.json`
- If not in extension, ask user which extension or create new one

### 2. Parse Model Properties

If properties are provided, parse them:

**Format:** `propertyName:type,propertyName:type`

**Supported types:**
- `string` → varchar(255)
- `text` → text
- `int` / `integer` → int(11)
- `float` / `double` → decimal(10,2)
- `bool` / `boolean` → tinyint(1)
- `datetime` → int(11) unsigned (TYPO3 uses timestamps)
- `date` → int(11) unsigned

**Default properties** (if none provided):
- `title:string`
- `description:text`

### 3. Generate Domain Model Class

**Path:** `Classes/Domain/Model/<ModelName>.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Domain\Model;

use TYPO3\CMS\Extbase\DomainObject\AbstractEntity;

/**
 * <ModelName> Model
 *
 * <Description>
 */
class <ModelName> extends AbstractEntity
{
    /**
     * Title
     *
     * @var string
     */
    protected string $title = '';

    /**
     * Description
     *
     * @var string
     */
    protected string $description = '';

    // Add additional properties based on input...

    /**
     * @return string
     */
    public function getTitle(): string
    {
        return $this->title;
    }

    /**
     * @param string $title
     */
    public function setTitle(string $title): void
    {
        $this->title = $title;
    }

    /**
     * @return string
     */
    public function getDescription(): string
    {
        return $this->description;
    }

    /**
     * @param string $description
     */
    public function setDescription(string $description): void
    {
        $this->description = $description;
    }

    // Generate getters/setters for all properties...
}
```

**Property Type Mapping:**

- `string` → `protected string $prop = '';`
- `text` → `protected string $prop = '';`
- `int` → `protected int $prop = 0;`
- `float` → `protected float $prop = 0.0;`
- `bool` → `protected bool $prop = false;`
- `datetime`/`date` → `protected ?\DateTime $prop = null;`

### 4. Generate Repository Class

**Path:** `Classes/Domain/Repository/<ModelName>Repository.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Domain\Repository;

use TYPO3\CMS\Extbase\Persistence\Repository;
use <VendorName>\<ExtensionKey>\Domain\Model\<ModelName>;

/**
 * <ModelName> Repository
 */
class <ModelName>Repository extends Repository
{
    /**
     * Find all active records
     *
     * @return array
     */
    public function findActive(): array
    {
        $query = $this->createQuery();

        return $query->matching(
            $query->equals('active', 1)
        )->execute()->toArray();
    }

    // Add custom query methods here...
}
```

**Note:** Only add `findActive()` if model has `active:bool` property.

### 5. Generate TCA Configuration

**Path:** `Configuration/TCA/<table_name>.php`

Table name format: `tx_<extensionkey>_domain_model_<modelname_lowercase>`

Example: `tx_myext_domain_model_product`

```php
<?php

defined('TYPO3') || die();

return [
    'ctrl' => [
        'title' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_db.xlf:<table_name>',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        'versioningWS' => true,
        'languageField' => 'sys_language_uid',
        'transOrigPointerField' => 'l10n_parent',
        'transOrigDiffSourceField' => 'l10n_diffsource',
        'translationSource' => 'l10n_source',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'searchFields' => 'title,description',
        'iconfile' => 'EXT:<extension_key>/Resources/Public/Icons/<ModelName>.svg'
    ],
    'types' => [
        '1' => [
            'showitem' => '
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
                    title, description,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:language,
                    --palette--;;language,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
                    --palette--;;hidden,
                    --palette--;;access,
            ',
        ],
    ],
    'palettes' => [
        'hidden' => [
            'showitem' => '
                hidden
            ',
        ],
        'language' => [
            'showitem' => '
                sys_language_uid, l10n_parent
            ',
        ],
        'access' => [
            'showitem' => '
                starttime, endtime
            ',
        ],
    ],
    'columns' => [
        'sys_language_uid' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.language',
            'config' => [
                'type' => 'language',
            ],
        ],
        'l10n_parent' => [
            'displayCond' => 'FIELD:sys_language_uid:>:0',
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.l18n_parent',
            'config' => [
                'type' => 'select',
                'renderType' => 'selectSingle',
                'items' => [
                    ['label' => '', 'value' => 0],
                ],
                'foreign_table' => '<table_name>',
                'foreign_table_where' => 'AND <table_name>.pid=###CURRENT_PID### AND <table_name>.sys_language_uid IN (-1,0)',
                'default' => 0,
            ],
        ],
        'l10n_source' => [
            'config' => [
                'type' => 'passthrough',
            ],
        ],
        'l10n_diffsource' => [
            'config' => [
                'type' => 'passthrough',
            ],
        ],
        'hidden' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.hidden',
            'config' => [
                'type' => 'check',
                'renderType' => 'checkboxToggle',
                'items' => [
                    [
                        'label' => '',
                        'invertStateDisplay' => true
                    ]
                ],
            ],
        ],
        'starttime' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.starttime',
            'config' => [
                'type' => 'datetime',
                'format' => 'datetime',
                'default' => 0,
            ],
        ],
        'endtime' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.endtime',
            'config' => [
                'type' => 'datetime',
                'format' => 'datetime',
                'default' => 0,
                'range' => [
                    'upper' => mktime(0, 0, 0, 1, 1, 2038),
                ],
            ],
        ],

        'title' => [
            'exclude' => false,
            'label' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_db.xlf:<table_name>.title',
            'config' => [
                'type' => 'input',
                'size' => 30,
                'max' => 255,
                'eval' => 'trim,required',
            ],
        ],
        'description' => [
            'exclude' => false,
            'label' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_db.xlf:<table_name>.description',
            'config' => [
                'type' => 'text',
                'cols' => 40,
                'rows' => 5,
                'eval' => 'trim',
            ],
        ],

        // Add additional property configurations based on input types...
    ],
];
```

**TCA Column Types by Property Type:**

- `string`:
  ```php
  'config' => [
      'type' => 'input',
      'size' => 30,
      'max' => 255,
      'eval' => 'trim',
  ]
  ```

- `text`:
  ```php
  'config' => [
      'type' => 'text',
      'cols' => 40,
      'rows' => 5,
      'eval' => 'trim',
  ]
  ```

- `int`:
  ```php
  'config' => [
      'type' => 'number',
      'size' => 10,
  ]
  ```

- `float`:
  ```php
  'config' => [
      'type' => 'number',
      'format' => 'decimal',
      'size' => 10,
  ]
  ```

- `bool`:
  ```php
  'config' => [
      'type' => 'check',
      'renderType' => 'checkboxToggle',
  ]
  ```

- `datetime`/`date`:
  ```php
  'config' => [
      'type' => 'datetime',
      'format' => 'datetime',  // or 'date'
  ]
  ```

### 6. Generate Database Schema

**Path:** `ext_tables.sql`

Append to existing file or create new:

```sql
CREATE TABLE tx_<extensionkey>_domain_model_<modelname> (
    uid int(11) NOT NULL auto_increment,
    pid int(11) DEFAULT '0' NOT NULL,

    title varchar(255) DEFAULT '' NOT NULL,
    description text,

    -- Add additional fields based on properties...

    tstamp int(11) unsigned DEFAULT '0' NOT NULL,
    crdate int(11) unsigned DEFAULT '0' NOT NULL,
    deleted tinyint(4) unsigned DEFAULT '0' NOT NULL,
    hidden tinyint(4) unsigned DEFAULT '0' NOT NULL,
    starttime int(11) unsigned DEFAULT '0' NOT NULL,
    endtime int(11) unsigned DEFAULT '0' NOT NULL,
    sorting int(11) DEFAULT '0' NOT NULL,

    sys_language_uid int(11) DEFAULT '0' NOT NULL,
    l10n_parent int(11) DEFAULT '0' NOT NULL,
    l10n_diffsource mediumblob,
    l10n_source int(11) DEFAULT '0' NOT NULL,

    PRIMARY KEY (uid),
    KEY parent (pid),
    KEY language (l10n_parent,sys_language_uid)
);
```

**SQL Field Types by Property Type:**

- `string` → `varchar(255) DEFAULT '' NOT NULL`
- `text` → `text`
- `int` → `int(11) DEFAULT '0' NOT NULL`
- `float` → `decimal(10,2) DEFAULT '0.00' NOT NULL`
- `bool` → `tinyint(1) DEFAULT '0' NOT NULL`
- `datetime`/`date` → `int(11) unsigned DEFAULT '0' NOT NULL`

### 7. Update locallang_db.xlf

Add labels for TCA fields in `Resources/Private/Language/locallang_db.xlf`:

```xml
<trans-unit id="<table_name>">
    <source><ModelName></source>
</trans-unit>
<trans-unit id="<table_name>.title">
    <source>Title</source>
</trans-unit>
<trans-unit id="<table_name>.description">
    <source>Description</source>
</trans-unit>
<!-- Add labels for all custom properties -->
```

### 8. Create Icon Placeholder

Create simple SVG icon at `Resources/Public/Icons/<ModelName>.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
    <rect width="16" height="16" fill="#007BFF"/>
    <circle cx="8" cy="8" r="5" fill="white"/>
</svg>
```

## Success Message

```
✓ Domain Model '<ModelName>' created successfully!

Files created:
- Classes/Domain/Model/<ModelName>.php
- Classes/Domain/Repository/<ModelName>Repository.php
- Configuration/TCA/tx_<extensionkey>_domain_model_<modelnamelowercase>.php
- ext_tables.sql (updated)
- Resources/Private/Language/locallang_db.xlf (updated)

Next steps:
1. Update database schema: typo3 extension:setup <extension_key>
2. Clear cache: typo3 cache:flush
3. Create controller: /typo3:controller <ModelName>Controller
4. Add custom methods to repository as needed

Table name: tx_<extensionkey>_domain_model_<modelnamelowercase>
```

## Important Notes

- Model class extends `AbstractEntity` (has uid, pid)
- All config files must have `defined('TYPO3') || die();`
- Use proper type declarations and `declare(strict_types=1);`
- TCA label field defaults to 'title' - change if needed
- searchFields in TCA includes title and description by default
- Standard TYPO3 fields added: hidden, deleted, starttime, endtime, sorting, language
- Repository includes `findActive()` only if `active` property exists
