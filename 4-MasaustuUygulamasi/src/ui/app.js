// src/ui/app.js - Masaüstü Arayüz Kontrolcüsü ve Reaktif İş Akışı

document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  try {
    if (window.api.reconcileState) {
      await window.api.reconcileState();
    }
  } catch (err) {
    console.warn('Durum senkronizasyonu uyarısı:', err);
  }
  await refreshAllViews();
});

async function refreshAllViews() {
  await Promise.all([
    loadDashboard(),
    loadResearchers(),
    loadUnassignedList(),
    loadMembersLoadList(),
    loadAssignmentsForEval(),
    loadDecisions(),
    loadQuickVerifyCodes()
  ]);
}

function switchTab(targetTabId) {
  const navItems = document.querySelectorAll('.nav-item');
  const tabs = document.querySelectorAll('.content-tab');

  navItems.forEach(n => {
    if (n.getAttribute('data-tab') === targetTabId) {
      n.classList.add('active');
    } else {
      n.classList.remove('active');
    }
  });

  tabs.forEach(t => {
    if (t.id === targetTabId) {
      t.classList.add('active');
    } else {
      t.classList.remove('active');
    }
  });

  if (targetTabId === 'tab-dashboard') loadDashboard();
  if (targetTabId === 'tab-application') loadResearchers();
  if (targetTabId === 'tab-assignment') {
    loadUnassignedList();
    loadMembersLoadList();
  }
  if (targetTabId === 'tab-evaluation') loadAssignmentsForEval();
  if (targetTabId === 'tab-decision') loadDecisions();
  if (targetTabId === 'tab-verify') loadQuickVerifyCodes();
}

// Sekme Yönetimi
function setupTabs() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTabId = item.getAttribute('data-tab');
      switchTab(targetTabId);
    });
  });
}

