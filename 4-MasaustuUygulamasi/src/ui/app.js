// src/ui/app.js - Masaüstü Arayüz Kontrolcüsü ve Reaktif İş Akışı

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  loadDashboard();
  loadResearchers();
  loadUnassignedList();
  loadMembersLoadList();
  loadAssignmentsForEval();
  loadDecisions();
});

// Sekme Yönetimi
function setupTabs() {
  const navItems = document.querySelectorAll('.nav-item');
  const tabs = document.querySelectorAll('.content-tab');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTabId = item.getAttribute('data-tab');
      navItems.forEach(n => n.classList.remove('active'));
      tabs.forEach(t => t.classList.remove('active'));

      item.classList.add('active');
      const targetTab = document.getElementById(targetTabId);
      if (targetTab) targetTab.classList.add('active');

      // Sekmeye özel veri tazeleme
      if (targetTabId === 'tab-dashboard') loadDashboard();
      if (targetTabId === 'tab-assignment') { loadUnassignedList(); loadMembersLoadList(); }
      if (targetTabId === 'tab-evaluation') loadAssignmentsForEval();
      if (targetTabId === 'tab-decision') loadDecisions();
    });
  });
}

// 1. DASHBOARD
async function loadDashboard() {
  try {
    const apps = await window.api.getApplications();
    const members = await window.api.getCommitteeMembers();

    document.getElementById('statTotalApps').innerText = apps.length;
    document.getElementById('statUnderReview').innerText = apps.filter(a => a.status === 'UnderReview' || a.status === 'Submitted').length;
    document.getElementById('statApproved').innerText = apps.filter(a => a.status === 'Approved').length;
    document.getElementById('statMembers').innerText = members.length;

    const tbody = document.getElementById('dashboardTableBody');
    tbody.innerHTML = '';

    if (apps.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:#888;">Henüz kayıtlı başvuru bulunmamaktadır.</td></tr>';
      return;
    }

    apps.forEach(a => {
      const tr = document.createElement('tr');
      const badgeClass = getBadgeClass(a.status);
      const dateStr = a.submittedAt ? new Date(a.submittedAt).toLocaleDateString('tr-TR') : '-';

      tr.innerHTML = `
        <td><strong>${a.protocolNumber}</strong></td>
        <td>${a.projectTitle}</td>
        <td>${a.researcherName}</td>
        <td><small class="text-muted">${a.fieldOfStudy}</small></td>
        <td><span class="status-badge ${badgeClass}">${formatStatus(a.status)}</span></td>
        <td>${dateStr}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    showToast('Dashboard verisi yüklenirken hata: ' + e.message, 'error');
  }
}

// 2. YENİ BAŞVURU
async function loadResearchers() {
  try {
    const researchers = await window.api.getResearchers();
    const sel = document.getElementById('appResearcherSelect');
    sel.innerHTML = '<option value="">Araştırmacı Seçiniz...</option>';
    researchers.forEach(r => {
      sel.innerHTML += `<option value="${r.id}">${r.title} ${r.fullName} (${r.department} - ${r.institution})</option>`;
    });
  } catch (e) {
    console.error(e);
  }
}

async function handleCreateApplication(event) {
  event.preventDefault();
  const researcherId = document.getElementById('appResearcherSelect').value;
  const projectTitle = document.getElementById('appProjectTitle').value;
  const researchType = document.getElementById('appResearchType').value;
  const fieldOfStudy = document.getElementById('appFieldOfStudy').value;
  const volunteerCount = document.getElementById('appVolunteerCount').value;
  const riskLevel = document.getElementById('appRiskLevel').value;
  const abstract = document.getElementById('appAbstract').value;
  const methodology = document.getElementById('appMethodology').value;

  try {
    const result = await window.api.createApplication({
      researcherId,
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
    document.querySelector('[data-tab="tab-assignment"]').click();
  } catch (e) {
    showToast('Başvuru gönderilirken hata: ' + e.message, 'error');
  }
}

// 3. OTOMATİK ATAMA
async function loadUnassignedList() {
  try {
    const apps = await window.api.getApplications();
    const assignments = await window.api.getAssignments();
    const assignedProtocols = assignments.map(a => a.protocolNumber);

    const unassigned = apps.filter(a => !assignedProtocols.includes(a.protocolNumber));
    const container = document.getElementById('unassignedList');
    container.innerHTML = '';

    if (unassigned.length === 0) {
      container.innerHTML = '<div style="color: #64748b; font-size: 13px; padding: 10px;">Atama bekleyen dosya bulunmuyor. Tüm başvurular raportörlere dağıtılmış.</div>';
      return;
    }

    unassigned.forEach(app => {
      const item = document.createElement('div');
      item.className = 'list-item-card';
      item.innerHTML = `
        <div>
          <div style="font-weight: 600; color: #1e3c72; font-size: 13.5px;">${app.protocolNumber} - ${app.projectTitle}</div>
          <div style="font-size: 11.5px; color: #64748b; margin-top: 4px;">
            Araştırmacı: ${app.researcherName} | Alan: <strong>${app.fieldOfStudy}</strong>
          </div>
        </div>
        <button class="btn btn-primary btn-sm" onclick="triggerAutoAssign('${app.protocolNumber}')">
          <i class="fa-solid fa-robot"></i> Otomatik Ata (2 Raportör)
        </button>
      `;
      container.appendChild(item);
    });
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
          <div style="font-weight: 600;">${m.title} ${m.fullName}</div>
          <div style="font-size: 11.5px; color: #64748b;">${m.fieldOfExpertise}</div>
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
      loadUnassignedList();
      loadMembersLoadList();
    } else {
      showToast(result.message || 'Atama tamamlanamadı.', 'error');
    }
  } catch (e) {
    showToast('Atama hatası: ' + e.message, 'error');
  }
}

// 4. DEĞERLENDİRME & PUANLAMA
async function loadAssignmentsForEval() {
  try {
    const assignments = await window.api.getAssignments();
    const pending = assignments.filter(a => a.status === 'Pending');
    const sel = document.getElementById('evalAssignmentSelect');
    sel.innerHTML = '<option value="">Bekleyen Atama Seçiniz...</option>';

    pending.forEach(a => {
      sel.innerHTML += `<option value="${a.id}" data-protocol="${a.protocolNumber}" data-member="${a.memberId}" data-title="${a.projectTitle} [${a.fieldOfStudy}]">
        ${a.protocolNumber} - ${a.memberTitle} ${a.memberName} (${a.projectTitle.substring(0, 35)}...)
      </option>`;
    });

    handleAssignmentSelectChange();
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
    showToast('Lütfen değerlendirilecek bir atama seçiniz.', 'error');
    return;
  }

  const assignmentId = opt.value;
  const protocolNumber = opt.getAttribute('data-protocol');
  const memberId = opt.getAttribute('data-member');
  const methodologyScore = document.getElementById('scoreMethodology').value;
  const consentFormScore = document.getElementById('scoreConsent').value;
  const riskAssessmentScore = document.getElementById('scoreRisk').value;
  const decision = document.getElementById('evalDecisionChoice').value;
  const feedbackNotes = document.getElementById('evalFeedbackNotes').value;

  try {
    await window.api.submitEvaluation({
      assignmentId,
      protocolNumber,
      memberId,
      methodologyScore,
      consentFormScore,
      riskAssessmentScore,
      decision,
      feedbackNotes
    });

    showToast('✅ Değerlendirme kaydedildi! Kurul kararına eklendi.', 'success');
    document.getElementById('evaluationForm').reset();
    loadAssignmentsForEval();

    // Eğer tüm raportörler puanladıysa otomatik karar kesinleştirmeyi tetikle
    const summary = await window.api.getEvaluationSummary(protocolNumber);
    if (summary.completedReviews >= summary.totalAssigned && summary.totalAssigned > 0) {
      await window.api.finalizeDecision({
        protocolNumber,
        finalDecision: summary.recommendation,
        summaryRationale: `Kurul üyelerinin oy birliği/çoğunluğu ile ${summary.recommendation === 'Approved' ? 'onaylanmıştır' : 'reddedilmiştir/revizyon istenmiştir'}. Ortalama Etik Puanı: ${summary.averageScore.toFixed(2)} / 5.00`
      });
      showToast(`🎉 ${protocolNumber} için nihai karar otomatik kesinleştirildi ve resmi belge oluşturuldu!`, 'success');
      document.querySelector('[data-tab="tab-decision"]').click();
    }
  } catch (e) {
    showToast('Değerlendirme kaydedilirken hata: ' + e.message, 'error');
  }
}

// 5. KARAR & BELGELER
async function loadDecisions() {
  try {
    const apps = await window.api.getApplications();
    const tbody = document.getElementById('decisionsTableBody');
    tbody.innerHTML = '';

    for (const app of apps) {
      const dec = await window.api.getDecision(app.protocolNumber);
      if (dec) {
        const tr = document.createElement('tr');
        const badgeClass = getBadgeClass(dec.finalDecision);
        tr.innerHTML = `
          <td><strong>${dec.decisionNumber}</strong></td>
          <td>${dec.protocolNumber}</td>
          <td>${dec.projectTitle}</td>
          <td>${dec.researcherName}</td>
          <td><span class="status-badge ${badgeClass}">${formatStatus(dec.finalDecision)}</span></td>
          <td><strong>${dec.averageScore ? dec.averageScore.toFixed(2) : '-'} / 5.0</strong></td>
          <td>
            <button class="btn btn-primary btn-sm" onclick="viewCertificate('${dec.protocolNumber}')">
              <i class="fa-solid fa-file-pdf"></i> Resmi Karar Belgesi (HTML/QR)
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }
    }

    if (tbody.children.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#888;">Henüz kesinleşmiş bir kurul kararı bulunmuyor.</td></tr>';
    }
  } catch (e) {
    console.error(e);
  }
}

