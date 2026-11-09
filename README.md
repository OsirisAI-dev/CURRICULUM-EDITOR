# 💼 Curriculum Vitae Studio

> **Éditeur de CV Professionnel Multi-Styles & Multi-Langues (FR / EN / DE)**  
> *Conçu pour l'accessibilité universelle : application Web 100% autonome (0 dépendance) & version bureau Windows.*

[![GitHub Pages](https://img.shields.io/badge/Demo-GitHub%20Pages-blue?style=flat-square&logo=github)](https://osirisai-dev.github.io/CURRICULUM-EDITOR/)
[![Python](https://img.shields.io/badge/Python-3.8+-brightgreen?style=flat-square&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## 🌟 Démonstration en Ligne Immédiate (GitHub Pages)

Vous pouvez tester l'application directement dans votre navigateur, sur mobile, tablette ou ordinateur sans rien installer :

👉 **[Accéder au Web Studio en Direct]([https://osirisai-dev.github.io/cv-maker/](https://github.com/OsirisAI-dev/CURRICULUM-EDITOR/blob/main/index.html)**

---

## 📋 Présentation du Projet

**Curriculum Vitae Studio** est une solution complète permettant de créer, personnaliser et exporter des Curriculum Vitae répondant aux exigences culturelles et normatives de plusieurs marchés du travail :

* **🇫🇷 France & Francophonie** : Format standardisé avec photo, état civil, permis et parcours structuré.
* **🇬🇧 Modèle Anglophone (US Resume / UK CV)** : Structure anti-discrimination stricte (sans photo, sans âge), accent porté sur l'impact mesurable, les compétences et le résumé professionnel.
* **🇩🇪 Modèle Germanophone (DACH : Deutschland, Österreich, Schweiz)** : *Tabellarischer Lebenslauf* rigoureux avec date de naissance, nationalité et signature formelle (*Ort, Datum, Unterschrift*).

---

## ✨ Fonctionnalités Clés

* **🎨 6 Styles Visuels Prédéfinis** :
  * *Moderne Minimaliste* (universel, épuré)
  * *Colonne Latérale Graphique* (2 colonnes, bandeau dynamique)
  * *Exécutif Corporate* (cadres, ingénieurs, juristes)
  * *Tabellarischer Lebenslauf* (standard DACH strict)
  * *Tech & Développeur* (densité d'information, tags de compétences)
  * *Académique & Europass* (recherche et enseignement)
* **📄 Export Multi-Formats 100% Client-Side** :
  * **DOCX (Word)** : Généré directement en OpenXML standard (compatible Word, LibreOffice, Google Docs).
  * **PDF & Impression** : Mise en page CSS vectorielle haute fidélité (`@media print` calibrée A4).
  * **HTML / JSON** : Sauvegarde et rechargement instantanés des données.
* **🌍 Zéro Dépendance Serveur** : Toutes les données restent privées et ne quittent jamais votre machine.

---

## 🚀 Utilisation & Lancement

### 1. Version Web (Recommandée - 0 installation)
Ouvrez simplement le fichier `index.html` dans n'importe quel navigateur ou utilisez le lien GitHub Pages ci-dessus.

### 2. Version Bureau Python (CustomTkinter)
Pour lancer l'interface graphique de bureau avec prévisualisation dynamique :

```bash
# 1. Cloner le dépôt
git clone https://github.com/OsirisAI-dev/cv-maker.git
cd cv-maker/desktop_app

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python cv_editor_ui.py
```

---

## 🏗️ Structure du Dépôt

```text
cv-maker/
├── index.html            # Point d'entrée du Web Studio (GitHub Pages)
├── css/                  # Feuilles de styles et thèmes
├── js/                   # Moteur d'exportation DOCX/PDF et logique
├── assets/               # Icônes et ressources graphiques
│
├── desktop_app/          # Application de bureau Python
│   ├── cv_editor_ui.py   # Interface CustomTkinter
│   ├── cv_models.py      # Modèles de données
│   ├── cv_translations.py# Dictionnaires FR/EN/DE & profils types
│   ├── cv_docx_gen.py    # Générateur Word natif
│   ├── cv_pdf_gen.py     # Moteur PDF vectoriel
│   └── requirements.txt  # Dépendances Python
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 👨‍🏫 Contexte & Démarche

Ce projet s'inscrit dans une démarche pédagogique et d'apprentissage continu : faire le pont entre la rigueur de la **linguistique** (enseignement de l'allemand) et la logique du **génie logiciel**.

---

## 📜 Licence

Ce projet est distribué sous licence libre **MIT**. Vous êtes libre de l'utiliser, le modifier et le redistribuer.
