// src/engine/embeddedWorkflow.js - Masaüstü Uygulaması Uçtan Uca İş Akışı Motoru

const CertificateEngine = require('./certificateEngine');

class EmbeddedWorkflow {
  constructor(store) {
    this.store = store;
  }

  // 1. Araştırmacılar
  getResearchers() {
    return this.store.data.researchers;
  }

  createResearcher(data) {
    const existing = this.store.data.researchers.find(r => r.email.toLowerCase() === data.email.toLowerCase());
    if (existing) return existing;

    const newId = this.store.data.researchers.length ? Math.max(...this.store.data.researchers.map(r => r.id)) + 1 : 1;
    const researcher = {
      id: newId,
      fullName: data.fullName,
      email: data.email,
      title: data.title || '',
      department: data.department || '',
      institution: data.institution || '',
      phoneNumber: data.phoneNumber || ''
    };
    this.store.data.researchers.push(researcher);
    this.store.save();
    return researcher;
  }

  // 2. Başvurular
  getApplications() {
    return this.store.data.applications;
  }

  getApplication(protocolNumber) {
    return this.store.data.applications.find(a => a.protocolNumber === protocolNumber) || null;
  }

  createApplication(data) {
    const year = new Date().getFullYear();
    const countThisYear = this.store.data.applications.filter(a => a.protocolNumber.startsWith(`ETIK-${year}`)).length;
    const protocolNumber = `ETIK-${year}-${String(countThisYear + 1).padStart(5, '0')}`;

    const newId = this.store.data.applications.length ? Math.max(...this.store.data.applications.map(a => a.id)) + 1 : 1;
    const researcher = this.store.data.researchers.find(r => r.id === parseInt(data.researcherId)) || {};

    const application = {
      id: newId,
      protocolNumber,
      researcherId: data.researcherId,
      researcherName: researcher.fullName || data.researcherName || 'Araştırmacı',
      researcherEmail: researcher.email || data.researcherEmail || '',
      projectTitle: data.projectTitle,
      researchType: data.researchType || 'Akademik Araştırma',
      fieldOfStudy: data.fieldOfStudy || 'Genel',
      abstract: data.abstract || '',
      methodology: data.methodology || '',
      targetAudience: data.targetAudience || '',
      volunteerCount: parseInt(data.volunteerCount) || 0,
      riskLevel: data.riskLevel || 'Düşük',
      status: 'Submitted',
      submittedAt: new Date().toISOString(),
      documents: data.documents || [
        { id: 1, documentType: 'Araştırma Protokolü', fileName: 'arastirma_protokolu.pdf', uploadDate: new Date().toISOString() },
        { id: 2, documentType: 'Bilgilendirilmiş Onam Formu', fileName: 'onam_formu.pdf', uploadDate: new Date().toISOString() }
      ]
    };

    this.store.data.applications.unshift(application);
    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'APPLICATION_SUBMITTED',
      details: { title: data.projectTitle, researcher: application.researcherName },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return application;
  }

  // 3. Kurul Üyeleri & Otomatik Dosya Dağıtımı
  getCommitteeMembers() {
    return this.store.data.committeeMembers;
  }

  autoAssign(protocolNumber, requiredReviewers = 2) {
    const app = this.getApplication(protocolNumber);
    if (!app) throw new Error(`Başvuru (${protocolNumber}) bulunamadı.`);

    // Zaten atanmış mı?
    const existing = this.store.data.assignments.filter(a => a.protocolNumber === protocolNumber);
    if (existing.length > 0) {
      return { status: 'already_assigned', message: 'Bu başvuruya zaten raportör atanmış.', assignments: existing };
    }

    const fieldKeywords = this.tokenizeField(app.fieldOfStudy);
    const members = this.store.data.committeeMembers.filter(m => m.isActive);

    const candidates = members.map(m => {
      const expKeywords = this.tokenizeField(m.fieldOfExpertise);
      const matchCount = expKeywords.filter(k => fieldKeywords.includes(k)).length;
      const score = (matchCount * 100) - (m.activeFileCount * 10);
      return { member: m, score, matchCount, activeFileCount: m.activeFileCount };
    });

    candidates.sort((a, b) => {
      if (a.score === b.score) return a.activeFileCount - b.activeFileCount;
      return b.score - a.score;
    });

    const selected = candidates.slice(0, requiredReviewers);
    const createdAssignments = [];

    selected.forEach(cand => {
      const m = cand.member;
      const assignmentId = this.store.data.assignments.length ? Math.max(...this.store.data.assignments.map(a => a.id)) + 1 : 1;
      const assignment = {
        id: assignmentId,
        protocolNumber,
        projectTitle: app.projectTitle,
        fieldOfStudy: app.fieldOfStudy,
        memberId: m.id,
        memberName: m.fullName,
        memberTitle: m.title,
        status: 'Pending',
        assignedAt: new Date().toISOString(),
        dueDate: new Date(Date.now() + 15 * 86400000).toISOString().split('T')[0]
      };
      m.activeFileCount = (m.activeFileCount || 0) + 1;
      this.store.data.assignments.push(assignment);
      createdAssignments.push(assignment);
    });

    app.status = 'UnderReview';
    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'MEMBERS_ASSIGNED',
      details: { reviewers: createdAssignments.map(a => a.memberName) },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return { status: 'success', protocolNumber, assignedCount: createdAssignments.length, assignments: createdAssignments };
  }

