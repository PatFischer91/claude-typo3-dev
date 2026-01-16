---
name: doctrine-dbal
description: Guides proper Doctrine DBAL and QueryBuilder usage instead of deprecated database methods. Use when writing database queries or migrations.
---

# Doctrine DBAL Skill

TYPO3 uses Doctrine DBAL for database operations. Use QueryBuilder for all database queries.

## QueryBuilder Basics

### Getting a QueryBuilder

```php
use TYPO3\CMS\Core\Database\ConnectionPool;

public function __construct(
    private readonly ConnectionPool $connectionPool
) {}

public function findProducts(): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    // Build and execute query...
}
```

### Simple SELECT Query

```php
public function findAll(): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    return $queryBuilder
        ->select('*')
        ->from('tx_myext_domain_model_product')
        ->executeQuery()
        ->fetchAllAssociative();
}
```

### SELECT with WHERE Clause

```php
public function findByCategory(int $categoryId): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    return $queryBuilder
        ->select('uid', 'title', 'price', 'stock')
        ->from('tx_myext_domain_model_product')
        ->where(
            $queryBuilder->expr()->eq(
                'category',
                $queryBuilder->createNamedParameter($categoryId, \PDO::PARAM_INT)
            )
        )
        ->executeQuery()
        ->fetchAllAssociative();
}
```

**Key Points:**
- Use `createNamedParameter()` to prevent SQL injection
- Specify PDO type: `\PDO::PARAM_INT`, `\PDO::PARAM_STR`, `\PDO::PARAM_BOOL`
- Use `fetchAllAssociative()` for multiple rows
- Use `fetchAssociative()` for single row

## Expression Builder

### Comparison Operators

```php
$expr = $queryBuilder->expr();

// Equals
$expr->eq('uid', $queryBuilder->createNamedParameter(123, \PDO::PARAM_INT))

// Not equals
$expr->neq('status', $queryBuilder->createNamedParameter(0, \PDO::PARAM_INT))

// Greater than
$expr->gt('price', $queryBuilder->createNamedParameter(100, \PDO::PARAM_INT))

// Greater than or equal
$expr->gte('stock', $queryBuilder->createNamedParameter(1, \PDO::PARAM_INT))

// Less than
$expr->lt('price', $queryBuilder->createNamedParameter(1000, \PDO::PARAM_INT))

// Less than or equal
$expr->lte('discount', $queryBuilder->createNamedParameter(50, \PDO::PARAM_INT))

// LIKE
$expr->like(
    'title',
    $queryBuilder->createNamedParameter('%' . $searchTerm . '%', \PDO::PARAM_STR)
)

// IN
$expr->in(
    'category',
    $queryBuilder->createNamedParameter([1, 2, 3], Connection::PARAM_INT_ARRAY)
)

// NOT IN
$expr->notIn(
    'status',
    $queryBuilder->createNamedParameter([0, 9], Connection::PARAM_INT_ARRAY)
)

// IS NULL
$expr->isNull('deleted_at')

// IS NOT NULL
$expr->isNotNull('image')
```

### Logical Operators

```php
// AND (all conditions must be true)
$queryBuilder->where(
    $queryBuilder->expr()->andX(
        $queryBuilder->expr()->eq('active', 1),
        $queryBuilder->expr()->gt('stock', 0)
    )
);

// OR (at least one condition must be true)
$queryBuilder->where(
    $queryBuilder->expr()->orX(
        $queryBuilder->expr()->eq('featured', 1),
        $queryBuilder->expr()->eq('on_sale', 1)
    )
);

// Combined
$queryBuilder->where(
    $queryBuilder->expr()->andX(
        $queryBuilder->expr()->eq('active', 1),
        $queryBuilder->expr()->orX(
            $queryBuilder->expr()->eq('featured', 1),
            $queryBuilder->expr()->gt('discount', 0)
        )
    )
);
```

### Multiple WHERE Clauses

```php
$queryBuilder
    ->select('*')
    ->from('tx_myext_domain_model_product')
    ->where(
        $queryBuilder->expr()->eq('active', 1)
    )
    ->andWhere(
        $queryBuilder->expr()->gt('stock', 0)
    )
    ->andWhere(
        $queryBuilder->expr()->like(
            'title',
            $queryBuilder->createNamedParameter('%' . $search . '%')
        )
    );
```

## Ordering and Limiting

### ORDER BY

```php
$queryBuilder
    ->select('*')
    ->from('tx_myext_domain_model_product')
    ->orderBy('title', 'ASC')
    ->addOrderBy('price', 'DESC');
```

### LIMIT and OFFSET

```php
$queryBuilder
    ->select('*')
    ->from('tx_myext_domain_model_product')
    ->setMaxResults(10)  // LIMIT 10
    ->setFirstResult(20); // OFFSET 20 (page 3 with 10 items per page)
```

### Pagination Example