async function viewCertificate(protocolNumber) {
  try {
    await window.api.openCertificateWindow(protocolNumber);
  } catch (e) {
    showToast('Belge açılırken hata: ' + e.message, 'error');
  }
}

// 6. DOĞRULAMA
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
      resultBox.innerHTML = `
        <div style="background: #dcfce7; border: 1px solid #86efac; padding: 18px; border-radius: 8px; color: #166534;">
          <h4 style="margin-bottom: 8px;"><i class="fa-solid fa-circle-check"></i> RESMİ ETİK KURUL KARAR BELGESİ DOĞRULANDI</h4>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Protokol No:</strong> ${res.protocolNumber}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Karar No:</strong> ${res.decisionNumber}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Proje Başlığı:</strong> ${res.projectTitle}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Sorumlu Araştırmacı:</strong> ${res.researcherName}</p>
          <p style="margin: 4px 0; font-size: 13px;"><strong>Kurul Kararı:</strong> <span class="status-badge badge-approved">${formatStatus(res.finalDecision)}</span></p>
          <p style="margin: 4px 0; font-size: 12px; color: #14532d;">Tarih: ${new Date(res.decidedAt).toLocaleDateString('tr-TR')}</p>
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
function getBadgeClass(status) {
  if (status === 'Approved') return 'badge-approved';
  if (status === 'RevisionNeeded' || status === 'RevisionRequested') return 'badge-revision';
  if (status === 'Rejected') return 'badge-rejected';
  if (status === 'UnderReview') return 'badge-underreview';
  return 'badge-submitted';
}

function formatStatus(status) {
  const map = {
    'Draft': 'Taslak',
    'Submitted': 'Başvuruldu',
    'UnderReview': 'İncelemede',
    'RevisionNeeded': 'Düzeltme İsteniyor',
    'RevisionRequested': 'Revizyon Talep Edildi',
    'Approved': 'ONAYLANDI',
    'Rejected': 'REDDEDİLDİ'
  };
  return map[status] || status;
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}
