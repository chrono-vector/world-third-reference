"""Read-only reconstruction example.

Reconstruction reports what is present in a trace.
It does not create decisions, repair history, resolve authority ambiguity,
or promote one state into another.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .work_trace import TraceIntegrityError, WorkTraceRecord, verify_trace


@dataclass(frozen=True)
class ReconstructionResult:
    status: str
    work_id: str | None
    event_count: int
    authority_presence: dict[str, str]
    events: tuple[dict[str, Any], ...]
    warnings: tuple[str, ...]


AUTHORITY_BY_RECORD_TYPE = {
    "INTAKE": "JOB_AGENT",
    "AUTHORIZATION_REF": "VECTOR",
    "ENFORCEMENT_RECEIPT": "EIG",
    "DENY_RECEIPT": "EIG",
    "EXECUTION_REF": "EXECUTOR",
    "EXECUTION_FAILURE_REF": "EXECUTOR",
    "VERIFICATION_REF": "WEAVER",
    "HUMAN_REVIEW_REF": "HUMAN",
    "EXTERNAL_IW_REF": "EXTERNAL_IW",
    "CANONICAL_STATUS_REF": "CANONICAL",
    "PUBLICATION_STATUS_REF": "PUBLICATION",
}


def reconstruct_trace(records: Iterable[WorkTraceRecord]) -> ReconstructionResult:
    items = tuple(records)
    if not items:
        return ReconstructionResult(
            status="WORK_NOT_FOUND",
            work_id=None,
            event_count=0,
            authority_presence={},
            events=(),
            warnings=(),
        )

    try:
        verified = verify_trace(items)
    except TraceIntegrityError as exc:
        return ReconstructionResult(
            status="TRACE_INTEGRITY_FAILURE",
            work_id=items[0].work_id if items else None,
            event_count=len(items),
            authority_presence={},
            events=(),
            warnings=(str(exc),),
        )

    present: set[str] = set()
    events: list[dict[str, Any]] = []

    for record in verified:
        authority = AUTHORITY_BY_RECORD_TYPE.get(record.record_type, "OTHER")
        present.add(authority)
        events.append(
            {
                "sequence": record.sequence,
                "record_type": record.record_type,
                "authority_class": authority,
                "record_digest": record.canonical_record_sha256,
            }
        )

    known = {
        "JOB_AGENT",
        "VECTOR",
        "EIG",
        "EXECUTOR",
        "WEAVER",
        "HUMAN",
        "EXTERNAL_IW",
        "CANONICAL",
        "PUBLICATION",
    }
    matrix = {name: ("PRESENT" if name in present else "NOT_PRESENT") for name in sorted(known)}

    return ReconstructionResult(
        status="RECONSTRUCTION_COMPLETE",
        work_id=verified[0].work_id,
        event_count=len(verified),
        authority_presence=matrix,
        events=tuple(events),
        warnings=(),
    )