// 1. DASHBOARD
async function loadDashboard() {
  try {
    const apps = await window.api.getApplications();
    const members = await window.api.getCommitteeMembers();
    const decisions = window.api.getDecisions ? await window.api.getDecisions() : [];

    const approvedCount = apps.filter(a => a.status === 'Approved').length;
    const underReviewCount = apps.filter(
      a => a.status === 'UnderReview' || a.status === 'Submitted' || a.status === 'RevisionNeeded' || a.status === 'RevisionRequested'
    ).length;

    document.getElementById('statTotalApps').innerText = apps.length;
    document.getElementById('statUnderReview').innerText = underReviewCount;
    document.getElementById('statApproved').innerText = Math.max(
      approvedCount,
      decisions.filter(d => d.finalDecision === 'Approved').length
    );
    document.getElementById('statMembers').innerText = members.filter(m => m.isActive).length;

    const tbody = document.getElementById('dashboardTableBody');
    tbody.innerHTML = '';

    if (apps.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#888;">Henüz kayıtlı başvuru bulunmamaktadır.</td></tr>';
      return;
    }

    apps.forEach(a => {
      const tr = document.createElement('tr');
      const badgeClass = getBadgeClass(a.status);
      const dateStr = a.submittedAt ? new Date(a.submittedAt).toLocaleDateString('tr-TR') : '-';

      let actionBtnHtml = '';
      if (a.status === 'Submitted') {
        actionBtnHtml = `
          <button class="btn btn-primary btn-xs" onclick="goToAssign('${escapeAttr(a.protocolNumber)}')">
            <i class="fa-solid fa-robot"></i> Raportör Ata
          </button>`;
      } else if (a.status === 'UnderReview') {
        actionBtnHtml = `
          <button class="btn btn-warning btn-xs" onclick="goToEvaluate('${escapeAttr(a.protocolNumber)}')">
            <i class="fa-solid fa-clipboard-check"></i> Değerlendir
          </button>`;
      } else {
        actionBtnHtml = `
          <div class="action-group">
            <button class="btn btn-success btn-xs" onclick="viewCertificate('${escapeAttr(a.protocolNumber)}')">
              <i class="fa-solid fa-file-pdf"></i> Karar Belgesi
            </button>
            <button class="btn btn-secondary btn-xs" onclick="switchTab('tab-decision')">
              <i class="fa-solid fa-stamp"></i> Kararlar
            </button>
          </div>`;
      }

      tr.innerHTML = `
        <td><strong>${escapeHtml(a.protocolNumber)}</strong></td>
        <td>${escapeHtml(a.projectTitle)}</td>
        <td>${escapeHtml(a.researcherName)}</td>
        <td><small class="text-muted">${escapeHtml(a.fieldOfStudy)}</small></td>
        <td><span class="status-badge ${badgeClass}">${formatStatus(a.status)}</span></td>
        <td>${dateStr}</td>
        <td>${actionBtnHtml}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    showToast('Dashboard verisi yüklenirken hata: ' + e.message, 'error');
  }
}

async function goToAssign(protocolNumber) {
  switchTab('tab-assignment');
  await triggerAutoAssign(protocolNumber);
}

async function goToEvaluate(protocolNumber) {
  switchTab('tab-evaluation');
  await loadAssignmentsForEval(protocolNumber);
}

// 2. YENİ BAŞVURU & ARAŞTIRMACI EKLEME
async function loadResearchers(selectedId) {
  try {
    const researchers = await window.api.getResearchers();
    const sel = document.getElementById('appResearcherSelect');
    const currentVal = selectedId || sel.value;
    sel.innerHTML = '<option value="">Araştırmacı Seçiniz...</option>';

    researchers.forEach(r => {
      const opt = document.createElement('option');
      opt.value = String(r.id);
      opt.textContent = `${r.title ? r.title + ' ' : ''}${r.fullName} (${r.department || 'Genel'} - ${r.institution || 'Üniversite'})`;
      if (String(currentVal) === String(r.id)) {
        opt.selected = true;
      }
      sel.appendChild(opt);
    });
  } catch (e) {
    console.error(e);
  }
}

function toggleNewResearcherBox() {
  const box = document.getElementById('newResearcherBox');
  if (!box) return;
  box.style.display = box.style.display === 'none' ? 'block' : 'none';
}

async function handleCreateResearcher() {
  const title = document.getElementById('newResTitle').value.trim();
  const fullName = document.getElementById('newResName').value.trim();
  const email = document.getElementById('newResEmail').value.trim();
  const department = document.getElementById('newResDept').value.trim();

  if (!fullName || !email) {
    showToast('Lütfen araştırmacının Ad Soyad ve E-Posta bilgilerini giriniz.', 'error');
    return;
  }

  try {
    const res = await window.api.createResearcher({
      title: title || 'Arş. Gör.',
      fullName,
      email,
      department: department || 'Akademik Bölüm',
      institution: 'Merkez Üniversitesi'
    });
    showToast(`✅ Araştırmacı eklendi: ${res.fullName}`, 'success');
    document.getElementById('newResTitle').value = '';
    document.getElementById('newResName').value = '';
    document.getElementById('newResEmail').value = '';
    document.getElementById('newResDept').value = '';
    document.getElementById('newResearcherBox').style.display = 'none';
    await loadResearchers(res.id);
  } catch (e) {
    showToast('Araştırmacı eklenirken hata: ' + e.message, 'error');
  }
}

async function handleCreateApplication(event) {
  event.preventDefault();
  const researcherId = document.getElementById('appResearcherSelect').value;
  const projectTitle = document.getElementById('appProjectTitle').value.trim();
  const researchType = document.getElementById('appResearchType').value;
  const fieldOfStudy = document.getElementById('appFieldOfStudy').value;
  const volunteerCount = document.getElementById('appVolunteerCount').value;
  const riskLevel = document.getElementById('appRiskLevel').value;
  const abstract = document.getElementById('appAbstract').value.trim();
  const methodology = document.getElementById('appMethodology').value.trim();

  if (!researcherId) {
    showToast('Lütfen bir sorumlu araştırmacı seçiniz.', 'error');
    return;
  }

  try {
    const result = await window.api.createApplication({
      researcherId: parseInt(researcherId, 10),
      projectTitle,
      researchType,
      fieldOfStudy,
      volunteerCount,
      riskLevel,
      abstract,
      methodology
    });

    showToast(`✅ Başvuru oluşturuldu! Protokol No: ${result.protocolNumber}`, 'success');
    document.getElementById('newApplicationForm').reset();
    await refreshAllViews();
    switchTab('tab-assignment');
  } catch (e) {
    showToast('Başvuru gönderilirken hata: ' + e.message, 'error');
  }
}

// 3. OTOMATİK ATAMA
async function loadUnassignedList() {
  try {
    const apps = await window.api.getApplications();
    const assignments = await window.api.getAssignments();
    const assignedProtocols = new Set(assignments.map(a => a.protocolNumber));

    const unassigned = apps.filter(a => !assignedProtocols.has(a.protocolNumber));
    const container = document.getElementById('unassignedList');
    container.innerHTML = '';

    if (unassigned.length === 0) {
      container.innerHTML = '<div style="color: #64748b; font-size: 13px; padding: 10px;">Atama bekleyen dosya bulunmuyor. Tüm başvurular raportörlere dağıtılmış.</div>';
    } else {
      unassigned.forEach(app => {
        const item = document.createElement('div');
        item.className = 'list-item-card';
        item.innerHTML = `
          <div>
            <div style="font-weight: 600; color: #1e3c72; font-size: 13.5px;">${escapeHtml(app.protocolNumber)} - ${escapeHtml(app.projectTitle)}</div>
            <div style="font-size: 11.5px; color: #64748b; margin-top: 4px;">
              Araştırmacı: ${escapeHtml(app.researcherName)} | Alan: <strong>${escapeHtml(app.fieldOfStudy)}</strong>
            </div>
          </div>
          <button class="btn btn-primary btn-sm" onclick="triggerAutoAssign('${escapeAttr(app.protocolNumber)}')">
            <i class="fa-solid fa-robot"></i> Otomatik Ata (2 Raportör)
          </button>
        `;
        container.appendChild(item);
      });
    }

    // Atanmış Dosyalar Tablosu
    const assignedTbody = document.getElementById('assignedFilesTableBody');
    if (assignedTbody) {
      assignedTbody.innerHTML = '';
      const assignedApps = apps.filter(a => assignedProtocols.has(a.protocolNumber));

      if (assignedApps.length === 0) {
        assignedTbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#888;">Henüz raportör atanmış başvuru bulunmuyor.</td></tr>';
      } else {
        assignedApps.forEach(app => {
          const appAssigns = assignments.filter(x => x.protocolNumber === app.protocolNumber);
          const completedCount = appAssigns.filter(x => x.status === 'Completed').length;
          const hasPending = appAssigns.some(x => x.status === 'Pending');

          const reviewersHtml = appAssigns
            .map(x => {
              const icon = x.status === 'Completed'
                ? '<i class="fa-solid fa-circle-check" style="color:#16a34a;"></i>'
                : '<i class="fa-solid fa-clock" style="color:#d97706;"></i>';
              return `<span class="badge-tag">${icon} ${escapeHtml(x.memberTitle)} ${escapeHtml(x.memberName)}</span>`;
            })
            .join(' ');

          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>${escapeHtml(app.protocolNumber)}</strong></td>
            <td>${escapeHtml(app.projectTitle)}</td>
            <td>${reviewersHtml}</td>
            <td>
              <span class="status-badge ${completedCount > 0 ? 'badge-approved' : 'badge-underreview'}">
                ${completedCount} / ${appAssigns.length} Değerlendirildi
              </span>
            </td>
            <td>
              ${hasPending
                ? `<button class="btn btn-warning btn-xs" onclick="goToEvaluate('${escapeAttr(app.protocolNumber)}')"><i class="fa-solid fa-clipboard-check"></i> Değerlendir</button>`
                : `<button class="btn btn-success btn-xs" onclick="switchTab('tab-decision')"><i class="fa-solid fa-stamp"></i> Kararı Gör</button>`
              }
            </td>
          `;
          assignedTbody.appendChild(tr);
        });
      }
    }
  } catch (e) {
    console.error(e);
  }
}

