// src/server.js - Modül 3: Express Sunucusu Giriş Noktası

const express = require('express');
const cors = require('cors');
const { connectDB } = require('./config/db');
const apiRoutes = require('./routes/apiRoutes');

const app = express();
const PORT = process.env.PORT || 5003;

app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// API Rotaları
app.use('/api', apiRoutes);

// Kök karşılama ve belge doğrulama arayüzü
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="tr">
    <head>
      <meta charset="UTF-8">
      <title>Modül 3: Karar & Belge Portalı</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
      <style>
        body { background: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero { background: linear-gradient(135deg, #0d6efd, #0b5ed7); color: white; padding: 40px 0; }
        .card { border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
      </style>
    </head>
    <body>
      <div class="hero text-center">
        <h2>📄 Etik Kurul Karar & Resmi Belge Doğrulama Modülü</h2>
        <p class="lead">Node.js (Express) + MongoDB</p>
      </div>
      <div class="container my-5" style="max-width: 700px;">
        <div class="card p-4">
          <h5 class="fw-bold text-primary mb-3">🔍 Resmi Karar Belgesi Doğrulama</h5>
          <p class="text-muted small">Belge üzerinde yer alan 24 haneli dijital doğrulama kodunu girerek belgenin gerçekliğini ve kurul onay durumunu sorgulayabilirsiniz.</p>
          <div class="input-group mb-3">
            <input type="text" id="verifyInput" class="form-control" placeholder="Doğrulama Kodu (Örn: A1B2C3D4...)">
            <button class="btn btn-primary" onclick="verifyDoc()">Doğrula</button>
          </div>
          <div id="verifyResult" class="mt-3"></div>
        </div>

        <div class="card p-4 mt-4">
          <h6 class="fw-bold mb-2">⚡ Modül 3 Aktif API Uç Noktaları:</h6>
          <ul class="small text-muted mb-0">
            <li><code>POST /api/decisions/finalize</code> - Nihai Karar Verme & Belge Üretme</li>
            <li><code>GET /api/decisions/:protocol/certificate</code> - Karar Belgesini Görüntüleme (HTML/PDF)</li>
            <li><code>POST /api/revisions/request</code> - Revizyon Talebi Gönderme</li>
            <li><code>GET /api/verify/:code</code> - Kriptografik Belge Doğrulama</li>
            <li><code>GET /api/audit/:protocol</code> - Denetim İzi (Audit Log) Geçmişi</li>
          </ul>
        </div>
      </div>
      <script>
        async function verifyDoc() {
          const code = document.getElementById('verifyInput').value.trim();
          if(!code) return alert('Lütfen doğrulama kodunu giriniz.');
          const res = await fetch('/api/verify/' + encodeURIComponent(code));
          const data = await res.json();
          const out = document.getElementById('verifyResult');
          if(res.ok && data.valid) {
            out.innerHTML = '<div class="alert alert-success"><strong>✅ Belge Doğrulandı!</strong><br>Protokol No: ' + data.protocolNumber + '<br>Karar No: ' + data.decisionNumber + '<br>Proje: ' + data.projectTitle + '<br>Sonuç: <strong>' + data.finalDecision + '</strong></div>';
          } else {
            out.innerHTML = '<div class="alert alert-danger">❌ Belge doğrulanamadı veya geçersiz kod.</div>';
          }
        }
      </script>
    </body>
    </html>
  `);
});

// Veritabanı bağlantısı ve başlatma
connectDB().then(() => {
  app.listen(PORT, () => {
    console.log(`[Modül 3] Karar ve Belge Servisi port ${PORT} üzerinde çalışıyor.`);
  });
});

module.exports = app;
