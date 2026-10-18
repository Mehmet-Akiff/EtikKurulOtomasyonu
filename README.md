# 🏛️ Etik Kurul Otomasyonu (Ethics Committee Automation System)

Akademik araştırma, tez ve projeler için etik kurul onay sürecini dijitalleştiren; başvuru formlarının ve evraklarının iletilmesinden kurul üyelerine otomatik dosya atamasına, revizyon takiplerinden QR kodlu resmi karar belgesi üretimine kadar tüm süreci yöneten **çok modüllü hibrit mimari** otomasyon yazılımıdır.

---

## 📌 Mimari ve Kullanılan Teknolojiler

Sistem, kullanıcının talepleri doğrultusunda **3 ayrı teknoloji yığını** ile **modüler olarak** (her işlev bağımsız kendi modülünde) tasarlanmıştır:

```
EtikKurulOtomasyonu/
│
├── 1-BasvuruModulu_DotNet/            # [1] ASP.NET Core (.NET 9) + MSSQL
│   ├── Controllers/                   # ApplicationsController, ResearchersController, DocumentsController
│   ├── Data/                          # ApplicationDbContext, MSSQL & Seeder
│   ├── Models/                        # Application, Researcher, ApplicationDocument, ApplicationStatus
│   ├── Services/                      # ApplicationService (Protokol No Üretici, Evrak Doğrulama)
│   ├── DTOs/                          # Request & Response Veri Modelleri
│   └── Program.cs                     # API Başlatıcı & DI Yapılandırması (Port: 5001)
│
├── 2-DegerlendirmeModulu_PHP/         # [2] PHP 8+ + MySQL
│   ├── config/                        # database.php (MySQL PDO bağlantısı & Fallback)
│   ├── database/                      # schema.sql (Tablolar ve Örnek Kurul Üyeleri)
│   ├── models/                        # CommitteeMember, Assignment, Evaluation
│   ├── services/                      # AutoAssignmentService (Akıllı Otomatik Dosya Dağıtım Motoru)
│   ├── controllers/                   # AssignmentController, EvaluationController
│   ├── views/                         # evaluation_form.html (Kurul Üyesi Değerlendirme Web Portalı)
│   └── index.php                      # REST API & Web Portalı Yönlendiricisi (Port: 5002)
│
├── 3-KararVeBelgeModulu_Node/         # [3] Node.js (Express) + MongoDB
│   ├── src/config/                    # db.js (Mongoose MongoDB Bağlantısı & Fallback)
│   ├── src/models/                    # Decision.js, RevisionRequest.js, AuditLog.js
│   ├── src/services/                  # decisionService.js, certificateGenerator.js (QR Kodlu Belge Motoru)
│   ├── src/controllers/               # decisionController.js, revisionController.js
│   ├── src/routes/                    # apiRoutes.js
│   └── src/server.js                  # Express Sunucusu & Doğrulama Portalı (Port: 5003)
│
├── docker-compose.yml                 # MSSQL, MySQL, MongoDB ve 3 modülü tek seferde ayağa kaldıran yapı
├── start-all.ps1                      # Windows PowerShell ile tüm modülleri başlatan script
├── test-workflow.ps1                  # Uçtan uca tüm modülleri doğrulayan otomatik test betiği
└── README.md                          # Detaylı sistem dokümantasyonu
```

---

## 🚀 İşlevsel Modül Detayları

### 1) Başvuru & Belge Yönetimi Modülü (`1-BasvuruModulu_DotNet`)
- **Teknoloji:** ASP.NET Core 9 (Web API), Entity Framework Core, Microsoft SQL Server (MSSQL).
- **İşlevler:**
  - Araştırmacı kaydı ve profil yönetimi.
  - Tez (YL/Doktora), akademik araştırma ve kurumsal proje başvurularının dijital form ile toplanması.
  - Dijital evrak yükleme (Araştırma Protokolü, Bilgilendirilmiş Onam Formu, Veri Toplama Ölçekleri).
  - Benzersiz Başvuru Protokol Numarası üretimi (`ETIK-YYYY-XXXXX`).
  - Başvuru yaşam döngüsü durumu yönetimi (`Draft`, `Submitted`, `UnderReview`, `RevisionRequested`, `Approved`, `Rejected`).
- **Önemli Uç Noktalar:**
  - `POST /api/researchers` -> Araştırmacı kaydı
  - `POST /api/applications` -> Yeni başvuru oluşturma
  - `POST /api/applications/{id}/documents` -> Belge yükleme
  - `POST /api/applications/{id}/submit` -> Başvuruyu onaya sunma

---