async function loadMembersLoadList() {
  try {
    const members = await window.api.getCommitteeMembers();
    const container = document.getElementById('membersLoadList');
    container.innerHTML = '';

    members.forEach(m => {
      const item = document.createElement('div');
      item.className = 'list-item-card';
      item.innerHTML = `
        <div>
          <div style="font-weight: 600;">${escapeHtml(m.title)} ${escapeHtml(m.fullName)}</div>
          <div style="font-size: 11.5px; color: #64748b;">${escapeHtml(m.fieldOfExpertise)}</div>
        </div>
        <div>
          <span class="status-badge ${m.activeFileCount > 2 ? 'badge-revision' : 'badge-underreview'}">
            ${m.activeFileCount || 0} Aktif Dosya
          </span>
        </div>
      `;
      container.appendChild(item);
    });
  } catch (e) {
    console.error(e);
  }
}

async function triggerAutoAssign(protocolNumber) {
  try {
    const result = await window.api.autoAssign(protocolNumber, 2);
    if (result.status === 'success') {
      const names = result.assignments.map(a => a.memberName).join(', ');
      showToast(`🤖 Başarıyla atandı: ${names}`, 'success');
      await refreshAllViews();
    } else {
      showToast(result.message || 'Bu başvuruya zaten raportör atanmış.', 'error');
      await refreshAllViews();
    }
  } catch (e) {
    showToast('Atama hatası: ' + e.message, 'error');
  }
}

