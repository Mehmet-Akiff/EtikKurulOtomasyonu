# -*- coding: utf-8 -*-
"""
Etik Kurul Otomasyonu - Akademik Atıflı Literatür Taraması + Teknik Mimari ve Doğrulama Raporu Üreticisi (.docx)
"""

import os
import re
import shutil
import zipfile
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
UPLOADED_DOCX = r"C:\Users\PC\.gemini\antigravity\brain\1d83398f-1d2c-47c4-a929-0bee756b01ff\.user_uploaded\media_1792569765316_20b8e4f4.docx"
DESKTOP_DOCX_PATH = r"C:\Users\PC\Desktop\Etik_Kurul_Otomasyonu_Teknik_Raporu.docx"
PROJECT_DOCX_PATH = os.path.join(BASE_DIR, "Etik_Kurul_Otomasyonu_Teknik_Raporu.docx")

os.makedirs(CHART_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def extract_literature_images():
    lit_images = {}
    mapping = {
        "word/media/image3.png": os.path.join(CHART_DIR, "lit_fig_01_tat.png"),
        "word/media/image10.png": os.path.join(CHART_DIR, "lit_fig_02_ux_ai.png"),
        "word/media/image11.png": os.path.join(CHART_DIR, "lit_fig_03_chat_irb.png"),
    }
    if os.path.exists(UPLOADED_DOCX):
        with zipfile.ZipFile(UPLOADED_DOCX, 'r') as z:
            for src_name, dst_path in mapping.items():
                if src_name in z.namelist():
                    with open(dst_path, 'wb') as f:
                        f.write(z.read(src_name))
                    lit_images[src_name] = dst_path
    return lit_images


def generate_technical_charts():
    # Grafik 1: Modüler Mimari ve İş Akışı
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

    for x1, x2 in [(2.4, 2.9), (4.9, 5.4), (7.4, 7.8)]:
        ax.annotate("", xy=(x2, 3.45), xytext=(x1, 3.45),
                    arrowprops=dict(arrowstyle="->", color="#1e293b", lw=2.5))

    desktop_rect = plt.Rectangle((0.4, 0.45), 9.3, 1.5, facecolor="#312e81", edgecolor="#c7d2fe", linewidth=2, zorder=3)
    ax.add_patch(desktop_rect)
    ax.text(5.05, 1.2,
            "MODÜL 4: WINDOWS MASAÜSTÜ UYGULAMASI (Electron + Gömülü İş Akışı Motoru)\n"
            "Setup (.exe) & Portable (.exe) | IPC Güvenli Köprü | Otomatik Durum Onarımı (reconcileState) | Yerel Kalıcı JSON Veritabanı",
            color="white", fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=4)

    for cx in [1.4, 3.9, 6.4, 8.75]:
        ax.annotate("", xy=(cx, 2.6), xytext=(cx, 1.95),
                    arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.8, ls="--"))

    ax.set_title("Şekil 4: Geliştirilen Etik Kurul Otomasyonu Çok Katmanlı Modüler Mimari ve Veri Akış Şeması",
                 fontsize=11.5, fontweight="bold", color="#0f172a", pad=10)
    plt.tight_layout()
    chart1_path = os.path.join(CHART_DIR, "chart_01_architecture.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close(fig)

    # Grafik 2: Akıllı Otomatik Dosya Atama Algoritması Puanlama Simülasyonu
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    members = [
        "Prof. Dr. Kerem Yaman\n(Biyomedikal / YZ - 1 Dosya)",
        "Prof. Dr. Selim Vural\n(Tıp / Klinik - 1 Dosya)",
        "Dr. Öğr. Üyesi Burcu Polat\n(Tıp / Halk Sağlığı - 0 Dosya)",
        "Doç. Dr. Aylin Çelik\n(Psikoloji - 1 Dosya)",
        "Prof. Dr. Murat Doğan\n(Hukuk / Sosyal - 0 Dosya)",
        "Doç. Dr. Zeynep Kaya\n(Eğitim Bilimleri - 1 Dosya)"
    ]
    scores_biomed = [90, 90, 100, -10, 0, -10]
    colors = ["#16a34a" if s >= 90 else "#94a3b8" for s in scores_biomed]

    y_pos = np.arange(len(members))
    bars = ax.barh(y_pos, scores_biomed, color=colors, height=0.55, edgecolor="#1e293b", linewidth=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(members, fontsize=9)
    ax.invert_yaxis()
    ax.axvline(0, color="#334155", linewidth=1)
    ax.set_xlim(-25, 125)
    ax.set_xlabel("Algoritma Uygunluk Puanı: Skor = (Uzmanlık Eşleşmesi × 100) − (Aktif Dosya Yükü × 10)", fontsize=9.5, fontweight="bold")
    ax.set_title("Şekil 5: 'Tıp / Biyomedikal' Başvurusu İçin Otomatik Raportör Seçim ve Yük Dengeleme Puanları",
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

    # Grafik 3: Başvuru Değerlendirme Kriterleri ve Karar Eşik Analizi
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
    ax.set_title("Şekil 6: Kurul Üyesi Çok Kriterli Etik Değerlendirme Puanları ve Karar Dağılımı",
                 fontsize=11, fontweight="bold", color="#0f172a")
    ax.axhline(4.0, color="#16a34a", linestyle="--", alpha=0.6, label="Onay Referans Eşiği (4.0+)")
    ax.legend(loc="upper right", fontsize=8.5, ncol=2)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    chart3_path = os.path.join(CHART_DIR, "chart_03_evaluation_scores.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close(fig)

    # Grafik 4: Modül Bazlı Otomatik Birim ve Entegrasyon Test Sonuçları
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

    plt.suptitle("Şekil 14: Uçtan Uca Kalite Güvencesi ve Birim Test Doğrulama Metrikleri", fontsize=11.5, fontweight="bold", y=1.01)
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


def add_styled_table(doc, caption_text, headers, rows, col_widths=None, header_bg="1E3C72"):
    if caption_text:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        cap.paragraph_format.space_before = Pt(8)
        cap.paragraph_format.space_after = Pt(4)
        c_run = cap.add_run(caption_text)
        c_run.bold = True
        c_run.font.size = Pt(9.5)
        c_run.font.name = "Segoe UI"
        c_run.font.color.rgb = RGBColor(30, 60, 114)

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(header_text)
        run.bold = True
        run.font.size = Pt(9)
        run.font.name = "Segoe UI"
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_shading(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.1
            add_text_with_citations(p, str(val), font_size=8.8, bold_first=(c_idx == 0))
            set_cell_shading(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=85, bottom=85, left=120, right=120)
            row_cells[c_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    doc.add_paragraph()
    return table


def add_text_with_citations(paragraph, text, font_size=10, bold_first=False):
    """
    Metin içindeki [1], [2, 6], [14] gibi köşeli parantezli akademik atıfları
    koyu mavi ve akademik formatta vurgulayarak paragrafa ekler.
    """
    parts = re.split(r'(\[\d+(?:[–\-,\s]+\d+)*\])', text)
    for part in parts:
        if not part:
            continue
        run = paragraph.add_run(part)
        run.font.name = "Segoe UI"
        run.font.size = Pt(font_size)
        if re.match(r'^\[\d+(?:[–\-,\s]+\d+)*\]$', part):
            run.bold = True
            run.font.color.rgb = RGBColor(30, 60, 114)
        else:
            if bold_first:
                run.bold = True
                run.font.color.rgb = RGBColor(15, 23, 42)
            else:
                run.font.color.rgb = RGBColor(31, 41, 55)


def add_academic_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.18
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Inches(0.25)
    add_text_with_citations(p, text, font_size=10, bold_first=False)
    return p


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    h.paragraph_format.space_after = Pt(4)
    for run in h.runs:
        run.font.name = "Segoe UI"
        if level == 1:
            run.font.size = Pt(14.5)
            run.font.color.rgb = RGBColor(30, 60, 114)
        elif level == 2:
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(2, 132, 199)
        else:
            run.font.size = Pt(10.8)
            run.font.color.rgb = RGBColor(15, 118, 110)
    return h


def add_figure(doc, image_path, caption_text, width_inches=6.2):
    if not image_path or not os.path.exists(image_path):
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(image_path, width=Inches(width_inches))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    add_text_with_citations(cap, caption_text, font_size=9, bold_first=True)


REFERENCES_LIST = [
    (1, "Reducing the Single IRB Burden: Streamlining Electronic IRB Systems.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC9035281/"),
    (2, "Mann, S. et al. (2025). Chat-IRB? How application-specific language models can enhance research ethics review.", "https://www.researchgate.net/publication/394319889_Chat-IRB_How_application-specific_language_models_can_enhance_research_ethics_review"),
    (3, "University of Kentucky Office of Research Integrity. IRB Frequently Asked Questions | UK Research.", "https://research.uky.edu/office-research-integrity/faqs/irb"),
    (4, "Edith Cowan University (ECU). Research Ethics Management System (REMS) Proportional Review Checklist User Manual.", "https://intranet.ecu.edu.au/__data/assets/pdf_file/0016/807100/ECU-REMS-Proportional-Review-Checklist-User-Manual.pdf"),
    (5, "Mkumbwa, S. et al. (2025). Going paperless: the strengths and limitations of electronic research ethics information management system (PubMed).", "https://pubmed.ncbi.nlm.nih.gov/39754181/"),
    (6, "Mkumbwa, S. et al. (2025). Going paperless: the strengths and limitations of electronic research ethics information management system in Tanzania.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC11697796/"),
    (7, "RHInnO Ethics Platform. Expert-Decision Support System for Research Ethics Committees.", "https://www.rhinno.app/about_us"),
    (8, "Directory of Open Access Journals (DOAJ). Going paperless: electronic research ethics information management systems.", "https://196.43.162.77/Record/doaj-art-2580422c72504460ab653887c867735f?sid=1500045"),
    (9, "Chulalongkorn University Research Ethics Committee (CUREC). Assessing satisfaction and performance of the CUREC electronic submission system.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC12910995/"),
    (10, "Seneka Yazılım / ONAYLARIM. Etik Kurul Başvurularında e-İmza ve Dijital Onay (5070 Sayılı Elektronik İmza Kanunu Uygulamaları).", "https://seneka.com.tr/blog/etik-kurul-basvurusu-islak-imza-elden-teslim"),
    (11, "University of Arizona Research. Human Subjects Protection Program (HSPP) & eIRB / Kuali Research.", "https://research.arizona.edu/tags/human-subjects-protection-program-hspp?page=1"),
    (12, "Bian, J. et al. CLARA: an integrated clinical research administration system.", "https://www.researchgate.net/publication/261956542_CLARA_an_integrated_clinical_research_administration_system"),
    (13, "Mkumbwa, S. et al. (2025). Going paperless: the strengths and limitations of electronic REIMS in a health training institution in Tanzania.", "https://www.researchgate.net/publication/387708240_Going_paperless_the_strengths_and_limitations_of_electronic_research_ethics_information_management_system_in_a_health_training_institution_in_Tanzania"),
    (14, "University of California, Irvine (UC Irvine) Office of Research. Post-Review Responsibilities & ZOT IRB System.", "https://research.uci.edu/human-research-protections/post-review-responsibilities/"),
    (15, "Rutgers University / NJ ACTS. Electronic IRB Review Performance During COVID-19 Surge.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC9161045/"),
    (16, "Boston University Medical Campus (BUMC). IRB Review Times and User Satisfaction (INSPIR II Analytics).", "https://www.bumc.bu.edu/irb/bumcirb/irb-review-time/"),
    (17, "Johns Hopkins University / JScholarship. Digital Modernization of VA IRB Processes: Designing an Integrated e-IRB Architecture.", "https://jscholarship.library.jhu.edu/server/api/core/bitstreams/7315e5ec-45c1-4607-8f20-70e08fb80bfe/content"),
    (18, "University of Pennsylvania (Penn IRB). eIRB Frequently Asked Questions & Proxy Access Management.", "https://irb.upenn.edu/homepage/faqs/eirb-faqs/"),
    (19, "Netiket Bilişim. Çoklu Etik Kurul Başvuru ve Değerlendirme Otomasyonu (e-Devlet SSO & Otomatik Karar Şablonu).", "https://www.netiket.com.tr/services/etik-kurul"),
    (20, "Korea Disease Control and Prevention Agency (KDCA) (2026). Introduction to the Revised Standard Operating Procedures of the Institutional Review Board.", "https://eng.phwr.org/journal/view.html?doi=10.56786/PHWR.2026.19.5.3"),
    (21, "Bioethics & Science Portal. Navigating IRB Expedited Review for Minor Changes: A Researcher's Guide to Efficient Protocol Modifications.", "https://www.bioethicssci.com/posts/navigating-irb-expedited-review-for-minor-changes-a-researchers-guide-to-efficient-protocol-modifications"),
    (22, "SciSpace Agents. Institutional Review Board (IRB) Checklist & Automated Protocol Compliance Guide.", "https://scispace.com/agents/institutional-review-board-irb-checklist-8ahhkxg6"),
    (23, "University of Kentucky Office of Research Integrity (ORI). Frequently Asked Questions on Electronic Submissions.", "https://research.uky.edu/office-research-integrity/faqs"),
    (24, "Implementation of single IRB review for multisite human subjects research: Turnaround time benchmarks.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10225260/"),
    (25, "Medical College of Wisconsin (MCW). The Real-Time IRB: A Collaborative Innovation to Decrease Turnaround Time.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6146014/"),
    (26, "Advarra Clinical Research. Choosing Your Electronic IRB System: A Guide for Research Sites and CTMS Integration.", "https://www.advarra.com/blog/choosing-your-electronic-irb-system-a-guide-for-sites/"),
    (27, "Fibi Research (2025). Simplifying IRB Agreements: Step-by-Step Implementation Guide for Multisite Reliance.", "https://fibiresearch.com/simplifying-irb-agreements-step-by-step-implementation-guide-for-2025/"),
    (28, "Garcia, M. B. Can You Use AI After Research Ethics Approval? Post-Approval Governance Guide.", "https://manuelgarcia.info/guides/research/guide/ai-use-after-research-ethics-approval"),
    (29, "University of the East (UE). Development and Evaluation of UE – Research Management System Using ISO/IEC 25010.", "https://ejournals.ph/article.php?id=34074"),
    (30, "ProQuest Dissertations. To Investigate the Impact of Data Privacy Regulation on Disclosure and Ethics Compliance.", "https://search.proquest.com/openview/8832aff4db5e444f898d115212ebb8a4/1?pq-origsite=gscholar&cbl=18750&diss=y"),
    (31, "NDLI / PubMed Central. Using Design Principles to Foster Understanding of Complex Health Research Protocols.", "https://ndl.iitkgp.ac.in/re_document/pubmed_central/1234567_pubmed/3041449"),
    (32, "Mayo Clinic Cancer Center. Building a Protocol Expressway: Concurrent Sub-Processes and Lean Redesign in IRB Review.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2727289/"),
    (33, "Notes from the Field: Jumpstarting the IRB Approval Process in Multicenter Studies.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC1955279/"),
    (34, "Regulatory Support Improves Subsequent IRB Approval Rates in 'Not Ready for Review' (NRR) Submissions.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6309298/"),
    (35, "Cambridge Core / JCTS (2026). Evaluation of the National Dental PBRN Central IRB Since Its Inception in 2014 Until 2025.", "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5F43C7B5E99F71D7E467FAF25140D50F/S2059866126107286a.pdf"),
    (36, "Northern Illinois University (NIU) Theses. Technology Acceptance Model (TAM) in Academic Digital Systems.", "https://huskiecommons.lib.niu.edu/cgi/viewcontent.cgi?article=7770&context=allgraduate-thesesdissertations"),
    (37, "Exploring Researchers' Perspectives on Institutional Review Boards Functions in Saudi Arabia: A Survey Utilizing the IRB-RAT Tool (2025).", "https://www.researchgate.net/publication/389027806_Exploring_Researchers'_Perspectives_on_Institutional_Review_Boards_Functions_in_Saudi_Arabia_A_Survey_Utilizing_the_IRB-RAT_Tool"),
    (38, "Kwon, S. et al. / Taylor & Francis (2025). Guidelines needed for the use of AI in the preparation or review of IRB, IBC, and IACUC applications.", "https://www.tandfonline.com/doi/full/10.1080/08989621.2025.2612564"),
    (39, "Researcher awareness and submission practices to ethics committees via electronic portals (2025).", "https://pmc.ncbi.nlm.nih.gov/articles/PMC12895601/"),
    (40, "Equinet Africa (2025). Digital Research Ethics Governance in Resource-Limited Settings.", "https://www.equinetafrica.org/newsletter/issue/2025-03-01.html"),
    (41, "Equinet Africa. Monitoring Equity and Research Policy in African Health Institutions.", "https://www.equinetafrica.org/newsletter/category/508.html"),
    (42, "Challenges and recommendations to improve institutional review boards' review of community-engaged research proposals: A scoping review.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC10130837/"),
    (43, "ResearchGate Preprint. Challenges and recommendations to improve IRBs' review of community-engaged research (CBPR/CEnR).", "https://www.researchgate.net/publication/369713390_Challenges_and_recommendations_to_improve_institutional_review_boards'_review_of_community-engaged_research_proposals_A_scoping_review"),
    (44, "Journal of Clinical and Translational Science (Cambridge Core). Improving IRB Review of Community-Engaged Research Proposals.", "https://www.cambridge.org/core/journals/journal-of-clinical-and-translational-science/article/challenges-and-recommendations-to-improve-institutional-review-boards-review-of-communityengaged-research-proposals-a-scoping-review/2E3A9779B7B8511B32D24824C666C0E2"),
    (45, "Cambridge Core. From paper to screen: regulatory and operational considerations for modernizing the informed consent process (eConsent).", "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B4D780788F74A0F56A1421111E98B151/S205986612200379Xa.pdf"),
    (46, "PubMed Central (PMC). From paper to screen: regulatory and operational considerations for electronic informed consent.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC9257776/"),
    (47, "SciSpace Archive. Collaborative Online Architectures and User Interaction Metrics.", "https://scispace.com/pdf/egress-online-towards-leveraging-massively-multiplayer-4w5eholwxw.pdf"),
    (48, "NIH StrokeNet Experience (Cambridge Core). Ten years of Central IRB review for an NIH-funded large clinical trial network by an academic IRB.", "https://www.cambridge.org/core/journals/journal-of-clinical-and-translational-science/article/ten-years-of-central-irb-review-for-an-nihfunded-large-clinical-trial-network-by-an-academic-irb-the-nih-strokenet-experience/2654F9122344F923B3460EE901D8A330"),
    (49, "Şırnak Üniversitesi Etik Kurulu Başkanlığı. Etik Kurula Başvuruda Bulunurken Dikkat Edilmesi Gereken Hususlar ve EBYS Süreci.", "https://etikkurulu.sirnak.edu.tr/tr/aktivite/etik-kurulu-baskanligina-basvuruda-bulunurken-dikkat-edilmesi-gereken-hususlar/44513"),
    (50, "Ege Üniversitesi Klinik Araştırmalar Etik Kurulu (KAEK). Elektronik Başvuru ve Süreç Takip Portalı.", "https://kaek.ege.edu.tr/"),
    (51, "Klinik Araştırmalar Derneği (KAD). TİTCK ve Etik Kurul Onay Süreçleri Sıkça Sorulan Sorular.", "https://www.klinikarastirmalar.org/Home/SSS"),
    (52, "Ondokuz Mayıs Üniversitesi (OMÜ). Etik Kurul Süreçlerinde Dijital Dönüşüm Adımı.", "https://www.omu.edu.tr/tr/icerik/haber/etik-kurul-sureclerinde-dijital-donusum-adimi"),
    (53, "İzmir Kâtip Çelebi Üniversitesi (İKÇÜ). ÜBYS Entegre Sağlık Araştırmaları Etik Kurulu Bilgi Sistemi.", "https://etik.ikcu.edu.tr/S/21717/saglik-arastirmalari-etik-kurulu-formlar"),
    (54, "Ankara Sosyal Bilimler Üniversitesi (ASBÜ). ÖBS Üzerinden Tez Konusu ve Etik Kurul Başvuruları El Kitabı.", "https://sbe.asbu.edu.tr/sites/enstituler/sbe.asbu.edu.tr/files/2023-08/tez-konusu-oneri-basvurusu-el-kitabi_3.pdf"),
    (55, "EİMZACI. Öğrenci ve Akademisyenler İçin Nitelikli Elektronik İmza (NES): EBYS ve YÖKSİS Entegrasyonları.", "https://eimzaci.com/ogrenciler-akademisyenler-icin-e-imza/"),
    (56, "Türkiye İlaç ve Tıbbi Cihaz Kurumu (TİTCK) (2025). Klinik Araştırma Başvuru Kılavuzu.", "https://portal.aifd.org.tr/wp-content/uploads/2025/12/TITCK-Klinik-Arastirma-Arastirmaci-Toplantisi-Basvuru-Kilavuzu-01.12.2025-Rev-02-002.pdf"),
    (57, "Ankara Medipol Üniversitesi. Girişimsel Olmayan Klinik Araştırmalar Etik Kurulu Kontrol Listeleri ve Taahhütnameleri.", "https://www.ankaramedipol.edu.tr/akademik/arastirma-etik-kurullari/girisimsel-olmayan-klinik-arastirmalar-etik-kurulu"),
    (58, "Netiket. Üniversite ve Kamu Süreç Otomasyon Yazılımları.", "https://www.netiket.com.tr/services"),
    (59, "Assan Bilişim A.Ş. Kurumsal İş Akışı (eBA) ve Dijital Dönüşüm Yazılım Hizmetleri.", "https://www.assanbilisim.com.tr/tr-tr/hizmetler/dijital-hizmetler/yazilim-gelistirme-hizmetleri"),
    (60, "Model İstatistik. Akademik Çalışmalarda Etik Kurul Başvurusu Nasıl Hazırlanır?", "https://modelistatistik.com/blog/etik-kurul-basvuru-rehberi"),
    (61, "Sivas Cumhuriyet Üniversitesi Tıp Fakültesi (GÖKAEK). Etik Kurul Başvuru Rehberi.", "https://tip.cumhuriyet.edu.tr/userfiles/32/files/Kurul%20Rehberi(1).pdf"),
    (62, "Dicle Üniversitesi. Etik Kurul Otomasyon Portalı (etik.otomasyon.dicle.edu.tr).", "https://etik.otomasyon.dicle.edu.tr/"),
    (63, "Hacettepe Üniversitesi. Klinik Araştırmalar Etikosistem Portalı (kaekdev).", "https://kaekdev.hacettepe.edu.tr/"),
    (64, "Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği (2026). Akademik Otomasyon Proje Listesi.", "https://webadmin.selcuk.edu.tr/uploads/Contents/teknoloji-bilgisayar_muhendisligi/duyuruO/82937/BMU_Proje_Listesi_16092026190421.pdf"),
    (65, "Model İstatistik. Türkiye Etik Kurul Sistemi: Kurumsal Yapı ve Mevzuat Çerçevesi.", "https://modelistatistik.com/blog/turkiye-etik-kurul-sistemi"),
    (66, "Selçuk Üniversitesi. Etik Kurul Yönergesi ve Dijital Başvuru Süreçleri.", "https://selcuk.edu.tr/birim/sayfa/5350/etik-kurul-166"),
    (67, "MDPI Information (2025). Large Language Models in Medicine: Systematic Review Using QUADAS-AI.", "https://www.scribd.com/document/882148167/information-16-00489-v2-1"),
    (68, "Mann, S. et al. (2025). Chat-IRB? How application-specific language models can enhance research ethics review. Journal of Medical Ethics (BMJ).", "https://jme.bmj.com/content/early/2025/12/14/jme-2025-110845"),
    (69, "Researcher.Life Discovery (2025). Guidelines needed for the use of AI in the preparation or review of IRB, IBC and IACUC applications.", "https://discovery.researcher.life/article/guidelines-needed-for-the-use-of-ai-in-the-preparation-or-review-of-irb-ibc-and-iacuc-applications/39bd05fa96ae39149ad0885a5adf1456"),
    (70, "ResearchGate. The IRB Structure and Medical Research Reform.", "https://www.researchgate.net/publication/324162504_The_IRB_structure_and_medical_research_reform"),
    (71, "PubMed (2025). Chat-IRB? Application-Specific Language Models in Research Ethics Governance (PMID: 40764013).", "https://pubmed.ncbi.nlm.nih.gov/40764013/"),
    (72, "DergiPark / Manas Sosyal Araştırmalar Dergisi (MJSS). Bilimsel Araştırmalarda Yapay Zekâ Kullanımı Etik İlkeleri.", "https://dergipark.org.tr/en/pub/mjss/article/1663647"),
    (73, "Lehigh University Research Integrity. Guidance: Generative AI and Human Subjects Research.", "https://research.lehigh.edu/policies-guidance-forms/guidance-generative-ai-and-human-subjects-research"),
    (74, "MDPI AI (2026). Human Evaluation of Large Language Models: A Review of Construct Mismatch and Multi-Dimensional Rubrics.", "https://www.mdpi.com/2673-2688/7/5/174")
]


def build_word_report(lit_images, tech_charts):
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(31, 41, 55)

    # =========================================================================
    # AKADEMİK KAPAK BÖLÜMÜ
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(10)
    r_top = title_p.add_run("T.C. AKADEMİK VE BİLİMSEL ARAŞTIRMALAR\nETİK KURUL OTOMASYON SİSTEMLERİ\n\n")
    r_top.bold = True
    r_top.font.size = Pt(18)
    r_top.font.color.rgb = RGBColor(30, 60, 114)

    r_sub = title_p.add_run(
        "Mimari Evrim, Operasyonel Verimlilik, Birlikte Çalışabilirlik, Yapay Zekâ Entegrasyonu\n"
        "ve Çok Katmanlı Modüler Otomasyon Yazılımı (ASP.NET Core, PHP, Node.js, Electron)\n"
        "Tasarım, Uygulama ve Doğrulama Akademik Raporu"
    )
    r_sub.bold = True
    r_sub.font.size = Pt(12.5)
    r_sub.font.color.rgb = RGBColor(2, 132, 199)

    add_styled_table(
        doc,
        "Tablo 1: Akademik Araştırma ve Yazılım Projesi Künye Bilgileri",
        ["Künye Parametresi", "Akademik ve Teknik Detaylar"],
        [
            ["Rapor / Çalışma Başlığı", "Etik Kurul Otomasyon Sistemleri: Kapsamlı Literatür Taraması ve Çok Katmanlı Modüler Otomasyon Yazılımı Tasarımı"],
            ["Yazar / Geliştirici", "Mehmet Akif Ürey"],
            ["Atıf ve Kaynakça Standardı", "Numaralı Akademik Atıf Formatı ([1] – [74] Uluslararası ve Ulusal Hakemli Literatür)"],
            ["Yazılım Mimarisi (4 Modül)", "1) ASP.NET Core 9 + MSSQL/SQLite (Başvuru & Evrak Modülü)\n2) PHP 8.3 + MySQL/SQLite (Akıllı Otomatik Dosya Atama & Değerlendirme Modülü)\n3) Node.js + MongoDB (Karar, Revizyon & Kriptografik QR Belge Modülü)\n4) Electron Masaüstü Uygulaması (Setup .exe & Portable .exe)"],
            ["Resmi Yazılım Deposu", "https://github.com/Mehmet-Akiff/EtikKurulOtomasyonu (Sürüm: v1.1.0)"],
            ["Deneysel Doğrulama", "Toplam 19/19 Otomatik Birim ve Uçtan Uca İş Akışı Testi (%100 Başarı Oranı)"],
            ["Tarih", "21 Ekim 2026"]
        ],
        col_widths=[2.0, 4.6]
    )

    # ÖZET (ABSTRACT)
    add_heading_styled(doc, "ÖZET", level=2)
    add_academic_paragraph(
        doc,
        "Bu çalışmada, bilimsel araştırmaların insan ve hayvan özneler üzerindeki etik, hukuki ve metodolojik uygunluğunu "
        "denetleyen Etik Kurul Otomasyon Sistemlerinin (eIRB / REIMS / REMS) tarihsel gelişimi, regülasyon uyumluluğu, "
        "operasyonel dönüş süreleri (Turnaround Time - TAT), birlikte çalışabilirlik (sIRB) sorunları, Türkiye'deki "
        "mevzuat ekosistemi ve üretken yapay zekâ (RAG tabanlı Chat-IRB) entegrasyonları 74 ulusal ve uluslararası "
        "kaynak ışığında incelenmiştir [1, 2, 6, 9, 10, 19]. Literatür bulguları doğrultusunda, kağıt tabanlı ve "
        "kopuk süreçlerin yarattığı darboğazları ortadan kaldırmak amacıyla dört katmanlı modüler bir Etik Kurul "
        "Otomasyonu yazılımı tasarlanmış ve gerçeklenmiştir: (1) ASP.NET Core 9 ve MSSQL tabanlı dijital başvuru ve "
        "SHA-256 evrak doğrulama modülü, (2) PHP 8.3 ve MySQL tabanlı uzmanlık eşleşmesi ve iş yükü dengelemeli "
        "otomatik raportör atama ve kriter puanlama modülü, (3) Node.js ve MongoDB tabanlı otomatik kurul kararı, "
        "revizyon takibi ve 24 haneli kriptografik doğrulama kodlu / QR kodlu resmi karar belgesi üretim modülü ve "
        "(4) son kullanıcıların sunucu kurulumuna ihtiyaç duymadan çalıştırabileceği Windows 11 masaüstü uygulaması "
        "(.exe). Geliştirilen sistem, 19 bağımsız birim ve entegrasyon testi ile doğrulanmış ve %100 başarı sağlamıştır."
    )
    kw_p = doc.add_paragraph()
    kw_p.paragraph_format.space_after = Pt(10)
    r_kw1 = kw_p.add_run("Anahtar Kelimeler: ")
    r_kw1.bold = True
    r_kw1.font.size = Pt(9.5)
    r_kw2 = kw_p.add_run(
        "Etik Kurul Otomasyonu, e-IRB, Araştırma Etiği Yönetim Sistemi (REIMS), Otomatik Raportör Atama, "
        "Kriptografik Belge Doğrulama, ASP.NET Core, PHP, Node.js, Electron, Yapay Zekâ Karar Destek (Chat-IRB)."
    )
    r_kw2.italic = True
    r_kw2.font.size = Pt(9.5)

    doc.add_page_break()

    # =========================================================================
    # BÖLÜM 1: KAPSAMLI LİTERATÜR TARAMASI (AKADEMİK ATIFLI)
    # =========================================================================
    add_heading_styled(
        doc,
        "1. Etik Kurul Otomasyon Sistemleri: Mimari Evrim, Operasyonel Verimlilik, Birlikte Çalışabilirlik ve Yapay Zekâ Entegrasyonu Üzerine Kapsamlı Literatür Taraması",
        level=1
    )

    # 1.1
    add_heading_styled(doc, "1.1. Kavramsal Çerçeve ve Dijital Dönüşümün Tarihsel Evrimi", level=2)
    add_academic_paragraph(
        doc,
        "Bilimsel araştırmaların insan ve hayvan özneler üzerindeki etik, hukuki ve metodolojik uygunluğunu denetleyen "
        "kurumsal yapıların dijitalleşmesi, modern araştırma yönetişiminin en kritik kırılma noktalarından birini "
        "oluşturmaktadır [1]. Uluslararası literatürde Elektronik Kurumsal İnceleme Kurulu (Electronic Institutional "
        "Review Board - eIRB veya e-IRB), Araştırma Etiği Bilgi Yönetim Sistemi (Research Ethics Information Management "
        "System - REIMS) ve Araştırma Etiği Yönetim Sistemi (Research Ethics Management System - REMS) kavramlarıyla "
        "tanımlanan etik kurul otomasyonları; araştırma protokollerinin sunulması, ön incelemeden geçirilmesi, hakem ve "
        "kurul üyelerine dağıtılması, revizyon döngülerinin yönetilmesi, onay sonrası izleme süreçlerinin yürütülmesi "
        "ve kurumsal arşivlemenin sağlanması amacıyla tasarlanmış uzmanlaşmış yazılım mimarileridir [1, 4, 5]. Bazı "
        "gelişmiş kurumsal örneklerde bu sistemler yalnızca bir evrak kayıt aracı olarak kalmamakta, RHInnO Ethics "
        "platformunda olduğu gibi bireysel araştırma etiği kurulları için doğrudan birer uzman karar destek sistemi "
        "(expert-decision support system) işlevi üstlenmektedir [7]."
    )
    add_academic_paragraph(
        doc,
        "Geleneksel kağıt tabanlı (paper-based) etik kurul yönetiminden elektronik otomasyonlara geçiş, yalnızca "
        "çevresel veya lojistik bir tercih değil, bilimsel üretimin hızını ve kalitesini doğrudan etkileyen yapısal "
        "bir zorunluluktur [6, 8]. Kağıt tabanlı süreçler; uzun değerlendirme ve dönüş süreleri (turnaround time - TAT), "
        "araştırmacılar üzerinde biriken yüksek baskı, çoğaltma ve kargo maliyetleri, fiziksel imzaların toplanmasındaki "
        "coğrafi engeller, dosyaların fiziksel transfer sırasında kaybolma riski ve kilitli dolaplara dayalı hantal "
        "arşivleme mekanizmaları nedeniyle ciddi darboğazlar üretmektedir [6, 10, 13]. Otomasyon sistemlerinin devreye "
        "girmesiyle birlikte bu süreçler kağıtsız (paperless) bir iş akışına taşınmış; araştırmacı eğitimi doğrulaması, "
        "çıkar çatışması (Conflict of Interest - COI) ve bağlılık (Conflict of Commitment - COC) beyanları, protokol "
        "versiyon kontrolü ve advers olay bildirimleri tekil bir veri tabanı üzerinde bütünleştirilmiştir [1, 11]."
    )
    add_academic_paragraph(
        doc,
        "Literatürdeki ampirik veriler, etik kurul otomasyonlarının küresel ölçekte kurumsal standart haline geldiğini "
        "göstermektedir [1]. İnsan Araştırmalarını Koruma Programları Akreditasyon Derneği (AAHRPP) tarafından akredite "
        "edilmiş etik kurulların %91'i toplantı ve inceleme materyallerini dağıtmak için bir e-IRB sistemi kullanmakta, "
        "%74'ü çevrimiçi başvuru kabul etmekte ve yine %74'ü protokol değerlendirme süreçlerini tamamen çevrimiçi "
        "sistemler üzerinden yürütmektedir [1]. Ancak bu sistemlerin tarihsel evrimi incelendiğinde, ilk nesil "
        "otomasyonların ciddi mimari sınırlılıklar barındırdığı görülmektedir [12]. Örneğin, erken dönem kurumsal "
        "sistemlerden olan ARIA ve CRIMSON, etik kurul ve bağlı denetim birimlerinin verimliliğini artırmış olmakla "
        "birlikte; arka uç (back-end) veri tabanlarının ölçeklenebilirlik sorunları ve kurum içi diğer veri kaynaklarıyla "
        "bütünleşme eksiklikleri nedeniyle zamanla yetersiz kalmıştır [12]. Bir klinik araştırmanın yalnızca etik "
        "kuruldan değil, aynı zamanda bütçe, sözleşme, radyasyon güvenliği ve biyogüvenlik gibi çoklu idari birimlerden "
        "onay alması gerektiği gerçeği; CLARA, Huron eIRB, Kuali Research, INSPIR II ve ZOT IRB gibi uçtan uca "
        "bütünleşik klinik araştırma yönetim sistemlerinin doğmasına zemin hazırlamıştır [11, 12, 14, 15, 16]."
    )

    # 1.2
    add_heading_styled(doc, "1.2. Sistem Mimarisi, Regülasyon Uyumluluğu ve Temel İş Akışı Modülleri", level=2)
    add_academic_paragraph(
        doc,
        "Modern bir etik kurul otomasyonunun yazılım mimarisi, doğrusal bir belge yükleme portalından ziyade, araştırma "
        "risk profiline göre şekillenen dinamik bir kural motoru (rule engine) üzerine inşa edilmektedir [3]. Kentucky "
        "Üniversitesi'nin E-IRB ve Arizona Üniversitesi'nin eDisclosure sistemlerinde görüldüğü üzere, güncel platformlar "
        "aşamalı akıllı formlar (progressive smart forms) kullanmaktadır [3, 11]. Araştırmacının 'Protokol Türü' "
        "aşamasında yaptığı seçimler (örneğin; Tıbbi Etik Kurul vs. Tıbbi Olmayan Etik Kurul veya Tam Kurul İncelemesi "
        "vs. Hızlandırılmış İnceleme vs. Muafiyet İncelemesi), sistemin arka planda hangi veri alanlarını açıp "
        "hangilerini gizleyeceğini ve hangi ek belgeleri zorunlu kılacağını otomatik olarak belirlemektedir [3]. Bu "
        "dinamik dallanma mimarisi, araştırmacının kendi çalışmasıyla ilgisi olmayan bürokratik sorularla karşılaşmasını "
        "önleyerek bilişsel yükü azaltmakta ve ilk başvurudaki hata oranlarını düşürmektedir [3, 23]."
    )
    add_academic_paragraph(
        doc,
        "Sistem mimarisinin ikinci temel sütununu, rol tabanlı erişim kontrolü, vekalet yönetimi ve otomatik "
        "zamanlayıcılar oluşturmaktadır [9, 18]. Pensilvanya Üniversitesi (UPenn) eIRB sisteminde uygulanan 'Uzakta Olma "
        "Süresi Ekle' (Add Away Period) ve vekil erişimi (proxy access) fonksiyonları, başaraştırmacının (PI) veya "
        "kurul üyesinin kurum dışında olduğu dönemlerde tüm sistem görevlerinin belirlenen bir başka kullanıcıya "
        "otomatik olarak devredilmesini sağlayarak kurumsal süreçlerin kesintiye uğramasını engellemektedir [18]. "
        "Benzer şekilde, Tayland'daki CUREC elektronik sistemi üzerine yapılan incelemeler, manuel takip ve kilitli "
        "dosya dolaplarından oluşan geleneksel yapının; sunucu tabanlı dijital güvenlik, hakem son değerlendirme "
        "tarihlerinden 3 gün önce ve sonra otomatik gönderilen hatırlatma e-postaları ve yıllık devam incelemelerinden "
        "(continuing review) 30 gün önce tetiklenen otomatik uyarı mekanizmalarıyla ikame edildiğini ortaya koymaktadır [9]."
    )

    add_styled_table(
        doc,
        "Tablo 2: Uluslararası Etik Kurul İnceleme Kategorileri, Otomasyon İş Akışları ve Dönüş Süresi (TAT) Kıyaslamaları [3, 11, 14–16, 20, 24, 25]",
        [
            "Süreç / İnceleme Kategorisi",
            "Kapsam ve Hedef Araştırma Profili",
            "Otomasyon İş Akışı ve Karar Mekanizması",
            "Uluslararası Kurumsal Dönüş Süresi (TAT) Kıyaslamaları"
        ],
        [
            [
                "Muafiyet İncelemesi\n(Exempt Review)",
                "Kamuya açık veriler, kimliksizleştirilmiş mevcut örnekler veya minimal risk barındıran eğitim/davranış araştırmaları [20].",
                "Akıllı form üzerinden otomatik kategori doğrulaması; kurul başkanı veya atanmış tekil uzman onayı; onay sonrası küçük değişikliklerde yeniden başvuru muafiyeti [11].",
                "• KDCA (Kore): 2–3 gün [20]\n• Boston Üniv. (INSPIR II): 9 gün (75. yüzdelik) [16]\n• Rutgers Üniv.: 11 gün (medyan) [15]\n• Kentucky Üniv.: 4–6 hafta [3]"
            ],
            [
                "Hızlandırılmış İnceleme\n(Expedited Review)",
                "Minimal riskli prospektif biyolojik örnek alımı (belirli hacim/sıklık sınırları dahilinde kan, tükürük vb.), onaylı ilaç/cihazların etiket içi kullanımı, küçük protokol değişiklikleri [20, 21].",
                "Sürekli (rolling) başvuru kabulü; kurul başkanı veya alt komite üyelerine otomatik atama; revizyonlarda hakeme 10 iş günü inceleme süresi tanımlanması [14].",
                "• KDCA (Kore): 2–3 gün [20]\n• Boston Üniv. (INSPIR II): 7 gün (75. yüzdelik) [16]\n• Optimize e-IRB Genel: < 2 hafta [24]\n• Kentucky Üniv.: 4–6 hafta [3]"
            ],
            [
                "Tam Kurul İncelemesi\n(Full / Regular Board)",
                "Minimal riskin üzerindeki girişimsel araştırmalar, hassas/kırılgan popülasyonları içeren çalışmalar, yeni ilaç (IND) veya tıbbi cihaz (IDE) araştırmaları [14].",
                "Toplantı tarihinden ~10 gün önce gündemin sistemde kapatılması; tüm üyelere dijital dağıtım; çoğunluk nisabı (quorum) ve kurum dışı üye katılımıyla oylama [3].",
                "• Boston Üniv. (INSPIR II): 17 gün (75. yüzdelik) [16]\n• MCW Gerçek Zamanlı e-IRB: 18,76–27,8 gün [25]\n• KDCA (Kore): < 60 gün (ayda bir döngü) [20]\n• MCW Standart e-IRB: 63 gün (ortalama) [25]"
            ],
            [
                "Devam İncelemesi\n(Continuing Review / CR)",
                "Minimal riskin üzerindeki veya FDA/DOJ denetimine tabi devam eden araştırmaların en az yılda bir kez periyodik denetimi [3].",
                "Süre bitiminden 30 gün önce otomatik bildirim; CR onaylanmadan sistemin yeni değişiklik (modification) başvurularını kilitlemesi; düşük riskli çalışmalarda 15 dakikalık kısaltılmış idari form [3].",
                "• UC Irvine (ZOT IRB): 3–4 hafta (sürekli/rolling bazda) [14]\n• Süre aşımında protokolün sistem tarafından otomatik askıya alınması [3]"
            ],
            [
                "Advers Olay ve Sapma Bildirimi\n(UP / RNI / AE)",
                "Beklenmeyen sorunlar (Unanticipated Problems), ciddi advers reaksiyonlar (SUSAR/UADE) ve acil protokol sapmaları [3].",
                "ZOT IRB gibi sistemlerde RNI (Reportable New Information) modülü üzerinden acil bildirim; kurul başkanı/başkan yardımcısı tarafından anlık triyaj değerlendirmesi [14].",
                "• Acil prospektif sapma: 96 saat içinde bildirim [14]\n• UP bildirimi: 5 iş günü içinde [14]\n• Sponsor UADE raporu: 10 iş günü içinde [14]"
            ]
        ],
        col_widths=[1.3, 1.7, 1.8, 1.8]
    )

    add_academic_paragraph(
        doc,
        "Tablo 2'de özetlenen iş akışlarının hukuki geçerliliği, otomasyon sistemlerinin ulusal ve uluslararası "
        "regülasyon standartlarına tam uyum sağlamasına bağlıdır [20]. Elektronik kayıtların ve elektronik imzaların "
        "güvenilirliğini düzenleyen ABD Gıda ve İlaç Dairesi'nin 21 CFR Part 11 standardı, Sağlık Sigortası "
        "Taşınabilirlik ve Sorumluluk Yasası (HIPAA) gizlilik kuralları, Ortak Kural (Common Rule - 45 CFR 46) ve "
        "yazılım kalitesini ölçen ISO/IEC 25010 standartları, e-IRB mimarilerinin temel referans noktalarıdır [17, 29, 30]. "
        "Özellikle denetim izi (audit trail) mekanizması kapsamında, her bir elektronik etik kurul kaydının beş temel "
        "bileşenle (protokol versiyonu, üye görüşleri, oylama kayıtları, onaylı onam formları ve yazışmalar) "
        "değiştirilemez biçimde ilişkilendirilmesi ve resmi saklama sürelerinin (retention period) çalışma kapanış "
        "raporunun sisteme yüklendiği tarihten itibaren otomatik olarak başlatılması zorunludur [14]."
    )
    add_academic_paragraph(
        doc,
        "Ayrıca sistemler arası veri akışı açısından, e-IRB yazılımlarının kurum içindeki Klinik Araştırma Yönetim "
        "Sistemleri (CTMS), iş zekâsı/raporlama araçları ve elektronik sağlık kaydı (EHR) sorgulama platformlarıyla "
        "entegre çalışabilmesi kritik bir tasarım kriteridir [26]. Kentucky Üniversitesi ve UC Irvine örneklerinde "
        "görüldüğü üzere, otomasyon sistemleri yalnızca onay öncesi süreci değil, onay sonrası (post-approval) yaşam "
        "döngüsünü de katı algoritmik kurallarla denetlemektedir [3, 14]. Örneğin, bir devam incelemesi (CR) sistemde "
        "onay beklerken araştırmacının aynı protokol üzerinde değişiklik talebi (modification request) göndermesi "
        "sistem tarafından otomatik olarak engellenmekte; benzer şekilde, 3 yıl veya daha uzun süre açık kaldığı halde "
        "hiçbir katılımcı kaydetmeyen veya veri toplamayan çalışmalar sistem tarafından tespit edilerek kapanış "
        "prosedürlerine (Study Closure SOP) yönlendirilmektedir [3]."
    )

    # 1.3
    add_heading_styled(doc, "1.3. Operasyonel Verimlilik, İşlem Süreleri (Turnaround Time) ve Süreç İyileştirme Dinamikleri", level=2)
    add_academic_paragraph(
        doc,
        "Literatürde etik kurul otomasyonlarının performansını değerlendirmek için kullanılan en temel nicel gösterge, "
        "başvurunun yapılmasından nihai kurul kararının (veya ilk inceleme görüşünün) araştırmacıya iletilmesine kadar "
        "geçen dönüş süresidir (Turnaround Time - TAT) [9]. Kağıt tabanlı veya standartlaştırılmamış yerel süreçlerde "
        "bu sürelerin öngörülemez boyutlara ulaştığı belgelenmiştir [17]. Örneğin, ABD hükümeti regülasyonlarına göre "
        "'hızlandırılmış inceleme' (expedited review) kapsamında değerlendirilmesi gereken tek bir standart protokolün "
        "45 farklı merkezde incelendiği çok merkezli bir çalışmada, yerel etik kurul onay sürelerinin 52 gün ile 798 "
        "gün arasında değiştiği saptanmıştır [33]. Benzer şekilde, büyük bir kentsel Gazi Sağlığı İdaresi (VA) tıp "
        "merkezinde iki yıllık süreçte yeni sunulan 103 protokolün süreç analizinde, toplam inceleme sürelerinin 16 ile "
        "631 takvim günü arasında dağıldığı ve bu devasa varyansın araştırma planlamasını imkânsız hale getirdiği "
        "görülmüştür [17]. Bir diğer çok merkezli araştırmada ise tam kurul incelemelerinin medyan 131 gün, "
        "hızlandırılmış incelemelerin ise 85 gün sürdüğü; 17 merkezli bir sağlık hizmetleri araştırmasının toplamda "
        "115 ayrı başvuru ve 6.700 saatin üzerinde personel mesaisi gerektirdiği kaydedilmiştir [27]."
    )
    add_academic_paragraph(
        doc,
        "Elektronik sistemlerin ve süreç yeniden tasarımının bu süreler üzerindeki etkisi incelendiğinde, literatür son "
        "derece kritik bir nedensel ilişkiyi ortaya koymaktadır: Yalnızca kağıt formları dijital ekranlara taşımak tek "
        "başına verimlilik sağlamamakta; asıl kazanım, otomasyonun eşzamanlı iş akışları, standartlaşma ve ön kontrol "
        "(triyaj) mekanizmalarıyla birleştirilmesiyle elde edilmektedir [17, 31, 32]. Nitekim kapsamlı bir protokol "
        "geliştirme ve inceleme birimi analizinde, iyileştirme öncesinde süreçteki 'katma değerli zaman oranının' "
        "(value-added ratio - gerçekte üretken olarak harcanan sürenin toplam süreye oranı) yalnızca %2 ile %12,6 "
        "arasında olduğu ve 'ilk seferde kalite' (first-time quality) oranının %0 olduğu, yani sunulan protokollerin "
        "%100'ünün yeniden işleme (rework) ve düzeltmeye ihtiyaç duyduğu tespit edilmiştir [32]. Birbirine bağımlı "
        "olmayan görevlerin eşzamanlı (concurrent) alt süreçler halinde paralel yürütülmesi ve üst akıştaki hataların "
        "eğitim ve standartlaşmayla sıfırlanması sonucunda; personel sayısı hiç artırılmadan dahili protokollerin "
        "ortalama tamamlanma süresi 25,00 haftadan 10,15 haftaya (P < 0,001), harici protokollerin süresi ise 20,61 "
        "haftadan 7,79 haftaya (P < 0,001) düşürülmüştür [32]. Daha da önemlisi, süreçteki varyans istatistiksel olarak "
        "anlamlı biçimde daraltılarak (dahili protokollerde P = 0,009; harici protokollerde P = 0,0002) 108 haftayı aşan "
        "öngörülemez gecikmeler tamamen ortadan kaldırılmış ve kontrol edilebilir bir operasyonel yapı kurulmuştur [32]."
    )
    add_academic_paragraph(
        doc,
        "Elektronik altyapının insan etkileşimiyle nasıl optimize edilebileceğine dair en yenilikçi model ise Wisconsin "
        "Tıp Fakültesi'nde geliştirilen 'Gerçek Zamanlı Etik Kurul' (Real-Time IRB) uygulamasıdır [25]. Araştırmacıların "
        "elektronik başvuru sistemini kullanarak eksiksiz dosya sunduğu, ancak olası revizyonların asenkron yazışmalar "
        "yerine kurul toplantısı sırasında araştırmacı ve komite arasında eşzamanlı/yüz yüze karara bağlandığı bu "
        "modelde; standart süreçte ortalama 63 takvim günü süren nihai onay süresi tüm gerçek zamanlı çalışmalarda "
        "ortalama 27,8 güne (medyan 21,5 gün), harici kurumsal sorunlar (bütçe ve sözleşme birimlerindeki gecikmeler) "
        "dışlandığında ise ortalama 18,76 güne düşerek toplam sürede %70 oranında bir azalma sağlamıştır [25]."
    )

    if "word/media/image3.png" in lit_images:
        add_figure(
            doc,
            lit_images["word/media/image3.png"],
            "Şekil 1: Süreç Standartlaşması ve Gerçek Zamanlı (Real-Time) e-IRB Tasarımının Onay Sürelerine Etkisi [25, 32]",
            width_inches=5.8
        )

    add_academic_paragraph(
        doc,
        "Literatürdeki bir diğer önemli bulgu, kağıt sistemden elektronik sisteme geçişin ilk aşamasında yaşanan "
        "'Geçiş Dönemi Paradoksu'dur [9]. Tayland'da CUREC elektronik başvuru sisteminin performansını üç dönemde — "
        "(1) Kağıt tabanlı dönem (Ocak–Aralık 2021), (2) Elektronik Faz I / Geçiş dönemi (Ocak 2022–Şubat 2024) ve "
        "(3) Elektronik Faz II / Tam uygulama dönemi (Mart–Aralık 2024) — Kruskal-Wallis testi ile karşılaştıran "
        "araştırmada, tüm inceleme türlerinin medyan dönüş süresinin Elektronik Faz I'de (geçiş döneminde) kağıt tabanlı "
        "döneme kıyasla arttığı, ancak sistemin tam olarak oturduğu Faz II'de (ve hızlandırılmış incelemelerde) anlamlı "
        "biçimde azaldığı saptanmıştır [9]. Benzer şekilde, Arizona Üniversitesi'nin yeni eIRB ve Kuali Research "
        "sistemlerine geçiş sürecinde görüldüğü üzere, kurumlar sistem devreye alınmadan (go-live) yaklaşık iki hafta "
        "önce hiçbir başvurunun kabul edilmediği planlı 'karartma dönemleri' (blackout periods) uygulamak zorunda "
        "kalmakta ve eski sistemdeki protokol belgeleri yeni sisteme otomatik aktarılamadığında (migration kısıtları) "
        "geçici operasyonel yavaşlamalar yaşanmaktadır [11]. Bu veriler, e-IRB kurulumlarının başlangıçta kurumsal "
        "öğrenme eğrisi ve hakem/komite yapısındaki adaptasyon süreçleri nedeniyle geçici bir sürtünme yarattığını, "
        "gerçek hız kazanımlarının ise ancak kurumsal olgunluk aşamasında (Faz II) ortaya çıktığını kanıtlamaktadır [9]. "
        "Nitekim Rutgers Üniversitesi'nin Huron eIRB sistemi üzerinden yürüttüğü 2019–2020 karşılaştırmalı analizi, "
        "olgunlaşmış bir elektronik altyapının kriz anlarındaki esnekliğini doğrulamaktadır: Mart 2020'deki COVID-19 "
        "acil durum kararının ardından başvuru hacminde yaşanan ani ve 15 ay süren devasa artışa rağmen, e-IRB iş akışı "
        "sayesinde hem COVID-19 hem de COVID-19 dışı tam kurul protokollerinde medyan onay süreleri ve uç değerler "
        "2019 yılına kıyasla daha da aşağı çekilmiştir [15]."
    )
    add_academic_paragraph(
        doc,
        "Öte yandan, onay sürelerindeki gecikmelerin kaynağını yalnızca etik kurul sekreteryasına veya hakemlere "
        "atfetmek yanıltıcıdır [23, 34]. Hızlandırılmış inceleme kapsamında onaylanan 593 çalışmanın incelendiği ampirik "
        "bir araştırmada, ilk başvurudan onaya kadar geçen toplam sürenin ortalama 57,0 gün (SS = 50,0) olduğu; ancak "
        "bu sürenin ortalama 21,9 gününde (SS = 34,1) başvurunun düzeltme veya eksiklik nedeniyle doğrudan araştırma "
        "ekibinin kendisinde beklediği belirlenmiştir [34]. Özellikle kıdemsiz öğretim üyeleri ve asistanlar "
        "(trainees/junior faculty) tarafından hazırlanan başvuruların kalitesi düşüktür [34]. Bu noktada e-IRB "
        "sistemlerine 'İncelemeye Hazır Değil' (Not Ready for Review - NRR) şeklinde bir ön triyaj mekanizması eklenmesi "
        "ve araştırmacılara regülasyon danışmanlığı verilmesi kritik rol oynamaktadır [34]. Danışmanlık desteği almayan "
        "NRR başvurularının %6,5'inin (n = 3) yeniden sunulduğunda tekrar NRR olarak reddedildiği, %13,0'ünün (n = 6) "
        "çözümsüz kaldığı ve %39,1'inin (n = 18) tamamen geri çekildiği görülmüştür [34]."
    )

    # 1.4
    add_heading_styled(doc, "1.4. Kullanıcı Deneyimi (UX), Teknoloji Kabulü ve Sosyo-Teknik Darboğazlar", level=2)
    add_academic_paragraph(
        doc,
        "Etik kurul otomasyonlarının teknik kapasitesi ne kadar yüksek olursa olsun, sistemin nihai başarısı "
        "araştırmacıların, kurul üyelerinin ve idari personelin sistemi nasıl deneyimlediği ve benimsediği ile doğrudan "
        "ilişkilidir [9, 36]. Literatürde bu sistemlerin kullanılabilirliğini (usability) ve hizmet kalitesini ölçmek "
        "için Sistem Kullanılabilirlik Ölçeği (System Usability Scale - SUS; 0–100 arası puanlanan 10 soruluk standart "
        "ölçek), Net Tavsiye Skoru (NPS), göz izleme (eye-tracking) analizlerindeki İlk Odaklanma Süresi (Time to First "
        "Fixation - TTF), Tıklama Oranı (CTR), Teknoloji Kabul Modeli (TAM) ve ISO/IEC 25010 yazılım kalite standartları "
        "gibi çok boyutlu metrikler kullanılmaktadır [17, 29, 36, 47]. Ayrıca genel etik kurul işlevlerini araştırmacı "
        "gözüyle değerlendirmek üzere Keith-Spiegel ve Koocher tarafından geliştirilen 45 maddelik IRB-RAT (IRB "
        "Researcher Assessment Tool) ölçeği, REDCap gibi güvenli elektronik veri tabanları üzerinden uygulanarak "
        "araştırmacıların 'ideal etik kurul' beklentileri ile 'mevcut sistem performansı' arasındaki farkları (7'li "
        "Likert ölçeğinde) ölçmektedir [37]. Nitekim Suudi Arabistan'da 53 kayıtlı etik kurulu kapsayan 2025 tarihli bir "
        "IRB-RAT araştırmasında, araştırmacıların en hayati bulduğu unsurun 'hakem ve komite önyargısının bulunmaması' "
        "(6,73 puan) olduğu; ideal ile mevcut durum arasındaki en küçük farkın 'insan katılımcıların korunması' "
        "(0,51 puan fark), en büyük açığın ise 'kurul başkanının deneyimli bir araştırmacı olması gerekliliği' "
        "(1,53 puan fark) maddesinde ortaya çıktığı belirlenmiştir [37]."
    )
    add_academic_paragraph(
        doc,
        "Elektronik platformlara geçişin kullanıcı memnuniyeti üzerindeki etkileri incelendiğinde, kurumsal olarak "
        "yapılandırılmış e-IRB sistemlerinin paydaşlar nezdinde yüksek kabul gördüğü, ancak kullanıcı grupları arasında "
        "dikkate değer bir algı farklılaşması yaşandığı gözlemlenmektedir [9]. CUREC elektronik sistemi üzerine yapılan "
        "çalışmada (toplam N = 125 katılımcı; uzman içerik geçerliliği IOC skoru araştırmacı anketi için 0,85, kurul "
        "üyeleri ve personel için 0,94), kurul üyelerinin %97,3'ü (%51,4 çok memnun, %45,9 memnun) sistemden memnuniyet "
        "duyarken, araştırmacılarda bu oran %80,0 (%28,2 çok memnun, %51,8 memnun; %18,8 kararsız ve %1,2 memnun değil) "
        "düzeyinde gerçekleşmiştir [9]. Sistemin en yüksek beğeni toplayan bileşenleri, bürokratik angaryayı doğrudan "
        "ortadan kaldıran 'sisteme kayıt süreci' (%93 memnun veya çok memnun) ile 'çevrimiçi onay sertifikası üretimi' "
        "(%92,3 memnun veya çok memnun) olmuştur [9]. Kurumsal e-IRB sistemlerinin bu yüksek performansına karşın, "
        "araştırmacıların karmaşık başvuru süreçlerini aşmak için başvurdukları doğrulanmamış genel amaçlı yapay zekâ "
        "araçları (Kwon vd., 2024 tarafından incelenen 42 uygulama) regülasyon gerekliliklerini karşılamada büyük "
        "ölçüde yetersiz kalmaktadır [38]."
    )

    if "word/media/image10.png" in lit_images:
        add_figure(
            doc,
            lit_images["word/media/image10.png"],
            "Şekil 2: Kurumsal e-IRB (CUREC) Paydaş Memnuniyet Dağılımı ve Mevcut Yapay Zekâ Araçlarının Yetkinlik Analizi [9, 38]",
            width_inches=5.8
        )

    add_academic_paragraph(
        doc,
        "CUREC sistemindeki olumlu tabloya rağmen, Boston Üniversitesi'nin INSPIR II sistemi üzerine yürüttüğü 2025 ve "
        "2026 yılı kullanıcı memnuniyeti anketleri (92 benzersiz protokolü kapsayan veriler), önemli bir tasarım "
        "paradoksunu açığa çıkarmaktadır [16]. Araştırmacıların %84'ü etik kurulun regülasyon engellerini aşmada "
        "yardımcı olduğunu ve %79'u revizyon taleplerinin açık ve anlaşılır olduğunu belirtirken, INSPIR II platformunun "
        "arayüz kullanılabilirliği (usability) kurumun en büyük sorun alanı olmaya devam etmiştir [16]. Bu durum, "
        "araştırmacıların etik kurulun kurumsal hizmetinden memnun olsalar dahi, karmaşık yazılım arayüzleriyle "
        "etkileşimde ciddi sürtünmeler yaşadıklarını göstermektedir [16]."
    )
    add_academic_paragraph(
        doc,
        "Literatürdeki nitel ve nicel araştırmalar, bu arayüz sürtünmelerinin ötesinde etik kurul otomasyonlarının "
        "beraberinde getirdiği derin sosyo-teknik darboğazları kapsamlı biçimde ortaya koymaktadır [6, 39]. İlk önemli "
        "darboğaz, deneyimsiz araştırmacıların metodolojik zayıflıklarının dijital ortamda büyümesi (amplification) "
        "olgusudur [39]. Endonezya, Malezya, Güney Afrika ve Suudi Arabistan'da yapılan çalışmalar, özellikle lisans ve "
        "lisansüstü öğrencilerin araştırma problemi tanımlama, metodoloji kurgulama ve etik ilkeleri operasyonelleştirme "
        "konusunda ciddi eğitim eksiklikleri bulunduğunu ve bu nedenle başvurularını defalarca yeniden sunmak "
        "(resubmission) zorunda kaldıklarını göstermektedir [39]. Dijital aracılı etik kurul sistemlerinde bu "
        "zayıflıklar azalmamakta, aksine daha da keskinleşmektedir; çünkü yeterli öğretici rehberlikten yoksun olan "
        "öğrenciler, karmaşık e-IRB arayüzlerinde gezinirken kavramsal bilgi ile operasyonel uygulama arasındaki "
        "boşlukta kaybolmaktadır [39]. Nitekim 2025 yılında Suudi Arabistan'da yürütülen kesitsel bir araştırmada, "
        "araştırmacıların etik farkındalıklarının keskin biçimde kutuplaştığı (%56,1 yüksek farkındalık, %37,8 düşük "
        "farkındalık ve yalnızca %6,0 orta düzey farkındalık) ve algılanan kurumsal destek ile e-IRB başvuru kolaylığı "
        "arasında istatistiksel olarak anlamlı fakat düşük büyüklükte (Cramer's V = 0,237) bir ilişki bulunduğu "
        "saptanmıştır [39]."
    )
    add_academic_paragraph(
        doc,
        "İkinci sosyo-teknik darboğaz, kaynak kısıtlı ortamlarda bilgi ve iletişim teknolojileri (BİT/ICT) altyapısına "
        "duyulan bağımlılık ve elektronik sistemlerin yarattığı iletişim kopukluğudur [6, 40, 41]. Tanzanya'daki "
        "Muhimbili Sağlık ve İlişkili Bilimler Üniversitesi'nde (MUHAS) hem kağıt tabanlı sistemi hem de REIMS "
        "otomasyonunu deneyimlemiş 16 öğretim üyesiyle yürütülen nitel ön-son değerlendirme çalışması (Mkumbwa vd., 2025), "
        "kağıtsız sisteme geçişin kayıt yönetimini iyileştirdiğini ve kullanım kolaylığı sağladığını doğrulamıştır [5, 6]. "
        "Ancak çalışma, gelişmekte olan ülkelerde kesintisiz internet ve sunucu altyapısına duyulan yüksek bağımlılığın "
        "yanı sıra, elektronik sistemin hakem ile araştırmacı arasındaki doğrudan etkileşimi sınırlandırdığını gün "
        "yüzüne çıkarmıştır [6, 13]. Benzer şekilde Gazi Sağlığı İdaresi (VA) tıp merkezi ihtiyaç analizlerinde de "
        "entegre olmayan dijital platformların araştırma ekipleri ile kurul arasında bir 'iletişim uçurumu' "
        "(communication divide) yaratarak önlenebilir hataları artırdığı vurgulanmıştır [17]."
    )
    add_academic_paragraph(
        doc,
        "Üçüncü temel darboğaz, geleneksel biyomedikal araştırmalar için kurgulanan kalıplaşmış e-IRB form yapılarının "
        "Toplum Temelli Katılımcı Araştırmaları (CBPR) ve Toplum Katılımlı Araştırmaları (CEnR) dışlamasıdır [42, 43, 44]. "
        "Sistematik kapsam incelemeleri, e-IRB sistemlerinin formülistik yaklaşımlarının toplum ortaklarını 'eşit "
        "araştırma ortağı' veya eş-yürütücü (co-PI) olarak tanımadığını, kurumsal güvenlik duvarları nedeniyle "
        "üniversite dışındaki toplum temsilcilerinin elektronik başvuru sistemine erişemediğini ve sistemin dayattığı "
        "uzun, teknik onam formu şablonlarının yerel topluluklarda güvensizlik yarattığını ortaya koymaktadır [42]. "
        "Bu darboğazı aşmak için e-IRB sistemlerini güncelleyerek toplum ortaklarına doğrudan portal erişimi ve CBPR "
        "şablonları sunan kurumlar, inceleme sürelerini anlamlı ölçüde kısaltmayı başarmıştır [44]. Bununla eşzamanlı "
        "olarak, modern e-IRB sistemleri yalnızca araştırmacının başvurusunu değil, katılımcının onam sürecini de "
        "elektronik bilgilendirilmiş onam (eConsent) modülleriyle dijitalleştirmeye başlamıştır [45, 46]."
    )

    # 1.5
    add_heading_styled(doc, "1.5. Çok Merkezli Araştırmalarda Tekil Etik Kurul (sIRB) Mandası ve Birlikte Çalışabilirlik Krizi", level=2)
    add_academic_paragraph(
        doc,
        "Etik kurul otomasyonları literatüründeki en derin yapısal kriz, çok merkezli araştırmalarda Tekil Etik Kurul "
        "(Single IRB - sIRB veya Central IRB - CIRB) modeline geçişle birlikte ortaya çıkmıştır [1, 24]. ABD Ulusal "
        "Sağlık Enstitüleri'nin (NIH) 25 Ocak 2018'de yürürlüğe giren sIRB politikası ve Ortak Kural düzenlemeleri, "
        "çok merkezli çalışmalarda her kurumun kendi yerel etik kurulunda mükerrer inceleme yapması yerine tek bir "
        "merkezî etik kurulun (Reviewing IRB) etik denetimi üstlenmesini ve diğer kurumların (Relying IRBs) bu karara "
        "dayanmasını (reliance) zorunlu kılmıştır [1]. Teorik olarak bürokrasiyi azaltması ve klinik araştırmaları "
        "hızlandırması beklenen bu reform, mevcut e-IRB yazılımlarının mimari yetersizlikleri nedeniyle pratikte yeni "
        "ve ağır bir idari yük doğurmuştur [1]."
    )
    add_academic_paragraph(
        doc,
        "Literatürdeki ampirik bulgular, bu uyumsuzluğun temelinde mevcut e-IRB sistemlerinin neredeyse tamamının yerel "
        "tekil kurum (Local IRB - LIRB) iş akışlarına, yerel popülasyon özelliklerine ve kurum içi fon kurallarına göre "
        "tasarlanmış olmasının yattığını göstermektedir [1]. Bir e-IRB sisteminin sIRB olarak görev yapabilmesi için; "
        "onlarca farklı araştırma merkeziyle yapılan güven/yetkilendirme anlaşmalarını (Reliance / Authorization "
        "Agreements) yürütmesi ve izlemesi, her merkezin kurumsal profilini ve yerel bağlam (local context) "
        "gereksinimlerini doğrulaması, yerel araştırmacıların eğitim ve çıkar çatışması bildirimlerini takip etmesi ve "
        "merkeze özgü onam formlarını ayrı ayrı yönetmesi gerekmektedir [1]. Mevcut e-IRB veri tabanları bu çok katmanlı "
        "ilişkisel yapıyı desteklemediği için, en gelişmiş elektronik sistemleri kullanan akademik etik kurul başkanları "
        "ve direktörleri dahi sistemin dışında harici Excel tabloları tutarak manuel geçici çözümlere (workarounds) "
        "başvurmak zorunda kaldıklarını bildirmektedir [1]."
    )
    add_academic_paragraph(
        doc,
        "Bu krizin ikinci boyutu, birlikte çalışabilirlik (interoperability) eksikliği ve siber güvenlik duvarlarıdır [1]. "
        "Farklı üniversitelerin kullandığı e-IRB yazılımları (veya aynı yazılımın farklı versiyonları) standartlaştırılmış "
        "bir veri formatı bulunmadığı için bilgisayardan bilgisayara (computer-to-computer) doğrudan iletişim "
        "kuramamaktadır [1]. Dahası, akademik kurumların katı veri güvenliği politikaları ve güvenlik duvarları "
        "(firewalls), dış kurumdaki bir araştırmacının incelemeyi yapan kurumun e-IRB sistemine doğrudan erişmesini "
        "engellemekte; erişim sağlansa dahi dış kullanıcılar aşina olmadıkları arayüzlerde hata yapmaktadır [1]. Sonuç "
        "olarak kurumlar, dış merkezlerdeki bilgileri manuel olarak toplayıp kendi e-IRB sistemlerine elle yeniden "
        "girecek özel irtibat personelleri (liaisons) görevlendirmekte; bu durum hem işgücü maliyetini artırmakta hem de "
        "manuel veri girişinden kaynaklanan transkripsiyon hatalarına yol açmaktadır [1]. Buna ek olarak, kurum "
        "hukukçularının sorumluluk, kişisel yaralanma tazminatları, sigorta ve HIPAA veri paylaşımı konularındaki "
        "incelemeleri, anlaşma süreçlerini aylarca geciktirmektedir [27]."
    )
    add_academic_paragraph(
        doc,
        "Bu sistemik izolasyonu aşmak amacıyla literatürde iki temel çözüm stratejisi gelişmiştir: Birincisi, kendi "
        "sIRB altyapısını yeniden mühendislik (reengineering) yoluyla kuracak finansal ve teknik kaynağa sahip olmayan "
        "kurumların çok merkezli incelemeleri ticari/bağımsız etik kurullara (commercial IRBs) devretmesi veya hibe "
        "bütçelerinde doğrudan maliyet (direct cost) kalemleri oluşturmasıdır [1]. İkincisi ve daha sürdürülebilir "
        "olanı ise, yerel e-IRB sistemlerinin üzerinde çalışan ulusal web tabanlı birlikte çalışabilirlik "
        "platformlarının kullanılmasıdır [27]. Özellikle SMART IRB (Master Common Reciprocal IRB Authorization Agreement "
        "ve Acceptance and Flexibility Agreement) çerçevesi ve IREx (IRB Reliance Exchange) ulusal web platformu; NIH "
        "StrokeNet ve Ulusal Diş Hekimliği Uygulama Temelli Araştırma Ağı (National Dental PBRN CIRB - 2014–2025 "
        "deneyimi) gibi büyük klinik araştırma ağlarında standart sözleşme şablonları ve merkezi evrak paylaşımı "
        "sağlayarak yerel e-IRB siloları arasındaki kopukluğu gidermektedir [27, 35, 48]."
    )

    # 1.6
    add_heading_styled(doc, "1.6. Türkiye'de Etik Kurul Otomasyon Ekosistemi, Mevzuat Uyumluluğu ve Uygulama Modelleri", level=2)
    add_academic_paragraph(
        doc,
        "Türkiye'deki yükseköğretim kurumları ve araştırma merkezlerinde etik kurul süreçlerinin dijitalleşmesi, "
        "uluslararası e-IRB literatürüyle paralel bir evrim göstermekle birlikte, ulusal kamu bilişim altyapısı ve "
        "yasal mevzuat çerçevesinde kendine özgü mimari modeller geliştirmiştir [10, 19, 65]. Geleneksel olarak "
        "araştırmacıların fiziksel çıktı alıp ıslak imza topladığı ve dosyaları elden veya kargo yoluyla sekreteryaya "
        "teslim ettiği klasik yapı; zaman kaybı, imza sırasının karışması, danışman veya ortak yürütücünün farklı "
        "şehir/ülkede bulunması nedeniyle sürecin durması ve belgelerin kargoda kaybolması gibi riskler nedeniyle hızla "
        "terk edilmektedir [10]."
    )
    add_academic_paragraph(
        doc,
        "Türkiye ekosistemindeki dijital dönüşümün hukuki ve teknik omurgasını 5070 sayılı Elektronik İmza Kanunu "
        "oluşturmaktadır [10, 55]. Bu kanun kapsamında üretilen Nitelikli Elektronik İmza (NES) ve mobil imza, ıslak "
        "imzalı fiziksel formlarla birebir aynı hukuki geçerliliğe sahiptir [10]. Üniversiteler ve yazılım "
        "geliştiriciler bu yasal zemini iki tamamlayıcı entegrasyon modeliyle etik kurul otomasyonlarına dahil "
        "etmektedir [10]. İlk yaklaşım olan araştırmacı odaklı bağımsız dijital onay modelinde (örneğin ONAYLARIM "
        "platformu), araştırmacılar başvuru formunu sisteme yükleyerek araştırma ekibindeki diğer imzacılara coğrafi "
        "bağımsızlık içinde sırayla imzalatabilmekte, dosyanın hangi imzacıda beklediğini anlık olarak izleyebilmekte "
        "ve dakikalar içinde tamamlanan elektronik imzalı belgeyi doğrudan etik kurula dijital olarak iletebilmektedir [10]. "
        "İkinci yaklaşım olan kurumsal arka uç API entegrasyonu modelinde (örneğin PrimeAPI) ise, kendi etik kurul "
        "başvuru otomasyonunu geliştirmiş olan üniversiteler sıfırdan e-imza altyapısı kurmak yerine dış servis "
        "sağlayıcıların API arayüzlerini kendi sistemlerine gömmektedir [10]. Bu sayede araştırmacı ve tez danışmanı, "
        "üniversitenin kendi portal arayüzünden ayrılmadan doğrudan nitelikli elektronik imzalı başvuru formu "
        "üretebilmekte, kurumlar da kullanıcı deneyimini koruyarak hukuki geçerliliği tam bir dijital onay döngüsü "
        "işletebilmektedir [10]."
    )

    add_styled_table(
        doc,
        "Tablo 3: Türkiye Etik Kurul Otomasyon Ekosistemi Mimari Katmanları ve Kurumsal Uygulama Modelleri [10, 19, 49–66]",
        [
            "Mimari Katman / Modül",
            "Türkiye Uygulama Ekosistemindeki Karşılığı ve Entegrasyon Biçimi",
            "Sağlanan Operasyonel ve Hukuki Kazanım",
            "Kurumsal ve Ticari Örnekler"
        ],
        [
            [
                "Kimlik Doğrulama ve Tekil Giriş (SSO)",
                "e-Devlet Kapısı, ÜBYS (Üniversite Bilgi Yönetim Sistemi) ve ÖBS (Öğrenci Bilgi Sistemi) entegrasyonu [19, 53, 54].",
                "Araştırmacının tek hesapla farklı kurullara başvurması; öğrenci başvurularında danışman onayının ÖBS üzerinden kağıtsız alınması [19, 54].",
                "İKÇÜ (ÜBYS Entegre) [53], ASBÜ (ÖBS Entegre) [54], Netiket (e-Devlet SSO) [19]"
            ],
            [
                "Elektronik İmza ve Resmi Yazışma",
                "5070 Sayılı Kanun (NES / Mobil İmza), EBYS (Elektronik Belge Yönetim Sistemi), YÖKSİS ve KEP entegrasyonu [10, 49, 55].",
                "Islak imza ve fiziksel kargo ihtiyacının sıfırlanması; coğrafi bağımsızlık; imza sırasının ('kimde bekliyor') anlık takibi [10].",
                "Şırnak Üniv. (EBYS) [49], Ege Üniv. KAEK [50], ONAYLARIM & PrimeAPI [10]"
            ],
            [
                "Çoklu Kurul Yönetimi (Multi-Tenant)",
                "'Bir Üniversite, Birden Çok Etik Kurul' mimarisi (Tıbbi, Girişimsel Olmayan, Sosyal Bilimler, Hayvan Deneyleri) [19, 57, 58].",
                "Her kurulun kendi çağrı takvimi, özel başvuru formu, kontrol listesi, sekreteryası ve üyeleriyle birbirine karışmadan tek sistemde çalışması [19].",
                "Netiket Etik Kurul Otomasyonu [19], Assan eBA İş Akışı Sistemleri [59]"
            ],
            [
                "Ön İnceleme, Hakemlik ve Karar Üretimi",
                "Sekreterya triyajı, otomatik protokol numarası atama, izole üye görüş ekranları ve şablondan otomatik karar yazısı üretimi [19, 60].",
                "Eksik dosyaların kurula ulaşmadan yakalanması; karar yazılarında başlık/protokol no yeniden yazım hatalarının önlenmesi; toplu ZIP çıktısı [19].",
                "Hacettepe Üniv. [63], Sivas Cumhuriyet Üniv. (GÖKAEK) [61], Dicle Üniv. [62], OMÜ [52], Selçuk Üniv. [64, 66]"
            ],
            [
                "Merkezi Regülasyon ve Klinik Denetim",
                "TİTCK (Türkiye İlaç ve Tıbbi Cihaz Kurumu) Klinik Araştırmalar Dairesi Başkanlığı standart formları ve onay süreçleri [51, 56].",
                "İlaç ve tıbbi cihaz klinik araştırmalarında etik kurul onayı sonrası TİTCK başlama izni ve ücret/form standartlarının sağlanması [51, 56].",
                "TİTCK Onaylı Klinik Araştırmalar Etik Kurulları (KAEK) [50, 51, 56]"
            ]
        ],
        col_widths=[1.4, 1.8, 1.8, 1.6]
    )

    add_academic_paragraph(
        doc,
        "Türkiye'deki üniversitelerin otomasyon mimarileri incelendiğinde, kurumsal yapıların hızla 'Çoklu Kurul "
        "(Multi-Tenant) Otomasyon Mimarisi'ne evrildiği görülmektedir [19, 58]. Bir üniversite bünyesinde Girişimsel "
        "Klinik Araştırmalar, Girişimsel Olmayan Araştırmalar, Sosyal ve Beşeri Bilimler ile Hayvan Deneyleri gibi görev "
        "alanı, üyeleri ve istediği belgeler birbirinden tamamen farklı birden çok etik kurul bulunmaktadır [19]. "
        "Gelişmiş yerli otomasyon yazılımlarında (örneğin Netiket Etik Kurul Başvuru Otomasyonu) her kurul kendi başvuru "
        "çağrısını, son başvuru tarihini, zorunlu belge kontrol listesini ve form şablonunu bağımsız olarak tanımlamakta; "
        "sekreterya yalnızca kendisine tanımlanan kurulun dosyalarını görürken, araştırmacı e-Devlet veya kurumsal "
        "hesabıyla tek bir ekrandan tüm başvurularını izleyebilmektedir [19]."
    )
    add_academic_paragraph(
        doc,
        "Bu sistemlerin iş akışı mühendisliği açısından getirdiği en önemli yeniliklerden biri, karar yazılarının "
        "başvuru verisinden otomatik olarak üretilmesidir [19]. Geleneksel süreçlerde sekreteryanın araştırma başlığını, "
        "yürütücü isimlerini ve protokol numarasını Word şablonlarına elle yeniden yazması (manual re-typing) hem zaman "
        "kaybına hem de maddi hatalara yol açarken; modern otomasyonlarda ön incelemeden geçen dosyaya sistem tarafından "
        "otomatik protokol numarası verilmekte, üyelerin izlenebilir görüşlerinin ardından nihai karar verildiğinde "
        "karar yazısı doğrudan başvurunun veritabanı kayıtlarından çekilerek kurul şablonu üzerinde otomatik "
        "oluşturulmakta ve protokol numarası/ad-soyad ile adlandırılmış toplu ZIP dosyaları halinde indirilebilmektedir [19]. "
        "İmzalanan nihai onay belgesi sisteme yüklendiğinde araştırmacı kendi ekranından belgesini anında "
        "indirebilmekte; Ankara Sosyal Bilimler Üniversitesi (ASBÜ) örneğinde olduğu gibi Öğrenci Bilgi Sistemi (ÖBS) "
        "üzerinden yürütülen tez etik kurul süreçlerinde enstitülere hiçbir fiziksel çıktı gönderilmesine gerek "
        "kalmamaktadır [19, 54]."
    )
    add_academic_paragraph(
        doc,
        "Üniversite bazlı uygulamalarda Ege Üniversitesi (KAEK Etik Kurul Başvuru Portalı), Dicle Üniversitesi "
        "(etik.otomasyon), Sivas Cumhuriyet Üniversitesi (GÖKAEK), Hacettepe Üniversitesi (kaekdev), İzmir Kâtip Çelebi "
        "Üniversitesi (ÜBYS entegre Etik Kurul Bilgi Sistemi), Ondokuz Mayıs Üniversitesi ve Selçuk Üniversitesi gibi "
        "kurumlar web tabanlı portallar üzerinden çevrimiçi başvuru, e-imza onayı ve anlık süreç takibi sağlamaktadır "
        "[50, 52, 53, 61, 62, 63, 64, 66]. Bununla birlikte, Hacettepe Üniversitesi örneğinde yıl sonu (Aralık ortası – "
        "Ocak başı) sistem kapatma dönemlerinin uygulanması ve Ankara Medipol Üniversitesi örneğinde olduğu gibi 2026 "
        "yılı itibarıyla revizyon notları, değişiklik talebi ve sonuç raporu taahhütnamelerinin standart kontrol "
        "listelerine bağlanması, Türkiye'deki elektronik sistemlerin de uluslararası literatürdeki dönemsel bakım/gündem "
        "kesintileri ve form standartlaşması süreçleriyle birebir aynı operasyonel dinamikleri yaşadığını "
        "göstermektedir [11, 57, 63]. İlaç ve tıbbi cihaz klinik araştırmalarında ise süreç iki aşamalı işlemekte; "
        "TİTCK onaylı Klinik Araştırmalar Etik Kurulu'ndan alınan elektronik onayın ardından, TİTCK Tıbbi Cihaz "
        "Onaylanmış Kuruluş ve Klinik Araştırmalar Dairesi Başkanlığı'na resmi başlama izni başvurusu yapılması zorunlu "
        "tutulmaktadır [51, 56]."
    )

    # 1.7
    add_heading_styled(doc, "1.7. Üretken Yapay Zekâ (GenAI), Büyük Dil Modelleri (LLM) ve Karar Destek Mimarilerinin Geleceği", level=2)
    add_academic_paragraph(
        doc,
        "2024–2026 yılları arasındaki güncel literatür, etik kurul otomasyonlarının salt 'iş akışı ve evrak yönlendirme' "
        "sistemlerinden, Doğal Dil İşleme (NLP) ve Büyük Dil Modelleri (LLM) ile güçlendirilmiş 'Bilişsel Karar Destek "
        "Sistemleri'ne doğru evrildiğini ortaya koymaktadır [2, 68, 71]. Bu dönüşüm iki farklı cephede eşzamanlı olarak "
        "yaşanmaktadır: Araştırmacıların başvuru hazırlarken yapay zekâ kullanması ve etik kurulların başvuruları "
        "değerlendirirken yapay zekâdan yararlanması [38, 69]."
    )

    add_heading_styled(doc, "1.7.1. Araştırmacı Cephesinde Yapay Zekâ Kullanımı ve Ampirik Kalite Krizi", level=3)
    add_academic_paragraph(
        doc,
        "Etik kurul başvurusu hazırlamak oldukça detaylı ve zaman alıcı bir süreç olduğundan, araştırmacılar protokol ve "
        "onam formu taslakları oluşturmak için giderek artan biçimde üretken yapay zekâ araçlarına yönelmektedir [38]. "
        "Örneğin, literatürde tanıtılan 'IRB Draft Generator' (Godwin vd., 2024) adlı araç; araştırmacıdan yalnızca dört "
        "temel girdiyi (kısa araştırma tanımı, hipotez, dahil etme/dışlama kriterleri ve çalışma tasarımı türü) almakta, "
        "ardından PubMed üzerinde otomatik bir literatür taraması gerçekleştirerek tam bir taslak protokol belgesi "
        "ürettiğini iddia etmektedir [38]. Benzer şekilde, yapay zekâ tarafından oluşturulan bilgilendirilmiş onam "
        "formlarının, insanlar tarafından yazılan onam formlarına kıyasla daha yüksek okunabilirlik (readability) "
        "skorlarına sahip olabildiği (Decker vd., 2023) ve SciSpace gibi platformların yapılandırılmış kontrol listesi, "
        "muafiyet şablonu ve değişiklik formları üreten ajanlar sunduğu bildirilmektedir [22, 38]."
    )
    add_academic_paragraph(
        doc,
        "Ancak Kwon ve çalışma arkadaşları (2024/2025) tarafından yürütülen sistematik bir inceleme, araştırmacıların "
        "kullandığı mevcut yapay zekâ araçlarının güvenilirliği konusunda çarpıcı bir gerçeği ortaya çıkarmıştır [38, 69]. "
        "ChatGPT üzerine inşa edilmiş ve araştırmacıların etik kurul başvurusu hazırlamasına yardımcı olduğunu iddia "
        "eden 42 farklı uygulamanın (IRB Guide, IRB Advisor vb.) ampirik olarak değerlendirildiği bu çalışmada; "
        "uygulamalardan yalnızca 4'ünün (%9,5) spesifik olarak etik kurul amaçları doğrultusunda eğitildiği (üstelik "
        "bunlardan birinin yalnızca tek bir onaylı onam formuyla eğitildiği) ve yalnızca 5 uygulamanın (%11,9) bir etik "
        "kurulun rolünü, incelediği araştırma türlerini ve standart bilgilendirilmiş onam gerekliliklerini doğru biçimde "
        "tanımlayabildiği saptanmıştır [38]. Bu bulgu, araştırmacıların doğrulanmamış genel amaçlı yapay zekâ araçlarına "
        "güvenerek hazırladıkları başvuruların, regülasyon gerekliliklerini karşılayacak doğru ve yeterli bilgiyi "
        "içermediğini ve etik kurulların iş yükünü azaltmak yerine niteliksiz başvuru yığınlarıyla artırdığını "
        "kanıtlamaktadır [38]."
    )

    add_heading_styled(doc, "1.7.2. Kurul Cephesinde 'Chat-IRB' ve Kurumsal Hafıza (RAG) Mimarisi", level=3)
    add_academic_paragraph(
        doc,
        "Etik kurulların kendi değerlendirme süreçlerinde karşılaştığı en temel yapısal sorunlardan biri, 'kurumsal "
        "hafıza eksikliği' (lack of institutional memory) olarak tanımlanmaktadır [2, 68]. Çoğu e-IRB sisteminde "
        "geçmişte incelenen protokollere, kurulun araştırmacılara yönelttiği sorulara ve tartışma/karar gerekçelerine "
        "dair aranabilir (searchable) bir anlamsal veritabanı bulunmamaktadır [2]. Bu eksiklik, benzer protokoller "
        "karşısında kurul kararlarının tutarsızlaşmasına (variability) ve inceleme sürelerinin uzamasına neden "
        "olmaktadır [2, 70]."
    )
    add_academic_paragraph(
        doc,
        "Mann ve çalışma arkadaşları (2025, Journal of Medical Ethics), bu sorunu çözmek üzere 'Chat-IRB' adını "
        "verdikleri, kuruma özgü (application-specific) büyük dil modeli mimarisini önermiştir [2, 68, 71]. Genel amaçlı, "
        "ticari ('off-the-shelf') dil modelleri etik kurul değerlendirmesi için uygun değildir; çünkü etik kurullar "
        "doğası gereği yereldir ve her kurumun kendine özgü misyonu, risk toleransı, yerel yasal düzenlemeleri ve hedef "
        "popülasyon hassasiyetleri bulunmaktadır [2]. Buna karşın, Erişim Destekli Üretim (Retrieval-Augmented "
        "Generation - RAG) ve ince ayar (fine-tuning) teknikleriyle; ilgili kurumun geçmiş etik kurul sorguları, komite "
        "tartışma tutanakları, geçmiş kararları, kurumsal standart çalışma prosedürleri (SOP) ve yerel mevzuatı üzerinde "
        "eğitilen bir 'Chat-IRB' sistemi çok boyutlu karar destek işlevleri üstlenebilmektedir [2, 68]. Bu mimari ilk "
        "aşamada ön tarama ve eksiklik kontrolü (pre-submission checks) gerçekleştirerek başvurunun tamlığını ve iç "
        "tutarlılığını kurul toplantısı öncesinde denetlemekte ve sekreterya yükünü hafifletmektedir [2]. İkinci "
        "aşamada protokoldeki olası etik ihlalleri tespit ederek etik risk bayraklaması (ethical red flags) yapmakta, "
        "hakemler için ön değerlendirme raporu üretmekte ve yeni başvurunun geçmiş kurul kararlarıyla tutarlılığını "
        "test etmektedir [2]. Üçüncü olarak ise özellikle sosyal ve davranışsal çalışmalarda bağlama duyarlı risk "
        "azaltma önerileri geliştirebilmekte; örneğin katılımcı mahremiyetini korumak amacıyla araştırmacıyla "
        "buluşulacak mekanların katılımcıyı ifşa etmeyecek şekilde seçilmesini veya araştırmacı iletişim bilgilerinin "
        "katılımcının yakınları tarafından 'araştırma kaynaklı' olduğu anlaşılmayacak bir formatta sunulmasını "
        "önerebilmektedir [68]."
    )

    if "word/media/image11.png" in lit_images:
        add_figure(
            doc,
            lit_images["word/media/image11.png"],
            "Şekil 3: RAG Tabanlı Chat-IRB Karar Destek Katmanı ve İnsan Döngüde (Human-in-the-Loop) Kurul Kararı Mimarisi [2, 10, 19, 68]",
            width_inches=5.8
        )

    add_heading_styled(doc, "1.7.3. Otomasyon Önyargısı, Değerlendirme Metrikleri ve Yapay Zekâ Yönetişimi", level=3)
    add_academic_paragraph(
        doc,
        "Yapay zekânın etik kurul otomasyonlarına entegrasyonu, beraberinde ciddi algoritmik ve etik riskler "
        "getirmektedir [38, 72]. Literatürde (2021–2024 yılları arasında 19 tıbbi uzmanlık alanındaki 84 LLM çalışmasını "
        "QUADAS-AI aracıyla inceleyen sistematik derlemeler dahil) genel NLP görevlerinde %90'ın üzerinde doğruluk "
        "bildirilirken, karmaşık tanı ve karar destek süreçlerinde doğruluğun %3'e kadar düşebildiği, halüsinasyon, "
        "şeffaflık eksikliği (opacity) ve güvenilirlik tutarsızlıklarının devam ettiği gösterilmiştir [38, 67]. Ayrıca "
        "karar vericilerin algoritmik çıktılara eleştirel süzgeç olmaksızın güvenmesi anlamına gelen 'otomasyon "
        "önyargısı' (automation bias), ayrımcılık yapmama ve şeffaflık ilkelerini tehdit etmektedir [38]."
    )
    add_academic_paragraph(
        doc,
        "Teknik açıdan, e-IRB sistemlerine entegre edilecek dil modellerinin performansını değerlendirirken BLEU, "
        "ROUGE, METEOR gibi yüzeysel kelime örtüşmesi metrikleri veya BERTScore ve perplexity gibi anlamsal benzerlik "
        "ölçümleri (Tier 1 otomatik metrikler) tek başına kullanılamaz [74]. Çünkü bu metrikler 'yapı uyumsuzluğu' "
        "(construct mismatch) yaşamakta; bir metnin olgusal doğruluğunu, akıl yürütme kalitesini veya etik kabul "
        "edilebilirliğini ölçememektedir [74]. Dolayısıyla etik kurul yapay zekâ sistemlerinin doğrulamasında alan "
        "uzmanlarının yürüttüğü çok boyutlu rubrik protokolleri, ikili karşılaştırmalar (pairwise comparisons) ve "
        "muhafazakâr karar eşikleri zorunlu tutulmaktadır [74]. En temel yönetişim ilkesi olarak literatürde tam bir "
        "mutabakat vardır: Etik planlama ve denetim, yapay zekâya devredilemeyecek temel insani değer yargıları (value "
        "judgments) içerdiğinden, nihai karar verici her zaman insan (Human-in-the-Loop) olmalıdır [2, 68]."
    )
    add_academic_paragraph(
        doc,
        "Son olarak, etik kurul otomasyonları yalnızca kendi iç süreçlerinde değil, onaylanan araştırmalarda "
        "araştırmacıların yapay zekâ kullanımını denetlemek üzere de yeni modüller geliştirmektedir [28, 73]. Lehigh "
        "Üniversitesi kılavuzları ve güncel regülasyon analizleri (Garcia), etik kurul onayı aldıktan sonra veri "
        "analizinde veya araştırma süreçlerinde üretken yapay zekâ kullanmak isteyen araştırmacıların sıkı bir yönetişim "
        "çerçevesine tabi olduğunu ortaya koymaktadır [28, 73]. Bu çerçeve uyarınca, insan öznelerden toplanan verilerin "
        "yapay zekâ modellerine aktarılmadan önce nasıl kimliksizleştirileceği (de-identification), olası yapay zekâ "
        "halüsinasyonlarının ve algoritmik önyargıların nasıl doğrulanacağı ve araştırma yöntemlerinin "
        "tekrarlanabilirliğinin (replicability) nasıl korunacağı e-IRB başvuru materyallerinde açıkça tanımlanmalıdır "
        "[73]. Veri güvenliği ihlallerini önlemek adına araştırmacılar gizli protokolleri veya katılımcı verilerini "
        "yetkisiz açık yapay zekâ servislerine yüklememeli, yalnızca kurumun ilgili veri sınıfı (örneğin Sınıf II veri "
        "güvenliği) için sözleşme imzaladığı kurumsal yapay zekâ ortamlarını kullanmalıdır [28, 73]. Halihazırda etik "
        "kurul onayı almış bir çalışmaya sonradan yapay zekâ araçlarının dahil edilmesi veya kullanılan yapay zekâ "
        "servis sağlayıcısının değiştirilmesi; veri işleme, saklama ve mahremiyet koşullarını farklılaştırarak "
        "çalışmanın etik risk dağılımını değiştirebileceğinden, araştırmacılar mevcut onayın bu değişiklikleri otomatik "
        "olarak kapsadığını varsaymamalı ve e-IRB sistemi üzerinden resmi protokol değişiklik (amendment) başvurusu "
        "gerçekleştirerek kurumsal onay almalıdır [28, 73]."
    )

    add_heading_styled(doc, "1.8. Sentez ve Stratejik Çıkarımlar", level=2)
    add_academic_paragraph(
        doc,
        "Etik kurul otomasyonları üzerine yapılan bu kapsamlı literatür taraması, dijitalleşmenin araştırma etiği "
        "yönetişiminde basit bir bürokratik modernizasyon olmadığını, bilimsel üretimin hızını, kalitesini ve çok "
        "merkezli işbirliği kapasitesini belirleyen stratejik bir altyapı unsuru olduğunu ortaya koymaktadır [1, 6]. "
        "Literatürdeki ampirik bulgular bütüncül olarak değerlendirildiğinde, bir e-IRB sisteminin onay sürelerini "
        "(TAT) gerçek anlamda kısaltabilmesi için yazılıma yalnızca form yükleme özelliği kazandırılmasının yeterli "
        "olmadığı, yazılım mimarisinin süreç mühendisliği ve etkin ön triyaj mekanizmalarıyla bütünleştirilmesi "
        "gerektiği anlaşılmaktadır [17, 32]. Başvuruların ortalama üçte birlik süreyi eksiklikler ve hatalar nedeniyle "
        "bizzat araştırma ekibinde bekleyerek geçirdiği gerçeği göz önüne alınarak [34]; otomasyon sistemleri zorunlu "
        "alan kontrolleri, aşamalı akıllı formlar, sekreterya ön triyajı (Not Ready for Review filtresi) ve kıdemsiz "
        "araştırmacılara yönelik yerleşik metodolojik/etik rehberlik modülleriyle donatılmalıdır [3, 34]. Ayrıca yüksek "
        "öncelikli veya karmaşık projelerde asenkron yazışma döngülerini ortadan kaldıran 'Gerçek Zamanlı Etik Kurul' "
        "(Real-Time IRB) gibi senkronize değerlendirme modelleri otomasyon iş akışlarına entegre edilerek değerlendirme "
        "varyansı kontrol altına alınmalıdır [25, 32]."
    )
    add_academic_paragraph(
        doc,
        "Kurumlar arası ölçekte ise en kritik stratejik öncelik, ulusal ve uluslararası birlikte çalışabilirlik "
        "(interoperability) standartlarının inşa edilmesidir [1, 27]. Türkiye'de TİTCK, YÖKSİS, EBYS ve üniversite "
        "otomasyonları arasında; uluslararası düzeyde ise SMART IRB ve IREx benzeri ağlar üzerinden standartlaştırılmış "
        "bir 'Etik Kurul Veri Değişim Protokolü' oluşturulmalı, ayrıca toplum katılımlı araştırmalarda (CBPR/CEnR) "
        "kurum dışı paydaşların güvenlik duvarlarına takılmadan sisteme ortak araştırmacı olarak dahil olabileceği esnek "
        "yetkilendirme katmanları kurulmalıdır [1, 10, 19, 42, 51]. Gelecek nesil etik kurul otomasyonlarının bilişsel "
        "omurgasını ise kurumsal hafıza destekli ve insan odaklı yapay zekâ (Human-in-the-Loop RAG) mimarileri "
        "oluşturacaktır [2, 68]. Etik kurul değerlendirme cephesinde, geçmiş kararları, kurul tartışmalarını ve yerel "
        "mevzuatı indeksleyen RAG tabanlı 'Chat-IRB' modelleri kurumsal hafızayı güçlendirmek, karar tutarlılığını "
        "sağlamak ve ön incelemeyi hızlandırmak için devreye alınmalı; ancak otomasyon önyargısını önlemek ve etik değer "
        "yargılarını korumak adına nihai muhakeme ve onay yetkisi mutlak surette insan kurul üyelerinde tutulmalıdır [2, 38, 68]."
    )

    # =========================================================================
    # BÖLÜM 2: GELİŞTİRİLEN ÇOK KATMANLI MODÜLER SİSTEM MİMARİSİ
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "2. Geliştirilen Çok Katmanlı Modüler Sistem Mimarisi ve Literatür Karşılıkları", level=1)
    add_academic_paragraph(
        doc,
        "Bölüm 1'deki literatür taramasında ortaya konulan mimari gereksinimler — özellikle erken dönem sistemlerin "
        "(ARIA, CRIMSON) yaşadığı ölçeklenebilirlik ve entegrasyon darboğazları [12], CUREC ve INSPIR II sistemlerinde "
        "incelenen dönüş süresi (TAT) ve kullanılabilirlik (UX) kriterleri [9, 16], 21 CFR Part 11 ile 5070 sayılı "
        "Elektronik İmza Kanunu kapsamındaki değiştirilemez denetim izi (audit trail) ve kriptografik belge doğrulama "
        "zorunluluğu [10, 14, 17] ve Netiket/ÜBYS örneklerindeki şablondan otomatik karar belgesi üretimi [19] — "
        "doğrudan referans alınarak bu projede 4 bağımsız modülden oluşan uçtan uca bir Etik Kurul Otomasyonu "
        "geliştirilmiştir. Şekil 4'te geliştirilen sistemin çok katmanlı mimarisi gösterilmiştir."
    )

    add_figure(doc, tech_charts[0], "Şekil 4: Geliştirilen Etik Kurul Otomasyonu Çok Katmanlı Modüler Mimari ve Veri Akış Şeması", width_inches=6.3)

    add_styled_table(
        doc,
        "Tablo 4: Geliştirilen Yazılım Modüllerinin Teknoloji Yığını ve Akademik Literatürdeki Karşılıkları",
        ["Modül Kodu ve Adı", "Teknoloji Yığını & Veritabanı", "Temel İşlevler", "Karşıladığı Literatür Gereksinimi"],
        [
            [
                "1-BasvuruModulu_DotNet",
                "C# / ASP.NET Core 9.0\nEF Core + MSSQL / SQLite\n(Port: 5001)",
                "Araştırmacı profil kaydı, yapılandırılmış dijital başvuru formu, PDF evrak yükleme, SHA-256 dosya özeti ve otomatik protokol numarası (ETIK-YYYY-XXXXX) üretimi.",
                "Kağıtsız başvuru (Paperless REIMS) [5, 6], aşamalı form doğrulaması [3] ve ön triyaj (NRR) eksiklik kontrolü [34]."
            ],
            [
                "2-DegerlendirmeModulu_PHP",
                "PHP 8.3 (PDO) MVC\nMySQL 8.x / SQLite\n(Port: 5002)",
                "Kurul üyelerinin uzmanlık ve aktif yük takibi, Akıllı Otomatik Dosya Dağıtım Algoritması, 3 kriterli (Metodoloji, Onam, Risk) 1-5 ölçeğinde puanlama.",
                "Hakem önyargısının önlenmesi (IRB-RAT) [37], uzmanlık uyumu ve otomatik iş yükü dengelemesi [9, 20]."
            ],
            [
                "3-KararVeBelgeModulu_Node",
                "Node.js + Express.js\nMongoDB + QRCode\n(Port: 5003)",
                "Nihai kurul kararı (Onay / Revizyon / Ret), revizyon takibi, 24 haneli SHA-256 doğrulama kodu, Base64 QR kodlu resmi HTML/PDF karar belgesi ve Audit Log.",
                "21 CFR Part 11 denetim izi [14, 17], 5070 sayılı e-İmza uyumu [10] ve şablondan otomatik sertifika üretimi (%92,3 memnuniyet) [9, 19]."
            ],
            [
                "4-MasaustuUygulamasi",
                "Electron 34 + Node.js\nWindows 11 Fluent UI\nNSIS Setup & Portable .exe",
                "3 arka uç modülünün tüm yeteneklerini yerel kalıcı veritabanı ve otomatik durum senkronizasyonu (reconcileState) ile tek masaüstü uygulamasında birleştirir.",
                "BİT/sunucu kesintilerine karşı yerel çalışma direnci [6, 13] ve yüksek arayüz kullanılabilirliği (SUS / ISO 25010) [16, 29]."
            ]
        ],
        col_widths=[1.4, 1.5, 1.9, 1.8]
    )

    # =========================================================================
    # BÖLÜM 3: MODÜL BAZLI MÜHENDİSLİK TASARIMI VE ALGORİTMALAR
    # =========================================================================
    add_heading_styled(doc, "3. Modül Bazlı Mühendislik Tasarımı, Algoritmalar ve Veri Modelleri", level=1)

    add_heading_styled(doc, "3.1. Modül 1: Başvuru ve Evrak İletim Modülü (ASP.NET Core 9 + MSSQL)", level=2)
    add_academic_paragraph(
        doc,
        "Modül 1, araştırmacıların akademik araştırma, tez veya projelerini sisteme kaydettiği giriş katmanıdır [3, 19]. "
        "Entity Framework Core üzerinde Researchers, Applications ve ApplicationDocuments varlıkları modellenmiş; "
        "kurumsal ortamda MSSQL Server üzerinden, yerel geliştirme ve test ortamlarında ise otomatik SQLite yedekleme "
        "(fallback) mekanizmasıyla kesintisiz çalışacak şekilde yapılandırılmıştır."
    )

    add_styled_table(
        doc,
        "Tablo 5: Modül 1 (ASP.NET Core 9 + MSSQL) REST API Uç Noktaları ve İşlevleri",
        ["HTTP Metodu & Endpoint", "Sınıf / Metot", "Teknik Açıklama"],
        [
            ["GET /api/applications", "ApplicationsController.GetAll()", "Tüm başvuruları araştırmacı ve yüklenen belgeleriyle birlikte listeler."],
            ["GET /api/applications/{protocol}", "ApplicationsController.GetByProtocol()", "Protokol numarasına (ETIK-2026-XXXXX) göre tekil başvuru detayını döner."],
            ["POST /api/applications", "ApplicationService.CreateApplicationAsync()", "Yeni başvuru oluşturur, benzersiz protokol numarası üretir ve veritabanına kaydeder."],
            ["POST /api/applications/{id}/documents", "ApplicationService.UploadDocumentAsync()", "Başvuruya ait PDF evraklarını SHA-256 dosya özeti (hash) ile kaydeder [14, 17]."],
            ["PATCH /api/applications/{protocol}/status", "ApplicationService.UpdateStatusAsync()", "Değerlendirme ve karar modüllerinden gelen bildirimle başvuru durumunu günceller."]
        ],
        col_widths=[2.1, 2.0, 2.5]
    )

    add_heading_styled(doc, "3.2. Modül 2: Akıllı Otomatik Dosya Atama ve Değerlendirme Modülü (PHP 8.3 + MySQL)", level=2)
    add_academic_paragraph(
        doc,
        "Literatürde IRB-RAT çalışmalarıyla vurgulanan 'hakem önyargısının önlenmesi ve uzmanlık uyumu' [37] ile "
        "inceleme dönüş sürelerinin (TAT) kısaltılması [9, 25] hedefleri doğrultusunda Modül 2'de deterministik bir "
        "otomatik dosya dağıtım algoritması geliştirilmiştir. Sistem, başvurunun çalışma alanını Türkçe karakter "
        "duyarlı (.toLocaleLowerCase('tr-TR') / mb_strtolower) anahtar kelimelere ayırmakta ve aktif kurul üyelerini "
        "şu matematiksel modelle puanlamaktadır:\n"
        "• Aday Uygunluk Skoru = (Uzmanlık Kelime Eşleşme Sayısı × 100) − (Üyenin Aktif Dosya Sayısı × 10)\n"
        "En yüksek puanlı 2 raportör otomatik olarak atanmakta, eşitlik halinde aktif dosya yükü daha az olan üyeye "
        "öncelik verilmektedir (Şekil 5)."
    )

    add_figure(doc, tech_charts[1], "Şekil 5: Akıllı Otomatik Dosya Dağıtım Algoritması Puanlama ve Yük Dengeleme Grafiği", width_inches=6.1)

    add_heading_styled(doc, "3.3. Modül 3: Karar, Revizyon ve Kriptografik QR Belge Modülü (Node.js + MongoDB)", level=2)
    add_academic_paragraph(
        doc,
        "CUREC araştırmasında kullanıcıların %92,3 oranında en yüksek memnuniyet bildirdiği modül olan 'çevrimiçi "
        "otomatik onay sertifikası üretimi' [9] ve Türkiye'deki otomasyonlarda aranan 'başvuru verisinden şablonla "
        "hatasız karar belgesi oluşturma' [19] gereksinimleri Modül 3'te hayata geçirilmiştir. Kurul üyesi 1–5 ölçeğinde "
        "3 temel kriteri (1: Metodoloji Uygunluğu, 2: Bilgilendirilmiş Onam ve Gönüllü Hakları, 3: Risk-Fayda Analizi) "
        "puanlayıp görüş bildirdiğinde, sistem ağırlıklı etik puan ortalamasını hesaplamakta (Şekil 6) ve SHA-256 "
        "tabanlı 24 haneli doğrulama kodu ile Base64 gömülü QR kod içeren resmi karar belgesini anında üretmektedir [10, 14]."
    )

    add_figure(doc, tech_charts[2], "Şekil 6: Kurul Üyesi Çok Kriterli Etik Değerlendirme Puanları ve Karar Dağılımı", width_inches=6.1)

    # =========================================================================
    # BÖLÜM 4: UYGULAMA İÇİ EKRAN GÖRÜNTÜLERİ
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "4. Uygulama İçi Gerçek Ekran Görüntüleri ve Uçtan Uca İş Akışı Doğrulaması", level=1)
    add_academic_paragraph(
        doc,
        "Aşağıdaki ekran görüntüleri (Şekil 7 – Şekil 13), geliştirilen Windows 11 masaüstü uygulamasının "
        "(4-MasaustuUygulamasi) canlı çalışma ortamından doğrudan alınmış olup, literatürde tanımlanan 6 temel "
        "e-IRB aşamasının (Genel Bakış, Başvuru, Otomatik Atama, Üye Değerlendirme, Karar & Sertifika Üretimi ve "
        "Kriptografik Doğrulama) uygulama içindeki işleyişini belgelendirmektedir [1, 3, 9, 19]."
    )

    screenshots_info = [
        (
            "01_dashboard.png",
            "Şekil 7: Sistem Genel Bakış (Dashboard) Sekmesi — Toplam başvuru, incelemedeki dosyalar, onaylanan kararlar "
            "(2 Onaylı Karar) ve her başvuru için durum bazlı 'Hızlı İşlem' butonları [9, 16]."
        ),
        (
            "02_application.png",
            "Şekil 8: Yeni Etik Kurul Başvurusu Sekmesi — Sorumlu araştırmacı seçimi, satır içi 'Yeni Araştırmacı Ekle' "
            "paneli, uzmanlık alanı seçimi ve otomatik eklenen dijital protokol/onam belgeleri [3, 19]."
        ),
        (
            "03_assignment.png",
            "Şekil 9: Otomatik Atama Sekmesi — Atama bekleyen başvurular, kurul üyelerinin aktif dosya yükleri ve alt "
            "kısımda yer alan 'Atanmış Dosyalar ve Raportör İnceleme Durumu' takip tablosu [9, 37]."
        ),
        (
            "04_evaluation.png",
            "Şekil 10: Kurul Üye Değerlendirme & Puanlama Sekmesi — Metodoloji, Bilgilendirilmiş Onam ve Risk-Fayda "
            "kriterleri (1-5 puan), üye karar tercihi ve 'Tamamlanan Üye Değerlendirmeleri' geçmiş tablosu [4, 20]."
        ),
        (
            "05_decision.png",
            "Şekil 11: Nihai Kurul Kararları & Belgeler Sekmesi — Onaylanan ve revizyon verilen başvuruların karar "
            "numaraları, etik puan ortalamaları, doğrulama kodları ve Hızlı Kurul Başkanlığı Kararı tablosu [14, 19, 25]."
        ),
        (
            "06_certificate.png",
            "Şekil 12: Otomatik Oluşturulan QR Kodlu Resmi Etik Kurul Karar Belgesi — Başvuru künyesi, nihai onay hükmü, "
            "kurul üyesi imzaları, Etik Kurul Başkanı onayı, 24 haneli kriptografik kod ve gömülü Karekod (QR) [9, 10, 19]."
        ),
        (
            "07_verification.png",
            "Şekil 13: Resmi Karar Belgesi Doğrulama Sekmesi — Kayıtlı karar kodlarına tek tıkla erişim ve 24 haneli "
            "kriptografik doğrulama kodu ile yapılan sorgulamada belgenin gerçekliğinin teyit edilmesi [10, 17]."
        )
    ]

    for fname, caption in screenshots_info:
        img_path = os.path.join(SCREENSHOT_DIR, fname)
        w_in = 5.3 if fname == "06_certificate.png" else 6.2
        add_figure(doc, img_path, caption, width_inches=w_in)

    # =========================================================================
    # BÖLÜM 5: YAZILIMSAL MANTIK HATALARININ GİDERİLMESİ
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "5. Yazılımsal Mantık Hatalarının Giderilmesi ve Süreç İyileştirme Analizi", level=1)
    add_academic_paragraph(
        doc,
        "Literatürde Mayo Clinic ve Wisconsin Tıp Fakültesi çalışmalarında vurgulandığı üzere, e-IRB süreçlerindeki "
        "bekleme ve senkronizasyon darboğazlarının kaldırılması toplam dönüş süresini (TAT) %70'e varan oranda "
        "iyileştirmektedir [25, 32]. Geliştirilen uygulamada yapılan kullanıcı testleri sonucunda tespit edilen "
        "'onaylanan dosyaların Karar sekmesine düşmemesi' problemi ve ilişkili 7 yazılımsal mantık hatası sistematik "
        "olarak analiz edilmiş ve tamamen giderilmiştir (Tablo 6)."
    )

    add_styled_table(
        doc,
        "Tablo 6: Tespit Edilen Yazılımsal Mantık Hataları, Kök Neden Analizi ve Uygulanan Mühendislik Çözümleri",
        ["Hata No & Başlığı", "Kök Neden Analizi (Önceki Hatalı Durum)", "Uygulanan Mühendislik Çözümü (Yeni Durum)"],
        [
            [
                "1. Tek Raportör Onayında Karar Sekmesinin Boş Kalması",
                "Otomatik atama 2 raportör atıyordu. 1. raportör onay verdiğinde getEvaluationSummary() 'AwaitingReviews' dönüyor ve 2. raportör de oy verene kadar finalizeDecision() hiç çağrılmıyordu.",
                "submitEvaluation() metodu asenkron hale getirildi ve ilk raportör değerlendirme yaptığı anda finalizeDecision() otomatik tetiklenerek karar ve sertifika anında Karar & Belgeler sekmesine düşürüldü. 2. raportör oy verdiğinde aynı karar numarası korunarak belge 2 imza ile güncelleniyor [20, 25]."
            ],
            [
                "2. Geçmişte Değerlendirilen Dosyaların Kurtarılması (reconcileState)",
                "Önceki sürümde değerlendirilip 'UnderReview' durumunda asılı kalan başvurular (ör. ETIK-2026-00002 - AI) için geriye dönük karar üretme mekanizması yoktu.",
                "EmbeddedWorkflow içerisine reconcileState() onarım motoru eklendi. Uygulama açılışında tüm değerlendirmeleri tarayarak kararı eksik olan başvuruları otomatik olarak KARAR-2026-00001 onay belgesine dönüştürdü [14]."
            ],
            [
                "3. Otomatik Kararlarda Yanlış Gerekçe (Ret Metni) Yazılması",
                "finalizeDecision() içinde finalDecision parametresi doğrudan gönderilmeyip summary.recommendation üzerinden 'Approved' geldiğinde, koşul hatası nedeniyle onaylanan belgeye ret gerekçesi yazılıyordu.",
                "Koşul effectiveDecision değişkenine bağlandı. Approved, RevisionNeeded ve Rejected durumları için ayrı resmi gerekçe şablonları tanımlandı ve raportörün feedbackNotes görüşü karar metnine eklendi [19]."
            ],
            [
                "4. Revizyon Sonrası Onaylama ve Doğrudan Karar Eksikliği",
                "Revizyon ('RevisionNeeded') alan bir başvurunun düzeltme sonrasında nasıl onaylanacağına dair arayüzde bir kontrol yoktu.",
                "Karar sekmesine revizyondaki dosyalar için tek tıkla 'Onayla' butonu ve henüz karara bağlanmamış dosyalar için 'Hızlı Kurul Başkanlığı Kararı (Onayla / Revizyon / Reddet)' tablosu eklendi [25]."
            ],
            [
                "5. Atanan Dosyaların ve Değerlendirme Geçmişinin Görünmemesi",
                "Otomatik Atama sekmesinde dosya atandıktan sonra listeden kayboluyor, hangi raportörlerin atandığı ve kaçının değerlendirme yaptığı izlenemiyordu.",
                "Otomatik Atama sekmesine 'Atanmış Dosyalar ve Raportör İnceleme Durumu' tablosu, Üye Değerlendirme sekmesine ise 'Tamamlanan Üye Değerlendirmeleri' tablosu eklendi [9, 16]."
            ],
            [
                "6. Türkçe Karakter ('İ/ı') Uzmanlık Eşleştirme ve Ünvan Tekrarı",
                "tokenizeField() fonksiyonunda standart .toLowerCase() kullanıldığı için 'İ' harfi bozuluyor ve üye listesinde ünvanlar ('Prof. Dr. Prof. Dr.') mükerrer yazılıyordu.",
                ".toLocaleLowerCase('tr-TR') kullanımına geçildi ve formatPersonName() yardımcı fonksiyonu ile ünvan tekrarları tamamen temizlendi."
            ],
            [
                "7. Doğrulama Sekmesinde Sabit Yeşil Rozet ve Kod Kopyalama Zorluğu",
                "Belge doğrulama ekranında ret veya revizyon kararları bile sabit yeşil rozetle gösteriliyordu ve 24 haneli kodu elle yazmak zordu.",
                "Dinamik getBadgeClass() rozeti eklendi; ayrıca Karar ve Doğrulama sekmelerine tek tıkla doğrulama kodunu seçip sorgulayan etkileşimli kod etiketleri (code-pill) eklendi [17]."
            ]
        ],
        col_widths=[1.5, 2.4, 2.7]
    )

    # =========================================================================
    # BÖLÜM 6: DENEYSEL DOĞRULAMA VE KALİTE GÜVENCESİ
    # =========================================================================
    add_heading_styled(doc, "6. Deneysel Doğrulama, Otomatik Birim Testleri ve Kalite Güvencesi Bulguları", level=1)
    add_academic_paragraph(
        doc,
        "ISO/IEC 25010 yazılım kalite standartları [29] doğrultusunda sistemdeki 4 modülün tamamı için bağımsız birim "
        "ve uçtan uca entegrasyon testleri geliştirilmiştir. PowerShell tabanlı 'test-workflow.ps1' doğrulama betiği ile "
        "yürütülen toplam 19 test senaryosunun tamamı (%100) başarıyla geçmiştir (Şekil 14 ve Tablo 7)."
    )

    add_figure(doc, tech_charts[3], "Şekil 14: Modül Bazlı Otomatik Test Sonuçları (19/19) ve İşlevsel Doğrulama Dağılımı", width_inches=6.2)

    add_styled_table(
        doc,
        "Tablo 7: Uçtan Uca Otomatik Birim ve Entegrasyon Test Senaryoları Doğrulama Matrisi",
        ["Modül", "Test Dosyası", "Doğrulanan Senaryolar", "Sonuç"],
        [
            [
                "Modül 1\n(.NET 9 + MSSQL)",
                "ApplicationServiceTests.cs",
                "1) Yeni başvuru ve ETIK-YYYY-XXXXX protokol üretimi\n"
                "2) Protokol numarası ile başvuru ve araştırmacı sorgulama\n"
                "3) Dijital belge yükleme ve SHA-256 hash doğrulaması\n"
                "4) Başvuru durumu güncelleme ve geçersiz durum koruması",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 2\n(PHP 8.3 + MySQL)",
                "AutoAssignmentTest.php",
                "1) Kurul üyelerinin ve uzmanlık alanlarının listelenmesi\n"
                "2) Uzmanlık ve yük dengesine göre 2 raportör otomatik atama\n"
                "3) Yinelenen atama (Idempotency) engelleme testi\n"
                "4) Üye kriter puanlaması ve görüş kaydı oluşturma",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 3\n(Node.js + MongoDB)",
                "decision.test.js",
                "1) Revizyon talebi ve 14 günlük son teslim tarihi oluşturma\n"
                "2) Nihai karar ve Base64 QR kodlu resmi HTML sertifika üretimi\n"
                "3) 24 haneli kriptografik kod ile belge doğrulama\n"
                "4) Denetim izi (Audit Log) kayıtlarının bütünlük kontrolü",
                "4 / 4 Başarılı\n(%100)"
            ],
            [
                "Modül 4\n(Masaüstü Motoru)",
                "engine.test.js",
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
        col_widths=[1.3, 1.7, 2.6, 1.0]
    )

    # =========================================================================
    # BÖLÜM 7: KAYNAKÇA (REFERENCES)
    # =========================================================================
    doc.add_page_break()
    add_heading_styled(doc, "7. Kaynakça (References)", level=1)
    add_academic_paragraph(
        doc,
        "Rapor boyunca metin içinde köşeli parantez ([1] – [74]) ile atıf yapılan tüm uluslararası ve ulusal "
        "akademik çalışmalar, kurumsal standart çalışma prosedürleri (SOP) ve mevzuat kaynakları aşağıda "
        "sırasıyla listelenmiştir:"
    )

    for ref_num, ref_title, ref_url in REFERENCES_LIST:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.12
        p.paragraph_format.space_after = Pt(3.5)
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.35)

        r_num = p.add_run(f"[{ref_num}] ")
        r_num.bold = True
        r_num.font.name = "Segoe UI"
        r_num.font.size = Pt(8.8)
        r_num.font.color.rgb = RGBColor(30, 60, 114)

        r_txt = p.add_run(f"{ref_title} Erişim: ")
        r_txt.font.name = "Segoe UI"
        r_txt.font.size = Pt(8.8)
        r_txt.font.color.rgb = RGBColor(31, 41, 55)

        r_link = p.add_run(ref_url)
        r_link.font.name = "Segoe UI"
        r_link.font.size = Pt(8.5)
        r_link.italic = True
        r_link.font.color.rgb = RGBColor(2, 132, 199)

    doc.save(DESKTOP_DOCX_PATH)
    shutil.copyfile(DESKTOP_DOCX_PATH, PROJECT_DOCX_PATH)
    print(f"Akademik Word Raporu Başarıyla Oluşturuldu:\n1) {DESKTOP_DOCX_PATH}\n2) {PROJECT_DOCX_PATH}")


if __name__ == "__main__":
    lit_imgs = extract_literature_images()
    tech_chrts = generate_technical_charts()
    build_word_report(lit_imgs, tech_chrts)
