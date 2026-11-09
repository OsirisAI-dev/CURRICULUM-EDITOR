"""
Modèles de données pour l'Éditeur Professionnel de Curriculum Vitae (CV).
Supporte les versions régionales (France / Francophone, Pays Anglophones US/UK, Pays Germanophones DACH),
le multilinguisme (Français, Anglais, Allemand), les systèmes d'évaluation linguistique (CECR / Descriptif / Points)
et les configurations de styles visuels.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class CVGeneralInfo:
    """Informations générales et état civil."""
    first_name: str = ""
    last_name: str = ""
    target_title: str = ""        # Intitulé du poste visé / Professional Title
    summary: str = ""             # Profil / Accroche / Professional Summary / Kurzprofil
    photo_path: str = ""          # Chemin vers la photo d'identité
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    postal_code: str = ""
    country: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio_url: str = ""
    
    # Données d'état civil (conventionnelles en Allemagne/Afrique/Europe, proscrites aux USA/UK)
    date_of_birth: str = ""       # Ex: 15/04/1992
    place_of_birth: str = ""      # Ex: Bouaké / Côte d'Ivoire (Essentiel en Allemagne : Geburtsort)
    nationality: str = ""         # Ex: Ivoirienne / Deutsch / British
    driving_license: str = ""     # Ex: Permis B / Driving Licence Class B / Führerschein Kl. B
    marital_status: str = ""      # Ex: Célibataire / Single / Ledig (Optionnel DACH/FR)


@dataclass
class CVExperience:
    """Expérience professionnelle / Work Experience / Berufserfahrung."""
    id: str = ""
    job_title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""          # Ex: 09/2021 ou Sept 2021
    end_date: str = ""            # Ex: Présent / Present / Heute ou 06/2024
    is_current: bool = False
    description: str = ""
    achievements: List[str] = field(default_factory=list)  # Réalisations clés / Bullet points


@dataclass
class CVEducation:
    """Études et Diplômes / Education & Qualifications / Ausbildung & Studium."""
    id: str = ""
    degree: str = ""              # Ex: Master en Informatique / B.Sc. Computer Science
    institution: str = ""         # Établissement / Université
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    field_of_study: str = ""
    honors: str = ""              # Mention / Note / Grade (ex: Mention Très Bien / First Class / 1,3)
    details: str = ""


@dataclass
class CVCertification:
    """Certifications et Formations continues / Weiterbildung & Zertifikate."""
    id: str = ""
    name: str = ""                # Nom du certificat / formation
    issuing_org: str = ""         # Organisme délivreur (ex: AWS, Goethe Institut, Scrum.org)
    issue_date: str = ""          # Année ou date d'obtention
    credential_id: str = ""       # Numéro / Lien du certificat


@dataclass
class CVSkill:
    """Compétences clés / Core Skills / Kenntnisse."""
    id: str = ""
    name: str = ""
    category: str = "Technique"   # Technique, Managériale, Outils, Soft Skills
    level: int = 4                # 1 à 5 (utilisé pour les barres graphiques ou étoiles)


@dataclass
class CVLanguage:
    """
    Langues parlées / Spoken Languages / Sprachkenntnisse.
    Systèmes d'évaluation pris en charge :
    1. 'cecr' : A1, A2, B1, B2, C1, C2 (Cadre Européen Commun de Référence)
    2. 'descriptive' : Débutant, Élémentaire, Intermédiaire, Avancé, Courant, Bilingue / Langue maternelle
    3. 'dots' : 1 à 5 points / cercles visuels (●●●●○)
    """
    id: str = ""
    language: str = ""            # Nom de la langue (Français, Anglais, Allemand, Espagnol...)
    eval_mode: str = "cecr"       # 'cecr', 'descriptive', 'dots'
    cecr_level: str = "B2"        # A1, A2, B1, B2, C1, C2
    desc_level: str = "Courant"   # Libellé textuel
    dots: int = 4                 # 1 à 5


@dataclass
class CVHobby:
    """Centres d'intérêt / Hobbies & Interests / Hobbys & Interessen."""
    id: str = ""
    name: str = ""                # Ex: Photographie, Échecs, Marathon, Bénévolat
    details: str = ""             # Ex: Pratique en club, semi-marathon en 1h45


