// tests/decision.test.js - Modül 3 Karar ve Belge Üretimi Birim & Entegrasyon Testleri

const assert = require('assert');
const { connectDB } = require('../src/config/db');
const DecisionService = require('../src/services/decisionService');
const CertificateGenerator = require('../src/services/certificateGenerator');

async function runTests() {
  await connectDB();
  console.log('=== [Modül 3: Node.js + MongoDB Testleri Başlıyor] ===\n');
  let passed = 0;
  let failed = 0;

  // Test 1: Revizyon Talebi Oluşturma
  try {
    const protocol = 'ETIK-2026-00042';
    const rev = await DecisionService.requestRevision({
      protocolNumber: protocol,
      feedbackSummary: 'Bilgilendirilmiş onam formunda veri saklama süresi belirtilmelidir.',
      requiredCorrections: [
        { section: 'Onam Formu', issue: 'Veri saklama süresi belirsiz', actionRequired: 'Madde 4 güncellenmeli' }
      ],
      deadlineDays: 14
    });

    assert.strictEqual(rev.protocolNumber, protocol);
    assert.strictEqual(rev.status, 'PendingResearcher');
    assert.ok(rev.deadline instanceof Date);
    console.log('✅ Test 1 Başarılı: Revizyon talebi ve son teslim tarihi başarıyla oluşturuldu.');
    passed++;
  } catch (err) {
    console.error('❌ Test 1 Başarısız:', err.message);
    failed++;
  }

  // Test 2: Nihai Karar Kesinleştirme ve Otomatik Karar Belgesi (HTML + QR) Üretimi
  let createdVerificationCode = null;
  const protocol = 'ETIK-2026-00042';
  try {
    const decision = await DecisionService.finalizeDecision({
      protocolNumber: protocol,
      projectTitle: 'Klinik Öncesi Biyosensör Güvenilirlik Çalışması',
      researcherName: 'Dr. Deniz Kaya',
      researcherEmail: 'deniz.kaya@universite.edu.tr',
      fieldOfStudy: 'Tıp / Biyomedikal',
      finalDecision: 'Approved',
      summaryRationale: 'Araştırma protokolü ve bilgilendirilmiş onam belgeleri incelenmiş, etik ilkelere tam uyumlu bulunmuştur.',
      conditions: [
        'Araştırma yalnızca onaylı protokol kapsamında yürütülmelidir.',
        'Herhangi bir yan etki veya protokol değişikliğinde kurula bildirim zorunludur.'
      ],
      averageScore: 4.85,
      memberVotes: [
        { memberName: 'Prof. Dr. Selim Vural', memberTitle: 'Prof. Dr.', decision: 'Approved', votedAt: new Date() },
        { memberName: 'Dr. Öğr. Üyesi Burcu Polat', memberTitle: 'Dr. Öğr. Üyesi', decision: 'Approved', votedAt: new Date() }
      ]
    });

    assert.strictEqual(decision.protocolNumber, protocol);
    assert.strictEqual(decision.finalDecision, 'Approved');
    assert.ok(decision.decisionNumber.startsWith('KARAR-'));
    assert.ok(decision.verificationCode.length >= 16);
    assert.ok(decision.certificateHtml.includes('ETİK AÇIDAN UYGUN BULUNMUŞTUR (ONAY)'));
    assert.ok(decision.certificateHtml.includes('data:image/png;base64')); // QR kod gömülmüş olmalı

    createdVerificationCode = decision.verificationCode;
    console.log(`✅ Test 2 Başarılı: Nihai karar ve QR kodlu resmi karar belgesi üretildi (${decision.decisionNumber}, Kod: ${decision.verificationCode}).`);
    passed++;
  } catch (err) {
    console.error('❌ Test 2 Başarısız:', err.message);
    failed++;
  }

  // Test 3: Resmi Karar Belgesi Doğrulama (Verification)
  try {
    assert.ok(createdVerificationCode, 'Doğrulama kodu mevcut olmalı');
    const verifyResult = await DecisionService.verifyCertificate(createdVerificationCode);

    assert.strictEqual(verifyResult.valid, true);
    assert.strictEqual(verifyResult.protocolNumber, protocol);
    assert.strictEqual(verifyResult.finalDecision, 'Approved');
    console.log('✅ Test 3 Başarılı: Kriptografik doğrulama kodu ile belge teyit edildi.');
    passed++;
  } catch (err) {
    console.error('❌ Test 3 Başarısız:', err.message);
    failed++;
  }

  // Test 4: Denetim İzi (Audit Log) Kontrolü
  try {
    const logs = await DecisionService.getAuditLogs(protocol);
    assert.ok(logs.length >= 2, 'En az 2 denetim kaydı bulunmalı (REVISION_REQUESTED ve DECISION_FINALIZED)');
    const actions = logs.map(l => l.action);
    assert.ok(actions.includes('DECISION_FINALIZED'));
    console.log(`✅ Test 4 Başarılı: Denetim izi (Audit Log) kayıtları doğrulandı (${logs.length} işlem kaydı).`);
    passed++;
  } catch (err) {
    console.error('❌ Test 4 Başarısız:', err.message);
    failed++;
  }

  console.log('\n--------------------------------------------------');
  console.log(`Özet: ${passed} Başarılı, ${failed} Başarısız.`);
  if (failed > 0) {
    process.exit(1);
  }
}

runTests();