```php
public function findPaginated(int $page = 1, int $itemsPerPage = 20): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $offset = ($page - 1) * $itemsPerPage;

    return $queryBuilder
        ->select('*')
        ->from('tx_myext_domain_model_product')
        ->setMaxResults($itemsPerPage)
        ->setFirstResult($offset)
        ->orderBy('created_at', 'DESC')
        ->executeQuery()
        ->fetchAllAssociative();
}
```

## JOIN Operations

### INNER JOIN

```php
$queryBuilder
    ->select('p.*', 'c.title AS category_title')
    ->from('tx_myext_domain_model_product', 'p')
    ->join(
        'p',
        'tx_myext_domain_model_category',
        'c',
        $queryBuilder->expr()->eq('p.category', $queryBuilder->quoteIdentifier('c.uid'))
    )
    ->where(
        $queryBuilder->expr()->eq('p.active', 1)
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

### LEFT JOIN

```php
$queryBuilder
    ->select('p.*', 'i.file AS image_file')
    ->from('tx_myext_domain_model_product', 'p')
    ->leftJoin(
        'p',
        'sys_file_reference',
        'i',
        $queryBuilder->expr()->andX(
            $queryBuilder->expr()->eq('i.tablenames', $queryBuilder->createNamedParameter('tx_myext_domain_model_product')),
            $queryBuilder->expr()->eq('i.uid_foreign', $queryBuilder->quoteIdentifier('p.uid')),
            $queryBuilder->expr()->eq('i.fieldname', $queryBuilder->createNamedParameter('image'))
        )
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

## Aggregate Functions

### COUNT

```php
public function countProducts(): int
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    return (int)$queryBuilder
        ->count('uid')
        ->from('tx_myext_domain_model_product')
        ->executeQuery()
        ->fetchOne();
}
```

### SUM, AVG, MIN, MAX

```php
$queryBuilder
    ->addSelectLiteral(
        'SUM(' . $queryBuilder->quoteIdentifier('price') . ') AS total_price',
        'AVG(' . $queryBuilder->quoteIdentifier('price') . ') AS avg_price',
        'MIN(' . $queryBuilder->quoteIdentifier('price') . ') AS min_price',
        'MAX(' . $queryBuilder->quoteIdentifier('price') . ') AS max_price'
    )
    ->from('tx_myext_domain_model_product')
    ->executeQuery()
    ->fetchAssociative();
```

### GROUP BY and HAVING

```php
$queryBuilder
    ->select('category')
    ->addSelectLiteral('COUNT(*) AS product_count')
    ->from('tx_myext_domain_model_product')
    ->groupBy('category')
    ->having(
        $queryBuilder->expr()->gt('COUNT(*)', 5)
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

## INSERT Operations

### Single INSERT

```php
public function insert(array $data): int
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->insert('tx_myext_domain_model_product')
        ->values([
            'pid' => $data['pid'],
            'title' => $data['title'],
            'price' => $data['price'],
            'stock' => $data['stock'],
            'active' => 1,
            'tstamp' => time(),
            'crdate' => time(),
        ])
        ->executeStatement();

    // Get last inserted ID
    return (int)$queryBuilder->getConnection()->lastInsertId();
}
```

### Bulk INSERT

```php
public function bulkInsert(array $products): void
{
    $connection = $this->connectionPool
        ->getConnectionForTable('tx_myext_domain_model_product');

    foreach ($products as $product) {
        $connection->insert(
            'tx_myext_domain_model_product',
            [
                'pid' => $product['pid'],
                'title' => $product['title'],
                'price' => $product['price'],
            ],
            [
                \PDO::PARAM_INT,
                \PDO::PARAM_STR,
                \PDO::PARAM_INT,
            ]
        );
    }
}
```

## UPDATE Operations

### Simple UPDATE

```php
public function updateStock(int $productId, int $newStock): void
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->update('tx_myext_domain_model_product')
        ->set('stock', $newStock)
        ->set('tstamp', time())
        ->where(
            $queryBuilder->expr()->eq(
                'uid',
                $queryBuilder->createNamedParameter($productId, \PDO::PARAM_INT)
            )
        )
        ->executeStatement();
}
```

### Conditional UPDATE

```php
public function activateProducts(array $categoryIds): void
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->update('tx_myext_domain_model_product')
        ->set('active', 1)
        ->set('tstamp', time())
        ->where(
            $queryBuilder->expr()->in(
                'category',
                $queryBuilder->createNamedParameter($categoryIds, Connection::PARAM_INT_ARRAY)
            )
        )
        ->executeStatement();
}
```

## DELETE Operations

### Soft Delete (TYPO3 Standard)

```php
public function softDelete(int $productId): void
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->update('tx_myext_domain_model_product')
        ->set('deleted', 1)
        ->set('tstamp', time())
        ->where(
            $queryBuilder->expr()->eq(
                'uid',
                $queryBuilder->createNamedParameter($productId, \PDO::PARAM_INT)
            )
        )
        ->executeStatement();
}
```

### Hard DELETE

```php
public function hardDelete(int $productId): void
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->delete('tx_myext_domain_model_product')
        ->where(
            $queryBuilder->expr()->eq(
                'uid',
                $queryBuilder->createNamedParameter($productId, \PDO::PARAM_INT)
            )
        )
        ->executeStatement();
}
```

## TYPO3 Query Restrictions

TYPO3 automatically adds restrictions for deleted, hidden, starttime, endtime fields.

### Disable All Restrictions

```php
$queryBuilder = $this->connectionPool
    ->getQueryBuilderForTable('tx_myext_domain_model_product');

