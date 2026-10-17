<?php
// controllers/AssignmentController.php

require_once __DIR__ . '/../services/AutoAssignmentService.php';
require_once __DIR__ . '/../models/Assignment.php';
require_once __DIR__ . '/../models/CommitteeMember.php';

class AssignmentController {

    public function autoAssign(): void {
        $input = json_decode(file_get_contents('php://input'), true);
        if (!$input || empty($input['protocolNumber']) || empty($input['projectTitle'])) {
            http_response_code(400);
            echo json_encode(['error' => 'Geçersiz veri. protocolNumber ve projectTitle zorunludur.']);
            return;
        }

        $service = new AutoAssignmentService();
        try {
            $result = $service->autoAssign(
                $input['protocolNumber'],
                $input['projectTitle'],
                $input['fieldOfStudy'] ?? 'Genel',
                (int)($input['requiredReviewers'] ?? 2)
            );
            http_response_code(200);
            echo json_encode($result);
        } catch (Throwable $e) {
            http_response_code(500);
            echo json_encode(['error' => $e->getMessage()]);
        }
    }

    public function getMemberAssignments(int $memberId): void {
        $status = $_GET['status'] ?? null;
        $assignments = Assignment::findByMember($memberId, $status);
        echo json_encode([
            'member_id' => $memberId,
            'count' => count($assignments),
            'assignments' => $assignments
        ]);
    }

    public function getProtocolAssignments(string $protocolNumber): void {
        $assignments = Assignment::findByProtocol($protocolNumber);
        echo json_encode([
            'protocol_number' => $protocolNumber,
            'assignments' => $assignments
        ]);
    }

    public function getMembers(): void {
        $members = CommitteeMember::all();
        echo json_encode($members);
    }
}