// 4. DEĞERLENDİRME & PUANLAMA
async function loadAssignmentsForEval(preselectProtocol) {
  try {
    const assignments = await window.api.getAssignments();
    const pending = assignments.filter(a => a.status === 'Pending');
    const sel = document.getElementById('evalAssignmentSelect');
    sel.innerHTML = '<option value="">Bekleyen Atama Seçiniz...</option>';

    let selectedIndexToPick = 0;

    pending.forEach((a, idx) => {
      const opt = document.createElement('option');
      opt.value = String(a.id);
      opt.setAttribute('data-protocol', a.protocolNumber);
      opt.setAttribute('data-member', String(a.memberId));
      opt.setAttribute('data-title', `${a.projectTitle} [${a.fieldOfStudy}]`);
      const shortTitle = a.projectTitle.length > 40 ? a.projectTitle.substring(0, 40) + '...' : a.projectTitle;
      opt.textContent = `${a.protocolNumber} — ${a.memberTitle} ${a.memberName} (${shortTitle})`;
      sel.appendChild(opt);

      if (preselectProtocol && a.protocolNumber === preselectProtocol && selectedIndexToPick === 0) {
        selectedIndexToPick = idx + 1;
      }
    });

    if (selectedIndexToPick > 0) {
      sel.selectedIndex = selectedIndexToPick;
    } else if (pending.length === 1) {
      sel.selectedIndex = 1;
    }

    handleAssignmentSelectChange();

    // Tamamlanan Değerlendirmeler Tablosunu Yükle
    const evalsTbody = document.getElementById('completedEvaluationsTableBody');
    if (evalsTbody && window.api.getEvaluations) {
      const evals = await window.api.getEvaluations();
      evalsTbody.innerHTML = '';

      if (!evals || evals.length === 0) {
        evalsTbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#888;">Henüz tamamlanmış üye değerlendirmesi bulunmuyor.</td></tr>';
      } else {
        const sortedEvals = [...evals].reverse();
        sortedEvals.forEach(ev => {
          const tr = document.createElement('tr');
          const badgeClass = getBadgeClass(ev.decision);
          const avg = ev.averageScore ? Number(ev.averageScore).toFixed(2) : '-';
          const dateStr = ev.evaluatedAt ? new Date(ev.evaluatedAt).toLocaleDateString('tr-TR') : '-';

          tr.innerHTML = `
            <td><strong>${escapeHtml(ev.protocolNumber)}</strong></td>
            <td>${escapeHtml(ev.memberTitle || '')} ${escapeHtml(ev.memberName)}</td>
            <td>${ev.methodologyScore} / ${ev.consentFormScore} / ${ev.riskAssessmentScore}</td>
            <td><strong>${avg} / 5.0</strong></td>
            <td><span class="status-badge ${badgeClass}">${formatStatus(ev.decision)}</span></td>
            <td><small>${escapeHtml(ev.feedbackNotes || '-')}</small></td>
            <td>${dateStr}</td>
          `;
          evalsTbody.appendChild(tr);
        });
      }
    }
  } catch (e) {
    console.error(e);
  }
}

function handleAssignmentSelectChange() {
  const sel = document.getElementById('evalAssignmentSelect');
  const opt = sel.options[sel.selectedIndex];
  if (opt && opt.value) {
    document.getElementById('evalProjectTitle').value = opt.getAttribute('data-title') || '';
  } else {
    document.getElementById('evalProjectTitle').value = '';
  }
}

