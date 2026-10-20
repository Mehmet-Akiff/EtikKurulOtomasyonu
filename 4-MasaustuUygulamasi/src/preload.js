// src/preload.js - Güvenli ContextBridge IPC Köprüsü

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  // State Sync
  reconcileState: () => ipcRenderer.invoke('reconcile-state'),

  // Researchers
  getResearchers: () => ipcRenderer.invoke('get-researchers'),
  createResearcher: (data) => ipcRenderer.invoke('create-researcher', data),

  // Applications
  getApplications: () => ipcRenderer.invoke('get-applications'),
  getApplication: (protocol) => ipcRenderer.invoke('get-application', protocol),
  createApplication: (data) => ipcRenderer.invoke('create-application', data),

  // Committee & Assignment
  getCommitteeMembers: () => ipcRenderer.invoke('get-committee-members'),
  autoAssign: (protocol, requiredReviewers) => ipcRenderer.invoke('auto-assign', { protocol, requiredReviewers }),
  getAssignments: (memberId) => ipcRenderer.invoke('get-assignments', memberId),

  // Evaluation
  submitEvaluation: (data) => ipcRenderer.invoke('submit-evaluation', data),
  getEvaluations: (protocol) => ipcRenderer.invoke('get-evaluations', protocol),
  getEvaluationSummary: (protocol) => ipcRenderer.invoke('get-evaluation-summary', protocol),

  // Decisions & Certificates
  finalizeDecision: (data) => ipcRenderer.invoke('finalize-decision', data),
  getDecisions: () => ipcRenderer.invoke('get-decisions'),
  getDecision: (protocol) => ipcRenderer.invoke('get-decision', protocol),
  verifyCertificate: (code) => ipcRenderer.invoke('verify-certificate', code),
  openCertificateWindow: (protocol) => ipcRenderer.invoke('open-certificate-window', protocol),

  // Revisions
  requestRevision: (data) => ipcRenderer.invoke('request-revision', data)
});
