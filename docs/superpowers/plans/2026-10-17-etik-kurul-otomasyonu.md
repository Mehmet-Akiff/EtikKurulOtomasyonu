# Etik Kurul Otomasyonu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Akademik araştırma, tez ve projeler için etik kurul onay sürecini yöneten, 3 farklı modül/teknoloji (ASP.NET Core + MSSQL, PHP + MySQL, Node.js + MongoDB) ile çalışan modüler Etik Kurul Otomasyonu sistemini hayata geçirmek.

**Architecture:** Çok katmanlı hibrit modüler mimari. Başvuru ve dosya yönetimi ASP.NET Core (.NET 9) ve MSSQL üzerinde; jüri/kurul üyeleri yönetimi, otomatik dosya atama ve üye değerlendirmeleri PHP ve MySQL üzerinde; revizyon takibi, nihai kurul kararları ve otomatik resmi karar belgesi (PDF/HTML) üretimi Node.js (Express) ve MongoDB üzerinde konumlandırılmıştır. Modüller REST/JSON ile entegredir.

**Tech Stack:** ASP.NET Core 9 (C#, Entity Framework Core, MSSQL), PHP 8+ (PDO, MySQL), Node.js (Express, Mongoose, MongoDB), Docker Compose, PowerShell.

**Spec:** `docs/superpowers/specs/2026-10-17-etik-kurul-otomasyonu-design.md`

## Global Constraints
- Her işlev kendi bağımsız modül dizininde yer almalıdır.
- Kullanıcı direktifindeki tüm teknolojiler (ASP.NET Core + MSSQL, PHP + MySQL, Node.js + MongoDB) eksiksiz ve fazlasız kullanılmalıdır.
- Veritabanı bağlantıları yapılandırılabilir olmalı ve yerel testler için SQLite/In-Memory yedekleri ile kolay çalıştırılabilmelidir.
- Tüm kodlar test edilebilir ve çalışır durumda olmalıdır.

---

### Task 1: Modül 1 - ASP.NET Core + MSSQL Başvuru ve Belge Yönetimi Modülü

**Files:**
- Create: `1-BasvuruModulu_DotNet/EtikKurul.BasvuruModulu.csproj`
- Create: `1-BasvuruModulu_DotNet/Program.cs`
- Create: `1-BasvuruModulu_DotNet/appsettings.json`
- Create: `1-BasvuruModulu_DotNet/Models/Application.cs`
- Create: `1-BasvuruModulu_DotNet/Models/Researcher.cs`
- Create: `1-BasvuruModulu_DotNet/Models/ApplicationDocument.cs`
- Create: `1-BasvuruModulu_DotNet/Data/ApplicationDbContext.cs`
- Create: `1-BasvuruModulu_DotNet/DTOs/ApplicationDtos.cs`
- Create: `1-BasvuruModulu_DotNet/Services/IApplicationService.cs`
- Create: `1-BasvuruModulu_DotNet/Services/ApplicationService.cs`
- Create: `1-BasvuruModulu_DotNet/Controllers/ApplicationsController.cs`
- Create: `1-BasvuruModulu_DotNet/Controllers/DocumentsController.cs`
- Test: `1-BasvuruModulu_DotNet/Tests/ApplicationServiceTests.cs`

**Interfaces:**
- Produces: 
  - `POST /api/applications` -> Yeni başvuru oluşturma
  - `POST /api/applications/{id}/documents` -> Belge yükleme
  - `POST /api/applications/{id}/submit` -> Başvuruyu onaya sunma ve protokol numarası (`ETIK-YYYY-XXXXX`) üretme
  - `GET /api/applications/{id}` -> Başvuru detayını getirme

- [ ] **Step 1: ASP.NET Core projesini ve bağımlılıklarını oluştur**
- [ ] **Step 2: Varlık (Entity) ve DbContext modellerini yaz**
- [ ] **Step 3: Başvuru ve dosya servis katmanını geliştir (Protokol no üretici dahil)**
- [ ] **Step 4: API Controller'larını ekle**
- [ ] **Step 5: Birim testlerini yaz ve `dotnet test` ile doğrula**
- [ ] **Step 6: Git commit**

---

### Task 2: Modül 2 - PHP + MySQL Kurul Üyeleri, Otomatik Atama ve Değerlendirme Modülü

**Files:**
- Create: `2-DegerlendirmeModulu_PHP/config/database.php`
- Create: `2-DegerlendirmeModulu_PHP/database/schema.sql`
- Create: `2-DegerlendirmeModulu_PHP/models/CommitteeMember.php`
- Create: `2-DegerlendirmeModulu_PHP/models/Assignment.php`
- Create: `2-DegerlendirmeModulu_PHP/models/Evaluation.php`
- Create: `2-DegerlendirmeModulu_PHP/services/AutoAssignmentService.php`
- Create: `2-DegerlendirmeModulu_PHP/controllers/AssignmentController.php`
- Create: `2-DegerlendirmeModulu_PHP/controllers/EvaluationController.php`
- Create: `2-DegerlendirmeModulu_PHP/views/evaluation_form.html`
- Create: `2-DegerlendirmeModulu_PHP/index.php`
- Test: `2-DegerlendirmeModulu_PHP/tests/AutoAssignmentTest.php`

**Interfaces:**
- Consumes: Başvuru verisi (Protokol no, Araştırma alanı/konusu, Araştırmacı bilgisi)
- Produces:
  - `POST /api/assignments/auto-assign` -> Uzmanlık ve yük dengesine göre üyeleri otomatik atama
  - `POST /api/evaluations` -> Üyenin görüş, puan ve kararını kaydetme
  - `GET /api/evaluations/summary/{protocolNumber}` -> Başvuruya ait tüm değerlendirmelerin özeti

- [ ] **Step 1: MySQL veritabanı şemasını ve PDO bağlantı sınıfını oluştur**
- [ ] **Step 2: Model sınıflarını (CommitteeMember, Assignment, Evaluation) yaz**
- [ ] **Step 3: Otomatik dosya dağıtımı algoritmasını (AutoAssignmentService) geliştir**
- [ ] **Step 4: Değerlendirme ve atama controller'ları ile REST yönlendiriciyi yaz**
- [ ] **Step 5: Otomatik atama mantığı testlerini çalıştır ve doğrula**
- [ ] **Step 6: Git commit**

---

### Task 3: Modül 3 - Node.js + MongoDB Karar, Revizyon ve Otomatik Belge Üretimi

**Files:**
- Create: `3-KararVeBelgeModulu_Node/package.json`
- Create: `3-KararVeBelgeModulu_Node/src/config/db.js`
- Create: `3-KararVeBelgeModulu_Node/src/models/Decision.js`
- Create: `3-KararVeBelgeModulu_Node/src/models/RevisionRequest.js`
- Create: `3-KararVeBelgeModulu_Node/src/models/AuditLog.js`
- Create: `3-KararVeBelgeModulu_Node/src/services/decisionService.js`
- Create: `3-KararVeBelgeModulu_Node/src/services/certificateGenerator.js`
- Create: `3-KararVeBelgeModulu_Node/src/controllers/decisionController.js`
- Create: `3-KararVeBelgeModulu_Node/src/controllers/revisionController.js`
- Create: `3-KararVeBelgeModulu_Node/src/templates/decision_certificate.html`
- Create: `3-KararVeBelgeModulu_Node/src/routes/apiRoutes.js`
- Create: `3-KararVeBelgeModulu_Node/src/server.js`
- Test: `3-KararVeBelgeModulu_Node/tests/certificate.test.js`

**Interfaces:**
- Consumes: Modül 2'den gelen değerlendirme puanları ve görüşleri
- Produces:
  - `POST /api/revisions/request` -> Araştırmacıdan revizyon talep etme
  - `POST /api/decisions/finalize` -> Nihai kurul kararını (Onay/Ret/Revizyon) verme
  - `GET /api/decisions/{protocolNumber}/certificate` -> Otomatik resmi karar belgesini (HTML/PDF formatında, QR ve doğrulama kodlu) indirme/görüntüleme

- [ ] **Step 1: Node.js projesi `package.json` ve Mongoose şemalarını oluştur**
- [ ] **Step 2: Karar ve Revizyon iş mantığı servislerini yaz**
- [ ] **Step 3: Resmi Karar Belgesi (Decision Certificate) üretim motorunu geliştir**
- [ ] **Step 4: Express controller ve API rotalarını tamamla**
- [ ] **Step 5: Belge üretimi ve karar motoru testlerini çalıştır ve doğrula**
- [ ] **Step 6: Git commit**

---

### Task 4: Entegrasyon, Orkestrasyon ve Uçtan Uca Doğrulama

**Files:**
- Create: `docker-compose.yml`
- Create: `start-all.ps1`
- Create: `test-workflow.ps1`
- Create: `README.md`

- [ ] **Step 1: `docker-compose.yml` dosyasını oluştur (MSSQL, MySQL, MongoDB ve 3 servis)**
- [ ] **Step 2: Windows PowerShell başlatıcı betiğini (`start-all.ps1`) hazırla**
- [ ] **Step 3: Uçtan uca akışı test eden otomasyon betiğini (`test-workflow.ps1`) yaz**
- [ ] **Step 4: Kapsamlı sistem ve kullanım dokümantasyonunu (`README.md`) hazırla**
- [ ] **Step 5: Tüm testleri çalıştırıp doğrula ve Git commit yap**
