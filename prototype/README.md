# Selective reader prototype

This throwaway prototype answers one question: can Genome Explorer fully
validate a compressed `.genome` bundle while storing only the JSON and Parquet
files needed for deterministic local search?

Run it with:

```sh
./prototype/run /path/to/sample.genome.tar.gz
```

The prototype creates an ignored `.genome-explorer/` workspace. It never
modifies the source archive and does not make network requests after the first
prebuilt DuckDB package download.
