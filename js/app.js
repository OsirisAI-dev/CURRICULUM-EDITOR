/**
 * ÉDITEUR PROFESSIONNEL DE CURRICULUM VITAE — APPLICATION JAVASCRIPT
 * Version autonome et ultra-légère pour navigateurs web et Android WebView
 */

// ── État Initial : 100% Vierge par Défaut ──
const defaultBlankState = {
  is_demo: false,
  general: {
    first_name: "",
    last_name: "",
    target_title: "",
    summary: "",
    photo_path: "",
    photo_b64: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    postal_code: "",
    country: "",
    linkedin: "",
    github: "",
    portfolio_url: "",
    date_of_birth: "",
    place_of_birth: "",
    nationality: "",
    driving_license: "",
    marital_status: ""
  },
  experiences: [],
  education: [],
  certifications: [],
  skills: [],
  languages: [],
  hobbies: [],
  signoff: {
    enabled: false,
    place: "",
    date_str: "",
    signature_name: ""
  },
  config: {
    country_version: "fr",
    cv_language: "fr",
    style_id: "modern_minimalist",
    primary_color: "#1e3a8a",
    secondary_color: "#0284c7",
    show_photo: true,
    show_civil_status: true,
    show_signoff: false
  }
};

let cvState = JSON.parse(JSON.stringify(defaultBlankState));

