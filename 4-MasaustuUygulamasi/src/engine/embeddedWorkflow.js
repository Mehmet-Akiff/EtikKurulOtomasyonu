// src/engine/embeddedWorkflow.js - Masaüstü Uygulaması Uçtan Uca İş Akışı Motoru

const CertificateEngine = require('./certificateEngine');

class EmbeddedWorkflow {
  constructor(store) {
    this.store = store;
  }

  // Geçmiş / Mevcut Verileri Senkronize Etme ve Onarma
  async reconcileState() {
    let changed = false;

    // 1. Araştırmacı ID tipini normalize et
    for (const app of this.store.data.applications) {
      if (typeof app.researcherId === 'string') {
        app.researcherId = parseInt(app.researcherId, 10) || 1;
        changed = true;
      }
    }

    // 2. Kurul üyelerinin aktif dosya sayılarını gerçek bekleyen atamalara göre senkronize et
    for (const member of this.store.data.committeeMembers) {
      const realPendingCount = this.store.data.assignments.filter(
        a => a.memberId === member.id && a.status === 'Pending'
      ).length;
      if (member.activeFileCount !== realPendingCount) {
        member.activeFileCount = realPendingCount;
        changed = true;
      }
    }

    // 3. Değerlendirmesi yapılmış ancak karar kaydı oluşmamış veya durumu UnderReview kalmış başvuruları onar
    for (const app of this.store.data.applications) {
      const evals = this.store.data.evaluations.filter(e => e.protocolNumber === app.protocolNumber);
      const existingDecision = this.getDecision(app.protocolNumber);

      if (evals.length > 0 && (!existingDecision || app.status === 'UnderReview' || app.status === 'Submitted')) {
        await this.finalizeDecision({ protocolNumber: app.protocolNumber });
        changed = true;
      }
    }

    if (changed) {
      this.store.save();
    }
    return { reconciled: true, changed };
  }

  // 1. Araştırmacılar
  getResearchers() {
    return this.store.data.researchers;
  }

  createResearcher(data) {
    const existing = this.store.data.researchers.find(
      r => r.email.toLocaleLowerCase('tr-TR') === (data.email || '').toLocaleLowerCase('tr-TR')
    );
    if (existing) return existing;

    const newId = this.store.data.researchers.length
      ? Math.max(...this.store.data.researchers.map(r => r.id)) + 1
      : 1;
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
    const prefix = `ETIK-${year}-`;
    const maxSeq = this.store.data.applications
      .filter(a => a.protocolNumber && a.protocolNumber.startsWith(prefix))
      .reduce((max, a) => {
        const num = parseInt(a.protocolNumber.replace(prefix, ''), 10);
        return !isNaN(num) && num > max ? num : max;
      }, 0);
    const protocolNumber = `${prefix}${String(maxSeq + 1).padStart(5, '0')}`;

    const newId = this.store.data.applications.length
      ? Math.max(...this.store.data.applications.map(a => a.id)) + 1
      : 1;
    const parsedResearcherId = parseInt(data.researcherId, 10) || 1;
    const researcher = this.store.data.researchers.find(r => r.id === parsedResearcherId) || {};

    const application = {
      id: newId,
      protocolNumber,
      researcherId: parsedResearcherId,
      researcherName: researcher.fullName || data.researcherName || 'Araştırmacı',
      researcherEmail: researcher.email || data.researcherEmail || '',
      projectTitle: data.projectTitle,
      researchType: data.researchType || 'Akademik Araştırma',
      fieldOfStudy: data.fieldOfStudy || 'Genel',
      abstract: data.abstract || '',
      methodology: data.methodology || '',
      targetAudience: data.targetAudience || '',
      volunteerCount: parseInt(data.volunteerCount, 10) || 0,
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
      const score = (matchCount * 100) - ((m.activeFileCount || 0) * 10);
      return { member: m, score, matchCount, activeFileCount: m.activeFileCount || 0 };
    });

    candidates.sort((a, b) => {
      if (a.score === b.score) return a.activeFileCount - b.activeFileCount;
      return b.score - a.score;
    });

    const count = Math.max(1, parseInt(requiredReviewers, 10) || 2);
    const selected = candidates.slice(0, count);
    const createdAssignments = [];

