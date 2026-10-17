// src/config/db.js - MongoDB / Mongoose Bağlantı Yöneticisi

const mongoose = require('mongoose');

let isConnected = false;
let useLocalFallback = false;
const memoryStore = {
  decisions: new Map(),
  revisions: new Map(),
  auditLogs: []
};

async function connectDB() {
  const mongoUri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/etikkurul_karar';

  try {
    await mongoose.connect(mongoUri, {
      serverSelectionTimeoutMS: 2000,
      connectTimeoutMS: 2000
    });
    isConnected = true;
    useLocalFallback = false;
    console.log('[MongoDB] MongoDB veritabanına başarıyla bağlanıldı:', mongoUri);
  } catch (err) {
    console.warn(`[MongoDB Uyarısı] MongoDB (${mongoUri}) bağlantısı kurulamadı: ${err.message}.`);
    console.warn('[MongoDB Bilgi] Yerel hafıza / mock saklama alanı (In-Memory Fallback) aktif edildi.');
    useLocalFallback = true;
  }
}

function getMemoryStore() {
  return memoryStore;
}

function isFallbackActive() {
  return useLocalFallback || mongoose.connection.readyState !== 1;
}

module.exports = {
  connectDB,
  getMemoryStore,
  isFallbackActive
};
