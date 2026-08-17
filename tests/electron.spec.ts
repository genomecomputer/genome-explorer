import { _electron as electron, expect, test } from "@playwright/test";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";

const repositoryRoot = path.resolve(__dirname, "..");
const sampleBundle = process.env.GENOME_EXPLORER_TEST_BUNDLE;

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
