# WORLD THIRD Quickstart

Run this reference implementation in about 5–10 minutes.

## 1. What this is

WORLD THIRD is a reference architecture for separating:

* capability
* authority
* enforcement
* execution
* verification
* human judgment
* independent witness status
* canonical designation
* publication

This repository is an educational/reference package. It is **not** an AI agent framework and **not** a production security system.

The center pipeline is:

```text
FIND → AUTHORIZE → ENFORCE → EXECUTE → VERIFY → HUMAN FINAL → LEARN
```

Core separations to keep in mind:

```text
Capability ≠ Authority
Authorization ≠ Execution
Execution ≠ Verification
Self-check ≠ Independent Verification
Verification ≠ Human Acceptance
Human ACCEPTED ≠ IW ACCEPTED
Human ACCEPTED ≠ Canonical
IW ACCEPTED ≠ Canonical
Canonical ≠ Publication
APPROVED_FOR_PUBLICATION ≠ publication performed
State ≠ Evidence
Classification ≠ Verdict
```

## 2. Requirements

* Python 3.10+
* pytest

## 3. Clone and run

```bash
git clone https://github.com/chrono-vector/world-third-reference.git
cd world-third-reference
python -m pytest -q
```

At the current `v0.1.0` baseline this suite reported `19 passed`. The suite may grow; treat the latest local run as the source of truth.

## 4. Minimal example

The public API records **reference records** in a Work Trace. Appending a record does **not** mean this package performed authorization, enforcement, execution, verification, human acceptance, canonical designation, or publication. It only stores synthetic references for teaching the lifecycle.

```python
from dataclasses import replace

from world_third_reference import WorkTrace, reconstruct_trace
from world_third_reference.work_trace import TraceIntegrityError, verify_trace

trace = WorkTrace("demo-001")

r0 = trace.append(
    record_type="INTAKE",
    author_component="JOB_AGENT",
    payload={"task": "synthetic example"},
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

r4 = trace.append(
    record_type="VERIFICATION_REF",
    author_component="WEAVER",
    payload={"verification_result": "PASS_SYNTHETIC"},
    expected_previous_digest=r3.canonical_record_sha256,
)

result = reconstruct_trace(trace.records)
print(result.authority_presence)
```

Expected presence for this synthetic chain:

* `WEAVER` = `PRESENT`
* `HUMAN` = `NOT_PRESENT`
* `EXTERNAL_IW` = `NOT_PRESENT`
* `CANONICAL` = `NOT_PRESENT`
* `PUBLICATION` = `NOT_PRESENT`

Most important: a `VERIFICATION_REF` does **not** become Human acceptance. Verification and human judgment remain separate authority lanes.

Run the packaged demos:

```bash
PYTHONPATH=src python examples/basic_flow.py
PYTHONPATH=src python examples/publication_separation.py
```

## 5. Tamper example

Integrity checks reject payload mutation and reordering. An integrity failure means the chain no longer verifies locally. It is **not** proof of a malicious actor.

```python
# continuing from the minimal example above

tampered = replace(r0, payload={"task": "altered"})
try:
    verify_trace([tampered, r1, r2, r3, r4])
except TraceIntegrityError as exc:
    print("integrity failure:", exc)

reordered = (r1, r0, r2, r3, r4)
try:
    verify_trace(reordered)
except TraceIntegrityError as exc:
    print("integrity failure:", exc)
```

## 6. What this demo does NOT prove

* external truth
* real authorization
* real enforcement
* human acceptance
* independent verification
* production security
* publication

See `BOUNDARIES_AND_NONCLAIMS.md` for the full nonclaim set.
