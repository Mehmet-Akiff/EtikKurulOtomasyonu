// src/models/Decision.js - Nihai Etik Kurul Kararı Mongoose Şeması

const mongoose = require('mongoose');

const memberVoteSchema = new mongoose.Schema({
  memberId: Number,
  memberName: String,
  memberTitle: String,
  decision: {
    type: String,
    enum: ['Approved', 'RevisionNeeded', 'Rejected']
  },
  scores: {
    methodology: Number,
    consentForm: Number,
    riskAssessment: Number,
    average: Number
  },
  feedback: String,
  votedAt: { type: Date, default: Date.now }
});

const decisionSchema = new mongoose.Schema({
  protocolNumber: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  decisionNumber: {
    type: String,
    required: true,
    unique: true // Örn: KARAR-2026-00042
  },
  projectTitle: {
    type: String,
    required: true
  },
  researcherName: {
    type: String,
    required: true
  },
  researcherEmail: String,
  fieldOfStudy: String,
  finalDecision: {
    type: String,
    required: true,
    enum: ['Approved', 'RevisionNeeded', 'Rejected']
  },
  summaryRationale: {
    type: String,
    required: true
  },
  conditions: [String],
  averageScore: {
    type: Number,
    default: 0
  },
  memberVotes: [memberVoteSchema],
  committeeChair: {
    name: { type: String, default: 'Prof. Dr. Selim Vural' },
    title: { type: String, default: 'Etik Kurul Başkanı' }
  },
  verificationCode: {
    type: String,
    required: true,
    unique: true
  },
  certificateHtml: String,
  decidedAt: {
    type: Date,
    default: Date.now
  }
}, { timestamps: true });

const Decision = mongoose.models.Decision || mongoose.model('Decision', decisionSchema);

module.exports = Decision;
