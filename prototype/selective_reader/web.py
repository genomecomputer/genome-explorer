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
    .topic-library-intro { max-width: 660px; margin: 9px 0 0; color: var(--muted); line-height: 1.55; }
    .topic-summary { flex: 0 0 auto; padding-bottom: 3px; color: var(--muted); font-size: 13px; }
    .catalog-note {
      display: flex; align-items: flex-start; gap: 10px; margin-top: 19px; padding: 13px 15px;
      color: #43544c; background: var(--blue-soft); border: 1px solid #d6e5ef; border-radius: 12px;
      font-size: 13px; line-height: 1.5;
    }
    .catalog-note svg { flex: 0 0 auto; margin-top: 1px; }
    .topic-catalog { margin-top: 20px; }
    .topic-indicator { min-width: 0; text-align: right; }
    .topic-indicator-value { display: block; color: var(--accent-dark); font-size: 12px; font-weight: 780; }
    .topic-indicator-detail { display: block; margin-top: 2px; color: var(--muted); font-size: 9px; line-height: 1.35; }
    .topic-indicator.research .topic-indicator-value { color: #37566d; }
    .topic-indicator.no-data .topic-indicator-value { color: var(--muted); font-weight: 680; }
    .topic-browser {
      display: grid; grid-template-columns: 210px minmax(0, 1fr); overflow: hidden;
      background: rgba(255,255,255,.86); border: 1px solid var(--line); border-radius: 16px;
      box-shadow: 0 7px 26px rgba(25,54,43,.045);
    }
    .directory-nav { padding: 15px; background: rgba(243,247,244,.82); border-right: 1px solid var(--line); }
    .directory-nav-label {
      margin: 2px 8px 10px; color: var(--muted); font-size: 10px; font-weight: 800;
      letter-spacing: .09em; text-transform: uppercase;
    }
    .directory-nav-list { display: grid; gap: 4px; }
    .directory-nav-button {
      display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 10px; width: 100%;
      padding: 10px 11px; color: #415149; background: transparent; border: 0; border-radius: 10px;
      font-size: 13px; font-weight: 700; text-align: left; cursor: pointer;
    }
    .directory-nav-button:hover { background: rgba(255,255,255,.82); }
    .directory-nav-button[aria-selected="true"] { color: var(--accent-dark); background: white; box-shadow: 0 1px 5px rgba(25,54,43,.08); }
    .directory-nav-count {
      min-width: 25px; padding: 3px 6px; color: var(--muted); background: rgba(101,115,109,.09);
      border-radius: 999px; font-size: 10px; text-align: center;
    }
    .directory-nav-button[aria-selected="true"] .directory-nav-count { color: var(--accent-dark); background: var(--accent-soft); }
    .directory-main { min-width: 0; padding: 20px; }
    .directory-toolbar { display: grid; grid-template-columns: minmax(0, 1fr) minmax(190px, 260px); align-items: end; gap: 18px; margin-bottom: 20px; }
    .directory-title { margin: 0; font-size: 19px; letter-spacing: -.025em; }
    .directory-description { margin: 5px 0 0; color: var(--muted); font-size: 12px; line-height: 1.45; }
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
      .topic-library-head { align-items: flex-start; flex-direction: column; gap: 8px; }
      .topic-browser { grid-template-columns: 1fr; }
      .directory-nav { border-right: 0; border-bottom: 1px solid var(--line); }
      .directory-nav-list { display: flex; overflow-x: auto; padding-bottom: 2px; }
      .directory-nav-button { flex: 0 0 auto; width: auto; }
      .directory-toolbar { grid-template-columns: 1fr; }
      .section-variants .cards { grid-template-columns: 1fr; }
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
      .simple-fields, .technical-fields, .bundle-facts { grid-template-columns: 1fr; }
      .results-head { align-items: flex-start; flex-direction: column; gap: 5px; }
      .bundle-summary { display: none; }
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
        <button class="quit-button" id="bundles-button" type="button" hidden>Bundles</button>
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
      <p class="eyebrow">Exploring <span id="active-bundle-name">your genome bundle</span></p>
      <h1>What would you like to explore?</h1>
      <p class="lede">Search a medication, trait, condition, or gene. Genome Explorer only shows information already recorded in this bundle.</p>

      <div class="search-panel">
        <form id="search-form">
          <input id="search-input" type="search" aria-label="Search your genome bundle" autocomplete="off" spellcheck="false" placeholder="Try a medication, trait, condition, or gene" autofocus>
          <button class="search-button" id="search-button" type="submit">Search</button>
        </form>
      </div>
      <section class="topic-library" aria-labelledby="topic-library-title">
        <div class="topic-library-head">
          <div>
            <h2 id="topic-library-title">Browse common topics</h2>
            <p class="topic-library-intro">Start with a medication, condition, or everyday trait people often look for.</p>
          </div>
          <div class="topic-summary" id="topic-summary"></div>
        </div>
        <div class="catalog-note">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>
          <span>Highlighted values are person-specific PGx results or polygenic scores already recorded in this bundle. Research context only means the bundle includes general evidence but no person-specific score for this topic.</span>
        </div>
        <div class="topic-catalog" id="topic-catalog"></div>

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
                <div class="bundle-fact"><dt>Nickname</dt><dd id="bundle-nickname">Loading</dd></div>
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
    const bundlesButton = document.querySelector("#bundles-button");
    const quitButton = document.querySelector("#quit-button");
    const desktop = window.genomeExplorer?.desktop === true;
    if (desktop) quitButton.hidden = true;
    let statusTimer = null;
    let explorerReady = false;
    let latestStatus = null;
    let latestTopics = [];

    const fieldLabels = {
      variant_id: "Variant identifier", rsid: "rsID", chrom: "Chromosome", pos: "Position",
      ref: "Reference allele", alt: "Alternate allele", genotype: "Genotype", zygosity: "Zygosity",
      call_confidence: "Call confidence", gene: "Gene annotation", gene_symbol: "Gene",
      hgvsp: "Protein change", clinvar_significance: "ClinVar classification",
      clinvar_review_stars: "ClinVar review stars", clinvar_id: "ClinVar record",
      clinical_grade: "Clinical-grade flag", diplotype: "Recorded diplotype", phenotype: "Recorded phenotype",
      activity_score: "Activity score", copy_number: "Copy number", cpic_level: "CPIC evidence level",
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
      pharmacogenomics: "Bundle pharmacogenomic record", polygenic_scores: "Recorded score",
      gwas: "Research association"
    };

    const primaryFields = {
      variants: ["zygosity", "call_confidence"],
      genes: ["variant_count", "actionable_count"],
      pharmacogenomics: [],
      polygenic_scores: ["percentile", "reference_population"],
      gwas: ["gene", "source"]
    };

    const topicKinds = {
      medications: {
        label: "Medications",
        icon: "Rx",
        prompt: "Could this bundle contain a person-specific pharmacogenomic call linked to this medication?"
      },
      conditions: {
        label: "Conditions",
        icon: "+",
        prompt: "Does this bundle record a score or research association mentioning this condition?"
      },
      traits: {
        label: "Traits",
        icon: "%",
        prompt: "Does this bundle record a score or research association mentioning this trait?"
      }
    };

    const directoryViews = {
      personal: {
        label: "Results in this bundle",
        title: "Person-specific results",
        description: "Personal PGx results and recorded scores. Research-only matches are not included here."
      },
      medications: {
        label: "Medications",
        title: "Medications",
        description: "Common medications, grouped by use. Rows show the phenotype and gene recorded in this bundle."
      },
      conditions: {
        label: "Conditions",
        title: "Conditions",
        description: "Common conditions with recorded polygenic scores when available."
      },
      traits: {
        label: "Traits",
        title: "Traits",
        description: "Everyday traits with recorded polygenic scores when available."
      }
    };

    function isPersonSpecificTopic(topic) {
      const sections = Array.isArray(topic.record_sections) ? topic.record_sections : [];
      return sections.includes("pharmacogenomics") || sections.includes("polygenic_scores");
    }

    function topicIndicator(topic) {
      const personal = topic.personal || {};
      const pgx = Array.isArray(personal.pharmacogenomics) ? personal.pharmacogenomics : [];
      const scores = Array.isArray(personal.polygenic_scores) ? personal.polygenic_scores : [];
      const researchCount = Number(topic.research_association_count || 0);
      const indicator = document.createElement("span");
      indicator.className = "topic-indicator";
      const value = document.createElement("span");
      value.className = "topic-indicator-value";
      const detail = document.createElement("span");
      detail.className = "topic-indicator-detail";

      if (pgx.length === 1) {
        value.textContent = pgx[0].phenotype || pgx[0].diplotype || "Recorded PGx result";
        detail.textContent = `Recorded PGx · ${pgx[0].gene_symbol}`;
      } else if (pgx.length > 1) {
        value.textContent = `${pgx.length} recorded PGx results`;
        detail.textContent = pgx.map(record => record.gene_symbol).join(", ");
      } else if (scores.length === 1) {
        const percentile = Number(scores[0].percentile).toLocaleString(undefined, { maximumFractionDigits: 1 });
        value.textContent = `${percentile}th percentile`;
        detail.textContent = "Recorded polygenic score";
      } else if (scores.length > 1) {
        value.textContent = `${scores.length} recorded scores`;
        detail.textContent = "Person-specific values in this bundle";
      } else if (researchCount > 0) {
        indicator.classList.add("research");
        value.textContent = "Research context only";
        detail.textContent = "No person-specific score recorded";
      } else {
        indicator.classList.add("no-data");
        value.textContent = "No personal topic data";
        detail.textContent = "This is not a negative result";
      }
      indicator.append(value, detail);
      return indicator;
    }

    function directoryRow(topic) {
      const row = document.createElement("button");
      row.className = "directory-row";
      row.type = "button";
      row.dataset.topicQuery = topic.query;
      row.setAttribute("aria-label", `Search this bundle for ${topic.label}`);
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
          : "This bundle does not contain a personal PGx result or recorded score for these common topics.";
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
      let viewValue = topics.some(isPersonSpecificTopic) ? "personal" : "medications";

      const nav = document.createElement("aside");
      nav.className = "directory-nav";
      const navLabel = document.createElement("p");
      navLabel.className = "directory-nav-label";
      navLabel.textContent = "Browse by";
      const navList = document.createElement("div");
      navList.className = "directory-nav-list";
      navList.setAttribute("role", "tablist");

      const main = document.createElement("div");
      main.className = "directory-main";
      const toolbar = document.createElement("div");
      toolbar.className = "directory-toolbar";
      const toolbarCopy = document.createElement("div");
      const title = document.createElement("h3");
      title.className = "directory-title";
      const description = document.createElement("p");
      description.className = "directory-description";
      toolbarCopy.append(title, description);
      const filter = document.createElement("input");
      filter.className = "directory-filter";
      filter.type = "search";
      filter.setAttribute("aria-label", "Filter common topics");
      const listHost = document.createElement("div");

      const viewCount = key => topics.filter(topic => key === "personal" ? isPersonSpecificTopic(topic) : topic.kind === key).length;
      const refresh = () => {
        const view = directoryViews[viewValue];
        title.textContent = view.title;
        description.textContent = view.description;
        filter.placeholder = viewValue === "personal" ? "Filter results" : `Filter ${view.label.toLowerCase()}`;
        navList.querySelectorAll(".directory-nav-button").forEach(control => {
          control.setAttribute("aria-selected", String(control.dataset.directoryView === viewValue));
        });
        listHost.replaceChildren(directoryGroups(topics, viewValue, filterValue));
      };

      Object.entries(directoryViews).forEach(([key, view]) => {
        const control = document.createElement("button");
        control.className = "directory-nav-button";
        control.type = "button";
        control.dataset.directoryView = key;
        control.setAttribute("role", "tab");
        const label = document.createElement("span");
        label.textContent = view.label;
        const count = document.createElement("span");
        count.className = "directory-nav-count";
        count.textContent = viewCount(key);
        control.append(label, count);
        control.addEventListener("click", () => {
          viewValue = key;
          filterValue = "";
          filter.value = "";
          refresh();
        });
        navList.append(control);
      });

      filter.addEventListener("input", () => {
        filterValue = filter.value;
        refresh();
      });
      nav.append(navLabel, navList);
      toolbar.append(toolbarCopy, filter);
      main.append(toolbar, listHost);
      wrapper.append(nav, main);
      refresh();
      return wrapper;
    }

    function renderTopicCatalog(topics) {
      latestTopics = Array.isArray(topics) ? topics : [];
      topicSummary.textContent = `${latestTopics.length} searchable topics`;
      topicCatalog.replaceChildren(renderDirectory(latestTopics));
    }

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
      meta.textContent = `${entry.file_name} · ${entry.genome_build} · ${formatBundleDate(entry.generated_at)}`;
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
      document.querySelector("#bundle-nickname").textContent = nickname;
      document.querySelector("#validation").textContent = cached ? "Previously verified" : "Verified";
      document.querySelector("#build").textContent = status.genome_build;
      document.querySelector("#snapshot").textContent = new Date(status.generated_at).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
      document.querySelector("#stored").textContent = formatBytes(status.stored_bytes);
      document.querySelector("#bundle-summary").textContent = cached ? "Previously verified and ready" : "Verified and ready";
    }

    function renderAppStatus(status) {
      renderBundleLibrary(status);
      if (status.status === "ready") {
        welcome.hidden = true;
        explorer.hidden = false;
        bundlesButton.hidden = !(status.bundles || []).length;
        bundlesButton.disabled = false;
        chooseButton.disabled = false;
        populateBundleStatus(status);
        renderTopicCatalog(status.topics);
        if (!explorerReady) {
          explorerReady = true;
          input.value = "";
          results.hidden = true;
          content.replaceChildren();
          input.focus();
        }
        return;
      }

      welcome.hidden = false;
      explorer.hidden = true;
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
      if (hit.section === "pharmacogenomics") {
        return hit.gene_symbol;
      }
      if (hit.section === "variants") return hit.gene || hit.rsid || "Recorded variant";
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
      if (hit.section === "gwas") {
        return "External population evidence recorded in the bundle";
      }
      return hit.rsid ? `Identifier: ${hit.rsid}` : "";
    }

    function summaryFor(hit) {
      if (hit.section === "pharmacogenomics") {
        return `This bundle contains a person-specific pharmacogenomic result for ${hit.gene_symbol}.`;
      }
      if (hit.section === "polygenic_scores") return `The bundle contains a recorded score for ${hit.trait}.`;
      if (hit.section === "gwas") {
        const identifier = hit.rsid || hit.variant_id || "this variant";
        return `The bundle includes an external research association between ${identifier} and ${hit.trait}.`;
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
        return `${hit.gene} is named by the external research source. This association has not been presented as a match to this person's genome.`;
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
      subtitle.textContent = subtitleFor(hit, query);
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

      if (hit.section === "pharmacogenomics") {
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
      const hasClearerRecord = Boolean(
        grouped.pharmacogenomics?.length ||
        grouped.polygenic_scores?.length
      );
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

    topicCatalog.addEventListener("click", event => {
      const trigger = event.target.closest("[data-topic-query]");
      if (!trigger) return;
      input.value = trigger.dataset.topicQuery;
      search(input.value);
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
