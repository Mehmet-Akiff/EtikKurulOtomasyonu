// src/models/AuditLog.js - Denetim İzi (Audit Log) Mongoose Şeması

const mongoose = require('mongoose');

const auditLogSchema = new mongoose.Schema({
  protocolNumber: {
    type: String,
    required: true,
    index: true
  },
  action: {
    type: String,
    required: true // 'APPLICATION_SUBMITTED', 'MEMBERS_ASSIGNED', 'EVALUATION_RECEIVED', 'REVISION_REQUESTED', 'DECISION_FINALIZED', 'CERTIFICATE_GENERATED'
  },
  actor: {
    type: String,
    default: 'System'
  },
  details: {
    type: mongoose.Schema.Types.Mixed
  },
  ipAddress: String,
  timestamp: {
    type: Date,
    default: Date.now
  }
});

const AuditLog = mongoose.models.AuditLog || mongoose.model('AuditLog', auditLogSchema);

module.exports = AuditLog;
