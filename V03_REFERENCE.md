# WORLD THIRD v0.3 Public Reference Notes

This document summarizes selected **public-safe concepts** from WORLD THIRD v0.3.
It is an educational/reference description only. It does not expose private enforcement topology, production identities, credentials, real evidence, or operational publication machinery.

## What v0.3 clarifies

WORLD THIRD v0.3 strengthens separation between identity, authority, evidence, execution, verification, and publication.

Core distinctions:

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
APPROVED_FOR_PUBLICATION ≠ PUBLICATION_PERFORMED
State ≠ Evidence
Classification ≠ Verdict
```

## 1. Authority identity is not real-world identity

A cryptographic signature can prove control of a configured signing key.
It does **not** prove:

- legal identity
- real-world identity
- that a decision was justified
- that a decision was correct
- that the signer should have had authority

A trustworthy system therefore keeps at least three questions separate:

1. Was this record signed by a configured key?
2. Was that key accepted for this authority lane?
3. What decision did that authority record actually make?

## 2. Authority lanes remain separate

WORLD THIRD treats these lanes as distinct:

- Human review
- External Independent Witness (IW)
- Canonical designation
- Publication decision
- Publication execution evidence

No lane should be silently promoted into another.

Examples:

```text
Weaver PASS ↛ Human ACCEPTED
Human ACCEPTED ↛ Canonical
IW ACCEPTED ↛ Canonical
Canonical ↛ Publication approval
Publication approval ↛ Publication execution
Publication execution ↛ Canonical / Human / IW
```

## 3. Publication decision and publication execution are different records

A publication decision answers:

> Is this artifact approved for publication within the declared scope?

A publication execution receipt answers:

> Is there evidence that a publisher/executor claims a publication action was attempted or performed?

These must not be merged into one status.

A useful reconstruction keeps separate axes such as:

```text
publication_decision:
  decision: APPROVED_FOR_PUBLICATION
  authority_signature: VERIFIED
  acceptance_state: ACCEPTED_AUTHORITY

publication_execution:
  presence: NOT_PRESENT
  status: NOT_PERFORMED
  trusted_execution_claim: false
```

`APPROVED_FOR_PUBLICATION / NOT_PERFORMED` is a valid state.

## 4. Trusted execution claims require more than field matching

A receipt whose fields match a publication decision is not automatically trusted.
A trust decision may additionally require:

- Work Trace integrity is valid
- publication authority signature is verified
- publication authority is accepted for that lane
- decision is `APPROVED_FOR_PUBLICATION`
- decision/receipt binding is valid

If these conditions do not hold, the receipt may still be present as historical evidence, but it should not be promoted into a trusted publication state.

## 5. Work Trace remains append-only evidence history

A Work Trace should preserve history rather than silently repair it.
Important properties include:

- chained record digests
- payload digests
- explicit sequence numbers
- compare-and-swap style append expectations
- separate classification of append conflict vs integrity failure
- no latest-wins repair of contradictory authority history

An append conflict does not itself mean the historical trace was corrupted.

## 6. Artifact verification is not semantic truth

A verifier may confirm that an artifact:

- exists under an allowed local root
- has the expected byte length
- has the expected digest
- has not changed during verification

That does not prove the artifact's claims are true, correct, safe, or authorized.

```text
VERIFIED_REF ≠ semantic truth
```

## 7. Filesystem hardening is bounded

Reference-level path safety concepts include:

- reject path traversal
- reject absolute paths when a confined root is required
- reject Windows drive/UNC escape forms
- detect symlink/reparse escapes where possible
- fail closed if the file changes during verification

These measures reduce risk. They do not claim perfect elimination of all OS-level race conditions.

## 8. Reconstruction should expose multiple axes

A useful audit reconstruction should avoid collapsing everything into one PASS/FAIL.
It may report independently:

- Work Trace integrity
- artifact verification
- authorization presence
- enforcement presence
- execution presence
- Weaver verification
- Human status
- External IW status
- Canonical status
- publication authority signature
- publication authority acceptance
- publication decision
- publication execution
- decision binding
- authority binding
- trusted execution claim

Presence is not acceptance, and acceptance is not truth.

## Public-reference boundary

This repository intentionally does **not** contain:

- production private keys
- production authority identities
- private policy mappings
- private enforcement topology
- operational publisher credentials
- real Human / IW / Canonical / Publication evidence
- production publication execution machinery

The goal is to make the separation model understandable and testable without exposing private operational material.

## Nonclaims

WORLD THIRD v0.3 public reference does not claim:

- legal or real-world identity verification
- HSM/KMS-backed production key custody
- trusted timestamp authority
- distributed consensus
- global distributed locking
- perfect OS race elimination
- independent verification merely because a local test passed
- that a publication receipt proves external truth
- that this repository performs production publication

Human agency remains the final authority boundary.
