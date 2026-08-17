import { _electron as electron, expect, test } from "@playwright/test";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const repositoryRoot = path.resolve(__dirname, "..");
const sampleBundle = process.env.GENOME_EXPLORER_TEST_BUNDLE;
const clinicalBundle = process.env.GENOME_EXPLORER_CLINICAL_TEST_BUNDLE;

function processIsAlive(pid: number): boolean {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function waitForProcessExit(pid: number): Promise<void> {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    if (!processIsAlive(pid)) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Genome engine process ${pid} remained alive after the app closed.`);
}

test("opens, searches, reuses a bundle, and owns engine shutdown", async () => {
  test.skip(!sampleBundle || !existsSync(sampleBundle), "Set GENOME_EXPLORER_TEST_BUNDLE to a synthetic bundle.");

  const userData = mkdtempSync(path.join(os.tmpdir(), "genome-explorer-electron-"));
  const pidFile = path.join(userData, "engine.pid");
  const environment = {
    ...process.env,
    GENOME_EXPLORER_TEST_BUNDLE: sampleBundle,
    GENOME_EXPLORER_TEST_PID_FILE: pidFile,
    GENOME_EXPLORER_USER_DATA: userData,
  };
  const executablePath = process.env.GENOME_EXPLORER_EXECUTABLE;
  const launchOptions = executablePath
    ? { executablePath, args: [] as string[], cwd: repositoryRoot, env: environment }
    : { args: [repositoryRoot], cwd: repositoryRoot, env: environment };

  let firstApp: Awaited<ReturnType<typeof electron.launch>> | undefined;
  let secondApp: Awaited<ReturnType<typeof electron.launch>> | undefined;
  try {
    firstApp = await electron.launch(launchOptions);
    const firstWindow = await firstApp.firstWindow();
    await expect(firstWindow.getByRole("heading", { name: "Explore your genome bundle privately." })).toBeVisible();
    await expect(firstWindow.locator("#quit-button")).toBeHidden();
    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      mkdirSync(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, { recursive: true });
      await firstWindow.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "welcome.png"),
      });
    }

    await firstWindow.getByRole("button", { name: "Add genome bundle" }).click();
    await expect(firstWindow.locator("#explorer")).toBeVisible({ timeout: 90_000 });
    await expect(firstWindow.locator("#validation")).toHaveText("Verified");
    await expect(firstWindow.locator(".topic-browser")).toBeVisible();
    await expect(firstWindow.getByRole("tab", { name: /Results in this bundle/ })).toHaveAttribute("aria-selected", "true");
    await expect(firstWindow.locator(".directory-row").first()).toBeVisible();
    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      await firstWindow.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "topic-library.png"),
        fullPage: true,
      });
    }
    await firstWindow.getByRole("tab", { name: /Conditions/ }).click();
    const pcosTopic = firstWindow.getByRole("button", { name: "Search this bundle for PCOS" });
    await expect(pcosTopic.locator(".topic-indicator-value")).toHaveText("85th percentile");
    await firstWindow.getByRole("tab", { name: /Traits/ }).click();
    const cholesterolTopic = firstWindow.getByRole("button", { name: "Search this bundle for Cholesterol levels" });
    await expect(cholesterolTopic.locator(".topic-indicator-value")).toHaveText("Related variants");
    const lactoseTopic = firstWindow.getByRole("button", { name: "Search this bundle for Lactose intolerance" });
    await expect(lactoseTopic.locator(".topic-indicator")).toHaveClass(/no-data/);
    await expect(lactoseTopic.locator(".topic-indicator-value")).toHaveText("No personal result");
    await lactoseTopic.click();
    await expect(firstWindow.locator("#results-title")).toHaveText("No personal result recorded");
    await expect(firstWindow.locator(".section-gwas")).toHaveCount(0);
    const cholesterolBounds = await cholesterolTopic.boundingBox();
    expect(cholesterolBounds).not.toBeNull();
    if (!cholesterolBounds) throw new Error("Cholesterol topic row has no bounding box.");
    await firstWindow.mouse.click(cholesterolBounds.x + 6, cholesterolBounds.y + cholesterolBounds.height / 2);
    await expect(firstWindow.getByText("Related variants", { exact: true }).last()).toBeVisible();
    await expect(firstWindow.getByText("High density lipoprotein cholesterol levels").first()).toBeVisible();
    const firstPersonalRecord = firstWindow.locator(".section-trait_variants .card").first();
    await expect(firstPersonalRecord.locator(".record-type, .recorded-summary, .meaning-note")).toHaveCount(0);
    await expect(firstPersonalRecord.getByText("G / C")).toBeVisible();
    await expect(firstPersonalRecord.getByRole("link", { name: "PubMed 34887591" })).toHaveAttribute(
      "href",
      "https://pubmed.ncbi.nlm.nih.gov/34887591/",
    );
    await expect(firstWindow.getByText("Research sources")).toBeVisible();
    await expect(firstWindow.getByText(/has not been presented as a match/)).toHaveCount(0);
    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      await firstWindow.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "person-linked-topic.png"),
        fullPage: true,
      });
    }
    const supportingResearch = firstWindow.locator(".section-gwas");
    await supportingResearch.locator(":scope > .result-disclosure > summary").click();
    await expect(supportingResearch.getByText("GWAS Catalog").first()).toBeVisible();
    await expect(supportingResearch.getByRole("link", { name: /PubMed/ }).first()).toHaveAttribute(
      "href",
      /pubmed\.ncbi\.nlm\.nih\.gov\/\d+\/$/,
    );
    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      await firstWindow.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "supporting-research.png"),
        fullPage: true,
      });
    }
    await firstWindow.getByRole("tab", { name: /Medications/ }).click();
    await expect(firstWindow.locator(".directory-row")).toHaveCount(15);

    await firstWindow.getByRole("searchbox", { name: "Search your genome bundle" }).fill("CYP2C19");
    await firstWindow.getByRole("button", { name: "Search", exact: true }).click();
    await expect(firstWindow.locator("#results-title")).toHaveText("What the bundle records");
    await expect(firstWindow.getByText("Person-specific data from this bundle").first()).toBeVisible();
    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      await firstWindow.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "search-results.png"),
        fullPage: true,
      });
    }

    const firstEnginePid = Number.parseInt(readFileSync(pidFile, "utf8"), 10);
    await firstApp.close();
    firstApp = undefined;
    await waitForProcessExit(firstEnginePid);

    secondApp = await electron.launch(launchOptions);
    const secondWindow = await secondApp.firstWindow();
    await expect(secondWindow.getByRole("heading", { name: "Choose a genome bundle." })).toBeVisible();
    await expect(secondWindow.locator(".bundle-item")).toHaveCount(1);
    await secondWindow.locator(".bundle-open").click();
    await expect(secondWindow.locator("#explorer")).toBeVisible();
    await expect(secondWindow.locator("#validation")).toHaveText("Previously verified");

    const secondEnginePid = Number.parseInt(readFileSync(pidFile, "utf8"), 10);
    await secondApp.close();
    secondApp = undefined;
    await waitForProcessExit(secondEnginePid);
  } finally {
    if (secondApp) await secondApp.close().catch(() => undefined);
    if (firstApp) await firstApp.close().catch(() => undefined);
    rmSync(userData, { recursive: true, force: true });
  }
});

test("shows clinical-grade findings with person calls and ClinVar evidence", async () => {
  test.skip(!clinicalBundle || !existsSync(clinicalBundle), "Set GENOME_EXPLORER_CLINICAL_TEST_BUNDLE to a synthetic v1.1 bundle.");

  const userData = mkdtempSync(path.join(os.tmpdir(), "genome-explorer-clinical-"));
  const pidFile = path.join(userData, "engine.pid");
  const environment = {
    ...process.env,
    GENOME_EXPLORER_TEST_BUNDLE: clinicalBundle,
    GENOME_EXPLORER_TEST_PID_FILE: pidFile,
    GENOME_EXPLORER_USER_DATA: userData,
  };
  const executablePath = process.env.GENOME_EXPLORER_EXECUTABLE;
  const launchOptions = executablePath
    ? { executablePath, args: [] as string[], cwd: repositoryRoot, env: environment }
    : { args: [repositoryRoot], cwd: repositoryRoot, env: environment };

  let app: Awaited<ReturnType<typeof electron.launch>> | undefined;
  try {
    app = await electron.launch(launchOptions);
    const window = await app.firstWindow();
    await window.getByRole("button", { name: "Add genome bundle" }).click();
    await expect(window.locator("#explorer")).toBeVisible({ timeout: 30_000 });

    const clinicalRow = window.getByRole("button", { name: "Search this bundle for Clinical findings" });
    await expect(clinicalRow.locator(".topic-indicator-value")).toHaveText("2 clinical findings");
    await clinicalRow.click();

    const section = window.locator(".section-clinical_findings");
    await expect(section.getByText("Clinical findings", { exact: true })).toBeVisible();
    const firstFinding = section.locator(".card").first();
    await expect(firstFinding.getByRole("heading", { name: "Dihydropyrimidine dehydrogenase deficiency" })).toBeVisible();
    await expect(firstFinding.locator(":scope > .simple-fields").getByText("Likely pathogenic", { exact: true })).toBeVisible();
    await expect(firstFinding.locator(":scope > .simple-fields").getByText("A / T", { exact: true })).toBeVisible();
    await expect(firstFinding.locator(":scope > .simple-fields").getByText("high", { exact: true })).toBeVisible();
    await expect(firstFinding.locator(":scope > .simple-fields").getByText("reviewed by expert panel", { exact: true })).toBeVisible();
    await expect(firstFinding.getByRole("link", { name: "ClinVar VCV000307730" })).toHaveAttribute(
      "href",
      "https://www.ncbi.nlm.nih.gov/clinvar/?term=VCV000307730",
    );
    await expect(section.getByText(/Conflicting ClinVar submissions/)).toBeVisible();

    if (process.env.GENOME_EXPLORER_SCREENSHOT_DIR) {
      mkdirSync(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, { recursive: true });
      await window.screenshot({
        path: path.join(process.env.GENOME_EXPLORER_SCREENSHOT_DIR, "clinical-findings.png"),
        fullPage: true,
      });
    }

    const enginePid = Number.parseInt(readFileSync(pidFile, "utf8"), 10);
    await app.close();
    app = undefined;
    await waitForProcessExit(enginePid);
  } finally {
    if (app) await app.close().catch(() => undefined);
    rmSync(userData, { recursive: true, force: true });
  }
});
