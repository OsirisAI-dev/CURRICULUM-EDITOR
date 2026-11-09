"""
Générateur HTML/CSS responsive et imprimable pour le Curriculum Vitae.
Permet une prévisualisation immédiate dans le navigateur et l'exportation web.
Prend en charge tous les styles, couleurs personnalisées, spécificités régionales (DACH, US, FR)
et évaluation linguistique (CECR, descriptif, points).
"""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Dict, Any

from cv_models import CVData
from cv_translations import SECTION_TITLES, CECR_LEVELS


def _image_to_base64(img_path: str) -> str:
    """Convertit une image en URI base64 pour un rendu HTML autonome."""
    if not img_path:
        return ""
    p = Path(img_path)
    if not p.exists() or not p.is_file():
        return ""
    try:
        suffix = p.suffix.lower().replace(".", "")
        if suffix == "jpg":
            suffix = "jpeg"
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/{suffix};base64,{b64}"
    except Exception:
        return ""


def _render_dots_html(level: int, max_dots: int = 5, color: str = "#1e3a8a") -> str:
    """Génère 5 pastilles visuelles (pleines et vides)."""
    dots_html = []
    for i in range(1, max_dots + 1):
        if i <= level:
            dots_html.append(f'<span class="dot filled" style="background-color: {color};"></span>')
        else:
            dots_html.append('<span class="dot empty"></span>')
    return "".join(dots_html)


