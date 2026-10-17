<?php
// tests/AutoAssignmentTest.php - Modül 2 Otomatik Atama ve Değerlendirme Testleri

putenv('DB_DRIVER=sqlite'); // Testler için SQLite kullan

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../models/CommitteeMember.php';
require_once __DIR__ . '/../models/Assignment.php';
require_once __DIR__ . '/../models/Evaluation.php';
require_once __DIR__ . '/../services/AutoAssignmentService.php';

function runTests() {
    echo "=== [Modül 2: PHP + MySQL/SQLite Testleri Başlıyor] ===\n\n";
    $passed = 0;
    $failed = 0;

    // Test 1: Kurul Üyeleri Listelenmeli
    try {
        $members = CommitteeMember::all();
        assert(count($members) >= 6, "En az 6 örnek kurul üyesi bulunmalı");
        echo "✅ Test 1 Başarılı: Kurul üyeleri listelendi (" . count($members) . " üye mevcut).\n";
        $passed++;
    } catch (Throwable $e) {
        echo "❌ Test 1 Başarısız: " . $e->getMessage() . "\n";
        $failed++;
    }

    // Test 2: Otomatik Atama - Uzmanlık ve Yük Dengesi Testi
    try {
        $service = new AutoAssignmentService();
        $protocol = "ETIK-TEST-" . uniqid();
        $res = $service->autoAssign($protocol, "Klinik Onkoloji Biyobelirteç Araştırması", "Tıp / Biyomedikal", 2);

        assert($res['status'] === 'success', "Atama başarılı olmalı");
        assert($res['assigned_count'] === 2, "2 raportör atanmalı");
        
        $assignedNames = array_column($res['assignments'], 'member_name');
        echo "✅ Test 2 Başarılı: Otomatik atama tamamlandı. Atanan Raportörler: " . implode(', ', $assignedNames) . "\n";
        $passed++;
    } catch (Throwable $e) {
        echo "❌ Test 2 Başarısız: " . $e->getMessage() . "\n";
        $failed++;
    }

    // Test 3: Aynı Başvuruya Tekrar Atama Yapılmamalı (Idempotency)
    try {
        $service = new AutoAssignmentService();
        $dupRes = $service->autoAssign($protocol, "Klinik Onkoloji Biyobelirteç Araştırması", "Tıp / Biyomedikal", 2);
        assert($dupRes['status'] === 'already_assigned', "Yinelenen atama engellenmeli");
        echo "✅ Test 3 Başarılı: Yinelenen dosya atama koruması doğrulandı.\n";
        $passed++;
    } catch (Throwable $e) {
        echo "❌ Test 3 Başarısız: " . $e->getMessage() . "\n";
        $failed++;
    }

    // Test 4: Değerlendirme ve Puan Kaydı Testi
    try {
        $assignments = Assignment::findByProtocol($protocol);
        assert(count($assignments) > 0, "Atama bulunmalı");
        $firstAssign = $assignments[0];

        $evalId = Evaluation::create([
            'assignment_id' => $firstAssign['id'],
            'protocol_number' => $protocol,
            'member_id' => $firstAssign['member_id'],
            'methodology_score' => 5,
            'consent_form_score' => 4,
            'risk_assessment_score' => 5,
            'decision' => 'Approved',
            'feedback_notes' => 'Protokol ve hasta onam formu eksiksiz hazırlanmıştır. Araştırma etik açıdan uygundur.'
        ]);

        assert($evalId > 0, "Değerlendirme ID üretilmeli");
        $evals = Evaluation::findByProtocol($protocol);
        assert(count($evals) === 1, "1 değerlendirme kaydı olmalı");
        assert($evals[0]['decision'] === 'Approved', "Karar Approved olmalı");

        echo "✅ Test 4 Başarılı: Üye değerlendirme ve görüş kaydı başarıyla oluşturuldu.\n";
        $passed++;
    } catch (Throwable $e) {
        echo "❌ Test 4 Başarısız: " . $e->getMessage() . "\n";
        $failed++;
    }

    echo "\n--------------------------------------------------\n";
    echo "Özet: {$passed} Başarılı, {$failed} Başarısız.\n";
    if ($failed > 0) {
        exit(1);
    }
}

runTests();
