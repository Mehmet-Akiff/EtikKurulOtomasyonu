// src/routes/apiRoutes.js - Modül 3 API Yönlendirmeleri

const express = require('express');
const router = express.Router();
const DecisionController = require('../controllers/decisionController');
const RevisionController = require('../controllers/revisionController');

// Karar ve Belge Rotaları
router.post('/decisions/finalize', DecisionController.finalizeDecision);
router.get('/decisions/:protocolNumber', DecisionController.getDecision);
router.get('/decisions/:protocolNumber/certificate', DecisionController.getCertificate);

// Revizyon Rotaları
router.post('/revisions/request', RevisionController.requestRevision);

// Doğrulama ve Audit Rotaları
router.get('/verify/:code', DecisionController.verifyCertificate);
router.get('/audit/:protocolNumber', DecisionController.getAuditLogs);

// Sağlık kontrolü
router.get('/health', (req, res) => {
  res.json({
    module: 'Modül 3: Karar, Revizyon & Otomatik Karar Belgesi',
    technology: 'Node.js (Express) + MongoDB',
    status: 'Active',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
