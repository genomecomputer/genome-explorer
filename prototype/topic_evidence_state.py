"""Pure topic-evidence state model for the throwaway TUI prototype."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TopicEvidence:
    pgx_phenotype: str = ""
    prs_percentile: float | None = None
    has_person_linked_variants: bool = False
    has_general_research: bool = False


@dataclass(frozen=True)
class TopicPresentation:
    state: str
    headline: str
    detail: str
    result_order: tuple[str, ...]
    show_general_research: bool


def present_topic(evidence: TopicEvidence) -> TopicPresentation:
    if evidence.pgx_phenotype:
        return TopicPresentation(
            state="recorded_pgx",
            headline=evidence.pgx_phenotype,
            detail="Person-specific PGx result recorded",
            result_order=("pgx",),
            show_general_research=False,
        )
    if evidence.prs_percentile is not None:
        return TopicPresentation(
            state="recorded_score",
            headline=f"{evidence.prs_percentile:g}th percentile",
            detail="Person-specific polygenic score recorded",
            result_order=("prs",),
            show_general_research=False,
        )
    if evidence.has_person_linked_variants:
        return TopicPresentation(
            state="related_personal_records",
            headline="Related records found",
            detail="Recorded annotations connect this genome to the topic",
            result_order=("person_linked_variants", "exact_supporting_research"),
            show_general_research=evidence.has_general_research,
        )
    return TopicPresentation(
        state="no_person_specific_result",
        headline="No personal result recorded",
        detail="This is not a negative result",
        result_order=(),
        show_general_research=False,
    )
