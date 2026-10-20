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

  try {
    // Test 1: Başvuru Oluşturma ve Protokol No Üretimi
    const app = workflow.createApplication({
      researcherId: '1',
      projectTitle: 'Klinik İlaç Deneyleri Etik İncelemesi',
      researchType: 'Tez',
      fieldOfStudy: 'Tıp / Biyomedikal',
      abstract: 'Test özeti',
      volunteerCount: 50,
      riskLevel: 'Orta'
    });

    assert.ok(app.protocolNumber.startsWith('ETIK-'));
    assert.strictEqual(app.researcherId, 1);
    assert.strictEqual(app.status, 'Submitted');
    console.log(`✅ Test 1 Başarılı: Başvuru oluşturuldu (Protokol: ${app.protocolNumber}).`);
    passed++;

    // Test 2: Akıllı Otomatik Dosya Dağıtımı (Uzmanlık Eşleme + Türkçe İ/ı Desteği)
    const assignResult = workflow.autoAssign(app.protocolNumber, 2);
    assert.strictEqual(assignResult.status, 'success');
    assert.strictEqual(assignResult.assignedCount, 2);
    assert.strictEqual(workflow.getApplication(app.protocolNumber).status, 'UnderReview');
    console.log(`✅ Test 2 Başarılı: Otomatik raportör ataması yapıldı (${assignResult.assignments.map(a => a.memberName).join(', ')}).`);
    passed++;

    // Test 3: Tek Üye Değerlendirmesi Sonrası Otomatik Karar ve Belge Oluşumu (Karar Sekmesi Senkronizasyonu)
    const firstAssign = assignResult.assignments[0];
    const secondAssign = assignResult.assignments[1];
    const evaluation1 = await workflow.submitEvaluation({
      assignmentId: firstAssign.id,
      protocolNumber: app.protocolNumber,
      memberId: firstAssign.memberId,
      methodologyScore: 5,
      consentFormScore: 5,
      riskAssessmentScore: 4,
      decision: 'Approved',
      feedbackNotes: 'Araştırma metodolojisi ve hasta onam belgeleri eksiksizdir.'
    });

    assert.strictEqual(evaluation1.decision, 'Approved');
    assert.strictEqual(evaluation1.methodologyScore, 5);

    // 1. değerlendirme yapılır yapılmaz karar sekmesinde görünmeli!
    const autoDecisionAfterFirst = workflow.getDecision(app.protocolNumber);
    assert.ok(autoDecisionAfterFirst, 'İlk değerlendirme sonrası karar kaydı otomatik oluşmalı');
    assert.strictEqual(autoDecisionAfterFirst.finalDecision, 'Approved');
    assert.strictEqual(workflow.getApplication(app.protocolNumber).status, 'Approved');
    assert.ok(autoDecisionAfterFirst.summaryRationale.includes('uyumlu') || autoDecisionAfterFirst.summaryRationale.includes('eksiksizdir'));
    console.log(`✅ Test 3 Başarılı: İlk kurul üyesi onayı sonrası karar ve sertifika otomatik üretildi (${autoDecisionAfterFirst.decisionNumber}).`);
    passed++;

    // Test 4: İkinci Üye Değerlendirmesi Sonrası Mevcut Kararın Güncellenmesi (Karar No Korunarak)
    await workflow.submitEvaluation({
      assignmentId: secondAssign.id,
      protocolNumber: app.protocolNumber,
      memberId: secondAssign.memberId,
      methodologyScore: 5,
      consentFormScore: 5,
      riskAssessmentScore: 5,
      decision: 'Approved',
      feedbackNotes: 'Etik açıdan tamamen uygundur.'
    });

    const updatedDecision = workflow.getDecision(app.protocolNumber);
    assert.strictEqual(updatedDecision.decisionNumber, autoDecisionAfterFirst.decisionNumber, 'Karar numarası değişmemeli');
    assert.strictEqual(updatedDecision.memberVotes.length, 2, 'Her iki üyenin oyu kararda yer almalı');
    assert.ok(updatedDecision.certificateHtml.includes('ETİK AÇIDAN UYGUN BULUNMUŞTUR (ONAY)'));
    assert.ok(updatedDecision.certificateHtml.includes('data:image/png;base64'));
    console.log(`✅ Test 4 Başarılı: İkinci değerlendirme sonrası karar belgesi 2 imza ile güncellendi.`);
    passed++;

    // Test 5: Kriptografik Belge Doğrulama
    const verify = workflow.verifyCertificate(updatedDecision.verificationCode);
    assert.strictEqual(verify.valid, true);
    assert.strictEqual(verify.protocolNumber, app.protocolNumber);
    console.log('✅ Test 5 Başarılı: Kriptografik doğrulama kodu başarıyla sorgulandı.');
    passed++;

    // Test 6: Revizyon Süreci ve Sonrasında Onaylama Akışı
    const revApp = workflow.createApplication({
      researcherId: 2,
      projectTitle: 'Yapay Zeka Tabanlı Öğrenci Analizi',
      researchType: 'Akademik Araştırma',
      fieldOfStudy: 'Mühendislik / Yapay Zeka',
      abstract: 'Özet',
      volunteerCount: 100,
      riskLevel: 'Düşük'
    });
    const revAssign = workflow.autoAssign(revApp.protocolNumber, 1);
    await workflow.submitEvaluation({
      assignmentId: revAssign.assignments[0].id,
      protocolNumber: revApp.protocolNumber,
      memberId: revAssign.assignments[0].memberId,
      methodologyScore: 3,
      consentFormScore: 2,
      riskAssessmentScore: 4,
      decision: 'RevisionNeeded',
      feedbackNotes: 'KVKK aydınlatma metni eklenmelidir.'
    });

    assert.strictEqual(workflow.getApplication(revApp.protocolNumber).status, 'RevisionNeeded');
    assert.strictEqual(workflow.getDecision(revApp.protocolNumber).finalDecision, 'RevisionNeeded');

    // Revizyon sonrası kurul onayı
    const approvedAfterRev = await workflow.finalizeDecision({
      protocolNumber: revApp.protocolNumber,
      finalDecision: 'Approved',
      summaryRationale: 'KVKK aydınlatma metni eklendiğinden oybirliği ile onaylanmıştır.'
    });
    assert.strictEqual(approvedAfterRev.finalDecision, 'Approved');
    assert.strictEqual(workflow.getApplication(revApp.protocolNumber).status, 'Approved');
    console.log('✅ Test 6 Başarılı: Revizyon kararı ve revizyon sonrası onay geçişi doğrulandı.');
    passed++;

    // Test 7: Geçmiş Verileri Onarma (reconcileState) - Değerlendirilmiş Ama Kararı Eksik Dosyaların Kurtarılması
    const orphanApp = workflow.createApplication({
      researcherId: 1,
      projectTitle: 'AI',
      researchType: 'Akademik Araştırma',
      fieldOfStudy: 'Mühendislik / Yapay Zeka',
      volunteerCount: 15,
      riskLevel: 'Düşük'
    });
    const orphanAssign = workflow.autoAssign(orphanApp.protocolNumber, 2);
    // Eski hatalı durumu simüle et: 1 değerlendirme var ama decision yok ve status UnderReview kalmış
    store.data.evaluations.push({
      id: 999,
      assignmentId: orphanAssign.assignments[0].id,
      protocolNumber: orphanApp.protocolNumber,
      memberId: orphanAssign.assignments[0].memberId,
      memberName: orphanAssign.assignments[0].memberName,
      memberTitle: orphanAssign.assignments[0].memberTitle,
      methodologyScore: 5,
      consentFormScore: 5,
      riskAssessmentScore: 5,
      averageScore: 5,
      decision: 'Approved',
      feedbackNotes: 'Uygundur.',
      evaluatedAt: new Date().toISOString()
    });
    orphanAssign.assignments[0].status = 'Completed';
    store.save();

    await workflow.reconcileState();
    const recoveredDecision = workflow.getDecision(orphanApp.protocolNumber);
    assert.ok(recoveredDecision, 'reconcileState eksik kararı otomatik oluşturmalı');
    assert.strictEqual(recoveredDecision.finalDecision, 'Approved');
    assert.strictEqual(workflow.getApplication(orphanApp.protocolNumber).status, 'Approved');
    console.log('✅ Test 7 Başarılı: reconcileState ile geçmişte değerlendirilmiş başvuruların karar belgeleri otomatik kurtarıldı.');
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