async function handleEvaluationSubmit(event) {
  event.preventDefault();
  const sel = document.getElementById('evalAssignmentSelect');
  const opt = sel.options[sel.selectedIndex];
  if (!opt || !opt.value) {
    showToast('Lütfen değerlendirilecek bir dosya/atama seçiniz.', 'error');
    return;
  }

  const assignmentId = opt.value;
  const protocolNumber = opt.getAttribute('data-protocol');
  const memberId = opt.getAttribute('data-member');
  const methodologyScore = document.getElementById('scoreMethodology').value;
  const consentFormScore = document.getElementById('scoreConsent').value;
  const riskAssessmentScore = document.getElementById('scoreRisk').value;
  const decision = document.getElementById('evalDecisionChoice').value;
  const feedbackNotes = document.getElementById('evalFeedbackNotes').value.trim();

  try {
    const res = await window.api.submitEvaluation({
      assignmentId,
      protocolNumber,
      memberId,
      methodologyScore,
      consentFormScore,
      riskAssessmentScore,
      decision,
      feedbackNotes
    });

    const decRecord = res.decisionRecord || (await window.api.getDecision(protocolNumber));
    document.getElementById('evaluationForm').reset();
    await refreshAllViews();

    if (decRecord) {
      showToast(
        `🎉 ${protocolNumber} için değerlendirme kaydedildi ve Kurul Kararı (${decRecord.decisionNumber} - ${formatStatus(decRecord.finalDecision)}) oluşturuldu!`,
        'success'
      );
      switchTab('tab-decision');
    } else {
      showToast('✅ Değerlendirme başarıyla kaydedildi!', 'success');
    }
  } catch (e) {
    showToast('Değerlendirme kaydedilirken hata: ' + e.message, 'error');
  }
}

// 5. KARAR & BELGELER
async function loadDecisions() {
  try {
    const apps = await window.api.getApplications();
    const allDecisions = window.api.getDecisions ? await window.api.getDecisions() : [];

    const tbody = document.getElementById('decisionsTableBody');
    const pendingTbody = document.getElementById('pendingDecisionsTableBody');
    tbody.innerHTML = '';
    if (pendingTbody) pendingTbody.innerHTML = '';

    // Kararları hem decisions listesinden hem de başvurular üzerinden eşleştir
    const decisionMap = new Map();
    allDecisions.forEach(d => decisionMap.set(d.protocolNumber, d));
    for (const app of apps) {
      if (!decisionMap.has(app.protocolNumber)) {
        const d = await window.api.getDecision(app.protocolNumber);
        if (d) decisionMap.set(app.protocolNumber, d);
      }
    }

    const decidedList = Array.from(decisionMap.values());

    if (decidedList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; color:#888;">Henüz kesinleşmiş bir kurul kararı bulunmuyor.</td></tr>';
    } else {
      for (const dec of decidedList) {
        const tr = document.createElement('tr');
        const badgeClass = getBadgeClass(dec.finalDecision);
        const avgStr = dec.averageScore ? Number(dec.averageScore).toFixed(2) : '5.00';
        const voteCount = Array.isArray(dec.memberVotes) ? dec.memberVotes.length : 0;

        let extraActions = '';
        if (dec.finalDecision === 'RevisionNeeded' || dec.finalDecision === 'Rejected') {
          extraActions = `
            <button class="btn btn-success btn-xs" title="Düzeltme sonrası kurula sunulan başvuruyu onayla" onclick="handleDirectDecision('${escapeAttr(dec.protocolNumber)}', 'Approved')">
              <i class="fa-solid fa-check"></i> Onayla
            </button>
          `;
        }

        tr.innerHTML = `
          <td><strong>${escapeHtml(dec.decisionNumber)}</strong></td>
          <td><strong>${escapeHtml(dec.protocolNumber)}</strong></td>
          <td>${escapeHtml(dec.projectTitle)}</td>
          <td>${escapeHtml(dec.researcherName)}</td>
          <td><span class="status-badge ${badgeClass}">${formatStatus(dec.finalDecision)}</span></td>
          <td>
            <strong>${avgStr} / 5.0</strong>
            <div style="font-size:11px; color:#64748b;">(${voteCount} Üye Oyu)</div>
          </td>
          <td>
            <span class="code-pill" title="Doğrulama sekmesinde sorgulamak için tıklayın" onclick="verifyFromDecision('${escapeAttr(dec.verificationCode)}')">
              <i class="fa-solid fa-shield-halved"></i> ${escapeHtml(dec.verificationCode)}
            </span>
          </td>
          <td>
            <div class="action-group">
              <button class="btn btn-primary btn-xs" onclick="viewCertificate('${escapeAttr(dec.protocolNumber)}')">
                <i class="fa-solid fa-file-pdf"></i> Resmi Belge (HTML/QR)
              </button>
              ${extraActions}
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      }
    }

    // Henüz Kararı Olmayan Başvuruları "Karar Bekleyen Başvurular" Tablosunda Göster
    if (pendingTbody) {
      const pendingApps = apps.filter(a => !decisionMap.has(a.protocolNumber));
      if (pendingApps.length === 0) {
        pendingTbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#888;">Karar bekleyen açık başvuru bulunmuyor. Tüm başvurular karara bağlanmış.</td></tr>';
      } else {
        for (const app of pendingApps) {
          const summary = await window.api.getEvaluationSummary(app.protocolNumber);
          const badgeClass = getBadgeClass(app.status);
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>${escapeHtml(app.protocolNumber)}</strong></td>
            <td>${escapeHtml(app.projectTitle)}</td>
            <td>${escapeHtml(app.researcherName)}</td>
            <td><span class="status-badge ${badgeClass}">${formatStatus(app.status)}</span></td>
            <td><small>${summary.completedReviews} / ${summary.totalAssigned} Raportör Oyu</small></td>
            <td>
              <div class="action-group">
                <button class="btn btn-success btn-xs" onclick="handleDirectDecision('${escapeAttr(app.protocolNumber)}', 'Approved')">
                  <i class="fa-solid fa-check"></i> Onayla
                </button>
                <button class="btn btn-warning btn-xs" onclick="handleDirectDecision('${escapeAttr(app.protocolNumber)}', 'RevisionNeeded')">
                  <i class="fa-solid fa-pen-to-square"></i> Revizyon
                </button>
                <button class="btn btn-danger btn-xs" onclick="handleDirectDecision('${escapeAttr(app.protocolNumber)}', 'Rejected')">
                  <i class="fa-solid fa-xmark"></i> Reddet
                </button>
              </div>
            </td>
          `;
          pendingTbody.appendChild(tr);
        }
      }
    }
  } catch (e) {
    console.error(e);
  }
}