// ── Profils Démo Réalistes (FR, EN, DE) pour Révision Immédiate ──
const DEMO_PROFILES = {
  fr: {
    is_demo: true,
    general: {
      first_name: "Osiris",
      last_name: "XXXXXXX-01",
      target_title: "Architecte Logiciel & Ingénierie des Systèmes (Projet Osiris)",
      summary: "Bâtisseur et architecte de systèmes modulaires inspiré par le principe de régénération d'Osiris. Expert en conception logicielle pérenne, éco-conception et modularité matérielle. Spécialiste des architectures résilientes, réparables et autonomes (offline-first).",
      photo_path: "",
      photo_b64: "",
      email: "osiris.xxxxxxx@mail.ci",
      phone: "+225 07 XXXXXXXX",
      address: "Boulevard de la Paix, Lot XXXXXXX",
      city: "Bouaké",
      postal_code: "01 BP XXXXXXX Bouaké",
      country: "Côte d'Ivoire",
      linkedin: "linkedin.com/in/osiris-xxxxxxx",
      github: "github.com/OsirisAI-dev",
      portfolio_url: "osiris-lab.xxxxxxx.ci",
      date_of_birth: "18/06/1993",
      place_of_birth: "Bouaké / Côte d'Ivoire",
      nationality: "Ivoirienne",
      driving_license: "Permis B (Véhicule personnel)",
      marital_status: ""
    },
    experiences: [
      {
        job_title: "Chef de Projet Technique & Lead Developer",
        company: "Centre d'Ingénierie & Systèmes Numériques (CISN)",
        location: "Bouaké, Côte d'Ivoire",
        start_date: "09/2021",
        end_date: "Présent",
        is_current: true,
        description: "Direction technique d'une squad de 8 développeurs pour la refonte du portail bancaire client.",
        achievements: [
          "Migration de l'architecture monolithique vers des microservices Docker/Kubernetes (-45% de temps de déploiement).",
          "Optimisation des performances API réduisant la latence moyenne de 320ms à 85ms.",
          "Instauration de revues de code systématiques et hausse de la couverture de tests automatisés à 88%."
        ]
      },
      {
        job_title: "Ingénieur d'Études & Développement Python",
        company: "Afrika Tech Solutions",
        location: "Katiola, Côte d'Ivoire",
        start_date: "01/2018",
        end_date: "08/2021",
        is_current: false,
        description: "Conception et développement d'applications métiers pour le secteur de l'énergie.",
        achievements: [
          "Développement d'un pipeline ETL automatisé traitant 2M+ de relevés de compteurs par jour.",
          "Création d'interfaces web réactives pour les superviseurs terrain.",
          "Rédaction de la documentation technique et formation de 12 nouveaux collaborateurs."
        ]
      }
    ],
    education: [
      {
        degree: "Diplôme d'Ingénieur en Informatique (Bac+5)",
        institution: "Université Alassane Ouattara (Bouaké)",
        location: "Bouaké, Côte d'Ivoire",
        start_date: "2015",
        end_date: "2018",
        field_of_study: "Génie Informatique & Systèmes d'Information",
        honors: "Mention Très Bien",
        details: "Major de promotion en architecture logicielle. Projet de fin d'études en intelligence artificielle."
      },
      {
        degree: "Classes Préparatoires aux Grandes Écoles (MPSI / MP)",
        institution: "Lycée Scientifique & Technique de Bouaké",
        location: "Katiola, Côte d'Ivoire",
        start_date: "2013",
        end_date: "2015",
        field_of_study: "Mathématiques et Physique",
        honors: "Admis sur concours",
        details: "Formation intensive en sciences fondamentales et algorithmique."
      }
    ],
    certifications: [
      {
        name: "AWS Certified Solutions Architect – Associate",
        issuing_org: "Amazon Web Services (AWS)",
        issue_date: "2023",
        credential_id: "AWS-PSA-89472"
      },
      {
        name: "Professional Scrum Master I (PSM I)",
        issuing_org: "Scrum.org",
        issue_date: "2022",
        credential_id: "PSM-39821"
      }
    ],
    skills: [
      { name: "Python (Django, FastAPI, Flask)", category: "Technique", level: 5 },
      { name: "Docker & Kubernetes", category: "Technique", level: 4 },
      { name: "PostgreSQL & Redis", category: "Technique", level: 4 },
      { name: "Gestion de Projet Agile (Scrum)", category: "Management", level: 5 },
      { name: "CI/CD (GitLab, GitHub Actions)", category: "Outils", level: 4 },
      { name: "Leadership & Esprit d'équipe", category: "Soft Skills", level: 5 }
    ],
    languages: [
      { language: "Français", eval_mode: "cecr", cecr_level: "C2", desc_level: "Langue maternelle", dots: 5 },
      { language: "Anglais", eval_mode: "cecr", cecr_level: "C1", desc_level: "Courant (Professionnel)", dots: 5 },
      { language: "Allemand", eval_mode: "cecr", cecr_level: "B2", desc_level: "Intermédiaire avancé", dots: 4 }
    ],
    hobbies: [
      { name: "Course à pied", details: "Marathon & Athlétisme Régional (Bouaké)" },
      { name: "Échecs", details: "Compétition en club, classement 1850 Elo" },
      { name: "Open Source", details: "Contributeur régulier sur outils Python" }
    ],
    signoff: {
      enabled: false,
      place: "Bouaké",
      date_str: "27 octobre 2026",
      signature_name: "Osiris XXXXXXX"
    },
    config: {
      country_version: "fr",
      cv_language: "fr",
      style_id: "modern_minimalist",
      primary_color: "#1e3a8a",
      secondary_color: "#0284c7",
      show_photo: true,
      show_civil_status: true,
      show_signoff: false
    }
  },

  en: {
    is_demo: true,
    general: {
      first_name: "Ausar",
      last_name: "XXXXXXX-02",
      target_title: "Principal Systems Architect & Hardware Lead (Osiris Core)",
      summary: "Visionary Systems Architect and Hardware-Software craftsman inspired by the Ausar/Osiris modularity paradigm. 8+ years designing decoupled, high-resilience computing architectures and educational open-source toolkits. Dedicated to durable, repairable software ecosystems.",
      photo_path: "",
      photo_b64: "",
      email: "ausar.core.xxxxxxx@domain.org",
      phone: "+44 20 XXXXXXX",
      address: "Abydos Enclosure, Suite XXXXXXX",
      city: "London",
      postal_code: "W1U-XXXXXXX",
      country: "United Kingdom",
      linkedin: "linkedin.com/in/ausar-xxxxxxx",
      github: "github.com/OsirisAI-dev",
      portfolio_url: "ausar-systems.xxxxxxx.io",
      date_of_birth: "",
      place_of_birth: "",
      nationality: "",
      driving_license: "",
      marital_status: ""
    },
    experiences: [
      {
        job_title: "Staff Cloud Architect",
        company: "FinTech Global UK",
        location: "London, UK",
        start_date: "10/2020",
        end_date: "Present",
        is_current: true,
        description: "Leading cloud modernization strategy across 4 product teams supporting £1.2B annual transactional volume.",
        achievements: [
          "Architected serverless payment gateway on AWS processing 12,000 requests/sec with sub-50ms latency.",
          "Reduced monthly AWS infrastructure expenditure by 34% through automated spot instance orchestrations.",
          "Spearheaded SOC2 Type II and ISO 27001 technical compliance accreditations with zero non-conformities."
        ]
      },
      {
        job_title: "Senior Backend Engineer",
        company: "Deliveroo",
        location: "London, UK",
        start_date: "03/2017",
        end_date: "09/2020",
        is_current: false,
        description: "Core logistics and driver dispatch algorithm optimization team member.",
        achievements: [
          "Refactored routing matching microservice in Python/Go, improving rider dispatch efficiency by 18%.",
          "Implemented distributed tracing with OpenTelemetry, cutting mean time to resolution (MTTR) by 50%."
        ]
      }
    ],
    education: [
      {
        degree: "M.Sc. Advanced Computer Science",
        institution: "Imperial College London",
        location: "London, UK",
        start_date: "2015",
        end_date: "2016",
        field_of_study: "Distributed Systems & Machine Learning",
        honors: "First Class Honours (Distinction)",
        details: "Dissertation on high-throughput consensus algorithms in edge networks."
      },
      {
        degree: "B.Sc. Computer Science",
        institution: "University of Edinburgh",
        location: "Edinburgh, UK",
        start_date: "2011",
        end_date: "2015",
        field_of_study: "Informatics",
        honors: "Upper Second Class (2:1)",
        details: "Coursework in Algorithms, Operating Systems and Cryptography."
      }
    ],
    certifications: [
      {
        name: "Google Cloud Certified – Professional Cloud Architect",
        issuing_org: "Google Cloud",
        issue_date: "2023",
        credential_id: "GCP-PCA-98214"
      },
      {
        name: "Certified Kubernetes Administrator (CKA)",
        issuing_org: "Cloud Native Computing Foundation (CNCF)",
        issue_date: "2022",
        credential_id: "CKA-77319"
      }
    ],
    skills: [
      { name: "Cloud Architecture (AWS, GCP)", category: "Technique", level: 5 },
      { name: "Python, Go, TypeScript", category: "Technique", level: 5 },
      { name: "Kubernetes & Terraform", category: "Outils", level: 5 },
      { name: "System Design & Microservices", category: "Technique", level: 5 },
      { name: "Engineering Management & Mentoring", category: "Management", level: 5 },
      { name: "Strategic Technical Roadmap", category: "Soft Skills", level: 4 }
    ],
    languages: [
      { language: "English", eval_mode: "descriptive", cecr_level: "C2", desc_level: "Native / Bilingual", dots: 5 },
      { language: "French", eval_mode: "cecr", cecr_level: "B2", desc_level: "Professional Working Proficiency", dots: 4 },
      { language: "German", eval_mode: "cecr", cecr_level: "A2", desc_level: "Elementary Proficiency", dots: 2 }
    ],
    hobbies: [
      { name: "Mountaineering", details: "Summited Mont Blanc (4,809m) and Kilimanjaro" },
      { name: "Open Source", details: "Active contributor to Kubernetes SIG-Node ecosystem" },
      { name: "Triathlon", details: "Completed 2 Half-Ironman races (70.3)" }
    ],
    signoff: {
      enabled: false,
      place: "",
      date_str: "",
      signature_name: ""
    },
    config: {
      country_version: "en",
      cv_language: "en",
      style_id: "executive_classic",
      primary_color: "#334155",
      secondary_color: "#0284c7",
      show_photo: false,
      show_civil_status: false,
      show_signoff: false
    }
  },

  de: {
    is_demo: true,
    general: {
      first_name: "Osiris",
      last_name: "XXXXXXX-03",
      target_title: "Chefarchitekt & Leiter Systemregeneration (Projekt Osiris)",
      summary: "Innovationsorientierter Chefarchitekt und Systementwickler, geprägt von der Idee der modularen Regeneration (Projekt Osiris). Langjährige Erfahrung in langlebigen Baukastensystemen, Entkopplung von Softwaremodulen und ressourceneffizienter IT.",
      photo_path: "",
      photo_b64: "",
      email: "osiris.dach.xxxxxxx@domain.de",
      phone: "+49 30 XXXXXXX",
      address: "Abydos-Promenade XXXXXXX",
      city: "Berlin",
      postal_code: "10000-XXXXXXX",
      country: "Deutschland",
      linkedin: "linkedin.com/in/osiris-dach-xxxxxxx",
      github: "github.com/OsirisAI-dev",
      portfolio_url: "osiris-tech.xxxxxxx.de",
      date_of_birth: "14. Mai 1991",
      place_of_birth: "Heidelberg",
      nationality: "Deutsch",
      driving_license: "Führerschein Klasse B & BE",
      marital_status: "Verheiratet"
    },
    experiences: [
      {
        job_title: "Leiter Digitale Transformation & IT-Systeme",
        company: "Siemens AG – Digital Industries",
        location: "Berlin, Deutschland",
        start_date: "04/2020",
        end_date: "Heute",
        is_current: true,
        description: "Gesamtverantwortung für das ERP-Modernisierungsprojekt (SAP S/4HANA Migration) für 3 Fertigungsstandorte mit 1.400 Anwendern.",
        achievements: [
          "Termin- und budgetgerechter Rollout der Cloud-ERP-Lösung mit einer Kostenersparnis von 14% gegenüber Plan.",
          "Reduktion der Durchlaufzeiten in der Materialwirtschaft um 28% durch automatisierte Prozess-Workflows.",
          "Führung eines interdisziplinären Projektteams aus 15 internen Entwicklern und externen Beratern."
        ]
      },
      {
        job_title: "Senior IT-Consultant & Prozessanalytiker",
        company: "Bosch Rexroth AG",
        location: "Stuttgart, Deutschland",
        start_date: "10/2016",
        end_date: "03/2020",
        is_current: false,
        description: "Analyse und Neugestaltung industrieller Produktions- und Logistikprozesse.",
        achievements: [
          "Einführung eines prädiktiven Wartungssystems auf Python-Basis (IoT-Sensordaten).",
          "Schulung von über 120 Mitarbeitern und Konzeption mehrsprachiger Betriebshandbücher."
        ]
      }
    ],
    education: [
      {
        degree: "Master of Science (M.Sc.) Wirtschaftsingenieurwesen",
        institution: "Karlsruher Institut für Technologie (KIT)",
        location: "Karlsruhe, Deutschland",
        start_date: "10/2014",
        end_date: "09/2016",
        field_of_study: "Informationsmanagement & Produktionstechnik",
        honors: "Gesamtnote : 1,2 (Mit Auszeichnung)",
        details: "Masterarbeit über KI-gestützte Kapazitätsplanung in Kooperation mit Daimler AG."
      },
      {
        degree: "Bachelor of Science (B.Sc.) Wirtschaftsingenieurwesen",
        institution: "Universität Heidelberg",
        location: "Heidelberg, Deutschland",
        start_date: "10/2011",
        end_date: "09/2014",
        field_of_study: "Betriebswirtschaftslehre & Informatik",
        honors: "Gesamtnote : 1,5",
        details: "Auslandssemester an der École Polytechnique Fédérale de Lausanne (EPFL)."
      }
    ],
    certifications: [
      {
        name: "Project Management Professional (PMP)",
        issuing_org: "Project Management Institute (PMI)",
        issue_date: "2021",
        credential_id: "PMP-2910482"
      },
      {
        name: "SAP Certified Application Associate – S/4HANA",
        issuing_org: "SAP SE",
        issue_date: "2020",
        credential_id: "SAP-CERT-4412"
      }
    ],
    skills: [
      { name: "ERP & SAP S/4HANA", category: "Technique", level: 5 },
      { name: "Agiles Projektmanagement (Scrum, Kanban)", category: "Management", level: 5 },
      { name: "Prozessanalyse & Lean Management", category: "Management", level: 5 },
      { name: "Python & SQL Datenanalyse", category: "Technique", level: 4 },
      { name: "Stakeholder Management", category: "Soft Skills", level: 5 },
      { name: "Jira, Confluence, PowerBI", category: "Outils", level: 5 }
    ],
    languages: [
      { language: "Deutsch", eval_mode: "cecr", cecr_level: "C2", desc_level: "Muttersprache", dots: 5 },
      { language: "Englisch", eval_mode: "cecr", cecr_level: "C1", desc_level: "Verhandlungssicher in Wort und Schrift", dots: 5 },
      { language: "Französisch", eval_mode: "cecr", cecr_level: "B2", desc_level: "Gute Kenntnisse", dots: 4 }
    ],
    hobbies: [
      { name: "Alpines Skifahren & Bergsteigen", details: "DAV-Mitglied, Skitouren in den Berner Alpen" },
      { name: "Klassisches Klavier", details: "Repertoire Chopin und Bach" },
      { name: "Fotografie", details: "Architektur- und Landschaftsfotografie" }
    ],
    signoff: {
      enabled: true,
      place: "Berlin",
      date_str: "27. Oktober 2026",
      signature_name: "Osiris XXXXXXX"
    },
    config: {
      country_version: "de",
      cv_language: "de",
      style_id: "german_tabular",
      primary_color: "#1e293b",
      secondary_color: "#0f766e",
      show_photo: true,
      show_civil_status: true,
      show_signoff: true
    }
  }
};

