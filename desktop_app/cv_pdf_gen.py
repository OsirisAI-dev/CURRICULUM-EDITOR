"""
Générateur de PDF professionnel pour le Curriculum Vitae avec ReportLab.
Rendu vectoriel de haute qualité, pagination A4 soignée, respect des conventions régionales
(CV France, Resume US/UK, Lebenslauf DACH avec Ort/Datum/Unterschrift),
gestion des photos d'identité et échelles d'évaluation linguistique (CECR, descriptif, points).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)

from cv_models import CVData
from cv_translations import SECTION_TITLES, CECR_LEVELS


def _render_dots_unicode(level: int, max_dots: int = 5) -> str:
    """Retourne une chaîne de points pleins et vides (ex: ●●●○○)."""
    level = max(0, min(level, max_dots))
    return "●" * level + "○" * (max_dots - level)


def generate_cv_pdf(data: CVData, output_path: str | Path) -> str:
    """Génère le document PDF du CV et retourne son chemin absolu."""
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lang = data.config.cv_language or "fr"
    titles = SECTION_TITLES.get(lang, SECTION_TITLES["fr"])
    p_hex = data.config.primary_color or "#1e3a8a"
    s_hex = data.config.secondary_color or "#0284c7"
    is_german = (data.config.country_version == "de")
    is_english = (data.config.country_version == "en")
    style_id = data.config.style_id or "modern_minimalist"

    c_primary = colors.HexColor(p_hex)
    c_secondary = colors.HexColor(s_hex)
    c_dark = colors.HexColor("#0f172a")
    c_text = colors.HexColor("#334155")
    c_muted = colors.HexColor("#64748b")
    c_light_bg = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#e2e8f0")

    # Marges A4
    margin = 36  # 0.5 pouce / 12.7 mm
    doc = SimpleDocTemplate(
        str(out_file),
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    usable_width = A4[0] - (2 * margin)

    # Styles typographiques
    styles = getSampleStyleSheet()

    st_name = ParagraphStyle(
        "CVName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=c_dark
    )
    st_title = ParagraphStyle(
        "CVTargetTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceAfter=4
    )
    st_contact = ParagraphStyle(
        "CVContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=c_muted
    )
    st_civil = ParagraphStyle(
        "CVCivil",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=c_muted
    )
    st_sec_hdr = ParagraphStyle(
        "CVSecHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4
    )
    st_item_role = ParagraphStyle(
        "CVRole",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=c_dark
    )
    st_item_company = ParagraphStyle(
        "CVCompany",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12.5,
        textColor=c_primary
    )
    st_item_date = ParagraphStyle(
        "CVDate",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=2,  # Align Right
        textColor=c_muted
    )
    st_item_date_tabular = ParagraphStyle(
        "CVDateTab",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=c_muted
    )
    st_body = ParagraphStyle(
        "CVBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=c_text
    )
    st_bullet = ParagraphStyle(
        "CVBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        leftIndent=12,
        firstLineIndent=-8
    )
    st_tag = ParagraphStyle(
        "CVTag",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=c_dark
    )
    st_badge = ParagraphStyle(
        "CVBadge",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        alignment=2,
        textColor=c_primary
    )

    story = []

    def make_section_header(title_text: str):
        p = Paragraph(f"<b>{title_text.upper()}</b>", st_sec_hdr)
        hr = HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=6)
        return KeepTogether([p, hr])

    # 1. En-tête / Header avec Photo optionnelle
    gen = data.general
    contact_parts = []
    if gen.email:
        contact_parts.append(f"✉ {gen.email}")
    if gen.phone:
        contact_parts.append(f"☎ {gen.phone}")
    if gen.city or gen.country:
        contact_parts.append(f"📍 {gen.city}{', ' + gen.country if gen.country else ''}")
    if gen.linkedin:
        contact_parts.append(f"🔗 {gen.linkedin}")
    if gen.github:
        contact_parts.append(f"💻 {gen.github}")

    contact_str = " &nbsp;•&nbsp; ".join(contact_parts)

    civil_parts = []
    if data.config.show_civil_status and not is_english:
        if gen.date_of_birth:
            civil_parts.append(f"<b>{titles['date_of_birth']}</b> {gen.date_of_birth}")
        if gen.place_of_birth:
            civil_parts.append(f"<b>{titles['place_of_birth']}</b> {gen.place_of_birth}")
        if gen.nationality:
            civil_parts.append(f"<b>{titles['nationality']}</b> {gen.nationality}")
        if gen.driving_license:
            civil_parts.append(f"<b>{titles['driving_license']}</b> {gen.driving_license}")
    civil_str = " &nbsp;•&nbsp; ".join(civil_parts)

    info_paras = [
        Paragraph(f"{gen.first_name} <font color='{p_hex}'>{gen.last_name.upper()}</font>", st_name),
        Paragraph(gen.target_title, st_title) if gen.target_title else Spacer(1, 1),
        Paragraph(contact_str, st_contact) if contact_str else Spacer(1, 1),
    ]
    if civil_str:
        info_paras.append(Spacer(1, 2))
        info_paras.append(Paragraph(civil_str, st_civil))

    # Photo d'identité
    photo_flowable = None
    if data.config.show_photo and gen.photo_path and Path(gen.photo_path).exists():
        try:
            photo_flowable = RLImage(gen.photo_path, width=70, height=85)
        except Exception:
            photo_flowable = None

    if photo_flowable:
        hdr_table = Table(
            [[info_paras, photo_flowable]],
            colWidths=[usable_width - 80, 80]
        )
        hdr_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(hdr_table)
    else:
        for p in info_paras:
            story.append(p)

    story.append(Spacer(1, 8))

    # 2. Profil Professionnel / Summary
    if gen.summary:
        story.append(make_section_header(titles["profile"]))
        story.append(Paragraph(gen.summary, st_body))
        story.append(Spacer(1, 6))

    # 3. Expériences Professionnelles
    if data.experiences:
        story.append(make_section_header(titles["experience"]))
        for exp in data.experiences:
            end_label = titles["present"] if exp.is_current else exp.end_date
            dates_str = f"{exp.start_date} – {end_label}" if exp.start_date else end_label

            if style_id == "german_tabular":
                # Style tabulaire avec dates à gauche
                cell_left = Paragraph(f"<b>{dates_str}</b>", st_item_date_tabular)
                right_paras = [
                    Paragraph(f"<b>{exp.job_title}</b>", st_item_role),
                    Paragraph(f"{exp.company}{' • ' + exp.location if exp.location else ''}", st_item_company)
                ]
                if exp.description:
                    right_paras.append(Paragraph(exp.description, st_body))
                for ach in exp.achievements:
                    if ach.strip():
                        right_paras.append(Paragraph(f"• {ach}", st_bullet))

                t_row = Table([[cell_left, right_paras]], colWidths=[110, usable_width - 110])
                t_row.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                story.append(KeepTogether([t_row]))
            else:
                # Style classique / minimaliste
                p_left = Paragraph(f"<b>{exp.job_title}</b> &nbsp;|&nbsp; <font color='{p_hex}'><b>{exp.company}</b></font>{f' ({exp.location})' if exp.location else ''}", st_item_role)
                p_right = Paragraph(dates_str, st_item_date)
                
                t_header = Table([[p_left, p_right]], colWidths=[usable_width - 100, 100])
                t_header.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                
                item_elements = [t_header]
                if exp.description:
                    item_elements.append(Paragraph(exp.description, st_body))
                for ach in exp.achievements:
                    if ach.strip():
                        item_elements.append(Paragraph(f"• {ach}", st_bullet))
                item_elements.append(Spacer(1, 6))

                story.append(KeepTogether(item_elements))

    # 4. Formations & Diplômes
    if data.education:
        story.append(make_section_header(titles["education"]))
        for edu in data.education:
            dates_str = f"{edu.start_date} – {edu.end_date}" if edu.start_date and edu.end_date else (edu.end_date or edu.start_date)

            if style_id == "german_tabular":
                cell_left = Paragraph(f"<b>{dates_str}</b>", st_item_date_tabular)
                right_paras = [
                    Paragraph(f"<b>{edu.degree}</b>", st_item_role),
                    Paragraph(f"{edu.institution}{' • ' + edu.location if edu.location else ''}", st_item_company)
                ]
                if edu.honors:
                    right_paras.append(Paragraph(f"<i>{edu.honors}</i>", st_body))
                if edu.details:
                    right_paras.append(Paragraph(edu.details, st_body))

                t_row = Table([[cell_left, right_paras]], colWidths=[110, usable_width - 110])
                t_row.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                story.append(KeepTogether([t_row]))
            else:
                p_left = Paragraph(f"<b>{edu.degree}</b> &nbsp;|&nbsp; <font color='{p_hex}'><b>{edu.institution}</b></font>{f' ({edu.location})' if edu.location else ''}", st_item_role)
                p_right = Paragraph(dates_str, st_item_date)
                
                t_header = Table([[p_left, p_right]], colWidths=[usable_width - 100, 100])
                t_header.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                
                item_elements = [t_header]
                if edu.honors:
                    item_elements.append(Paragraph(f"<i>{edu.honors}</i>", st_body))
                if edu.details:
                    item_elements.append(Paragraph(edu.details, st_body))
                item_elements.append(Spacer(1, 5))

                story.append(KeepTogether(item_elements))

    # 5. Certifications & Formations continues
    if data.certifications:
        story.append(make_section_header(titles["certifications"]))
        cert_rows = []
        for cert in data.certifications:
            p_desc = Paragraph(f"<b>{cert.name}</b> • <font color='{p_hex}'>{cert.issuing_org}</font>{f' [ID: {cert.credential_id}]' if cert.credential_id else ''}", st_body)
            p_date = Paragraph(cert.issue_date, st_item_date)
            cert_rows.append([p_desc, p_date])

        t_cert = Table(cert_rows, colWidths=[usable_width - 80, 80])
        t_cert.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(t_cert)
        story.append(Spacer(1, 4))

    # 6. Compétences & Langues (En deux colonnes juxtaposées)
    skills_flowables = []
    if data.skills:
        skills_flowables.append(Paragraph(f"<b>{titles['skills'].upper()}</b>", st_sec_hdr))
        skills_flowables.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
        for sk in data.skills:
            dots_str = _render_dots_unicode(sk.level, 5)
            row_t = Table(
                [[Paragraph(sk.name, st_tag), Paragraph(f"<font color='{p_hex}'>{dots_str}</font>", st_badge)]],
                colWidths=[(usable_width / 2) - 60, 50]
            )
            row_t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ]))
            skills_flowables.append(row_t)

    lang_flowables = []
    if data.languages:
        lang_flowables.append(Paragraph(f"<b>{titles['languages'].upper()}</b>", st_sec_hdr))
        lang_flowables.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
        for l in data.languages:
            if l.eval_mode == "cecr":
                badge_text = f"<b>{l.cecr_level}</b>"
            elif l.eval_mode == "dots":
                badge_text = _render_dots_unicode(l.dots, 5)
            else:
                badge_text = l.desc_level

            row_t = Table(
                [[Paragraph(l.language, st_tag), Paragraph(f"<font color='{p_hex}'>{badge_text}</font>", st_badge)]],
                colWidths=[(usable_width / 2) - 80, 70]
            )
            row_t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ]))
            lang_flowables.append(row_t)

    if skills_flowables or lang_flowables:
        col_w = (usable_width - 16) / 2
        dual_table = Table(
            [[skills_flowables or Spacer(1, 1), lang_flowables or Spacer(1, 1)]],
            colWidths=[col_w, col_w]
        )
        dual_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(Spacer(1, 4))
        story.append(KeepTogether([dual_table]))

    # 7. Centres d'intérêt / Hobbys
    if data.hobbies:
        story.append(make_section_header(titles["hobbies"]))
        h_strs = [f"<b>{h.name}</b>{f' ({h.details})' if h.details else ''}" for h in data.hobbies]
        story.append(Paragraph(" &nbsp;•&nbsp; ".join(h_strs), st_body))
        story.append(Spacer(1, 6))

    # 8. Clôture et Signature (Spécifique DACH / Lebenslauf ou activé)
    if data.config.show_signoff:
        place_date_txt = titles["signoff_place_date"].format(
            place=data.signoff.place or gen.city or "Lieu",
            date=data.signoff.date_str or "Date"
        )
        sig_name = data.signoff.signature_name or f"{gen.first_name} {gen.last_name}"

        sig_img_flowable = None
        if data.signoff.signature_image_path and Path(data.signoff.signature_image_path).exists():
            try:
                sig_img_flowable = RLImage(data.signoff.signature_image_path, width=120, height=35)
            except Exception:
                sig_img_flowable = None

        sig_paras = []
        if sig_img_flowable:
            sig_paras.append(sig_img_flowable)
        sig_paras.append(HRFlowable(width="100%", thickness=1, color=c_dark, spaceBefore=4, spaceAfter=2))
        sig_paras.append(Paragraph(sig_name, ParagraphStyle("SigName", parent=st_body, alignment=1, fontSize=8.5)))

        t_sign = Table(
            [[Paragraph(place_date_txt, st_body), sig_paras]],
            colWidths=[usable_width - 150, 150]
        )
        t_sign.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 16),
        ]))
        story.append(KeepTogether([t_sign]))

    doc.build(story)
    return str(out_file)
