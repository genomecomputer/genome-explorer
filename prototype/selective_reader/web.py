PAGE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="data:,">
  <title>Genome Explorer</title>
  <style nonce="__NONCE__">
    :root {
      color-scheme: light;
      --ink: #14211d;
      --muted: #65736d;
      --line: #dce5df;
      --surface: #ffffff;
      --soft: #f3f7f4;
      --accent: #176b4d;
      --accent-dark: #0d4934;
      --accent-soft: #e5f2eb;
      --blue-soft: #eaf2f8;
      --shadow: 0 18px 60px rgba(25, 54, 43, 0.10);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% 0%, rgba(93, 173, 134, .14), transparent 30rem),
        linear-gradient(180deg, #fbfdfb 0%, #f4f8f5 100%);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    button, input { font: inherit; }
    .shell { width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 26px 0 64px; }
    header { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
    .brand { display: flex; align-items: center; gap: 12px; font-weight: 760; letter-spacing: -.02em; }
    .mark {
      width: 34px; height: 34px; border-radius: 10px; display: grid; place-items: center;
      color: white; background: var(--accent); box-shadow: 0 8px 20px rgba(23, 107, 77, .22);
    }
    .mark svg { width: 19px; height: 19px; }
    .privacy {
      display: inline-flex; align-items: center; gap: 8px; padding: 8px 11px;
      color: var(--accent-dark); background: var(--accent-soft); border: 1px solid #cde4d6;
      border-radius: 999px; font-size: 13px; font-weight: 680;
    }
    .privacy-dot { width: 7px; height: 7px; border-radius: 50%; background: #269663; box-shadow: 0 0 0 4px rgba(38,150,99,.10); }
    main { padding-top: 62px; }
    .eyebrow { margin: 0 0 14px; color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    h1 { max-width: 940px; margin: 0; font-size: clamp(38px, 5.3vw, 66px); line-height: .98; letter-spacing: -.055em; }
    .lede { max-width: 700px; margin: 22px 0 0; color: var(--muted); font-size: 18px; line-height: 1.6; }
    .search-panel {
      margin-top: 32px; padding: 10px; background: rgba(255,255,255,.92); border: 1px solid var(--line);
      border-radius: 18px; box-shadow: var(--shadow); backdrop-filter: blur(14px);
    }
    form { display: flex; gap: 8px; }
    input[type="search"] {
      width: 100%; min-width: 0; padding: 17px 18px; color: var(--ink); background: transparent;
      border: 0; outline: none; font-size: 17px;
    }
    input[type="search"]::placeholder { color: #8b9892; }
    .search-button {
      flex: 0 0 auto; padding: 0 23px; color: white; background: var(--accent); border: 0;
      border-radius: 12px; font-weight: 750; cursor: pointer; transition: background .15s, transform .15s;
    }
    .search-button:hover { background: var(--accent-dark); }
    .search-button:active { transform: translateY(1px); }
    .search-button:disabled { cursor: wait; opacity: .7; }
    .examples { display: flex; align-items: center; flex-wrap: wrap; gap: 7px; margin-top: 13px; }
    .examples span { margin-right: 3px; color: var(--muted); font-size: 12px; }
    .example {
      padding: 7px 10px; color: #3d4e46; background: rgba(255,255,255,.75); border: 1px solid var(--line);
      border-radius: 999px; font-size: 12px; cursor: pointer;
    }
    .example:hover { color: var(--accent-dark); border-color: #afcbbd; background: var(--accent-soft); }
    .bundle-strip {
      display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; margin-top: 40px;
      overflow: hidden; background: var(--line); border: 1px solid var(--line); border-radius: 15px;
    }
    .bundle-stat { min-height: 105px; padding: 19px; background: rgba(255,255,255,.88); }
    .bundle-stat dt { margin-bottom: 8px; color: var(--muted); font-size: 11px; font-weight: 760; letter-spacing: .08em; text-transform: uppercase; }
    .bundle-stat dd { margin: 0; font-size: 16px; font-weight: 720; letter-spacing: -.01em; }
    .bundle-stat small { display: block; margin-top: 6px; color: var(--muted); font-size: 12px; font-weight: 450; }
    .results { margin-top: 48px; }
    .results[hidden] { display: none; }
    .results-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 18px; }
    .results h2 { margin: 0; font-size: 25px; letter-spacing: -.03em; }
    .result-meta { color: var(--muted); font-size: 13px; }
    .notice {
      display: flex; gap: 10px; align-items: flex-start; margin-bottom: 20px; padding: 13px 15px;
      color: #43544c; background: var(--blue-soft); border: 1px solid #d6e5ef; border-radius: 12px; font-size: 13px; line-height: 1.5;
    }
    .notice svg { flex: 0 0 auto; margin-top: 1px; }
    .section { margin-top: 28px; }
    .section-title { display: flex; align-items: center; gap: 10px; margin-bottom: 11px; color: #35453e; font-size: 13px; font-weight: 790; letter-spacing: .06em; text-transform: uppercase; }
    .count { padding: 3px 7px; color: var(--accent-dark); background: var(--accent-soft); border-radius: 999px; font-size: 11px; }
    .cards { display: grid; gap: 10px; }
    .section-variants .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .section-variants .fields { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .card { padding: 20px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; box-shadow: 0 5px 20px rgba(25,54,43,.045); }
    .card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
    .card h3 { margin: 0; font-size: 17px; letter-spacing: -.02em; }
    .card-id { color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
    .fields { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px 22px; margin: 18px 0 0; }
    .field dt { margin-bottom: 5px; color: var(--muted); font-size: 10px; font-weight: 760; letter-spacing: .07em; text-transform: uppercase; }
    .field dd { margin: 0; overflow-wrap: anywhere; font-size: 13px; line-height: 1.45; }
    .field a { color: var(--accent); font-weight: 680; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .empty { padding: 38px; text-align: center; color: var(--muted); background: var(--surface); border: 1px dashed #cbd8d0; border-radius: 14px; }
    .error { color: #812f2f; background: #fff1f0; border-color: #f0d2cf; }
    .spinner { display: inline-block; width: 15px; height: 15px; margin-right: 7px; vertical-align: -2px; border: 2px solid rgba(255,255,255,.4); border-top-color: white; border-radius: 50%; animation: spin .7s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 760px) {
      .shell { width: min(100% - 24px, 1120px); padding-top: 18px; }
      main { padding-top: 52px; }
      .privacy { font-size: 0; }
      .privacy-dot { margin: 3px; }
      form { align-items: stretch; }
      .search-button { padding: 0 17px; }
      .bundle-strip { grid-template-columns: 1fr 1fr; }
      .fields { grid-template-columns: 1fr 1fr; }
      .section-variants .cards { grid-template-columns: 1fr; }
    }
    @media (max-width: 480px) {
      h1 { font-size: 39px; }
      .lede { font-size: 16px; }
      .search-panel { padding: 7px; }
      input[type="search"] { padding: 14px 12px; font-size: 15px; }
      .search-button { padding: 0 13px; font-size: 14px; }
      .bundle-strip { grid-template-columns: 1fr; }
      .fields { grid-template-columns: 1fr; }
      .results-head { align-items: flex-start; flex-direction: column; gap: 5px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="brand">
        <span class="mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 3c0 5 8 5 8 10s-8 5-8 8M16 3c0 5-8 5-8 10s8 5 8 8M8.8 7h6.4M8.8 17h6.4"/></svg>
        </span>
        <span>Genome Explorer</span>
      </div>
      <div class="privacy"><span class="privacy-dot"></span>Private and local</div>
    </header>

    <main>
      <p class="eyebrow">Your bundle is ready</p>
      <h1>Search your genome without sending it anywhere.</h1>
      <p class="lede">Explore recorded variants, genes, medications, traits, and genomic coordinates. Every result comes directly from this bundle.</p>

      <div class="search-panel">
        <form id="search-form">
          <input id="search-input" type="search" aria-label="Search your genome" autocomplete="off" spellcheck="false" placeholder="Try a gene, rsID, coordinate, medication, or trait" autofocus>
          <button class="search-button" id="search-button" type="submit">Search</button>
        </form>
      </div>
      <div class="examples" aria-label="Example searches">
        <span>Try</span>
        <button class="example" type="button">CYP2C19</button>
        <button class="example" type="button">rs11188082</button>
        <button class="example" type="button">chr10:94808278</button>
        <button class="example" type="button">clopidogrel</button>
        <button class="example" type="button">cholesterol</button>
      </div>

      <dl class="bundle-strip" id="bundle-strip" aria-label="Bundle status">
        <div class="bundle-stat"><dt>Validation</dt><dd id="validation">Verified</dd><small id="validation-detail">Checking bundle</small></div>
        <div class="bundle-stat"><dt>Reference</dt><dd id="build">Loading</dd><small>Genome build</small></div>
        <div class="bundle-stat"><dt>Snapshot</dt><dd id="snapshot">Loading</dd><small>Recorded bundle date</small></div>
        <div class="bundle-stat"><dt>Local data</dt><dd id="stored">Loading</dd><small>Available to search</small></div>
      </dl>

      <section class="results" id="results" hidden aria-live="polite">
        <div class="results-head">
          <h2 id="results-title">Recorded matches</h2>
          <div class="result-meta" id="result-meta"></div>
        </div>
        <div class="notice">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>
          <span>Results reproduce fields recorded in the bundle. Genome Explorer does not infer diagnoses or treatment advice.</span>
        </div>
        <div id="result-content"></div>
      </section>
    </main>
  </div>

  <script nonce="__NONCE__">
    const basePath = "__BASE_PATH__";
    const form = document.querySelector("#search-form");
    const input = document.querySelector("#search-input");
    const button = document.querySelector("#search-button");
    const results = document.querySelector("#results");
    const content = document.querySelector("#result-content");

    const fieldLabels = {
      variant_id: "Variant", rsid: "rsID", chrom: "Chromosome", pos: "Position",
      ref: "Reference", alt: "Alternate", genotype: "Genotype", zygosity: "Zygosity",
      call_confidence: "Call confidence", gene: "Gene", gene_symbol: "Gene",
      hgvsp: "Protein change", clinvar_significance: "ClinVar classification",
      clinvar_review_stars: "ClinVar review stars", clinvar_id: "ClinVar record",
      clinical_grade: "Clinical-grade flag", diplotype: "Diplotype", phenotype: "Phenotype",
      activity_score: "Activity score", copy_number: "Copy number", cpic_level: "CPIC level",
      affected_drugs: "Affected medications", guideline_url: "Recorded guideline",
      trait: "Trait", score_value: "Score", percentile: "Percentile",
      reference_population: "Reference population", training_source: "Training source",
      training_date: "Training date", effect_allele: "Effect allele", effect_size: "Effect size",
      effect_type: "Effect type", p_value: "P value", source: "Source", pubmed_id: "PubMed",
      study_accession: "Study accession", catalog_version: "Catalog version",
      start_pos: "Gene start", end_pos: "Gene end", variant_count: "Recorded variants",
      actionable_count: "Recorded actionable findings"
    };

    const sectionLabels = {
      variants: "Variants", genes: "Genes", pharmacogenomics: "Pharmacogenomics",
      polygenic_scores: "Polygenic scores", gwas: "GWAS associations"
    };

    function formatBytes(bytes) {
      const units = ["B", "KiB", "MiB", "GiB"];
      let value = bytes;
      let index = 0;
      while (value >= 1024 && index < units.length - 1) { value /= 1024; index += 1; }
      return `${value.toFixed(index ? 1 : 0)} ${units[index]}`;
    }

    function formatValue(value) {
      if (Array.isArray(value)) return value.join(", ");
      if (typeof value === "boolean") return value ? "Yes" : "No";
      return String(value).replaceAll("_", " ");
    }

    function titleFor(hit) {
      if (hit.section === "variants") return hit.gene || hit.rsid || hit.variant_id;
      if (hit.section === "pharmacogenomics") return hit.gene_symbol;
      if (hit.section === "genes") return hit.gene_symbol;
      return hit.trait || hit.rsid || "Recorded result";
    }

    function subtitleFor(hit) {
      if (hit.section === "variants") return hit.rsid || hit.variant_id;
      if (hit.section === "pharmacogenomics") return hit.phenotype || "Recorded PGx call";
      if (hit.section === "genes") return `${hit.chrom}:${hit.start_pos}-${hit.end_pos}`;
      return hit.rsid || hit.study_accession || "";
    }

    function cardFor(hit) {
      const card = document.createElement("article");
      card.className = "card";
      const top = document.createElement("div");
      top.className = "card-top";
      const title = document.createElement("h3");
      title.textContent = titleFor(hit);
      const subtitle = document.createElement("div");
      subtitle.className = "card-id";
      subtitle.textContent = subtitleFor(hit);
      top.append(title, subtitle);
      card.append(top);

      const fields = document.createElement("dl");
      fields.className = "fields";
      Object.entries(hit).forEach(([key, value]) => {
        if (key === "section" || value === null || value === "" || key === "gene_symbol" || key === "trait") return;
        const wrapper = document.createElement("div");
        wrapper.className = "field";
        const label = document.createElement("dt");
        label.textContent = fieldLabels[key] || key.replaceAll("_", " ");
        const detail = document.createElement("dd");
        if (typeof value === "string" && value.startsWith("https://")) {
          const link = document.createElement("a");
          link.href = value;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = "Open recorded source";
          detail.append(link);
        } else {
          detail.textContent = formatValue(value);
        }
        wrapper.append(label, detail);
        fields.append(wrapper);
      });
      card.append(fields);
      return card;
    }

    function renderSearch(payload) {
      results.hidden = false;
      const count = payload.hits.length;
      document.querySelector("#results-title").textContent = count ? "Recorded matches" : "Not covered";
      document.querySelector("#result-meta").textContent = `${count} ${count === 1 ? "match" : "matches"} · ${payload.elapsed_seconds.toFixed(3)} seconds`;
      content.replaceChildren();
      if (!count) {
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "This search is not covered by the bundle's recorded fields.";
        content.append(empty);
        return;
      }
      const grouped = Object.groupBy(payload.hits, hit => hit.section);
      Object.entries(grouped).forEach(([sectionName, hits]) => {
        const section = document.createElement("section");
        section.className = `section section-${sectionName}`;
        const heading = document.createElement("div");
        heading.className = "section-title";
        const label = document.createElement("span");
        label.textContent = sectionLabels[sectionName] || sectionName;
        const badge = document.createElement("span");
        badge.className = "count";
        badge.textContent = hits.length;
        heading.append(label, badge);
        const cards = document.createElement("div");
        cards.className = "cards";
        hits.forEach(hit => cards.append(cardFor(hit)));
        section.append(heading, cards);
        content.append(section);
      });
      results.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    async function search(query) {
      button.disabled = true;
      button.innerHTML = '<span class="spinner"></span>Searching';
      try {
        const response = await fetch(`${basePath}/api/search`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query })
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || "Search failed");
        renderSearch(payload);
      } catch (error) {
        results.hidden = false;
        document.querySelector("#results-title").textContent = "Search unavailable";
        document.querySelector("#result-meta").textContent = "";
        content.innerHTML = '<div class="empty error"></div>';
        content.firstElementChild.textContent = error.message;
      } finally {
        button.disabled = false;
        button.textContent = "Search";
      }
    }

    form.addEventListener("submit", event => {
      event.preventDefault();
      const query = input.value.trim();
      if (query) search(query);
    });

    document.querySelectorAll(".example").forEach(example => {
      example.addEventListener("click", () => {
        input.value = example.textContent;
        search(input.value);
      });
    });

    fetch(`${basePath}/api/status`)
      .then(response => response.json())
      .then(status => {
        const cached = status.validation_mode === "cached";
        document.querySelector("#validation").textContent = cached ? "Previously verified" : "Verified";
        document.querySelector("#validation-detail").textContent = cached
          ? `${status.validated_entries} entries · opened in ${status.validation_seconds.toFixed(3)} seconds`
          : `${status.validated_entries} manifest entries in ${status.validation_seconds.toFixed(3)} seconds`;
        document.querySelector("#build").textContent = status.genome_build;
        document.querySelector("#snapshot").textContent = new Date(status.generated_at).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
        document.querySelector("#stored").textContent = formatBytes(status.stored_bytes);
      });
  </script>
</body>
</html>'''
