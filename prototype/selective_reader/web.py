# The topic library is a compact directory. It separates person-specific bundle
# fields from research context and never derives a new health interpretation.
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
    .bundle-library { margin-top: 36px; }
    .library-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 13px; }
    .library-head h2 { margin: 0; font-size: 22px; letter-spacing: -.03em; }
    .library-head p { margin: 0; color: var(--muted); font-size: 13px; }
    .bundle-list { display: grid; gap: 10px; }
    .bundle-item {
      display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 15px;
      padding: 17px; background: rgba(255,255,255,.92); border: 1px solid var(--line); border-radius: 15px;
      box-shadow: 0 5px 20px rgba(25,54,43,.04);
    }
    .bundle-avatar {
      width: 42px; height: 42px; display: grid; place-items: center; color: var(--accent-dark);
      background: var(--accent-soft); border-radius: 12px; font-size: 15px; font-weight: 820; text-transform: uppercase;
    }
    .bundle-name { margin: 0; font-size: 17px; letter-spacing: -.015em; }
    .bundle-meta { margin: 5px 0 0; color: var(--muted); font-size: 12px; line-height: 1.45; overflow-wrap: anywhere; }
    .bundle-unavailable { color: #8a3d36; }
    .bundle-actions { display: flex; align-items: center; gap: 8px; }
    .secondary-button, .text-button {
      min-height: 38px; padding: 0 13px; border-radius: 10px; font-size: 13px; font-weight: 720; cursor: pointer;
    }
    .secondary-button { color: white; background: var(--accent); border: 1px solid var(--accent); }
    .secondary-button:hover { background: var(--accent-dark); }
    .text-button { color: var(--accent-dark); background: transparent; border: 1px solid var(--line); }
    .text-button:hover { background: var(--soft); }
    .secondary-button:disabled, .text-button:disabled { cursor: not-allowed; opacity: .5; }
    .nickname-form { display: flex; align-items: center; gap: 8px; margin-top: 9px; }
    .nickname-input {
      width: min(320px, 100%); min-height: 38px; padding: 8px 10px; color: var(--ink); background: white;
      border: 1px solid #b9cbc1; border-radius: 9px; outline: none;
    }
    .nickname-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(23,107,77,.10); }
    .nickname-error { margin: 7px 0 0; color: #8a3d36; font-size: 12px; }
    .bundle-library:not([hidden]) + .selection-status { margin-top: 13px; }
    .bundle-library:not([hidden]) ~ .open-card { margin-top: 18px; box-shadow: none; }
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
    .featured-searches { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    .featured-searches > span { margin-right: 2px; color: var(--muted); font-size: 13px; }
    .featured-search {
      padding: 8px 11px; color: #3d4e46; background: rgba(255,255,255,.75); border: 1px solid var(--line);
      border-radius: 999px; font-size: 13px; cursor: pointer;
    }
    .featured-search:hover { color: var(--accent-dark); border-color: #afcbbd; background: var(--accent-soft); }
    .examples { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
    .examples > span { margin-right: 2px; color: var(--muted); font-size: 13px; }
    .example {
      padding: 8px 11px; color: #3d4e46; background: rgba(255,255,255,.75); border: 1px solid var(--line);
      border-radius: 999px; font-size: 13px; cursor: pointer;
    }
    .example:hover { color: var(--accent-dark); border-color: #afcbbd; background: var(--accent-soft); }
    .topic-library { margin-top: 58px; }
    .topic-library h2, .results h2 { margin: 0; font-size: 25px; letter-spacing: -.03em; }
    .topic-library-head { display: flex; align-items: end; justify-content: space-between; gap: 24px; }
    .topic-summary { flex: 0 0 auto; padding-bottom: 3px; color: var(--muted); font-size: 13px; }
    .topic-catalog { margin-top: 20px; }
    .topic-indicator { min-width: 0; text-align: right; }
    .topic-indicator-value { display: block; color: var(--accent-dark); font-size: 12px; font-weight: 780; }
    .topic-indicator.related .topic-indicator-value { color: #37566d; }
    .topic-indicator.no-data .topic-indicator-value { color: var(--muted); font-weight: 680; }
    .topic-browser {
      display: grid; grid-template-columns: 210px minmax(0, 1fr); overflow: hidden;
      background: rgba(255,255,255,.86); border: 1px solid var(--line); border-radius: 16px;
      box-shadow: 0 7px 26px rgba(25,54,43,.045);
    }
    .directory-main { min-width: 0; padding: 20px; }
    .directory-toolbar { display: grid; grid-template-columns: minmax(0, 1fr) minmax(190px, 260px); align-items: end; gap: 18px; margin-bottom: 20px; }
    .directory-title { margin: 0; font-size: 19px; letter-spacing: -.025em; }
    input.directory-filter {
      min-height: 43px; padding: 10px 13px; color: var(--ink); background: white; border: 1px solid var(--line);
      border-radius: 11px; outline: none;
    }
    input.directory-filter:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(23,107,77,.1); }
    .directory-groups { display: grid; gap: 20px; }
    .directory-group-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin: 0 2px 8px; }
    .directory-group-head h4 { margin: 0; color: #48584f; font-size: 11px; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; }
    .directory-group-count { color: var(--muted); font-size: 10px; }
    .directory-list { overflow: hidden; border: 1px solid var(--line); border-radius: 11px; }
    .directory-row {
      display: grid; grid-template-columns: minmax(170px, 1fr) minmax(220px, auto) 22px;
      align-items: center; gap: 14px; width: 100%; padding: 13px 15px; color: inherit; background: transparent;
      border: 0; border-bottom: 1px solid var(--line); text-align: left; cursor: pointer;
    }
    .directory-row:last-child { border-bottom: 0; }
    .directory-row:hover { background: var(--soft); }
    .directory-name { font-size: 14px; font-weight: 730; }
    .directory-arrow { color: var(--accent); text-align: right; }
    .directory-empty { padding: 34px 24px; color: var(--muted); text-align: center; border: 1px dashed #cbd8d0; border-radius: 11px; }
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
    .section-variants .cards, .section-trait_variants .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .record-list { overflow: hidden; background: var(--surface); border: 1px solid var(--line); border-radius: 13px; }
    .record-list-head, .record-row-summary {
      display: grid; align-items: center; gap: 14px; padding: 0 15px;
    }
    .record-layout-trait_variants .record-list-head, .record-layout-trait_variants .record-row-summary {
      grid-template-columns: minmax(100px, .85fr) minmax(82px, .65fr) minmax(90px, .8fr) minmax(210px, 1.7fr) minmax(90px, .72fr) 14px;
    }
    .record-layout-variants .record-list-head, .record-layout-variants .record-row-summary {
      grid-template-columns: minmax(130px, 1.2fr) minmax(90px, .7fr) minmax(100px, .9fr) minmax(105px, .75fr) 14px;
    }
    .record-layout-gwas .record-list-head, .record-layout-gwas .record-row-summary {
      grid-template-columns: minmax(220px, 1.8fr) minmax(110px, .75fr) minmax(120px, 1fr) minmax(105px, .72fr) 14px;
    }
    .record-list-head {
      min-height: 39px; color: var(--muted); background: var(--soft); border-bottom: 1px solid var(--line);
      font-size: 9px; font-weight: 800; letter-spacing: .07em; text-transform: uppercase;
    }
    .record-row { border-bottom: 1px solid var(--line); }
    .record-row:last-child { border-bottom: 0; }
    .record-row-summary {
      min-height: 54px; padding-top: 9px; padding-bottom: 9px; list-style: none; cursor: pointer;
    }
    .record-row-summary::-webkit-details-marker { display: none; }
    .record-row-summary:hover { background: var(--soft); }
    .record-row[open] > .record-row-summary { background: #f4f8f5; border-bottom: 1px solid var(--line); }
    .record-row-cell { min-width: 0; color: #495950; font-size: 12px; line-height: 1.35; overflow-wrap: anywhere; }
    .record-row-value { display: -webkit-box; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }
    .record-row-primary { color: var(--ink); font-size: 13px; font-weight: 760; }
    .record-row-primary .record-row-value { -webkit-line-clamp: 1; }
    .record-row-arrow { color: var(--accent); font-size: 17px; text-align: center; transition: transform .15s ease; }
    .record-row[open] .record-row-arrow { transform: rotate(90deg); }
    .record-row-details { padding: 16px 15px 18px; background: rgba(247,250,248,.72); }
    .record-row-fields { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px 20px; margin: 0; }
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
    .result-disclosure > .paginated-results { padding: 0 14px 14px; }
    .result-pagination {
      display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-top: 12px;
      padding-top: 12px; border-top: 1px solid var(--line);
    }
    .pagination-range { color: var(--muted); font-size: 12px; }
    .pagination-actions { display: flex; gap: 7px; }
    .pagination-button {
      min-height: 36px; padding: 0 12px; color: var(--accent-dark); background: var(--surface);
      border: 1px solid var(--line); border-radius: 9px; font-size: 12px; font-weight: 720; cursor: pointer;
    }
    .pagination-button:hover:not(:disabled) { border-color: #a9c9b8; background: var(--accent-soft); }
    .pagination-button:disabled { color: #9ba8a1; cursor: default; opacity: .7; }
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
    .personal-data {
      margin-top: 20px; padding: 18px; background: var(--accent-soft); border: 1px solid #cde4d6; border-radius: 13px;
    }
    .data-group-label { margin: 0; color: var(--accent-dark); font-size: 10px; font-weight: 820; letter-spacing: .09em; text-transform: uppercase; }
    .data-group-copy { margin: 7px 0 0; color: #405048; font-size: 13px; line-height: 1.5; }
    .personal-data .simple-fields { margin-top: 16px; }
    .reference-context { margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--line); }
    .reference-context .data-group-label { color: var(--muted); }
    .reference-context .simple-fields { margin-top: 15px; }
    .simple-fields { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 15px 22px; margin: 20px 0 0; }
    .field dt { margin-bottom: 5px; color: var(--muted); font-size: 10px; font-weight: 760; letter-spacing: .07em; text-transform: uppercase; }
    .field dd { margin: 0; overflow-wrap: anywhere; font-size: 14px; line-height: 1.45; }
    .field a { color: var(--accent); font-weight: 680; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    .reference-links { display: flex; flex-wrap: wrap; gap: 5px 12px; }
    .source-link { display: inline-flex; margin-top: 18px; color: var(--accent); font-size: 13px; font-weight: 720; text-underline-offset: 3px; }
    .clinical-conflict { margin-top: 16px; padding: 10px 12px; color: #714d12; background: #fff7e7; border: 1px solid #efd9ad; border-radius: 10px; font-size: 13px; font-weight: 680; }
    .clinical-sources { display: grid; gap: 8px; margin-top: 19px; padding-top: 16px; border-top: 1px solid var(--line); }
    .clinical-source { display: flex; align-items: baseline; flex-wrap: wrap; gap: 5px 10px; font-size: 12px; }
    .clinical-source .source-link { margin-top: 0; }
    .clinical-source strong { font-size: 13px; }
    .clinical-source span { color: var(--muted); }
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
      .way-grid, .secondary-tools { grid-template-columns: 1fr; }
      .way { min-height: 0; }
      .topic-library-head { align-items: flex-start; flex-direction: column; gap: 8px; }
      .topic-browser { grid-template-columns: 1fr; }
      .directory-toolbar { grid-template-columns: 1fr; }
      .section-variants .cards, .section-trait_variants .cards { grid-template-columns: 1fr; }
      .record-list-head { display: none; }
      .record-row-summary, .record-layout-trait_variants .record-row-summary,
      .record-layout-variants .record-row-summary, .record-layout-gwas .record-row-summary {
        grid-template-columns: minmax(0, 1fr) auto; gap: 7px 14px; padding-top: 13px; padding-bottom: 13px;
      }
      .record-row-cell { grid-column: 1; display: grid; grid-template-columns: 105px minmax(0, 1fr); gap: 10px; }
      .record-row-cell::before {
        content: attr(data-label); color: var(--muted); font-size: 9px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase;
      }
      .record-row-primary { display: block; font-size: 14px; }
      .record-row-primary::before { content: none; }
      .record-row-arrow { grid-column: 2; grid-row: 1; }
      .record-row-fields { grid-template-columns: 1fr 1fr; }
      .technical-fields { grid-template-columns: 1fr 1fr; }
      .open-card { grid-template-columns: auto 1fr; }
      .choose-button { grid-column: 1 / -1; }
      .trust-grid { grid-template-columns: 1fr; }
      .bundle-item { grid-template-columns: auto minmax(0, 1fr); }
      .bundle-actions { grid-column: 1 / -1; justify-content: flex-end; }
    }
    @media (max-width: 480px) {
      h1 { font-size: 40px; }
      .lede { font-size: 16px; }
      .search-panel { padding: 7px; }
      input[type="search"] { padding: 14px 12px; font-size: 15px; }
      .search-button { padding: 0 13px; font-size: 14px; }
      .simple-fields, .technical-fields, .record-row-fields { grid-template-columns: 1fr; }
      .record-row-cell { grid-template-columns: 90px minmax(0, 1fr); }
      .results-head { align-items: flex-start; flex-direction: column; gap: 5px; }
      .welcome { padding-top: 52px; }
      .open-card { grid-template-columns: 1fr; }
      .open-icon { width: 46px; height: 46px; }
      .library-head { align-items: flex-start; flex-direction: column; gap: 5px; }
      .bundle-item { grid-template-columns: 1fr; }
      .bundle-avatar { width: 38px; height: 38px; }
      .bundle-actions { grid-column: auto; justify-content: stretch; }
      .bundle-actions button { flex: 1; }
      .nickname-form { align-items: stretch; flex-direction: column; }
      .nickname-input { width: 100%; }
      .directory-row { grid-template-columns: minmax(0, 1fr) 22px; gap: 8px; }
      .directory-row .topic-indicator { grid-column: 1 / -1; grid-row: 2; text-align: left; }
      .directory-arrow { grid-column: 2; grid-row: 1; }
    }

    /* Workbench layout. */
    body { background: #edf3ef; }
    .shell {
      display: grid; grid-template-columns: 236px minmax(0, 1fr); width: 100%; min-height: 100vh; margin: 0; padding: 0;
    }
    header {
      position: sticky; top: 0; align-self: start; display: flex; flex-direction: column; align-items: stretch;
      justify-content: flex-start; height: 100vh; padding: 25px 18px 22px; color: white; background: #123d2e;
    }
    .brand { align-items: flex-start; line-height: 1.15; }
    .mark { flex: 0 0 auto; color: #123d2e; background: #dceee4; border-radius: 5px; box-shadow: none; }
    .sidebar-context { display: flex; min-height: 0; flex: 1; flex-direction: column; margin-top: 38px; }
    .sidebar-bundle { margin-top: auto; padding: 18px 9px 0; border-top: 1px solid rgba(255,255,255,.14); }
    .sidebar-label {
      margin: 0 0 9px; color: #91b6a5; font-size: 9px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase;
    }
    .sidebar-bundle-name { display: block; color: white; font-size: 15px; font-weight: 760; line-height: 1.3; overflow-wrap: anywhere; }
    .sidebar-bundle-status { display: block; margin-top: 7px; color: #a9d3bf; font-size: 10px; font-weight: 720; }
    .sidebar-bundle-meta { display: block; margin-top: 6px; color: #b9d2c6; font-size: 11px; line-height: 1.45; }
    .sidebar-nav { display: grid; gap: 3px; margin-top: 23px; }
    .sidebar-view-list { display: grid; gap: 3px; }
    .sidebar-nav .sidebar-label { margin: 0 9px 7px; }
    .sidebar-nav-button {
      display: grid; grid-template-columns: 22px minmax(0, 1fr) auto; align-items: center; gap: 7px; width: 100%;
      min-height: 38px; padding: 0 9px; color: #c9ddd3; background: transparent; border: 0; border-radius: 5px;
      font-size: 12px; font-weight: 680; text-align: left; cursor: pointer;
    }
    .sidebar-nav-button:hover { color: white; background: rgba(255,255,255,.08); }
    .sidebar-nav-button[aria-selected="true"], .sidebar-nav-button.is-active { color: #123d2e; background: #dceee4; }
    .sidebar-nav-index { color: #7ea994; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 9px; }
    .sidebar-nav-button[aria-selected="true"] .sidebar-nav-index, .sidebar-nav-button.is-active .sidebar-nav-index { color: #4a7863; }
    .sidebar-nav-count { color: #91b6a5; font-size: 9px; font-weight: 760; }
    .sidebar-nav-button[aria-selected="true"] .sidebar-nav-count, .sidebar-nav-button.is-active .sidebar-nav-count { color: #4a7863; }
    .header-actions { align-items: stretch; flex-direction: column; width: 100%; margin-top: 13px; }
    .quit-button {
      width: 100%; color: #e3eee8; background: rgba(255,255,255,.06); border-color: rgba(255,255,255,.17); border-radius: 6px;
    }
    .quit-button:hover { color: white; background: rgba(255,255,255,.12); }
    main { grid-column: 2; width: min(1080px, calc(100% - 64px)); margin: 0 auto; padding: 44px 0 72px; }
    .welcome { padding-top: 74px; }
    #explorer h1 { max-width: none; font-size: clamp(34px, 4vw, 48px); letter-spacing: -.045em; }
    #explorer .lede { margin-top: 9px; font-size: 15px; }
    #explorer .eyebrow { margin-bottom: 9px; }
    .workspace-view.topic-library, .workspace-view.results { margin-top: 0; }
    #explorer .topic-library h1 { font-size: clamp(34px, 4vw, 44px); }
    #explorer .results h1 { font-size: clamp(30px, 3.2vw, 40px); }
    .workspace-back {
      margin: 0 0 23px; padding: 0; color: var(--accent-dark); background: transparent; border: 0;
      font-size: 13px; font-weight: 740; cursor: pointer;
    }
    .workspace-back:hover { text-decoration: underline; text-underline-offset: 3px; }
    .search-panel {
      margin-top: 23px; padding: 6px; background: white; border-color: #cbd9d1; border-radius: 8px; box-shadow: none; backdrop-filter: none;
    }
    .search-button { border-radius: 5px; }
    .featured-search, .example { border-radius: 5px; }
    .secondary-tools { grid-template-columns: 1fr; margin-top: 18px; }
    .disclosure, .topic-browser, .record-list, .result-disclosure, .card, .open-card, .bundle-item, .trust-item {
      border-radius: 7px; box-shadow: none;
    }
    .topic-browser { display: block; background: white; }
    .directory-main { padding: 22px; }
    .directory-toolbar { display: flex; justify-content: flex-end; }

    @media (max-width: 980px) {
      .shell { grid-template-columns: 200px minmax(0, 1fr); }
      main { width: min(100% - 36px, 1080px); }
    }
    @media (max-width: 760px) {
      .shell { display: block; }
      header { position: static; height: auto; padding: 18px 16px; }
      .brand { align-items: center; }
      .sidebar-context { margin-top: 22px; }
      .sidebar-bundle { margin-top: 18px; padding-left: 0; padding-right: 0; }
      .sidebar-nav { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .sidebar-nav .sidebar-label { grid-column: 1 / -1; margin-left: 0; }
      .sidebar-view-list { display: contents; }
      .header-actions { margin-top: 14px; }
      main { width: min(100% - 24px, 1080px); padding-top: 48px; }
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
      <div class="sidebar-context" id="sidebar-context" hidden>
        <nav class="sidebar-nav" aria-label="Explore this bundle">
          <p class="sidebar-label">Browse</p>
          <button class="sidebar-nav-button" id="sidebar-search" type="button">
            <span class="sidebar-nav-index">01</span><span>Genome search</span>
          </button>
          <div class="sidebar-view-list" role="tablist" aria-label="Topic views">
            <button class="sidebar-nav-button" type="button" role="tab" aria-controls="topic-catalog" data-sidebar-view="personal">
              <span class="sidebar-nav-index">02</span><span>Personal results</span><span class="sidebar-nav-count"></span>
            </button>
            <button class="sidebar-nav-button" type="button" role="tab" aria-controls="topic-catalog" data-sidebar-view="medications">
              <span class="sidebar-nav-index">03</span><span>Medications</span><span class="sidebar-nav-count"></span>
            </button>
            <button class="sidebar-nav-button" type="button" role="tab" aria-controls="topic-catalog" data-sidebar-view="conditions">
              <span class="sidebar-nav-index">04</span><span>Conditions</span><span class="sidebar-nav-count"></span>
            </button>
            <button class="sidebar-nav-button" type="button" role="tab" aria-controls="topic-catalog" data-sidebar-view="traits">
              <span class="sidebar-nav-index">05</span><span>Traits</span><span class="sidebar-nav-count"></span>
            </button>
          </div>
        </nav>
        <div class="sidebar-bundle">
          <p class="sidebar-label">Bundle details</p>
          <strong class="sidebar-bundle-name" id="sidebar-bundle-name">Genome bundle</strong>
          <span class="sidebar-bundle-status" id="validation">Verified</span>
          <span class="sidebar-bundle-meta">Genome spec <span id="spec-version">Loading</span> · <span id="build">Loading</span></span>
          <span class="sidebar-bundle-meta"><span id="snapshot">Loading</span> · <span id="stored">Loading</span> local data</span>
        </div>
      </div>
      <div class="header-actions">
        <button class="quit-button" id="bundles-button" type="button" hidden>Manage bundles</button>
        <button class="quit-button" id="quit-button" type="button">Quit</button>
      </div>
    </header>

    <main class="welcome" id="welcome">
      <p class="eyebrow">Welcome to Genome Explorer</p>
      <h1 id="welcome-title">Explore your genome bundle privately.</h1>
      <p class="lede" id="welcome-lede">Choose a compatible bundle to get started. It stays on this computer and is never uploaded.</p>

      <section class="bundle-library" id="bundle-library" aria-labelledby="library-title" hidden>
        <div class="library-head">
          <h2 id="library-title">Your bundles</h2>
          <p>Saved on this computer</p>
        </div>
        <div class="bundle-list" id="bundle-list"></div>
      </section>

      <div class="selection-status" id="selection-status" hidden aria-live="polite">
        <span class="status-spinner" id="status-spinner" aria-hidden="true"></span>
        <span id="selection-message"></span>
      </div>

      <section class="open-card" aria-labelledby="open-title">
        <div class="open-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7.5h5l1.6 2H20v8.5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7.5Z"/><path d="M4 8V6a2 2 0 0 1 2-2h3l1.6 2H18a2 2 0 0 1 2 2v1.5"/></svg>
        </div>
        <div class="open-copy">
          <h2 id="open-title">Add a genome bundle</h2>
          <p>Select a compatible genome bundle from this computer. The original file will not be changed.</p>
        </div>
        <button class="choose-button" id="choose-button" type="button">Add genome bundle</button>
      </section>

      <div class="trust-grid" aria-label="Privacy information">
        <div class="trust-item"><strong>Stays local</strong><span>The bundle is read only on this computer.</span></div>
        <div class="trust-item"><strong>No account or AI</strong><span>No sign-in, API key, or AI connection is required.</span></div>
        <div class="trust-item"><strong>No upload</strong><span>Explorer never copies the source bundle, and the app does not send it over the network.</span></div>
      </div>
    </main>

    <main id="explorer" hidden>
      <section class="workspace-view explorer-intro" id="view-search">
        <p class="eyebrow">Exploring <span id="active-bundle-name">your genome bundle</span></p>
        <h1>What would you like to explore?</h1>
        <p class="lede">Search this bundle by topic, medication, gene, or variant.</p>

        <div class="search-panel">
          <form id="search-form">
            <input id="search-input" type="search" aria-label="Search your genome bundle" autocomplete="off" spellcheck="false" placeholder="Try a medication, trait, condition, or gene" autofocus>
            <button class="search-button" id="search-button" type="submit">Search</button>
          </form>
        </div>
        <div class="featured-searches" aria-label="Popular searches">
          <span>Popular searches</span>
          <button class="featured-search" type="button" data-query="MTHFR">MTHFR</button>
          <button class="featured-search" type="button" data-query="Ehlers-Danlos">Ehlers-Danlos syndrome</button>
          <button class="featured-search" type="button" data-query="Parkinson">Parkinson's disease</button>
          <button class="featured-search" type="button" data-query="primary immunodeficiency">Primary immunodeficiency</button>
          <button class="featured-search" type="button" data-query="clopidogrel">Clopidogrel</button>
          <button class="featured-search" type="button" data-query="cholesterol">Cholesterol</button>
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
        </div>
      </section>
      <section class="workspace-view topic-library" id="view-library" aria-labelledby="topic-library-title" hidden>
        <div class="topic-library-head">
          <div>
            <p class="eyebrow">Bundle library</p>
            <h1 id="topic-library-title">Personal results</h1>
            <p class="lede" id="topic-library-lede">Browse person-specific results recorded in this bundle.</p>
          </div>
          <div class="topic-summary" id="topic-summary"></div>
        </div>
        <div class="topic-catalog" id="topic-catalog" role="tabpanel"></div>
      </section>

      <section class="workspace-view results" id="results" hidden aria-live="polite">
        <button class="workspace-back" id="results-back" type="button">← Back</button>
        <div class="results-head">
          <h1 id="results-title">What the bundle records</h1>
          <div class="result-meta" id="result-meta"></div>
        </div>
        <div class="notice">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>
          <span>Bundle records only. Not a diagnosis.</span>
        </div>
        <div id="result-content"></div>
      </section>
    </main>
  </div>
  <script nonce="__NONCE__">
    const basePath = "__BASE_PATH__";
    const welcome = document.querySelector("#welcome");
    const explorer = document.querySelector("#explorer");
    const welcomeTitle = document.querySelector("#welcome-title");
    const welcomeLede = document.querySelector("#welcome-lede");
    const bundleLibrary = document.querySelector("#bundle-library");
    const bundleList = document.querySelector("#bundle-list");
    const openTitle = document.querySelector("#open-title");
    const chooseButton = document.querySelector("#choose-button");
    const selectionStatus = document.querySelector("#selection-status");
    const selectionMessage = document.querySelector("#selection-message");
    const statusSpinner = document.querySelector("#status-spinner");
    const form = document.querySelector("#search-form");
    const input = document.querySelector("#search-input");
    const button = document.querySelector("#search-button");
    const results = document.querySelector("#results");
    const content = document.querySelector("#result-content");
    const topicCatalog = document.querySelector("#topic-catalog");
    const topicSummary = document.querySelector("#topic-summary");
    const topicLibrary = document.querySelector(".topic-library");
    const topicLibraryTitle = document.querySelector("#topic-library-title");
    const topicLibraryLede = document.querySelector("#topic-library-lede");
    const viewSearch = document.querySelector("#view-search");
    const resultsBack = document.querySelector("#results-back");
    const sidebarContext = document.querySelector("#sidebar-context");
    const sidebarBundleName = document.querySelector("#sidebar-bundle-name");
    const sidebarSearch = document.querySelector("#sidebar-search");
    const sidebarViewButtons = Array.from(document.querySelectorAll("[data-sidebar-view]"));
    const bundlesButton = document.querySelector("#bundles-button");
    const quitButton = document.querySelector("#quit-button");
    const desktop = window.genomeExplorer?.desktop === true;
    if (desktop) quitButton.hidden = true;
    let statusTimer = null;
    let explorerReady = false;
    let latestStatus = null;
    let latestTopics = [];
    let activeDirectoryView = "personal";
    let activeWorkspaceRoute = "search";
    let resultReturnRoute = "search";

    const fieldLabels = {
      variant_id: "Variant identifier", rsid: "rsID", chrom: "Chromosome", pos: "Position",
      ref: "Reference allele", alt: "Alternate allele", genotype: "Genotype", zygosity: "Zygosity",
      call_confidence: "Call confidence", gene: "Gene annotation", gene_symbol: "Gene",
      hgvsp: "Protein change", clinvar_significance: "ClinVar classification",
      clinvar_review_stars: "ClinVar review", clinvar_id: "ClinVar record",
      clinvar_has_conflicts: "ClinVar conflicts", clinvar_conflict_summary: "Conflict summary",
      clinvar_submitters_count: "ClinVar submitters", finding_id: "Finding identifier",
      condition: "Condition", claim_type: "Claim type", classification: "Classification",
      called_alleles: "Recorded genotype", evidence_ids: "Evidence identifiers", review_status: "Review status",
      clinical_grade: "Clinical-grade flag", diplotype: "Recorded diplotype", phenotype: "Recorded phenotype",
      activity_score: "Activity score", copy_number: "Copy number", cpic_level: "CPIC evidence level",
      affected_drugs: "Related medications", guideline_url: "Recorded guideline",
      trait: "Trait", score_value: "Recorded score", percentile: "Recorded percentile",
      reference_population: "Comparison group recorded in bundle", training_source: "Training source",
      training_date: "Training date", effect_allele: "Effect allele", effect_size: "Effect size",
      effect_type: "Effect type", p_value: "P value", source: "Recorded source", pubmed_id: "PubMed",
      study_pmids: "Research references", study_accession: "Study accession",
      catalog_version: "Catalog version", source_version: "Source version",
      effect_allele_in_call: "Effect allele recorded in this genome",
      start_pos: "Gene start", end_pos: "Gene end", variant_count: "Variants recorded",
      actionable_count: "Actionable records"
    };

    const sectionLabels = {
      clinical_findings: "Clinical findings",
      variants: "Your recorded variants", genes: "Records for this gene",
      pharmacogenomics: "Medication-related records", polygenic_scores: "Traits and scores",
      trait_variants: "Related variants",
      gwas: "Research sources"
    };

    const recordLabels = {
      clinical_findings: "",
      variants: "Personal variant record", genes: "Personal gene summary",
      pharmacogenomics: "Bundle pharmacogenomic record", polygenic_scores: "Recorded score",
      trait_variants: "",
      gwas: ""
    };

    const primaryFields = {
      clinical_findings: ["classification", "called_alleles", "gene_symbol", "call_confidence", "review_status"],
      variants: ["zygosity", "call_confidence"],
      genes: ["variant_count", "actionable_count"],
      pharmacogenomics: [],
      polygenic_scores: ["percentile", "reference_population"],
      trait_variants: ["called_alleles", "matched_traits", "gene", "call_confidence", "study_pmids"],
      gwas: ["rsid", "gene", "source", "study_pmids", "study_accession"]
    };

    const topicKinds = {
      clinical: {
        label: "Clinical",
        icon: "+",
        prompt: "Which clinical findings are recorded in this bundle?"
      },
      medications: {
        label: "Medications",
        icon: "Rx",
        prompt: "Could this bundle contain a person-specific pharmacogenomic call linked to this medication?"
      },
      conditions: {
        label: "Conditions",
        icon: "+",
        prompt: "Does this bundle record a score or person-linked annotation mentioning this condition?"
      },
      traits: {
        label: "Traits",
        icon: "%",
        prompt: "Does this bundle record a score or person-linked annotation mentioning this trait?"
      }
    };

    const directoryViews = {
      personal: {
        label: "Personal results",
        title: "Personal results",
        description: "Browse person-specific results recorded in this bundle."
      },
      medications: {
        label: "Medications",
        title: "Medications",
        description: "Browse medications linked to pharmacogenomic records in this bundle."
      },
      conditions: {
        label: "Conditions",
        title: "Conditions",
        description: "Browse conditions covered by recorded scores and person-linked annotations."
      },
      traits: {
        label: "Traits",
        title: "Traits",
        description: "Browse traits covered by recorded scores and person-linked annotations."
      }
    };

    function isPersonSpecificTopic(topic) {
      const sections = Array.isArray(topic.record_sections) ? topic.record_sections : [];
      return sections.includes("clinical_findings") || sections.includes("pharmacogenomics") || sections.includes("polygenic_scores");
    }

    function topicIndicator(topic) {
      const personal = topic.personal || {};
      const clinical = Array.isArray(personal.clinical_findings) ? personal.clinical_findings : [];
      const pgx = Array.isArray(personal.pharmacogenomics) ? personal.pharmacogenomics : [];
      const scores = Array.isArray(personal.polygenic_scores) ? personal.polygenic_scores : [];
      const hasPersonLinkedVariants = Boolean(personal.has_person_linked_variants);
      const indicator = document.createElement("span");
      indicator.className = "topic-indicator";
      const value = document.createElement("span");
      value.className = "topic-indicator-value";

      if (clinical.length === 1) {
        const finding = clinical[0];
        const classification = formatValue(finding.classification || "Clinical finding");
        value.textContent = finding.gene_symbol ? `${classification} · ${finding.gene_symbol}` : classification;
      } else if (clinical.length > 1) {
        value.textContent = `${clinical.length} clinical findings`;
      } else if (pgx.length === 1) {
        const result = pgx[0].phenotype || pgx[0].diplotype || "PGx result";
        value.textContent = `${result} · ${pgx[0].gene_symbol}`;
      } else if (pgx.length > 1) {
        value.textContent = `${pgx.length} PGx results`;
      } else if (scores.length === 1) {
        const percentile = Number(scores[0].percentile).toLocaleString(undefined, { maximumFractionDigits: 1 });
        value.textContent = `${percentile}th percentile`;
      } else if (scores.length > 1) {
        value.textContent = `${scores.length} scores`;
      } else if (hasPersonLinkedVariants) {
        indicator.classList.add("related");
        value.textContent = "Related variants";
      } else {
        indicator.classList.add("no-data");
        value.textContent = "No personal result";
      }
      indicator.append(value);
      return indicator;
    }

    function directoryRow(topic) {
      const row = document.createElement("button");
      row.className = "directory-row";
      row.type = "button";
      row.dataset.topicQuery = topic.query;
      row.setAttribute("aria-label", `Search this bundle for ${topic.label}`);
      row.addEventListener("click", () => {
        input.value = topic.query;
        search(topic.query);
      });
      const name = document.createElement("span");
      name.className = "directory-name";
      name.textContent = topic.label;
      const arrow = document.createElement("span");
      arrow.className = "directory-arrow";
      arrow.setAttribute("aria-hidden", "true");
      arrow.textContent = "›";
      row.append(name, topicIndicator(topic), arrow);
      return row;
    }

    function topicsForDirectoryView(topics, view, filter) {
      const normalized = filter.trim().toLowerCase();
      return topics
        .filter(topic => view === "personal" ? isPersonSpecificTopic(topic) : topic.kind === view)
        .filter(topic => !normalized || `${topic.label} ${topic.group}`.toLowerCase().includes(normalized));
    }

    function directoryGroups(topics, view, filter) {
      const host = document.createElement("div");
      host.className = "directory-groups";
      const visible = topicsForDirectoryView(topics, view, filter);
      if (!visible.length) {
        const empty = document.createElement("div");
        empty.className = "directory-empty";
        empty.textContent = filter
          ? "No topics match that filter."
          : "This bundle does not contain a clinical finding, PGx result, or recorded score for these topics.";
        host.append(empty);
        return host;
      }
      const grouped = Object.groupBy(
        visible,
        topic => view === "personal" ? topicKinds[topic.kind].label : topic.group
      );
      Object.entries(grouped)
        .sort(([left], [right]) => left.localeCompare(right))
        .forEach(([groupName, groupTopics]) => {
          const section = document.createElement("section");
          section.className = "directory-group";
          const groupHead = document.createElement("div");
          groupHead.className = "directory-group-head";
          const heading = document.createElement("h4");
          heading.textContent = groupName;
          const count = document.createElement("span");
          count.className = "directory-group-count";
          count.textContent = `${groupTopics.length} ${groupTopics.length === 1 ? "topic" : "topics"}`;
          groupHead.append(heading, count);
          const list = document.createElement("div");
          list.className = "directory-list";
          groupTopics
            .sort((left, right) => left.label.localeCompare(right.label))
            .forEach(topic => list.append(directoryRow(topic)));
          section.append(groupHead, list);
          host.append(section);
        });
      return host;
    }

    function renderDirectory(topics) {
      const wrapper = document.createElement("div");
      wrapper.className = "topic-browser";
      let filterValue = "";

      const main = document.createElement("div");
      main.className = "directory-main";
      const toolbar = document.createElement("div");
      toolbar.className = "directory-toolbar";
      const filter = document.createElement("input");
      filter.className = "directory-filter";
      filter.type = "search";
      filter.setAttribute("aria-label", "Filter common topics");
      const listHost = document.createElement("div");

      const refresh = () => {
        const view = directoryViews[activeDirectoryView];
        filter.placeholder = activeDirectoryView === "personal" ? "Filter results" : `Filter ${view.label.toLowerCase()}`;
        listHost.replaceChildren(directoryGroups(topics, activeDirectoryView, filterValue));
      };

      filter.addEventListener("input", () => {
        filterValue = filter.value;
        refresh();
      });
      toolbar.append(filter);
      main.append(toolbar, listHost);
      wrapper.append(main);
      refresh();
      return wrapper;
    }

    function renderTopicCatalog(topics) {
      latestTopics = Array.isArray(topics) ? topics : [];
      sidebarViewButtons.forEach(control => {
        const view = control.dataset.sidebarView;
        const count = latestTopics.filter(topic => view === "personal" ? isPersonSpecificTopic(topic) : topic.kind === view).length;
        control.querySelector(".sidebar-nav-count").textContent = count;
      });
      const currentView = directoryViews[activeDirectoryView];
      const visibleCount = latestTopics.filter(topic => activeDirectoryView === "personal" ? isPersonSpecificTopic(topic) : topic.kind === activeDirectoryView).length;
      topicLibraryTitle.textContent = currentView.title;
      topicLibraryLede.textContent = currentView.description;
      topicSummary.textContent = `${visibleCount} ${visibleCount === 1 ? "topic" : "topics"}`;
      topicCatalog.replaceChildren(renderDirectory(latestTopics));
    }

    function updateSidebarRoute(route) {
      const searchActive = route === "search" || (route === "results" && resultReturnRoute === "search");
      sidebarSearch.classList.toggle("is-active", searchActive);
      if (searchActive) sidebarSearch.setAttribute("aria-current", "page");
      else sidebarSearch.removeAttribute("aria-current");
      sidebarViewButtons.forEach(control => {
        const selected = route === control.dataset.sidebarView ||
          (route === "results" && resultReturnRoute === control.dataset.sidebarView);
        control.setAttribute("aria-selected", String(selected));
      });
    }

    function showWorkspaceRoute(route, { historyMode = "push", focusSearch = false } = {}) {
      const isDirectoryRoute = Object.hasOwn(directoryViews, route);
      const resolvedRoute = route === "results" || route === "search" || isDirectoryRoute ? route : "search";
      if (Object.hasOwn(directoryViews, resolvedRoute) && activeDirectoryView !== resolvedRoute) {
        activeDirectoryView = resolvedRoute;
        renderTopicCatalog(latestTopics);
      }
      viewSearch.hidden = resolvedRoute !== "search";
      topicLibrary.hidden = !Object.hasOwn(directoryViews, resolvedRoute);
      results.hidden = resolvedRoute !== "results";
      activeWorkspaceRoute = resolvedRoute;
      updateSidebarRoute(resolvedRoute);

      const targetHash = `#${resolvedRoute}`;
      if (historyMode === "replace") window.history.replaceState({ route: resolvedRoute }, "", targetHash);
      else if (historyMode === "push" && window.location.hash !== targetHash) {
        window.history.pushState({ route: resolvedRoute }, "", targetHash);
      }
      window.scrollTo({ top: 0, behavior: "auto" });
      if (focusSearch) window.setTimeout(() => input.focus(), 0);
    }

    sidebarSearch.addEventListener("click", () => showWorkspaceRoute("search", { focusSearch: true }));

    sidebarViewButtons.forEach(control => {
      control.addEventListener("click", () => showWorkspaceRoute(control.dataset.sidebarView));
    });

    resultsBack.addEventListener("click", () => {
      if (window.location.hash === "#results" && window.history.state?.route === "results") window.history.back();
      else showWorkspaceRoute(resultReturnRoute);
    });

    window.addEventListener("popstate", () => {
      if (!explorerReady) return;
      showWorkspaceRoute(window.location.hash.slice(1), { historyMode: "none" });
    });

    function formatBytes(bytes) {
      const units = ["B", "KiB", "MiB", "GiB"];
      let value = bytes;
      let index = 0;
      while (value >= 1024 && index < units.length - 1) { value /= 1024; index += 1; }
      return `${value.toFixed(index ? 1 : 0)} ${units[index]}`;
    }

    function formatBundleDate(value) {
      const parsed = new Date(value);
      if (Number.isNaN(parsed.getTime())) return "Date not recorded";
      return parsed.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
    }

    async function postJson(path, payload) {
      const options = { method: "POST" };
      if (payload !== undefined) {
        options.headers = { "Content-Type": "application/json" };
        options.body = JSON.stringify(payload);
      }
      const response = await fetch(`${basePath}${path}`, options);
      const status = await response.json();
      if (!response.ok) throw new Error(status.error || "The local request could not be completed.");
      return status;
    }

    function beginNicknameEdit(body, actions, entry) {
      if (body.querySelector(".nickname-form")) return;
      actions.hidden = true;
      const form = document.createElement("form");
      form.className = "nickname-form";
      const nickname = document.createElement("input");
      nickname.className = "nickname-input";
      nickname.type = "text";
      nickname.maxLength = 80;
      nickname.value = entry.nickname;
      nickname.setAttribute("aria-label", `Nickname for ${entry.file_name}`);
      const save = document.createElement("button");
      save.className = "secondary-button";
      save.type = "submit";
      save.textContent = "Save";
      const cancel = document.createElement("button");
      cancel.className = "text-button";
      cancel.type = "button";
      cancel.textContent = "Cancel";
      const error = document.createElement("p");
      error.className = "nickname-error";
      error.hidden = true;
      form.append(nickname, save, cancel);
      body.append(form, error);

      cancel.addEventListener("click", () => renderBundleLibrary(latestStatus));
      form.addEventListener("submit", async event => {
        event.preventDefault();
        save.disabled = true;
        cancel.disabled = true;
        error.hidden = true;
        try {
          const status = await postJson("/api/library/rename", {
            bundle_id: entry.bundle_id,
            nickname: nickname.value
          });
          renderAppStatus(status);
        } catch (requestError) {
          error.textContent = requestError.message;
          error.hidden = false;
          save.disabled = false;
          cancel.disabled = false;
        }
      });
      nickname.focus();
      nickname.select();
    }

    async function openSavedBundle(entry) {
      showSelectionStatus(`Opening ${entry.nickname} locally.`, { busy: true });
      bundleList.querySelectorAll("button").forEach(control => { control.disabled = true; });
      try {
        const status = await postJson("/api/library/open", { bundle_id: entry.bundle_id });
        renderAppStatus(status);
        if (status.status === "validating") scheduleStatusPoll(150);
      } catch (error) {
        showSelectionStatus(error.message, { error: true });
        refreshStatus();
      }
    }

    function bundleItem(entry, busy) {
      const item = document.createElement("article");
      item.className = "bundle-item";
      const avatar = document.createElement("div");
      avatar.className = "bundle-avatar";
      avatar.setAttribute("aria-hidden", "true");
      avatar.textContent = entry.nickname.trim().charAt(0) || "G";
      const body = document.createElement("div");
      const name = document.createElement("h3");
      name.className = "bundle-name";
      name.textContent = entry.nickname;
      const meta = document.createElement("p");
      meta.className = "bundle-meta";
      meta.textContent = `${entry.file_name} · Genome spec v${entry.schema_version} · ${entry.genome_build} · ${formatBundleDate(entry.generated_at)}`;
      body.append(name, meta);
      if (!entry.available) {
        const unavailable = document.createElement("p");
        unavailable.className = "bundle-meta bundle-unavailable";
        unavailable.textContent = "Source file is no longer available at its saved location.";
        body.append(unavailable);
      }
      const actions = document.createElement("div");
      actions.className = "bundle-actions";
      const rename = document.createElement("button");
      rename.className = "text-button";
      rename.type = "button";
      rename.textContent = "Rename";
      rename.disabled = busy;
      rename.addEventListener("click", () => beginNicknameEdit(body, actions, entry));
      const open = document.createElement("button");
      open.className = "secondary-button bundle-open";
      open.type = "button";
      open.textContent = "Open";
      open.disabled = busy || !entry.available;
      open.addEventListener("click", () => openSavedBundle(entry));
      actions.append(rename, open);
      item.append(avatar, body, actions);
      return item;
    }

    function renderBundleLibrary(status) {
      latestStatus = status;
      const bundles = Array.isArray(status?.bundles) ? status.bundles : [];
      const busy = status?.status === "choosing" || status?.status === "validating";
      bundleLibrary.hidden = bundles.length === 0;
      bundleList.replaceChildren(...bundles.map(entry => bundleItem(entry, busy)));
      if (bundles.length) {
        welcomeTitle.textContent = "Choose a genome bundle.";
        welcomeLede.textContent = "Reopen a previously verified bundle or add another. Nicknames and retained data stay on this computer.";
        openTitle.textContent = "Add another genome bundle";
        if (!busy) chooseButton.textContent = "Add another bundle";
      } else {
        welcomeTitle.textContent = "Explore your genome bundle privately.";
        welcomeLede.textContent = "Choose a compatible bundle to get started. It stays on this computer and is never uploaded.";
        openTitle.textContent = "Add a genome bundle";
        if (!busy) chooseButton.textContent = "Add genome bundle";
      }
    }

    function showSelectionStatus(message, { busy = false, error = false } = {}) {
      selectionStatus.hidden = !message;
      selectionStatus.classList.toggle("error", error);
      statusSpinner.hidden = !busy;
      selectionMessage.textContent = message;
    }

    function populateBundleStatus(status) {
      const cached = status.validation_mode === "cached";
      const nickname = status.active_nickname || "Genome bundle";
      document.querySelector("#active-bundle-name").textContent = nickname;
      sidebarBundleName.textContent = nickname;
      document.querySelector("#validation").textContent = cached ? "Previously verified" : "Verified";
      document.querySelector("#spec-version").textContent = `v${status.schema_version}`;
      document.querySelector("#build").textContent = status.genome_build;
      document.querySelector("#snapshot").textContent = formatBundleDate(status.generated_at);
      document.querySelector("#stored").textContent = formatBytes(status.stored_bytes);
    }

    function renderAppStatus(status) {
      renderBundleLibrary(status);
      if (status.status === "ready") {
        welcome.hidden = true;
        explorer.hidden = false;
        sidebarContext.hidden = false;
        bundlesButton.hidden = !(status.bundles || []).length;
        bundlesButton.disabled = false;
        chooseButton.disabled = false;
        populateBundleStatus(status);
        if (!explorerReady) activeDirectoryView = "personal";
        renderTopicCatalog(status.topics);
        if (!explorerReady) {
          explorerReady = true;
          input.value = "";
          content.replaceChildren();
          resultReturnRoute = "search";
          showWorkspaceRoute("search", { historyMode: "replace", focusSearch: true });
        }
        return;
      }

      welcome.hidden = false;
      explorer.hidden = true;
      sidebarContext.hidden = true;
      bundlesButton.hidden = true;
      bundlesButton.disabled = false;
      explorerReady = false;
      if (status.status === "choosing") {
        chooseButton.disabled = true;
        chooseButton.textContent = "Waiting for selection";
        showSelectionStatus("Choose a genome bundle in the file window that just opened.", { busy: true });
      } else if (status.status === "validating") {
        chooseButton.disabled = true;
        chooseButton.textContent = "Opening bundle";
        const name = status.archive_name || "your bundle";
        showSelectionStatus(`Opening ${name} locally. New bundles may take a few minutes to verify.`, { busy: true });
      } else if (status.status === "failed") {
        chooseButton.disabled = false;
        chooseButton.textContent = (status.bundles || []).length ? "Add another bundle" : "Choose another bundle";
        showSelectionStatus(status.error || "This bundle could not be opened.", { error: true });
      } else {
        chooseButton.disabled = false;
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
      if (hit.section === "clinical_findings") return hit.condition;
      if (hit.section === "pharmacogenomics") {
        return hit.gene_symbol;
      }
      if (hit.section === "variants") return hit.gene || hit.rsid || "Recorded variant";
      if (hit.section === "trait_variants") return hit.rsid || hit.variant_id || hit.gene || "Recorded variant";
      if (hit.section === "genes") return hit.gene_symbol;
      return hit.trait || hit.rsid || "Recorded result";
    }

    function subtitleFor(hit, query) {
      if (hit.section === "pharmacogenomics") {
        const medication = matchingMedication(hit, query);
        return medication ? `Matched medication: ${capitalize(medication)}` : "Person-specific bundle result";
      }
      if (hit.section === "variants") return hit.rsid ? `Identifier: ${hit.rsid}` : "";
      if (hit.section === "genes") return "Personal variant records found";
      return hit.rsid ? `Identifier: ${hit.rsid}` : "";
    }

    function summaryFor(hit, query) {
      if (hit.section === "pharmacogenomics") {
        return `This bundle contains a person-specific pharmacogenomic result for ${hit.gene_symbol}.`;
      }
      if (hit.section === "polygenic_scores") return `The bundle contains a recorded score for ${hit.trait}.`;
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
      return "";
    }

    function fieldLabelFor(section, key) {
      if (section === "gwas" && key === "gene") return "Gene named by research";
      if (section === "clinical_findings" && key === "call_confidence") return "Technical call quality";
      if (section === "trait_variants" && key === "called_alleles") return "Recorded genotype";
      if (section === "trait_variants" && key === "matched_traits") return "Matching recorded topics";
      if (section === "trait_variants" && key === "recorded_traits") return "Recorded topic labels";
      if (section === "trait_variants" && key === "study_pmids") return "Research references";
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
      } else if (key === "study_pmids" || key === "pubmed_id") {
        const identifiers = (Array.isArray(value) ? value : [value]).map(String).filter(identifier => /^\d+$/.test(identifier));
        if (identifiers.length) {
          detail.classList.add("reference-links");
          identifiers.forEach(identifier => {
            const link = document.createElement("a");
            link.href = `https://pubmed.ncbi.nlm.nih.gov/${identifier}/`;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.textContent = `PubMed ${identifier}`;
            detail.append(link);
          });
        } else {
          detail.textContent = formatValue(value);
        }
      } else if (key === "study_accession" && typeof value === "string" && /^GCST\d+$/i.test(value)) {
        const link = document.createElement("a");
        link.href = `https://www.ebi.ac.uk/gwas/studies/${encodeURIComponent(value)}`;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = `GWAS Catalog ${value}`;
        detail.append(link);
      } else if (key === "clinvar_id" && typeof value === "string") {
        const link = document.createElement("a");
        link.href = /^\d+$/.test(value)
          ? `https://www.ncbi.nlm.nih.gov/clinvar/variation/${encodeURIComponent(value)}/`
          : `https://www.ncbi.nlm.nih.gov/clinvar/?term=${encodeURIComponent(value)}`;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = `ClinVar ${value}`;
        detail.append(link);
      } else if (key === "clinvar_review_stars") {
        detail.textContent = `${value} of 4 stars`;
      } else if (key === "called_alleles" && Array.isArray(value)) {
        detail.textContent = value.join(" / ");
      } else if (key === "source" && value === "gwas_catalog") {
        detail.textContent = "GWAS Catalog";
      } else {
        detail.textContent = formatValue(value);
      }
      wrapper.append(label, detail);
      return wrapper;
    }

    function appendClinicalFindingData(card, hit) {
      if (hit.clinvar_has_conflicts) {
        const conflict = document.createElement("div");
        conflict.className = "clinical-conflict";
        conflict.textContent = hit.clinvar_conflict_summary
          ? `Conflicting ClinVar submissions · ${formatValue(hit.clinvar_conflict_summary)}`
          : "Conflicting ClinVar submissions";
        card.append(conflict);
      }

      const evidence = Array.isArray(hit.evidence) ? hit.evidence : [];
      const clinvarEvidence = evidence.find(item => String(item?.source || "").toLowerCase() === "clinvar");
      const reviewStatus = clinvarEvidence?.review_status || (
        hit.clinvar_review_stars !== null && hit.clinvar_review_stars !== undefined
          ? `${hit.clinvar_review_stars} of 4 stars`
          : ""
      );
      const visible = { ...hit, review_status: reviewStatus };
      const fields = document.createElement("dl");
      fields.className = "simple-fields";
      ["classification", "called_alleles", "gene_symbol", "call_confidence", "review_status"].forEach(key => {
        const value = visible[key];
        if (value !== null && value !== undefined && value !== "") {
          fields.append(fieldElement(key, value, hit.section));
        }
      });
      if (fields.children.length) card.append(fields);

      const sources = document.createElement("div");
      sources.className = "clinical-sources";
      const links = new Set();
      evidence.forEach(item => {
        if (!item || typeof item !== "object") return;
        const sourceName = formatValue(item.source || "Recorded source");
        const sourceId = item.source_record_id ? String(item.source_record_id) : "";
        const row = document.createElement("div");
        row.className = "clinical-source";
        if (String(item.source || "").toLowerCase() === "clinvar" && sourceId) {
          const link = document.createElement("a");
          link.className = "source-link";
          link.href = /^\d+$/.test(sourceId)
            ? `https://www.ncbi.nlm.nih.gov/clinvar/variation/${encodeURIComponent(sourceId)}/`
            : `https://www.ncbi.nlm.nih.gov/clinvar/?term=${encodeURIComponent(sourceId)}`;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          link.textContent = `ClinVar ${sourceId}`;
          row.append(link);
          links.add(sourceId);
        } else {
          const name = document.createElement("strong");
          name.textContent = sourceId ? `${sourceName} ${sourceId}` : sourceName;
          row.append(name);
        }
        const metadata = [
          item.source_version,
          item.retrieved_at ? formatBundleDate(item.retrieved_at) : ""
        ].filter(value => value !== null && value !== undefined && value !== "");
        if (metadata.length) {
          const detail = document.createElement("span");
          detail.textContent = metadata.join(" · ");
          row.append(detail);
        }
        sources.append(row);
      });
      if (hit.clinvar_id && !links.has(String(hit.clinvar_id))) {
        const row = document.createElement("div");
        row.className = "clinical-source";
        const link = document.createElement("a");
        link.className = "source-link";
        link.href = /^\d+$/.test(String(hit.clinvar_id))
          ? `https://www.ncbi.nlm.nih.gov/clinvar/variation/${encodeURIComponent(hit.clinvar_id)}/`
          : `https://www.ncbi.nlm.nih.gov/clinvar/?term=${encodeURIComponent(hit.clinvar_id)}`;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = `ClinVar ${hit.clinvar_id}`;
        row.append(link);
        sources.append(row);
      }
      if (sources.children.length) card.append(sources);
    }

    function appendPharmacogenomicsData(card, hit, query) {
      const personal = document.createElement("section");
      personal.className = "personal-data";
      const personalLabel = document.createElement("h4");
      personalLabel.className = "data-group-label";
      personalLabel.textContent = "Person-specific data from this bundle";
      const personalCopy = document.createElement("p");
      personalCopy.className = "data-group-copy";
      personalCopy.textContent = "These values describe the person represented by this bundle.";
      const personalFields = document.createElement("dl");
      personalFields.className = "simple-fields";
      ["diplotype", "phenotype", "activity_score", "copy_number"].forEach(key => {
        const value = hit[key];
        if (value !== null && value !== undefined && value !== "") {
          personalFields.append(fieldElement(key, value, hit.section));
        }
      });
      personal.append(personalLabel, personalCopy, personalFields);
      card.append(personal);

      const context = document.createElement("section");
      context.className = "reference-context";
      const contextLabel = document.createElement("h4");
      contextLabel.className = "data-group-label";
      contextLabel.textContent = "Reference context included in the bundle";
      const contextCopy = document.createElement("p");
      contextCopy.className = "data-group-copy";
      const medication = matchingMedication(hit, query);
      contextCopy.textContent = medication
        ? `The bundle links ${hit.gene_symbol} with recorded guidance for ${capitalize(medication)}. This context is not unique to this person.`
        : `The bundle includes recorded medication guidance for ${hit.gene_symbol}. This context is not unique to this person.`;
      const contextFields = document.createElement("dl");
      contextFields.className = "simple-fields";
      if (hit.cpic_level !== null && hit.cpic_level !== undefined && hit.cpic_level !== "") {
        contextFields.append(fieldElement("cpic_level", hit.cpic_level, hit.section));
      }
      context.append(contextLabel, contextCopy, contextFields);
      if (typeof hit.guideline_url === "string" && hit.guideline_url.startsWith("https://")) {
        const source = document.createElement("a");
        source.className = "source-link";
        source.href = hit.guideline_url;
        source.target = "_blank";
        source.rel = "noopener noreferrer";
        source.textContent = "View recorded guideline";
        context.append(source);
      }
      card.append(context);
    }

    function cardFor(hit, query) {
      const card = document.createElement("article");
      card.className = "card";
      const compact = hit.section === "clinical_findings" || hit.section === "trait_variants" || hit.section === "gwas";

      if (!compact) {
        const type = document.createElement("div");
        type.className = "record-type";
        type.textContent = recordLabels[hit.section] || "Bundle record";
        card.append(type);
      }

      const top = document.createElement("div");
      top.className = "card-top";
      const title = document.createElement("h3");
      title.textContent = titleFor(hit, query);
      const subtitle = document.createElement("div");
      subtitle.className = "card-id";
      subtitle.textContent = subtitleFor(hit, query);
      top.append(title);
      if (!compact && subtitle.textContent) top.append(subtitle);
      card.append(top);

      if (!compact) {
        const summary = document.createElement("p");
        summary.className = "recorded-summary";
        summary.textContent = summaryFor(hit, query);
        card.append(summary);

        const meaning = meaningFor(hit);
        if (meaning) {
          const note = document.createElement("p");
          note.className = "meaning-note";
          note.textContent = meaning;
          card.append(note);
        }
      }

      if (hit.section === "clinical_findings") {
        appendClinicalFindingData(card, hit);
      } else if (hit.section === "pharmacogenomics") {
        appendPharmacogenomicsData(card, hit, query);
      } else {
        const simple = document.createElement("dl");
        simple.className = "simple-fields";
        (primaryFields[hit.section] || []).forEach(key => {
          const value = hit[key];
          if (value !== null && value !== undefined && value !== "") simple.append(fieldElement(key, value, hit.section));
        });
        if (simple.children.length) card.append(simple);
      }

      if (hit.section !== "pharmacogenomics" && typeof hit.guideline_url === "string" && hit.guideline_url.startsWith("https://")) {
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
      const alreadyShown = new Set(primaryFields[hit.section] || []);
      Object.entries(hit).forEach(([key, value]) => {
        if (key === "section" || value === null || value === undefined || value === "") return;
        if (hit.section === "clinical_findings" && [
          "condition", "classification", "called_alleles", "gene_symbol", "call_confidence",
          "clinvar_has_conflicts", "clinvar_conflict_summary", "clinvar_review_stars",
          "clinvar_submitters_count", "clinvar_id", "evidence"
        ].includes(key)) return;
        if ((hit.section === "trait_variants" || hit.section === "gwas") && alreadyShown.has(key)) return;
        fields.append(fieldElement(key, value, hit.section));
      });
      technical.append(technicalSummary, fields);
      card.append(technical);
      return card;
    }

    function sectionHeading(sectionName, count, showCount = true) {
      const heading = document.createElement("div");
      heading.className = "section-title";
      const label = document.createElement("span");
      label.textContent = sectionLabels[sectionName] || sectionName;
      heading.append(label);
      if (showCount) {
        const badge = document.createElement("span");
        badge.className = "count";
        badge.textContent = count;
        heading.append(badge);
      }
      return heading;
    }

    function cardsFor(hits, query) {
      const cards = document.createElement("div");
      cards.className = "cards";
      hits.forEach(hit => cards.append(cardFor(hit, query)));
      return cards;
    }

    const compactRecordSections = new Set(["variants", "trait_variants", "gwas"]);

    function compactValue(key, value) {
      if (value === null || value === undefined || value === "") return "Not recorded";
      if (key === "called_alleles" && Array.isArray(value)) return value.join(" / ");
      if (key === "source" && value === "gwas_catalog") return "GWAS Catalog";
      return formatValue(value);
    }

    function recordColumnsFor(hit) {
      if (hit.section === "trait_variants") {
        return [
          { label: "Variant", key: hit.rsid ? "rsid" : "variant_id", value: hit.rsid || hit.variant_id },
          { label: "Genotype", key: "called_alleles", value: hit.called_alleles },
          { label: "Gene", key: "gene", value: hit.gene },
          { label: "Matching topic", key: "matched_traits", value: hit.matched_traits },
          { label: "Call confidence", key: "call_confidence", value: hit.call_confidence }
        ];
      }
      if (hit.section === "gwas") {
        return [
          { label: "Research topic", key: "trait", value: hit.trait },
          { label: "Variant", key: hit.rsid ? "rsid" : "variant_id", value: hit.rsid || hit.variant_id },
          { label: "Gene", key: "gene", value: hit.gene },
          { label: "Source", key: "source", value: hit.source }
        ];
      }
      return [
        { label: "Variant", key: hit.rsid ? "rsid" : "variant_id", value: hit.rsid || hit.variant_id },
        { label: "Zygosity", key: "zygosity", value: hit.zygosity },
        { label: "Gene", key: "gene", value: hit.gene },
        { label: "Call confidence", key: "call_confidence", value: hit.call_confidence }
      ];
    }

    function recordRowFor(hit) {
      const row = document.createElement("details");
      row.className = "record-row";
      const summary = document.createElement("summary");
      summary.className = "record-row-summary";
      const columns = recordColumnsFor(hit);
      columns.forEach((column, index) => {
        const cell = document.createElement("span");
        cell.className = `record-row-cell${index === 0 ? " record-row-primary" : ""}`;
        cell.dataset.label = column.label;
        const value = document.createElement("span");
        value.className = "record-row-value";
        value.textContent = compactValue(column.key, column.value);
        value.title = value.textContent;
        cell.append(value);
        summary.append(cell);
      });
      const arrow = document.createElement("span");
      arrow.className = "record-row-arrow";
      arrow.setAttribute("aria-hidden", "true");
      arrow.textContent = "›";
      summary.append(arrow);

      const details = document.createElement("div");
      details.className = "record-row-details";
      const fields = document.createElement("dl");
      fields.className = "record-row-fields";
      const shownKeys = new Set(columns.map(column => column.key));
      Object.entries(hit).forEach(([key, value]) => {
        if (key === "section" || shownKeys.has(key) || value === null || value === undefined || value === "") return;
        fields.append(fieldElement(key, value, hit.section));
      });
      details.append(fields);
      row.append(summary, details);
      return row;
    }

    function recordListFor(hits, sectionName) {
      const list = document.createElement("div");
      list.className = `record-list record-layout-${sectionName}`;
      const head = document.createElement("div");
      head.className = "record-list-head";
      head.setAttribute("aria-hidden", "true");
      recordColumnsFor(hits[0]).forEach(column => {
        const label = document.createElement("span");
        label.textContent = column.label;
        head.append(label);
      });
      head.append(document.createElement("span"));
      list.append(head, ...hits.map(recordRowFor));
      return list;
    }

    function recordsFor(hits, query, sectionName) {
      return compactRecordSections.has(sectionName)
        ? recordListFor(hits, sectionName)
        : cardsFor(hits, query);
    }

    function paginatedResults(hits, query, sectionName) {
      const pageSize = compactRecordSections.has(sectionName) ? 10 : 4;
      if (hits.length <= pageSize) return recordsFor(hits, query, sectionName);

      const wrapper = document.createElement("div");
      wrapper.className = "paginated-results";
      const pageContent = document.createElement("div");
      pageContent.className = "result-page";
      const pagination = document.createElement("nav");
      pagination.className = "result-pagination";
      pagination.setAttribute("aria-label", `${sectionLabels[sectionName] || sectionName} pages`);
      const range = document.createElement("span");
      range.className = "pagination-range";
      range.setAttribute("aria-live", "polite");
      const actions = document.createElement("div");
      actions.className = "pagination-actions";
      const previous = document.createElement("button");
      previous.className = "pagination-button";
      previous.type = "button";
      previous.textContent = "Previous";
      previous.setAttribute("aria-label", `Previous page of ${sectionLabels[sectionName] || sectionName}`);
      const next = document.createElement("button");
      next.className = "pagination-button";
      next.type = "button";
      next.textContent = "Next";
      next.setAttribute("aria-label", `Next page of ${sectionLabels[sectionName] || sectionName}`);
      actions.append(previous, next);
      pagination.append(range, actions);
      wrapper.append(pageContent, pagination);

      let page = 0;
      const pageCount = Math.ceil(hits.length / pageSize);
      const renderPage = ({ scroll = false } = {}) => {
        const start = page * pageSize;
        const end = Math.min(start + pageSize, hits.length);
        pageContent.replaceChildren(recordsFor(hits.slice(start, end), query, sectionName));
        range.textContent = `${start + 1}-${end} of ${hits.length}`;
        previous.disabled = page === 0;
        next.disabled = page === pageCount - 1;
        if (scroll) pageContent.scrollIntoView({ behavior: "smooth", block: "start" });
      };
      previous.addEventListener("click", () => {
        if (page === 0) return;
        page -= 1;
        renderPage({ scroll: true });
      });
      next.addEventListener("click", () => {
        if (page === pageCount - 1) return;
        page += 1;
        renderPage({ scroll: true });
      });
      renderPage();
      return wrapper;
    }

    function renderSearch(payload) {
      const count = payload.hits.length;
      const matchingTopic = latestTopics.find(topic => topic.query.toLowerCase() === payload.query.toLowerCase());
      const grouped = Object.groupBy(payload.hits, hit => hit.section);
      const hasPersonLinkedRecords = Boolean(grouped.clinical_findings?.length || grouped.trait_variants?.length);
      document.querySelector("#results-title").textContent = count
        ? "What the bundle records"
        : matchingTopic ? "No personal result recorded" : "Not covered";
      document.querySelector("#result-meta").textContent = hasPersonLinkedRecords
        ? ""
        : count ? `${count} recorded ${count === 1 ? "match" : "matches"}` : "";
      content.replaceChildren();
      if (!count) {
        const empty = document.createElement("div");
        empty.className = "empty";
        empty.textContent = matchingTopic
          ? "No score or related variant is recorded for this topic."
          : "This search is not covered by the bundle's recorded fields.";
        content.append(empty);
        return;
      }
      const sectionOrder = ["clinical_findings", "pharmacogenomics", "polygenic_scores", "trait_variants", "genes", "variants", "gwas"];
      const hasClearerRecord = Boolean(
        grouped.clinical_findings?.length ||
        grouped.pharmacogenomics?.length ||
        grouped.polygenic_scores?.length ||
        grouped.trait_variants?.length
      );
      sectionOrder.filter(sectionName => grouped[sectionName]?.length).forEach(sectionName => {
        const hits = grouped[sectionName];
        const section = document.createElement("section");
        section.className = `section section-${sectionName}`;
        const isSecondary = hasClearerRecord && (sectionName === "variants" || sectionName === "gwas");
        const showCount = !hasPersonLinkedRecords || !["clinical_findings", "trait_variants", "gwas"].includes(sectionName);
        if (isSecondary) {
          const disclosure = document.createElement("details");
          disclosure.className = "result-disclosure";
          const summary = document.createElement("summary");
          summary.append(sectionHeading(sectionName, hits.length, showCount));
          disclosure.append(summary, paginatedResults(hits, payload.query, sectionName));
          section.append(disclosure);
        } else {
          section.append(sectionHeading(sectionName, hits.length, showCount), paginatedResults(hits, payload.query, sectionName));
        }
        content.append(section);
      });
    }

    async function search(query) {
      if (activeWorkspaceRoute !== "results") resultReturnRoute = activeWorkspaceRoute;
      showWorkspaceRoute("results");
      button.disabled = true;
      button.innerHTML = '<span class="spinner"></span>Searching';
      document.querySelector("#results-title").textContent = "Searching";
      document.querySelector("#result-meta").textContent = "";
      content.innerHTML = '<div class="empty">Searching this bundle...</div>';
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

    document.querySelectorAll(".featured-search").forEach(shortcut => {
      shortcut.addEventListener("click", () => {
        input.value = shortcut.dataset.query || shortcut.textContent;
        search(input.value);
      });
    });

    chooseButton.addEventListener("click", async () => {
      chooseButton.disabled = true;
      chooseButton.textContent = "Opening file selector";
      showSelectionStatus("Opening the local file selector.", { busy: true });
      try {
        const status = desktop
          ? await window.genomeExplorer.chooseBundle()
          : await postJson("/api/select");
        renderAppStatus(status);
        if (status.status === "choosing" || status.status === "validating") scheduleStatusPoll(150);
      } catch (error) {
        chooseButton.disabled = false;
        chooseButton.textContent = "Try again";
        showSelectionStatus(error.message || "The local file selector could not be opened.", { error: true });
      }
    });
    if (desktop) {
      window.genomeExplorer.onChooseBundleRequested(() => chooseButton.click());
    }

    bundlesButton.addEventListener("click", async () => {
      window.clearTimeout(statusTimer);
      bundlesButton.disabled = true;
      try {
        const status = await postJson("/api/library/show");
        renderAppStatus(status);
      } catch (error) {
        bundlesButton.disabled = false;
      }
    });

    quitButton.addEventListener("click", async () => {
      window.clearTimeout(statusTimer);
      quitButton.disabled = true;
      quitButton.textContent = "Stopping";
      try {
        if (desktop) {
          await window.genomeExplorer.quit();
        } else {
          await fetch(`${basePath}/api/shutdown`, { method: "POST" });
        }
      } finally {
        document.body.innerHTML = '<main class="shell"><p class="eyebrow">Genome Explorer stopped</p><h1>Your local session has ended.</h1><p class="lede">You can close this tab. Your source bundle was not modified.</p></main>';
      }
    });

    refreshStatus();
  </script>
</body>
</html>'''
