#!/usr/bin/env python3
"""Synthetic demo: APPROVED_FOR_PUBLICATION ≠ publication performed.

This script only appends reference records. It does not call network APIs,
upload files, push releases, or otherwise publish.
"""

from __future__ import annotations

from world_third_reference import WorkTrace, reconstruct_trace
from world_third_reference.work_trace import verify_trace


def main() -> int:
    trace = WorkTrace("demo-publication-separation-001")

    r0 = trace.append(
        record_type="INTAKE",
        author_component="JOB_AGENT",
        payload={"task": "synthetic publication separation"},
        expected_previous_digest=None,
    )
    r1 = trace.append(
        record_type="HUMAN_REVIEW_REF",
        author_component="HUMAN",
        payload={"decision": "REVIEWED_SYNTHETIC"},
        expected_previous_digest=r0.canonical_record_sha256,
    )
    r2 = trace.append(
        record_type="CANONICAL_STATUS_REF",
        author_component="CANONICAL",
        payload={"canonical_status": "DESIGNATED_SYNTHETIC"},
        expected_previous_digest=r1.canonical_record_sha256,
    )
    trace.append(
        record_type="PUBLICATION_STATUS_REF",
        author_component="PUBLICATION",
        payload={"publication_status": "APPROVED_FOR_PUBLICATION"},
        expected_previous_digest=r2.canonical_record_sha256,
    )

    verify_trace(trace.records)
    result = reconstruct_trace(trace.records)

    publication_present = result.authority_presence["PUBLICATION"] == "PRESENT"
    publication_performed = False

    print(f"work_id: {trace.work_id}")
    print(f"records: {len(trace.records)}")
    print(f"publication_authority_record_present: {str(publication_present).lower()}")
    print(f"publication_performed: {str(publication_performed).lower()}")
    print()
    print("note: PUBLICATION presence means a status reference was recorded.")
    print("note: no publish action, network call, or upload was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
