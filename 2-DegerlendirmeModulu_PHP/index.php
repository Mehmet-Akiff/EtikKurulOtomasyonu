<?php
// index.php - Modül 2: Kurul Değerlendirme & Atama API & Portal Yönlendiricisi (PHP + MySQL)

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/controllers/AssignmentController.php';
require_once __DIR__ . '/controllers/EvaluationController.php';

$uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

// JSON yanıt başlığı (HTML portal haricinde)
if (str_starts_with($uri, '/api/')) {
    header("Content-Type: application/json; charset=UTF-8");
}

$assignmentController = new AssignmentController();
$evaluationController = new EvaluationController();

// Yönlendirme (Routing)
if ($uri === '/' || $uri === '/index.php') {
    // Kurul Üyesi Arayüzünü sun
    include __DIR__ . '/views/evaluation_form.html';
    exit;
}

if ($uri === '/api/members' && $method === 'GET') {
    $assignmentController->getMembers();
    exit;
}

if ($uri === '/api/assignments/auto-assign' && $method === 'POST') {
    $assignmentController->autoAssign();
    exit;
}

if (preg_match('#^/api/assignments/member/(\d+)$#', $uri, $matches) && $method === 'GET') {
    $assignmentController->getMemberAssignments((int)$matches[1]);
    exit;
}

if (preg_match('#^/api/assignments/protocol/(.+)$#', $uri, $matches) && $method === 'GET') {
    $assignmentController->getProtocolAssignments(urldecode($matches[1]));
    exit;
}

if ($uri === '/api/evaluations' && $method === 'POST') {
    $evaluationController->submitEvaluation();
    exit;
}

if (preg_match('#^/api/evaluations/summary/(.+)$#', $uri, $matches) && $method === 'GET') {
    $evaluationController->getSummary(urldecode($matches[1]));
    exit;
}

// Sağlık kontrolü
if ($uri === '/api/health') {
    echo json_encode([
        'module' => 'Modül 2: Kurul Değerlendirme & Otomatik Atama',
        'technology' => 'PHP + MySQL',
        'status' => 'Active',
        'timestamp' => date('c')
    ]);
    exit;
}

// Bulunamadı (404)
http_response_code(404);
echo json_encode(['error' => 'Endpoint bulunamadı.', 'uri' => $uri]);
