<?php
// models/CommitteeMember.php

require_once __DIR__ . '/../config/database.php';

class CommitteeMember {
    public static function all(bool $activeOnly = true): array {
        $pdo = Database::getConnection();
        $sql = "SELECT * FROM committee_members";
        if ($activeOnly) {
            $sql .= " WHERE is_active = 1";
        }
        $sql .= " ORDER BY active_file_count ASC, id ASC";
        return $pdo->query($sql)->fetchAll();
    }

    public static function find(int $id): ?array {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("SELECT * FROM committee_members WHERE id = ?");
        $stmt->execute([$id]);
        $res = $stmt->fetch();
        return $res ?: null;
    }

    public static function create(array $data): int {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("INSERT INTO committee_members (full_name, title, field_of_expertise, email, phone, active_file_count, is_active) VALUES (?, ?, ?, ?, ?, 0, 1)");
        $stmt->execute([
            $data['full_name'],
            $data['title'],
            $data['field_of_expertise'],
            $data['email'],
            $data['phone'] ?? null
        ]);
        return (int)$pdo->lastInsertId();
    }

    public static function incrementFileCount(int $id, int $by = 1): void {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("UPDATE committee_members SET active_file_count = active_file_count + ? WHERE id = ?");
        $stmt->execute([$by, $id]);
    }

    public static function decrementFileCount(int $id, int $by = 1): void {
        $pdo = Database::getConnection();
        $stmt = $pdo->prepare("UPDATE committee_members SET active_file_count = CASE WHEN active_file_count >= ? THEN active_file_count - ? ELSE 0 END WHERE id = ?");
        $stmt->execute([$by, $by, $id]);
    }
}
