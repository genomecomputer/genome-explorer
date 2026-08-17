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
      --shadow: 0 18px 60px rgba(25, 54, 43, .10);
    }
    * { box-sizing: border-box; }
    [hidden] { display: none !important; }
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
    button { color: inherit; }
    .shell { width: min(1040px, calc(100% - 40px)); margin: 0 auto; padding: 26px 0 72px; }
    header { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
    .brand { display: flex; align-items: center; gap: 12px; font-weight: 760; letter-spacing: -.02em; }
    .mark {
      width: 34px; height: 34px; border-radius: 10px; display: grid; place-items: center;
      color: white; background: var(--accent); box-shadow: 0 8px 20px rgba(23, 107, 77, .22);
    }
    .mark svg { width: 19px; height: 19px; }
    .header-actions { display: flex; align-items: center; gap: 9px; }
    .privacy {
      display: inline-flex; align-items: center; gap: 8px; padding: 8px 11px;
      color: var(--accent-dark); background: var(--accent-soft); border: 1px solid #cde4d6;
      border-radius: 999px; font-size: 13px; font-weight: 680;
    }
    .privacy-dot { width: 7px; height: 7px; border-radius: 50%; background: #269663; box-shadow: 0 0 0 4px rgba(38,150,99,.10); }
    .quit-button {
      padding: 8px 11px; color: var(--muted); background: rgba(255,255,255,.7);
      border: 1px solid var(--line); border-radius: 999px; font-size: 13px; font-weight: 680; cursor: pointer;
    }
    .quit-button:hover { color: var(--ink); background: var(--surface); }
    .quit-button:disabled { cursor: wait; opacity: .7; }
    main { padding-top: 64px; }
    .eyebrow { margin: 0 0 13px; color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    h1 { max-width: 790px; margin: 0; font-size: clamp(40px, 5.2vw, 62px); line-height: 1.02; letter-spacing: -.052em; }
    .lede { max-width: 690px; margin: 20px 0 0; color: var(--muted); font-size: 18px; line-height: 1.6; }
    .welcome { padding-top: 78px; }
    .welcome h1 { max-width: 720px; }
    .open-card {
      display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 20px;
      margin-top: 36px; padding: 22px; background: rgba(255,255,255,.94); border: 1px solid var(--line);
      border-radius: 18px; box-shadow: var(--shadow);
    }
    .open-icon {
      width: 52px; height: 52px; display: grid; place-items: center; color: var(--accent);
      background: var(--accent-soft); border-radius: 15px;
    }
    .open-icon svg { width: 25px; height: 25px; }
    .open-copy h2 { margin: 0; font-size: 18px; letter-spacing: -.02em; }
    .open-copy p { margin: 6px 0 0; color: var(--muted); font-size: 14px; line-height: 1.5; }
    .choose-button {
      min-height: 48px; padding: 0 19px; color: white; background: var(--accent); border: 0;
      border-radius: 12px; font-weight: 750; cursor: pointer;
    }
    .choose-button:hover { background: var(--accent-dark); }
    .choose-button:disabled { cursor: wait; opacity: .72; }
    .selection-status {
      display: flex; align-items: flex-start; gap: 10px; margin: 13px 0 0; padding: 13px 15px;
      color: #43544c; background: var(--blue-soft); border: 1px solid #d6e5ef; border-radius: 12px;
      font-size: 13px; line-height: 1.5;
    }
    .selection-status.error { color: #812f2f; background: #fff1f0; border-color: #f0d2cf; }
    .status-spinner {
      flex: 0 0 auto; width: 15px; height: 15px; margin-top: 2px;
      border: 2px solid rgba(23,107,77,.2); border-top-color: var(--accent); border-radius: 50%; animation: spin .7s linear infinite;
    }
    .trust-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 22px; }
    .trust-item { padding: 17px; background: rgba(255,255,255,.62); border: 1px solid var(--line); border-radius: 13px; }
    .trust-item strong { display: block; font-size: 14px; }
    .trust-item span { display: block; margin-top: 5px; color: var(--muted); font-size: 12px; line-height: 1.45; }
    .search-panel {
      margin-top: 30px; padding: 10px; background: rgba(255,255,255,.94); border: 1px solid var(--line);
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
    .examples { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    .examples > span { margin-right: 2px; color: var(--muted); font-size: 13px; }
    .example {
      padding: 8px 11px; color: #3d4e46; background: rgba(255,255,255,.75); border: 1px solid var(--line);
      border-radius: 999px; font-size: 13px; cursor: pointer;
    }
    .example:hover { color: var(--accent-dark); border-color: #afcbbd; background: var(--accent-soft); }
    .ways { margin-top: 58px; }
    .ways h2, .results h2 { margin: 0; font-size: 25px; letter-spacing: -.03em; }
    .ways-intro { margin: 9px 0 0; color: var(--muted); line-height: 1.55; }
    .way-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 20px; }
    .way {
      display: flex; flex-direction: column; min-height: 210px; padding: 23px;
      background: rgba(255,255,255,.88); border: 1px solid var(--line); border-radius: 16px;
      box-shadow: 0 6px 24px rgba(25,54,43,.045);
    }
    .way-icon {
      width: 38px; height: 38px; display: grid; place-items: center; margin-bottom: 20px;
      color: var(--accent); background: var(--accent-soft); border-radius: 11px; font-size: 19px;
    }
    .way h3 { margin: 0; font-size: 18px; letter-spacing: -.02em; }
    .way p { margin: 9px 0 20px; color: var(--muted); font-size: 14px; line-height: 1.55; }
    .way .example { align-self: flex-start; margin-top: auto; background: var(--surface); }
    .secondary-tools { display: grid; grid-template-columns: 1.2fr .8fr; gap: 12px; margin-top: 12px; }
    .disclosure {
      background: rgba(255,255,255,.75); border: 1px solid var(--line); border-radius: 14px;
    }
    .disclosure summary {
      display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 17px 19px;
      list-style: none; font-size: 14px; font-weight: 720; cursor: pointer;
    }
    .disclosure summary::-webkit-details-marker { display: none; }
    .disclosure summary::after { content: "+"; color: var(--muted); font-size: 20px; font-weight: 400; }
    .disclosure[open] summary::after { content: "−"; }
    .disclosure-body { padding: 0 19px 19px; color: var(--muted); font-size: 14px; line-height: 1.55; }
    .disclosure-body p { margin: 0 0 13px; }
    .technical-examples { margin: 0; }
    .bundle-summary { color: var(--muted); font-size: 12px; font-weight: 520; }
    .bundle-facts { display: grid; grid-template-columns: 1fr 1fr; gap: 13px 20px; margin: 0; }
    .bundle-fact dt { margin-bottom: 3px; color: var(--muted); font-size: 10px; font-weight: 760; letter-spacing: .07em; text-transform: uppercase; }
    .bundle-fact dd { margin: 0; color: var(--ink); font-size: 13px; font-weight: 650; }
    .results { margin-top: 58px; scroll-margin-top: 28px; }
    .results[hidden] { display: none; }
    .results-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 18px; }
    .result-meta { color: var(--muted); font-size: 13px; }
    .notice {
      display: flex; gap: 10px; align-items: flex-start; margin-bottom: 20px; padding: 13px 15px;
      color: #43544c; background: var(--blue-soft); border: 1px solid #d6e5ef; border-radius: 12px; font-size: 13px; line-height: 1.5;
    }
    .notice svg { flex: 0 0 auto; margin-top: 1px; }
    .section { margin-top: 30px; }
    .section-title { display: flex; align-items: center; gap: 10px; margin-bottom: 11px; color: #35453e; font-size: 13px; font-weight: 790; letter-spacing: .06em; text-transform: uppercase; }
    .count { padding: 3px 7px; color: var(--accent-dark); background: var(--accent-soft); border-radius: 999px; font-size: 11px; }
    .cards { display: grid; gap: 11px; }
    .section-variants .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .result-disclosure {
      overflow: hidden; background: rgba(255,255,255,.75); border: 1px solid var(--line); border-radius: 14px;
    }
    .result-disclosure > summary {
      display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 17px 19px;
      list-style: none; cursor: pointer;
    }
    .result-disclosure > summary::-webkit-details-marker { display: none; }
    .result-disclosure > summary::after { content: "Show"; color: var(--accent); font-size: 12px; font-weight: 750; }
    .result-disclosure[open] > summary::after { content: "Hide"; }
    .result-disclosure .section-title { margin: 0; }
    .result-disclosure > .cards { padding: 0 14px 14px; }
    .more-results { margin-top: 11px; }
    .more-results > summary { color: var(--accent); font-size: 13px; font-weight: 720; }
    .more-results > summary::after { content: "+"; font-size: 18px; font-weight: 450; }
    .more-results[open] > summary::after { content: "−"; }
    .card { padding: 23px; background: var(--surface); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 5px 20px rgba(25,54,43,.045); }
    .record-type { margin-bottom: 8px; color: var(--accent); font-size: 10px; font-weight: 800; letter-spacing: .09em; text-transform: uppercase; }
    .card-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 18px; }
    .card h3 { margin: 0; font-size: 20px; letter-spacing: -.025em; }
    .card-id { padding-top: 3px; color: var(--muted); font-size: 12px; }
    .recorded-summary { margin: 12px 0 0; color: #405048; font-size: 15px; line-height: 1.55; }
    .meaning-note {
      margin: 16px 0 0; padding: 12px 14px; color: #526159; background: var(--soft);
      border-left: 3px solid #a9c9b8; border-radius: 0 10px 10px 0; font-size: 13px; line-height: 1.5;
    }
    .simple-fields { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 15px 22px; margin: 20px 0 0; }
    .field dt { margin-bottom: 5px; color: var(--muted); font-size: 10px; font-weight: 760; letter-spacing: .07em; text-transform: uppercase; }
    .field dd { margin: 0; overflow-wrap: anywhere; font-size: 14px; line-height: 1.45; }
    .field a { color: var(--accent); font-weight: 680; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .source-link { display: inline-flex; margin-top: 18px; color: var(--accent); font-size: 13px; font-weight: 720; text-underline-offset: 3px; }
    .technical-details { margin-top: 19px; padding-top: 16px; border-top: 1px solid var(--line); }
    .technical-details summary { color: var(--muted); font-size: 13px; font-weight: 680; cursor: pointer; }
    .technical-fields { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 15px 20px; margin: 17px 0 0; }
    .empty { padding: 38px; text-align: center; color: var(--muted); background: var(--surface); border: 1px dashed #cbd8d0; border-radius: 14px; }
    .error { color: #812f2f; background: #fff1f0; border-color: #f0d2cf; }
    .spinner { display: inline-block; width: 15px; height: 15px; margin-right: 7px; vertical-align: -2px; border: 2px solid rgba(255,255,255,.4); border-top-color: white; border-radius: 50%; animation: spin .7s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 760px) {
      .shell { width: min(100% - 24px, 1040px); padding-top: 18px; }
      main { padding-top: 48px; }
      .privacy { font-size: 0; }
      .privacy-dot { margin: 3px; }
      .way-grid, .secondary-tools { grid-template-columns: 1fr; }
      .way { min-height: 0; }
      .section-variants .cards { grid-template-columns: 1fr; }
      .technical-fields { grid-template-columns: 1fr 1fr; }
      .open-card { grid-template-columns: auto 1fr; }
      .choose-button { grid-column: 1 / -1; }
      .trust-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 480px) {
      h1 { font-size: 40px; }
      .lede { font-size: 16px; }
      .search-panel { padding: 7px; }
      input[type="search"] { padding: 14px 12px; font-size: 15px; }
      .search-button { padding: 0 13px; font-size: 14px; }
      .simple-fields, .technical-fields, .bundle-facts { grid-template-columns: 1fr; }
      .results-head { align-items: flex-start; flex-direction: column; gap: 5px; }
      .bundle-summary { display: none; }
      .welcome { padding-top: 52px; }
      .open-card { grid-template-columns: 1fr; }
      .open-icon { width: 46px; height: 46px; }
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
      <div class="header-actions">
        <div class="privacy"><span class="privacy-dot"></span>Stays on this computer</div>
        <button class="quit-button" id="quit-button" type="button">Quit</button>
      </div>
    </header>

    <main class="welcome" id="welcome">
      <p class="eyebrow">Welcome to Genome Explorer</p>
      <h1>Explore your genome bundle privately.</h1>
      <p class="lede">Choose a compatible bundle to get started. It stays on this computer and is never uploaded.</p>

      <section class="open-card" aria-labelledby="open-title">
        <div class="open-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7.5h5l1.6 2H20v8.5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7.5Z"/><path d="M4 8V6a2 2 0 0 1 2-2h3l1.6 2H18a2 2 0 0 1 2 2v1.5"/></svg>
        </div>
        <div class="open-copy">
          <h2 id="open-title">Open a genome bundle</h2>
          <p>Select a compatible genome bundle from this computer. The original file will not be changed.</p>
        </div>
        <button class="choose-button" id="choose-button" type="button">Choose genome bundle</button>
      </section>

      <div class="selection-status" id="selection-status" hidden aria-live="polite">
        <span class="status-spinner" id="status-spinner" aria-hidden="true"></span>
        <span id="selection-message"></span>
      </div>

      <div class="trust-grid" aria-label="Privacy information">
        <div class="trust-item"><strong>Stays local</strong><span>The bundle is read only on this computer.</span></div>
        <div class="trust-item"><strong>No account or AI</strong><span>No sign-in, API key, or AI connection is required.</span></div>
        <div class="trust-item"><strong>No upload</strong><span>The browser never copies the bundle, and the app does not send it over the network.</span></div>
      </div>
    </main>

    <main id="explorer" hidden>
      <p class="eyebrow">Your genome bundle is ready</p>
      <h1>What would you like to explore?</h1>
      <p class="lede">Search a medication, trait, condition, or gene. Genome Explorer only shows information already recorded in this bundle.</p>

      <div class="search-panel">
        <form id="search-form">
          <input id="search-input" type="search" aria-label="Search your genome bundle" autocomplete="off" spellcheck="false" placeholder="Try a medication, trait, condition, or gene" autofocus>
          <button class="search-button" id="search-button" type="submit">Search</button>
        </form>
      </div>
      <div class="examples" aria-label="Example searches">
        <span>Try an example</span>
        <button class="example" type="button" data-query="clopidogrel">Clopidogrel</button>
        <button class="example" type="button" data-query="extraversion">Extraversion</button>
        <button class="example" type="button" data-query="pcos">PCOS</button>
      </div>

      <section class="ways" aria-labelledby="ways-title">
        <h2 id="ways-title">Ways to explore</h2>
        <p class="ways-intro">Start with something familiar. You can move into the technical details only when you want them.</p>
        <div class="way-grid">
          <article class="way">
            <div class="way-icon" aria-hidden="true">Rx</div>
            <h3>Medication records</h3>
            <p>Search a medication to see what this bundle records about it.</p>
            <button class="example" type="button" data-query="clopidogrel">Try Clopidogrel</button>
          </article>
          <article class="way">
            <div class="way-icon" aria-hidden="true">%</div>
            <h3>Traits and conditions</h3>
            <p>Search a familiar term to see what this bundle records about it.</p>
            <button class="example" type="button" data-query="extraversion">Try Extraversion</button>
          </article>
        </div>

        <div class="secondary-tools">
          <details class="disclosure">
            <summary>Looking for a specific gene or variant?</summary>
            <div class="disclosure-body">
              <p>You can search a gene name, rsID, or genomic position when you know the exact identifier.</p>
              <div class="examples technical-examples">
                <button class="example" type="button" data-query="CYP2C19">CYP2C19</button>
                <button class="example" type="button" data-query="rs11188082">rs11188082</button>
                <button class="example" type="button" data-query="chr10:94808278">chr10:94808278</button>
              </div>
            </div>
          </details>

          <details class="disclosure" id="bundle-details">
            <summary><span>Bundle details</span><span class="bundle-summary" id="bundle-summary">Verified and ready</span></summary>
            <div class="disclosure-body">
              <dl class="bundle-facts">
                <div class="bundle-fact"><dt>Status</dt><dd id="validation">Verified</dd></div>
                <div class="bundle-fact"><dt>Genome reference</dt><dd id="build">Loading</dd></div>
                <div class="bundle-fact"><dt>Bundle date</dt><dd id="snapshot">Loading</dd></div>
                <div class="bundle-fact"><dt>Local data</dt><dd id="stored">Loading</dd></div>
              </dl>
            </div>
          </details>
        </div>
      </section>

      <section class="results" id="results" hidden aria-live="polite">
        <div class="results-head">
          <h2 id="results-title">What the bundle records</h2>
          <div class="result-meta" id="result-meta"></div>
        </div>
        <div class="notice">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>
          <span>These are records from the bundle, not a diagnosis or treatment recommendation.</span>
        </div>
        <div id="result-content"></div>
      </section>
    </main>
  </div>

  <script nonce="__NONCE__">
    const basePath = "__BASE_PATH__";
    const welcome = document.querySelector("#welcome");
    const explorer = document.querySelector("#explorer");
    const chooseButton = document.querySelector("#choose-button");
    const selectionStatus = document.querySelector("#selection-status");
    const selectionMessage = document.querySelector("#selection-message");
    const statusSpinner = document.querySelector("#status-spinner");
    const form = document.querySelector("#search-form");
    const input = document.querySelector("#search-input");
    const button = document.querySelector("#search-button");
    const results = document.querySelector("#results");
    const content = document.querySelector("#result-content");
    const quitButton = document.querySelector("#quit-button");
    let statusTimer = null;
    let explorerReady = false;

    const fieldLabels = {
      variant_id: "Variant identifier", rsid: "rsID", chrom: "Chromosome", pos: "Position",
      ref: "Reference allele", alt: "Alternate allele", genotype: "Genotype", zygosity: "Zygosity",
      call_confidence: "Call confidence", gene: "Gene annotation", gene_symbol: "Gene",
      hgvsp: "Protein change", clinvar_significance: "ClinVar classification",
      clinvar_review_stars: "ClinVar review stars", clinvar_id: "ClinVar record",
      clinical_grade: "Clinical-grade flag", diplotype: "Diplotype", phenotype: "Recorded result",
      activity_score: "Activity score", copy_number: "Copy number", cpic_level: "Evidence level",
      affected_drugs: "Related medications", guideline_url: "Recorded guideline",
      trait: "Trait", score_value: "Recorded score", percentile: "Recorded percentile",
      reference_population: "Comparison group recorded in bundle", training_source: "Training source",
      training_date: "Training date", effect_allele: "Effect allele", effect_size: "Effect size",
      effect_type: "Effect type", p_value: "P value", source: "Recorded source", pubmed_id: "PubMed",
      study_accession: "Study accession", catalog_version: "Catalog version",
      start_pos: "Gene start", end_pos: "Gene end", variant_count: "Variants recorded",
      actionable_count: "Actionable records"
    };

    const sectionLabels = {
      variants: "Your recorded variants", genes: "Records for this gene",
      pharmacogenomics: "Medication-related records", polygenic_scores: "Traits and scores",
      gwas: "Research associations"
    };

    const recordLabels = {
      variants: "Personal variant record", genes: "Personal gene summary",
      pharmacogenomics: "Medication-related record", polygenic_scores: "Recorded score",
      gwas: "Research association"
    };

    const primaryFields = {
      variants: ["zygosity", "call_confidence"],
      genes: ["variant_count", "actionable_count"],
      pharmacogenomics: ["phenotype", "cpic_level"],
      polygenic_scores: ["percentile", "reference_population"],
      gwas: ["gene", "source"]
    };

    function formatBytes(bytes) {
      const units = ["B", "KiB", "MiB", "GiB"];
      let value = bytes;
      let index = 0;
      while (value >= 1024 && index < units.length - 1) { value /= 1024; index += 1; }
      return `${value.toFixed(index ? 1 : 0)} ${units[index]}`;
    }

    function showSelectionStatus(message, { busy = false, error = false } = {}) {
      selectionStatus.hidden = !message;
      selectionStatus.classList.toggle("error", error);
      statusSpinner.hidden = !busy;
      selectionMessage.textContent = message;
    }

    function populateBundleStatus(status) {
      const cached = status.validation_mode === "cached";
      document.querySelector("#validation").textContent = cached ? "Previously verified" : "Verified";
      document.querySelector("#build").textContent = status.genome_build;
      document.querySelector("#snapshot").textContent = new Date(status.generated_at).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
      document.querySelector("#stored").textContent = formatBytes(status.stored_bytes);
      document.querySelector("#bundle-summary").textContent = cached ? "Previously verified and ready" : "Verified and ready";
    }

    function renderAppStatus(status) {
      if (status.status === "ready") {
        welcome.hidden = true;
        explorer.hidden = false;
        chooseButton.disabled = false;
        populateBundleStatus(status);
        if (!explorerReady) {
          explorerReady = true;
          input.focus();
        }
        return;
      }

      welcome.hidden = false;
      explorer.hidden = true;
      explorerReady = false;
      if (status.status === "choosing") {
        chooseButton.disabled = true;
        chooseButton.textContent = "Waiting for selection";
        showSelectionStatus("Choose a genome bundle in the file window that just opened.", { busy: true });
      } else if (status.status === "validating") {
        chooseButton.disabled = true;
        chooseButton.textContent = "Verifying bundle";
        const name = status.archive_name || "your bundle";
        showSelectionStatus(`Verifying ${name} locally. Large bundles may take a few minutes.`, { busy: true });
      } else if (status.status === "failed") {
        chooseButton.disabled = false;
        chooseButton.textContent = "Choose another bundle";
        showSelectionStatus(status.error || "This bundle could not be opened.", { error: true });
      } else {
        chooseButton.disabled = false;
        chooseButton.textContent = "Choose genome bundle";
        showSelectionStatus("");
      }
    }

    function scheduleStatusPoll(delay = 350) {
      window.clearTimeout(statusTimer);
      statusTimer = window.setTimeout(refreshStatus, delay);
    }

    async function refreshStatus() {
      try {
        const response = await fetch(`${basePath}/api/status`);
        const status = await response.json();
        renderAppStatus(status);
        if (status.status === "choosing" || status.status === "validating") scheduleStatusPoll();
      } catch (error) {
        welcome.hidden = false;
        explorer.hidden = true;
        chooseButton.disabled = false;
        chooseButton.textContent = "Try again";
        showSelectionStatus("Genome Explorer could not check the local bundle status.", { error: true });
      }
    }

    function formatValue(value) {
      if (Array.isArray(value)) return value.join(", ");
      if (typeof value === "boolean") return value ? "Yes" : "No";
      return String(value).replaceAll("_", " ");
    }

    function capitalize(value) {
      return value ? value.charAt(0).toUpperCase() + value.slice(1) : value;
    }

    function matchingMedication(hit, query) {
      if (!Array.isArray(hit.affected_drugs)) return "";
      const normalized = query.toLowerCase();
      return hit.affected_drugs.find(drug => drug.toLowerCase().includes(normalized)) || "";
    }

    function titleFor(hit, query) {
      if (hit.section === "pharmacogenomics") {
        return capitalize(matchingMedication(hit, query)) || hit.gene_symbol;
      }
      if (hit.section === "variants") return hit.gene || hit.rsid || "Recorded variant";
      if (hit.section === "genes") return hit.gene_symbol;
      return hit.trait || hit.rsid || "Recorded result";
    }

    function subtitleFor(hit) {
      if (hit.section === "pharmacogenomics") return `Related gene: ${hit.gene_symbol}`;
      if (hit.section === "variants") return hit.rsid ? `Identifier: ${hit.rsid}` : "";
      if (hit.section === "genes") return "Personal variant records found";
      if (hit.section === "gwas") {
        const identifier = hit.rsid || hit.variant_id;
        return identifier ? `Variant in your bundle: ${identifier}` : "";
      }
      return hit.rsid ? `Identifier: ${hit.rsid}` : "";
    }

    function summaryFor(hit) {
      if (hit.section === "pharmacogenomics") {
        return hit.phenotype
          ? `The bundle records “${formatValue(hit.phenotype)}” for ${hit.gene_symbol}.`
          : `The bundle contains a medication-related record for ${hit.gene_symbol}.`;
      }
      if (hit.section === "polygenic_scores") return `The bundle contains a recorded score for ${hit.trait}.`;
      if (hit.section === "gwas") {
        const identifier = hit.rsid || hit.variant_id || "this variant";
        return `Your bundle records ${identifier}. The research source associates this variant with ${hit.trait}.`;
      }
      if (hit.section === "genes") {
        return `Your bundle contains ${formatValue(hit.variant_count)} personal variant records assigned to ${hit.gene_symbol}.`;
      }
      return hit.gene
        ? `Your bundle contains a personal variant record annotated to ${hit.gene}.`
        : "Your bundle contains this personal variant record.";
    }

    function meaningFor(hit) {
      if (hit.section === "genes") {
        return "This shows that the bundle has personal variant records for this gene. It is not a test of whether the gene itself is present or absent.";
      }
      if (hit.section === "gwas" && hit.gene) {
        return `${hit.gene} is named by the research source. This is research context, not a result saying that you have or do not have that gene.`;
      }
      return "";
    }

    function fieldLabelFor(section, key) {
      if (section === "gwas" && key === "gene") return "Gene named by research";
      if (section === "variants" && key === "gene") return "Gene annotation";
      return fieldLabels[key] || key.replaceAll("_", " ");
    }

    function fieldElement(key, value, section) {
      const wrapper = document.createElement("div");
      wrapper.className = "field";
      const label = document.createElement("dt");
      label.textContent = fieldLabelFor(section, key);
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
      return wrapper;
    }

    function cardFor(hit, query) {
      const card = document.createElement("article");
      card.className = "card";

      const type = document.createElement("div");
      type.className = "record-type";
      type.textContent = recordLabels[hit.section] || "Bundle record";
      card.append(type);

      const top = document.createElement("div");
      top.className = "card-top";
      const title = document.createElement("h3");
      title.textContent = titleFor(hit, query);
      const subtitle = document.createElement("div");
      subtitle.className = "card-id";
      subtitle.textContent = subtitleFor(hit);
      top.append(title, subtitle);
      card.append(top);

      const summary = document.createElement("p");
      summary.className = "recorded-summary";
      summary.textContent = summaryFor(hit);
      card.append(summary);

      const meaning = meaningFor(hit);
      if (meaning) {
        const note = document.createElement("p");
        note.className = "meaning-note";
        note.textContent = meaning;
        card.append(note);
      }

      const simple = document.createElement("dl");
      simple.className = "simple-fields";
      (primaryFields[hit.section] || []).forEach(key => {
        const value = hit[key];
        if (value !== null && value !== undefined && value !== "") simple.append(fieldElement(key, value, hit.section));
      });
      if (simple.children.length) card.append(simple);

      if (typeof hit.guideline_url === "string" && hit.guideline_url.startsWith("https://")) {
        const source = document.createElement("a");
        source.className = "source-link";
        source.href = hit.guideline_url;
        source.target = "_blank";
        source.rel = "noopener noreferrer";
        source.textContent = "View recorded guideline";
        card.append(source);
      }

      const technical = document.createElement("details");
      technical.className = "technical-details";
      const technicalSummary = document.createElement("summary");
      technicalSummary.textContent = "Technical details";
      const fields = document.createElement("dl");
      fields.className = "technical-fields";
      Object.entries(hit).forEach(([key, value]) => {
        if (key === "section" || value === null || value === undefined || value === "") return;
        fields.append(fieldElement(key, value, hit.section));
      });
      technical.append(technicalSummary, fields);
      card.append(technical);
      return card;
    }

    function sectionHeading(sectionName, count) {
      const heading = document.createElement("div");
      heading.className = "section-title";
      const label = document.createElement("span");
      label.textContent = sectionLabels[sectionName] || sectionName;
      const badge = document.createElement("span");
      badge.className = "count";
      badge.textContent = count;
      heading.append(label, badge);
      return heading;
    }

    function cardsFor(hits, query) {
      const cards = document.createElement("div");
      cards.className = "cards";
      hits.forEach(hit => cards.append(cardFor(hit, query)));
      return cards;
    }

    function renderSearch(payload) {
      results.hidden = false;
      const count = payload.hits.length;
      document.querySelector("#results-title").textContent = count ? "What the bundle records" : "Not covered";
      document.querySelector("#result-meta").textContent = `${count} recorded ${count === 1 ? "match" : "matches"}`;
      content.replaceChildren();
      if (!count) {
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = "This search is not covered by the bundle's recorded fields.";
        content.append(empty);
        results.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      const grouped = Object.groupBy(payload.hits, hit => hit.section);
      const sectionOrder = ["pharmacogenomics", "polygenic_scores", "genes", "variants", "gwas"];
      const hasClearerRecord = Boolean(grouped.pharmacogenomics?.length || grouped.polygenic_scores?.length);
      sectionOrder.filter(sectionName => grouped[sectionName]?.length).forEach(sectionName => {
        const hits = grouped[sectionName];
        const section = document.createElement("section");
        section.className = `section section-${sectionName}`;
        const isSecondary = hasClearerRecord && (sectionName === "variants" || sectionName === "gwas");
        if (isSecondary) {
          const disclosure = document.createElement("details");
          disclosure.className = "result-disclosure";
          const summary = document.createElement("summary");
          summary.append(sectionHeading(sectionName, hits.length));
          disclosure.append(summary, cardsFor(hits, payload.query));
          section.append(disclosure);
        } else {
          const visibleHits = hits.slice(0, sectionName === "pharmacogenomics" ? hits.length : 4);
          section.append(sectionHeading(sectionName, hits.length), cardsFor(visibleHits, payload.query));
          if (visibleHits.length < hits.length) {
            const more = document.createElement("details");
            more.className = "result-disclosure more-results";
            const summary = document.createElement("summary");
            summary.textContent = `Show ${hits.length - visibleHits.length} more recorded matches`;
            more.append(summary, cardsFor(hits.slice(visibleHits.length), payload.query));
            section.append(more);
          }
        }
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
        input.value = example.dataset.query || example.textContent;
        search(input.value);
      });
    });

    chooseButton.addEventListener("click", async () => {
      chooseButton.disabled = true;
      chooseButton.textContent = "Opening file selector";
      showSelectionStatus("Opening the local file selector.", { busy: true });
      try {
        const response = await fetch(`${basePath}/api/select`, { method: "POST" });
        const status = await response.json();
        renderAppStatus(status);
        if (status.status === "choosing" || status.status === "validating") scheduleStatusPoll(150);
      } catch (error) {
        chooseButton.disabled = false;
        chooseButton.textContent = "Try again";
        showSelectionStatus("The local file selector could not be opened.", { error: true });
      }
    });

    quitButton.addEventListener("click", async () => {
      window.clearTimeout(statusTimer);
      quitButton.disabled = true;
      quitButton.textContent = "Stopping";
      try {
        await fetch(`${basePath}/api/shutdown`, { method: "POST" });
      } finally {
        document.body.innerHTML = '<main class="shell"><p class="eyebrow">Genome Explorer stopped</p><h1>Your local session has ended.</h1><p class="lede">You can close this tab. Your source bundle was not modified.</p></main>';
      }
    });

    refreshStatus();
  </script>
</body>
</html>'''
