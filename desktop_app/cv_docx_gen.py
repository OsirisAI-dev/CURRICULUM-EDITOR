"""
Générateur de documents Word (.docx) pour le Curriculum Vitae.
Respecte les standards graphiques et conventions régionales (FR, EN, DE).
"""
from __future__ import annotations

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from cv_models import CVData
from cv_translations import SECTION_TITLES


def _hex_to_rgb(hex_str: str) -> RGBColor:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 6:
        return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))
    return RGBColor(30, 58, 138)


def _set_cell_margins(cell, top=50, bottom=50, left=50, right=50):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def _add_colored_heading(doc: Document, text: str, hex_color: str):
    """Ajoute un titre de section stylisé avec un filet inférieur."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = "Segoe UI"
    run.font.color.rgb = _hex_to_rgb(hex_color)

    # Filet horizontal sous le titre
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="2" w:color="{hex_color.lstrip("#")}"/></w:pBdr>')
    p._element.get_or_add_pPr().append(pBdr)


def generate_cv_docx(data: CVData, output_path: str | Path) -> str:
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    lang = data.config.cv_language or "fr"
    titles = SECTION_TITLES.get(lang, SECTION_TITLES["fr"])
    p_hex = data.config.primary_color or "#1e3a8a"
    p_rgb = _hex_to_rgb(p_hex)
    is_german = (data.config.country_version == "de")
    is_english = (data.config.country_version == "en")
    style_id = data.config.style_id or "modern_minimalist"

    doc = Document()

    # Définition des marges (0.5 pouce)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    gen = data.general

    # 1. En-Tête (Tableau à 2 colonnes : infos à gauche, photo à droite)
    has_photo = data.config.show_photo and gen.photo_path and Path(gen.photo_path).exists()
    tbl_hdr = doc.add_table(rows=1, cols=2 if has_photo else 1)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False

    cell_info = tbl_hdr.cell(0, 0)
    p_name = cell_info.paragraphs[0]
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    
    r_fn = p_name.add_run(f"{gen.first_name} ")
    r_fn.bold = True
    r_fn.font.size = Pt(20)
    r_fn.font.name = "Segoe UI"
    
    r_ln = p_name.add_run(gen.last_name.upper())
    r_ln.bold = True
    r_ln.font.size = Pt(20)
    r_ln.font.name = "Segoe UI"
    r_ln.font.color.rgb = p_rgb

    if gen.target_title:
        p_t = cell_info.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(4)
        r_t = p_t.add_run(gen.target_title.upper())
        r_t.bold = True
        r_t.font.size = Pt(11)
        r_t.font.name = "Segoe UI"
        r_t.font.color.rgb = p_rgb

    # Coordonnées
    contact_parts = []
    if gen.email:
        contact_parts.append(f"✉ {gen.email}")
    if gen.phone:
        contact_parts.append(f"☎ {gen.phone}")
    loc_str = ", ".join(filter(None, [gen.city, gen.country]))
    if loc_str:
        contact_parts.append(f"📍 {loc_str}")
    if gen.linkedin:
        contact_parts.append(f"🔗 {gen.linkedin}")
    if gen.github:
        contact_parts.append(f"💻 {gen.github}")
    if gen.portfolio_url:
        contact_parts.append(f"🌐 {gen.portfolio_url}")

    if contact_parts:
        p_c = cell_info.add_paragraph()
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(2)
        r_c = p_c.add_run("  •  ".join(contact_parts))
        r_c.font.size = Pt(9)
        r_c.font.name = "Segoe UI"
        r_c.font.color.rgb = RGBColor(100, 116, 139)

    # État civil (si activé et non-US)
    civil_parts = []
    if data.config.show_civil_status and not is_english:
        if gen.date_of_birth:
            civil_parts.append(f"{titles['date_of_birth']} {gen.date_of_birth}")
        if gen.place_of_birth:
            civil_parts.append(f"{titles['place_of_birth']} {gen.place_of_birth}")
        if gen.nationality:
            civil_parts.append(f"{titles['nationality']} {gen.nationality}")
        if gen.driving_license:
            civil_parts.append(f"{titles['driving_license']} {gen.driving_license}")

    if civil_parts:
        p_civ = cell_info.add_paragraph()
        p_civ.paragraph_format.space_before = Pt(0)
        p_civ.paragraph_format.space_after = Pt(2)
        r_civ = p_civ.add_run("  •  ".join(civil_parts))
        r_civ.font.size = Pt(8.5)
        r_civ.font.name = "Segoe UI"
        r_civ.font.color.rgb = RGBColor(100, 116, 139)

    # Photo
    if has_photo:
        cell_photo = tbl_hdr.cell(0, 1)
        p_ph = cell_photo.paragraphs[0]
        p_ph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ph.add_run().add_picture(gen.photo_path, width=Inches(1.1))

    # 2. Profil Professionnel
    if gen.summary:
        _add_colored_heading(doc, titles["profile"], p_hex)
        p_sum = doc.add_paragraph()
        p_sum.paragraph_format.space_before = Pt(2)
        p_sum.paragraph_format.space_after = Pt(4)
        r_sum = p_sum.add_run(gen.summary)
        r_sum.font.size = Pt(9.5)
        r_sum.font.name = "Segoe UI"

    # 3. Expériences Professionnelles
    if data.experiences:
        _add_colored_heading(doc, titles["experience"], p_hex)
        for exp in data.experiences:
            end_label = titles["present"] if exp.is_current else exp.end_date
            dates_str = f"{exp.start_date} – {end_label}" if (exp.start_date and end_label) else (exp.start_date or end_label or "")

            p_item = doc.add_paragraph()
            p_item.paragraph_format.space_before = Pt(4)
            p_item.paragraph_format.space_after = Pt(1)

            r_role = p_item.add_run(f"{exp.job_title} ")
            r_role.bold = True
            r_role.font.size = Pt(10)
            r_role.font.name = "Segoe UI"

            if exp.company:
                r_comp = p_item.add_run(f"|  {exp.company} ")
                r_comp.bold = True
                r_comp.font.size = Pt(10)
                r_comp.font.name = "Segoe UI"
                r_comp.font.color.rgb = p_rgb

            if exp.location:
                r_loc = p_item.add_run(f"({exp.location}) ")
                r_loc.font.size = Pt(9)
                r_loc.font.name = "Segoe UI"
                r_loc.font.color.rgb = RGBColor(100, 116, 139)

            if dates_str:
                r_dt = p_item.add_run(f"       [{dates_str}]")
                r_dt.italic = True
                r_dt.font.size = Pt(9)
                r_dt.font.name = "Segoe UI"
                r_dt.font.color.rgb = RGBColor(100, 116, 139)

            if exp.description:
                p_desc = doc.add_paragraph()
                p_desc.paragraph_format.space_before = Pt(1)
                p_desc.paragraph_format.space_after = Pt(2)
                r_d = p_desc.add_run(exp.description)
                r_d.font.size = Pt(9)
                r_d.font.name = "Segoe UI"

            for ach in exp.achievements:
                if ach.strip():
                    p_b = doc.add_paragraph(style='List Bullet')
                    p_b.paragraph_format.space_before = Pt(0)
                    p_b.paragraph_format.space_after = Pt(1)
                    r_b = p_b.add_run(ach)
                    r_b.font.size = Pt(9)
                    r_b.font.name = "Segoe UI"

    # 4. Formations & Diplômes
    if data.education:
        _add_colored_heading(doc, titles["education"], p_hex)
        for edu in data.education:
            dates_str = f"{edu.start_date} – {edu.end_date}" if edu.start_date and edu.end_date else (edu.end_date or edu.start_date or "")

            p_e = doc.add_paragraph()
            p_e.paragraph_format.space_before = Pt(4)
            p_e.paragraph_format.space_after = Pt(1)

            r_deg = p_e.add_run(f"{edu.degree} ")
            r_deg.bold = True
            r_deg.font.size = Pt(10)
            r_deg.font.name = "Segoe UI"

            if edu.institution:
                r_inst = p_e.add_run(f"|  {edu.institution} ")
                r_inst.bold = True
                r_inst.font.size = Pt(9.5)
                r_inst.font.name = "Segoe UI"
                r_inst.font.color.rgb = p_rgb

            if edu.location:
                r_l = p_e.add_run(f"({edu.location}) ")
                r_l.font.size = Pt(9)
                r_l.font.name = "Segoe UI"
                r_l.font.color.rgb = RGBColor(100, 116, 139)

            if dates_str:
                r_ed = p_e.add_run(f"       [{dates_str}]")
                r_ed.italic = True
                r_ed.font.size = Pt(9)
                r_ed.font.name = "Segoe UI"
                r_ed.font.color.rgb = RGBColor(100, 116, 139)

            if edu.honors:
                p_hon = doc.add_paragraph()
                p_hon.paragraph_format.space_before = Pt(0)
                p_hon.paragraph_format.space_after = Pt(1)
                r_h = p_hon.add_run(edu.honors)
                r_h.italic = True
                r_h.font.size = Pt(9)
                r_h.font.name = "Segoe UI"
                r_h.font.color.rgb = RGBColor(4, 120, 87)

            if edu.details:
                p_det = doc.add_paragraph()
                p_det.paragraph_format.space_before = Pt(0)
                p_det.paragraph_format.space_after = Pt(2)
                r_det = p_det.add_run(edu.details)
                r_det.font.size = Pt(8.5)
                r_det.font.name = "Segoe UI"

    # 5. Certifications
    if data.certifications:
        _add_colored_heading(doc, titles["certifications"], p_hex)
        for cert in data.certifications:
            p_c = doc.add_paragraph(style='List Bullet')
            p_c.paragraph_format.space_before = Pt(1)
            p_c.paragraph_format.space_after = Pt(1)
            r_cn = p_c.add_run(f"{cert.name} ")
            r_cn.bold = True
            r_cn.font.size = Pt(9)
            r_co = p_c.add_run(f"• {cert.issuing_org} ({cert.issue_date})")
            r_co.font.size = Pt(9)

    # 6. Compétences & Langues (dans un tableau 2 colonnes)
    if data.skills or data.languages:
        _add_colored_heading(doc, f"{titles['skills']} & {titles['languages']}", p_hex)
        tbl_sl = doc.add_table(rows=1, cols=2)
        tbl_sl.autofit = False

        c_sk = tbl_sl.cell(0, 0)
        p_sk_h = c_sk.paragraphs[0]
        r_sk_h = p_sk_h.add_run(titles["skills"])
        r_sk_h.bold = True
        r_sk_h.font.size = Pt(9.5)
        r_sk_h.font.color.rgb = p_rgb
        for sk in data.skills:
            p_s = c_sk.add_paragraph()
            p_s.paragraph_format.space_after = Pt(1)
            r_sn = p_s.add_run(f"• {sk.name} : ")
            r_sn.font.size = Pt(8.5)
            dots = "●" * sk.level + "○" * (5 - sk.level)
            r_sd = p_s.add_run(dots)
            r_sd.font.size = Pt(8.5)
            r_sd.font.color.rgb = p_rgb

        c_lg = tbl_sl.cell(0, 1)
        p_lg_h = c_lg.paragraphs[0]
        r_lg_h = p_lg_h.add_run(titles["languages"])
        r_lg_h.bold = True
        r_lg_h.font.size = Pt(9.5)
        r_lg_h.font.color.rgb = p_rgb
        for l in data.languages:
            p_l = c_lg.add_paragraph()
            p_l.paragraph_format.space_after = Pt(1)
            r_ln = p_l.add_run(f"• {l.language} : ")
            r_ln.font.size = Pt(8.5)
            val = l.cecr_level if l.eval_mode == "cecr" else (l.desc_level if l.eval_mode == "descriptive" else ("●" * l.dots))
            r_lv = p_l.add_run(str(val))
            r_lv.bold = True
            r_lv.font.size = Pt(8.5)
            r_lv.font.color.rgb = p_rgb

    # 7. Centres d'intérêt
    if data.hobbies:
        _add_colored_heading(doc, titles["hobbies"], p_hex)
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(2)
        p_h.paragraph_format.space_after = Pt(4)
        h_strs = [f"{h.name}{f' ({h.details})' if h.details else ''}" for h in data.hobbies]
        r_h = p_h.add_run("   •   ".join(h_strs))
        r_h.font.size = Pt(9)

    # 8. Clôture et Signature (Spécifique DACH / Allemand)
    if data.config.show_signoff:
        def_place = "Ort" if is_german else ("Location" if is_english else "Lieu")
        def_date = "Datum" if is_german else ("Date" if is_english else "Date")
        place_date_txt = titles["signoff_place_date"].format(
            place=data.signoff.place or gen.city or def_place,
            date=data.signoff.date_str or def_date
        )
        sig_name = data.signoff.signature_name or f"{gen.first_name} {gen.last_name}"

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(16)
        
        tbl_sig = doc.add_table(rows=1, cols=2)
        c_left = tbl_sig.cell(0, 0)
        p_l = c_left.paragraphs[0]
        p_l.add_run(place_date_txt).font.size = Pt(9)

        c_right = tbl_sig.cell(0, 1)
        p_r = c_right.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if data.signoff.signature_image_path and Path(data.signoff.signature_image_path).exists():
            try:
                p_r.add_run().add_picture(data.signoff.signature_image_path, width=Inches(1.3))
                p_r = c_right.add_paragraph()
                p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            except Exception:
                pass
        r_sn = p_r.add_run(f"___________________\n{sig_name}")
        r_sn.font.size = Pt(8.5)

    doc.save(str(out_file))
    return str(out_file)