    selected.forEach(cand => {
      const m = cand.member;
      const assignmentId = this.store.data.assignments.length
        ? Math.max(...this.store.data.assignments.map(a => a.id)) + 1
        : 1;
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
    return text
      .toLocaleLowerCase('tr-TR')
      .replace(/[^a-z0-9ğüşıöç\s]/gi, ' ')
      .split(/\s+/)
      .filter(w => w.length > 2 && !['ve', 'ile', 'veya', 'bir', 'için', 'bilimleri', 'bilimler'].includes(w));
  }

  getAssignments(memberId) {
    if (memberId) {
      return this.store.data.assignments.filter(a => a.memberId === parseInt(memberId, 10));
    }
    return this.store.data.assignments;
  }

  getEvaluations(protocolNumber) {
    if (protocolNumber) {
      return this.store.data.evaluations.filter(e => e.protocolNumber === protocolNumber);
    }
    return this.store.data.evaluations;
  }

  // 4. Değerlendirme & Puanlama (Otomatik Karar Senkronizasyonlu)
  async submitEvaluation(data) {
    const {
      assignmentId,
      protocolNumber,
      memberId,
      methodologyScore,
      consentFormScore,
      riskAssessmentScore,
      decision,
      feedbackNotes
    } = data;

    const parsedAssignmentId = parseInt(assignmentId, 10);
    const parsedMemberId = parseInt(memberId, 10);
    const assignment = this.store.data.assignments.find(a => a.id === parsedAssignmentId);
    if (!assignment) throw new Error('Atama kaydı bulunamadı.');

    const member = this.store.data.committeeMembers.find(m => m.id === parsedMemberId);
    const mScore = parseInt(methodologyScore, 10) || 5;
    const cScore = parseInt(consentFormScore, 10) || 5;
    const rScore = parseInt(riskAssessmentScore, 10) || 5;

    // Aynı atama için daha önce değerlendirme yapılmış mı kontrol et
    const existingEvalIdx = this.store.data.evaluations.findIndex(e => e.assignmentId === parsedAssignmentId);
    let evaluation;

    if (existingEvalIdx >= 0) {
      evaluation = {
        ...this.store.data.evaluations[existingEvalIdx],
        methodologyScore: mScore,
        consentFormScore: cScore,
        riskAssessmentScore: rScore,
        averageScore: (mScore + cScore + rScore) / 3.0,
        decision,
        feedbackNotes: feedbackNotes || '',
        evaluatedAt: new Date().toISOString()
      };
      this.store.data.evaluations[existingEvalIdx] = evaluation;
    } else {
      const evalId = this.store.data.evaluations.length
        ? Math.max(...this.store.data.evaluations.map(e => e.id)) + 1
        : 1;

      evaluation = {
        id: evalId,
        assignmentId: parsedAssignmentId,
        protocolNumber,
        memberId: parsedMemberId,
        memberName: member?.fullName || assignment.memberName,
        memberTitle: member?.title || assignment.memberTitle,
        methodologyScore: mScore,
        consentFormScore: cScore,
        riskAssessmentScore: rScore,
        averageScore: (mScore + cScore + rScore) / 3.0,
        decision,
        feedbackNotes: feedbackNotes || '',
        evaluatedAt: new Date().toISOString()
      };

      this.store.data.evaluations.push(evaluation);

      if (assignment.status !== 'Completed') {
        assignment.status = 'Completed';
        if (member && member.activeFileCount > 0) {
          member.activeFileCount -= 1;
        }
      }
    }

    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'EVALUATION_RECEIVED',
      details: { member: evaluation.memberName, decision },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    // Değerlendirme kaydedildiği anda kurul kararını ve sertifikayı otomatik oluştur/güncelle
    const decisionRecord = await this.finalizeDecision({ protocolNumber });
    const summary = this.getEvaluationSummary(protocolNumber);

    return {
      ...evaluation,
      decisionRecord,
      summary
    };
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
    if (evals.length > 0) {
      if (votes.Rejected > 0) recommendation = 'Rejected';
      else if (votes.RevisionNeeded > 0) recommendation = 'RevisionNeeded';
      else recommendation = 'Approved';
    }

    return {
      protocolNumber,
      totalAssigned: assigns.length,
      completedReviews: evals.length,
      allCompleted: assigns.length > 0 && evals.length >= assigns.length,
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
    const effectiveDecision =
      finalDecision ||
      (summary.recommendation !== 'AwaitingReviews' ? summary.recommendation : 'Approved');

    // Bu protokol için daha önce üretilmiş karar varsa karar numarasını koru
    const existingIdx = this.store.data.decisions.findIndex(d => d.protocolNumber === protocolNumber);
    const year = new Date().getFullYear();
    const prefix = `KARAR-${year}-`;

    let decisionNumber;
    if (existingIdx >= 0 && this.store.data.decisions[existingIdx].decisionNumber) {
      decisionNumber = this.store.data.decisions[existingIdx].decisionNumber;
    } else {
      const maxSeq = this.store.data.decisions
        .filter(d => d.decisionNumber && d.decisionNumber.startsWith(prefix))
        .reduce((max, d) => {
          const num = parseInt(d.decisionNumber.replace(prefix, ''), 10);
          return !isNaN(num) && num > max ? num : max;
        }, 0);
      decisionNumber = `${prefix}${String(maxSeq + 1).padStart(5, '0')}`;
    }

    const verificationCode = CertificateEngine.generateVerificationCode(protocolNumber, decisionNumber);

    const reviewerNotes = summary.evaluations
      .map(e => (e.feedbackNotes || '').trim())
      .filter(Boolean)
      .join(' | ');

    let defaultRationale;
    if (effectiveDecision === 'Approved') {
      defaultRationale =
        'Etik Kurul tarafından yapılan inceleme neticesinde araştırma önerisi bilimsel ve etik ilkelere tam uyumlu bulunmuştur.' +
        (reviewerNotes ? ` Raportör Görüşü: ${reviewerNotes}` : '');
    } else if (effectiveDecision === 'RevisionNeeded') {
      defaultRationale =
        'Kurul değerlendirmesi sonucunda araştırmanın etik onayı öncesinde belirtilen hususlarda düzeltme (revizyon) yapılmasına karar verilmiştir.' +
        (reviewerNotes ? ` Düzeltme Talebi: ${reviewerNotes}` : '');
    } else {
      defaultRationale =
        'Araştırma önerisinde yer alan etik riskler ve metodolojik eksiklikler sebebiyle etik uygunluk verilememiştir.' +
        (reviewerNotes ? ` Ret Gerekçesi: ${reviewerNotes}` : '');
    }

    const certificateData = {
      protocolNumber,
      decisionNumber,
      projectTitle: app.projectTitle,
      researcherName: app.researcherName,
      researcherEmail: app.researcherEmail,
      fieldOfStudy: app.fieldOfStudy,
      finalDecision: effectiveDecision,
      summaryRationale: summaryRationale || defaultRationale,
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
    if (existingIdx >= 0) {
      this.store.data.decisions[existingIdx] = decisionRecord;
    } else {
      this.store.data.decisions.unshift(decisionRecord);
    }

    app.status = effectiveDecision;

    if (effectiveDecision === 'RevisionNeeded') {
      const hasPendingRev = this.store.data.revisions.some(
        r => r.protocolNumber === protocolNumber && r.status === 'PendingResearcher'
      );
      if (!hasPendingRev) {
        const deadline = new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0];
        this.store.data.revisions.push({
          id: this.store.data.revisions.length + 1,
          protocolNumber,
          feedbackSummary: certificateData.summaryRationale,
          requiredCorrections: reviewerNotes ? [reviewerNotes] : [],
          deadline,
          status: 'PendingResearcher',
          requestedAt: new Date().toISOString()
        });
      }
    } else if (effectiveDecision === 'Approved') {
      // Varsa açık revizyon taleplerini tamamlandı olarak işaretle
      this.store.data.revisions
        .filter(r => r.protocolNumber === protocolNumber && r.status === 'PendingResearcher')
        .forEach(r => {
          r.status = 'Completed';
          r.completedAt = new Date().toISOString();
        });
    }

    this.store.data.auditLogs.push({
      protocolNumber,
      action: 'DECISION_FINALIZED',
      details: { decisionNumber, finalDecision: effectiveDecision, verificationCode },
      timestamp: new Date().toISOString()
    });
    this.store.save();

    return decisionRecord;
  }

  getDecisions() {
    return this.store.data.decisions;
  }

  getDecision(protocolNumber) {
    return this.store.data.decisions.find(d => d.protocolNumber === protocolNumber) || null;
  }

  verifyCertificate(code) {
    if (!code) {
      return { valid: false, message: 'Doğrulama kodu boş olamaz.' };
    }
    const cleanCode = code.trim().toUpperCase();
    const decision = this.store.data.decisions.find(d => d.verificationCode === cleanCode);
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
    app.status = 'RevisionNeeded';
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
