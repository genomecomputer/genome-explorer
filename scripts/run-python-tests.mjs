import { existsSync } from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(scriptDirectory, "..");
const candidates = process.platform === "win32"
  ? [
      path.join(repositoryRoot, ".genome-explorer", "prototype-venv", "Scripts", "python.exe"),
      "python",
    ]
  : [
      path.join(repositoryRoot, ".genome-explorer", "prototype-venv", "bin", "python"),
      "python3",
    ];
const python = candidates.find((candidate) => !candidate.includes(path.sep) || existsSync(candidate));
if (!python) throw new Error("Python is required to run contributor tests.");

const result = spawnSync(
  python,
  ["-m", "unittest", "discover", "-s", "prototype/tests"],
  {
    cwd: repositoryRoot,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    stdio: "inherit",
  },
);
if (result.error) throw result.error;
process.exit(result.status ?? 1);
