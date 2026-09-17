# WORLD THIRD Public Reference — Boundaries and Nonclaims

This document defines what a future public reference may explain without overstating what WORLD THIRD v0.2 proves.

## Authority boundaries

The public explanation must preserve these separations:

```text
Capability ≠ Authority
Authorization ≠ Execution
Execution ≠ Verification
Verification ≠ Independent Witness Acceptance
Verification ≠ Human Acceptance
Human Acceptance ≠ Canonical
Independent Witness Acceptance ≠ Canonical
Canonical ≠ Publication Approval
Publication Approval ≠ Publication Performed
```

No public example may silently promote one state into another.

## Identity nonclaim

Recorded authority identities are identifiers, not cryptographic authentication.

The public reference must not claim that v0.2 provides:

- cryptographically authenticated Human authority
- cryptographically authenticated External IW identity
- cryptographically authenticated Canonical authority
- cryptographically authenticated Publication authority

Those are production-hardening concerns.

## Security nonclaim

The public reference may demonstrate fail-closed application semantics but must not claim universal security.

It must not imply complete protection against:

- distributed races
- arbitrary filesystem junction/reparse attacks
- all TOCTOU conditions
- compromised hosts
- compromised signing infrastructure
- malicious external services
- production secrets-management failures

## Verification nonclaim

Artifact byte verification and deterministic replay are not independent verification.

Weaver PASS remains a Weaver result only unless a separate IW artifact records IW status.

## Human-agency boundary

Human Review is an explicit authority lane.

The public reference should make clear that machine checks do not become final human judgment automatically.

## Publication boundary

A publication-status artifact represents a bounded decision.

It does not:

- upload files
- push to GitHub
- publish a release
- perform redaction
- perform a secrets scan
- prove that publication occurred

Actual release execution requires a separate action/receipt model if introduced later.

## Evidence boundary

State is not evidence.

A public example should reference immutable/synthetic evidence rather than treating a database status flag or log message as proof.

## Public-reference scope

The public reference is educational/reference architecture.

It must not be presented as:

- certification
- legal or regulatory approval
- production security guarantee
- universal agent safety
- independent audit acceptance
- operational authorization
- proof of external truth
