# Masaüstü Uygulaması (.EXE) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Etik Kurul Otomasyonu için Microsoft Store kalitesinde, sıfır bağımlılıkla çalışan Windows Masaüstü Uygulaması (.exe) geliştirmek ve hem Kurulumlu (Setup .exe) hem de Taşınabilir (Portable .exe) olarak paketlemek.

**Architecture:** Electron 34+ tabanlı modern Windows masaüstü kabuğu. İçerisinde başvuru, otomatik atama, değerlendirme ve QR kodlu karar belgesi üretme motorlarını barındıran gömülü veri katmanı (embedded store & workflow). Çıktı olarak `electron-builder` ile Windows NSIS Setup ve Portable EXE üretimi.

**Tech Stack:** Electron, Node.js, HTML5/CSS3 (Windows 11 Fluent UI), electron-builder, QRCode, Cryptography.

**Spec:** `docs/superpowers/specs/2026-10-18-desktop-app-design.md`

---

### Task 1: Masaüstü Uygulaması Çekirdeği ve Gömülü Motorun Oluşturulması
**Files:**
- Create: `4-MasaustuUygulamasi/package.json`
- Create: `4-MasaustuUygulamasi/src/engine/embeddedStore.js`
- Create: `4-MasaustuUygulamasi/src/engine/embeddedWorkflow.js`
- Create: `4-MasaustuUygulamasi/src/engine/certificateEngine.js`
- Create: `4-MasaustuUygulamasi/src/main.js`
- Create: `4-MasaustuUygulamasi/src/preload.js`
- Test: `4-MasaustuUygulamasi/tests/engine.test.js`

- [ ] **Step 1: `package.json` ve bağımlılıkları tanımla**
- [ ] **Step 2: Gömülü veri saklama ve iş akışı motorunu (embeddedStore & embeddedWorkflow) yaz**
- [ ] **Step 3: QR kodlu resmi karar belgesi üretim motorunu (certificateEngine) entegre et**
- [ ] **Step 4: Electron ana işlemcisi (`main.js`) ve IPC köprüsünü (`preload.js`) yaz**
- [ ] **Step 5: Gömülü motor testlerini çalıştır ve doğrula**

---

### Task 2: Modern Windows 11 Fluent UI Arayüzü
**Files:**
- Create: `4-MasaustuUygulamasi/src/ui/index.html`
- Create: `4-MasaustuUygulamasi/src/ui/styles.css`
- Create: `4-MasaustuUygulamasi/src/ui/app.js`

- [ ] **Step 1: Sekmeli modern Fluent UI arayüzünü (HTML) tasarla**
- [ ] **Step 2: Windows 11 Fluent tasarım CSS'ini yaz (Mica/Acrylic efekti, kartlar, formlar)**
- [ ] **Step 3: Dinamik JavaScript kontrolcüsünü (app.js) bağla (Başvuru, Atama, Puanlama, Belge)**

---

### Task 3: Simge & electron-builder ile EXE Paketleme (Setup & Portable)
**Files:**
- Create: `4-MasaustuUygulamasi/build/icon.png`
- Create: `4-MasaustuUygulamasi/build/icon.ico`
- Output: `4-MasaustuUygulamasi/dist/EtikKurulOtomasyonu Setup 1.0.0.exe`
- Output: `4-MasaustuUygulamasi/dist/EtikKurulOtomasyonu-Portable.exe`

- [ ] **Step 1: Uygulama simgesini hazırla**
- [ ] **Step 2: electron-builder yapılandırmasını NSIS ve Portable olarak tamamla**
- [ ] **Step 3: `npm run build:exe` komutunu çalıştırarak EXE paketlerini üret**
- [ ] **Step 4: Üretilen EXE dosyalarını ve boyutlarını doğrula**

---

### Task 4: GitHub Yüklemesi & Dokümantasyon Güncellemesi
- [ ] **Step 1: Masaüstü uygulamasını proje ana dokümanına (`README.md`) ekle**
- [ ] **Step 2: Git commit ve GitHub push hazırlığı**