async function handleDirectDecision(protocolNumber, finalDecision) {
  try {
    let rationale;
    if (finalDecision === 'Approved') {
      rationale = 'Etik Kurul Başkanlığı ve kurul üyelerinin değerlendirmesi neticesinde araştırma protokolünün bilimsel ve etik ilkelere uygun olduğuna oybirliği ile karar verilmiştir.';
    } else if (finalDecision === 'RevisionNeeded') {
      rationale = 'Kurul incelemesi sonucunda araştırma protokolünde ve aydınlatma metninde düzeltme (revizyon) yapılmasına karar verilmiştir.';
    } else {
      rationale = 'Araştırma protokolünün mevcut haliyle etik ilkelere ve gönüllü güvenliği kriterlerine uygun olmadığına karar verilmiştir.';
    }

    const dec = await window.api.finalizeDecision({
      protocolNumber,
      finalDecision,
      summaryRationale: rationale
    });

    showToast(`✅ ${protocolNumber} için "${formatStatus(finalDecision)}" kararı (${dec.decisionNumber}) kesinleştirildi!`, 'success');
    await refreshAllViews();
  } catch (e) {
    showToast('Karar oluşturulurken hata: ' + e.message, 'error');
  }
}

async function viewCertificate(protocolNumber) {
  try {
    const res = await window.api.openCertificateWindow(protocolNumber);
    if (res && res.success === false) {
      showToast(res.message || 'Karar belgesi açılamadı.', 'error');
    }
  } catch (e) {
    showToast('Belge açılırken hata: ' + e.message, 'error');
  }
}

function verifyFromDecision(verificationCode) {
  switchTab('tab-verify');
  const input = document.getElementById('verifyCodeInput');
  if (input) {
    input.value = verificationCode;
    handleVerifyDocument();
  }
}

