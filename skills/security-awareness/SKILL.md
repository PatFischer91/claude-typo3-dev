---
name: security-awareness
description: Identifies security vulnerabilities in TYPO3 code including XSS, SQL injection, and insecure data handling. Use when handling user input, database queries, or rendering output.
---

# Security Awareness Skill

Security is critical in TYPO3 development. This skill helps identify and prevent common vulnerabilities.

## OWASP Top 10 for TYPO3

### 1. SQL Injection

#### ❌ Vulnerable Code

```php
// NEVER do this!
$productId = $_GET['id'];
$query = "SELECT * FROM tx_myext_product WHERE uid = " . $productId;
$result = $GLOBALS['TYPO3_DB']->sql_query($query);
```

#### ✅ Secure Code

```php
use TYPO3\CMS\Core\Database\ConnectionPool;

public function __construct(
    private readonly ConnectionPool $connectionPool
) {}

public function findById(int $productId): array
{
    $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_product');

    return $queryBuilder
        ->select('*')
        ->from('tx_myext_product')
        ->where(
            $queryBuilder->expr()->eq(
                'uid',
                $queryBuilder->createNamedParameter($productId, \PDO::PARAM_INT)
            )
        )
        ->executeQuery()
        ->fetchAssociative();
}
```

**Key Points:**
- Use QueryBuilder with named parameters
- Never concatenate user input into queries
- Use proper PDO parameter types (`\PDO::PARAM_INT`, `\PDO::PARAM_STR`)

### 2. Cross-Site Scripting (XSS)

#### ❌ Vulnerable Code

**Controller:**
```php
$this->view->assign('userInput', $_GET['search']);
```

**Template:**
```html
<h1>Search Results for: <f:format.raw>{userInput}</f:format.raw></h1>
```

#### ✅ Secure Code

**Controller:**
```php
use Psr\Http\Message\ServerRequestInterface;

public function searchAction(ServerRequestInterface $request): ResponseInterface
{
    $searchTerm = $request->getQueryParams()['search'] ?? '';
    $this->view->assign('searchTerm', $searchTerm);
    return $this->htmlResponse();
}
```

**Template:**
```html
<!-- Fluid escapes by default -->
<h1>Search Results for: {searchTerm}</h1>

<!-- Or explicitly -->
<h1>Search Results for: <f:format.htmlspecialchars>{searchTerm}</f:format.htmlspecialchars></h1>
```

**Key Points:**
- Fluid escapes output by default
- Never use `f:format.raw()` on user input
- Use Request object, not `$_GET`/`$_POST` directly

### 3. Insecure Direct Object References

#### ❌ Vulnerable Code

```php
public function deleteAction(): ResponseInterface
{
    $productId = $_GET['id'];
    $this->productRepository->remove($productId);  // No permission check!
}
```

#### ✅ Secure Code

```php
public function deleteAction(int $product): ResponseInterface
{
    // Check ownership/permissions
    if (!$this->accessControl->canDelete($this->getCurrentUser(), $product)) {
        throw new AccessDeniedException('You cannot delete this product');
    }

    $this->productRepository->remove($product);
    $this->redirect('list');
}
```

### 4. Cross-Site Request Forgery (CSRF)

#### ✅ Automatic Protection

Extbase forms have built-in CSRF protection via `__hmac` parameter:

```html
<f:form action="update" object="{product}" name="product">
    <!-- __hmac is automatically added -->
    <f:form.textfield property="title" />
    <f:form.submit value="Save" />
</f:form>
```

#### Backend Modules

Use `FormProtectionFactory` for backend forms:

```php
use TYPO3\CMS\Core\FormProtection\FormProtectionFactory;

$formProtection = FormProtectionFactory::get();
$token = $formProtection->generateToken('myForm');

// In template
$this->view->assign('csrfToken', $token);

// Verify on submit
if (!$formProtection->validateToken($submittedToken, 'myForm')) {
    throw new \Exception('CSRF token invalid');
}
```

### 5. Sensitive Data Exposure

#### ❌ Logging Sensitive Data

```php
// DON'T log passwords, tokens, credit cards
$this->logger->info('User login', [
    'username' => $username,
    'password' => $password  // NEVER!
]);
```

#### ✅ Secure Logging

```php
$this->logger->info('User login attempt', [
    'username' => $username,
    'ip' => $request->getServerParams()['REMOTE_ADDR']
]);
```

#### Configuration

Store sensitive config in environment variables:

