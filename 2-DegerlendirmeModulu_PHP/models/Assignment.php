<?php
// models/Assignment.php

require_once __DIR__ . '/../config/database.php';

class Assignment {
    public static function create(array $data): int {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("INSERT INTO file_assignments (protocol_number, project_title, field_of_study, member_id, assignment_status, due_date) VALUES (?, ?, ?, ?, 'Pending', ?)");
        $stmt->execute([
            $data['protocol_number'],
            $data['project_title'],
            $data['field_of_study'],
            $data['member_id'],
            $data['due_date'] ?? date('Y-m-d', strtotime('+15 days'))
        ]);
        return (int)$pdo->lastInsertId();
    }

    public static function findByProtocol(string $protocolNumber): array {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("SELECT a.*, m.full_name as member_name, m.title as member_title, m.email as member_email 
                                FROM file_assignments a 
                                JOIN committee_members m ON a.member_id = m.id 
                                WHERE a.protocol_number = ?");
        $stmt->execute([$protocolNumber]);
        return $stmt->fetchAll();
    }

    public static function findByMember(int $memberId, ?string $status = null): array {
        $pdo = Database::getConnection();
        $sql = "SELECT * FROM file_assignments WHERE member_id = ?";
        $params = [$memberId];
        if ($status !== null) {
            $sql .= " AND assignment_status = ?";
            $params[] = $status;
        }
        $sql .= " ORDER BY assigned_at DESC";
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll();
    }

    public static function updateStatus(int $assignmentId, string $status): void {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("UPDATE file_assignments SET assignment_status = ? WHERE id = ?");
        $stmt->execute([$status, $assignmentId]);
    }
}
