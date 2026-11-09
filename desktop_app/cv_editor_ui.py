"""
Application Principale : Éditeur Professionnel de Curriculum Vitae (CV).
Mise en page moderne CustomTkinter avec support multi-styles, multi-versions (FR / US-UK / DE),
multilingue (Français, Anglais, Allemand), ajout dynamique de toutes les sous-catégories,
évaluation linguistique avancée (CECRL A1-C2, Descriptif, Points) et export direct PDF, DOCX et HTML.
"""
from __future__ import annotations

import os
import sys
import webbrowser
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Dict, Any, Optional

import customtkinter as ctk
from PIL import Image

from cv_models import (
    CVData, CVGeneralInfo, CVExperience, CVEducation, CVCertification,
    CVSkill, CVLanguage, CVHobby, CVSignOff, CVConfig
)
from cv_translations import (
    COUNTRY_VERSIONS, CV_LANGUAGES, CV_STYLES, COLOR_PALETTES,
    SECTION_TITLES, CECR_LEVELS, DESCRIPTIVE_LEVELS, DEMO_PROFILES
)
from cv_icons import get_cv_icons
from cv_pdf_gen import generate_cv_pdf
from cv_docx_gen import generate_cv_docx
from cv_html_gen import generate_cv_html


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "exports"


class CVEditorApp(ctk.CTk):
    """Fenêtre principale de l'Éditeur de Curriculum Vitae."""

    def __init__(self):
        super().__init__()
        self.icons = get_cv_icons()
        self.data = CVData()
        
        # Initialiser avec un formulaire 100% vierge par défaut (Démos FR/EN/DE disponibles via la barre d'outils)
        self.data = CVData()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Curriculum Vitae Studio • Multi-Styles & Multi-Versions (FR / EN / DE)")
        self.geometry("1180x820")
        self.minsize(1020, 680)

        ico_p = BASE_DIR / "cv_icon.ico"
        if ico_p.exists():
            try:
                self.iconbitmap(str(ico_p))
            except Exception:
                pass

        # Listes de widgets pour les éléments dynamiques
        self.exp_cards: List[Dict[str, Any]] = []
        self.edu_cards: List[Dict[str, Any]] = []
        self.cert_cards: List[Dict[str, Any]] = []
        self.skill_cards: List[Dict[str, Any]] = []
        self.lang_cards: List[Dict[str, Any]] = []
        self.hobby_cards: List[Dict[str, Any]] = []

        self._setup_ui()

    def _setup_ui(self):
        # 1. En-Tête Supérieur (Top Bar)
        self.top_bar = ctk.CTkFrame(self, fg_color=("#1e3a8a", "#0f172a"), height=65, corner_radius=0)
        self.top_bar.pack(side="top", fill="x")
        self._build_top_bar()

        # 2. Barre d'outils secondaire (Toolbar)
        self.toolbar = ctk.CTkFrame(self, fg_color=("#f1f5f9", "#1e293b"), height=46, corner_radius=0)
        self.toolbar.pack(side="top", fill="x")
        self._build_toolbar()

        # 3. Zone principale avec onglets
        self.tabview = ctk.CTkTabview(self, corner_radius=8, fg_color=("#f8fafc", "#0f172a"))
        self.tabview.pack(side="top", fill="both", expand=True, padx=12, pady=(6, 10))

        self.tab_general = self.tabview.add("1. 👤 Informations & État Civil")
        self.tab_exp = self.tabview.add("2. 💼 Expériences")
        self.tab_edu = self.tabview.add("3. 🎓 Études & Diplômes")
        self.tab_cert = self.tabview.add("4. 📜 Certifications")
        self.tab_skills = self.tabview.add("5. ⚡ Compétences")
        self.tab_lang = self.tabview.add("6. 🌍 Langues")
        self.tab_hobbies = self.tabview.add("7. 🎯 Hobbys & Intérêts")
        self.tab_signoff = self.tabview.add("8. ✍️ Signature DACH")
        self.tab_export = self.tabview.add("9. 🚀 Styles & Export")

        self._build_tab_general()
        self._build_tab_experiences()
        self._build_tab_education()
        self._build_tab_certifications()
        self._build_tab_skills()
        self._build_tab_languages()
        self._build_tab_hobbies()
        self._build_tab_signoff()
        self._build_tab_export()

        # Synchroniser les widgets avec les données initiales
        self._sync_ui_with_data()

    # ═════════════════════════════════════════════════════════════════════════
    #  Barre Supérieure & Sélecteurs (Version Pays, Langue, Style)
    # ═════════════════════════════════════════════════════════════════════════

    def _build_top_bar(self):
        f_left = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        f_left.pack(side="left", padx=14, pady=10)

        lbl_app = ctk.CTkLabel(
            f_left,
            text=" CURRICULUM VITAE STUDIO",
            image=self.icons.get_white_icon("user", 22),
            compound="left",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#ffffff"
        )
        lbl_app.pack(anchor="w")

        f_right = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        f_right.pack(side="right", padx=14, pady=10)

        # Sélecteur de Version Pays (FR, EN, DE)
        ctk.CTkLabel(f_right, text="Modèle Régional :", font=ctk.CTkFont(size=11, weight="bold"), text_color="#cbd5e1").pack(side="left", padx=(0, 4))
        self.combo_country = ctk.CTkComboBox(
            f_right,
            values=[
                "France & Francophone (FR)",
                "Anglophone US/UK (EN)",
                "Germanophone DACH (DE)"
            ],
            width=200,
            height=28,
            command=self._on_country_version_changed
        )
        self.combo_country.set("France & Francophone (FR)")
        self.combo_country.pack(side="left", padx=(0, 10))

        # Sélecteur de Langue du CV
        ctk.CTkLabel(f_right, text="Langue du CV :", font=ctk.CTkFont(size=11, weight="bold"), text_color="#cbd5e1").pack(side="left", padx=(0, 4))
        self.combo_cv_lang = ctk.CTkComboBox(
            f_right,
            values=["Français (FR)", "English (EN)", "Deutsch (DE)"],
            width=135,
            height=28,
            command=self._on_cv_lang_changed
        )
        self.combo_cv_lang.set("Français (FR)")
        self.combo_cv_lang.pack(side="left", padx=(0, 10))

        # Thème clair/sombre
        btn_theme = ctk.CTkButton(
            f_right,
            text="",
            image=self.icons.get_white_icon("theme", 15),
            width=32,
            height=28,
            fg_color="#0f172a",
            hover_color="#334155",
            command=self._toggle_theme
        )
        btn_theme.pack(side="left")

    def _build_toolbar(self):
        f_tools = self.toolbar

        # Sélecteur de Style Visuel
        lbl_st = ctk.CTkLabel(f_tools, text="Style Visuel :", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#0f172a", "#f8fafc"))
        lbl_st.pack(side="left", padx=(14, 4), pady=8)

        style_labels = [f"{v['name']}" for v in CV_STYLES.values()]
        self.combo_style = ctk.CTkComboBox(
            f_tools,
            values=style_labels,
            width=220,
            height=28,
            command=self._on_style_changed
        )
        self.combo_style.set(CV_STYLES["modern_minimalist"]["name"])
        self.combo_style.pack(side="left", padx=(0, 10), pady=8)

        # Démo Rapide (Boutons pour charger 1 profil type)
        btn_demo_fr = ctk.CTkButton(
            f_tools, text=" Démo FR", width=85, height=26, font=ctk.CTkFont(size=10, weight="bold"),
            image=self.icons.get_icon("sparkles", 12, "#1e3a8a", "#60a5fa"), compound="left",
            fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"),
            command=lambda: self._load_demo_data("fr")
        )
        btn_demo_fr.pack(side="left", padx=3)

        btn_demo_en = ctk.CTkButton(
            f_tools, text=" Démo EN", width=85, height=26, font=ctk.CTkFont(size=10, weight="bold"),
            image=self.icons.get_icon("sparkles", 12, "#1e3a8a", "#60a5fa"), compound="left",
            fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"),
            command=lambda: self._load_demo_data("en")
        )
        btn_demo_en.pack(side="left", padx=3)

        btn_demo_de = ctk.CTkButton(
            f_tools, text=" Démo DE", width=85, height=26, font=ctk.CTkFont(size=10, weight="bold"),
            image=self.icons.get_icon("sparkles", 12, "#1e3a8a", "#60a5fa"), compound="left",
            fg_color=("#e2e8f0", "#334155"), text_color=("#0f172a", "#f8fafc"),
            command=lambda: self._load_demo_data("de")
        )
        btn_demo_de.pack(side="left", padx=3)

        btn_clear = ctk.CTkButton(
            f_tools, text=" 🧹 Vider", width=75, height=26, font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=("#64748b", "#475569"), hover_color=("#475569", "#334155"),
            text_color="#ffffff",
            command=self._clear_all_fields_blank
        )
        btn_clear.pack(side="left", padx=(6, 3))

        # Boutons d'action à droite
        btn_html = ctk.CTkButton(
            f_tools, text=" Aperçu Web", width=105, height=28, font=ctk.CTkFont(size=11, weight="bold"),
            image=self.icons.get_white_icon("eye", 13), compound="left",
            fg_color=("#0284c7", "#0369a1"), hover_color=("#0369a1", "#075985"),
            command=self._preview_html
        )
        btn_html.pack(side="right", padx=(4, 14), pady=8)

        btn_pdf = ctk.CTkButton(
            f_tools, text=" Exporter PDF", width=115, height=28, font=ctk.CTkFont(size=11, weight="bold"),
            image=self.icons.get_white_icon("download", 13), compound="left",
            fg_color=("#1e3a8a", "#1d4ed8"), hover_color=("#1e40af", "#1e3a8a"),
            command=self._export_pdf
        )
        btn_pdf.pack(side="right", padx=4, pady=8)

        btn_docx = ctk.CTkButton(
            f_tools, text=" Exporter Word", width=115, height=28, font=ctk.CTkFont(size=11),
            image=self.icons.get_icon("doc_word", 13, "#0f172a", "#f8fafc"), compound="left",
            fg_color=("#cbd5e1", "#334155"), text_color=("#0f172a", "#f8fafc"),
            command=self._export_docx
        )
        btn_docx.pack(side="right", padx=4, pady=8)

    def _toggle_theme(self):
        curr = ctk.get_appearance_mode()
        nxt = "dark" if curr == "Light" else "light"
        ctk.set_appearance_mode(nxt)

    def _on_country_version_changed(self, choice: str):
        if "France" in choice:
            cid = "fr"
        elif "Anglophone" in choice:
            cid = "en"
        else:
            cid = "de"
        self.data.config.country_version = cid
        meta = COUNTRY_VERSIONS[cid]
        # Ajuster automatiquement les options par défaut du pays
        self.data.config.show_photo = meta["defaults"]["show_photo"]
        self.data.config.show_civil_status = meta["defaults"]["show_civil_status"]
        self.data.config.show_signoff = meta["defaults"]["show_signoff"]

        # Synchroniser l'état des cases à cocher dans les onglets
        if hasattr(self, "cb_show_photo"):
            if self.data.config.show_photo:
                self.cb_show_photo.select()
            else:
                self.cb_show_photo.deselect()
        if hasattr(self, "cb_show_civil"):
            if self.data.config.show_civil_status:
                self.cb_show_civil.select()
            else:
                self.cb_show_civil.deselect()
        if hasattr(self, "cb_show_signoff"):
            if self.data.config.show_signoff:
                self.cb_show_signoff.select()
            else:
                self.cb_show_signoff.deselect()

    def _on_cv_lang_changed(self, choice: str):
        if "Français" in choice:
            self.data.config.cv_language = "fr"
        elif "English" in choice:
            self.data.config.cv_language = "en"
        else:
            self.data.config.cv_language = "de"

    def _on_style_changed(self, choice: str):
        for k, v in CV_STYLES.items():
            if v["name"] == choice:
                self.data.config.style_id = k
                self.data.config.primary_color = v["default_color"]
                break

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 1 : Informations Générales & État Civil
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_general(self):
        container = ctk.CTkScrollableFrame(self.tab_general, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        card_perso = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card_perso.pack(fill="x", padx=4, pady=(0, 10))

        lbl_h = ctk.CTkLabel(card_perso, text="IDENTITÉ & ACCROCHE PROFESSIONNELLE", font=ctk.CTkFont(size=13, weight="bold"), text_color=("#1e3a8a", "#60a5fa"))
        lbl_h.pack(anchor="w", padx=14, pady=(10, 6))

        # Rangée 1 : Prénom, Nom, Intitulé
        f_r1 = ctk.CTkFrame(card_perso, fg_color="transparent")
        f_r1.pack(fill="x", padx=14, pady=4)

        ctk.CTkLabel(f_r1, text="Prénom :").grid(row=0, column=0, sticky="w", padx=4)
        self.ent_fn = ctk.CTkEntry(f_r1, width=170)
        self.ent_fn.grid(row=1, column=0, sticky="w", padx=4, pady=(2, 6))

        ctk.CTkLabel(f_r1, text="Nom de famille :").grid(row=0, column=1, sticky="w", padx=4)
        self.ent_ln = ctk.CTkEntry(f_r1, width=170)
        self.ent_ln.grid(row=1, column=1, sticky="w", padx=4, pady=(2, 6))

        ctk.CTkLabel(f_r1, text="Intitulé du poste / Métier visé :").grid(row=0, column=2, sticky="w", padx=4)
        self.ent_title = ctk.CTkEntry(f_r1, width=320)
        self.ent_title.grid(row=1, column=2, sticky="w", padx=4, pady=(2, 6))

        # Rangée 2 : Photo d'identité
        f_photo = ctk.CTkFrame(card_perso, fg_color="transparent")
        f_photo.pack(fill="x", padx=14, pady=4)

        self.cb_show_photo = ctk.CTkCheckBox(f_photo, text="Afficher la photo d'identité (Déconseillé en version US/UK)", font=ctk.CTkFont(size=11, weight="bold"))
        self.cb_show_photo.select()
        self.cb_show_photo.pack(side="left", padx=4)

        self.btn_pick_photo = ctk.CTkButton(f_photo, text="Choisir photo...", width=120, height=24, command=self._pick_photo)
        self.btn_pick_photo.pack(side="left", padx=10)

        self.lbl_photo_status = ctk.CTkLabel(f_photo, text="Aucune photo sélectionnée", font=ctk.CTkFont(size=10, slant="italic"), text_color=("#64748b", "#94a3b8"))
        self.lbl_photo_status.pack(side="left")

        # Rangée 3 : Résumé / Accroche
        f_sum = ctk.CTkFrame(card_perso, fg_color="transparent")
        f_sum.pack(fill="x", padx=14, pady=6)

        ctk.CTkLabel(f_sum, text="Profil / Résumé professionnel (3 à 5 lignes percutantes) :").pack(anchor="w")
        self.txt_summary = ctk.CTkTextbox(f_sum, height=75)
        self.txt_summary.pack(fill="x", pady=(2, 6))

        # Carte Coordonnées & Réseaux
        card_contact = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card_contact.pack(fill="x", padx=4, pady=(0, 10))

        lbl_c = ctk.CTkLabel(card_contact, text="COORDONNÉES & LIENS PROFESSIONNELS", font=ctk.CTkFont(size=13, weight="bold"), text_color=("#1e3a8a", "#60a5fa"))
        lbl_c.pack(anchor="w", padx=14, pady=(10, 6))

        f_cgrid = ctk.CTkFrame(card_contact, fg_color="transparent")
        f_cgrid.pack(fill="x", padx=14, pady=(0, 10))

        ctk.CTkLabel(f_cgrid, text="Email :").grid(row=0, column=0, sticky="w", padx=4)
        self.ent_email = ctk.CTkEntry(f_cgrid, width=220)
        self.ent_email.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_cgrid, text="Téléphone :").grid(row=0, column=1, sticky="w", padx=4)
        self.ent_phone = ctk.CTkEntry(f_cgrid, width=170)
        self.ent_phone.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_cgrid, text="Ville & Pays :").grid(row=0, column=2, sticky="w", padx=4)
        self.ent_city = ctk.CTkEntry(f_cgrid, width=220)
        self.ent_city.grid(row=1, column=2, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_cgrid, text="Profil LinkedIn :").grid(row=2, column=0, sticky="w", padx=4, pady=(6, 0))
        self.ent_linkedin = ctk.CTkEntry(f_cgrid, width=220)
        self.ent_linkedin.grid(row=3, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_cgrid, text="GitHub / GitLab :").grid(row=2, column=1, sticky="w", padx=4, pady=(6, 0))
        self.ent_github = ctk.CTkEntry(f_cgrid, width=170)
        self.ent_github.grid(row=3, column=1, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_cgrid, text="Site / Portfolio :").grid(row=2, column=2, sticky="w", padx=4, pady=(6, 0))
        self.ent_portfolio = ctk.CTkEntry(f_cgrid, width=220)
        self.ent_portfolio.grid(row=3, column=2, sticky="w", padx=4, pady=2)

        # Carte État Civil (Selon pays)
        card_civil = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card_civil.pack(fill="x", padx=4, pady=(0, 10))

        f_chdr = ctk.CTkFrame(card_civil, fg_color="transparent")
        f_chdr.pack(fill="x", padx=14, pady=(10, 4))

        self.cb_show_civil = ctk.CTkCheckBox(
            f_chdr,
            text="Inclure l'État Civil (Traditionnel en France & Allemagne, Proscrit aux USA/UK)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.cb_show_civil.select()
        self.cb_show_civil.pack(side="left")

        f_civil_grid = ctk.CTkFrame(card_civil, fg_color="transparent")
        f_civil_grid.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkLabel(f_civil_grid, text="Date de naissance :").grid(row=0, column=0, sticky="w", padx=4)
        self.ent_dob = ctk.CTkEntry(f_civil_grid, width=160, placeholder_text="ex: 18/06/1993")
        self.ent_dob.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_civil_grid, text="Lieu de naissance (DACH Geburtsort) :").grid(row=0, column=1, sticky="w", padx=4)
        self.ent_pob = ctk.CTkEntry(f_civil_grid, width=180, placeholder_text="ex: Bouaké / Côte d'Ivoire")
        self.ent_pob.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_civil_grid, text="Nationalité :").grid(row=0, column=2, sticky="w", padx=4)
        self.ent_nat = ctk.CTkEntry(f_civil_grid, width=160, placeholder_text="ex: Française / Deutsch")
        self.ent_nat.grid(row=1, column=2, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_civil_grid, text="Permis de conduire :").grid(row=0, column=3, sticky="w", padx=4)
        self.ent_license = ctk.CTkEntry(f_civil_grid, width=160, placeholder_text="ex: Permis B")
        self.ent_license.grid(row=1, column=3, sticky="w", padx=4, pady=2)

    def _pick_photo(self):
        f = filedialog.askopenfilename(
            title="Sélectionner une photo professionnelle",
            filetypes=[("Images (*.jpg;*.jpeg;*.png)", "*.jpg *.jpeg *.png"), ("Tous les fichiers", "*.*")]
        )
        if f:
            self.data.general.photo_path = f
            self.lbl_photo_status.configure(text=Path(f).name, text_color=("#15803d", "#4ade80"))

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 2 : Expériences Professionnelles
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_experiences(self):
        top_bar = ctk.CTkFrame(self.tab_exp, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter une Expérience Professionnelle",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_experience_card()
        )
        btn_add.pack(side="left")

        self.scroll_exp = ctk.CTkScrollableFrame(self.tab_exp, fg_color="transparent")
        self.scroll_exp.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_experience_card(self, exp: Optional[CVExperience] = None):
        card = ctk.CTkFrame(self.scroll_exp, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=6, padx=4)

        f_top = ctk.CTkFrame(card, fg_color="transparent")
        f_top.pack(fill="x", padx=10, pady=(8, 2))

        ctk.CTkLabel(f_top, text="Poste :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4)
        ent_role = ctk.CTkEntry(f_top, width=240, placeholder_text="ex: Lead Developer Python")
        ent_role.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_top, text="Entreprise :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=4)
        ent_comp = ctk.CTkEntry(f_top, width=200, placeholder_text="ex: Airbus / Thales")
        ent_comp.grid(row=1, column=1, sticky="w", padx=4)

        ctk.CTkLabel(f_top, text="Lieu :").grid(row=0, column=2, sticky="w", padx=4)
        ent_loc = ctk.CTkEntry(f_top, width=140, placeholder_text="ex: Bouaké, Côte d'Ivoire")
        ent_loc.grid(row=1, column=2, sticky="w", padx=4)

        ctk.CTkLabel(f_top, text="Début / Fin :").grid(row=0, column=3, sticky="w", padx=4)
        f_dates = ctk.CTkFrame(f_top, fg_color="transparent")
        f_dates.grid(row=1, column=3, sticky="w", padx=4)

        ent_start = ctk.CTkEntry(f_dates, width=80, placeholder_text="09/2021")
        ent_start.pack(side="left")
        ctk.CTkLabel(f_dates, text="–").pack(side="left", padx=2)
        ent_end = ctk.CTkEntry(f_dates, width=80, placeholder_text="Présent")
        ent_end.pack(side="left")

        def _set_exp_period(s_val="2020", e_val="2026"):
            ent_start.delete(0, "end")
            ent_start.insert(0, s_val)
            ent_end.delete(0, "end")
            ent_end.insert(0, e_val)

        btn_date_adder = ctk.CTkButton(
            f_dates, text="2020-2026", width=75, height=24, font=ctk.CTkFont(size=9, weight="bold"),
            fg_color=("#e0f2fe", "#075985"), text_color=("#0369a1", "#e0f2fe"),
            hover_color=("#bae6fd", "#0284c7"),
            command=lambda: _set_exp_period("2020", "2026")
        )
        btn_date_adder.pack(side="left", padx=(4, 0))

        cb_cur = ctk.CTkCheckBox(f_top, text="Actuel")
        cb_cur.grid(row=1, column=4, padx=6)

        btn_del = ctk.CTkButton(
            f_top, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.exp_cards)
        )
        btn_del.grid(row=1, column=5, padx=(6, 0))

        # Description & Réalisations
        f_desc = ctk.CTkFrame(card, fg_color="transparent")
        f_desc.pack(fill="x", padx=10, pady=(4, 8))

        ctk.CTkLabel(f_desc, text="Description & Réalisations clés (1 puce par ligne précédée de • ou tiret) :", font=ctk.CTkFont(size=11)).pack(anchor="w")
        txt_desc = ctk.CTkTextbox(f_desc, height=70)
        txt_desc.pack(fill="x", pady=2)

        if exp:
            ent_role.insert(0, exp.job_title)
            ent_comp.insert(0, exp.company)
            ent_loc.insert(0, exp.location)
            ent_start.insert(0, exp.start_date)
            ent_end.insert(0, exp.end_date)
            if exp.is_current:
                cb_cur.select()
            desc_full = exp.description
            if exp.achievements:
                desc_full += "\n" + "\n".join([f"• {a}" for a in exp.achievements])
            txt_desc.insert("1.0", desc_full.strip())

        self.exp_cards.append({
            "frame": card,
            "role": ent_role,
            "company": ent_comp,
            "location": ent_loc,
            "start": ent_start,
            "end": ent_end,
            "is_current": cb_cur,
            "desc": txt_desc
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 3 : Études & Diplômes
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_education(self):
        top_bar = ctk.CTkFrame(self.tab_edu, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter une Formation / Diplôme",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_education_card()
        )
        btn_add.pack(side="left")

        self.scroll_edu = ctk.CTkScrollableFrame(self.tab_edu, fg_color="transparent")
        self.scroll_edu.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_education_card(self, edu: Optional[CVEducation] = None):
        card = ctk.CTkFrame(self.scroll_edu, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=6, padx=4)

        f_top = ctk.CTkFrame(card, fg_color="transparent")
        f_top.pack(fill="x", padx=10, pady=(8, 6))

        ctk.CTkLabel(f_top, text="Diplôme / Intitulé :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4)
        ent_deg = ctk.CTkEntry(f_top, width=280, placeholder_text="ex: Master en Informatique")
        ent_deg.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_top, text="Établissement / Université :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=4)
        ent_inst = ctk.CTkEntry(f_top, width=220, placeholder_text="ex: Sorbonne / INSA / KIT")
        ent_inst.grid(row=1, column=1, sticky="w", padx=4)

        ctk.CTkLabel(f_top, text="Années (ex: 2020 – 2026) :").grid(row=0, column=2, sticky="w", padx=4)
        f_edu_dates = ctk.CTkFrame(f_top, fg_color="transparent")
        f_edu_dates.grid(row=1, column=2, sticky="w", padx=4)
        ent_dates = ctk.CTkEntry(f_edu_dates, width=105, placeholder_text="2020 – 2026")
        ent_dates.pack(side="left")

        btn_edu_quick = ctk.CTkButton(
            f_edu_dates, text="2020-2026", width=75, height=24, font=ctk.CTkFont(size=9, weight="bold"),
            fg_color=("#e0f2fe", "#075985"), text_color=("#0369a1", "#e0f2fe"),
            hover_color=("#bae6fd", "#0284c7"),
            command=lambda: (ent_dates.delete(0, "end"), ent_dates.insert(0, "2020 – 2026"))
        )
        btn_edu_quick.pack(side="left", padx=(4, 0))

        btn_del = ctk.CTkButton(
            f_top, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.edu_cards)
        )
        btn_del.grid(row=1, column=3, padx=(6, 0))

        # Détails / Mention
        f_sub = ctk.CTkFrame(card, fg_color="transparent")
        f_sub.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(f_sub, text="Mention / Spécialisation / Précisions :", font=ctk.CTkFont(size=11)).pack(anchor="w")
        ent_det = ctk.CTkEntry(f_sub, placeholder_text="ex: Mention Très Bien • Major de promotion en architecture logicielle")
        ent_det.pack(fill="x", pady=2)

        if edu:
            ent_deg.insert(0, edu.degree)
            ent_inst.insert(0, edu.institution)
            dates_val = f"{edu.start_date} – {edu.end_date}" if edu.start_date and edu.end_date else (edu.end_date or edu.start_date)
            ent_dates.insert(0, dates_val)
            det_val = f"{edu.honors} • {edu.details}" if edu.honors and edu.details else (edu.honors or edu.details)
            ent_det.insert(0, det_val)

        self.edu_cards.append({
            "frame": card,
            "degree": ent_deg,
            "institution": ent_inst,
            "dates": ent_dates,
            "details": ent_det
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 4 : Certifications & Formations Continues
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_certifications(self):
        top_bar = ctk.CTkFrame(self.tab_cert, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter une Certification / Habilitation",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_certification_card()
        )
        btn_add.pack(side="left")

        self.scroll_cert = ctk.CTkScrollableFrame(self.tab_cert, fg_color="transparent")
        self.scroll_cert.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_certification_card(self, cert: Optional[CVCertification] = None):
        card = ctk.CTkFrame(self.scroll_cert, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=4, padx=4)

        f_row = ctk.CTkFrame(card, fg_color="transparent")
        f_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(f_row, text="Nom Certification :").grid(row=0, column=0, sticky="w", padx=4)
        ent_n = ctk.CTkEntry(f_row, width=320, placeholder_text="ex: AWS Certified Solutions Architect")
        ent_n.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Organisme délivreur :").grid(row=0, column=1, sticky="w", padx=4)
        ent_o = ctk.CTkEntry(f_row, width=220, placeholder_text="ex: Amazon Web Services / Scrum.org")
        ent_o.grid(row=1, column=1, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Année :").grid(row=0, column=2, sticky="w", padx=4)
        ent_y = ctk.CTkEntry(f_row, width=90, placeholder_text="2024")
        ent_y.grid(row=1, column=2, sticky="w", padx=4)

        btn_del = ctk.CTkButton(
            f_row, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.cert_cards)
        )
        btn_del.grid(row=1, column=3, padx=(6, 0))

        if cert:
            ent_n.insert(0, cert.name)
            ent_o.insert(0, cert.issuing_org)
            ent_y.insert(0, cert.issue_date)

        self.cert_cards.append({
            "frame": card,
            "name": ent_n,
            "org": ent_o,
            "year": ent_y
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 5 : Compétences Clés (Skills)
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_skills(self):
        top_bar = ctk.CTkFrame(self.tab_skills, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter une Compétence",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_skill_card()
        )
        btn_add.pack(side="left")

        self.scroll_skills = ctk.CTkScrollableFrame(self.tab_skills, fg_color="transparent")
        self.scroll_skills.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_skill_card(self, sk: Optional[CVSkill] = None):
        card = ctk.CTkFrame(self.scroll_skills, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=4, padx=4)

        f_row = ctk.CTkFrame(card, fg_color="transparent")
        f_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(f_row, text="Compétence / Outil :").grid(row=0, column=0, sticky="w", padx=4)
        ent_n = ctk.CTkEntry(f_row, width=320, placeholder_text="ex: Python, Docker, Gestion de projet")
        ent_n.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Catégorie :").grid(row=0, column=1, sticky="w", padx=4)
        combo_cat = ctk.CTkComboBox(f_row, values=["Technique", "Méthodologique", "Outils / Logiciels", "Soft Skills / Leadership"], width=200)
        combo_cat.set("Technique")
        combo_cat.grid(row=1, column=1, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Niveau (1 à 5 pastilles) :").grid(row=0, column=2, sticky="w", padx=4)
        combo_lvl = ctk.CTkComboBox(f_row, values=["5 (Expert / Maîtrise)", "4 (Très bon)", "3 (Bon / Opérationnel)", "2 (Intermédiaire)", "1 (Notions)"], width=170)
        combo_lvl.set("4 (Très bon)")
        combo_lvl.grid(row=1, column=2, sticky="w", padx=4)

        btn_del = ctk.CTkButton(
            f_row, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.skill_cards)
        )
        btn_del.grid(row=1, column=3, padx=(6, 0))

        if sk:
            ent_n.insert(0, sk.name)
            combo_cat.set(sk.category or "Technique")
            for v in ["5 (Expert / Maîtrise)", "4 (Très bon)", "3 (Bon / Opérationnel)", "2 (Intermédiaire)", "1 (Notions)"]:
                if v.startswith(str(sk.level)):
                    combo_lvl.set(v)
                    break

        self.skill_cards.append({
            "frame": card,
            "name": ent_n,
            "cat": combo_cat,
            "level": combo_lvl
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 6 : Langues Parlées (CECR / Descriptif / Pastilles)
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_languages(self):
        top_bar = ctk.CTkFrame(self.tab_lang, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter une Langue",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_language_card()
        )
        btn_add.pack(side="left")

        lbl_info = ctk.CTkLabel(
            top_bar,
            text="💡 Chaque langue supporte 3 modes d'évaluation : CECRL officiel (A1-C2), Libellé textuel ou Pastilles (●●●○○).",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color=("#475569", "#94a3b8")
        )
        lbl_info.pack(side="left", padx=16)

        self.scroll_lang = ctk.CTkScrollableFrame(self.tab_lang, fg_color="transparent")
        self.scroll_lang.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_language_card(self, lang_item: Optional[CVLanguage] = None):
        card = ctk.CTkFrame(self.scroll_lang, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=4, padx=4)

        f_row = ctk.CTkFrame(card, fg_color="transparent")
        f_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(f_row, text="Langue :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4)
        combo_name = ctk.CTkComboBox(f_row, values=["Français", "Anglais", "Allemand", "Espagnol", "Italien", "Mandarin", "Arabe", "Russe", "Japonais", "Portugais"], width=150)
        combo_name.set("Anglais")
        combo_name.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Mode d'Évaluation :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=4)
        combo_mode = ctk.CTkComboBox(
            f_row,
            values=["Échelle CECRL (A1 - C2)", "Libellé Descriptif", "Pastilles / Points (●●●●○)"],
            width=200
        )
        combo_mode.set("Échelle CECRL (A1 - C2)")
        combo_mode.grid(row=1, column=1, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Niveau sélectionné :", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=4)
        combo_val = ctk.CTkComboBox(
            f_row,
            values=[
                "C2 - Maîtrise / Bilingue",
                "C1 - Autonome / Courant",
                "B2 - Avancé / Intermédiaire sup.",
                "B1 - Seuil / Opérationnel",
                "A2 - Élémentaire",
                "A1 - Débutant / Notions"
            ],
            width=260
        )
        combo_val.set("B2 - Avancé / Intermédiaire sup.")
        combo_val.grid(row=1, column=2, sticky="w", padx=4)

        def on_mode_change(choice):
            if "CECRL" in choice:
                combo_val.configure(values=[
                    "C2 - Maîtrise / Bilingue",
                    "C1 - Autonome / Courant",
                    "B2 - Avancé / Intermédiaire sup.",
                    "B1 - Seuil / Opérationnel",
                    "A2 - Élémentaire",
                    "A1 - Débutant / Notions"
                ])
                combo_val.set("B2 - Avancé / Intermédiaire sup.")
            elif "Descriptif" in choice:
                combo_val.configure(values=DESCRIPTIVE_LEVELS["fr"])
                combo_val.set("Courant (Professionnel)")
            else:
                combo_val.configure(values=[
                    "5 points (●●●●●)",
                    "4 points (●●●●○)",
                    "3 points (●●●○○)",
                    "2 points (●●○○○)",
                    "1 point  (●○○○○)"
                ])
                combo_val.set("4 points (●●●●○)")

        combo_mode.configure(command=on_mode_change)

        btn_del = ctk.CTkButton(
            f_row, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.lang_cards)
        )
        btn_del.grid(row=1, column=3, padx=(10, 0))

        if lang_item:
            combo_name.set(lang_item.language)
            if lang_item.eval_mode == "cecr":
                combo_mode.set("Échelle CECRL (A1 - C2)")
                on_mode_change("CECRL")
                for v in combo_val.cget("values"):
                    if v.startswith(lang_item.cecr_level):
                        combo_val.set(v)
                        break
            elif lang_item.eval_mode == "dots":
                combo_mode.set("Pastilles / Points (●●●●○)")
                on_mode_change("Pastilles")
                for v in combo_val.cget("values"):
                    if v.startswith(str(lang_item.dots)):
                        combo_val.set(v)
                        break
            else:
                combo_mode.set("Libellé Descriptif")
                on_mode_change("Descriptif")
                combo_val.set(lang_item.desc_level)

        self.lang_cards.append({
            "frame": card,
            "lang": combo_name,
            "mode": combo_mode,
            "val": combo_val
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 7 : Hobbys & Centres d'Intérêt
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_hobbies(self):
        top_bar = ctk.CTkFrame(self.tab_hobbies, fg_color="transparent")
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        btn_add = ctk.CTkButton(
            top_bar,
            text=" Ajouter un Centre d'Intérêt / Passion",
            image=self.icons.get_white_icon("plus", 14),
            compound="left",
            height=32,
            font=ctk.CTkFont(weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=lambda: self._add_hobby_card()
        )
        btn_add.pack(side="left")

        self.scroll_hobbies = ctk.CTkScrollableFrame(self.tab_hobbies, fg_color="transparent")
        self.scroll_hobbies.pack(fill="both", expand=True, padx=8, pady=4)

    def _add_hobby_card(self, h: Optional[CVHobby] = None):
        card = ctk.CTkFrame(self.scroll_hobbies, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", pady=4, padx=4)

        f_row = ctk.CTkFrame(card, fg_color="transparent")
        f_row.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(f_row, text="Activité / Passion :").grid(row=0, column=0, sticky="w", padx=4)
        ent_n = ctk.CTkEntry(f_row, width=240, placeholder_text="ex: Course à pied, Échecs, Bénévolat")
        ent_n.grid(row=1, column=0, sticky="w", padx=4)

        ctk.CTkLabel(f_row, text="Précisions / Niveau / Réalisation :").grid(row=0, column=1, sticky="w", padx=4)
        ent_d = ctk.CTkEntry(f_row, width=420, placeholder_text="ex: Marathonien, pratique associative, etc.")
        ent_d.grid(row=1, column=1, sticky="w", padx=4)

        btn_del = ctk.CTkButton(
            f_row, text="", image=self.icons.get_icon("trash", 13, "#ef4444", "#f87171"),
            width=28, height=26, fg_color=("#fee2e2", "#450a0a"), hover_color=("#fecaca", "#7f1d1d"),
            command=lambda: self._remove_card(card, self.hobby_cards)
        )
        btn_del.grid(row=1, column=2, padx=(6, 0))

        if h:
            ent_n.insert(0, h.name)
            ent_d.insert(0, h.details)

        self.hobby_cards.append({
            "frame": card,
            "name": ent_n,
            "details": ent_d
        })

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 8 : Signature & Mentions DACH (Ort, Datum, Unterschrift)
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_signoff(self):
        container = ctk.CTkFrame(self.tab_signoff, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        card = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card.pack(fill="x", padx=4, pady=4)

        lbl_h = ctk.CTkLabel(card, text="CLÔTURE & SIGNATURE (TRADITION ALLEMANDE DACH)", font=ctk.CTkFont(size=13, weight="bold"), text_color=("#1e3a8a", "#60a5fa"))
        lbl_h.pack(anchor="w", padx=14, pady=(10, 4))

        self.cb_show_signoff = ctk.CTkCheckBox(
            card,
            text="Activer la section 'Lieu, Date et Signature' au bas du CV (Recommandé pour Allemagne / Suisse / Autriche)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.cb_show_signoff.pack(anchor="w", padx=14, pady=(6, 12))

        f_grid = ctk.CTkFrame(card, fg_color="transparent")
        f_grid.pack(fill="x", padx=14, pady=(0, 14))

        ctk.CTkLabel(f_grid, text="Lieu de rédaction (Ort) :").grid(row=0, column=0, sticky="w", padx=4)
        self.ent_sign_place = ctk.CTkEntry(f_grid, width=200, placeholder_text="ex: Bouaké / Côte d'Ivoire")
        self.ent_sign_place.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_grid, text="Date de rédaction (Datum) :").grid(row=0, column=1, sticky="w", padx=4)
        self.ent_sign_date = ctk.CTkEntry(f_grid, width=200, placeholder_text="ex: 27. Oktober 2026")
        self.ent_sign_date.insert(0, date.today().strftime("%d/%m/%Y"))
        self.ent_sign_date.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(f_grid, text="Nom pour signature manuscrite :").grid(row=0, column=2, sticky="w", padx=4)
        self.ent_sign_name = ctk.CTkEntry(f_grid, width=240, placeholder_text="ex: Osiris XXXXXXX")
        self.ent_sign_name.grid(row=1, column=2, sticky="w", padx=4, pady=2)

        btn_sign_img = ctk.CTkButton(
            f_grid,
            text="Image signature...",
            width=130,
            command=self._pick_signature_image
        )
        btn_sign_img.grid(row=1, column=3, sticky="w", padx=10, pady=2)

    def _pick_signature_image(self):
        f = filedialog.askopenfilename(
            title="Sélectionner une image de signature scannée",
            filetypes=[("Images (*.png;*.jpg)", "*.png *.jpg *.jpeg")]
        )
        if f:
            self.data.signoff.signature_image_path = f
            messagebox.showinfo("Signature", f"Image de signature chargée : {Path(f).name}")

    # ═════════════════════════════════════════════════════════════════════════
    #  Onglet 9 : Styles, Prévisualisation & Export
    # ═════════════════════════════════════════════════════════════════════════

    def _build_tab_export(self):
        container = ctk.CTkScrollableFrame(self.tab_export, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # Carte Palette de couleurs
        card_col = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card_col.pack(fill="x", padx=4, pady=(0, 10))

        lbl_c = ctk.CTkLabel(card_col, text="PALETTE DE COULEURS D'ACCENTUATION", font=ctk.CTkFont(size=13, weight="bold"), text_color=("#1e3a8a", "#60a5fa"))
        lbl_c.pack(anchor="w", padx=14, pady=(10, 6))

        f_pals = ctk.CTkFrame(card_col, fg_color="transparent")
        f_pals.pack(fill="x", padx=10, pady=(0, 10))

        for idx, pal in enumerate(COLOR_PALETTES):
            btn_p = ctk.CTkButton(
                f_pals,
                text=pal["name"],
                fg_color=pal["hex"],
                hover_color=pal["hex"],
                text_color="#ffffff",
                height=30,
                command=lambda h=pal["hex"]: self._set_primary_color(h)
            )
            btn_p.grid(row=idx // 3, column=idx % 3, sticky="we", padx=4, pady=3)
            f_pals.grid_columnconfigure(idx % 3, weight=1)

        # Carte Actions d'exportation
        card_exp = ctk.CTkFrame(container, fg_color=("#ffffff", "#1e293b"), corner_radius=8)
        card_exp.pack(fill="x", padx=4, pady=(0, 10))

        lbl_e = ctk.CTkLabel(card_exp, text="GÉNÉRATION & EXPORTATION DES DOCUMENTS", font=ctk.CTkFont(size=13, weight="bold"), text_color=("#1e3a8a", "#60a5fa"))
        lbl_e.pack(anchor="w", padx=14, pady=(10, 8))

        f_btn_grid = ctk.CTkFrame(card_exp, fg_color="transparent")
        f_btn_grid.pack(fill="x", padx=14, pady=(0, 14))

        btn_pdf_big = ctk.CTkButton(
            f_btn_grid,
            text=" Exporter en PDF Haute Résolution",
            image=self.icons.get_white_icon("download", 16),
            compound="left",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#1e3a8a", "#1d4ed8"),
            hover_color=("#1e40af", "#1e3a8a"),
            command=self._export_pdf
        )
        btn_pdf_big.grid(row=0, column=0, sticky="we", padx=6, pady=4)

        btn_docx_big = ctk.CTkButton(
            f_btn_grid,
            text=" Exporter en Document Word (.docx)",
            image=self.icons.get_white_icon("doc_word", 16),
            compound="left",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#0284c7", "#0369a1"),
            hover_color=("#0369a1", "#075985"),
            command=self._export_docx
        )
        btn_docx_big.grid(row=0, column=1, sticky="we", padx=6, pady=4)

        btn_html_big = ctk.CTkButton(
            f_btn_grid,
            text=" Prévisualiser dans le Navigateur Web",
            image=self.icons.get_white_icon("eye", 16),
            compound="left",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#0f766e", "#14b8a6"),
            hover_color=("#0d9488", "#0f766e"),
            command=self._preview_html
        )
        btn_html_big.grid(row=1, column=0, sticky="we", padx=6, pady=4)

        btn_save_json = ctk.CTkButton(
            f_btn_grid,
            text=" Sauvegarder Profil (.json)",
            image=self.icons.get_white_icon("save", 16),
            compound="left",
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color=("#475569", "#334155"),
            hover_color=("#334155", "#1e293b"),
            command=self._save_json_file
        )
        btn_save_json.grid(row=1, column=1, sticky="we", padx=6, pady=4)

        f_btn_grid.grid_columnconfigure(0, weight=1)
        f_btn_grid.grid_columnconfigure(1, weight=1)

    def _set_primary_color(self, hex_color: str):
        self.data.config.primary_color = hex_color
        messagebox.showinfo("Couleur Appliquée", f"Couleur principale mise à jour : {hex_color}")

    # ═════════════════════════════════════════════════════════════════════════
    #  Collecte des données & Synchronisation
    # ═════════════════════════════════════════════════════════════════════════

    def _collect_data(self) -> CVData:
        d = self.data

        # 1. Infos générales
        g = d.general
        g.first_name = self.ent_fn.get().strip()
        g.last_name = self.ent_ln.get().strip()
        g.target_title = self.ent_title.get().strip()
        g.summary = self.txt_summary.get("1.0", "end").strip()
        g.email = self.ent_email.get().strip()
        g.phone = self.ent_phone.get().strip()
        raw_loc = self.ent_city.get().strip()
        if not raw_loc:
            g.city = ""
            g.country = ""
        elif "," in raw_loc:
            parts = [p.strip() for p in raw_loc.split(",", 1)]
            g.city = parts[0]
            g.country = parts[1]
        else:
            g.city = raw_loc
            g.country = ""
        g.linkedin = self.ent_linkedin.get().strip()
        g.github = self.ent_github.get().strip()
        g.portfolio_url = self.ent_portfolio.get().strip()
        g.date_of_birth = self.ent_dob.get().strip()
        g.place_of_birth = self.ent_pob.get().strip()
        g.nationality = self.ent_nat.get().strip()
        g.driving_license = self.ent_license.get().strip()

        d.config.show_photo = (self.cb_show_photo.get() == 1)
        d.config.show_civil_status = (self.cb_show_civil.get() == 1)
        d.config.show_signoff = (self.cb_show_signoff.get() == 1)

        # 2. Expériences
        d.experiences = []
        for card in self.exp_cards:
            role = card["role"].get().strip()
            comp = card["company"].get().strip()
            if not role and not comp:
                continue
            desc_raw = card["desc"].get("1.0", "end").strip()
            lines = desc_raw.splitlines()
            main_desc = []
            achievements = []
            for l in lines:
                l_s = l.strip()
                if l_s.startswith("•") or l_s.startswith("-") or l_s.startswith("*"):
                    achievements.append(l_s.lstrip("•-* ").strip())
                else:
                    main_desc.append(l_s)

            d.experiences.append(CVExperience(
                job_title=role,
                company=comp,
                location=card["location"].get().strip(),
                start_date=card["start"].get().strip(),
                end_date=card["end"].get().strip(),
                is_current=(card["is_current"].get() == 1),
                description="\n".join(main_desc),
                achievements=achievements
            ))

        # 3. Études
        d.education = []
        for card in self.edu_cards:
            deg = card["degree"].get().strip()
            inst = card["institution"].get().strip()
            if not deg and not inst:
                continue
            d.education.append(CVEducation(
                degree=deg,
                institution=inst,
                end_date=card["dates"].get().strip(),
                details=card["details"].get().strip()
            ))

        # 4. Certifications
        d.certifications = []
        for card in self.cert_cards:
            name = card["name"].get().strip()
            if not name:
                continue
            d.certifications.append(CVCertification(
                name=name,
                issuing_org=card["org"].get().strip(),
                issue_date=card["year"].get().strip()
            ))

        # 5. Compétences
        d.skills = []
        for card in self.skill_cards:
            name = card["name"].get().strip()
            if not name:
                continue
            lvl_str = card["level"].get()
            lvl = int(lvl_str[0]) if lvl_str and lvl_str[0].isdigit() else 4
            d.skills.append(CVSkill(
                name=name,
                category=card["cat"].get(),
                level=lvl
            ))

        # 6. Langues
        d.languages = []
        for card in self.lang_cards:
            name = card["lang"].get().strip()
            mode_str = card["mode"].get()
            val_str = card["val"].get()

            if "CECRL" in mode_str:
                em = "cecr"
                cecr_code = val_str[:2]
                dots_cnt = 4
                desc_txt = val_str
            elif "Pastilles" in mode_str:
                em = "dots"
                cecr_code = "B2"
                dots_cnt = int(val_str[0]) if val_str and val_str[0].isdigit() else 4
                desc_txt = f"{dots_cnt}/5"
            else:
                em = "descriptive"
                cecr_code = "B2"
                dots_cnt = 4
                desc_txt = val_str

            d.languages.append(CVLanguage(
                language=name,
                eval_mode=em,
                cecr_level=cecr_code,
                desc_level=desc_txt,
                dots=dots_cnt
            ))

        # 7. Hobbys
        d.hobbies = []
        for card in self.hobby_cards:
            name = card["name"].get().strip()
            if not name:
                continue
            d.hobbies.append(CVHobby(
                name=name,
                details=card["details"].get().strip()
            ))

        # 8. Signature DACH
        d.signoff.enabled = (self.cb_show_signoff.get() == 1)
        d.signoff.place = self.ent_sign_place.get().strip()
        d.signoff.date_str = self.ent_sign_date.get().strip()
        d.signoff.signature_name = self.ent_sign_name.get().strip()

        return d

    def _remove_card(self, frame_to_remove, cards_list):
        for idx, c in enumerate(cards_list):
            if c["frame"] == frame_to_remove:
                del cards_list[idx]
                break
        frame_to_remove.destroy()

    # ═════════════════════════════════════════════════════════════════════════
    #  Chargement de Démo / Remplissage / Réinitialisation Vierge
    # ═════════════════════════════════════════════════════════════════════════

    def _clear_all_fields_blank(self):
        """Réinitialise tous les champs du CV pour démarrer sur un formulaire 100% vierge."""
        if messagebox.askyesno("Vider tous les champs", "Voulez-vous vider entièrement le CV pour démarrer sur un formulaire 100% vierge ?"):
            self.data = CVData()
            self._sync_ui_with_data()
            messagebox.showinfo("Formulaire Vierge", "Tous les champs du CV ont été réinitialisés à vide.")

    def _load_demo_data(self, lang_code: str, confirm_dialog: bool = True):
        if confirm_dialog:
            if not messagebox.askyesno("Charger Modèle Démo", f"Voulez-vous charger l'exemple complet en version '{lang_code.upper()}' ?\nVos saisies actuelles seront remplacées."):
                return

        demo_dict = DEMO_PROFILES.get(lang_code, DEMO_PROFILES["fr"])
        self.data = CVData.from_dict(demo_dict)

        # Mettre à jour l'IHM
        self._sync_ui_with_data()

    def _sync_ui_with_data(self):
        d = self.data
        gen = d.general

        # Onglet 1
        if hasattr(self, "ent_fn"):
            self.ent_fn.delete(0, "end")
            self.ent_fn.insert(0, gen.first_name)
            self.ent_ln.delete(0, "end")
            self.ent_ln.insert(0, gen.last_name)
            self.ent_title.delete(0, "end")
            self.ent_title.insert(0, gen.target_title)
            self.txt_summary.delete("1.0", "end")
            self.txt_summary.insert("1.0", gen.summary)

            self.ent_email.delete(0, "end")
            self.ent_email.insert(0, gen.email)
            self.ent_phone.delete(0, "end")
            self.ent_phone.insert(0, gen.phone)
            self.ent_city.delete(0, "end")
            if gen.city and gen.country and gen.country.lower() not in gen.city.lower():
                self.ent_city.insert(0, f"{gen.city}, {gen.country}")
            elif gen.city:
                self.ent_city.insert(0, gen.city)
            elif gen.country:
                self.ent_city.insert(0, gen.country)
            self.ent_linkedin.delete(0, "end")
            self.ent_linkedin.insert(0, gen.linkedin)
            self.ent_github.delete(0, "end")
            self.ent_github.insert(0, gen.github)
            self.ent_portfolio.delete(0, "end")
            self.ent_portfolio.insert(0, gen.portfolio_url)

            self.ent_dob.delete(0, "end")
            self.ent_dob.insert(0, gen.date_of_birth)
            self.ent_pob.delete(0, "end")
            self.ent_pob.insert(0, gen.place_of_birth)
            self.ent_nat.delete(0, "end")
            self.ent_nat.insert(0, gen.nationality)
            self.ent_license.delete(0, "end")
            self.ent_license.insert(0, gen.driving_license)

            if d.config.show_photo:
                self.cb_show_photo.select()
            else:
                self.cb_show_photo.deselect()
            if d.config.show_civil_status:
                self.cb_show_civil.select()
            else:
                self.cb_show_civil.deselect()
            if d.config.show_signoff:
                self.cb_show_signoff.select()
            else:
                self.cb_show_signoff.deselect()

        # Onglet 2 : Expériences
        if hasattr(self, "scroll_exp"):
            for c in list(self.exp_cards):
                c["frame"].destroy()
            self.exp_cards.clear()
            for exp in d.experiences:
                self._add_experience_card(exp)

        # Onglet 3 : Études
        if hasattr(self, "scroll_edu"):
            for c in list(self.edu_cards):
                c["frame"].destroy()
            self.edu_cards.clear()
            for edu in d.education:
                self._add_education_card(edu)

        # Onglet 4 : Certifications
        if hasattr(self, "scroll_cert"):
            for c in list(self.cert_cards):
                c["frame"].destroy()
            self.cert_cards.clear()
            for cert in d.certifications:
                self._add_certification_card(cert)

        # Onglet 5 : Compétences
        if hasattr(self, "scroll_skills"):
            for c in list(self.skill_cards):
                c["frame"].destroy()
            self.skill_cards.clear()
            for sk in d.skills:
                self._add_skill_card(sk)

        # Onglet 6 : Langues
        if hasattr(self, "scroll_lang"):
            for c in list(self.lang_cards):
                c["frame"].destroy()
            self.lang_cards.clear()
            for l in d.languages:
                self._add_language_card(l)

        # Onglet 7 : Hobbys
        if hasattr(self, "scroll_hobbies"):
            for c in list(self.hobby_cards):
                c["frame"].destroy()
            self.hobby_cards.clear()
            for h in d.hobbies:
                self._add_hobby_card(h)

        # Onglet 8 : Signoff
        if hasattr(self, "ent_sign_place"):
            self.ent_sign_place.delete(0, "end")
            self.ent_sign_place.insert(0, d.signoff.place)
            self.ent_sign_date.delete(0, "end")
            self.ent_sign_date.insert(0, d.signoff.date_str or date.today().strftime("%d/%m/%Y"))
            self.ent_sign_name.delete(0, "end")
            self.ent_sign_name.insert(0, d.signoff.signature_name)

        # Menus déroulants Top bar
        if hasattr(self, "combo_country"):
            c_map = {"fr": "France & Francophone (FR)", "en": "Anglophone US/UK (EN)", "de": "Germanophone DACH (DE)"}
            self.combo_country.set(c_map.get(d.config.country_version, "France & Francophone (FR)"))
        if hasattr(self, "combo_cv_lang"):
            l_map = {"fr": "Français (FR)", "en": "English (EN)", "de": "Deutsch (DE)"}
            self.combo_cv_lang.set(l_map.get(d.config.cv_language, "Français (FR)"))
        if hasattr(self, "combo_style"):
            st_info = CV_STYLES.get(d.config.style_id, CV_STYLES["modern_minimalist"])
            self.combo_style.set(st_info["name"])

    # ═════════════════════════════════════════════════════════════════════════
    #  Actions d'Exportation (PDF, DOCX, HTML, JSON)
    # ═════════════════════════════════════════════════════════════════════════

    def _preview_html(self):
        """Génère un rendu HTML pixel-perfect et l'ouvre dans le navigateur."""
        data = self._collect_data()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        html_file = OUTPUT_DIR / "preview_cv.html"

        html_content = generate_cv_html(data)
        html_file.write_text(html_content, encoding="utf-8")

        webbrowser.open(str(html_file.resolve()))

    def _export_pdf(self):
        """Génère le document PDF vectoriel via ReportLab."""
        data = self._collect_data()
        fn = f"CV_{data.general.first_name}_{data.general.last_name}_{data.config.country_version.upper()}.pdf".replace(" ", "_")
        
        target = filedialog.asksaveasfilename(
            title="Enregistrer le CV en PDF",
            initialdir=str(OUTPUT_DIR),
            initialfile=fn,
            filetypes=[("Document PDF (*.pdf)", "*.pdf")]
        )
        if not target:
            return

        try:
            pdf_path = generate_cv_pdf(data, target)
            if messagebox.askyesno("Succès", f"Le PDF a été généré avec succès :\n{pdf_path}\n\nVoulez-vous l'ouvrir maintenant ?"):
                os.startfile(pdf_path)
        except Exception as e:
            messagebox.showerror("Erreur d'exportation PDF", str(e))

    def _export_docx(self):
        """Génère le document Word .docx."""
        data = self._collect_data()
        fn = f"CV_{data.general.first_name}_{data.general.last_name}_{data.config.country_version.upper()}.docx".replace(" ", "_")

        target = filedialog.asksaveasfilename(
            title="Enregistrer le CV en Word",
            initialdir=str(OUTPUT_DIR),
            initialfile=fn,
            filetypes=[("Document Word (*.docx)", "*.docx")]
        )
        if not target:
            return

        try:
            docx_path = generate_cv_docx(data, target)
            if messagebox.askyesno("Succès", f"Le document Word a été généré avec succès :\n{docx_path}\n\nVoulez-vous l'ouvrir maintenant ?"):
                os.startfile(docx_path)
        except Exception as e:
            messagebox.showerror("Erreur d'exportation Word", str(e))

    def _save_json_file(self):
        """Sauvegarde les données dans un fichier JSON réutilisable."""
        data = self._collect_data()
        fn = f"profil_cv_{data.general.first_name}_{data.general.last_name}.json".replace(" ", "_")
        target = filedialog.asksaveasfilename(
            title="Sauvegarder le profil CV",
            initialdir=str(BASE_DIR),
            initialfile=fn,
            filetypes=[("Fichier JSON (*.json)", "*.json")]
        )
        if target:
            data.save_json(target)
            messagebox.showinfo("Sauvegarde", f"Profil sauvegardé avec succès dans :\n{target}")


def main():
    app = CVEditorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
