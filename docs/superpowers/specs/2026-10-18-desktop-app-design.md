# Etik Kurul Otomasyonu - Masaüstü Uygulaması (Desktop App) Tasarım Dokümanı

**Tarih:** 2026-10-18  
**Proje:** Etik Kurul Otomasyonu - Windows Masaüstü Uygulaması (.EXE Setup & Portable)  
**Hedef:** Son kullanıcılara ve kurul üyelerine bağımlılıksız (sıfır kurulum gerektiren), Microsoft Store kalitesinde modern bir masaüstü uygulaması sunmak.

---

## 1. Amaç ve Kapsam
Kullanıcının *"telefonda APK nasılsa bilgisayarda EXE, Microsoft Store'dan indirilmiş gibi her şeyi içinde olsun, başkasına doğrudan verebileyim"* talebi doğrultusunda:
- Hem **Kurulum Sihirbazı (Setup Installer .exe)**
- Hem de **Kurulumsuz Taşınabilir (Portable .exe)**
formatında, modern Windows 11 Fluent tasarımına sahip bağımsız bir masaüstü uygulaması geliştirilecektir.

---

## 2. Mimari Yapı (Electron + Embedded Engine + electron-builder)

```
4-MasaustuUygulamasi/
│
├── src/
│   ├── main.js                  # Electron ana işlemci, pencere yönetimi, menüler
│   ├── preload.js               # Güvenli IPC köprüsü (contextBridge)
│   ├── engine/                  # Bağımlılıksız gömülü servis ve veri yöneticisi
│   │   ├── embeddedStore.js     # Yerel SQLite / JSON veri saklama motoru
│   │   ├── embeddedWorkflow.js  # Başvuru, Otomatik Atama ve Karar motoru
│   │   └── certificateEngine.js # QR Kodlu Resmi Karar Belgesi üreticisi
│   │
│   └── ui/                      # Microsoft Store / Windows Fluent Tasarımlı Arayüz
│       ├── index.html           # Ana Dashboard ve Sekmeli Navigasyon
│       ├── app.js               # Dinamik UI etkileşimleri ve reaktif durum yönetimi
│       └── styles.css           # Fluent UI, koyu/açık tema, modern kartlar
│
├── build/
│   └── icon.ico                 # Uygulama simgesi (Etik Kurul terazisi & mühür)
├── package.json                 # electron & electron-builder konfigürasyonu
└── dist/                        # Üretilen EXE çıktıları:
    ├── EtikKurulOtomasyonu Setup 1.0.0.exe (Kurulumlu)
    └── EtikKurulOtomasyonu 1.0.0.exe (Portable / Taşınabilir)
```

---

## 3. Temel Özellikler
1. **Bağımsız Çalışma:** Hedef bilgisayarda Node.js, PHP, .NET veya veritabanı kurulu olmasa dahi tek tıkla çalışır.
2. **Birleşik Arayüz:**
   - 📋 **Başvuru Portalı:** Araştırmacı formları, proje/tez detayları, dosya ekleme ve protokol numarası üretimi.
   - ⚖️ **Kurul Değerlendirme & Otomatik Atama:** Uzmanlık ve yük dengesine göre üyelerin otomatik atanması, kurul üyelerinin 1-5 arası puanlama ve görüş bildirmesi.
   - 📜 **Karar & Resmi Belge:** Nihai karar kesinleştirme, QR kodlu ve kriptografik onaylı Resmi Etik Kurul Karar Belgesi üretimi, yazdırma ve doğrulama.
3. **Dağıtım Formatları:**
   - `EtikKurulOtomasyonu Setup 1.0.0.exe`: Masaüstü kısayolu, Başlat menüsü entegrasyonu ve kaldırma desteği olan NSIS kurulum paketi.
   - `EtikKurulOtomasyonu 1.0.0.exe`: Çift tıklamayla doğrudan açılan tek dosya taşınabilir sürüm.
