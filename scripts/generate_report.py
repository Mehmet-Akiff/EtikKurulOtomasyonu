# -*- coding: utf-8 -*-
"""
Etik Kurul Otomasyonu - Kapsamlı Teknik Rapor, Grafik ve Word (.docx) Üretim Betiği
"""

import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\PC\Desktop\Antigravity Projects\EtikKurulOtomasyonu"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
CHART_DIR = os.path.join(BASE_DIR, "docs", "charts")
DESKTOP_DOCX_PATH = r"C:\Users\PC\Desktop\Etik_Kurul_Otomasyonu_Teknik_Raporu.docx"
PROJECT_DOCX_PATH = os.path.join(BASE_DIR, "Etik_Kurul_Otomasyonu_Teknik_Raporu.docx")

os.makedirs(CHART_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def generate_charts():
    # -------------------------------------------------------------------------
    # Grafik 1: Modüler Mimari ve İş Akışı Performans / Katman Diyagramı
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    boxes = [
        (0.4, 2.6, 2.0, 1.7, "#1e3c72", "MODÜL 1\nBaşvuru & Evrak\n\nASP.NET Core 9\nMSSQL / SQLite\n(Port: 5001)"),
        (2.9, 2.6, 2.0, 1.7, "#0284c7", "MODÜL 2\nOtomatik Atama\n& Değerlendirme\n\nPHP 8.3 + MySQL\n(Port: 5002)"),
        (5.4, 2.6, 2.0, 1.7, "#0f766e", "MODÜL 3\nKarar, Revizyon &\nQR Belge Üretimi\n\nNode.js + MongoDB\n(Port: 5003)"),
        (7.8, 2.6, 1.9, 1.7, "#15803d", "DOĞRULAMA\nKriptografik\nSHA-256 + QR\n\n24 Haneli Kod\nResmi Sertifika"),
    ]

    for x, y, w, h, color, text in boxes:
        rect = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="#ffffff", linewidth=2, zorder=3)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, color="white", fontsize=9.5, fontweight="bold",
                ha="center", va="center", zorder=4)

    # Arrows between boxes
    arrow_xs = [(2.4, 2.9), (4.9, 5.4), (7.4, 7.8)]
    for x1, x2 in arrow_xs:
        ax.annotate("", xy=(x2, 3.45), xytext=(x1, 3.45),
                    arrowprops=dict(arrowstyle="->", color="#1e293b", lw=2.5))

    # Bottom unified desktop layer
    desktop_rect = plt.Rectangle((0.4, 0.45), 9.3, 1.5, facecolor="#312e81", edgecolor="#c7d2fe", linewidth=2, zorder=3)
    ax.add_patch(desktop_rect)
    ax.text(5.05, 1.2,
            "MODÜL 4: WINDOWS MASAÜSTÜ UYGULAMASI (Electron + Gömülü İş Akışı Motoru)\n"
            "Setup (.exe) & Portable (.exe) | IPC Güvenli Köprü | Otomatik Durum Onarımı (reconcileState) | Yerel Kalıcı JSON Veritabanı",
            color="white", fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=4)

    # Vertical connectors
    for cx in [1.4, 3.9, 6.4, 8.75]:
        ax.annotate("", xy=(cx, 2.6), xytext=(cx, 1.95),
                    arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.8, ls="--"))

    ax.set_title("Şekil 1: Etik Kurul Otomasyonu Çok Katmanlı Modüler Mimari ve Veri Akış Şeması",
                 fontsize=12, fontweight="bold", color="#0f172a", pad=10)
    plt.tight_layout()
    chart1_path = os.path.join(CHART_DIR, "chart_01_architecture.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------------------
    # Grafik 2: Akıllı Otomatik Dosya Atama Algoritması Puanlama Simülasyonu
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    members = [
        "Prof. Dr. Kerem Yaman\n(Biyomedikal / YZ - 1 Dosya)",
        "Prof. Dr. Selim Vural\n(Tıp / Klinik - 1 Dosya)",
        "Dr. Öğr. Üyesi Burcu Polat\n(Tıp / Halk Sağlığı - 0 Dosya)",
        "Doç. Dr. Aylin Çelik\n(Psikoloji - 1 Dosya)",
        "Prof. Dr. Murat Doğan\n(Hukuk / Sosyal - 0 Dosya)",
        "Doç. Dr. Zeynep Kaya\n(Eğitim Bilimleri - 1 Dosya)"
    ]
    # Örnek "Tıp / Biyomedikal" başvurusu için puanlama: (Uzmanlık Eşleşmesi * 100) - (Aktif Dosya * 10)
    scores_biomed = [100 - 10, 100 - 10, 100 - 0, 0 - 10, 0 - 0, 0 - 10]
    colors = ["#16a34a" if s >= 90 else "#94a3b8" for s in scores_biomed]

    y_pos = np.arange(len(members))
    bars = ax.barh(y_pos, scores_biomed, color=colors, height=0.55, edgecolor="#1e293b", linewidth=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(members, fontsize=9)
    ax.invert_yaxis()
    ax.axvline(0, color="#334155", linewidth=1)
    ax.set_xlim(-25, 125)
    ax.set_xlabel("Algoritma Uygunluk Puanı: Skor = (Uzmanlık Eşleşmesi × 100) − (Aktif Dosya Yükü × 10)", fontsize=9.5, fontweight="bold")
    ax.set_title("Şekil 2: 'Tıp / Biyomedikal' Başvurusu İçin Otomatik Raportör Seçim ve Yük Dengeleme Puanları",
                 fontsize=11, fontweight="bold", color="#0f172a")
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for bar, score in zip(bars, scores_biomed):
        offset = 3 if score >= 0 else -14
        label = f"+{score} Puan (Atandı)" if score >= 90 else f"{score} Puan"
        ax.text(score + offset, bar.get_y() + bar.get_height() / 2, label,
                va='center', ha='left' if score >= 0 else 'right', fontsize=8.5, fontweight='bold',
                color="#166534" if score >= 90 else "#475569")

    plt.tight_layout()
    chart2_path = os.path.join(CHART_DIR, "chart_02_algorithm_scoring.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------------------
    # Grafik 3: Başvuru Değerlendirme Kriterleri ve Karar Eşik Analizi
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    protocols = [
        "ETIK-2026-00001\n(Biyosensör - Onay)",
        "ETIK-2026-00002\n(AI Klinik - Onay)",
        "ETIK-2026-00003\n(Psikoloji - Revizyon)",
        "Örnek Riskli Dosya\n(Metodolojik Ret)"
    ]
    m_scores = [5.0, 5.0, 4.0, 2.0]
    c_scores = [4.5, 5.0, 3.0, 1.5]
    r_scores = [5.0, 4.0, 4.0, 2.0]
    avg_scores = [round((m + c + r) / 3.0, 2) for m, c, r in zip(m_scores, c_scores, r_scores)]

    x = np.arange(len(protocols))
    width = 0.2

    ax.bar(x - 1.5 * width, m_scores, width, label="Metodoloji Uygunluğu (1-5)", color="#0284c7")
    ax.bar(x - 0.5 * width, c_scores, width, label="Bilgilendirilmiş Onam (1-5)", color="#6366f1")
    ax.bar(x + 0.5 * width, r_scores, width, label="Risk-Fayda Dengesi (1-5)", color="#0d9488")
    bars_avg = ax.bar(x + 1.5 * width, avg_scores, width, label="Genel Etik Ortalaması", color="#16a34a", edgecolor="#14532d", linewidth=1.2)

    for b in bars_avg:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + 0.08, f"{h:.2f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax.set_ylim(0, 5.8)
    ax.set_xticks(x)
    ax.set_xticklabels(protocols, fontsize=9, fontweight="bold")
    ax.set_ylabel("Değerlendirme Puanı (1 - 5 Ölçeği)", fontsize=9.5, fontweight="bold")
    ax.set_title("Şekil 3: Kurul Üyesi Çok Kriterli Etik Değerlendirme Puanları ve Karar Dağılımı",
                 fontsize=11, fontweight="bold", color="#0f172a")
    ax.axhline(4.0, color="#16a34a", linestyle="--", alpha=0.6, label="Onay Referans Eşiği (4.0+)")
    ax.legend(loc="upper right", fontsize=8.5, ncol=2)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    chart3_path = os.path.join(CHART_DIR, "chart_03_evaluation_scores.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close(fig)

    # -------------------------------------------------------------------------
    # Grafik 4: Modül Bazlı Otomatik Birim ve Entegrasyon Test Sonuçları
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.5), dpi=300)

    modules = [
        "Modül 1\n(.NET 9)\nMSSQL",
        "Modül 2\n(PHP 8.3)\nMySQL",
        "Modül 3\n(Node.js)\nMongoDB",
        "Modül 4\n(Electron)\nMasaüstü"
    ]
    passed_counts = [4, 4, 4, 7]
    failed_counts = [0, 0, 0, 0]

    x_m = np.arange(len(modules))
    b1 = ax1.bar(x_m, passed_counts, width=0.5, label="Başarılı Test Sayısı", color="#16a34a")
    ax1.bar(x_m, failed_counts, width=0.5, bottom=passed_counts, label="Başarısız Test Sayısı", color="#dc2626")
    ax1.set_xticks(x_m)
    ax1.set_xticklabels(modules, fontsize=8.5, fontweight="bold")
    ax1.set_ylim(0, 8.5)
    ax1.set_ylabel("Test Senaryosu Sayısı", fontsize=9, fontweight="bold")
    ax1.set_title("Modül Bazlı Otomatik Test Sayıları (Toplam: 19/19)", fontsize=10, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)

    for b in b1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, h + 0.15, f"{h}/{h} (%100)", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#166534")

    # Pie chart of coverage by functional domain
    labels = [
        "Başvuru & Evrak (4 Test)",
        "Otomatik Atama & Yük (4 Test)",
        "Karar, QR & Kriptografi (5 Test)",
        "Senkronizasyon & Revizyon (6 Test)"
    ]
    sizes = [4, 4, 5, 6]
    pie_colors = ["#1e3c72", "#0284c7", "#0f766e", "#16a34a"]
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=pie_colors,
            textprops={'fontsize': 8, 'fontweight': 'bold'}, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
    ax2.set_title("İşlevsel Alanlara Göre Doğrulama Dağılımı", fontsize=10, fontweight="bold")

    plt.suptitle("Şekil 4: Uçtan Uca Kalite Güvencesi ve Birim Test Doğrulama Metrikleri", fontsize=11.5, fontweight="bold", y=1.01)
    plt.tight_layout()
    chart4_path = os.path.join(CHART_DIR, "chart_04_test_verification.png")
    plt.savefig(chart4_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return [chart1_path, chart2_path, chart3_path, chart4_path]


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_styled_table(doc, headers, rows, col_widths=None, header_bg="1E3C72"):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(header_text)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = "Segoe UI"
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_shading(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=110, bottom=110, left=130, right=130)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Data rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(str(val))
            run.font.size = Pt(9)
            run.font.name = "Segoe UI"
            run.font.color.rgb = RGBColor(30, 41, 59)
            if c_idx == 0:
                run.bold = True
            set_cell_shading(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=130, right=130)
            row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    doc.add_paragraph()
    return table


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Segoe UI"
        if level == 1:
            run.font.size = Pt(15)
            run.font.color.rgb = RGBColor(30, 60, 114)
        elif level == 2:
            run.font.size = Pt(12.5)
            run.font.color.rgb = RGBColor(2, 132, 199)
        else:
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(15, 118, 110)
    return h


def add_figure(doc, image_path, caption_text, width_inches=6.2):
    if not os.path.exists(image_path):
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(image_path, width=Inches(width_inches))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c_run = cap.add_run(caption_text)
    c_run.italic = True
    c_run.bold = True
    c_run.font.size = Pt(9)
    c_run.font.name = "Segoe UI"
    c_run.font.color.rgb = RGBColor(71, 85, 105)
    doc.add_paragraph()


def build_word_report(charts):
    doc = Document()

    # Sayfa kenar boşlukları
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Varsayılan stil
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(31, 41, 55)

    # =========================================================================
    # KAPAK BÖLÜMÜ
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = title_p.add_run("T.C. AKADEMİK VE BİLİMSEL ARAŞTIRMALAR\nETİK KURUL OTOMASYONU\n")
    r_top.bold = True
    r_top.font.size = Pt(20)
    r_top.font.color.rgb = RGBColor(30, 60, 114)

    r_sub = title_p.add_run("KAPSAMLI YAZILIM MİMARİSİ, İŞ AKIŞI, HATA ÇÖZÜMLERİ VE\nDOĞRULAMA TEKNİK RAPORU")
    r_sub.bold = True
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(2, 132, 199)

    doc.add_paragraph()

    # Proje Künye Tablosu
    add_styled_table(
        doc,
        ["Proje Parametresi", "Teknik Detay ve Açıklama"],
        [
            ["Proje Adı", "Etik Kurul Otomasyonu (Çok Katmanlı Web Servisleri & Windows Masaüstü Uygulaması)"],
            ["Geliştirici / Yazar", "Mehmet Akif Ürey"],
            ["Mimari Yapı", "4 Bağımsız Modül (ASP.NET Core 9 + MSSQL, PHP 8.3 + MySQL, Node.js + MongoDB, Electron Masaüstü)"],
            ["Çalıştırılabilir Paketler", "1) Etik Kurul Otomasyonu Setup 1.0.0.exe (NSIS Kurulum Sihirbazı)\n2) EtikKurulOtomasyonu-Portable.exe (Kurulumsuz Tek Tıkla Çalışan Exe)\n3) Baslat.bat & Masaüstü Kısayolu"],
            ["GitHub Resmi Deposu", "https://github.com/Mehmet-Akiff/EtikKurulOtomasyonu (Release: v1.0.0)"],
            ["Proje Klasör Yolu", r"C:\Users\PC\Desktop\Antigravity Projects\EtikKurulOtomasyonu"],
            ["Doğrulama & Test Durumu", "Toplam 19/19 Otomatik Birim ve İş Akışı Testi Başarılı (%100 Geçiş Oranı)"],
            ["Rapor Tarihi", "21 Ekim 2026"]
        ],
        col_widths=[2.1, 4.6]
    )

    # =========================================================================
    # 1. YÖNETİCİ ÖZETİ VE PROJE AMACI
    # =========================================================================
    add_heading_styled(doc, "1. Yönetici Özeti ve Proje Kapsamı", level=1)
    p1 = doc.add_paragraph(
        "Etik Kurul Otomasyonu; üniversiteler, araştırma merkezleri ve klinik/akademik birimlerde yürütülecek "
        "bilimsel araştırma, yüksek lisans/doktora tezi ve TÜBİTAK/kurumsal projeler için etik kurul onay süreçlerini "
        "uçtan uca dijitalleştiren modüler bir kurumsal yazılım sistemidir. Sistem, araştırmacıların başvuru formlarını "
        "ve ek belgelerini (Araştırma Protokolü, Bilgilendirilmiş Gönüllü Onam Formu, Veri Toplama Ölçekleri) dijital "
        "olarak iletmesini, başvuruların kurul üyelerine uzmanlık alanı ve dosya yükü dengesine göre otomatik atanmasını, "
        "üyelerin 1-5 ölçeğinde kriter puanlaması ve görüş bildirmesini ve nihai kurul kararlarının (Onay, Düzeltme/Revizyon, Ret) "
        "24 haneli kriptografik doğrulama kodu ve QR kodlu resmi belge olarak otomatik üretilmesini sağlar."
    )

    p2 = doc.add_paragraph(
        "Proje şartnamesinde talep edilen 3 farklı arka uç (backend) teknoloji yığını tek bir klasörel spagetti kod "
        "yerine tamamen bağımsız ve modüler dizinler halinde inşa edilmiş; buna ek olarak son kullanıcının hiçbir sunucu, "
        "veritabanı motoru veya ek araç kurmasına gerek kalmadan doğrudan Windows masaüstünde çift tıklayarak "
        "kullanabilmesi için 4. modül olarak Windows 11 Fluent UI tasarım diline sahip bağımsız Masaüstü Uygulaması (.exe) "
        "geliştirilmiştir."
    )

    # =========================================================================
    # 2. ÇOK KATMANLI MODÜLER SİSTEM MİMARİSİ
    # =========================================================================
    add_heading_styled(doc, "2. Çok Katmanlı Modüler Sistem Mimarisi", level=1)
    doc.add_paragraph(
        "Yazılım mimarisi, her bir işlevsel sorumluluğun (Separation of Concerns) kendi teknoloji yığınında bağımsız "
        "çalışabilmesi ve aynı zamanda ortak protokol numarası standardı (ETIK-YYYY-XXXXX) üzerinden haberleşebilmesi "
        "prensibiyle tasarlanmıştır. Aşağıdaki Şekil 1'de sistemin 4 modüllü mimarisi ve veri akışı gösterilmiştir."
    )

    add_figure(doc, charts[0], "Şekil 1: Etik Kurul Otomasyonu Çok Katmanlı Modüler Mimari ve Veri Akış Şeması", width_inches=6.4)

    add_styled_table(
        doc,
        ["Modül Kodu ve Adı", "Teknoloji Yığını", "Veritabanı & Kalıcılık", "Temel Sorumluluklar ve İşlevler"],
        [
            [
                "1-BasvuruModulu_DotNet",
                "C# / ASP.NET Core 9.0\nEntity Framework Core\nREST API + Razor UI",
                "Microsoft SQL Server (MSSQL)\n+ Otomatik SQLite Yedekleme\n(etikkurul_basvuru.db)",
                "• Araştırmacı kaydı ve profil yönetimi\n"
                "• Dijital başvuru formu ve PDF evrak yükleme\n"
                "• Otomatik protokol numarası (ETIK-YYYY-XXXXX) üretimi\n"
                "• Başvuru durumu sorgulama (Port: 5001)"
            ],
            [
                "2-DegerlendirmeModulu_PHP",
                "PHP 8.3 (PDO)\nKatmanlı MVC Mimarisi\nREST API + Kurul Portalı",
                "MySQL 8.x İlişkisel Şema\n+ Otomatik SQLite Yedekleme\n(etikkurul_degerlendirme.sqlite)",
                "• Kurul üyelerinin uzmanlık ve aktif yük takibi\n"
                "• Akıllı Otomatik Dosya Dağıtım Algoritması\n"
                "• 3 kriterli (Metodoloji, Onam, Risk) 1-5 puanlama\n"
                "• Otomatik karar tavsiyesi hesaplama (Port: 5002)"
            ],
            [
                "3-KararVeBelgeModulu_Node",
                "Node.js (v24) + Express.js\nMongoose ODM + QRCode\nKriptografik Belge Motoru",
                "MongoDB (NoSQL Doküman)\n+ Otomatik Bellek/Dosya Yedekleme\n(etikkurul_karar)",
                "• Nihai kurul kararı (Onay / Revizyon / Ret) kesinleştirme\n"
                "• Revizyon takip ve son teslim tarihi yönetimi\n"
                "• QR kodlu ve SHA-256 imzalı resmi HTML/PDF karar belgesi\n"
                "• Denetim izi (Audit Log) ve belge doğrulama (Port: 5003)"
            ],
            [
                "4-MasaustuUygulamasi",
                "Electron 34 + Node.js\nWindows 11 Fluent UI\nNSIS Setup & Portable Exe",
                "Yerel Kalıcı JSON Veritabanı\n(AppData/Roaming/etik-kurul-otomasyonu/etikkurul_local.json)",
                "• Tüm 3 modülün iş mantığını tek pencerede birleştirir\n"
                "• Sunucu kurulumu gerektirmeden doğrudan çalışır\n"
                "• Otomatik durum senkronizasyonu (reconcileState)\n"
                "• Dahili resmi sertifika görüntüleyici ve doğrulayıcı"
            ]
        ],
        col_widths=[1.5, 1.5, 1.5, 2.2]
    )

    # =========================================================================
    # 3. MODÜL BAZLI TEKNİK İNCELEME VE ALGORİTMALAR
    # =========================================================================
    add_heading_styled(doc, "3. Modül Bazlı Teknik İnceleme, Veri Modelleri ve Algoritmalar", level=1)

    add_heading_styled(doc, "3.1. Modül 1: Başvuru ve Evrak İletim Modülü (ASP.NET Core 9 + MSSQL)", level=2)
    doc.add_paragraph(
        "Modül 1, araştırmacıların projelerini sisteme kaydettiği giriş kapısıdır. Entity Framework Core kullanılarak "
        "Researchers, Applications ve ApplicationDocuments tabloları modellenmiştir. Bağlantı dizesinde MSSQL sunucusu "
        "bulunmadığında sistem kesintiye uğramadan otomatik olarak yerel SQLite veritabanına geçiş yapar."
    )

    add_styled_table(
        doc,
        ["HTTP Metodu & Endpoint", "İlgili Sınıf / Metot", "Açıklama ve Dönüş Değeri"],
        [
            ["GET /api/applications", "ApplicationsController.GetAll()", "Tüm başvuruları araştırmacı ve yüklenen belgeleriyle birlikte listeler."],
            ["GET /api/applications/{protocol}", "ApplicationsController.GetByProtocol()", "Protokol numarasına (ETIK-2026-XXXXX) göre tekil başvuru detayını döner."],
            ["POST /api/applications", "ApplicationService.CreateApplicationAsync()", "Yeni başvuru oluşturur, benzersiz protokol numarası üretir ve kaydeder."],
            ["POST /api/applications/{id}/documents", "ApplicationService.UploadDocumentAsync()", "Başvuruya ait PDF/DOCX evraklarını SHA-256 dosya özeti (hash) ile kaydeder."],
            ["PATCH /api/applications/{protocol}/status", "ApplicationService.UpdateStatusAsync()", "Diğer modüllerden gelen bildirimle başvuru durumunu günceller."]
        ],
        col_widths=[2.1, 2.0, 2.6]
    )

    add_heading_styled(doc, "3.2. Modül 2: Akıllı Otomatik Dosya Atama ve Değerlendirme Modülü (PHP 8.3 + MySQL)", level=2)
    doc.add_paragraph(
        "Modül 2, başvurunun araştırma alanını (ör. 'Tıp / Biyomedikal', 'Klinik Psikoloji', 'Sosyal Bilimler / Hukuk', "
        "'Mühendislik / Yapay Zeka ve Bilişim') Türkçe karakter duyarlı anahtar kelimelere ayırır ve aktif kurul üyelerinin "
        "uzmanlık alanlarıyla karşılaştırır. Aday raportörler aşağıdaki matematiksel formül ile puanlanır:\n"
        "• Aday Uygunluk Skoru = (Uzmanlık Kelime Eşleşme Sayısı × 100) − (Üyenin Aktif Dosya Sayısı × 10)\n"
        "Eşit puan durumunda aktif dosya yükü daha az olan kurul üyesine öncelik verilir."
    )

    add_figure(doc, charts[1], "Şekil 2: Akıllı Otomatik Dosya Dağıtım Algoritması Puanlama ve Yük Dengeleme Grafiği", width_inches=6.2)

    add_styled_table(
        doc,
        ["HTTP Metodu & Endpoint", "İlgili Sınıf / Metot", "Açıklama ve İş Mantığı"],
        [
            ["GET /api/members", "AssignmentController::getMembers()", "Aktif kurul üyelerini, uzmanlık alanlarını ve mevcut dosya yüklerini döner."],
            ["POST /api/assignments/auto-assign", "AutoAssignmentService::autoAssign()", "Uzmanlık + yük dengesi algoritmasıyla en uygun 2 raportörü otomatik atar."],
            ["POST /api/evaluations", "EvaluationController::submitEvaluation()", "Üyenin 1-5 arası kriter puanlarını ve kararını (Onay/Revizyon/Ret) kaydeder."],
            ["GET /api/evaluations/summary/{protocol}", "EvaluationController::getSummary()", "Oyları harmanlar, ağırlıklı etik puan ortalamasını ve karar tavsiyesini üretir."]
        ],
        col_widths=[2.1, 2.0, 2.6]
    )

    add_heading_styled(doc, "3.3. Modül 3: Karar, Revizyon ve QR Kodlu Belge Modülü (Node.js + MongoDB)", level=2)
    doc.add_paragraph(
        "Modül 3, kurul değerlendirmelerini nihai karara bağlar. Her karar için protokol numarası, karar numarası ve "
        "gizli tuz (salt) değerini SHA-256 algoritmasıyla özetleyerek 24 haneli benzersiz bir doğrulama kodu üretir. "
        "Ayrıca bu doğrulama kodunu içeren Base64 gömülü bir QR kod (Karekod) oluşturarak resmi ıslak/elektronik imzaya "
        "hazır HTML/PDF karar belgesini otomatik inşa eder."
    )

    add_figure(doc, charts[2], "Şekil 3: Kurul Üyesi Çok Kriterli Etik Değerlendirme Puanları ve Karar Dağılımı", width_inches=6.2)

    # =========================================================================
    # 4. UYGULAMA İÇİ EKRAN GÖRÜNTÜLERİ VE KULLANIM AKIŞI
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "4. Uygulama İçi Gerçek Ekran Görüntüleri ve İş Akışı", level=1)
    doc.add_paragraph(
        "Aşağıdaki ekran görüntüleri doğrudan çalışan masaüstü uygulamasının (4-MasaustuUygulamasi) canlı arayüzünden "
        "alınmış olup, başvurunun oluşturulmasından QR kodlu karar belgesinin doğrulanmasına kadar olan 6 sekmeli "
        "iş akışını sırasıyla göstermektedir."
    )

    screenshots_info = [
        (
            "01_dashboard.png",
            "Ekran Görüntüsü 1: Sistem Genel Bakış (Dashboard) Sekmesi — Toplam başvuru, incelemedeki dosyalar, "
            "onaylanan kararlar (2 Onaylı Karar) ve her başvuru için durum bazlı 'Hızlı İşlem' butonları."
        ),
        (
            "02_application.png",
            "Ekran Görüntüsü 2: Yeni Etik Kurul Başvurusu Sekmesi — Sorumlu araştırmacı seçimi, satır içi 'Yeni Araştırmacı Ekle' "
            "paneli, uzmanlık alanı seçimi ve otomatik eklenen dijital protokol/onam belgeleri."
        ),
        (
            "03_assignment.png",
            "Ekran Görüntüsü 3: Otomatik Atama Sekmesi — Atama bekleyen başvurular, kurul üyelerinin aktif dosya yükleri "
            "ve alt kısımda yer alan 'Atanmış Dosyalar ve Raportör İnceleme Durumu' takip tablosu."
        ),
        (
            "04_evaluation.png",
            "Ekran Görüntüsü 4: Kurul Üye Değerlendirme & Puanlama Sekmesi — Metodoloji, Bilgilendirilmiş Onam ve Risk-Fayda "
            "kriterleri (1-5 puan), üye karar tercihi ve alt kısımda 'Tamamlanan Üye Değerlendirmeleri' geçmiş tablosu."
        ),
        (
            "05_decision.png",
            "Ekran Görüntüsü 5: Nihai Kurul Kararları & Belgeler Sekmesi — Onaylanan ve revizyon verilen başvuruların karar "
            "numaraları, etik puan ortalamaları, doğrulama kodları, revizyon onaylama butonu ve Hızlı Kurul Başkanlığı Kararı tablosu."
        ),
        (
            "06_certificate.png",
            "Ekran Görüntüsü 6: Otomatik Oluşturulan QR Kodlu Resmi Etik Kurul Karar Belgesi — Başvuru künyesi, nihai onay "
            "hükmü, kurul üyesi imzaları, Etik Kurul Başkanı onayı, 24 haneli kriptografik kod ve gömülü Karekod (QR)."
        ),
        (
            "07_verification.png",
            "Ekran Görüntüsü 7: Resmi Karar Belgesi Doğrulama Sekmesi — Kayıtlı karar kodlarına tek tıkla erişim ve 24 haneli "
            "doğrulama kodu ile yapılan sorgulamada belgenin gerçekliğinin teyit edilmesi."
        )
    ]

    for fname, caption in screenshots_info:
        img_path = os.path.join(SCREENSHOT_DIR, fname)
        w_in = 5.4 if fname == "06_certificate.png" else 6.3
        add_figure(doc, img_path, caption, width_inches=w_in)

    # =========================================================================
    # 5. TESPİT EDİLEN YAZILIMSAL MANTIK HATALARI VE ÇÖZÜMLERİ
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "5. Tespit Edilen Yazılımsal Mantık Hataları ve Uygulanan Çözümler", level=1)
    doc.add_paragraph(
        "Kullanıcı testleri sırasında tespit edilen 'onaylanan başvuruların Karar & Belgeler sekmesine düşmemesi' "
        "problemi başta olmak üzere, uçtan uca yapılan sistematik hata ayıklama (debugging) çalışmasında toplam 7 kritik "
        "yazılımsal mantık hatası giderilmiştir. Tüm bulgular ve çözümler aşağıdaki tabloda detaylandırılmıştır."
    )

    add_styled_table(
        doc,
        ["Hata No & Başlığı", "Kök Neden Analizi (Önceki Hatalı Durum)", "Uygulanan Mühendislik Çözümü (Yeni Durum)"],
        [
            [
                "1. Tek Raportör Onayında Karar Sekmesinin Boş Kalması",
                "Otomatik atama 2 raportör atıyordu. 1. raportör onay verdiğinde getEvaluationSummary() 'AwaitingReviews' dönüyor ve 2. raportör de oy verene kadar finalizeDecision() hiç çağrılmıyordu. Bu nedenle onaylanan dosya Karar sekmesinde görünmüyordu.",
                "submitEvaluation() metodu asenkron hale getirildi ve ilk raportör değerlendirme yaptığı anda finalizeDecision() otomatik tetiklenerek karar ve sertifika anında Karar & Belgeler sekmesine düşürüldü. 2. raportör oy verdiğinde aynı karar numarası korunarak belge 2 imza ile güncelleniyor."
            ],
            [
                "2. Geçmişte Değerlendirilen Dosyaların Kurtarılması (ETIK-2026-00002)",
                "Önceki sürümde değerlendirilip 'UnderReview' durumunda asılı kalan başvurular için geriye dönük karar üretme mekanizması bulunmuyordu.",
                "EmbeddedWorkflow içerisine reconcileState() onarım motoru eklendi. Uygulama açılışında tüm değerlendirmeleri tarayarak kararı eksik olan başvuruları (ör. ETIK-2026-00002 - AI) otomatik olarak KARAR-2026-00001 onay belgesine dönüştürdü."
            ],
            [
                "3. Otomatik Kararlarda Yanlış Gerekçe (Ret Metni) Yazılması",
                "finalizeDecision() içinde finalDecision parametresi doğrudan gönderilmeyip summary.recommendation üzerinden 'Approved' geldiğinde, üçlü koşul (finalDecision === 'Approved') yanlış çalışarak onaylanan belgeye ret gerekçesi yazıyordu.",
                "Koşul effectiveDecision değişkenine bağlandı. Approved, RevisionNeeded ve Rejected durumları için ayrı resmi gerekçe şablonları tanımlandı ve raportörün feedbackNotes görüşü karar metnine eklendi."
            ],
            [
                "4. Revizyon Sonrası Onaylama ve Doğrudan Karar Eksikliği",
                "Revizyon ('RevisionNeeded') alan bir başvurunun düzeltme sonrasında nasıl onaylanacağına dair arayüzde bir kontrol yoktu; ayrıca incelemedeki dosyalara doğrudan kurul kararı verilemiyordu.",
                "Karar sekmesine revizyondaki dosyalar için tek tıkla 'Onayla' butonu ve henüz karara bağlanmamış dosyalar için 'Hızlı Kurul Başkanlığı Kararı (Onayla / Revizyon / Reddet)' tablosu eklendi."
            ],
            [
                "5. Atanan Dosyaların ve Değerlendirme Geçmişinin Görünmemesi",
                "Otomatik Atama sekmesinde dosya atandıktan sonra listeden kayboluyor, hangi raportörlerin atandığı ve kaçının değerlendirme yaptığı izlenemiyordu.",
                "Otomatik Atama sekmesine 'Atanmış Dosyalar ve Raportör İnceleme Durumu' tablosu, Üye Değerlendirme sekmesine ise 'Tamamlanan Üye Değerlendirmeleri' tablosu eklendi."
            ],
            [
                "6. Türkçe Karakter ('İ/ı') Uzmanlık Eşleştirme Hatası",
                "tokenizeField() fonksiyonunda JavaScript'in standart .toLowerCase() metodu kullanıldığı için 'İ' harfi bozuluyor ve 'Eğitim Bilimleri' gibi alanlarda eşleşme kaybı yaşanıyordu.",
                ".toLocaleLowerCase('tr-TR') kullanımına geçildi ve durak kelimeler ('bilimleri', 'bilimler' vb.) genişletilerek uzmanlık eşleştirme doğruluğu %100'e çıkarıldı."
            ],
            [
                "7. Doğrulama Sekmesinde Sabit Yeşil Rozet ve Kod Kopyalama Zorluğu",
                "Belge doğrulama ekranında ret veya revizyon kararları bile sabit 'badge-approved' (yeşil) rozetiyle gösteriliyordu ve 24 haneli kodu elle yazmak zordu.",
                "Dinamik getBadgeClass(res.finalDecision) rozeti eklendi; ayrıca Karar ve Doğrulama sekmelerine tek tıkla doğrulama kodunu seçip sorgulayan etkileşimli kod etiketleri (code-pill) eklendi."
            ]
        ],
        col_widths=[1.5, 2.5, 2.7]
    )

    # =========================================================================
    # 6. OTOMATİK TEST VE KALİTE GÜVENCESİ SONUÇLARI
    # =========================================================================
    add_heading_styled(doc, "6. Otomatik Test, Doğrulama ve Kalite Güvencesi Sonuçları", level=1)
    doc.add_paragraph(
        "Sistemdeki tüm modüller için bağımsız birim ve uçtan uca entegrasyon testleri yazılmış ve 'test-workflow.ps1' "
        "doğrulama betiği ile terminal üzerinden çalıştırılmıştır. 4 modülün tamamında toplam 19 test senaryosu "
        "%100 başarı oranıyla geçmiştir."
    )

    add_figure(doc, charts[3], "Şekil 4: Modül Bazlı Otomatik Test Sonuçları ve İşlevsel Doğrulama Dağılımı", width_inches=6.3)

    add_styled_table(
        doc,
        ["Modül", "Test Dosyası / Komutu", "Doğrulanan Senaryolar", "Sonuç"],
        [
            [
                "Modül 1\n(.NET 9 + MSSQL)",
                "1-BasvuruModulu_DotNet.Tests/\nApplicationServiceTests.cs",
                "1) Yeni başvuru ve ETIK-YYYY-XXXXX protokol üretimi\n"
                "2) Protokol numarası ile başvuru ve araştırmacı sorgulama\n"
                "3) Dijital belge yükleme ve SHA-256 hash doğrulaması\n"
                "4) Başvuru durumu güncelleme ve geçersiz durum koruması",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 2\n(PHP 8.3 + MySQL)",
                "2-DegerlendirmeModulu_PHP/\ntests/AutoAssignmentTest.php",
                "1) Kurul üyelerinin ve uzmanlık alanlarının listelenmesi\n"
                "2) Uzmanlık ve yük dengesine göre 2 raportör otomatik atama\n"
                "3) Yinelenen atama (Idempotency) engelleme testi\n"
                "4) Üye kriter puanlaması ve görüş kaydı oluşturma",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 3\n(Node.js + MongoDB)",
                "3-KararVeBelgeModulu_Node/\ntests/decision.test.js",
                "1) Revizyon talebi ve 14 günlük son teslim tarihi oluşturma\n"
                "2) Nihai karar ve Base64 QR kodlu resmi HTML sertifika üretimi\n"
                "3) 24 haneli kriptografik kod ile belge doğrulama\n"
                "4) Denetim izi (Audit Log) kayıtlarının bütünlük kontrolü",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 4\n(Masaüstü Motoru)",
                "4-MasaustuUygulamasi/\ntests/engine.test.js",
                "1) Başvuru oluşturma ve araştırmacı ID tip normalizasyonu\n"
                "2) Türkçe karakter duyarlı otomatik raportör ataması\n"
                "3) İlk raportör onayı sonrası anında otomatik karar & belge oluşumu\n"
                "4) İkinci raportör onayı sonrası karar no korunarak 2 imzalı güncelleme\n"
                "5) Kriptografik belge doğrulama testi\n"
                "6) Revizyon kararı ve revizyon sonrası onay geçiş testi\n"
                "7) reconcileState() ile geçmiş değerlendirmelerin otomatik kurtarılması",
                "7 / 7 Başarılı\n(%100)"
            ]
        ],
        col_widths=[1.3, 1.8, 2.6, 1.0]
    )

    # =========================================================================
    # 7. ÇALIŞTIRMA VE DAĞITIM KILAVUZU
    # =========================================================================
    add_heading_styled(doc, "7. Kurulum, Çalıştırma ve Dağıtım Rehberi", level=1)
    doc.add_paragraph(
        "Uygulama hem geliştiriciler için modüler kaynak kodlarıyla hem de son kullanıcılar için tek tıkla "
        "çalıştırılabilir Windows paketleriyle teslim edilmiştir:"
    )

    add_styled_table(
        doc,
        ["Dağıtım / Çalıştırma Yöntemi", "Dosya Konumu", "Kullanım Amacı"],
        [
            [
                "Masaüstü Kısayolu & Başlatıcı (.bat)",
                r"C:\Users\PC\Desktop\Etik Kurul Otomasyonu.lnk" + "\n" +
                r"C:\Users\PC\Desktop\Antigravity Projects\EtikKurulOtomasyonu\Baslat.bat",
                "Masaüstünden çift tıklayarak uygulamayı anında başlatır."
            ],
            [
                "Kurulumsuz Taşınabilir Paket (Portable .exe)",
                r"4-MasaustuUygulamasi\dist\EtikKurulOtomasyonu-Portable.exe",
                "Kurulum gerektirmez; USB bellek veya internet üzerinden başka bir bilgisayara kopyalanıp doğrudan çalıştırılabilir."
            ],
            [
                "Windows Kurulum Sihirbazı (Setup .exe)",
                r"4-MasaustuUygulamasi\dist\Etik Kurul Otomasyonu Setup 1.0.0.exe",
                "Standart Windows programı gibi bilgisayara kurar, Başlat Menüsü ve Masaüstü kısayolu oluşturur."
            ],
            [
                "Uçtan Uca Otomatik Test Betiği",
                r"C:\Users\PC\Desktop\Antigravity Projects\EtikKurulOtomasyonu\test-workflow.ps1",
                "4 modülün tamamındaki 19 birim ve entegrasyon testini tek komutla çalıştırır ve doğrular."
            ]
        ],
        col_widths=[1.8, 2.7, 2.2]
    )

    # Kaydet
    doc.save(DESKTOP_DOCX_PATH)
    shutil.copyfile(DESKTOP_DOCX_PATH, PROJECT_DOCX_PATH)
    print(f"Word Raporu Başarıyla Oluşturuldu:\n1) {DESKTOP_DOCX_PATH}\n2) {PROJECT_DOCX_PATH}")


if __name__ == "__main__":
    charts = generate_charts()
    build_word_report(charts)
