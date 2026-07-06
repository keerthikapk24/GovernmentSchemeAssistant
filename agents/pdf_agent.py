"""
PDF Report Agent
-----------------
Generates a downloadable PDF summary of the citizen's eligible schemes,
documents needed, and application steps - in English or Tamil.

Tamil rendering requires a Unicode font that supports Tamil script,
since ReportLab's built-in fonts only cover English/Latin characters.
We register "NotoSansTamil-Regular.ttf" and "NotoSansTamil-Bold.ttf"
from the /fonts folder if present. If they're missing, Tamil PDFs will
gracefully fall back to English fonts.
"""

import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from translations import t, translate_doc, scheme_field

# ---------------- Tamil font registration ----------------
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts")
TAMIL_FONT_AVAILABLE = False
TAMIL_FONT_ERROR = None
try:
    pdfmetrics.registerFont(TTFont("NotoTamil", os.path.join(FONT_DIR, "NotoSansTamil-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("NotoTamil-Bold", os.path.join(FONT_DIR, "NotoSansTamil-Bold.ttf")))
    TAMIL_FONT_AVAILABLE = True
except Exception as e:
    TAMIL_FONT_AVAILABLE = False
    TAMIL_FONT_ERROR = f"{type(e).__name__}: {e} (looked in: {os.path.abspath(FONT_DIR)})"


def generate_pdf(profile, results, lang="en"):
    use_tamil_font = (lang == "ta" and TAMIL_FONT_AVAILABLE)
    font_regular = "NotoTamil" if use_tamil_font else "Helvetica"
    font_bold = "NotoTamil-Bold" if use_tamil_font else "Helvetica-Bold"

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"],
                                  fontName=font_bold, fontSize=18, spaceAfter=6)
    heading_style = ParagraphStyle("SchemeHeading", parent=styles["Heading2"],
                                    fontName=font_bold, textColor=colors.HexColor("#1a5632"),
                                    spaceBefore=14)
    subheading_style = ParagraphStyle("SubHeading", parent=styles["Heading3"], fontName=font_bold)
    label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName=font_bold, spaceBefore=6)
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName=font_regular)

    story = []

    # ---- Header ----
    story.append(Paragraph(t(lang, "pdf_title"), title_style))
    story.append(Paragraph(t(lang, "pdf_generated_on", date=datetime.now().strftime('%d %B %Y')), body_style))
    story.append(Spacer(1, 6))

    occ_label = t(lang, "occupation_options").get(profile["occupation"], profile["occupation"])
    gender_label = t(lang, "gender_options").get(profile["gender"], profile["gender"])
    category_label = t(lang, "category_options").get(profile["category"], profile["category"])

    profile_summary = (
        f"{t(lang, 'age_label')}: {profile['age']}  |  {t(lang, 'gender_label')}: {gender_label}  |  "
        f"{t(lang, 'occupation_label')}: {occ_label}  |  "
        f"{t(lang, 'income_label')}: Rs {profile['annual_income']:,}  |  "
        f"{t(lang, 'category_label')}: {category_label}"
    )
    story.append(Paragraph(profile_summary, body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey, spaceBefore=10, spaceAfter=10))

    story.append(Paragraph(t(lang, "pdf_eligible_intro", count=len(results)), subheading_style))

    # ---- Each scheme ----
    for r in results:
        scheme = r["scheme"]
        docs = r["documents"]
        guide = r["guide"]
        deadline = r["deadline"]

        name = scheme_field(scheme, "name", lang)
        sector = scheme_field(scheme, "sector", lang)
        description = scheme_field(scheme, "description", lang)
        office = scheme_field(scheme, "office", lang)
        steps = scheme_field(scheme, "how_to_apply", lang)

        story.append(Paragraph(f"{name} ({sector})", heading_style))
        story.append(Paragraph(description, body_style))

        story.append(Paragraph(t(lang, "pdf_why_qualify"), label_style))
        story.append(ListFlowable(
            [ListItem(Paragraph(reason, body_style)) for reason in r["reasons"]],
            bulletType="bullet", leftIndent=14
        ))

        story.append(Paragraph(t(lang, "pdf_docs_have"), label_style))
        have_names = [translate_doc(d, lang) for d in docs["have"]]
        have_text = ", ".join(have_names) if have_names else t(lang, "pdf_none_yet")
        story.append(Paragraph(have_text, body_style))

        story.append(Paragraph(t(lang, "pdf_docs_missing"), label_style))
        missing_names = [translate_doc(d, lang) for d in docs["missing"]]
        missing_text = ", ".join(missing_names) if missing_names else t(lang, "pdf_all_ready")
        story.append(Paragraph(missing_text, body_style))

        story.append(Paragraph(t(lang, "pdf_how_to_apply"), label_style))
        story.append(ListFlowable(
            [ListItem(Paragraph(step, body_style)) for step in steps],
            bulletType="1", leftIndent=14
        ))

        story.append(Paragraph(f"<b>{t(lang, 'apply_online')}</b> {scheme['apply_link']}", body_style))
        story.append(Paragraph(f"<b>{t(lang, 'or_visit')}</b> {office}", body_style))
        story.append(Paragraph(f"<b>{t(lang, 'pdf_deadline')}</b> {deadline['status']}", body_style))

        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey,
                                 spaceBefore=10, spaceAfter=4))

    doc.build(story)
    buffer.seek(0)
    return buffer
