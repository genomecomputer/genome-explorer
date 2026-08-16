# Selective reader prototype

This throwaway prototype answers one question: can Genome Explorer fully
validate a compressed `.genome` bundle while storing only the JSON and Parquet
files needed for deterministic local search?

Run it with:

```sh
./prototype/run /path/to/sample.genome.tar.gz
```

Open the local browser interface with:

```sh
./prototype/run /path/to/sample.genome.tar.gz --serve
```

Build a double-clickable macOS app with:

```sh
./prototype/build app
open "./dist/Genome Explorer.app"
```

Opening the app without arguments presents a native bundle picker, then opens
the private local interface in the default browser. Its retained workspace is
stored under `~/Library/Application Support/Genome Explorer/`.

Build a standalone command-line executable with:

```sh
./prototype/build cli
./dist/genome-explorer /path/to/sample.genome.tar.gz --serve
```

The prototype creates an ignored `.genome-explorer/` workspace. It never
modifies the source archive and does not make network requests after the first
prebuilt DuckDB package download.

The first open performs full manifest and hash validation and writes a local
validation receipt. Later opens reuse that workspace only while the archive's
path, size, modification time, device, and inode still match and retained file
sizes remain intact. Pass `--verify` to force full validation again.