```php
// DON'T commit to git
$apiKey = 'sk_live_abc123';  // Wrong!

// DO use environment variables
$apiKey = getenv('API_KEY');

// OR better: use DI
public function __construct(
    #[Autowire(env: 'API_KEY')]
    private readonly string $apiKey
) {}
```

### 6. File Upload Vulnerabilities

#### ❌ Unsafe File Upload

```php
$uploadedFile = $_FILES['file'];
$destination = 'uploads/' . $uploadedFile['name'];
move_uploaded_file($uploadedFile['tmp_name'], $destination);  // Dangerous!
```

#### ✅ Secure File Upload

```php
use TYPO3\CMS\Core\Resource\ResourceFactory;
use TYPO3\CMS\Core\Resource\StorageRepository;
use TYPO3\CMS\Core\Utility\GeneralUtility;

public function __construct(
    private readonly ResourceFactory $resourceFactory
) {}

public function uploadAction(ServerRequestInterface $request): ResponseInterface
{
    $uploadedFiles = $request->getUploadedFiles();
    $file = $uploadedFiles['file'] ?? null;

    if (!$file || $file->getError() !== UPLOAD_ERR_OK) {
        throw new \Exception('File upload failed');
    }

    // Validate file type
    $allowedExtensions = ['jpg', 'png', 'pdf'];
    $extension = pathinfo($file->getClientFilename(), PATHINFO_EXTENSION);

    if (!in_array(strtolower($extension), $allowedExtensions)) {
        throw new \Exception('File type not allowed');
    }

    // Validate file size (5MB max)
    if ($file->getSize() > 5 * 1024 * 1024) {
        throw new \Exception('File too large');
    }

    // Use FAL (File Abstraction Layer)
    $storage = $this->resourceFactory->getDefaultStorage();
    $folder = $storage->getFolder('user_uploads/');

    $uploadedFile = $storage->addUploadedFile(
        [
            'tmp_name' => $file->getStream()->getMetadata('uri'),
            'name' => $file->getClientFilename(),
            'size' => $file->getSize(),
        ],
        $folder,
        null,
        \TYPO3\CMS\Core\Resource\DuplicationBehavior::RENAME
    );

    return $this->jsonResponse(json_encode(['success' => true]));
}
```

## Input Validation

### Never Trust User Input

#### ❌ Dangerous

```php
$email = $_POST['email'];
$this->sendMail($email);  // No validation!
```

#### ✅ Validated

```php
use TYPO3\CMS\Core\Utility\GeneralUtility;

public function subscribeAction(ServerRequestInterface $request): ResponseInterface
{
    $data = $request->getParsedBody();
    $email = $data['email'] ?? '';

    // Validate email
    if (!GeneralUtility::validEmail($email)) {
        $this->addFlashMessage('Invalid email address', '', \TYPO3\CMS\Core\Messaging\AbstractMessage::ERROR);
        return $this->redirect('form');
    }

    // Sanitize
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);

    $this->newsletterService->subscribe($email);

    return $this->redirect('success');
}
```

### Extbase Validation

```php
use TYPO3\CMS\Extbase\Annotation as Extbase;

class NewsletterController extends ActionController
{
    /**
     * @Extbase\Validate("NotEmpty", param="email")
     * @Extbase\Validate("EmailAddress", param="email")
     */
    public function subscribeAction(string $email): ResponseInterface
    {
        // Email is already validated by Extbase
        $this->newsletterService->subscribe($email);
        return $this->redirect('success');
    }
}
```

## Output Encoding

### HTML Context

```html
<!-- Automatic escaping (default) -->
<p>{product.description}</p>

<!-- Explicit escaping -->
<p><f:format.htmlspecialchars>{product.description}</f:format.htmlspecialchars></p>
```

### JavaScript Context

```html
<script>
var productName = '<f:format.jsString>{product.name}</f:format.jsString>';
</script>
```

### URL Context

```html
<a href="<f:uri.action arguments="{search: searchTerm}" />">Search</a>
<!-- Fluid automatically encodes URL parameters -->
```

### JSON Context

```php
// Always use json_encode
$data = json_encode($product, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_QUOT);
return $this->jsonResponse($data);
```

## Authentication & Authorization

### Frontend User Authentication

```php
use TYPO3\CMS\Core\Context\Context;

public function __construct(
    private readonly Context $context
) {}

public function restrictedAction(): ResponseInterface
{
    $userAspect = $this->context->getAspect('frontend.user');

    if (!$userAspect->isLoggedIn()) {
        return $this->redirect('login');
    }

    $userId = $userAspect->get('id');
    $userGroups = $userAspect->get('groupIds');

    // Check permissions...
}
```

