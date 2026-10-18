// tests/engine.test.js - Masaüstü Gömülü Motoru Birim ve İş Akışı Testleri

const assert = require('assert');
const path = require('path');
const fs = require('fs');
const EmbeddedStore = require('../src/engine/embeddedStore');
const EmbeddedWorkflow = require('../src/engine/embeddedWorkflow');

async function runTests() {
  console.log('=== [Masaüstü Uygulaması: Gömülü Motor Testleri Başlıyor] ===\n');
  let passed = 0;
  let failed = 0;

  const testDataDir = path.join(__dirname, 'temp_test_data');
  if (fs.existsSync(testDataDir)) {
    fs.rmSync(testDataDir, { recursive: true, force: true });
  }

  const store = new EmbeddedStore(testDataDir);
  const workflow = new EmbeddedWorkflow(store);

  // Test 1: Başvuru Oluşturma ve Protokol No Üretimi
  try {
    const app = workflow.createApplication({
      researcherId: 1,
      projectTitle: 'Klinik İlaç Deneyleri Etik İncelemesi',
      researchType: 'Tez',
      fieldOfStudy: 'Tıp / Biyomedikal',
      abstract: 'Test özeti',
      volunteerCount: 50,
      riskLevel: 'Orta'
    });

    assert.ok(app.protocolNumber.startsWith('ETIK-'));
    assert.strictEqual(app.status, 'Submitted');
    console.log(`✅ Test 1 Başarılı: Başvuru oluşturuldu (Protokol: ${app.protocolNumber}).`);
    passed++;

    // Test 2: Akıllı Otomatik Dosya Dağıtımı (Uzmanlık Eşleme)
    const assignResult = workflow.autoAssign(app.protocolNumber, 2);
    assert.strictEqual(assignResult.status, 'success');
    assert.strictEqual(assignResult.assignedCount, 2);
    assert.strictEqual(workflow.getApplication(app.protocolNumber).status, 'UnderReview');
    console.log(`✅ Test 2 Başarılı: Otomatik raportör ataması yapıldı (${assignResult.assignments.map(a => a.memberName).join(', ')}).`);
    passed++;

    // Test 3: Kurul Üyesi Değerlendirme ve Puanlama
    const firstAssign = assignResult.assignments[0];
    const evaluation = workflow.submitEvaluation({
      assignmentId: firstAssign.id,
      protocolNumber: app.protocolNumber,
      memberId: firstAssign.memberId,
      methodologyScore: 5,
      consentFormScore: 5,
      riskAssessmentScore: 4,
      decision: 'Approved',
      feedbackNotes: 'Araştırma metodolojisi ve hasta onam belgeleri eksiksizdir.'
    });

    assert.strictEqual(evaluation.decision, 'Approved');
    assert.strictEqual(evaluation.methodologyScore, 5);
    console.log('✅ Test 3 Başarılı: Kurul üyesi değerlendirmesi ve kriter puanları kaydedildi.');
    passed++;

    // Test 4: Nihai Karar ve Resmi Belge (HTML + QR) Üretimi
    const decision = await workflow.finalizeDecision({
      protocolNumber: app.protocolNumber,
      finalDecision: 'Approved',
      summaryRationale: 'Tüm kurul üyelerince olumlu değerlendirilmiştir.'
    });

    assert.strictEqual(decision.protocolNumber, app.protocolNumber);
    assert.strictEqual(decision.finalDecision, 'Approved');
    assert.ok(decision.verificationCode.length >= 16);
    assert.ok(decision.certificateHtml.includes('ETİK AÇIDAN UYGUN BULUNMUŞTUR (ONAY)'));
    assert.ok(decision.certificateHtml.includes('data:image/png;base64')); // QR kod
    console.log(`✅ Test 4 Başarılı: Karar kesinleştirildi ve resmi karar belgesi üretildi (Kod: ${decision.verificationCode}).`);
    passed++;

    // Test 5: Kriptografik Belge Doğrulama
    const verify = workflow.verifyCertificate(decision.verificationCode);
    assert.strictEqual(verify.valid, true);
    assert.strictEqual(verify.protocolNumber, app.protocolNumber);
    console.log('✅ Test 5 Başarılı: Kriptografik doğrulama kodu başarıyla sorgulandı.');
    passed++;

  } catch (err) {
    console.error('❌ Test Hatası:', err);
    failed++;
  } finally {
    if (fs.existsSync(testDataDir)) {
      fs.rmSync(testDataDir, { recursive: true, force: true });
    }
  }

  console.log('\n--------------------------------------------------');
  console.log(`Özet: ${passed} Başarılı, ${failed} Başarısız.`);
  if (failed > 0) process.exit(1);
}

runTests();
