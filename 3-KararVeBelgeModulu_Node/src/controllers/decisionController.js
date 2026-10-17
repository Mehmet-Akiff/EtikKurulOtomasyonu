// src/controllers/decisionController.js - Karar ve Belge Controller'ı

const DecisionService = require('../services/decisionService');

class DecisionController {

  static async finalizeDecision(req, res) {
    try {
      const decision = await DecisionService.finalizeDecision(req.body);
      res.status(201).json({
        success: true,
        message: 'Kurul kararı başarıyla kesinleştirildi ve resmi karar belgesi otomatik oluşturuldu.',
        decisionNumber: decision.decisionNumber,
        protocolNumber: decision.protocolNumber,
        verificationCode: decision.verificationCode,
        certificateUrl: `/api/decisions/${encodeURIComponent(decision.protocolNumber)}/certificate`
      });
    } catch (err) {
      res.status(400).json({ success: false, error: err.message });
    }
  }

  static async getDecision(req, res) {
    try {
      const decision = await DecisionService.getDecision(req.params.protocolNumber);
      if (!decision) {
        return res.status(404).json({ success: false, error: 'Karar kaydı bulunamadı.' });
      }
      res.json(decision);
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  }

  static async getCertificate(req, res) {
    try {
      const decision = await DecisionService.getDecision(req.params.protocolNumber);
      if (!decision || !decision.certificateHtml) {
        return res.status(404).send('<h2>Karar belgesi bulunamadı.</h2>');
      }
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      res.send(decision.certificateHtml);
    } catch (err) {
      res.status(500).send(`<h2>Belge üretilirken hata: ${err.message}</h2>`);
    }
  }

  static async verifyCertificate(req, res) {
    try {
      const result = await DecisionService.verifyCertificate(req.params.code);
      if (!result.valid) {
        return res.status(404).json(result);
      }
      res.json(result);
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  }

  static async getAuditLogs(req, res) {
    try {
      const logs = await DecisionService.getAuditLogs(req.params.protocolNumber);
      res.json(logs);
    } catch (err) {
      res.status(500).json({ success: false, error: err.message });
    }
  }
}

module.exports = DecisionController;
