---
description: Creates a Symfony Console Command for TYPO3 CLI with proper attributes, options, arguments, and registration
allowed-tools: Read, Write, Edit, Glob
---

# Create TYPO3 Console Command

Generates a Symfony Console Command for CLI usage.

## Usage

```
/typo3:command <CommandName> [description]
```

**Parameters:**
- `CommandName`: Command name (e.g., `ImportProducts`, `CleanupExpired`)
- `description`: Optional command description

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Find extension key and vendor name
- Determine namespace

### 2. Generate Command Class

**Path:** `Classes/Command/<CommandName>Command.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Command;

use Psr\Log\LoggerInterface;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;

/**
 * <CommandName> Console Command
 *
 * Usage: typo3 <extension_key>:<commandname> [options] [arguments]
 */
#[AsCommand(
    name: '<extension_key>:<commandname>',
    description: '<Description of what this command does>',
    aliases: ['<alias>']
)]
final class <CommandName>Command extends Command
{
    public function __construct(
        private readonly LoggerInterface $logger,
        // Add your dependencies here
    ) {
        parent::__construct();
    }

    /**
     * Configure command arguments and options
     */
    protected function configure(): void
    {
        $this
            ->addArgument(
                'target',
                InputArgument::OPTIONAL,
                'Target to process',
                'default'
            )
            ->addOption(
                'limit',
                'l',
                InputOption::VALUE_OPTIONAL,
                'Maximum number of items to process',
                100
            )
            ->addOption(
                'dry-run',
                'd',
                InputOption::VALUE_NONE,
                'Execute in dry-run mode (no changes)'
            )
            ->addOption(
                'force',
                'f',
                InputOption::VALUE_NONE,
                'Force execution without confirmation'
            )
            ->setHelp(<<<'HELP'
The <info>%command.name%</info> command does something useful.

<info>php %command.full_name% [target] [--limit=100] [--dry-run]</info>

Examples:
  <info>typo3 <extension_key>:<commandname></info>
      Run with default settings

  <info>typo3 <extension_key>:<commandname> products --limit=50</info>
      Process products with limit of 50

  <info>typo3 <extension_key>:<commandname> --dry-run</info>
      Execute in dry-run mode

HELP
            );
    }

    /**
     * Initialize command (runs before execute)
     */
    protected function initialize(InputInterface $input, OutputInterface $output): void
    {
        // Initialization logic
    }

    /**
     * Interactive command setup
     */
    protected function interact(InputInterface $input, OutputInterface $output): void
    {
        $io = new SymfonyStyle($input, $output);

        // Ask for missing arguments interactively
        if (!$input->getArgument('target')) {
            $target = $io->ask('What target should be processed?', 'default');
            $input->setArgument('target', $target);
        }
    }

    /**
     * Execute the command
     */
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        // Get arguments and options
        $target = $input->getArgument('target');
        $limit = (int)$input->getOption('limit');
        $dryRun = (bool)$input->getOption('dry-run');
        $force = (bool)$input->getOption('force');

        // Display header
        $io->title('<CommandName> Command');

        if ($dryRun) {
            $io->warning('Running in DRY-RUN mode - no changes will be made');
        }

        // Confirmation (unless --force)
        if (!$force && !$dryRun) {
            if (!$io->confirm('Do you want to proceed?', false)) {
                $io->note('Operation cancelled');
                return Command::SUCCESS;
            }
        }

        // Progress bar for batch operations
        $io->progressStart($limit);

        try {
            // Your command logic here
            $processedCount = 0;

            for ($i = 0; $i < $limit; $i++) {
                // Process item
                // ...

                $io->progressAdvance();
                $processedCount++;

                // Simulate work
                // if (!$dryRun) { $this->processItem($item); }
            }

            $io->progressFinish();

            // Log and display results
            $this->logger->info('<CommandName> command completed', [
                'target' => $target,
                'processed' => $processedCount,
                'dryRun' => $dryRun,
            ]);

            $io->success(sprintf(
                'Successfully processed %d items%s',
                $processedCount,
                $dryRun ? ' (dry-run)' : ''
            ));

            return Command::SUCCESS;

        } catch (\Throwable $e) {
            $this->logger->error('<CommandName> command failed', [
                'exception' => $e->getMessage(),
            ]);

            $io->error('Command failed: ' . $e->getMessage());

            if ($output->isVerbose()) {
                $io->listing(explode("\n", $e->getTraceAsString()));
            }

            return Command::FAILURE;
        }
    }
}
```

### 3. Register Command in Services.yaml

Add to `Configuration/Services.yaml`:

```yaml
services:
  <VendorName>\<ExtensionKey>\Command\<CommandName>Command:
    tags:
      - name: console.command
```

### 4. Alternative: Configure.php Registration (TYPO3 v12+)

**Path:** `Configuration/Commands.php` (legacy, not needed with `#[AsCommand]`)

```php
<?php

return [
    '<extension_key>:<commandname>' => [
        'class' => \<VendorName>\<ExtensionKey>\Command\<CommandName>Command::class,
        'schedulable' => true,  // Can be used in scheduler
    ],
];
```

### 5. Run the Command

```bash
# Show help
typo3 <extension_key>:<commandname> --help

# Run with defaults
typo3 <extension_key>:<commandname>

# Run with options
typo3 <extension_key>:<commandname> products --limit=50 --dry-run

# Verbose output
typo3 <extension_key>:<commandname> -v

# Very verbose (debug)
typo3 <extension_key>:<commandname> -vvv
```

### 6. Common Patterns

**Table Output:**
```php
$io->table(
    ['ID', 'Title', 'Status'],
    [
        [1, 'Product A', 'Active'],
        [2, 'Product B', 'Inactive'],
    ]
);
```

**Sections:**
```php
$io->section('Processing Products');
$io->listing(['Item 1', 'Item 2', 'Item 3']);
```

**Notes and Warnings:**
```php
$io->note('This is a note');
$io->warning('This is a warning');
$io->caution('This is a caution');
$io->success('Operation completed');
$io->error('Something went wrong');
```

**Choices:**
```php
$choice = $io->choice('Select environment', ['dev', 'staging', 'prod'], 'dev');
```

## Success Message

```
✓ Console Command '<extension_key>:<commandname>' created!

Files created:
- Classes/Command/<CommandName>Command.php
- Configuration/Services.yaml (updated)

Run command:
  typo3 <extension_key>:<commandname> --help

Schedule via Scheduler:
  Use "Execute console command" task

Next steps:
1. Implement command logic
2. Add dependencies via constructor
3. Clear cache: typo3 cache:flush
4. Test: typo3 <extension_key>:<commandname> --dry-run
```