// 6. DOĞRULAMA
async function loadQuickVerifyCodes() {
  const box = document.getElementById('quickVerifyCodesBox');
  if (!box || !window.api.getDecisions) return;

  try {
    const decisions = await window.api.getDecisions();
    if (!decisions || decisions.length === 0) {
      box.innerHTML = '';
      return;
    }

    const pills = decisions
      .map(
        d => `
        <span class="code-pill" onclick="selectVerifyCode('${escapeAttr(d.verificationCode)}')">
          <i class="fa-solid fa-key"></i> <strong>${escapeHtml(d.protocolNumber)}:</strong> ${escapeHtml(d.verificationCode)}
        </span>`
      )
      .join(' ');

    box.innerHTML = `
      <div style="background:#f8fafc; border:1px dashed #cbd5e1; padding:10px 14px; border-radius:6px;">
        <div style="font-size:11.5px; color:#475569; margin-bottom:6px; font-weight:600;">
          <i class="fa-solid fa-bolt"></i> Sistemde Kayıtlı Karar Belgeleri (Sorgulamak için koda tıklayın):
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px;">${pills}</div>
      </div>
    `;
  } catch (e) {
    console.error(e);
  }
}

function selectVerifyCode(code) {
  const input = document.getElementById('verifyCodeInput');
  if (input) {
    input.value = code;
    handleVerifyDocument();
  }
}

async function handleVerifyDocument() {
  const code = document.getElementById('verifyCodeInput').value.trim();
  if (!code) {
    showToast('Lütfen 24 haneli doğrulama kodunu giriniz.', 'error');
    return;
  }

  const resultBox = document.getElementById('verifyResultBox');
  try {
    const res = await window.api.verifyCertificate(code);
    if (res.valid) {
      const badgeClass = getBadgeClass(res.finalDecision);
      resultBox.innerHTML = `
        <div style="background: #dcfce7; border: 1px solid #86efac; padding: 18px; border-radius: 8px; color: #166534;">
          <h4 style="margin-bottom: 8px;"><i class="fa-solid fa-circle-check"></i> RESMİ ETİK KURUL KARAR BELGESİ DOĞRULANDI</h4>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Protokol No:</strong> ${escapeHtml(res.protocolNumber)}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Karar No:</strong> ${escapeHtml(res.decisionNumber)}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Proje Başlığı:</strong> ${escapeHtml(res.projectTitle)}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Sorumlu Araştırmacı:</strong> ${escapeHtml(res.researcherName)}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Kurul Kararı:</strong> <span class="status-badge ${badgeClass}">${formatStatus(res.finalDecision)}</span></p>
          <p style="margin: 4px 0; font-size: 12px; color: #14532d;">Karar Tarihi: ${new Date(res.decidedAt).toLocaleDateString('tr-TR')}</p>
          <div style="margin-top: 10px;">
            <button class="btn btn-primary btn-sm" onclick="viewCertificate('${escapeAttr(res.protocolNumber)}')">
              <i class="fa-solid fa-file-pdf"></i> Belgeyi Görüntüle
            </button>
          </div>
        </div>
      `;
    } else {
      resultBox.innerHTML = `
        <div style="background: #fee2e2; border: 1px solid #fca5a5; padding: 18px; border-radius: 8px; color: #991b1b;">
          <h4><i class="fa-solid fa-triangle-exclamation"></i> DOĞRULAMA BAŞARISIZ</h4>
          <p style="font-size: 13px; margin-top: 6px;">Girilen kod ile sistemde eşleşen resmi bir etik kurul kararı bulunamadı. Lütfen kodu kontrol ediniz.</p>
        </div>
      `;
    }
  } catch (e) {
    showToast('Doğrulama hatası: ' + e.message, 'error');
  }
}

// Yardımcı Fonksiyonlar
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(str) {
  if (str === null || str === undefined) return '';
  return String(str).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function getBadgeClass(status) {
  if (status === 'Approved') return 'badge-approved';
  if (status === 'RevisionNeeded' || status === 'RevisionRequested') return 'badge-revision';
  if (status === 'Rejected') return 'badge-rejected';
  if (status === 'UnderReview') return 'badge-underreview';
  return 'badge-submitted';
}

function formatStatus(status) {
  const map = {
    Draft: 'Taslak',
    Submitted: 'Başvuruldu',
    UnderReview: 'İncelemede',
    RevisionNeeded: 'Düzeltme İsteniyor',
    RevisionRequested: 'Revizyon Talep Edildi',
    Approved: 'ONAYLANDI',
    Rejected: 'REDDEDİLDİ'
  };
  return map[status] || status;
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> ${escapeHtml(message)}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}