### Backend User Authentication

```php
use TYPO3\CMS\Core\Authentication\BackendUserAuthentication;

protected function getBackendUser(): ?BackendUserAuthentication
{
    return $GLOBALS['BE_USER'] ?? null;
}

public function adminAction(): ResponseInterface
{
    $backendUser = $this->getBackendUser();

    if (!$backendUser || !$backendUser->isAdmin()) {
        throw new AccessDeniedException('Admin access required');
    }

    // Admin functionality...
}
```

## Secure Communication

### HTTPS Enforcement

```php
use TYPO3\CMS\Core\Utility\GeneralUtility;

// Check if HTTPS
if (!GeneralUtility::getIndpEnv('TYPO3_SSL')) {
    // Redirect to HTTPS
    $httpsUrl = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    header('Location: ' . $httpsUrl);
    exit;
}
```

### API Calls with RequestFactory

```php
use TYPO3\CMS\Core\Http\RequestFactory;

public function __construct(
    private readonly RequestFactory $requestFactory
) {}

public function fetchFromApi(): array
{
    try {
        $response = $this->requestFactory->request(
            'https://api.example.com/products',
            'GET',
            [
                'headers' => [
                    'Authorization' => 'Bearer ' . $this->apiToken,
                    'Accept' => 'application/json'
                ],
                'verify' => true,  // Verify SSL certificate
                'timeout' => 10
            ]
        );

        return json_decode($response->getBody()->getContents(), true);
    } catch (\Exception $e) {
        $this->logger->error('API request failed', ['exception' => $e]);
        return [];
    }
}
```

## Session Security

### Secure Session Configuration

**LocalConfiguration.php:**

```php
'FE' => [
    'sessionTimeout' => 3600,  // 1 hour
    'sessionDataLifetime' => 86400,  // 24 hours
    'lockHashKeyWords' => 'useragent',  // Session fixation protection
    'lockIP' => 4,  // Lock first 4 IP octets
],
'BE' => [
    'sessionTimeout' => 28800,  // 8 hours
    'lockIP' => 4,
],
```

### Regenerate Session on Login

```php
use TYPO3\CMS\Core\Session\SessionManager;

public function __construct(
    private readonly SessionManager $sessionManager
) {}

public function loginAction(string $username, string $password): ResponseInterface
{
    // Authenticate user...

    // Regenerate session ID to prevent session fixation
    $this->sessionManager->removeSession($oldSessionId);
    $newSession = $this->sessionManager->createSession($userId);

    // ...
}
```

## Security Checklist

Before deploying TYPO3 code:

- [ ] No direct `$_GET`, `$_POST`, `$_SESSION`, `$_COOKIE` access
- [ ] All database queries use QueryBuilder with named parameters
- [ ] User input is validated and sanitized
- [ ] Output is properly escaped (Fluid default or manual)
- [ ] File uploads are validated (type, size, content)
- [ ] Authentication checks before sensitive operations
- [ ] CSRF protection enabled for forms
- [ ] Sensitive data not logged or exposed
- [ ] HTTPS enforced for production
- [ ] API calls use RequestFactory with SSL verification
- [ ] Sessions configured securely
- [ ] No secrets in version control
- [ ] Error messages don't expose sensitive information

## Common Vulnerabilities

### ❌ Command Injection

```php
// NEVER!
$filename = $_GET['file'];
exec("cat " . $filename);  // Command injection!
```

### ❌ Path Traversal

```php
// Vulnerable
$file = $_GET['file'];
$content = file_get_contents('uploads/' . $file);  // Can access ../../etc/passwd
```

### ✅ Secure Path Handling

```php
use TYPO3\CMS\Core\Utility\GeneralUtility;

$file = basename($_GET['file']);  // Remove path components
$absolutePath = GeneralUtility::getFileAbsFileName('fileadmin/uploads/' . $file);

if (!$absolutePath || !file_exists($absolutePath)) {
    throw new \Exception('File not found');
}

$content = file_get_contents($absolutePath);
```

### ❌ Unserialize User Input

```php
// NEVER unserialize user input!
$data = unserialize($_POST['data']);  // Remote code execution risk!
```

### ✅ Use JSON

```php
$data = json_decode($_POST['data'], true);
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [TYPO3 Security Guidelines](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/)
- [TYPO3 Security Team](https://typo3.org/community/teams/security)
- [Secure Coding Practices](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/GuidelinesIntegrators/)
