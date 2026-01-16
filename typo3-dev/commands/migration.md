---
description: Creates Doctrine DBAL database migrations for TYPO3 extensions with proper up/down methods
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Create TYPO3 Database Migration

Generates Doctrine DBAL migrations for database schema changes.

## Usage

```
/typo3:migration <MigrationName> [type]
```

**Parameters:**
- `MigrationName`: Migration description (e.g., `AddProductTable`, `AddStatusFieldToOrder`)
- `type`: Migration type - `schema` (default), `data`, `combined`

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key
- Determine migration path

### 2. Generate Migration Class

**Path:** `Migrations/Mysql/Version<Timestamp><MigrationName>.php`

Example: `Migrations/Mysql/Version20240116120000AddProductTable.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Migrations\Mysql;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Migration: <MigrationName>
 *
 * <Description of what this migration does>
 */
final class Version<Timestamp><MigrationName> extends AbstractMigration
{
    public function getDescription(): string
    {
        return '<MigrationName> - <description>';
    }

    public function up(Schema $schema): void
    {
        // Add your schema changes here

        // Example: Create new table
        // $table = $schema->createTable('tx_<extensionkey>_domain_model_<modelname>');
        // $table->addColumn('uid', 'integer', ['autoincrement' => true, 'notnull' => true]);
        // $table->addColumn('pid', 'integer', ['default' => 0, 'notnull' => true]);
        // $table->addColumn('title', 'string', ['length' => 255, 'default' => '', 'notnull' => true]);
        // $table->addColumn('tstamp', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
        // $table->addColumn('crdate', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
        // $table->setPrimaryKey(['uid']);
        // $table->addIndex(['pid'], 'parent');

        // Example: Add column to existing table
        // $table = $schema->getTable('tx_<extensionkey>_domain_model_product');
        // $table->addColumn('status', 'smallint', ['default' => 0, 'notnull' => true]);

        // Example: Create index
        // $table->addIndex(['status'], 'status');

        // Example: Add foreign key
        // $table->addForeignKeyConstraint(
        //     'tx_<extensionkey>_domain_model_category',
        //     ['category'],
        //     ['uid'],
        //     ['onDelete' => 'CASCADE']
        // );
    }

    public function down(Schema $schema): void
    {
        // Reverse the changes made in up()

        // Example: Drop table
        // $schema->dropTable('tx_<extensionkey>_domain_model_<modelname>');

        // Example: Drop column
        // $table = $schema->getTable('tx_<extensionkey>_domain_model_product');
        // $table->dropColumn('status');
    }
}
```

### 3. Schema Migration Templates

**Create Table:**
```php
public function up(Schema $schema): void
{
    $table = $schema->createTable('tx_<extensionkey>_domain_model_product');

    // Standard TYPO3 fields
    $table->addColumn('uid', 'integer', ['autoincrement' => true, 'notnull' => true]);
    $table->addColumn('pid', 'integer', ['default' => 0, 'notnull' => true]);
    $table->addColumn('tstamp', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('crdate', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('deleted', 'smallint', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('hidden', 'smallint', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('starttime', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('endtime', 'integer', ['default' => 0, 'unsigned' => true, 'notnull' => true]);
    $table->addColumn('sorting', 'integer', ['default' => 0, 'notnull' => true]);

    // Language fields
    $table->addColumn('sys_language_uid', 'integer', ['default' => 0, 'notnull' => true]);
    $table->addColumn('l10n_parent', 'integer', ['default' => 0, 'notnull' => true]);
    $table->addColumn('l10n_diffsource', 'blob', ['notnull' => false]);

    // Custom fields
    $table->addColumn('title', 'string', ['length' => 255, 'default' => '', 'notnull' => true]);
    $table->addColumn('description', 'text', ['notnull' => false]);
    $table->addColumn('price', 'decimal', ['precision' => 10, 'scale' => 2, 'default' => '0.00']);
    $table->addColumn('stock', 'integer', ['default' => 0, 'notnull' => true]);
    $table->addColumn('active', 'smallint', ['default' => 0, 'notnull' => true]);

    // Keys
    $table->setPrimaryKey(['uid']);
    $table->addIndex(['pid'], 'parent');
    $table->addIndex(['l10n_parent', 'sys_language_uid'], 'language');
}
```

