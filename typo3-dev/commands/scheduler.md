---
description: Creates a TYPO3 Scheduler Task with proper registration, configurable fields, and execute method
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Create TYPO3 Scheduler Task

Generates a Scheduler Task with proper structure and registration.

## Usage

```
/typo3:scheduler <TaskName> [description]
```

**Parameters:**
- `TaskName`: Task name in StudlyCase (e.g., `ImportProducts`, `CleanupExpired`)
- `description`: Optional task description

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key and vendor name
- Determine namespace

### 2. Create Scheduler Task Class

**Path:** `Classes/Task/<TaskName>Task.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Task;

use Psr\Log\LoggerInterface;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\Scheduler\Task\AbstractTask;

/**
 * <TaskName> Scheduler Task
 *
 * <Description of what this task does>
 */
class <TaskName>Task extends AbstractTask
{
    /**
     * Configurable task fields
     */
    public int $itemLimit = 100;
    public string $targetFolder = 'fileadmin/imports/';
    public bool $sendNotification = false;

    /**
     * Execute the scheduler task
     *
     * @return bool Returns TRUE on successful execution, FALSE on error
     */
    public function execute(): bool
    {
        $logger = $this->getLogger();
        $logger->info('<TaskName> task started');

        try {
            // Get configured values
            $limit = $this->itemLimit;
            $folder = $this->targetFolder;

            // Your task logic here
            // Example:
            // $processedCount = $this->processItems($limit);

            $logger->info('<TaskName> task completed', [
                'limit' => $limit,
                // 'processed' => $processedCount,
            ]);

            // Send notification if enabled
            if ($this->sendNotification) {
                $this->sendNotificationEmail();
            }

            return true;

        } catch (\Throwable $e) {
            $logger->error('<TaskName> task failed', [
                'exception' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
            ]);

            return false;
        }
    }

    /**
     * Get additional information to display in scheduler module
     *
     * @return string Information to display
     */
    public function getAdditionalInformation(): string
    {
        return sprintf(
            'Limit: %d, Folder: %s, Notify: %s',
            $this->itemLimit,
            $this->targetFolder,
            $this->sendNotification ? 'Yes' : 'No'
        );
    }

    /**
     * Get PSR-3 logger instance
     */
    private function getLogger(): LoggerInterface
    {
        return GeneralUtility::makeInstance(\TYPO3\CMS\Core\Log\LogManager::class)
            ->getLogger(__CLASS__);
    }

    /**
     * Send notification email
     */
    private function sendNotificationEmail(): void
    {
        // Implement notification logic
    }
}
```

### 3. Create Additional Fields Provider

**Path:** `Classes/Task/<TaskName>AdditionalFieldProvider.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Task;

use TYPO3\CMS\Core\Localization\LanguageService;
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\Scheduler\AbstractAdditionalFieldProvider;
use TYPO3\CMS\Scheduler\Controller\SchedulerModuleController;
use TYPO3\CMS\Scheduler\Task\AbstractTask;
use TYPO3\CMS\Scheduler\Task\Enumeration\Action;

/**
 * Additional field provider for <TaskName> task
 */
class <TaskName>AdditionalFieldProvider extends AbstractAdditionalFieldProvider
{
    /**
     * Get additional fields for task configuration
     *
     * @param array $taskInfo Current task info
     * @param AbstractTask|null $task Task object (null when adding)
     * @param SchedulerModuleController $schedulerModule Reference to scheduler module
     * @param Action $currentAction Current action (add/edit)
     * @return array Array of additional fields
     */
    public function getAdditionalFields(
        array &$taskInfo,
        $task,
        SchedulerModuleController $schedulerModule,
        Action $currentAction
    ): array {
        $additionalFields = [];

        // Item Limit field
        $fieldId = 'task_itemLimit';
        $fieldValue = $task instanceof <TaskName>Task ? $task->itemLimit : 100;

        if ($currentAction === Action::ADD) {
            $fieldValue = $taskInfo[$fieldId] ?? 100;
        }

        $additionalFields[$fieldId] = [
            'code' => '<input type="number" class="form-control" name="tx_scheduler[' . $fieldId . ']" '
                . 'id="' . $fieldId . '" value="' . (int)$fieldValue . '" min="1" max="10000">',
            'label' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.itemLimit',
            'cshKey' => '_MOD_system_txschedulerM1',
            'cshLabel' => $fieldId,
        ];

        // Target Folder field
        $fieldId = 'task_targetFolder';
        $fieldValue = $task instanceof <TaskName>Task ? $task->targetFolder : 'fileadmin/imports/';

        if ($currentAction === Action::ADD) {
            $fieldValue = $taskInfo[$fieldId] ?? 'fileadmin/imports/';
        }

        $additionalFields[$fieldId] = [
            'code' => '<input type="text" class="form-control" name="tx_scheduler[' . $fieldId . ']" '
                . 'id="' . $fieldId . '" value="' . htmlspecialchars($fieldValue) . '">',
            'label' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.targetFolder',
            'cshKey' => '_MOD_system_txschedulerM1',
            'cshLabel' => $fieldId,
        ];

        // Send Notification checkbox
        $fieldId = 'task_sendNotification';
        $fieldValue = $task instanceof <TaskName>Task ? $task->sendNotification : false;

        if ($currentAction === Action::ADD) {
            $fieldValue = (bool)($taskInfo[$fieldId] ?? false);
        }

        $checked = $fieldValue ? ' checked="checked"' : '';
        $additionalFields[$fieldId] = [
            'code' => '<input type="checkbox" class="form-check-input" name="tx_scheduler[' . $fieldId . ']" '
                . 'id="' . $fieldId . '" value="1"' . $checked . '>',
            'label' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.sendNotification',
            'cshKey' => '_MOD_system_txschedulerM1',
            'cshLabel' => $fieldId,
        ];

        return $additionalFields;
    }

    /**
     * Validate additional fields
     *
     * @param array $submittedData Data submitted by user
     * @param SchedulerModuleController $schedulerModule Scheduler module
     * @return bool TRUE if validation passed
     */
    public function validateAdditionalFields(
        array &$submittedData,
        SchedulerModuleController $schedulerModule
    ): bool {
        $result = true;

        // Validate item limit
        $itemLimit = (int)($submittedData['task_itemLimit'] ?? 0);
        if ($itemLimit < 1 || $itemLimit > 10000) {
            $this->addMessage(
                $this->getLanguageService()->sL(
                    'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.error.invalidLimit'
                ),
                \TYPO3\CMS\Core\Messaging\FlashMessage::ERROR
            );
            $result = false;
        }

        // Validate target folder
        $targetFolder = $submittedData['task_targetFolder'] ?? '';
        if (empty($targetFolder)) {
            $this->addMessage(
                $this->getLanguageService()->sL(
                    'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.error.emptyFolder'
                ),
                \TYPO3\CMS\Core\Messaging\FlashMessage::ERROR
            );
            $result = false;
        }

        return $result;
    }

    /**
     * Save additional fields to task
     *
     * @param array $submittedData Data submitted by user
     * @param AbstractTask $task Task to save data to
     */
    public function saveAdditionalFields(array $submittedData, AbstractTask $task): void
    {
        if ($task instanceof <TaskName>Task) {
            $task->itemLimit = (int)($submittedData['task_itemLimit'] ?? 100);
            $task->targetFolder = (string)($submittedData['task_targetFolder'] ?? 'fileadmin/imports/');
            $task->sendNotification = (bool)($submittedData['task_sendNotification'] ?? false);
        }
    }

    /**
     * Get language service
     */
    protected function getLanguageService(): LanguageService
    {
        return $GLOBALS['LANG'];
    }
}
```

