// src/services/decisionService.js - Karar, Revizyon ve Denetim İzi İş Mantığı

const Decision = require('../models/Decision');
const RevisionRequest = require('../models/RevisionRequest');
const AuditLog = require('../models/AuditLog');
const CertificateGenerator = require('./certificateGenerator');
const { isFallbackActive, getMemoryStore } = require('../config/db');

class DecisionService {

  static async finalizeDecision(payload) {
    const {
      protocolNumber,
      projectTitle,
      researcherName,
      researcherEmail,
      fieldOfStudy,
      finalDecision,
      summaryRationale,
      conditions = [],
      averageScore = 0,
      memberVotes = []
    } = payload;

    if (!protocolNumber || !projectTitle || !finalDecision) {
      throw new Error('Eksik bilgi: protocolNumber, projectTitle ve finalDecision zorunludur.');
    }

    const year = new Date().getFullYear();
    const decisionNumber = payload.decisionNumber || `KARAR-${year}-${Math.floor(1000 + Math.random() * 9000)}`;
    const verificationCode = CertificateGenerator.generateVerificationCode(protocolNumber, decisionNumber);

    const certificateData = {
      protocolNumber,
      decisionNumber,
      projectTitle,
      researcherName: researcherName || 'Sorumlu Araştırmacı',
      researcherEmail,
      fieldOfStudy,
      finalDecision,
      summaryRationale: summaryRationale || (finalDecision === 'Approved' ? 'Araştırma önerisi etik kurul yönergelerine uygun bulunmuştur.' : 'Araştırma önerisi etik kurul yönergelerine uygun bulunmamıştır.'),
      conditions,
      averageScore,
      decidedAt: new Date(),
      memberVotes,
      verificationCode
    };

    const certificateHtml = await CertificateGenerator.generateCertificateHtml(certificateData);

    const decisionRecord = {
      ...certificateData,
      certificateHtml
    };

    if (isFallbackActive()) {
      const store = getMemoryStore();
      store.decisions.set(protocolNumber, decisionRecord);
      store.auditLogs.push({
        protocolNumber,
        action: 'DECISION_FINALIZED',
        details: { finalDecision, decisionNumber, verificationCode },
        timestamp: new Date()
      });
    } else {
      await Decision.findOneAndUpdate(
        { protocolNumber },
        decisionRecord,
        { upsert: true, new: true }
      );

      await AuditLog.create({
        protocolNumber,
        action: 'DECISION_FINALIZED',
        details: { finalDecision, decisionNumber, verificationCode }
      });
    }

    return decisionRecord;
  }

  static async requestRevision(payload) {
    const {
      protocolNumber,
      feedbackSummary,
      requiredCorrections = [],
      deadlineDays = 14
    } = payload;

    if (!protocolNumber || !feedbackSummary) {
      throw new Error('protocolNumber ve feedbackSummary zorunludur.');
    }

    const deadline = new Date();
    deadline.setDate(deadline.getDate() + deadlineDays);

    const revisionData = {
      protocolNumber,
      feedbackSummary,
      requiredCorrections,
      deadline,
      status: 'PendingResearcher',
      createdAt: new Date()
    };

    if (isFallbackActive()) {
      const store = getMemoryStore();
      const list = store.revisions.get(protocolNumber) || [];
      list.push(revisionData);
      store.revisions.set(protocolNumber, list);
      store.auditLogs.push({
        protocolNumber,
        action: 'REVISION_REQUESTED',
        details: { deadline, feedbackSummary },
        timestamp: new Date()
      });
    } else {
      await RevisionRequest.create(revisionData);
      await AuditLog.create({
        protocolNumber,
        action: 'REVISION_REQUESTED',
        details: { deadline, feedbackSummary }
      });
    }

    return revisionData;
  }

  static async getDecision(protocolNumber) {
    if (isFallbackActive()) {
      const store = getMemoryStore();
      return store.decisions.get(protocolNumber) || null;
    }
    return await Decision.findOne({ protocolNumber });
  }

  static async verifyCertificate(verificationCode) {
    if (isFallbackActive()) {
      const store = getMemoryStore();
      for (const dec of store.decisions.values()) {
        if (dec.verificationCode === verificationCode) {
          return {
            valid: true,
            protocolNumber: dec.protocolNumber,
            decisionNumber: dec.decisionNumber,
            projectTitle: dec.projectTitle,
            researcherName: dec.researcherName,
            finalDecision: dec.finalDecision,
            decidedAt: dec.decidedAt
          };
        }
      }
      return { valid: false, message: 'Geçersiz doğrulama kodu.' };
    }

    const dec = await Decision.findOne({ verificationCode });
    if (!dec) {
      return { valid: false, message: 'Geçersiz doğrulama kodu.' };
    }

    return {
      valid: true,
      protocolNumber: dec.protocolNumber,
      decisionNumber: dec.decisionNumber,
      projectTitle: dec.projectTitle,
      researcherName: dec.researcherName,
      finalDecision: dec.finalDecision,
      decidedAt: dec.decidedAt
    };
  }

  static async getAuditLogs(protocolNumber) {
    if (isFallbackActive()) {
      const store = getMemoryStore();
      return store.auditLogs.filter(l => l.protocolNumber === protocolNumber);
    }
    return await AuditLog.find({ protocolNumber }).sort({ timestamp: -1 });
  }
}

module.exports = DecisionService;
