// src/models/RevisionRequest.js - Revizyon Talepleri Mongoose Şeması

const mongoose = require('mongoose');

const revisionRequestSchema = new mongoose.Schema({
  protocolNumber: {
    type: String,
    required: true,
    index: true
  },
  cycle: {
    type: Number,
    default: 1
  },
  requestedBy: {
    type: String,
    default: 'Etik Kurul Raportörleri'
  },
  feedbackSummary: {
    type: String,
    required: true
  },
  requiredCorrections: [{
    section: String, // 'Metodoloji', 'Bilgilendirilmiş Onam Formu', 'Veri Güvenliği' vb.
    issue: String,
    actionRequired: String
  }],
  deadline: {
    type: Date,
    required: true
  },
  status: {
    type: String,
    enum: ['PendingResearcher', 'SubmittedByResearcher', 'Accepted', 'Rejected'],
    default: 'PendingResearcher'
  },
  researcherResponse: {
    responseNotes: String,
    resubmittedFiles: [String],
    submittedAt: Date
  }
}, { timestamps: true });

const RevisionRequest = mongoose.models.RevisionRequest || mongoose.model('RevisionRequest', revisionRequestSchema);

module.exports = RevisionRequest;