### 4. Register Task in ext_localconf.php

Add to `ext_localconf.php`:

```php
// Register Scheduler Task
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['scheduler']['tasks'][\<VendorName>\<ExtensionKey>\Task\<TaskName>Task::class] = [
    'extension' => '<extension_key>',
    'title' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.title',
    'description' => 'LLL:EXT:<extension_key>/Resources/Private/Language/locallang_be.xlf:task.<taskname>.description',
    'additionalFields' => \<VendorName>\<ExtensionKey>\Task\<TaskName>AdditionalFieldProvider::class,
];
```

### 5. Add Language Labels

**Path:** `Resources/Private/Language/locallang_be.xlf`

```xml
<trans-unit id="task.<taskname>.title">
    <source><TaskName> Task</source>
</trans-unit>
<trans-unit id="task.<taskname>.description">
    <source>Executes the <TaskName> task. <Description></source>
</trans-unit>
<trans-unit id="task.<taskname>.itemLimit">
    <source>Item limit</source>
</trans-unit>
<trans-unit id="task.<taskname>.targetFolder">
    <source>Target folder</source>
</trans-unit>
<trans-unit id="task.<taskname>.sendNotification">
    <source>Send notification email</source>
</trans-unit>
<trans-unit id="task.<taskname>.error.invalidLimit">
    <source>Item limit must be between 1 and 10000</source>
</trans-unit>
<trans-unit id="task.<taskname>.error.emptyFolder">
    <source>Target folder cannot be empty</source>
</trans-unit>
```

## Alternative: Command-based Task (TYPO3 v12+)

For TYPO3 v12+, consider using Symfony Commands instead:

**Path:** `Classes/Command/<TaskName>Command.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;

#[AsCommand(
    name: '<extension_key>:<taskname>',
    description: '<TaskName> command'
)]
final class <TaskName>Command extends Command
{
    protected function configure(): void
    {
        $this
            ->addOption('limit', 'l', InputOption::VALUE_OPTIONAL, 'Item limit', 100)
            ->addOption('folder', 'f', InputOption::VALUE_OPTIONAL, 'Target folder', 'fileadmin/imports/');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        $limit = (int)$input->getOption('limit');
        $folder = $input->getOption('folder');

        $io->title('<TaskName> Command');
        $io->writeln("Processing with limit: {$limit}");

        // Your logic here

        $io->success('Task completed successfully');

        return Command::SUCCESS;
    }
}
```

Then schedule via cron or Scheduler's "Execute console command" task.

## Success Message

```
✓ Scheduler Task '<TaskName>Task' created!

Files created:
- Classes/Task/<TaskName>Task.php
- Classes/Task/<TaskName>AdditionalFieldProvider.php
- ext_localconf.php (updated)
- Resources/Private/Language/locallang_be.xlf (updated)

Next steps:
1. Clear cache: typo3 cache:flush
2. Go to Scheduler module in TYPO3 backend
3. Add new task of type '<TaskName>'
4. Configure task settings
5. Set execution frequency

The task will appear in:
System > Scheduler > Add task > <TaskName>
```
