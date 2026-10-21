// scripts/capture_screenshots.js - Uygulama İçi Gerçek Ekran Görüntüsü Alma Betiği

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const EmbeddedStore = require('../src/engine/embeddedStore');
const EmbeddedWorkflow = require('../src/engine/embeddedWorkflow');

const outDir = path.join(__dirname, '..', '..', 'docs', 'screenshots');
const tempStoreDir = path.join(__dirname, 'temp_screenshot_store');

let mainWindow;
let store;
let workflow;

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function seedRichDemoData() {
  if (fs.existsSync(tempStoreDir)) {
    fs.rmSync(tempStoreDir, { recursive: true, force: true });
  }
  store = new EmbeddedStore(tempStoreDir);
  workflow = new EmbeddedWorkflow(store);

  // Mevcut varsayılan başvuru (ETIK-2026-00001) için atama ve değerlendirme
  const assign1 = workflow.autoAssign('ETIK-2026-00001', 2);
  await workflow.submitEvaluation({
    assignmentId: assign1.assignments[0].id,
    protocolNumber: 'ETIK-2026-00001',
    memberId: assign1.assignments[0].memberId,
    methodologyScore: 5,
    consentFormScore: 5,
    riskAssessmentScore: 5,
    decision: 'Approved',
    feedbackNotes: 'Biyosensör veri güvenliği ve hasta aydınlatılmış onam formları eksiksizdir.'
  });
  await workflow.submitEvaluation({
    assignmentId: assign1.assignments[1].id,
    protocolNumber: 'ETIK-2026-00001',
    memberId: assign1.assignments[1].memberId,
    methodologyScore: 5,
    consentFormScore: 4,
    riskAssessmentScore: 5,
    decision: 'Approved',
    feedbackNotes: 'Klinik araştırma protokolü etik ilkelere tam uyumludur.'
  });

  // Başvuru 2: AI Projesi (Onaylanmış)
  const app2 = workflow.createApplication({
    researcherId: 1,
    projectTitle: 'AI Tabanlı Klinik Karar Destek Sistemlerinin Etik Analizi',
    researchType: 'Akademik Araştırma',
    fieldOfStudy: 'Mühendislik / Yapay Zeka ve Bilişim',
    abstract: 'Derin öğrenme modellerinin klinik karar süreçlerinde şeffaflık ve algoritmik adalet ilkeleri açısından incelenmesi.',
    methodology: 'Retrospektif anonim veri analizi ve uzman hekim anket çalışması.',
    volunteerCount: 120,
    riskLevel: 'Düşük'
  });
  const assign2 = workflow.autoAssign(app2.protocolNumber, 2);
  await workflow.submitEvaluation({
    assignmentId: assign2.assignments[0].id,
    protocolNumber: app2.protocolNumber,
    memberId: assign2.assignments[0].memberId,
    methodologyScore: 5,
    consentFormScore: 5,
    riskAssessmentScore: 4,
    decision: 'Approved',
    feedbackNotes: 'Veri anonimleştirme protokolü KVKK ve GDPR standartlarına uygundur.'
  });

  // Başvuru 3: Psikoloji Tezi (Revizyon İstenmiş / İncelemede)
  const app3 = workflow.createApplication({
    researcherId: 2,
    projectTitle: 'Üniversite Öğrencilerinde Dijital Tükenmişlik ve Kaygı Düzeyi İlişkisi',
    researchType: 'Yüksek Lisans / Doktora Tezi',
    fieldOfStudy: 'Klinik Psikoloji',
    abstract: 'Üniversite öğrencilerinde ekran süresi ile akademik tükenmişlik arasındaki ilişkinin ölçeklerle incelenmesi.',
    methodology: 'Çevrimiçi ölçek uygulaması (N=350).',
    volunteerCount: 350,
    riskLevel: 'Düşük'
  });
  const assign3 = workflow.autoAssign(app3.protocolNumber, 2);
  await workflow.submitEvaluation({
    assignmentId: assign3.assignments[0].id,
    protocolNumber: app3.protocolNumber,
    memberId: assign3.assignments[0].memberId,
    methodologyScore: 4,
    consentFormScore: 3,
    riskAssessmentScore: 4,
    decision: 'RevisionNeeded',
    feedbackNotes: 'Bilgilendirilmiş onam formuna çalışmadan istediği an çekilebilme maddesi eklenmelidir.'
  });

  // Başvuru 4: Yeni Başvuru (Atama Bekleyen)
  workflow.createApplication({
    researcherId: 3,
    projectTitle: 'Kişisel Sağlık Verilerinin Bulut Ortamında İşlenmesinin Hukuki Boyutu',
    researchType: 'Kurumsal / TÜBİTAK Projesi',
    fieldOfStudy: 'Sosyal Bilimler / Hukuk',
    abstract: 'Sağlık bilişim sistemlerinde açık rıza ve istisna hallerinin karşılaştırmalı hukuk analizi.',
    methodology: 'Yargı kararları incelemesi ve yarı yapılandırılmış uzman görüşmeleri.',
    volunteerCount: 40,
    riskLevel: 'Düşük'
  });

  await workflow.reconcileState();
}

