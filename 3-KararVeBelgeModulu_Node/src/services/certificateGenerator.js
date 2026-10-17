// src/services/certificateGenerator.js - Otomatik Resmi Karar Belgesi (Decision Certificate) Üretici

const QRCode = require('qrcode');
const crypto = require('crypto');

class CertificateGenerator {

  /**
   * Benzersiz kriptografik doğrulama kodu üretir.
   */
  static generateVerificationCode(protocolNumber, decisionNumber) {
    const seed = `${protocolNumber}:${decisionNumber}:${Date.now()}:${crypto.randomBytes(8).toString('hex')}`;
    return crypto.createHash('sha256').update(seed).digest('hex').substring(0, 24).toUpperCase();
  }

  /**
   * Karar verisine dayalı resmi, yüksek çözünürlüklü ve QR kodlu HTML/PDF belgesi üretir.
   */
  static async generateCertificateHtml(decisionData) {
    const {
      protocolNumber,
      decisionNumber,
      projectTitle,
      researcherName,
      researcherEmail,
      fieldOfStudy,
      finalDecision,
      summaryRationale,
      conditions = [],
      averageScore,
      decidedAt,
      committeeChair,
      memberVotes = [],
      verificationCode
    } = decisionData;

    const formattedDate = new Date(decidedAt || Date.now()).toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    // QR Kod içeriği (Resmi doğrulama URL'si)
    const verificationUrl = `https://etikkurul.universite.edu.tr/dogrula?kod=${verificationCode}&protokol=${protocolNumber}`;
    const qrDataUri = await QRCode.toDataURL(verificationUrl, {
      margin: 1,
      width: 140,
      color: {
        dark: '#1e3c72',
        light: '#ffffff'
      }
    });

    const isApproved = (finalDecision === 'Approved');
    const isRevision = (finalDecision === 'RevisionNeeded');

    const badgeColor = isApproved ? '#198754' : (isRevision ? '#ffc107' : '#dc3545');
    const badgeBg = isApproved ? '#d1e7dd' : (isRevision ? '#fff3cd' : '#f8d7da');
    const decisionTextTr = isApproved 
      ? 'ETİK AÇIDAN UYGUN BULUNMUŞTUR (ONAY)' 
      : (isRevision ? 'DÜZELTME / REVİZYON İSTENMESİNE KARAR VERİLMİŞTİR' : 'ETİK AÇIDAN UYGUN BULUNMAMIŞTIR (RET)');

    const conditionsListHtml = (conditions && conditions.length > 0)
      ? conditions.map(c => `<li>${c}</li>`).join('')
      : '<li>Araştırma boyunca Helsinki Bildirgesi ve ilgili mevzuat hükümlerine tam riayet edilmelidir.</li>';

    const signaturesHtml = memberVotes.map(v => `
      <div style="flex: 1; min-width: 180px; text-align: center; margin: 10px; border-top: 1px dashed #999; padding-top: 8px;">
        <div style="font-weight: bold; font-size: 13px; color: #333;">${v.memberName || 'Kurul Üyesi'}</div>
        <div style="font-size: 11px; color: #666;">${v.memberTitle || 'Raportör Üye'}</div>
        <div style="font-size: 10px; color: #198754; margin-top: 4px;">[e-İmzalıdır - ${new Date(v.votedAt || Date.now()).toLocaleDateString('tr-TR')}]</div>
      </div>
    `).join('');

    return `<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Resmi Etik Kurul Karar Belgesi - ${protocolNumber}</title>
    <style>
        @page { size: A4; margin: 15mm; }
        body {
            font-family: 'Times New Roman', Times, serif;
            color: #222;
            background: #fdfdfd;
            margin: 0;
            padding: 20px;
        }
        .cert-container {
            border: 3px double #1e3c72;
            padding: 35px 40px;
            background: #fff;
            max-width: 800px;
            margin: 0 auto;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            position: relative;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        .header h1 {
            margin: 0;
            font-size: 20px;
            letter-spacing: 1px;
            color: #1e3c72;
            text-transform: uppercase;
        }
        .header h2 {
            margin: 5px 0;
            font-size: 16px;
            color: #444;
            font-weight: normal;
        }
        .header h3 {
            margin: 5px 0 0 0;
            font-size: 14px;
            color: #666;
            text-decoration: underline;
        }
        .meta-table {
            width: 100%;
            margin-bottom: 20px;
            border-collapse: collapse;
            font-size: 13px;
        }
        .meta-table td {
            padding: 5px 8px;
            vertical-align: top;
        }
        .meta-table td.label {
            font-weight: bold;
            width: 25%;
            color: #333;
            background: #f8f9fa;
        }
        .decision-box {
            background-color: ${badgeBg};
            border: 2px solid ${badgeColor};
            border-radius: 6px;
            padding: 15px;
            text-align: center;
            margin: 25px 0;
        }
        .decision-title {
            font-size: 16px;
            font-weight: bold;
            color: ${badgeColor};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .content-section {
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 15px;
            text-align: justify;
        }
        .signatures {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin-top: 40px;
            padding-top: 15px;
        }
        .chair-section {
            text-align: center;
            margin: 30px auto 10px auto;
            width: 260px;
            border-top: 1px solid #1e3c72;
            padding-top: 8px;
        }
        .footer-verification {
            margin-top: 35px;
            border-top: 1px solid #ddd;
            padding-top: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            color: #666;
        }
        .qr-area {
            text-align: center;
        }
        .security-badge {
            background: #eef2ff;
            border: 1px solid #c7d2fe;
            border-radius: 4px;
            padding: 8px 12px;
            font-family: monospace;
            font-size: 11px;
            color: #1e3c72;
        }
        @media print {
            body { padding: 0; background: none; }
            .cert-container { box-shadow: none; border: 2px solid #000; }
        }
    </style>
</head>
<body>
    <div class="cert-container">
        <div class="header">
            <h1>T.C. ÜNİVERSİTE REKTÖRLÜĞÜ</h1>
            <h2>BİLİMSEL VE AKADEMİK ARAŞTIRMALAR ETİK KURULU</h2>
            <h3>ETİK KURUL RESMİ KARAR BELGESİ</h3>
        </div>

        <table class="meta-table" border="1" bordercolor="#e0e0e0">
            <tr>
                <td class="label">Protokol Numarası:</td>
                <td><strong>${protocolNumber}</strong></td>
                <td class="label">Karar Numarası:</td>
                <td><strong>${decisionNumber}</strong></td>
            </tr>
            <tr>
                <td class="label">Karar Tarihi:</td>
                <td>${formattedDate}</td>
                <td class="label">Etik Uygunluk Puanı:</td>
                <td>${averageScore ? averageScore.toFixed(2) + ' / 5.00' : 'Değerlendirildi'}</td>
            </tr>
            <tr>
                <td class="label">Sorumlu Araştırmacı:</td>
                <td colspan="3">${researcherName} (${researcherEmail || '-'})</td>
            </tr>
            <tr>
                <td class="label">Araştırma / Proje Başlığı:</td>
                <td colspan="3"><strong>${projectTitle}</strong></td>
            </tr>
            <tr>
                <td class="label">Araştırma Alanı:</td>
                <td colspan="3">${fieldOfStudy || 'Genel Akademik Araştırma'}</td>
            </tr>
        </table>

        <div class="decision-box">
            <div class="decision-title">${decisionTextTr}</div>
        </div>

        <div class="content-section">
            <strong>GEREKÇE VE KURUL GÖRÜŞÜ:</strong><br>
            ${summaryRationale}
        </div>

        ${isApproved ? `
        <div class="content-section">
            <strong>GEÇERLİLİK KOŞULLARI VE HÜKÜMLER:</strong>
            <ul style="margin-top: 5px; padding-left: 20px;">
                ${conditionsListHtml}
            </ul>
        </div>
        ` : ''}

        <div class="chair-section">
            <div style="font-weight: bold; font-size: 14px;">${committeeChair?.name || 'Prof. Dr. Selim Vural'}</div>
            <div style="font-size: 12px; color: #555;">${committeeChair?.title || 'Etik Kurul Başkanı'}</div>
            <div style="font-size: 11px; color: #198754; margin-top: 5px;">[Güvenli Elektronik İmza ile İmzalanmıştır]</div>
        </div>

        <div class="signatures">
            ${signaturesHtml}
        </div>

        <div class="footer-verification">
            <div>
                <div class="security-badge">
                    DOĞRULAMA KODU: ${verificationCode}
                </div>
                <div style="margin-top: 6px;">
                    Bu belge 5070 sayılı Elektronik İmza Kanunu kapsamında ıslak imza gerektirmeksizin dijital olarak üretilmiştir.<br>
                    Belge doğruluğu sağdaki QR kod okutularak veya doğrulama sistemi üzerinden sorgulanabilir.
                </div>
            </div>
            <div class="qr-area">
                <img src="${qrDataUri}" alt="Doğrulama QR Kodu" style="width: 100px; height: 100px;"><br>
                <span style="font-size: 9px; color: #777;">Karekod Doğrulama</span>
            </div>
        </div>
    </div>
</body>
</html>`;
  }
}

module.exports = CertificateGenerator;