  tokenizeField(text) {
    if (!text) return [];
    return text.toLowerCase()
      .replace(/[^a-z0-9ğüşıöç\s]/gi, ' ')
      .split(/\s+/)
      .filter(w => w.length > 2 && !['ve', 'ile', 'veya', 'bir', 'için', 'bilimleri'].includes(w));
  }

  getAssignments(memberId) {
    if (memberId) {
      return this.store.data.assignments.filter(a => a.memberId === parseInt(memberId));
    }
    return this.store.data.assignments;
  }

  // 4. Değerlendirme & Puanlama
  submitEvaluation(data) {
    const { assignmentId, protocolNumber, memberId, methodologyScore, consentFormScore, riskAssessmentScore, decision, feedbackNotes } = data;
    const assignment = this.store.data.assignments.find(a => a.id === parseInt(assignmentId));
    if (!assignment) throw new Error('Atama kaydı bulunamadı.');

    const member = this.store.data.committeeMembers.find(m => m.id === parseInt(memberId));
    const evalId = this.store.data.evaluations.length ? Math.max(...this.store.data.evaluations.map(e => e.id)) + 1 : 1;

    const evaluation = {
      id: evalId,
      assignmentId: parseInt(assignmentId),
      protocolNumber,
      memberId: parseInt(memberId),
      memberName: member?.fullName || assignment.memberName,
      memberTitle: member?.title || assignment.memberTitle,
      methodologyScore: parseInt(methodologyScore),
      consentFormScore: parseInt(consentFormScore),
      riskAssessmentScore: parseInt(riskAssessmentScore),
      averageScore: (parseInt(methodologyScore) + parseInt(consentFormScore) + parseInt(riskAssessmentScore)) / 3.0,
      decision,
      feedbackNotes,
      evaluatedAt: new Date().toISOString()
    };

    this.store.data.evaluations.push(evaluation);
    assignment.status = 'Completed';

    if (member && member.activeFileCount > 0) {
      member.activeFileCount -= 1;
    }

    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'EVALUATION_RECEIVED',
      details: { member: evaluation.memberName, decision },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return evaluation;
  }

  getEvaluationSummary(protocolNumber) {
    const evals = this.store.data.evaluations.filter(e => e.protocolNumber === protocolNumber);
    const assigns = this.store.data.assignments.filter(a => a.protocolNumber === protocolNumber);
    
    const votes = { Approved: 0, RevisionNeeded: 0, Rejected: 0 };
    let totalScore = 0;
    evals.forEach(e => {
      if (votes[e.decision] !== undefined) votes[e.decision]++;
      totalScore += e.averageScore;
    });

    const averageScore = evals.length ? totalScore / evals.length : 0;
    let recommendation = 'AwaitingReviews';
    if (evals.length >= assigns.length && assigns.length > 0) {
      if (votes.Rejected > 0) recommendation = 'Rejected';
      else if (votes.RevisionNeeded > 0) recommendation = 'RevisionNeeded';
      else recommendation = 'Approved';
    }

    return {
      protocolNumber,
      totalAssigned: assigns.length,
      completedReviews: evals.length,
      recommendation,
      averageScore,
      votes,
      evaluations: evals
    };
  }