**Add Column:**
```php
public function up(Schema $schema): void
{
    $table = $schema->getTable('tx_<extensionkey>_domain_model_product');
    $table->addColumn('category', 'integer', ['default' => 0, 'notnull' => true]);
    $table->addIndex(['category'], 'category');
}

public function down(Schema $schema): void
{
    $table = $schema->getTable('tx_<extensionkey>_domain_model_product');
    $table->dropIndex('category');
    $table->dropColumn('category');
}
```

**Rename Column:**
```php
public function up(Schema $schema): void
{
    $this->addSql('ALTER TABLE tx_myext_product RENAME COLUMN old_name TO new_name');
}
```

**Modify Column:**
```php
public function up(Schema $schema): void
{
    $table = $schema->getTable('tx_<extensionkey>_domain_model_product');
    $table->changeColumn('price', ['precision' => 12, 'scale' => 4]);
}
```

### 4. Data Migration Template

**Path:** `Migrations/Mysql/Version<Timestamp>MigrateData.php`

```php
public function up(Schema $schema): void
{
    // Data migration using raw SQL
    $this->addSql("
        UPDATE tx_<extensionkey>_domain_model_product
        SET status = 1
        WHERE active = 1 AND deleted = 0
    ");

    // Or using platform-specific queries
    $this->addSql("
        INSERT INTO tx_<extensionkey>_domain_model_category (pid, title, tstamp, crdate)
        SELECT DISTINCT pid, category_name, UNIX_TIMESTAMP(), UNIX_TIMESTAMP()
        FROM tx_<extensionkey>_domain_model_product
        WHERE category_name != ''
    ");
}
```

### 5. Configure Migration

**Path:** `Configuration/Migrations.php` (if needed)

```php
<?php

return [
    'table_prefix' => '',
    'migrations_paths' => [
        '<VendorName>\\<ExtensionKey>\\Migrations\\Mysql' => 'EXT:<extension_key>/Migrations/Mysql',
    ],
];
```

### 6. Update ext_tables.sql

Also update `ext_tables.sql` to match the migration:

```sql
CREATE TABLE tx_<extensionkey>_domain_model_product (
    title varchar(255) DEFAULT '' NOT NULL,
    description text,
    price decimal(10,2) DEFAULT '0.00' NOT NULL,
    stock int(11) DEFAULT '0' NOT NULL,
    active tinyint(1) DEFAULT '0' NOT NULL,
    category int(11) DEFAULT '0' NOT NULL,

    KEY category (category)
);
```

Note: TYPO3 automatically adds standard fields (uid, pid, tstamp, etc.) based on TCA.

## Running Migrations

```bash
# Show migration status
vendor/bin/typo3 doctrine:migrationsstatus

# Execute pending migrations
vendor/bin/typo3 doctrine:migrationsexecute

# Execute specific migration
vendor/bin/typo3 doctrine:migrationsexecute --version=Version20240116120000AddProductTable

# Rollback last migration
vendor/bin/typo3 doctrine:migrationsexecute --down

# Alternative: Use extension:setup
typo3 extension:setup
```

## Column Type Reference

| PHP/DBAL Type | MySQL Type | TCA Type |
|---------------|------------|----------|
| `string` | `varchar(255)` | `input` |
| `text` | `text` | `text` |
| `integer` | `int(11)` | `number` |
| `smallint` | `smallint` | `check` |
| `bigint` | `bigint(20)` | `number` |
| `decimal` | `decimal(p,s)` | `number` |
| `float` | `double` | `number` |
| `boolean` | `tinyint(1)` | `check` |
| `datetime` | `datetime` | `datetime` |
| `date` | `date` | `datetime` |
| `time` | `time` | `datetime` |
| `blob` | `blob` | - |

## Success Message

```
✓ Migration 'Version<Timestamp><MigrationName>' created!

File created:
- Migrations/Mysql/Version<Timestamp><MigrationName>.php

Run migration:
  typo3 extension:setup

Or manually:
  vendor/bin/typo3 doctrine:migrationsexecute

Next steps:
1. Review and adjust the migration code
2. Test migration on development database
3. Update ext_tables.sql to match
4. Commit migration file
```
