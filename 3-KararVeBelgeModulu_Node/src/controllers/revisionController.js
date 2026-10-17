// src/controllers/revisionController.js - Revizyon Talepleri Controller'ı

const DecisionService = require('../services/decisionService');

class RevisionController {

  static async requestRevision(req, res) {
    try {
      const revision = await DecisionService.requestRevision(req.body);
      res.status(201).json({
        success: true,
        message: 'Revizyon talebi araştırmacıya iletilmek üzere kaydedildi.',
        revision
      });
    } catch (err) {
      res.status(400).json({ success: false, error: err.message });
    }
  }
}

module.exports = RevisionController;