  // 5. Karar Kesinleştirme ve Otomatik Belge Üretimi
  async finalizeDecision(data) {
    const { protocolNumber, finalDecision, summaryRationale, conditions } = data;
    const app = this.getApplication(protocolNumber);
    if (!app) throw new Error(`Başvuru (${protocolNumber}) bulunamadı.`);

    const summary = this.getEvaluationSummary(protocolNumber);
    const year = new Date().getFullYear();
    const countThisYear = this.store.data.decisions.filter(d => d.decisionNumber.startsWith(`KARAR-${year}`)).length;
    const decisionNumber = `KARAR-${year}-${String(countThisYear + 1).padStart(5, '0')}`;
    const verificationCode = CertificateEngine.generateVerificationCode(protocolNumber, decisionNumber);

    const certificateData = {
      protocolNumber,
      decisionNumber,
      projectTitle: app.projectTitle,
      researcherName: app.researcherName,
      researcherEmail: app.researcherEmail,
      fieldOfStudy: app.fieldOfStudy,
      finalDecision: finalDecision || summary.recommendation || 'Approved',
      summaryRationale: summaryRationale || (finalDecision === 'Approved' 
        ? 'Etik Kurul tarafından yapılan inceleme neticesinde araştırma önerisi bilimsel ve etik ilkelere tam uyumlu bulunmuştur.'
        : 'Araştırma önerisinde yer alan riskler ve metodolojik yetersizlikler sebebiyle etik uygunluk verilememiştir.'),
      conditions: conditions || [
        'Araştırma yalnızca kurula sunulan ve onaylanan protokol kapsamında yürütülmelidir.',
        'Herhangi bir protokol değişikliği durumunda kurula ek onay başvurusu yapılmalıdır.'
      ],
      averageScore: summary.averageScore || 5.0,
      decidedAt: new Date().toISOString(),
      committeeChair: { name: 'Prof. Dr. Selim Vural', title: 'Etik Kurul Başkanı' },
      memberVotes: summary.evaluations.map(e => ({
        memberName: e.memberName,
        memberTitle: e.memberTitle,
        decision: e.decision,
        votedAt: e.evaluatedAt
      })),
      verificationCode
    };

    const certificateHtml = await CertificateEngine.generateCertificateHtml(certificateData);
    const decisionRecord = {
      ...certificateData,
      certificateHtml
    };

    // Varsa güncelle yoksa ekle
    const existingIdx = this.store.data.decisions.findIndex(d => d.protocolNumber === protocolNumber);
    if (existingIdx >= 0) {
      this.store.data.decisions[existingIdx] = decisionRecord;
    } else {
      this.store.data.decisions.unshift(decisionRecord);
    }

    app.status = certificateData.finalDecision;
    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'DECISION_FINALIZED',
      details: { decisionNumber, finalDecision: certificateData.finalDecision, verificationCode },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return decisionRecord;
  }

  getDecision(protocolNumber) {
    return this.store.data.decisions.find(d => d.protocolNumber === protocolNumber) || null;
  }

  verifyCertificate(code) {
    const decision = this.store.data.decisions.find(d => d.verificationCode === code.trim().toUpperCase());
    if (!decision) {
      return { valid: false, message: 'Geçersiz veya bulunamayan doğrulama kodu.' };
    }
    return {
      valid: true,
      protocolNumber: decision.protocolNumber,
      decisionNumber: decision.decisionNumber,
      projectTitle: decision.projectTitle,
      researcherName: decision.researcherName,
      finalDecision: decision.finalDecision,
      decidedAt: decision.decidedAt
    };
  }

  // 6. Revizyon Talebi
  requestRevision(data) {
    const { protocolNumber, feedbackSummary, requiredCorrections, deadlineDays = 14 } = data;
    const app = this.getApplication(protocolNumber);
    if (!app) throw new Error('Başvuru bulunamadı.');

    const deadline = new Date(Date.now() + deadlineDays * 86400000).toISOString().split('T')[0];
    const revision = {
      id: this.store.data.revisions.length + 1,
      protocolNumber,
      feedbackSummary,
      requiredCorrections: requiredCorrections || [],
      deadline,
      status: 'PendingResearcher',
      requestedAt: new Date().toISOString()
    };

    this.store.data.revisions.push(revision);
    app.status = 'RevisionRequested';
    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'REVISION_REQUESTED',
      details: { deadline, feedbackSummary },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return revision;
  }
}

module.exports = EmbeddedWorkflow;