// ── Initialisation au Chargement ──
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initEventListeners();
  bindFormInputs();
  renderAll();
});

// ── Gestion des Onglets ──
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      document.getElementById(targetId).classList.add("active");
      if (targetId === "tab-preview") {
        renderPreview();
      }
    });
  });
}

// ── Événements Globaux de Barre d'Outils ──
function initEventListeners() {
  // Sélecteur Version Pays (FR, EN, DE)
  document.getElementById("selectCountryVersion").addEventListener("change", (e) => {
    cvState.config.country_version = e.target.value;
    if (e.target.value === "en") {
      cvState.config.show_photo = false;
      cvState.config.show_civil_status = false;
      cvState.config.show_signoff = false;
    } else if (e.target.value === "de") {
      cvState.config.show_photo = true;
      cvState.config.show_civil_status = true;
      cvState.config.show_signoff = true;
    }
    renderAll();
  });

  // Sélecteur Langue CV (FR, EN, DE)
  document.getElementById("selectCvLang").addEventListener("change", (e) => {
    cvState.config.cv_language = e.target.value;
    renderPreview();
  });

  // Sélecteur Style Visuel
  document.getElementById("selectStyle").addEventListener("change", (e) => {
    cvState.config.style_id = e.target.value;
    renderPreview();
  });

  // Boutons Démo
  document.getElementById("btnDemoFr").addEventListener("click", () => fillDemoData("fr"));
  document.getElementById("btnDemoEn").addEventListener("click", () => fillDemoData("en"));
  document.getElementById("btnDemoDe").addEventListener("click", () => fillDemoData("de"));

  // Bouton Revert / Vider
  document.getElementById("btnClearAll").addEventListener("click", clearAllFields);

  // Bouton Photo Upload
  const photoInput = document.getElementById("inputPhotoFile");
  if (photoInput) {
    photoInput.addEventListener("change", handlePhotoUpload);
  }

  // Boutons d'ajout de cartes
  document.getElementById("btnAddExp").addEventListener("click", () => addExperienceCard());
  document.getElementById("btnAddEdu").addEventListener("click", () => addEducationCard());
  document.getElementById("btnAddCert").addEventListener("click", () => addCertificationCard());
  document.getElementById("btnAddSkill").addEventListener("click", () => addSkillCard());
  document.getElementById("btnAddLang").addEventListener("click", () => addLanguageCard());
  document.getElementById("btnAddHobby").addEventListener("click", () => addHobbyCard());

  // Checkboxes de configuration
  document.getElementById("cbShowPhoto").addEventListener("change", (e) => {
    cvState.config.show_photo = e.target.checked;
    renderPreview();
  });
  document.getElementById("cbShowCivil").addEventListener("change", (e) => {
    cvState.config.show_civil_status = e.target.checked;
    renderPreview();
  });
  document.getElementById("cbShowSignoff").addEventListener("change", (e) => {
    cvState.config.show_signoff = e.target.checked;
    renderPreview();
  });

  // Actions d'Export
  document.getElementById("btnPrintPdf").addEventListener("click", triggerPrint);
  document.getElementById("btnExportDocx").addEventListener("click", triggerExportDocx);
  document.getElementById("btnSaveJson").addEventListener("click", exportJsonState);
  document.getElementById("fileInputJson").addEventListener("change", importJsonState);
  document.getElementById("btnLoadJson").addEventListener("click", () => {
    document.getElementById("fileInputJson").click();
  });

  // Palette de couleurs
  document.querySelectorAll(".color-swatch").forEach(swatch => {
    swatch.addEventListener("click", () => {
      document.querySelectorAll(".color-swatch").forEach(s => s.classList.remove("active"));
      swatch.classList.add("active");
      const hex = swatch.getAttribute("data-color");
      cvState.config.primary_color = hex;
      renderPreview();
    });
  });
}

// ── Liaison des Champs Saisis avec l'État ──
function bindFormInputs() {
  const fields = [
    { id: "entFirstName", key: "general.first_name" },
    { id: "entLastName", key: "general.last_name" },
    { id: "entTargetTitle", key: "general.target_title" },
    { id: "txtSummary", key: "general.summary" },
    { id: "entEmail", key: "general.email" },
    { id: "entPhone", key: "general.phone" },
    { id: "entAddress", key: "general.address" },
    { id: "entCity", key: "general.city" },
    { id: "entPostalCode", key: "general.postal_code" },
    { id: "entCountry", key: "general.country" },
    { id: "entLinkedin", key: "general.linkedin" },
    { id: "entGithub", key: "general.github" },
    { id: "entPortfolio", key: "general.portfolio_url" },
    { id: "entDob", key: "general.date_of_birth" },
    { id: "entPob", key: "general.place_of_birth" },
    { id: "entNationality", key: "general.nationality" },
    { id: "entDrivingLicense", key: "general.driving_license" },
    { id: "entMaritalStatus", key: "general.marital_status" },
    { id: "entSignPlace", key: "signoff.place" },
    { id: "entSignDate", key: "signoff.date_str" },
    { id: "entSignName", key: "signoff.signature_name" }
  ];

  fields.forEach(f => {
    const el = document.getElementById(f.id);
    if (!el) return;
    el.addEventListener("input", () => {
      const parts = f.key.split(".");
      if (parts.length === 2) {
        cvState[parts[0]][parts[1]] = el.value;
      }
    });
  });
}

// ── Gestion de l'Upload Photo ──
function handlePhotoUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (event) => {
    cvState.general.photo_b64 = event.target.result;
    document.getElementById("imgPhotoPreview").src = event.target.result;
    document.getElementById("imgPhotoPreview").style.display = "block";
    renderPreview();
  };
  reader.readAsDataURL(file);
}