def generate_cv_html(data: CVData) -> str:
    """Génère le code HTML complet et autonome du CV."""
    lang = data.config.cv_language or "fr"
    titles = SECTION_TITLES.get(lang, SECTION_TITLES["fr"])
    style_id = data.config.style_id or "modern_minimalist"
    p_color = data.config.primary_color or "#1e3a8a"
    s_color = data.config.secondary_color or "#0284c7"
    is_german = (data.config.country_version == "de")
    is_english = (data.config.country_version == "en")

    photo_b64 = _image_to_base64(data.general.photo_path) if data.config.show_photo else ""
    sign_b64 = _image_to_base64(data.signoff.signature_image_path) if data.config.show_signoff else ""

    # CSS Global et spécifique aux styles
    css = f"""
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1e293b;
        background-color: #f1f5f9;
        line-height: 1.5;
        font-size: 13.5px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}
    .cv-page {{
        width: 210mm;
        min-height: 297mm;
        margin: 20px auto;
        background: #ffffff;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 24mm 20mm;
        position: relative;
    }}
    @media print {{
        body {{
            background: none;
        }}
        .cv-page {{
            margin: 0;
            box-shadow: none;
            padding: 16mm 16mm;
            min-height: auto;
        }}
        .no-print {{
            display: none !important;
        }}
    }}

    /* Barre d'impression rapide */
    .print-bar {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #0f172a;
        color: #fff;
        padding: 10px 18px;
        border-radius: 30px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        cursor: pointer;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
    }}
    .print-bar:hover {{
        background: #1e293b;
    }}

    /* Typographie */
    h1 {{
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #0f172a;
        line-height: 1.15;
    }}
    .target-title {{
        font-size: 15px;
        font-weight: 600;
        color: {p_color};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
        margin-bottom: 8px;
    }}
    .section-title {{
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: {p_color};
        border-bottom: 2px solid {p_color};
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .section-title::before {{
        content: "";
        display: inline-block;
        width: 5px;
        height: 14px;
        background-color: {p_color};
        border-radius: 2px;
    }}

    /* Contact & Liens */
    .contact-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px 18px;
        font-size: 12px;
        color: #475569;
        margin-top: 6px;
        margin-bottom: 12px;
    }}
    .contact-item {{
        display: flex;
        align-items: center;
        gap: 5px;
    }}

    /* Cartes de parcours */
    .timeline-item {{
        margin-bottom: 14px;
        position: relative;
    }}
    .timeline-hdr {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2px;
    }}
    .role-title {{
        font-size: 14px;
        font-weight: 700;
        color: #0f172a;
    }}
    .institution-name {{
        font-weight: 600;
        color: {p_color};
    }}
    .date-badge {{
        font-size: 11.5px;
        font-weight: 600;
        color: #64748b;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 2px 7px;
        border-radius: 4px;
        white-space: nowrap;
    }}
    .item-desc {{
        font-size: 12.5px;
        color: #334155;
        margin-top: 3px;
    }}
    .bullets {{
        margin-top: 4px;
        padding-left: 18px;
        color: #334155;
    }}
    .bullets li {{
        margin-bottom: 2px;
        font-size: 12.5px;
    }}

    /* Compétences Tags */
    .skills-wrap {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }}
    .skill-tag {{
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #0f172a;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    /* Langues */
    .lang-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        padding: 4px 0;
        border-bottom: 1px dashed #e2e8f0;
        font-size: 12.5px;
    }}
    .lang-name {{
        font-weight: 600;
        color: #0f172a;
    }}
    .lang-badge {{
        font-size: 11px;
        font-weight: 700;
        color: #fff;
        background: {p_color};
        padding: 2px 7px;
        border-radius: 4px;
    }}
    .dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-left: 3px;
    }}
    .dot.empty {{
        background-color: #cbd5e1;
    }}

    /* Photo */
    .photo-frame {{
        width: 100px;
        height: 120px;
        border-radius: 6px;
        object-fit: cover;
        border: 2px solid {p_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    /* Signature allemande (Ort, Datum, Unterschrift) */
    .signoff-box {{
        margin-top: 28px;
        padding-top: 14px;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    .signoff-date {{
        font-size: 12.5px;
        color: #475569;
    }}
    .signature-container {{
        text-align: right;
    }}
    .signature-img {{
        max-height: 48px;
        max-width: 140px;
        display: block;
        margin-bottom: 4px;
        margin-left: auto;
    }}
    .signature-line {{
        border-top: 1px solid #0f172a;
        width: 160px;
        margin-left: auto;
        padding-top: 3px;
        font-size: 11px;
        color: #64748b;
        text-align: center;
    }}

    /* Style 2 : Colonne Latérale (Creative Sidebar) */
    .sidebar-layout {{
        display: grid;
        grid-template-columns: 66mm 1fr;
        gap: 0;
        margin: -24mm -20mm;
        min-height: 297mm;
    }}
    .sidebar-col {{
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
        padding: 24mm 16mm;
    }}
    .main-col {{
        padding: 24mm 20mm;
    }}

    /* Style 4 : Tabellarischer Lebenslauf (German Tabular) */
    .tabular-row {{
        display: grid;
        grid-template-columns: 46mm 1fr;
        gap: 16mm;
        margin-bottom: 12px;
        align-items: start;
    }}
    .tabular-date {{
        font-weight: 600;
        font-size: 12px;
        color: #475569;
        text-align: right;
        padding-top: 2px;
    }}
    """

    # Construction du corps
    gen = data.general

    # 1. En-tête / Header
    header_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
        <div style="flex: 1;">
            <h1>{gen.first_name} <span style="color: {p_color};">{gen.last_name.upper()}</span></h1>
            {f'<div class="target-title">{gen.target_title}</div>' if gen.target_title else ''}
            
            <div class="contact-grid">
                {f'<div class="contact-item">✉️ {gen.email}</div>' if gen.email else ''}
                {f'<div class="contact-item">📞 {gen.phone}</div>' if gen.phone else ''}
                {f'<div class="contact-item">📍 {gen.city}{", " + gen.country if gen.country else ""}</div>' if gen.city or gen.country else ''}
                {f'<div class="contact-item">🔗 {gen.linkedin}</div>' if gen.linkedin else ''}
                {f'<div class="contact-item">💻 {gen.github}</div>' if gen.github else ''}
            </div>

            {f'''
            <div style="font-size: 11.5px; color: #64748b; margin-top: 4px; display: flex; gap: 14px; flex-wrap: wrap;">
                {f'<span><b>{titles["date_of_birth"]}</b> {gen.date_of_birth}</span>' if gen.date_of_birth and data.config.show_civil_status else ''}
                {f'<span><b>{titles["place_of_birth"]}</b> {gen.place_of_birth}</span>' if gen.place_of_birth and data.config.show_civil_status else ''}
                {f'<span><b>{titles["nationality"]}</b> {gen.nationality}</span>' if gen.nationality and data.config.show_civil_status else ''}
                {f'<span><b>{titles["driving_license"]}</b> {gen.driving_license}</span>' if gen.driving_license and data.config.show_civil_status else ''}
            </div>
            ''' if data.config.show_civil_status and not is_english else ''}
        </div>
        {f'<img src="{photo_b64}" class="photo-frame" alt="Photo">' if photo_b64 else ''}
    </div>
    """

    # 2. Profil résumé
    summary_html = ""
    if gen.summary:
        summary_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["profile"]}</div>
            <p style="font-size: 13px; color: #334155; text-align: justify; line-height: 1.6;">
                {gen.summary}
            </p>
        </div>
        """

    # 3. Expériences
    exp_html = ""
    if data.experiences:
        items_html = []
        for exp in data.experiences:
            bullets_li = "".join([f"<li>{b}</li>" for b in exp.achievements if b.strip()])
            end_label = titles["present"] if exp.is_current else exp.end_date
            dates_str = f"{exp.start_date} – {end_label}" if exp.start_date else end_label

            if style_id == "german_tabular":
                item = f"""
                <div class="tabular-row">
                    <div class="tabular-date">{dates_str}</div>
                    <div>
                        <div class="role-title">{exp.job_title}</div>
                        <div class="institution-name">{exp.company} {f'• {exp.location}' if exp.location else ''}</div>
                        {f'<div class="item-desc">{exp.description}</div>' if exp.description else ''}
                        {f'<ul class="bullets">{bullets_li}</ul>' if bullets_li else ''}
                    </div>
                </div>
                """
            else:
                item = f"""
                <div class="timeline-item">
                    <div class="timeline-hdr">
                        <div class="role-title">{exp.job_title} <span class="institution-name">@ {exp.company}</span></div>
                        <div class="date-badge">{dates_str}</div>
                    </div>
                    {f'<div style="font-size: 11.5px; color: #64748b; margin-bottom: 3px;">📍 {exp.location}</div>' if exp.location else ''}
                    {f'<div class="item-desc">{exp.description}</div>' if exp.description else ''}
                    {f'<ul class="bullets">{bullets_li}</ul>' if bullets_li else ''}
                </div>
                """
            items_html.append(item)

        exp_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["experience"]}</div>
            {"".join(items_html)}
        </div>
        """

    # 4. Formations & Diplômes
    edu_html = ""
    if data.education:
        items_html = []
        for edu in data.education:
            dates_str = f"{edu.start_date} – {edu.end_date}" if edu.start_date and edu.end_date else (edu.end_date or edu.start_date)
            
            if style_id == "german_tabular":
                item = f"""
                <div class="tabular-row">
                    <div class="tabular-date">{dates_str}</div>
                    <div>
                        <div class="role-title">{edu.degree}</div>
                        <div class="institution-name">{edu.institution} {f'• {edu.location}' if edu.location else ''}</div>
                        {f'<div style="font-size: 12px; color: #0f766e; font-weight: 600;">{edu.honors}</div>' if edu.honors else ''}
                        {f'<div class="item-desc">{edu.details}</div>' if edu.details else ''}
                    </div>
                </div>
                """
            else:
                item = f"""
                <div class="timeline-item">
                    <div class="timeline-hdr">
                        <div class="role-title">{edu.degree}</div>
                        <div class="date-badge">{dates_str}</div>
                    </div>
                    <div class="institution-name">{edu.institution} {f'({edu.location})' if edu.location else ''}</div>
                    {f'<div style="font-size: 12px; color: #047857; font-weight: 600; margin-top: 2px;">{edu.honors}</div>' if edu.honors else ''}
                    {f'<div class="item-desc">{edu.details}</div>' if edu.details else ''}
                </div>
                """
            items_html.append(item)

        edu_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["education"]}</div>
            {"".join(items_html)}
        </div>
        """

    # 5. Certifications
    cert_html = ""
    if data.certifications:
        items_html = []
        for cert in data.certifications:
            item = f"""
            <div style="margin-bottom: 6px; font-size: 12.5px;">
                <b>{cert.name}</b> • <span style="color: {p_color};">{cert.issuing_org}</span> 
                {f'({cert.issue_date})' if cert.issue_date else ''}
                {f'<span style="color: #64748b; font-size: 11px;"> [ID: {cert.credential_id}]</span>' if cert.credential_id else ''}
            </div>
            """
            items_html.append(item)
        cert_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["certifications"]}</div>
            {"".join(items_html)}
        </div>
        """

    # 6. Compétences
    skills_html = ""
    if data.skills:
        tags = []
        for sk in data.skills:
            tags.append(f'<span class="skill-tag"><b>{sk.name}</b> {_render_dots_html(sk.level, 5, p_color)}</span>')
        skills_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["skills"]}</div>
            <div class="skills-wrap">
                {"".join(tags)}
            </div>
        </div>
        """

    # 7. Langues
    lang_html = ""
    if data.languages:
        items_html = []
        for l in data.languages:
            if l.eval_mode == "cecr":
                badge = f'<span class="lang-badge">{l.cecr_level}</span>'
            elif l.eval_mode == "dots":
                badge = _render_dots_html(l.dots, 5, p_color)
            else:
                badge = f'<span style="color: #475569; font-style: italic;">{l.desc_level}</span>'

            items_html.append(f"""
            <div class="lang-item">
                <span class="lang-name">{l.language}</span>
                <div>{badge}</div>
            </div>
            """)
        lang_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["languages"]}</div>
            {"".join(items_html)}
        </div>
        """

    # 8. Centres d'intérêt
    hobbies_html = ""
    if data.hobbies:
        tags = [f'<span class="skill-tag">🎯 <b>{h.name}</b>{f" : {h.details}" if h.details else ""}</span>' for h in data.hobbies]
        hobbies_html = f"""
        <div style="margin-bottom: 16px;">
            <div class="section-title">{titles["hobbies"]}</div>
            <div class="skills-wrap">{"".join(tags)}</div>
        </div>
        """

    # 9. Clôture & Signature (Spécifique DACH / Allemand ou activé)
    signoff_html = ""
    if data.config.show_signoff:
        place_date_txt = titles["signoff_place_date"].format(
            place=data.signoff.place or gen.city or "Lieu",
            date=data.signoff.date_str or "Date"
        )
        sig_name = data.signoff.signature_name or f"{gen.first_name} {gen.last_name}"
        signoff_html = f"""
        <div class="signoff-box">
            <div class="signoff-date">{place_date_txt}</div>
            <div class="signature-container">
                {f'<img src="{sign_b64}" class="signature-img" alt="Unterschrift">' if sign_b64 else ''}
                <div class="signature-line">{sig_name}</div>
            </div>
        </div>
        """

    # Assemblage selon la présence ou non de la colonne latérale
    if style_id == "creative_sidebar":
        # Layout 2 colonnes
        body_content = f"""
        <div class="sidebar-layout">
            <div class="sidebar-col">
                {f'<img src="{photo_b64}" class="photo-frame" style="width: 100%; height: auto; max-height: 180px; margin-bottom: 16px;" alt="Photo">' if photo_b64 else ''}
                
                <div style="margin-bottom: 18px;">
                    <h2 style="font-size: 18px; font-weight: 800; color: #0f172a;">{gen.first_name} {gen.last_name.upper()}</h2>
                    <div style="font-size: 13px; font-weight: 600; color: {p_color}; margin-top: 2px;">{gen.target_title}</div>
                </div>

                <div class="section-title" style="margin-top: 0;">{titles["contact"]}</div>
                <div style="font-size: 12px; color: #334155; display: flex; flex-direction: column; gap: 8px;">
                    {f'<div>✉️ {gen.email}</div>' if gen.email else ''}
                    {f'<div>📞 {gen.phone}</div>' if gen.phone else ''}
                    {f'<div>📍 {gen.city}, {gen.country}</div>' if gen.city or gen.country else ''}
                    {f'<div>🔗 {gen.linkedin}</div>' if gen.linkedin else ''}
                    {f'<div>💻 {gen.github}</div>' if gen.github else ''}
                </div>

                {skills_html}
                {lang_html}
                {hobbies_html}
            </div>

            <div class="main-col">
                {summary_html}
                {exp_html}
                {edu_html}
                {cert_html}
                {signoff_html}
            </div>
        </div>
        """
    else:
        # Layout linéaire ou tabulaire
        body_content = f"""
        {header_html}
        {summary_html}
        {exp_html}
        {edu_html}
        {cert_html}
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>{skills_html}</div>
            <div>{lang_html}</div>
        </div>
        
        {hobbies_html}
        {signoff_html}
        """

    full_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>Curriculum Vitae • {gen.first_name} {gen.last_name}</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="print-bar no-print" onclick="window.print()">
        🖨️ Imprimer / Sauvegarder en PDF
    </div>

    <div class="cv-page">
        {body_content}
    </div>
</body>
</html>
"""
    return full_html
