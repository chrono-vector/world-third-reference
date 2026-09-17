# WORLD THIRD Architecture

This document summarizes the public reference architecture. The repository demonstrates separation concepts with synthetic records. It does **not** ship production implementations of every named component.

## Lifecycle

| Stage | Role | Question |
| --- | --- | --- |
| FIND | Job Agent | What work is being proposed? |
| AUTHORIZE | VECTOR | Is this work allowed within defined bounds? |
| ENFORCE | EIG | Are those bounds enforced at execution time? |
| EXECUTE | Executor | What actually happened? |
| VERIFY | Weaver Forge | Does the evidence/result satisfy declared checks? |
| HUMAN FINAL | Human | What does the human decide? |
| LEARN | downstream | What may be learned without rewriting authority history? |

Pipeline reminder:

```text
FIND → AUTHORIZE → ENFORCE → EXECUTE → VERIFY → HUMAN FINAL → LEARN
```

## Separate authority lanes

After verification, additional lanes remain distinct:

* **Human** — explicit human review / acceptance decision
* **External IW** — independent witness status, separate from Weaver checks
* **Canonical** — designation of canonical status, not automatic from acceptance
* **Publication** — publication *approval* records, not the act of publishing

Keep these inequalities intact:

```text
Verification ≠ Human Acceptance
Human ACCEPTED ≠ IW ACCEPTED
Human ACCEPTED ≠ Canonical
IW ACCEPTED ≠ Canonical
Canonical ≠ Publication
APPROVED_FOR_PUBLICATION ≠ publication performed
```

## Work Trace

The reference Work Trace is an append-only educational ledger:

* each record carries payload digest and record digest
* records chain through `previous_record_digest`
* append uses optimistic CAS (`expected_previous_digest`)
* integrity verification rejects gaps, reordering, and digest mismatches

Recording a reference is not the same as performing the named authority action.

## Reconstruction

`reconstruct_trace` is read-only presence reporting:

* verifies chain integrity first
* reports `PRESENT` / `NOT_PRESENT` for known authority classes
* does not repair history
* does not promote verification into human, IW, canonical, or publication decisions
* does not perform publication

## Nonclaims

See [`BOUNDARIES_AND_NONCLAIMS.md`](BOUNDARIES_AND_NONCLAIMS.md) for identity, security, verification, human-agency, publication, and evidence boundaries.
