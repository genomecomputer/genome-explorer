"""Throwaway logic prototype.

Question: Which bundle-evidence states make a topic useful without implying a
new health interpretation, and when should external research be visible?

Run with: npm run prototype:topic-states
"""

from __future__ import annotations

from dataclasses import replace

from topic_evidence_state import TopicEvidence, present_topic


BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"


def render(evidence: TopicEvidence) -> None:
    presentation = present_topic(evidence)
    print(CLEAR, end="")
    print(BOLD + "Topic evidence state prototype" + RESET)
    print(DIM + "Does this topic have a reason to appear in a private genome explorer?" + RESET)
    print()
    print(BOLD + "Bundle evidence" + RESET)
    print(f"pgx phenotype: {evidence.pgx_phenotype or 'none'}")
    print(f"prs percentile: {evidence.prs_percentile if evidence.prs_percentile is not None else 'none'}")
    print(f"person-linked variant annotations: {evidence.has_person_linked_variants}")
    print(f"general research table matches: {evidence.has_general_research}")
    print()
    print(BOLD + "Presentation" + RESET)
    print(f"state: {presentation.state}")
    print(f"headline: {presentation.headline}")
    print(f"detail: {presentation.detail}")
    print(f"result order: {', '.join(presentation.result_order) or 'no result page'}")
    print(f"show general research: {presentation.show_general_research}")
    print()
    print(BOLD + "[p]" + RESET + DIM + " toggle PGx  " + RESET, end="")
    print(BOLD + "[s]" + RESET + DIM + " toggle score  " + RESET, end="")
    print(BOLD + "[v]" + RESET + DIM + " toggle person-linked variants  " + RESET, end="")
    print(BOLD + "[g]" + RESET + DIM + " toggle general research  " + RESET, end="")
    print(BOLD + "[r]" + RESET + DIM + " reset  " + RESET, end="")
    print(BOLD + "[q]" + RESET + DIM + " quit" + RESET)


def main() -> None:
    evidence = TopicEvidence()
    while True:
        render(evidence)
        action = input("> ").strip().lower()
        if action == "q":
            return
        if action == "p":
            evidence = replace(
                evidence,
                pgx_phenotype="Rapid Metabolizer" if not evidence.pgx_phenotype else "",
            )
        elif action == "s":
            evidence = replace(
                evidence,
                prs_percentile=85.0 if evidence.prs_percentile is None else None,
            )
        elif action == "v":
            evidence = replace(
                evidence,
                has_person_linked_variants=not evidence.has_person_linked_variants,
            )
        elif action == "g":
            evidence = replace(
                evidence,
                has_general_research=not evidence.has_general_research,
            )
        elif action == "r":
            evidence = TopicEvidence()


if __name__ == "__main__":
    main()
