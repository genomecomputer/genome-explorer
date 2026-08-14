from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .core import WorkspaceReport, json_ready, open_bundle, search_workspace


BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"


@dataclass
class PrototypeState:
    archive: str
    status: str = "not opened"
    report: Optional[WorkspaceReport] = None
    last_query: str = ""
    last_kind: str = ""
    last_elapsed: float = 0.0
    hits: Optional[List[dict]] = None
    error: str = ""


def _format_bytes(value: int) -> str:
    units = ["B", "KiB", "MiB", "GiB"]
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return "%.1f %s" % (amount, unit)
        amount /= 1024
    return "%d B" % value


def _render(state: PrototypeState) -> None:
    print(CLEAR, end="")
    print(BOLD + "Selective reader prototype" + RESET)
    print(DIM + "Fully validates the archive, but stores only JSON and Parquet." + RESET)
    print()
    print(BOLD + "archive: " + RESET + state.archive)
    print(BOLD + "status: " + RESET + state.status)
    if state.report:
        report = state.report
        print(BOLD + "workspace: " + RESET + report.workspace)
        print(BOLD + "schema: " + RESET + report.schema_version)
        print(BOLD + "genome build: " + RESET + report.genome_build)
        print(BOLD + "validated: " + RESET + "%d manifest entries" % report.validated_entries)
        print(BOLD + "stored: " + RESET + "%d files, %s" % (
            report.extracted_files, _format_bytes(report.extracted_bytes)
        ))
        print(BOLD + "streamed only: " + RESET + "%d files, %s" % (
            report.skipped_files, _format_bytes(report.skipped_bytes)
        ))
        print(BOLD + "open time: " + RESET + "%.3f s" % report.elapsed_seconds)
    if state.last_query:
        print()
        print(BOLD + "last query: " + RESET + state.last_query)
        print(BOLD + "query kind: " + RESET + state.last_kind)
        print(BOLD + "query time: " + RESET + "%.3f s" % state.last_elapsed)
        print(BOLD + "matches: " + RESET + str(len(state.hits or [])))
        for hit in (state.hits or [])[:5]:
            print("  " + json.dumps(json_ready(hit), sort_keys=True))
    if state.error:
        print()
        print(BOLD + "error: " + RESET + state.error)
    print()
    print(BOLD + "[o]" + RESET + DIM + " open and validate  " + RESET, end="")
    print(BOLD + "[s]" + RESET + DIM + " search  " + RESET, end="")
    print(BOLD + "[q]" + RESET + DIM + " quit" + RESET)


def _workspace_root() -> Path:
    return Path.cwd() / ".genome-explorer" / "workspaces"


def run_tui(archive: str) -> None:
    state = PrototypeState(archive=archive)
    while True:
        _render(state)
        action = input("> ").strip().lower()
        if action == "q":
            return
        if action == "o":
            state.error = ""
            state.status = "opening"
            _render(state)
            try:
                state.report = open_bundle(archive, _workspace_root())
                state.status = "validated and ready"
            except Exception as error:
                state.status = "failed"
                state.error = str(error)
        elif action == "s":
            if not state.report:
                state.error = "open the bundle first"
                continue
            query = input("search: ").strip()
            try:
                result = search_workspace(state.report.workspace, query)
                state.last_query = result.query
                state.last_kind = result.query_kind
                state.last_elapsed = result.elapsed_seconds
                state.hits = result.hits
                state.error = ""
            except Exception as error:
                state.error = str(error)


def run_batch(archive: str, queries: List[str]) -> None:
    report = open_bundle(archive, _workspace_root())
    payload = {
        "report": report.to_dict(),
        "searches": [
            search_workspace(report.workspace, query).to_dict() for query in queries
        ],
    }
    print(json.dumps(json_ready(payload), indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Throwaway selective `.genome` reader prototype"
    )
    parser.add_argument("archive", help="path to a .genome.tar.gz archive")
    parser.add_argument(
        "--batch",
        action="append",
        default=[],
        metavar="QUERY",
        help="open the archive and run a deterministic query without the TUI",
    )
    args = parser.parse_args()
    archive = os.path.abspath(os.path.expanduser(args.archive))
    if args.batch:
        run_batch(archive, args.batch)
    else:
        run_tui(archive)


if __name__ == "__main__":
    main()