// ── Remplissage des Données Démo (Mock Data) ──
function fillDemoData(lang) {
  const profile = DEMO_PROFILES[lang] || DEMO_PROFILES.fr;
  cvState = JSON.parse(JSON.stringify(profile));
  renderAll();
  const banner = document.getElementById("bannerDemoActive");
  if (banner) banner.style.display = "flex";
}

// ── Vider tous les champs (Formulaire Vierge) ──
function clearAllFields() {
  if (!confirm("Voulez-vous vider entièrement le CV pour démarrer sur un formulaire 100% vierge ?")) return;
  cvState = JSON.parse(JSON.stringify(defaultBlankState));
  renderAll();
  const banner = document.getElementById("bannerDemoActive");
  if (banner) banner.style.display = "none";
}

// ── Rendu Complet de l'IHM et des Cartes ──
function renderAll() {
  // Sync Top Selectors
  document.getElementById("selectCountryVersion").value = cvState.config.country_version || "fr";
  document.getElementById("selectCvLang").value = cvState.config.cv_language || "fr";
  document.getElementById("selectStyle").value = cvState.config.style_id || "modern_minimalist";

  // Sync Checkboxes
  document.getElementById("cbShowPhoto").checked = !!cvState.config.show_photo;
  document.getElementById("cbShowCivil").checked = !!cvState.config.show_civil_status;
  document.getElementById("cbShowSignoff").checked = !!cvState.config.show_signoff;

  // Sync General Inputs
  const gen = cvState.general || {};
  document.getElementById("entFirstName").value = gen.first_name || "";
  document.getElementById("entLastName").value = gen.last_name || "";
  document.getElementById("entTargetTitle").value = gen.target_title || "";
  document.getElementById("txtSummary").value = gen.summary || "";
  document.getElementById("entEmail").value = gen.email || "";
  document.getElementById("entPhone").value = gen.phone || "";
  document.getElementById("entAddress").value = gen.address || "";
  document.getElementById("entCity").value = gen.city || "";
  document.getElementById("entPostalCode").value = gen.postal_code || "";
  document.getElementById("entCountry").value = gen.country || "";
  document.getElementById("entLinkedin").value = gen.linkedin || "";
  document.getElementById("entGithub").value = gen.github || "";
  document.getElementById("entPortfolio").value = gen.portfolio_url || "";
  document.getElementById("entDob").value = gen.date_of_birth || "";
  document.getElementById("entPob").value = gen.place_of_birth || "";
  document.getElementById("entNationality").value = gen.nationality || "";
  document.getElementById("entDrivingLicense").value = gen.driving_license || "";
  document.getElementById("entMaritalStatus").value = gen.marital_status || "";

  // Photo
  const imgEl = document.getElementById("imgPhotoPreview");
  if (gen.photo_b64) {
    imgEl.src = gen.photo_b64;
    imgEl.style.display = "block";
  } else {
    imgEl.src = "";
    imgEl.style.display = "none";
  }

  // Signoff
  const sign = cvState.signoff || {};
  document.getElementById("entSignPlace").value = sign.place || "";
  document.getElementById("entSignDate").value = sign.date_str || "";
  document.getElementById("entSignName").value = sign.signature_name || "";

  // Render Sub-cards
  renderExperienceList();
  renderEducationList();
  renderCertificationList();
  renderSkillsList();
  renderLanguagesList();
  renderHobbiesList();

  // Render Live Preview
  renderPreview();
}

// ── Cartes d'Expériences ──
function renderExperienceList() {
  const container = document.getElementById("expListContainer");
  container.innerHTML = "";
  if (!cvState.experiences || cvState.experiences.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:24px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucune expérience ajoutée. Cliquez sur "+ Ajouter une Expérience" ou sur un bouton Démo.</i></div>`;
    return;
  }
  cvState.experiences.forEach((exp, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    const achText = (exp.achievements || []).map(a => `• ${a}`).join("\n");
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">💼 Expérience ${idx + 1}</span>
        <button class="btn btn-danger btn-sm" onclick="removeExperience(${idx})">✕ Supprimer</button>
      </div>
      <div class="grid-3">
        <div class="form-group">
          <label>Intitulé du Poste :</label>
          <input type="text" class="form-control" value="${escapeHtml(exp.job_title)}" placeholder="ex: Lead Developer Python" oninput="updateExpField(${idx}, 'job_title', this.value)">
        </div>
        <div class="form-group">
          <label>Entreprise / Organisation :</label>
          <input type="text" class="form-control" value="${escapeHtml(exp.company)}" placeholder="ex: Centre CISN" oninput="updateExpField(${idx}, 'company', this.value)">
        </div>
        <div class="form-group">
          <label>Lieu :</label>
          <input type="text" class="form-control" value="${escapeHtml(exp.location)}" placeholder="ex: Bouaké, Côte d'Ivoire" oninput="updateExpField(${idx}, 'location', this.value)">
        </div>
      </div>
      <div class="grid-3" style="align-items:center;">
        <div class="form-group">
          <label>Date Début (ex: 2020 ou 09/2020) :</label>
          <input type="text" class="form-control" id="expStart_${idx}" value="${escapeHtml(exp.start_date)}" placeholder="09/2020" oninput="updateExpField(${idx}, 'start_date', this.value)">
        </div>
        <div class="form-group">
          <label>Date Fin (ex: 2026 ou Présent) :</label>
          <input type="text" class="form-control" id="expEnd_${idx}" value="${escapeHtml(exp.end_date)}" placeholder="Présent" oninput="updateExpField(${idx}, 'end_date', this.value)">
        </div>
        <div class="form-group" style="padding-top:16px;">
          <button class="btn-badge-date" type="button" onclick="setExpPeriod(${idx}, '2020', '2026')">+ Période 2020 - 2026</button>
          <label style="margin-left:8px; display:inline-flex; align-items:center; gap:4px; font-size:12px; cursor:pointer;">
            <input type="checkbox" ${exp.is_current ? 'checked' : ''} onchange="updateExpField(${idx}, 'is_current', this.checked)"> Poste actuel
          </label>
        </div>
      </div>
      <div class="form-group">
        <label>Description du rôle :</label>
        <textarea class="form-control" style="min-height:50px;" placeholder="Responsabilités principales..." oninput="updateExpField(${idx}, 'description', this.value)">${escapeHtml(exp.description || '')}</textarea>
      </div>
      <div class="form-group">
        <label>Réalisations clés & Résultats chiffrés (1 par ligne) :</label>
        <textarea class="form-control" style="min-height:60px;" placeholder="• Réduction de 45% du temps de build&#10;• Management de 8 ingénieurs" oninput="updateExpAchievements(${idx}, this.value)">${escapeHtml(achText)}</textarea>
      </div>
    `;
    container.appendChild(card);
  });
}

function addExperienceCard() {
  cvState.experiences.push({
    job_title: "",
    company: "",
    location: "",
    start_date: "",
    end_date: "",
    is_current: false,
    description: "",
    achievements: []
  });
  renderExperienceList();
  renderPreview();
}

function removeExperience(idx) {
  cvState.experiences.splice(idx, 1);
  renderExperienceList();
  renderPreview();
}

function updateExpField(idx, field, val) {
  cvState.experiences[idx][field] = val;
  renderPreview();
}

function updateExpAchievements(idx, text) {
  cvState.experiences[idx].achievements = text.split("\n").map(l => l.replace(/^•\s*/, '').trim()).filter(Boolean);
  renderPreview();
}

function setExpPeriod(idx, startVal, endVal) {
  cvState.experiences[idx].start_date = startVal;
  cvState.experiences[idx].end_date = endVal;
  const s = document.getElementById(`expStart_${idx}`);
  const e = document.getElementById(`expEnd_${idx}`);
  if (s) s.value = startVal;
  if (e) e.value = endVal;
  renderPreview();
}