function setupIpcHandlers() {
  ipcMain.handle('reconcile-state', async () => await workflow.reconcileState());
  ipcMain.handle('get-researchers', () => workflow.getResearchers());
  ipcMain.handle('create-researcher', (e, data) => workflow.createResearcher(data));
  ipcMain.handle('get-applications', () => workflow.getApplications());
  ipcMain.handle('get-application', (e, protocol) => workflow.getApplication(protocol));
  ipcMain.handle('create-application', (e, data) => workflow.createApplication(data));
  ipcMain.handle('get-committee-members', () => workflow.getCommitteeMembers());
  ipcMain.handle('auto-assign', (e, { protocol, requiredReviewers }) => workflow.autoAssign(protocol, requiredReviewers));
  ipcMain.handle('get-assignments', (e, memberId) => workflow.getAssignments(memberId));
  ipcMain.handle('submit-evaluation', async (e, data) => await workflow.submitEvaluation(data));
  ipcMain.handle('get-evaluations', (e, protocol) => workflow.getEvaluations(protocol));
  ipcMain.handle('get-evaluation-summary', (e, protocol) => workflow.getEvaluationSummary(protocol));
  ipcMain.handle('finalize-decision', async (e, data) => await workflow.finalizeDecision(data));
  ipcMain.handle('get-decisions', () => workflow.getDecisions());
  ipcMain.handle('get-decision', (e, protocol) => workflow.getDecision(protocol));
  ipcMain.handle('verify-certificate', (e, code) => workflow.verifyCertificate(code));
  ipcMain.handle('request-revision', (e, data) => workflow.requestRevision(data));
  ipcMain.handle('open-certificate-window', async () => ({ success: true }));
}

async function captureWindow(win, filename) {
  await delay(700);
  const image = await win.webContents.capturePage();
  const filePath = path.join(outDir, filename);
  fs.writeFileSync(filePath, image.toPNG());
  console.log('Captured:', filePath);
}

app.whenReady().then(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  await seedRichDemoData();
  setupIpcHandlers();

  mainWindow = new BrowserWindow({
    width: 1360,
    height: 1080,
    show: true,
    paintWhenInitiallyHidden: true,
    webPreferences: {
      preload: path.join(__dirname, '..', 'src', 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      backgroundThrottling: false
    }
  });

  await mainWindow.loadFile(path.join(__dirname, '..', 'src', 'ui', 'index.html'));
  await delay(2000); // FontAwesome ikonlarının ve tabloların yüklenmesini bekle
  await mainWindow.webContents.setZoomFactor(0.92);

  // CSS animasyonlarını kapat ki sekme geçişleri anında %100 görünür olsun
  await mainWindow.webContents.executeJavaScript(`
    const style = document.createElement('style');
    style.innerHTML = '*, .content-tab, .content-tab.active { animation: none !important; transition: none !important; opacity: 1 !important; transform: none !important; }';
    document.head.appendChild(style);
  `);
  await delay(300);

  // 1. Genel Bakış (Dashboard)
  await mainWindow.webContents.executeJavaScript(`switchTab('tab-dashboard');`);
  await captureWindow(mainWindow, '01_dashboard.png');

  // 2. Yeni Başvuru Sekmesi
  await mainWindow.webContents.executeJavaScript(`
    switchTab('tab-application');
    document.getElementById('appResearcherSelect').selectedIndex = 1;
    document.getElementById('appProjectTitle').value = 'Nörodejeneratif Hastalıklarda Erken Tanı Biyobelirteçlerinin Etik İncelemesi';
    document.getElementById('appAbstract').value = 'Bu araştırmada erken evre Alzheimer hastalarından alınan kan örneklerinde yeni nesil biyobelirteçlerin tanısal doğruluğu ve hasta mahremiyeti incelenecektir.';
    document.getElementById('appMethodology').value = 'Prospektif gözlemsel kohort çalışması, bilgilendirilmiş gönüllü olur formu ve çift kör laboratuvar analizi.';
    document.getElementById('newResearcherBox').style.display = 'block';
  `);
  await captureWindow(mainWindow, '02_application.png');

  // 3. Otomatik Atama Sekmesi
  await mainWindow.webContents.executeJavaScript(`switchTab('tab-assignment');`);
  await captureWindow(mainWindow, '03_assignment.png');

  // 4. Üye Değerlendirme Sekmesi
  await mainWindow.webContents.executeJavaScript(`
    switchTab('tab-evaluation');
    document.getElementById('evalFeedbackNotes').value = 'Araştırma protokolü, veri güvenliği önlemleri ve gönüllü aydınlatılmış onam formu etik kurul yönergesine tam uyumludur.';
  `);
  await captureWindow(mainWindow, '04_evaluation.png');

  // 5. Karar & Belgeler Sekmesi
  await mainWindow.webContents.executeJavaScript(`switchTab('tab-decision');`);
  await captureWindow(mainWindow, '05_decision.png');

  // 6. Belge Doğrulama Sekmesi (Onaylı AI Projesinin Doğrulama Koduyla)
  const approvedDec = workflow.getDecision('ETIK-2026-00002') || workflow.getDecisions()[0];
  await mainWindow.webContents.executeJavaScript(`
    switchTab('tab-verify');
    selectVerifyCode('${approvedDec.verificationCode}');
  `);
  await captureWindow(mainWindow, '07_verification.png');

  // 7. Resmi Karar Belgesi (Onaylı Belge + Tam QR Kod Görünümü)
  const certWin = new BrowserWindow({
    width: 900,
    height: 1120,
    show: true,
    paintWhenInitiallyHidden: true,
    webPreferences: {
      backgroundThrottling: false
    }
  });
  await certWin.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(approvedDec.certificateHtml)}`);
  await delay(600);
  await certWin.webContents.setZoomFactor(0.86);
  await captureWindow(certWin, '06_certificate.png');

  certWin.destroy();
  mainWindow.destroy();

  if (fs.existsSync(tempStoreDir)) {
    fs.rmSync(tempStoreDir, { recursive: true, force: true });
  }

  app.quit();
});
