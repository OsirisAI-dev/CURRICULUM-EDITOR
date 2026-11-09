/**
 * Générateur Word (.docx) 100% Client-Side pour Éditeur de Curriculum Vitae (CV)
 * Génère un document Microsoft Word (.docx) authentique et valide sans aucun serveur requis.
 */

function escapeXml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function exportCvDocx(data) {
  if (typeof JSZip === "undefined") {
    alert("Erreur: JSZip non chargé. Export DOCX impossible.");
    return;
  }

  const zip = new JSZip();

  // 1. [Content_Types].xml
  zip.file("[Content_Types].xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>`);

  // 2. _rels/.rels
  zip.folder("_rels").file(".rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>`);

  // 3. word/_rels/document.xml.rels
  zip.folder("word").folder("_rels").file("document.xml.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`);

  // 4. word/styles.xml
  zip.folder("word").file("styles.xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI" w:cs="Segoe UI"/>
        <w:sz w:val="21"/>
        <w:color w:val="1E293B"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>`);

  // Section titles mapping based on language
  const lang = (data.config && data.config.cv_language) || "fr";
  const titlesMap = {
    fr: {
      profile: "PROFIL PROFESSIONNEL",
      experiences: "EXPÉRIENCES PROFESSIONNELLES",
      education: "ÉTUDES & DIPLÔMES",
      certifications: "CERTIFICATIONS & FORMATIONS",
      skills: "COMPÉTENCES CLÉS",
      languages: "LANGUES",
      hobbies: "CENTRES D'INTÉRÊT"
    },
    en: {
      profile: "PROFESSIONAL SUMMARY",
      experiences: "WORK EXPERIENCE",
      education: "EDUCATION & QUALIFICATIONS",
      certifications: "CERTIFICATIONS",
      skills: "CORE SKILLS",
      languages: "LANGUAGES",
      hobbies: "HOBBIES & INTERESTS"
    },
    de: {
      profile: "KURZPROFIL",
      experiences: "BERUFSERFAHRUNG",
      education: "AUSBILDUNG & STUDIUM",
      certifications: "WEITERBILDUNG & ZERTIFIKATE",
      skills: "KENNTNISSE & FÄHIGKEITEN",
      languages: "SPRACHKENNTNISSE",
      hobbies: "HOBBYS & INTERESSEN"
    }
  };
  const t = titlesMap[lang] || titlesMap.fr;
  const pHex = ((data.config && data.config.primary_color) || "#1e3a8a").replace("#", "").toUpperCase();

  const gen = data.general || {};

  function makeHeading(titleText) {
    return `
    <w:p>
      <w:pPr>
        <w:spacing w:before="240" w:after="80"/>
        <w:pBdr>
          <w:bottom w:val="single" w:sz="12" w:space="4" w:color="${pHex}"/>
        </w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="22"/>
          <w:color w:val="${pHex}"/>
        </w:rPr>
        <w:t>${escapeXml(titleText)}</w:t>
      </w:r>
    </w:p>`;
  }

  // 5. Build word/document.xml
  let docXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <!-- EN-TETE DU CANDIDAT -->
    <w:p>
      <w:pPr>
        <w:spacing w:after="40"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="38"/>
          <w:color w:val="0F172A"/>
        </w:rPr>
        <w:t>${escapeXml(gen.first_name || "")} </w:t>
      </w:r>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="38"/>
          <w:color w:val="${pHex}"/>
        </w:rPr>
        <w:t>${escapeXml((gen.last_name || "").toUpperCase())}</w:t>
      </w:r>
    </w:p>`;

  if (gen.target_title) {
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="80"/></w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="24"/>
          <w:color w:val="${pHex}"/>
        </w:rPr>
        <w:t>${escapeXml(gen.target_title.toUpperCase())}</w:t>
      </w:r>
    </w:p>`;
  }

  // Contact info
  const contactParts = [];
  if (gen.email) contactParts.push(`✉ ${gen.email}`);
  if (gen.phone) contactParts.push(`☎ ${gen.phone}`);
  if (gen.city || gen.country) contactParts.push(`📍 ${[gen.city, gen.country].filter(Boolean).join(", ")}`);
  if (gen.linkedin) contactParts.push(`🔗 ${gen.linkedin}`);
  if (gen.github) contactParts.push(`💻 ${gen.github}`);

  if (contactParts.length > 0) {
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="120"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="18"/><w:color w:val="475569"/></w:rPr>
        <w:t>${escapeXml(contactParts.join("   •   "))}</w:t>
      </w:r>
    </w:p>`;
  }

  // État civil (si autorisé / présent)
  const civilParts = [];
  if (gen.date_of_birth) civilParts.push(`Né(e) le: ${gen.date_of_birth}`);
  if (gen.place_of_birth) civilParts.push(`à: ${gen.place_of_birth}`);
  if (gen.nationality) civilParts.push(`Nationalité: ${gen.nationality}`);
  if (gen.driving_license) civilParts.push(`Permis: ${gen.driving_license}`);
  if (civilParts.length > 0) {
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="120"/></w:pPr>
      <w:r>
        <w:rPr><w:i/><w:sz w:val="17"/><w:color w:val="64748B"/></w:rPr>
        <w:t>${escapeXml(civilParts.join(" | "))}</w:t>
      </w:r>
    </w:p>`;
  }

  // Résumé / Profil
  if (gen.summary) {
    docXml += makeHeading(t.profile);
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="120"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="20"/></w:rPr>
        <w:t>${escapeXml(gen.summary)}</w:t>
      </w:r>
    </w:p>`;
  }

  // Expériences
  if (data.experiences && data.experiences.length > 0) {
    docXml += makeHeading(t.experiences);
    data.experiences.forEach(exp => {
      const dates = [exp.start_date, exp.end_date || (exp.is_current ? "Présent" : "")].filter(Boolean).join(" – ");
      docXml += `
      <w:p>
        <w:pPr><w:spacing w:before="100" w:after="20"/></w:pPr>
        <w:r>
          <w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="0F172A"/></w:rPr>
          <w:t>${escapeXml(exp.job_title || "")} </w:t>
        </w:r>
        <w:r>
          <w:rPr><w:b/><w:sz w:val="20"/><w:color w:val="${pHex}"/></w:rPr>
          <w:t>| ${escapeXml(exp.company || "")}</w:t>
        </w:r>
        ${dates ? `
        <w:r>
          <w:rPr><w:sz w:val="18"/><w:color w:val="64748B"/></w:rPr>
          <w:t> (${escapeXml(dates)})</w:t>
        </w:r>` : ''}
      </w:p>`;

      if (exp.description) {
        docXml += `
      <w:p>
        <w:pPr><w:spacing w:after="40"/></w:pPr>
        <w:r><w:rPr><w:sz w:val="19"/></w:rPr><w:t>${escapeXml(exp.description)}</w:t></w:r>
      </w:p>`;
      }

      if (exp.achievements && exp.achievements.length > 0) {
        exp.achievements.forEach(ach => {
          docXml += `
      <w:p>
        <w:pPr><w:spacing w:after="20"/><w:ind w:left="280"/></w:pPr>
        <w:r><w:rPr><w:color w:val="${pHex}"/></w:rPr><w:t>• </w:t></w:r>
        <w:r><w:rPr><w:sz w:val="19"/></w:rPr><w:t>${escapeXml(ach)}</w:t></w:r>
      </w:p>`;
        });
      }
    });
  }

  // Études / Diplômes
  if (data.education && data.education.length > 0) {
    docXml += makeHeading(t.education);
    data.education.forEach(edu => {
      const dates = [edu.start_date, edu.end_date].filter(Boolean).join(" – ");
      docXml += `
      <w:p>
        <w:pPr><w:spacing w:before="80" w:after="20"/></w:pPr>
        <w:r><w:rPr><w:b/><w:sz w:val="21"/></w:rPr><w:t>${escapeXml(edu.degree || "")} </w:t></w:r>
        <w:r><w:rPr><w:color w:val="${pHex}"/></w:rPr><w:t>– ${escapeXml(edu.institution || "")}</w:t></w:r>
        ${dates ? `<w:r><w:rPr><w:sz w:val="18"/><w:color w:val="64748B"/></w:rPr><w:t> [${escapeXml(dates)}]</w:t></w:r>` : ''}
      </w:p>`;

      const details = [edu.honors, edu.details].filter(Boolean).join(" • ");
      if (details) {
        docXml += `
      <w:p>
        <w:pPr><w:spacing w:after="40"/><w:ind w:left="200"/></w:pPr>
        <w:r><w:rPr><w:i/><w:sz w:val="18"/><w:color w:val="475569"/></w:rPr><w:t>${escapeXml(details)}</w:t></w:r>
      </w:p>`;
      }
    });
  }

  // Certifications
  if (data.certifications && data.certifications.length > 0) {
    docXml += makeHeading(t.certifications);
    data.certifications.forEach(cert => {
      docXml += `
      <w:p>
        <w:pPr><w:spacing w:after="30"/></w:pPr>
        <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• ${escapeXml(cert.name || "")} </w:t></w:r>
        <w:r><w:rPr><w:color w:val="64748B"/><w:sz w:val="18"/></w:rPr><w:t>(${escapeXml(cert.issuing_org || "")}${cert.issue_date ? " - " + escapeXml(cert.issue_date) : ""})</w:t></w:r>
      </w:p>`;
    });
  }

  // Compétences
  if (data.skills && data.skills.length > 0) {
    docXml += makeHeading(t.skills);
    const skillList = data.skills.map(s => `${s.name}${s.category ? " (" + s.category + ")" : ""}`).join("   •   ");
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="19"/></w:rPr><w:t>${escapeXml(skillList)}</w:t></w:r>
    </w:p>`;
  }

  // Langues
  if (data.languages && data.languages.length > 0) {
    docXml += makeHeading(t.languages);
    data.languages.forEach(l => {
      let lvl = l.cecr_level ? `[${l.cecr_level}]` : "";
      if (l.desc_level) lvl += ` ${l.desc_level}`;
      docXml += `
      <w:p>
        <w:pPr><w:spacing w:after="20"/></w:pPr>
        <w:r><w:rPr><w:b/><w:sz w:val="19"/></w:rPr><w:t>• ${escapeXml(l.language)} : </w:t></w:r>
        <w:r><w:rPr><w:color w:val="475569"/><w:sz w:val="18"/></w:rPr><w:t>${escapeXml(lvl)}</w:t></w:r>
      </w:p>`;
    });
  }

  // Hobbys
  if (data.hobbies && data.hobbies.length > 0) {
    docXml += makeHeading(t.hobbies);
    const hobList = data.hobbies.map(h => `${h.name}${h.details ? " : " + h.details : ""}`).join("   •   ");
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="18"/><w:color w:val="475569"/></w:rPr><w:t>${escapeXml(hobList)}</w:t></w:r>
    </w:p>`;
  }

  // Signoff DACH
  if (data.signoff && data.signoff.enabled) {
    docXml += `
    <w:p>
      <w:pPr><w:spacing w:before="300" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/></w:rPr><w:t>${escapeXml(data.signoff.place || "")}, ${escapeXml(data.signoff.date_str || "")}</w:t></w:r>
    </w:p>
    <w:p>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/><w:color w:val="${pHex}"/></w:rPr><w:t>${escapeXml(data.signoff.signature_name || "")}</w:t></w:r>
    </w:p>`;
  }

  docXml += `
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>
    </w:sectPr>
  </w:body>
</w:document>`;

  zip.folder("word").file("document.xml", docXml);

  // Generate and download
  zip.generateAsync({ type: "blob" }).then(function (content) {
    const fn = (gen.first_name || "CV").replace(/\s+/g, "_");
    const ln = (gen.last_name || "CANDIDAT").replace(/\s+/g, "_");
    const filename = `CV_${fn}_${ln}_${lang.toUpperCase()}.docx`;
    const link = document.createElement("a");
    link.href = URL.createObjectURL(content);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  });
}
