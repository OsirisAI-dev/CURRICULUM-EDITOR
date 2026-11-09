"""
Dictionnaire de traductions, métadonnées régionales, échelles linguistiques CECR
et modèles types (Démo pré-remplie FR, EN, DE) pour l'Éditeur de CV.
"""
from __future__ import annotations

from typing import Dict, Any, List


# ── 1. Versions régionales de CV ──────────────────────────────────────────────
COUNTRY_VERSIONS = {
    "fr": {
        "id": "fr",
        "name": "Côte d'Ivoire & Francophonie (CV Standard)",
        "flag": "🇫🇷",
        "desc": "Photo recommandée, état civil complet (âge/date de naissance, permis B), 1 à 2 pages bien structurées.",
        "defaults": {"show_photo": True, "show_civil_status": True, "show_signoff": False}
    },
    "en": {
        "id": "en",
        "name": "Anglophone (US Resume / UK & International CV)",
        "flag": "🇬🇧",
        "desc": "Strictement sans photo ni données personnelles (anti-discrimination lois US/UK). Focus sur le résumé et les résultats.",
        "defaults": {"show_photo": False, "show_civil_status": False, "show_signoff": False}
    },
    "de": {
        "id": "de",
        "name": "Germanophone (DACH : Deutschland, Österreich, Schweiz)",
        "flag": "🇩🇪",
        "desc": "Tabellarischer Lebenslauf : Bewerbungsfoto, Persönliche Angaben (lieu de naissance, nationalité), et clôture 'Ort, Datum, Unterschrift'.",
        "defaults": {"show_photo": True, "show_civil_status": True, "show_signoff": True}
    }
}


# ── 2. Langues de rédaction du CV ────────────────────────────────────────────
CV_LANGUAGES = {
    "fr": {"id": "fr", "name": "Français", "flag": "🇫🇷"},
    "en": {"id": "en", "name": "English", "flag": "🇬🇧"},
    "de": {"id": "de", "name": "Deutsch", "flag": "🇩🇪"}
}


# ── 3. Styles visuels de CV ──────────────────────────────────────────────────
CV_STYLES = {
    "modern_minimalist": {
        "id": "modern_minimalist",
        "name": "Moderne Minimaliste",
        "desc": "Typographie soignée, en-tête sobre, mise en page aérée et élégante adaptée à tous les secteurs.",
        "has_sidebar": False,
        "default_color": "#1e3a8a"
    },
    "creative_sidebar": {
        "id": "creative_sidebar",
        "name": "Colonne Latérale Graphique",
        "desc": "Deux colonnes avec bandeau coloré à gauche (photo, contact, compétences, langues) et parcours à droite.",
        "has_sidebar": True,
        "default_color": "#047857"
    },
    "executive_classic": {
        "id": "executive_classic",
        "name": "Exécutif & Classique Corporate",
        "desc": "Structure institutionnelle, filets fins, équilibre parfait, idéal cadres, ingénieurs et juristes.",
        "has_sidebar": False,
        "default_color": "#334155"
    },
    "german_tabular": {
        "id": "german_tabular",
        "name": "Tabellarischer Lebenslauf (Standard DACH)",
        "desc": "Format officiel allemand en tableau strict avec dates à gauche, mentions complètes et signature finale.",
        "has_sidebar": False,
        "default_color": "#1e293b"
    },
    "tech_compact": {
        "id": "tech_compact",
        "name": "Tech & Développeur Compact",
        "desc": "Focalisé sur la densité d'informations, tags de compétences, projets et certifications techniques.",
        "has_sidebar": True,
        "default_color": "#2563eb"
    },
    "academic_europass": {
        "id": "academic_europass",
        "name": "Académique & Europass",
        "desc": "Format normé européen pour chercheurs, enseignants et profils internationaux multilingues.",
        "has_sidebar": False,
        "default_color": "#0f766e"
    }
}


