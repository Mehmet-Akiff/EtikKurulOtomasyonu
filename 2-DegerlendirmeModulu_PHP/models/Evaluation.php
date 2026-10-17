<?php
// models/Evaluation.php

require_once __DIR__ . '/../config/database.php';

class Evaluation {
    public static function create(array $data): int {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("INSERT INTO evaluations (assignment_id, protocol_number, member_id, methodology_score, consent_form_score, risk_assessment_score, decision, feedback_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
        $stmt->execute([
            $data['assignment_id'],
            $data['protocol_number'],
            $data['member_id'],
            $data['methodology_score'],
            $data['consent_form_score'],
            $data['risk_assessment_score'],
            $data['decision'],
            $data['feedback_notes']
        ]);
        return (int)$pdo->lastInsertId();
    }

    public static function findByProtocol(string $protocolNumber): array {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("SELECT e.*, m.full_name as member_name, m.title as member_title 
                                FROM evaluations e 
                                JOIN committee_members m ON e.member_id = m.id 
                                WHERE e.protocol_number = ? 
                                ORDER BY e.evaluated_at ASC");
        $stmt->execute([$protocolNumber]);
        return $stmt->fetchAll();
    }
}
