from dataclasses import replace

import pytest

from world_third_reference.work_trace import (
    AppendConflict,
    TraceIntegrityError,
    WorkTrace,
    verify_trace,
)


def test_append_chain_and_verify():
    trace = WorkTrace("work-demo-001")
    first = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={"request": "synthetic"}, expected_previous_digest=None)
    second = trace.append(record_type="AUTHORIZATION_REF", author_component="VECTOR", payload={"decision": "bounded-demo"}, expected_previous_digest=first.canonical_record_sha256)
    verified = verify_trace(trace.records)
    assert len(verified) == 2
    assert second.previous_record_digest == first.canonical_record_sha256


def test_stale_cas_fails_closed():
    trace = WorkTrace("work-demo-002")
    first = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    with pytest.raises(AppendConflict, match="APPEND_CONFLICT"):
        trace.append(record_type="AUTHORIZATION_REF", author_component="VECTOR", payload={}, expected_previous_digest=None)
    assert trace.head_digest == first.canonical_record_sha256


def test_payload_tamper_is_rejected():
    trace = WorkTrace("work-demo-003")
    record = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={"a": 1}, expected_previous_digest=None)
    with pytest.raises(TraceIntegrityError, match="PAYLOAD_DIGEST_MISMATCH"):
        verify_trace([replace(record, payload={"a": 2})])


def test_record_digest_tamper_is_rejected():
    trace = WorkTrace("work-demo-004")
    record = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={"a": 1}, expected_previous_digest=None)
    with pytest.raises(TraceIntegrityError, match="RECORD_DIGEST_MISMATCH"):
        verify_trace([replace(record, canonical_record_sha256="0" * 64)])


def test_reordering_is_rejected():
    trace = WorkTrace("work-demo-005")
    first = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    trace.append(record_type="AUTHORIZATION_REF", author_component="VECTOR", payload={}, expected_previous_digest=first.canonical_record_sha256)
    with pytest.raises(TraceIntegrityError):
        verify_trace(reversed(trace.records))


def test_cross_work_mismatch_is_rejected():
    a = WorkTrace("work-a")
    r0 = a.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    b = WorkTrace("work-b")
    r1 = b.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    forged = replace(r1, sequence=1, previous_record_digest=r0.canonical_record_sha256)
    with pytest.raises(TraceIntegrityError):
        verify_trace([r0, forged])