# ── 4. Palettes de Couleurs Recommandées ──────────────────────────────────────
COLOR_PALETTES = [
    {"name": "Bleu Nuit (Corporate)", "hex": "#1e3a8a"},
    {"name": "Émeraude Moderne", "hex": "#047857"},
    {"name": "Bordeaux / Grenat", "hex": "#831843"},
    {"name": "Bleu Royal Tech", "hex": "#2563eb"},
    {"name": "Ardoise / Slate", "hex": "#334155"},
    {"name": "Vert Forêt Institutionnel", "hex": "#15803d"},
    {"name": "Anthracite / Charcoal", "hex": "#1e293b"},
    {"name": "Sarcelle / Teal", "hex": "#0f766e"},
    {"name": "Prune Sombre", "hex": "#581c87"},
]


# ── 5. Titres de sections traduits ───────────────────────────────────────────
SECTION_TITLES = {
    "fr": {
        "profile": "Profil Professionnel",
        "experience": "Expérience Professionnelle",
        "education": "Formation & Diplômes",
        "certifications": "Certifications & Formations",
        "skills": "Compétences Clés",
        "languages": "Langues",
        "hobbies": "Centres d'Intérêt",
        "contact": "Coordonnées",
        "personal_info": "État Civil",
        "date_of_birth": "Date de naissance :",
        "place_of_birth": "Lieu de naissance :",
        "nationality": "Nationalité :",
        "driving_license": "Permis de conduire :",
        "marital_status": "Situation de famille :",
        "present": "Présent",
        "signoff_place_date": "Fait à {place}, le {date}",
        "signature_label": "Signature"
    },
    "en": {
        "profile": "Professional Summary",
        "experience": "Work Experience",
        "education": "Education & Qualifications",
        "certifications": "Certifications & Training",
        "skills": "Core Skills & Expertise",
        "languages": "Languages",
        "hobbies": "Interests & Hobbies",
        "contact": "Contact Information",
        "personal_info": "Personal Details",
        "date_of_birth": "Date of Birth:",
        "place_of_birth": "Place of Birth:",
        "nationality": "Nationality:",
        "driving_license": "Driving Licence:",
        "marital_status": "Marital Status:",
        "present": "Present",
        "signoff_place_date": "{place}, {date}",
        "signature_label": "Signature"
    },
    "de": {
        "profile": "Kurzprofil & Motivation",
        "experience": "Beruflicher Werdegang",
        "education": "Schul- & Hochschulbildung",
        "certifications": "Weiterbildung & Zertifikate",
        "skills": "Kenntnisse & Fähigkeiten",
        "languages": "Sprachkenntnisse",
        "hobbies": "Interessen & Engagement",
        "contact": "Kontaktdaten",
        "personal_info": "Persönliche Daten",
        "date_of_birth": "Geburtsdatum:",
        "place_of_birth": "Geburtsort:",
        "nationality": "Staatsangehörigkeit:",
        "driving_license": "Führerschein:",
        "marital_status": "Familienstand:",
        "present": "Heute",
        "signoff_place_date": "{place}, den {date}",
        "signature_label": "Unterschrift"
    }
}


# ── 6. Niveaux de langues : CECRL et Descriptifs ─────────────────────────────
CECR_LEVELS = [
    {"code": "A1", "name": "A1 - Débutant / Breakthrough", "desc_fr": "Utilisateur élémentaire (Notions de base)", "desc_en": "Basic user (Breakthrough)", "desc_de": "Elementare Sprachverwendung (Einstieg)", "dots": 1},
    {"code": "A2", "name": "A2 - Élémentaire / Waystage", "desc_fr": "Utilisateur élémentaire (Phrases usuelles)", "desc_en": "Basic user (Waystage)", "desc_de": "Elementare Sprachverwendung (Grundlagen)", "dots": 2},
    {"code": "B1", "name": "B1 - Intermédiaire / Threshold", "desc_fr": "Utilisateur indépendant (Compréhension autonome)", "desc_en": "Independent user (Threshold)", "desc_de": "Selbstständige Sprachverwendung (Mittelstufe)", "dots": 3},
    {"code": "B2", "name": "B2 - Avancé / Vantage", "desc_fr": "Utilisateur indépendant (Communication fluide)", "desc_en": "Independent user (Vantage / Upper intermediate)", "desc_de": "Selbstständige Sprachverwendung (Gute Mittelstufe)", "dots": 4},
    {"code": "C1", "name": "C1 - Autonome / Effective", "desc_fr": "Utilisateur expérimenté (Courant professionnel)", "desc_en": "Proficient user (Effective operational)", "desc_de": "Kompetente Sprachverwendung (Fachkundig)", "dots": 5},
    {"code": "C2", "name": "C2 - Maîtrise / Mastery", "desc_fr": "Utilisateur expérimenté (Bilingue / Maîtrise totale)", "desc_en": "Proficient user (Mastery / Native)", "desc_de": "Kompetente Sprachverwendung (Exzellent / Muttersprache)", "dots": 5},
]

