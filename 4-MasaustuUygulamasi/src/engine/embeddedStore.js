// src/engine/embeddedStore.js - Masaüstü Uygulaması Yerel Veri Saklama Motoru

const fs = require('fs');
const path = require('path');

class EmbeddedStore {
  constructor(storageDir) {
    this.storageDir = storageDir || path.join(__dirname, '..', '..', 'data');
    if (!fs.existsSync(this.storageDir)) {
      fs.mkdirSync(this.storageDir, { recursive: true });
    }
    this.dbPath = path.join(this.storageDir, 'etikkurul_local.json');
    this.data = this.load();
  }

  load() {
    if (fs.existsSync(this.dbPath)) {
      try {
        return JSON.parse(fs.readFileSync(this.dbPath, 'utf8'));
      } catch (e) {
        console.error('[Store] Veri okuma hatası, varsayılan şema oluşturuluyor:', e);
      }
    }
    return this.getInitialSchema();
  }

  save() {
    try {
      fs.writeFileSync(this.dbPath, JSON.stringify(this.data, null, 2), 'utf8');
    } catch (e) {
      console.error('[Store] Veri kaydetme hatası:', e);
    }
  }

  getInitialSchema() {
    return {
      researchers: [
        {
          id: 1,
          fullName: 'Dr. Deniz Kaya',
          email: 'deniz.kaya@universite.edu.tr',
          title: 'Dr. Öğr. Üyesi',
          department: 'Bilgisayar Mühendisliği',
          institution: 'Teknik Üniversite',
          phoneNumber: '+90 555 123 4567'
        },
        {
          id: 2,
          fullName: 'Araş. Gör. Zeynep Çelik',
          email: 'zeynep.celik@universite.edu.tr',
          title: 'Araştırma Görevlisi (Doktora Adayı)',
          department: 'Klinik Psikoloji',
          institution: 'Devlet Üniversitesi',
          phoneNumber: '+90 555 987 6543'
        }
      ],
      committeeMembers: [
        { id: 1, fullName: 'Prof. Dr. Selim Vural', title: 'Prof. Dr.', fieldOfExpertise: 'Tıp / Biyomedikal', email: 'selim.vural@universite.edu.tr', activeFileCount: 0, isActive: true },
        { id: 2, fullName: 'Doç. Dr. Ayşe Gündüz', title: 'Doç. Dr.', fieldOfExpertise: 'Klinik Psikoloji', email: 'ayse.gunduz@universite.edu.tr', activeFileCount: 0, isActive: true },
        { id: 3, fullName: 'Prof. Dr. Kerem Yaman', title: 'Prof. Dr.', fieldOfExpertise: 'Sosyal Bilimler / Hukuk', email: 'kerem.yaman@universite.edu.tr', activeFileCount: 0, isActive: true },
        { id: 4, fullName: 'Doç. Dr. Emre Karaca', title: 'Doç. Dr.', fieldOfExpertise: 'Eğitim Bilimleri', email: 'emre.karaca@universite.edu.tr', activeFileCount: 0, isActive: true },
        { id: 5, fullName: 'Dr. Öğr. Üyesi Burcu Polat', title: 'Dr. Öğr. Üyesi', fieldOfExpertise: 'Biyomedikal / Genetik', email: 'burcu.polat@universite.edu.tr', activeFileCount: 0, isActive: true },
        { id: 6, fullName: 'Prof. Dr. Murat Doğan', title: 'Prof. Dr.', fieldOfExpertise: 'Tıp / Dahili Bilimler', email: 'murat.dogan@universite.edu.tr', activeFileCount: 0, isActive: true }
      ],
      applications: [
        {
          id: 1,
          protocolNumber: 'ETIK-2026-00001',
          researcherId: 1,
          researcherName: 'Dr. Deniz Kaya',
          researcherEmail: 'deniz.kaya@universite.edu.tr',
          projectTitle: 'Yapay Zeka Destekli Biyosensörlerin Etik İncelemesi',
          researchType: 'Akademik Araştırma',
          fieldOfStudy: 'Tıp / Biyomedikal',
          abstract: 'Giyilebilir biyosensör verilerinin hasta mahremiyeti ve etik standartlar açısından değerlendirilmesi.',
          methodology: 'Çift kör klinik anket ve laboratuvar testleri.',
          targetAudience: 'Yetişkin gönüllüler (18-65 yaş)',
          volunteerCount: 120,
          riskLevel: 'Düşük',
          status: 'Submitted',
          submittedAt: new Date().toISOString(),
          documents: [
            { id: 1, documentType: 'Araştırma Protokolü', fileName: 'arastirma_protokolu.pdf', uploadDate: new Date().toISOString() },
            { id: 2, documentType: 'Bilgilendirilmiş Onam Formu', fileName: 'onam_formu.pdf', uploadDate: new Date().toISOString() }
          ]
        }
      ],
      assignments: [],
      evaluations: [],
      decisions: [],
      revisions: [],
      auditLogs: []
    };
  }
}

module.exports = EmbeddedStore;