// Remove ALL restrictions (show deleted, hidden, etc.)
$queryBuilder->getRestrictions()->removeAll();

$result = $queryBuilder
    ->select('*')
    ->from('tx_myext_domain_model_product')
    ->executeQuery()
    ->fetchAllAssociative();
```

### Remove Specific Restrictions

```php
use TYPO3\CMS\Core\Database\Query\Restriction\DeletedRestriction;
use TYPO3\CMS\Core\Database\Query\Restriction\HiddenRestriction;

$queryBuilder = $this->connectionPool
    ->getQueryBuilderForTable('tx_myext_domain_model_product');

// Keep DeletedRestriction, remove others
$queryBuilder
    ->getRestrictions()
    ->removeAll()
    ->add(GeneralUtility::makeInstance(DeletedRestriction::class));

// Remove only HiddenRestriction
$queryBuilder
    ->getRestrictions()
    ->removeByType(HiddenRestriction::class);
```

## Transactions

```php
use TYPO3\CMS\Core\Database\Connection;

public function transferStock(int $fromProductId, int $toProductId, int $quantity): void
{
    $connection = $this->connectionPool
        ->getConnectionForTable('tx_myext_domain_model_product');

    $connection->beginTransaction();

    try {
        // Reduce stock from source product
        $connection->update(
            'tx_myext_domain_model_product',
            ['stock' => new \Doctrine\DBAL\Query\Expression\ExpressionBuilder($connection)
                ->subtract('stock', $quantity)
            ],
            ['uid' => $fromProductId]
        );

        // Increase stock for target product
        $connection->update(
            'tx_myext_domain_model_product',
            ['stock' => new \Doctrine\DBAL\Query\Expression\ExpressionBuilder($connection)
                ->add('stock', $quantity)
            ],
            ['uid' => $toProductId]
        );

        $connection->commit();
    } catch (\Exception $e) {
        $connection->rollBack();
        throw $e;
    }
}
```

## Doctrine DBAL Migrations

### Creating a Migration

```bash
vendor/bin/typo3 extension:migration:create MyExtension AddProductTable
```

### Migration Class

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Migrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

final class Version20240116000000 extends AbstractMigration
{
    public function up(Schema $schema): void
    {
        $table = $schema->createTable('tx_myext_domain_model_product');

        $table->addColumn('uid', 'integer', [
            'autoincrement' => true,
            'notnull' => true,
        ]);
        $table->addColumn('pid', 'integer', ['default' => 0, 'notnull' => true]);
        $table->addColumn('title', 'string', ['length' => 255, 'default' => '', 'notnull' => true]);
        $table->addColumn('price', 'decimal', ['precision' => 10, 'scale' => 2, 'default' => '0.00']);
        $table->addColumn('stock', 'integer', ['default' => 0]);

        $table->setPrimaryKey(['uid']);
        $table->addIndex(['pid'], 'parent');
    }

    public function down(Schema $schema): void
    {
        $schema->dropTable('tx_myext_domain_model_product');
    }
}
```

## Common Mistakes

### ❌ String Concatenation (SQL Injection!)

```php
// NEVER!
$queryBuilder
    ->where('uid = ' . $productId);  // SQL injection risk!
```

### ✅ Named Parameters

```php
$queryBuilder
    ->where(
        $queryBuilder->expr()->eq(
            'uid',
            $queryBuilder->createNamedParameter($productId, \PDO::PARAM_INT)
        )
    );
```

### ❌ Using Deprecated $GLOBALS['TYPO3_DB']

```php
// Removed in TYPO3 v10!
$result = $GLOBALS['TYPO3_DB']->exec_SELECTgetRows('*', 'tx_myext_product', 'uid = 1');
```

### ✅ Use QueryBuilder

```php
$queryBuilder->select('*')->from('tx_myext_product')->where(...)->executeQuery()->fetchAllAssociative();
```

## Best Practices

- ✅ **Always use QueryBuilder** for database operations
- ✅ **Named parameters** - prevent SQL injection
- ✅ **Specify PDO types** - `\PDO::PARAM_INT`, `\PDO::PARAM_STR`
- ✅ **Use restrictions** - respect TYPO3 deleted/hidden flags
- ✅ **Transactions** - for multi-step operations
- ✅ **Migrations** - for schema changes
- ❌ **No string concatenation** - SQL injection risk
- ❌ **No raw SQL** - use QueryBuilder
- ❌ **No $GLOBALS['TYPO3_DB']** - removed since v10

## References

- [Doctrine DBAL Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/)
- [QueryBuilder Reference](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/QueryBuilder/)
- [Doctrine Migrations](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/Migrations.html)
