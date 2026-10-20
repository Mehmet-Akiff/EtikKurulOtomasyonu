// src/main.js - Electron Ana İşlemcisi (Main Process)

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const EmbeddedStore = require('./engine/embeddedStore');
const EmbeddedWorkflow = require('./engine/embeddedWorkflow');

let mainWindow;
let store;
let workflow;

async function createWindow() {
  const userDataDir = app.getPath('userData');
  store = new EmbeddedStore(userDataDir);
  workflow = new EmbeddedWorkflow(store);

  // Mevcut veritabanındaki değerlendirilmiş dosyaların karar kayıtlarını senkronize et
  await workflow.reconcileState();

  mainWindow = new BrowserWindow({
    width: 1240,
    height: 840,
    minWidth: 1020,
    minHeight: 700,
    title: 'Etik Kurul Otomasyonu',
    icon: path.join(__dirname, '..', 'build', 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    autoHideMenuBar: true
  });

  mainWindow.loadFile(path.join(__dirname, 'ui', 'index.html'));
}

app.whenReady().then(async () => {
  setupIpcHandlers();
  await createWindow();

  app.on('activate', async () => {
    if (BrowserWindow.getAllWindows().length === 0) await createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

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

  ipcMain.handle('open-certificate-window', async (e, protocol) => {
    let dec = workflow.getDecision(protocol);
    if (!dec) {
      const appRecord = workflow.getApplication(protocol);
      if (appRecord) {
        dec = await workflow.finalizeDecision({ protocolNumber: protocol });
      }
    }
    if (!dec || !dec.certificateHtml) return { success: false, message: 'Karar belgesi bulunamadı.' };

    const certWin = new BrowserWindow({
      width: 920,
      height: 960,
      title: `Resmi Karar Belgesi - ${protocol}`,
      parent: mainWindow,
      modal: false,
      autoHideMenuBar: true
    });

    certWin.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(dec.certificateHtml)}`);
    return { success: true };
  });
}