### 2) Kurul Üyeleri & Otomatik Dosya Atama Modülü (`2-DegerlendirmeModulu_PHP`)
- **Teknoloji:** PHP 8+, MySQL (PDO), Bootstrap 5 Arayüzü.
- **İşlevler:**
  - Etik Kurul üyeleri yönetimi (Unvan, Uzmanlık Alanı, Aktif Dosya Yükü).
  - **Akıllı Otomatik Dosya Dağıtımı (Auto-Assignment Algorithm):**
    - Başvurunun araştırma konusu (Örn: Tıp, Klinik Psikoloji, Hukuk, Eğitim) ile kurul üyelerinin uzmanlık alanını eşleştirir.
    - Eşleşen üyeler arasında aktif dosya sayısı en az olan raportörleri (yük dengeleme) belirleyerek dosyayı 2 veya 3 raportöre otomatik atar.
  - Kurul Üyeleri İnceleme & Değerlendirme Portalı (`views/evaluation_form.html`):
    - 3 temel etik kriter puanlaması (1-5 arası: Metodoloji, Onam Formu, Risk Analizi).
    - Karar bildirme: `Approved` (Onay), `RevisionNeeded` (Revizyon), `Rejected` (Ret).
    - Detaylı gerekçe ve görüş notu girişi.
- **Önemli Uç Noktalar:**
  - `GET /` -> Web Değerlendirme Portalı
  - `POST /api/assignments/auto-assign` -> Otomatik jüri dağıtımı yapma
  - `GET /api/assignments/member/{id}` -> Üyenin üzerindeki bekleyen dosyalar
  - `POST /api/evaluations` -> Üye değerlendirmesini kaydetme
  - `GET /api/evaluations/summary/{protocol}` -> Başvuruya ait tüm üye değerlendirmeleri özeti

---

### 3) Karar, Revizyon & Otomatik Karar Belgesi Modülü (`3-KararVeBelgeModulu_Node`)
- **Teknoloji:** Node.js (Express), MongoDB (Mongoose), QRCode Motoru.
- **İşlevler:**
  - **Revizyon Talepleri Takibi:** Kurul raporlarını harmanlayarak araştırmacıya iletilecek düzeltme maddelerini, son teslim tarihini (`deadline`) ve revizyon döngüsünü yönetir.
  - **Nihai Karar Verme:** Jüri değerlendirme puan ve görüşlerini kesinleştirir, resmi karar numarası (`KARAR-YYYY-XXXX`) üretir.
  - **Otomatik Resmi Karar Belgesi (Decision Certificate) Üretimi:**
    - Onaylanan veya reddedilen başvurular için resmi formatta, protokol numaralı, tarihli, karar özeti ve gerekçesini içeren resmi HTML / PDF-ready karar belgesi üretir.
    - Belge üzerine **dinamik karekod (QR Kod)** ve 24 haneli kriptografik doğrulama kodu (`verificationCode`) yerleştirir.
  - **Denetim İzi (Audit Log):** Sistemdeki her işlemi NoSQL esnek doküman yapısında zaman damgalı olarak arşivler.
- **Önemli Uç Noktalar:**
  - `POST /api/revisions/request` -> Revizyon talep etme
  - `POST /api/decisions/finalize` -> Karar kesinleştirme ve resmi belge üretme
  - `GET /api/decisions/{protocol}/certificate` -> Resmi Karar Belgesini görüntüleme (HTML + QR)
  - `GET /api/verify/{code}` -> Belge doğrulama sorgusu
  - `GET /api/audit/{protocol}` -> Denetim izi geçmişi

---

## 💻 Çalıştırma Yöntemleri

### Yöntem 1: Yerel Olarak Başlatma (Windows PowerShell)

Tüm modülleri tek komutla aynı anda başlatmak için proje ana dizininde:

```powershell
.\start-all.ps1
```

Bu script:
- Port 5001'de ASP.NET Core servisini,
- Port 5002'de PHP portalını,
- Port 5003'te Node.js karar servisini ayağa kaldırır.

### Yöntem 2: Docker Compose ile Başlatma

Veritabanları (MSSQL, MySQL, MongoDB) ve 3 servisi tam yalıtımlı konteyner olarak başlatmak için:

```bash
docker-compose up -d
```

---

## 🧪 Uçtan Uca Doğrulama ve Testler

Tüm modüllerin birim ve entegrasyon testlerini tek seferde çalıştırmak için:

```powershell
.\test-workflow.ps1
```

Bu test şunları sırayla icra eder:
1. `dotnet test` ile ASP.NET Core başvuru ve belge iş mantığını test eder.
2. `php tests/AutoAssignmentTest.php` ile akıllı otomatik atama motorunu ve üye değerlendirmelerini test eder.
3. `node tests/decision.test.js` ile karar kesinleştirme, QR kodlu karar belgesi üretimini ve doğrulama kodunu test eder.

---

## 🖥️ 4) Windows Masaüstü Uygulaması (.EXE)

Microsoft Store kalitesinde, modern Windows 11 Fluent arayüzlü ve bağımsız (sıfır ön kurulum gerektiren) masaüstü sürümü:

- **Konum:** `4-MasaustuUygulamasi/dist/`
  - 📦 **Kurulumlu Sürüm (Setup):** `Etik Kurul Otomasyonu Setup 1.0.0.exe` (Masaüstü kısayolu, Başlat menüsü ve kaldırma desteği)
  - 🚀 **Taşınabilir Sürüm (Portable):** `EtikKurulOtomasyonu-Portable.exe` (Kurulumsuz, çift tıkla her Windows bilgisayarda anında çalışır)

Masaüstü uygulamasını yeniden derlemek için:
```bash
cd 4-MasaustuUygulamasi
npm run build:exe
```