DESCRIPTIVE_LEVELS = {
    "fr": [
        "Langue maternelle",
        "Bilingue",
        "Courant (Professionnel)",
        "Intermédiaire avancé (Très bon niveau)",
        "Intermédiaire (Bon niveau opérationnel)",
        "Élémentaire (Notions professionnelles)",
        "Débutant (Notions de base)"
    ],
    "en": [
        "Native / Bilingual",
        "Full Professional Proficiency",
        "Professional Working Proficiency",
        "Limited Working Proficiency",
        "Elementary Proficiency",
        "Basic / Beginner"
    ],
    "de": [
        "Muttersprache",
        "Verhandlungssicher",
        "Fließend in Wort und Schrift",
        "Sehr gute Kenntnisse",
        "Gute Kenntnisse",
        "Grundkenntnisse"
    ]
}


# ── 7. Modèles Démo Complets et Réalistes (1 clic pour tester) ───────────────

DEMO_PROFILES: Dict[str, Dict[str, Any]] = {
    "fr": {
        "general": {
            "first_name": "Osiris",
            "last_name": "XXXXXXX-01",
            "target_title": "Chef de Projet Informatique & Développeur Senior",
            "summary": "Bâtisseur et architecte de systèmes modulaires inspiré par le principe de régénération d'Osiris. Expert en conception logicielle pérenne, éco-conception et modularité matérielle. Spécialiste des architectures résilientes, réparables et autonomes (offline-first).",
            "photo_path": "",
            "email": "osiris.xxxxxxx@mail.ci",
            "phone": "+225 07 XXXXXXXX",
            "address": "7 Voie Solaire, Lot XXXXXXX",
            "city": "Bouaké",
            "postal_code": "01 BP XXXXXXX Bouaké",
            "country": "Côte d'Ivoire",
            "linkedin": "linkedin.com/in/osiris-xxxxxxx",
            "github": "github.com/OsirisAI-dev",
            "portfolio_url": "osiris-lab.xxxxxxx.io",
            "date_of_birth": "18/06/1993",
            "place_of_birth": "Bouaké / Côte d'Ivoire",
            "nationality": "Ivoirienne",
            "driving_license": "Permis B (Véhicule personnel)",
            "marital_status": ""
        },
        "experiences": [
            {
                "id": "exp_1",
                "job_title": "Chef de Projet Technique & Lead Developer",
                "company": "Centre d'Ingénierie & Systèmes Numériques (CISN)",
                "location": "Bouaké, Côte d'Ivoire",
                "start_date": "09/2021",
                "end_date": "Présent",
                "is_current": True,
                "description": "Direction technique d'une squad de 8 développeurs pour la refonte du portail bancaire client.",
                "achievements": [
                    "Migration de l'architecture monolithique vers des microservices Docker/Kubernetes (-45% de temps de déploiement).",
                    "Optimisation des performances API réduisant la latence moyenne de 320ms à 85ms.",
                    "Instauration de revues de code systématiques et hausse de la couverture de tests automatisés à 88%."
                ]
            },
            {
                "id": "exp_2",
                "job_title": "Ingénieur d'Études & Développement Python",
                "company": "Afrika Tech Solutions",
                "location": "Katiola, Côte d'Ivoire",
                "start_date": "01/2018",
                "end_date": "08/2021",
                "is_current": False,
                "description": "Conception et développement d'applications métiers pour le secteur de l'énergie.",
                "achievements": [
                    "Développement d'un pipeline ETL automatisé traitant 2M+ de relevés de compteurs par jour.",
                    "Création d'interfaces web réactives avec CustomTkinter et React pour les superviseurs terrain.",
                    "Rédaction de la documentation technique et formation de 12 nouveaux collaborateurs."
                ]
            }
        ],
        "education": [
            {
                "id": "edu_1",
                "degree": "Diplôme d'Ingénieur en Informatique (Bac+5)",
                "institution": "Université Alassane Ouattara (Bouaké)",
                "location": "Bouaké, Côte d'Ivoire",
                "start_date": "2015",
                "end_date": "2018",
                "field_of_study": "Génie Informatique & Systèmes d'Information",
                "honors": "Mention Très Bien",
                "details": "Major de promotion en architecture logicielle. Projet de fin d'études en intelligence artificielle."
            },
            {
                "id": "edu_2",
                "degree": "Classes Préparatoires aux Grandes Écoles (MPSI / MP)",
                "institution": "Lycée Scientifique & Technique de Bouaké",
                "location": "Katiola, Côte d'Ivoire",
                "start_date": "2013",
                "end_date": "2015",
                "field_of_study": "Mathématiques et Physique",
                "honors": "Admis sur concours",
                "details": "Formation intensive en sciences fondamentales et algorithmique."
            }
        ],
        "certifications": [
            {
                "id": "cert_1",
                "name": "AWS Certified Solutions Architect – Associate",
                "issuing_org": "Amazon Web Services (AWS)",
                "issue_date": "2023",
                "credential_id": "AWS-PSA-89472"
            },
            {
                "id": "cert_2",
                "name": "Professional Scrum Master I (PSM I)",
                "issuing_org": "Scrum.org",
                "issue_date": "2022",
                "credential_id": "PSM-39821"
            }
        ],
        "skills": [
            {"id": "sk_1", "name": "Python (Django, FastAPI, Flask)", "category": "Technique", "level": 5},
            {"id": "sk_2", "name": "Docker & Kubernetes", "category": "Technique", "level": 4},
            {"id": "sk_3", "name": "PostgreSQL & Redis", "category": "Technique", "level": 4},
            {"id": "sk_4", "name": "Gestion de Projet Agile (Scrum)", "category": "Management", "level": 5},
            {"id": "sk_5", "name": "CI/CD (GitLab, GitHub Actions)", "category": "Outils", "level": 4},
            {"id": "sk_6", "name": "Communication & Leadership", "category": "Soft Skills", "level": 5}
        ],
        "languages": [
            {"id": "lang_1", "language": "Français", "eval_mode": "cecr", "cecr_level": "C2", "desc_level": "Langue maternelle", "dots": 5},
            {"id": "lang_2", "language": "Anglais", "eval_mode": "cecr", "cecr_level": "C1", "desc_level": "Courant (Professionnel)", "dots": 5},
            {"id": "lang_3", "language": "Allemand", "eval_mode": "cecr", "cecr_level": "B2", "desc_level": "Intermédiaire avancé", "dots": 4}
        ],
        "hobbies": [
            {"id": "hob_1", "name": "Course à pied", "details": "Marathon & Athlétisme Régional (Bouaké)"},
            {"id": "hob_2", "name": "Échecs", "details": "Classement Elo 1850, compétition en club"},
            {"id": "hob_3", "name": "Open Source", "details": "Contributeur régulier sur des outils de productivité Python"}
        ],
        "signoff": {
            "enabled": False,
            "place": "Bouaké",
            "date_str": "27 octobre 2026",
            "signature_name": "Osiris XXXXXXX",
            "signature_image_path": ""
        },
        "config": {
            "country_version": "fr",
            "cv_language": "fr",
            "style_id": "modern_minimalist",
            "primary_color": "#1e3a8a",
            "secondary_color": "#0284c7",
            "show_photo": True,
            "show_civil_status": True,
            "show_signoff": False
        }
    },

    "en": {
        "general": {
            "first_name": "Ausar",
            "last_name": "XXXXXXX-02",
            "target_title": "Senior Software Architect & Engineering Manager",
            "summary": "Visionary Systems Architect and Hardware-Software craftsman inspired by the Ausar/Osiris modularity paradigm. 8+ years designing decoupled, high-resilience computing architectures and educational open-source toolkits. Dedicated to durable, repairable software ecosystems.",
            "photo_path": "",
            "email": "ausar.core.xxxxxxx@domain.org",
            "phone": "+44 20 XXXXXXX",
            "address": "Abydos Enclosure, Suite XXXXXXX",
            "city": "London",
            "postal_code": "W1U 7DF",
            "country": "United Kingdom",
            "linkedin": "linkedin.com/in/ausar-xxxxxxx",
            "github": "github.com/OsirisAI-dev",
            "portfolio_url": "ausar-systems.xxxxxxx.io",
            "date_of_birth": "",
            "place_of_birth": "",
            "nationality": "",
            "driving_license": "",
            "marital_status": ""
        },
        "experiences": [
            {
                "id": "exp_1",
                "job_title": "Staff Cloud Architect",
                "company": "FinTech Global UK",
                "location": "London, UK",
                "start_date": "10/2020",
                "end_date": "Present",
                "is_current": True,
                "description": "Leading cloud modernization strategy across 4 product teams supporting £1.2B annual transactional volume.",
                "achievements": [
                    "Architected serverless payment gateway on AWS processing 12,000 requests/sec with sub-50ms latency.",
                    "Reduced monthly AWS infrastructure expenditure by 34% through automated spot instance orchestrations.",
                    "Spearheaded SOC2 Type II and ISO 27001 technical compliance accreditations with zero non-conformities."
                ]
            },
            {
                "id": "exp_2",
                "job_title": "Senior Backend Engineer",
                "company": "Deliveroo",
                "location": "London, UK",
                "start_date": "03/2017",
                "end_date": "09/2020",
                "is_current": False,
                "description": "Core logistics and driver dispatch algorithm optimization team member.",
                "achievements": [
                    "Refactored routing matching microservice in Python/Go, improving rider dispatch efficiency by 18%.",
                    "Implemented distributed tracing with OpenTelemetry, cutting mean time to resolution (MTTR) by 50%."
                ]
            }
        ],
        "education": [
            {
                "id": "edu_1",
                "degree": "M.Sc. Advanced Computer Science",
                "institution": "Imperial College London",
                "location": "London, UK",
                "start_date": "2015",
                "end_date": "2016",
                "field_of_study": "Distributed Systems & Machine Learning",
                "honors": "Distinction (First Class Honours)",
                "details": "Dissertation published in IEEE Transactions on Cloud Computing."
            },
            {
                "id": "edu_2",
                "degree": "B.Sc. (Hons) Computer Systems",
                "institution": "University of Manchester",
                "location": "Manchester, UK",
                "start_date": "2012",
                "end_date": "2015",
                "field_of_study": "Software Engineering & Computer Systems",
                "honors": "First Class Honours",
                "details": "Recipient of the British Computer Society Excellence Award."
            }
        ],
        "certifications": [
            {
                "id": "cert_1",
                "name": "AWS Certified Solutions Architect – Professional",
                "issuing_org": "Amazon Web Services",
                "issue_date": "2024",
                "credential_id": "AWS-SAP-78910"
            },
            {
                "id": "cert_2",
                "name": "Certified Kubernetes Administrator (CKA)",
                "issuing_org": "The Linux Foundation & CNCF",
                "issue_date": "2023",
                "credential_id": "CKA-29402"
            }
        ],
        "skills": [
            {"id": "sk_1", "name": "System Architecture & High Concurrency", "category": "Technical", "level": 5},
            {"id": "sk_2", "name": "Python, Go, TypeScript", "category": "Technical", "level": 5},
            {"id": "sk_3", "name": "AWS Cloud & Terraform", "category": "Cloud/DevOps", "level": 5},
            {"id": "sk_4", "name": "Kubernetes & Microservices", "category": "Cloud/DevOps", "level": 4},
            {"id": "sk_5", "name": "Technical Roadmapping & Mentorship", "category": "Leadership", "level": 5}
        ],
        "languages": [
            {"id": "lang_1", "language": "English", "eval_mode": "descriptive", "cecr_level": "C2", "desc_level": "Native / Bilingual", "dots": 5},
            {"id": "lang_2", "language": "German", "eval_mode": "cecr", "cecr_level": "C1", "desc_level": "Professional Working Proficiency", "dots": 5},
            {"id": "lang_3", "language": "French", "eval_mode": "cecr", "cecr_level": "B2", "desc_level": "Limited Working Proficiency", "dots": 4}
        ],
        "hobbies": [
            {"id": "hob_1", "name": "Mountain Hiking", "details": "Summited Mont Blanc and Kilimanjaro"},
            {"id": "hob_2", "name": "Technical Blogging", "details": "Author of cloud architecture tutorials with 40k+ monthly reads"}
        ],
        "signoff": {
            "enabled": False,
            "place": "London",
            "date_str": "October 27, 2026",
            "signature_name": "Ausar XXXXXXX",
            "signature_image_path": ""
        },
        "config": {
            "country_version": "en",
            "cv_language": "en",
            "style_id": "executive_classic",
            "primary_color": "#334155",
            "secondary_color": "#0284c7",
            "show_photo": False,
            "show_civil_status": False,
            "show_signoff": False
        }
    },

    "de": {
        "general": {
            "first_name": "Osiris",
            "last_name": "XXXXXXX-03",
            "target_title": "Diplom-Wirtschaftsingenieur & Senior IT-Projektleiter",
            "summary": "Innovationsorientierter Chefarchitekt und Systementwickler, geprägt von der Idee der modularen Regeneration (Projekt Osiris). Langjährige Erfahrung in langlebigen Baukastensystemen, Entkopplung von Softwaremodulen und ressourceneffizienter IT.",
            "photo_path": "",
            "email": "osiris.dach.xxxxxxx@domain.de",
            "phone": "+49 30 XXXXXXX",
            "address": "Abydos-Promenade XXXXXXX",
            "city": "Berlin",
            "postal_code": "10435",
            "country": "Deutschland",
            "linkedin": "linkedin.com/in/osiris-dach-xxxxxxx",
            "github": "github.com/OsirisAI-dev",
            "portfolio_url": "osiris-tech.xxxxxxx.de",
            "date_of_birth": "14. Mai 1991",
            "place_of_birth": "Heidelberg",
            "nationality": "Deutsch",
            "driving_license": "Führerschein Klasse B & BE",
            "marital_status": "Verheiratet"
        },
        "experiences": [
            {
                "id": "exp_1",
                "job_title": "Leiter Digitale Transformation & IT-Systeme",
                "company": "Siemens AG – Digital Industries",
                "location": "Berlin, Deutschland",
                "start_date": "04/2020",
                "end_date": "Heute",
                "is_current": True,
                "description": "Gesamtverantwortung für das ERP-Modernisierungsprojekt (SAP S/4HANA Migration) für 3 Fertigungsstandorte mit 1.400 Anwendern.",
                "achievements": [
                    "Termin- und budgetgerechter Rollout der Cloud-ERP-Lösung mit einer Kostenersparnis von 14% gegenüber Plan.",
                    "Reduktion der Durchlaufzeiten in der Materialwirtschaft um 28% durch automatisierte Prozess-Workflows.",
                    "Führung eines interdisziplinären Projektteams aus 15 internen Entwicklern und externen Beratern."
                ]
            },
            {
                "id": "exp_2",
                "job_title": "Senior IT-Consultant & Prozessanalytiker",
                "company": "Bosch Rexroth AG",
                "location": "Stuttgart, Deutschland",
                "start_date": "10/2016",
                "end_date": "03/2020",
                "is_current": False,
                "description": "Analyse und Neugestaltung industrieller Produktions- und Logistikprozesse.",
                "achievements": [
                    "Einführung eines prädiktiven Wartungssystems (Predictive Maintenance) auf Python-Basis (IoT-Sensordaten).",
                    "Schulung von über 120 Mitarbeitern und Konzeption mehrsprachiger Betriebshandbücher."
                ]
            }
        ],
        "education": [
            {
                "id": "edu_1",
                "degree": "Master of Science (M.Sc.) Wirtschaftsingenieurwesen",
                "institution": "Karlsruher Institut für Technologie (KIT)",
                "location": "Karlsruhe, Deutschland",
                "start_date": "10/2014",
                "end_date": "09/2016",
                "field_of_study": "Schwerpunkt : Informationsmanagement & Produktionstechnik",
                "honors": "Gesamtnote : 1,2 (Mit Auszeichnung)",
                "details": "Masterarbeit über KI-gestützte Kapazitätsplanung in Kooperation mit Daimler AG."
            },
            {
                "id": "edu_2",
                "degree": "Bachelor of Science (B.Sc.) Wirtschaftsingenieurwesen",
                "institution": "Universität Heidelberg",
                "location": "Heidelberg, Deutschland",
                "start_date": "10/2011",
                "end_date": "09/2014",
                "field_of_study": "Betriebswirtschaftslehre & Informatik",
                "honors": "Gesamtnote : 1,4",
                "details": "Auslandssemester an der École Polytechnique Fédérale de Lausanne (EPFL), Schweiz."
            }
        ],
        "certifications": [
            {
                "id": "cert_1",
                "name": "Prince2 Practitioner – Projektmanagement",
                "issuing_org": "AXELOS Global Best Practice",
                "issue_date": "2023",
                "credential_id": "PR2-84920"
            },
            {
                "id": "cert_2",
                "name": "SAP Certified Application Associate – SAP S/4HANA",
                "issuing_org": "SAP SE",
                "issue_date": "2021",
                "credential_id": "SAP-S4H-1039"
            }
        ],
        "skills": [
            {"id": "sk_1", "name": "SAP S/4HANA & ERP-Architektur", "category": "Fachkenntnisse", "level": 5},
            {"id": "sk_2", "name": "Python & Datenanalyse (Pandas, NumPy)", "category": "IT & Programmierung", "level": 4},
            {"id": "sk_3", "name": "Agiles Projektmanagement (Scrum, Kanban)", "category": "Methoden", "level": 5},
            {"id": "sk_4", "name": "Prozessoptimierung (Six Sigma Green Belt)", "category": "Methoden", "level": 4},
            {"id": "sk_5", "name": "Budgetverantwortung & Stakeholder-Management", "category": "Führung", "level": 5}
        ],
        "languages": [
            {"id": "lang_1", "language": "Deutsch", "eval_mode": "cecr", "cecr_level": "C2", "desc_level": "Muttersprache", "dots": 5},
            {"id": "lang_2", "language": "Englisch", "eval_mode": "cecr", "cecr_level": "C1", "desc_level": "Verhandlungssicher in Wort und Schrift", "dots": 5},
            {"id": "lang_3", "language": "Französisch", "eval_mode": "cecr", "cecr_level": "B2", "desc_level": "Fließend (Auslandssemester)", "dots": 4}
        ],
        "hobbies": [
            {"id": "hob_1", "name": "Segeln & Wassersport", "details": "Inhaber Sportbootführerschein Binnen & See"},
            {"id": "hob_2", "name": "Ehrenamtliche Nachhilfe", "details": "Mathematikförderung für Jugendliche beim DRK Berlin"}
        ],
        "signoff": {
            "enabled": True,
            "place": "Berlin",
            "date_str": "27. Oktober 2026",
            "signature_name": "Osiris XXXXXXX",
            "signature_image_path": ""
        },
        "config": {
            "country_version": "de",
            "cv_language": "de",
            "style_id": "german_tabular",
            "primary_color": "#1e293b",
            "secondary_color": "#0284c7",
            "show_photo": True,
            "show_civil_status": True,
            "show_signoff": True
        }
    }
}
