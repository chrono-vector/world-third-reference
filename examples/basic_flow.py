#!/usr/bin/env python3
"""Synthetic WORLD THIRD basic flow demo.

Records reference entries only. This script does not authorize, enforce,
execute, verify independently, accept as a human, designate canonical status,
or publish anything.
"""

from __future__ import annotations

from world_third_reference import WorkTrace, reconstruct_trace
from world_third_reference.work_trace import verify_trace

PRESENCE_ORDER = (
    "JOB_AGENT",
    "VECTOR",
    "EIG",
    "EXECUTOR",
    "WEAVER",
    "HUMAN",
    "EXTERNAL_IW",
    "CANONICAL",
    "PUBLICATION",
)


def main() -> int:
    trace = WorkTrace("demo-world-third-001")

    r0 = trace.append(
        record_type="INTAKE",
        author_component="JOB_AGENT",
        payload={"task": "synthetic basic flow"},
        expected_previous_digest=None,
    )
    r1 = trace.append(
        record_type="AUTHORIZATION_REF",
        author_component="VECTOR",
        payload={"decision": "ALLOW_SYNTHETIC"},
        expected_previous_digest=r0.canonical_record_sha256,
    )
    r2 = trace.append(
        record_type="ENFORCEMENT_RECEIPT",
        author_component="EIG",
        payload={"receipt": "synthetic-bounds-noted"},
        expected_previous_digest=r1.canonical_record_sha256,
    )
    r3 = trace.append(
        record_type="EXECUTION_REF",
        author_component="EXECUTOR",
        payload={"result": "synthetic-output"},
        expected_previous_digest=r2.canonical_record_sha256,
    )
    trace.append(
        record_type="VERIFICATION_REF",
        author_component="WEAVER",
        payload={"verification_result": "PASS_SYNTHETIC"},
        expected_previous_digest=r3.canonical_record_sha256,
    )

    # Integrity label comes only from verify_trace(), not from reconstruction.
    verify_trace(trace.records)
    result = reconstruct_trace(trace.records)

    print(f"work_id: {trace.work_id}")
    print(f"records: {len(trace.records)}")
    print("trace_integrity: VALID")
    print()
    print("authority_presence:")
    for name in PRESENCE_ORDER:
        print(f"  {name}: {result.authority_presence[name]}")
    print()
    print("verification_does_not_equal_human_acceptance: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