@dataclass
class CVSignOff:
    """
    Section signature et date (Tradition essentielle du Lebenslauf allemand / DACH).
    "Ort, Datum und Unterschrift"
    """
    enabled: bool = False
    place: str = ""               # Ex: Bouaké / Côte d'Ivoire
    date_str: str = ""            # Ex: 27. Oktober 2026
    signature_name: str = ""      # Nom pour signature textuelle
    signature_image_path: str = ""# Image de signature scannée (optionnel)


@dataclass
class CVConfig:
    """Paramètres régionaux, linguistiques et stylistiques du CV."""
    country_version: str = "fr"   # 'fr' (France/Francophonie), 'en' (US/UK International), 'de' (DACH / Allemagne)
    cv_language: str = "fr"       # 'fr' (Français), 'en' (English), 'de' (Deutsch)
    style_id: str = "modern_minimalist" 
    # Styles disponibles :
    # 'modern_minimalist' : Design épuré contemporain, équilibre parfait du blanc
    # 'creative_sidebar'  : Colonne latérale de couleur + contenu principal
    # 'executive_classic' : Style sobre, élégant, symétrique (Corporate / Droit / Finance)
    # 'german_tabular'    : Lebenslauf tabulaire officiel DACH avec colonne de dates à gauche
    # 'tech_compact'      : Format optimisé pour profils tech et développeurs
    # 'academic_europass' : Structure académique complète

    primary_color: str = "#1e3a8a"  # Couleur d'accentuation (Bleu nuit par défaut)
    secondary_color: str = "#0284c7"# Couleur d'appoint
    dark_text_color: str = "#0f172a"
    light_bg_color: str = "#f8fafc"
    
    show_photo: bool = True       # En mode 'en', conseillé False
    show_civil_status: bool = True# En mode 'en', conseillé False (Anti-discrimination)
    show_signoff: bool = False    # En mode 'de', conseillé True (Ort, Datum, Unterschrift)


@dataclass
class CVData:
    """Conteneur principal de toutes les données du CV."""
    general: CVGeneralInfo = field(default_factory=CVGeneralInfo)
    experiences: List[CVExperience] = field(default_factory=list)
    education: List[CVEducation] = field(default_factory=list)
    certifications: List[CVCertification] = field(default_factory=list)
    skills: List[CVSkill] = field(default_factory=list)
    languages: List[CVLanguage] = field(default_factory=list)
    hobbies: List[CVHobby] = field(default_factory=list)
    signoff: CVSignOff = field(default_factory=CVSignOff)
    config: CVConfig = field(default_factory=CVConfig)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CVData:
        cv = cls()
        if "general" in data:
            cv.general = CVGeneralInfo(**data["general"])
        if "experiences" in data:
            cv.experiences = [CVExperience(**item) for item in data["experiences"]]
        if "education" in data:
            cv.education = [CVEducation(**item) for item in data["education"]]
        if "certifications" in data:
            cv.certifications = [CVCertification(**item) for item in data["certifications"]]
        if "skills" in data:
            cv.skills = [CVSkill(**item) for item in data["skills"]]
        if "languages" in data:
            cv.languages = [CVLanguage(**item) for item in data["languages"]]
        if "hobbies" in data:
            cv.hobbies = [CVHobby(**item) for item in data["hobbies"]]
        if "signoff" in data:
            cv.signoff = CVSignOff(**data["signoff"])
        if "config" in data:
            cv.config = CVConfig(**data["config"])
        return cv

    def save_json(self, filepath: Path | str) -> None:
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, filepath: Path | str) -> CVData:
        p = Path(filepath)
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