// ── Cartes d'Études / Diplômes ──
function renderEducationList() {
  const container = document.getElementById("eduListContainer");
  container.innerHTML = "";
  if (!cvState.education || cvState.education.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:24px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucune formation enregistrée. Cliquez sur "+ Ajouter une Formation".</i></div>`;
    return;
  }
  cvState.education.forEach((edu, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">🎓 Formation ${idx + 1}</span>
        <button class="btn btn-danger btn-sm" onclick="removeEducation(${idx})">✕ Supprimer</button>
      </div>
      <div class="grid-3">
        <div class="form-group">
          <label>Diplôme / Titre :</label>
          <input type="text" class="form-control" value="${escapeHtml(edu.degree)}" placeholder="ex: Master en Informatique" oninput="updateEduField(${idx}, 'degree', this.value)">
        </div>
        <div class="form-group">
          <label>Établissement / Université :</label>
          <input type="text" class="form-control" value="${escapeHtml(edu.institution)}" placeholder="ex: Université de Bouaké" oninput="updateEduField(${idx}, 'institution', this.value)">
        </div>
        <div class="form-group">
          <label>Lieu :</label>
          <input type="text" class="form-control" value="${escapeHtml(edu.location)}" placeholder="ex: Katiola, Côte d'Ivoire" oninput="updateEduField(${idx}, 'location', this.value)">
        </div>
      </div>
      <div class="grid-3" style="align-items:center;">
        <div class="form-group">
          <label>Année Début :</label>
          <input type="text" class="form-control" id="eduStart_${idx}" value="${escapeHtml(edu.start_date)}" placeholder="2020" oninput="updateEduField(${idx}, 'start_date', this.value)">
        </div>
        <div class="form-group">
          <label>Année Fin :</label>
          <input type="text" class="form-control" id="eduEnd_${idx}" value="${escapeHtml(edu.end_date)}" placeholder="2026" oninput="updateEduField(${idx}, 'end_date', this.value)">
        </div>
        <div class="form-group" style="padding-top:16px;">
          <button class="btn-badge-date" type="button" onclick="setEduPeriod(${idx}, '2020', '2026')">+ Période 2020 - 2026</button>
        </div>
      </div>
      <div class="grid-2">
        <div class="form-group">
          <label>Mention / Spécialité :</label>
          <input type="text" class="form-control" value="${escapeHtml(edu.honors)}" placeholder="ex: Mention Très Bien" oninput="updateEduField(${idx}, 'honors', this.value)">
        </div>
        <div class="form-group">
          <label>Détails / Projet de fin d'études :</label>
          <input type="text" class="form-control" value="${escapeHtml(edu.details)}" placeholder="Détails académiques..." oninput="updateEduField(${idx}, 'details', this.value)">
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function addEducationCard() {
  cvState.education.push({
    degree: "",
    institution: "",
    location: "",
    start_date: "",
    end_date: "",
    field_of_study: "",
    honors: "",
    details: ""
  });
  renderEducationList();
  renderPreview();
}

function removeEducation(idx) {
  cvState.education.splice(idx, 1);
  renderEducationList();
  renderPreview();
}

function updateEduField(idx, field, val) {
  cvState.education[idx][field] = val;
  renderPreview();
}

function setEduPeriod(idx, startVal, endVal) {
  cvState.education[idx].start_date = startVal;
  cvState.education[idx].end_date = endVal;
  const s = document.getElementById(`eduStart_${idx}`);
  const e = document.getElementById(`eduEnd_${idx}`);
  if (s) s.value = startVal;
  if (e) e.value = endVal;
  renderPreview();
}

// ── Cartes de Certifications ──
function renderCertificationList() {
  const container = document.getElementById("certListContainer");
  container.innerHTML = "";
  if (!cvState.certifications || cvState.certifications.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:20px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucune certification. Cliquez sur "+ Ajouter une Certification".</i></div>`;
    return;
  }
  cvState.certifications.forEach((c, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div class="item-card-header">
        <span class="item-card-title">📜 Certification ${idx + 1}</span>
        <button class="btn btn-danger btn-sm" onclick="removeCertification(${idx})">✕</button>
      </div>
      <div class="grid-3">
        <div class="form-group">
          <label>Intitulé du Certificat :</label>
          <input type="text" class="form-control" value="${escapeHtml(c.name)}" placeholder="ex: AWS Solutions Architect" oninput="updateCertField(${idx}, 'name', this.value)">
        </div>
        <div class="form-group">
          <label>Organisme Délivereur :</label>
          <input type="text" class="form-control" value="${escapeHtml(c.issuing_org)}" placeholder="ex: Amazon Web Services" oninput="updateCertField(${idx}, 'issuing_org', this.value)">
        </div>
        <div class="form-group">
          <label>Année / Date :</label>
          <input type="text" class="form-control" value="${escapeHtml(c.issue_date)}" placeholder="ex: 2023" oninput="updateCertField(${idx}, 'issue_date', this.value)">
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function addCertificationCard() {
  cvState.certifications.push({ name: "", issuing_org: "", issue_date: "", credential_id: "" });
  renderCertificationList();
  renderPreview();
}

function removeCertification(idx) {
  cvState.certifications.splice(idx, 1);
  renderCertificationList();
  renderPreview();
}

function updateCertField(idx, field, val) {
  cvState.certifications[idx][field] = val;
  renderPreview();
}

// ── Cartes de Compétences ──
function renderSkillsList() {
  const container = document.getElementById("skillsListContainer");
  container.innerHTML = "";
  if (!cvState.skills || cvState.skills.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:20px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucune compétence renseignée. Cliquez sur "+ Ajouter une Compétence".</i></div>`;
    return;
  }
  cvState.skills.forEach((sk, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
        <input type="text" class="form-control" style="width:40%;" value="${escapeHtml(sk.name)}" placeholder="Compétence (ex: Python, Docker...)" oninput="updateSkillField(${idx}, 'name', this.value)">
        <select class="form-control" style="width:30%;" onchange="updateSkillField(${idx}, 'category', this.value)">
          <option value="Technique" ${sk.category === 'Technique' ? 'selected' : ''}>Technique</option>
          <option value="Management" ${sk.category === 'Management' ? 'selected' : ''}>Management</option>
          <option value="Outils" ${sk.category === 'Outils' ? 'selected' : ''}>Outils & DevOps</option>
          <option value="Soft Skills" ${sk.category === 'Soft Skills' ? 'selected' : ''}>Soft Skills</option>
        </select>
        <div style="display:flex; align-items:center; gap:4px; width:20%;">
          <label style="font-size:11px; font-weight:bold;">Niveau:</label>
          <select class="form-control" onchange="updateSkillField(${idx}, 'level', parseInt(this.value))">
            <option value="1" ${sk.level === 1 ? 'selected' : ''}>1/5</option>
            <option value="2" ${sk.level === 2 ? 'selected' : ''}>2/5</option>
            <option value="3" ${sk.level === 3 ? 'selected' : ''}>3/5</option>
            <option value="4" ${sk.level === 4 ? 'selected' : ''}>4/5</option>
            <option value="5" ${sk.level === 5 ? 'selected' : ''}>5/5</option>
          </select>
        </div>
        <button class="btn btn-danger btn-sm" onclick="removeSkill(${idx})">✕</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function addSkillCard() {
  cvState.skills.push({ name: "", category: "Technique", level: 4 });
  renderSkillsList();
  renderPreview();
}

function removeSkill(idx) {
  cvState.skills.splice(idx, 1);
  renderSkillsList();
  renderPreview();
}

function updateSkillField(idx, field, val) {
  cvState.skills[idx][field] = val;
  renderPreview();
}

// ── Cartes de Langues Parlées (CECR / Descriptif / Dots) ──
function renderLanguagesList() {
  const container = document.getElementById("langListContainer");
  container.innerHTML = "";
  if (!cvState.languages || cvState.languages.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:20px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucune langue ajoutée. Cliquez sur "+ Ajouter une Langue".</i></div>`;
    return;
  }
  cvState.languages.forEach((lang, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap;">
        <input type="text" class="form-control" style="width:25%;" value="${escapeHtml(lang.language)}" placeholder="Langue (ex: Anglais, Allemand...)" oninput="updateLangField(${idx}, 'language', this.value)">
        <select class="form-control" style="width:22%;" onchange="updateLangField(${idx}, 'eval_mode', this.value); renderLanguagesList();">
          <option value="cecr" ${lang.eval_mode === 'cecr' ? 'selected' : ''}>Cadre CECR (A1-C2)</option>
          <option value="descriptive" ${lang.eval_mode === 'descriptive' ? 'selected' : ''}>Descriptif textuel</option>
          <option value="dots" ${lang.eval_mode === 'dots' ? 'selected' : ''}>Points visuels (1-5)</option>
        </select>

        ${lang.eval_mode === 'cecr' ? `
          <select class="form-control" style="width:20%;" onchange="updateLangField(${idx}, 'cecr_level', this.value)">
            <option value="A1" ${lang.cecr_level === 'A1' ? 'selected' : ''}>A1 : Débutant</option>
            <option value="A2" ${lang.cecr_level === 'A2' ? 'selected' : ''}>A2 : Élémentaire</option>
            <option value="B1" ${lang.cecr_level === 'B1' ? 'selected' : ''}>B1 : Intermédiaire</option>
            <option value="B2" ${lang.cecr_level === 'B2' ? 'selected' : ''}>B2 : Intermédiaire avancé</option>
            <option value="C1" ${lang.cecr_level === 'C1' ? 'selected' : ''}>C1 : Autonome / Courant</option>
            <option value="C2" ${lang.cecr_level === 'C2' ? 'selected' : ''}>C2 : Maîtrise / Bilingue</option>
          </select>
        ` : (lang.eval_mode === 'descriptive' ? `
          <input type="text" class="form-control" style="width:25%;" value="${escapeHtml(lang.desc_level || '')}" placeholder="ex: Courant / Bilingue" oninput="updateLangField(${idx}, 'desc_level', this.value)">
        ` : `
          <select class="form-control" style="width:18%;" onchange="updateLangField(${idx}, 'dots', parseInt(this.value))">
            <option value="1" ${lang.dots === 1 ? 'selected' : ''}>●○○○○ (1/5)</option>
            <option value="2" ${lang.dots === 2 ? 'selected' : ''}>●●○○○ (2/5)</option>
            <option value="3" ${lang.dots === 3 ? 'selected' : ''}>●●●○○ (3/5)</option>
            <option value="4" ${lang.dots === 4 ? 'selected' : ''}>●●●●○ (4/5)</option>
            <option value="5" ${lang.dots === 5 ? 'selected' : ''}>●●●●● (5/5)</option>
          </select>
        `)}

        <button class="btn btn-danger btn-sm" onclick="removeLanguage(${idx})">✕</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function addLanguageCard() {
  cvState.languages.push({ language: "", eval_mode: "cecr", cecr_level: "B2", desc_level: "Courant", dots: 4 });
  renderLanguagesList();
  renderPreview();
}

function removeLanguage(idx) {
  cvState.languages.splice(idx, 1);
  renderLanguagesList();
  renderPreview();
}

function updateLangField(idx, field, val) {
  cvState.languages[idx][field] = val;
  renderPreview();
}

// ── Cartes de Hobbys ──
function renderHobbiesList() {
  const container = document.getElementById("hobbiesListContainer");
  container.innerHTML = "";
  if (!cvState.hobbies || cvState.hobbies.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:20px; color:#64748b; border:1px dashed #cbd5e1; border-radius:6px;"><i>Aucun centre d'intérêt renseigné.</i></div>`;
    return;
  }
  cvState.hobbies.forEach((h, idx) => {
    const card = document.createElement("div");
    card.className = "item-card";
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
        <input type="text" class="form-control" style="width:35%;" value="${escapeHtml(h.name)}" placeholder="Activité (ex: Marathon, Échecs...)" oninput="updateHobbyField(${idx}, 'name', this.value)">
        <input type="text" class="form-control" style="width:55%;" value="${escapeHtml(h.details)}" placeholder="Détails (ex: Club, Réalisations...)" oninput="updateHobbyField(${idx}, 'details', this.value)">
        <button class="btn btn-danger btn-sm" onclick="removeHobby(${idx})">✕</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function addHobbyCard() {
  cvState.hobbies.push({ name: "", details: "" });
  renderHobbiesList();
  renderPreview();
}

function removeHobby(idx) {
  cvState.hobbies.splice(idx, 1);
  renderHobbiesList();
  renderPreview();
}

function updateHobbyField(idx, field, val) {
  cvState.hobbies[idx][field] = val;
  renderPreview();
}

// ── Rendu de la Prévisualisation A4 Haute Définition ──
function renderPreview() {
  const container = document.getElementById("previewDocumentContent");
  if (!container) return;

  const gen = cvState.general || {};
  const hasContent = cvState.is_demo || 
    Boolean(gen.first_name || gen.last_name || gen.target_title || 
            (cvState.experiences && cvState.experiences.length > 0) || 
            (cvState.education && cvState.education.length > 0));

  if (!hasContent) {
    container.innerHTML = `
      <div class="preview-blank-placeholder">
        <div style="font-size:48px; margin-bottom:12px;">📄</div>
        <h3 style="font-size:18px; font-weight:700; color:#0f172a; margin-bottom:8px;">Curriculum Vitae Vierge</h3>
        <p style="font-size:13px; max-width:480px; margin:0 auto 20px; line-height:1.6;">
          Tous les champs sont actuellement vierges. Remplissez vos rubriques dans les onglets ci-dessus, ou chargez l'un des modèles démo pour réviser un exemple complet en 1 clic.
        </p>
        <div style="display:flex; justify-content:center; gap:8px;">
          <button class="btn btn-purple" onclick="fillDemoData('fr')">◈ Démo Osiris (Bouaké / CI)</button>
          <button class="btn btn-purple" onclick="fillDemoData('en')">🎲 Démo International (EN)</button>
          <button class="btn btn-purple" onclick="fillDemoData('de')">🎲 Démo Allemagne (DE)</button>
        </div>
      </div>
    `;
    return;
  }

  const pColor = cvState.config.primary_color || "#1e3a8a";
  const styleId = cvState.config.style_id || "modern_minimalist";
  const lang = cvState.config.cv_language || "fr";

  const titlesMap = {
    fr: {
      profile: "Profil Professionnel",
      experiences: "Expériences Professionnelles",
      education: "Études & Diplômes",
      certifications: "Certifications",
      skills: "Compétences Clés",
      languages: "Langues",
      hobbies: "Centres d'Intérêt"
    },
    en: {
      profile: "Professional Summary",
      experiences: "Work Experience",
      education: "Education & Qualifications",
      certifications: "Certifications",
      skills: "Core Skills",
      languages: "Languages",
      hobbies: "Hobbies & Interests"
    },
    de: {
      profile: "Kurzprofil",
      experiences: "Berufserfahrung",
      education: "Ausbildung & Studium",
      certifications: "Weiterbildung & Zertifikate",
      skills: "Kenntnisse & Fähigkeiten",
      languages: "Sprachkenntnisse",
      hobbies: "Hobbys & Interessen"
    }
  };
  const t = titlesMap[lang] || titlesMap.fr;

  let html = "";

  // Contact list items
  const contactItems = [];
  if (gen.email) contactItems.push(`<span>✉ ${escapeHtml(gen.email)}</span>`);
  if (gen.phone) contactItems.push(`<span>☎ ${escapeHtml(gen.phone)}</span>`);
  if (gen.city || gen.country) contactItems.push(`<span>📍 ${escapeHtml([gen.city, gen.country].filter(Boolean).join(", "))}</span>`);
  if (gen.linkedin) contactItems.push(`<span>🔗 ${escapeHtml(gen.linkedin)}</span>`);
  if (gen.github) contactItems.push(`<span>💻 ${escapeHtml(gen.github)}</span>`);

  // Civil status items (si affiché)
  const civilItems = [];
  if (cvState.config.show_civil_status) {
    if (gen.date_of_birth) civilItems.push(`Né(e) le : ${escapeHtml(gen.date_of_birth)}`);
    if (gen.place_of_birth) civilItems.push(`à ${escapeHtml(gen.place_of_birth)}`);
    if (gen.nationality) civilItems.push(`Nationalité : ${escapeHtml(gen.nationality)}`);
    if (gen.driving_license) civilItems.push(`Permis : ${escapeHtml(gen.driving_license)}`);
  }

  // Photo HTML
  const photoHtml = (cvState.config.show_photo && gen.photo_b64) 
    ? `<img src="${gen.photo_b64}" alt="Photo" style="width:90px; height:110px; object-fit:cover; border-radius:4px; border:2px solid ${pColor};">` 
    : '';

  // ── Rendu selon le Style Visuel ──
  if (styleId === "creative_sidebar") {
    // 2. Colonne Latérale Graphique
    html = `
      <div class="sidebar-col">
        ${photoHtml ? `<div style="text-align:center; margin-bottom:14px;">${photoHtml}</div>` : ''}
        <h2 style="font-size:16px; font-weight:800; color:${pColor};">${escapeHtml(gen.first_name)} ${escapeHtml((gen.last_name || '').toUpperCase())}</h2>
        <div style="font-size:12px; font-weight:600; color:#475569; margin-bottom:12px;">${escapeHtml(gen.target_title)}</div>

        <div class="cv-sec-title" style="color:${pColor}; border-bottom:1px solid ${pColor}; font-weight:bold; font-size:11.5px; margin-top:14px; text-transform:uppercase;">Contact</div>
        <div style="font-size:11px; line-height:1.6; margin-top:6px; color:#334155;">
          ${contactItems.map(c => `<div>${c}</div>`).join('')}
        </div>

        ${civilItems.length > 0 ? `
          <div class="cv-sec-title" style="color:${pColor}; border-bottom:1px solid ${pColor}; font-weight:bold; font-size:11.5px; margin-top:14px; text-transform:uppercase;">État Civil</div>
          <div style="font-size:10.5px; line-height:1.5; margin-top:4px; color:#64748b;">
            ${civilItems.map(ci => `<div>${ci}</div>`).join('')}
          </div>
        ` : ''}

        ${renderSkillsSidebarHtml(pColor, t.skills)}
        ${renderLanguagesSidebarHtml(pColor, t.languages)}
        ${renderHobbiesSidebarHtml(pColor, t.hobbies)}
      </div>

      <div class="main-col">
        ${gen.summary ? `
          <div class="cv-sec-title" style="color:${pColor}; border-bottom:2px solid ${pColor}; font-weight:bold; font-size:12.5px; text-transform:uppercase; margin-bottom:6px;">${t.profile}</div>
          <div style="font-size:11.5px; line-height:1.5; color:#334155; margin-bottom:14px;">${escapeHtml(gen.summary)}</div>
        ` : ''}

        ${renderExperiencesHtml(pColor, t.experiences)}
        ${renderEducationHtml(pColor, t.education)}
        ${renderCertificationsHtml(pColor, t.certifications)}
        ${renderSignoffHtml(pColor)}
      </div>
    `;
  } else {
    // Styles 1, 3, 4, 5, 6 en format Standard / Tabulaire
    html = `
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid ${pColor}; padding-bottom:12px; margin-bottom:12px;">
        <div>
          <h1 style="margin:0; font-size:24px; color:#0f172a;">${escapeHtml(gen.first_name)} <span style="color:${pColor};">${escapeHtml((gen.last_name || '').toUpperCase())}</span></h1>
          <div style="font-size:14px; font-weight:600; color:${pColor}; text-transform:uppercase; margin-top:2px;">${escapeHtml(gen.target_title)}</div>
          <div style="display:flex; flex-wrap:wrap; gap:12px; font-size:11px; color:#475569; margin-top:6px;">
            ${contactItems.join('')}
          </div>
          ${civilItems.length > 0 ? `
            <div style="font-size:10.5px; color:#64748b; font-style:italic; margin-top:4px;">
              ${civilItems.join(' • ')}
            </div>
          ` : ''}
        </div>
        ${photoHtml ? `<div>${photoHtml}</div>` : ''}
      </div>

      ${gen.summary ? `
        <div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:10px; margin-bottom:6px;">${t.profile}</div>
        <div style="font-size:11.5px; line-height:1.5; color:#334155; margin-bottom:12px;">${escapeHtml(gen.summary)}</div>
      ` : ''}

      ${renderExperiencesHtml(pColor, t.experiences, styleId)}
      ${renderEducationHtml(pColor, t.education, styleId)}
      ${renderCertificationsHtml(pColor, t.certifications)}
      ${renderSkillsStandardHtml(pColor, t.skills)}
      ${renderLanguagesStandardHtml(pColor, t.languages)}
      ${renderHobbiesStandardHtml(pColor, t.hobbies)}
      ${renderSignoffHtml(pColor)}
    `;
  }

  container.className = `cv-paper style-${styleId}`;
  container.innerHTML = html;
}

// ── Helpers de Rendu HTML pour le CV ──
function renderExperiencesHtml(pColor, secTitle, styleId) {
  if (!cvState.experiences || cvState.experiences.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:12px; margin-bottom:8px;">${secTitle}</div>`;
  cvState.experiences.forEach(exp => {
    const dates = [exp.start_date, exp.end_date || (exp.is_current ? 'Présent' : '')].filter(Boolean).join(" – ");
    if (styleId === "german_tabular") {
      out += `
        <div class="tab-row" style="display:grid; grid-template-columns:110px 1fr; gap:12px; margin-bottom:10px; font-size:11.5px;">
          <div class="tab-date" style="font-weight:bold; color:${pColor};">${escapeHtml(dates)}</div>
          <div>
            <strong>${escapeHtml(exp.job_title)}</strong> • <span style="color:${pColor};">${escapeHtml(exp.company)}</span> (${escapeHtml(exp.location)})
            ${exp.description ? `<div style="margin-top:2px; color:#475569;">${escapeHtml(exp.description)}</div>` : ''}
            ${(exp.achievements || []).map(a => `<div style="padding-left:8px;">• ${escapeHtml(a)}</div>`).join('')}
          </div>
        </div>
      `;
    } else {
      out += `
        <div style="margin-bottom:10px; font-size:11.5px;">
          <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <div><strong>${escapeHtml(exp.job_title)}</strong> | <span style="color:${pColor}; font-weight:600;">${escapeHtml(exp.company)}</span> (${escapeHtml(exp.location)})</div>
            <div style="font-size:10.5px; font-weight:bold; color:#64748b;">${escapeHtml(dates)}</div>
          </div>
          ${exp.description ? `<div style="margin-top:2px; color:#334155;">${escapeHtml(exp.description)}</div>` : ''}
          ${(exp.achievements || []).map(a => `<div style="padding-left:10px; color:#334155;">• ${escapeHtml(a)}</div>`).join('')}
        </div>
      `;
    }
  });
  return out;
}

function renderEducationHtml(pColor, secTitle, styleId) {
  if (!cvState.education || cvState.education.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:12px; margin-bottom:8px;">${secTitle}</div>`;
  cvState.education.forEach(edu => {
    const dates = [edu.start_date, edu.end_date].filter(Boolean).join(" – ");
    if (styleId === "german_tabular") {
      out += `
        <div class="tab-row" style="display:grid; grid-template-columns:110px 1fr; gap:12px; margin-bottom:8px; font-size:11.5px;">
          <div class="tab-date" style="font-weight:bold; color:${pColor};">${escapeHtml(dates)}</div>
          <div>
            <strong>${escapeHtml(edu.degree)}</strong> • ${escapeHtml(edu.institution)}
            ${edu.honors ? `<div style="font-style:italic; color:#475569;">${escapeHtml(edu.honors)}</div>` : ''}
          </div>
        </div>
      `;
    } else {
      out += `
        <div style="margin-bottom:8px; font-size:11.5px;">
          <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <div><strong>${escapeHtml(edu.degree)}</strong> – <span style="color:${pColor};">${escapeHtml(edu.institution)}</span> (${escapeHtml(edu.location)})</div>
            <div style="font-size:10.5px; font-weight:bold; color:#64748b;">${escapeHtml(dates)}</div>
          </div>
          ${(edu.honors || edu.details) ? `<div style="font-size:10.5px; color:#475569; font-style:italic;">${escapeHtml([edu.honors, edu.details].filter(Boolean).join(' • '))}</div>` : ''}
        </div>
      `;
    }
  });
  return out;
}

function renderCertificationsHtml(pColor, secTitle) {
  if (!cvState.certifications || cvState.certifications.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:10px; margin-bottom:6px;">${secTitle}</div>`;
  out += `<div style="font-size:11px; line-height:1.6;">`;
  cvState.certifications.forEach(c => {
    out += `<div>• <strong>${escapeHtml(c.name)}</strong> – <span style="color:#64748b;">${escapeHtml(c.issuing_org)} (${escapeHtml(c.issue_date)})</span></div>`;
  });
  out += `</div>`;
  return out;
}

function renderSkillsStandardHtml(pColor, secTitle) {
  if (!cvState.skills || cvState.skills.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:10px; margin-bottom:6px;">${secTitle}</div>`;
  out += `<div style="font-size:11px; display:flex; flex-wrap:wrap; gap:6px;">`;
  cvState.skills.forEach(s => {
    out += `<span class="skill-tag" style="border-left:3px solid ${pColor};">${escapeHtml(s.name)}</span>`;
  });
  out += `</div>`;
  return out;
}

function renderLanguagesStandardHtml(pColor, secTitle) {
  if (!cvState.languages || cvState.languages.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:10px; margin-bottom:6px;">${secTitle}</div>`;
  out += `<div style="font-size:11px; display:flex; flex-wrap:wrap; gap:16px;">`;
  cvState.languages.forEach(l => {
    let badge = "";
    if (l.eval_mode === 'cecr') badge = `<strong>[${escapeHtml(l.cecr_level)}]</strong> ${escapeHtml(l.desc_level || '')}`;
    else if (l.eval_mode === 'descriptive') badge = `<em>${escapeHtml(l.desc_level || '')}</em>`;
    else badge = `<span class="dots-container">${renderDotsHtml(l.dots || 4, pColor)}</span>`;
    out += `<div><strong>${escapeHtml(l.language)} :</strong> ${badge}</div>`;
  });
  out += `</div>`;
  return out;
}

function renderHobbiesStandardHtml(pColor, secTitle) {
  if (!cvState.hobbies || cvState.hobbies.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1.5px solid ${pColor}; font-weight:bold; font-size:12px; text-transform:uppercase; margin-top:10px; margin-bottom:6px;">${secTitle}</div>`;
  out += `<div style="font-size:11px; color:#475569;">`;
  out += cvState.hobbies.map(h => `<strong>${escapeHtml(h.name)}</strong>${h.details ? ' (' + escapeHtml(h.details) + ')' : ''}`).join('   •   ');
  out += `</div>`;
  return out;
}

function renderSkillsSidebarHtml(pColor, secTitle) {
  if (!cvState.skills || cvState.skills.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1px solid ${pColor}; font-weight:bold; font-size:11.5px; margin-top:14px; text-transform:uppercase;">${secTitle}</div><div style="font-size:11px; line-height:1.5; margin-top:4px;">`;
  cvState.skills.forEach(s => {
    out += `<div>• ${escapeHtml(s.name)}</div>`;
  });
  out += `</div>`;
  return out;
}

function renderLanguagesSidebarHtml(pColor, secTitle) {
  if (!cvState.languages || cvState.languages.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1px solid ${pColor}; font-weight:bold; font-size:11.5px; margin-top:14px; text-transform:uppercase;">${secTitle}</div><div style="font-size:11px; line-height:1.5; margin-top:4px;">`;
  cvState.languages.forEach(l => {
    let lvl = l.eval_mode === 'cecr' ? `[${l.cecr_level}]` : (l.desc_level || `${l.dots}/5`);
    out += `<div><strong>${escapeHtml(l.language)}:</strong> ${escapeHtml(lvl)}</div>`;
  });
  out += `</div>`;
  return out;
}

function renderHobbiesSidebarHtml(pColor, secTitle) {
  if (!cvState.hobbies || cvState.hobbies.length === 0) return "";
  let out = `<div class="cv-sec-title" style="color:${pColor}; border-bottom:1px solid ${pColor}; font-weight:bold; font-size:11.5px; margin-top:14px; text-transform:uppercase;">${secTitle}</div><div style="font-size:10.5px; line-height:1.5; margin-top:4px; color:#475569;">`;
  out += cvState.hobbies.map(h => escapeHtml(h.name)).join(', ');
  out += `</div>`;
  return out;
}

function renderSignoffHtml(pColor) {
  if (!cvState.config.show_signoff || !cvState.signoff || !cvState.signoff.enabled) return "";
  return `
    <div style="margin-top:28px; font-size:11px; page-break-inside:avoid;">
      <div><em>${escapeHtml(cvState.signoff.place || '')}, ${escapeHtml(cvState.signoff.date_str || '')}</em></div>
      <div style="font-weight:bold; color:${pColor}; text-decoration:underline; margin-top:6px;">${escapeHtml(cvState.signoff.signature_name || '')}</div>
    </div>
  `;
}

function renderDotsHtml(level, color) {
  let dots = "";
  for (let i = 1; i <= 5; i++) {
    dots += `<span class="dot-item ${i <= level ? 'filled' : ''}" style="${i <= level ? 'background-color:' + color + '; border-color:' + color : ''}"></span>`;
  }
  return dots;
}

// ── Export & Impression ──
function triggerPrint() {
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
  document.querySelector('[data-tab="tab-preview"]').classList.add("active");
  document.getElementById("tab-preview").classList.add("active");
  renderPreview();
  setTimeout(() => {
    window.print();
  }, 150);
}

function triggerExportDocx() {
  exportCvDocx(cvState);
}

function exportJsonState() {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(cvState, null, 2));
  const dl = document.createElement("a");
  const fn = (cvState.general.first_name || "CV").replace(/\s+/g, '_');
  const ln = (cvState.general.last_name || "CANDIDAT").replace(/\s+/g, '_');
  dl.setAttribute("href", dataStr);
  dl.setAttribute("download", `CV_${fn}_${ln}.json`);
  document.body.appendChild(dl);
  dl.click();
  dl.remove();
}

function importJsonState(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (event) => {
    try {
      const parsed = JSON.parse(event.target.result);
      cvState = Object.assign({}, defaultBlankState, parsed);
      renderAll();
      alert("Sauvegarde CV chargée avec succès !");
    } catch (err) {
      alert("Erreur de lecture du fichier JSON : " + err.message);
    }
  };
  reader.readAsText(file);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
