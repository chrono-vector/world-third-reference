from dataclasses import replace

from world_third_reference.reconstruction import reconstruct_trace
from world_third_reference.work_trace import WorkTrace


def test_reconstruction_reports_presence_without_promotion():
    trace = WorkTrace("work-demo-006")
    a = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    trace.append(record_type="VERIFICATION_REF", author_component="WEAVER", payload={"verification_result": "PASS"}, expected_previous_digest=a.canonical_record_sha256)
    result = reconstruct_trace(trace.records)
    assert result.status == "RECONSTRUCTION_COMPLETE"
    assert result.authority_presence["WEAVER"] == "PRESENT"
    assert result.authority_presence["HUMAN"] == "NOT_PRESENT"
    assert result.authority_presence["EXTERNAL_IW"] == "NOT_PRESENT"
    assert result.authority_presence["CANONICAL"] == "NOT_PRESENT"
    assert result.authority_presence["PUBLICATION"] == "NOT_PRESENT"


def test_publication_presence_does_not_mean_publication_performed():
    trace = WorkTrace("work-demo-007")
    a = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    trace.append(record_type="PUBLICATION_STATUS_REF", author_component="PUBLICATION", payload={"publication_status": "APPROVED_FOR_PUBLICATION"}, expected_previous_digest=a.canonical_record_sha256)
    result = reconstruct_trace(trace.records)
    assert result.authority_presence["PUBLICATION"] == "PRESENT"
    assert all("publication_performed" not in event for event in result.events)


def test_broken_trace_is_not_repaired():
    trace = WorkTrace("work-demo-008")
    record = trace.append(record_type="INTAKE", author_component="JOB_AGENT", payload={}, expected_previous_digest=None)
    result = reconstruct_trace([replace(record, sequence=3)])
    assert result.status == "TRACE_INTEGRITY_FAILURE"
    assert result.events == ()
