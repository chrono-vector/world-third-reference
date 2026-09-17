# WORLD THIRD Public Reference

WORLD THIRD separates an AI system's ability to act from the authority to act, the evidence that an action occurred, the verification of results, and the human decision that follows.

```text
FIND → AUTHORIZE → ENFORCE → EXECUTE → VERIFY → HUMAN FINAL → LEARN
```

## Authority separation

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

## Start here

- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `examples/basic_flow.py`
- `examples/publication_separation.py`

## What this reference demonstrates

This package is an educational/reference implementation. It includes:

- deterministic content identity and append-only trace examples
- optimistic CAS semantics
- local ArtifactRef verification
- read-only authority-presence reconstruction
- synthetic tests
- public-facing boundary and nonclaim documentation

It does not include operational authority bridges, real evidence, real identities, private enforcement topology, credentials, or publication machinery.

See `BOUNDARIES_AND_NONCLAIMS.md` for the full nonclaim set.

## Tests

From this directory:

```bash
PYTHONPATH=src python -m pytest -q
```

Pull requests are checked automatically with pytest on supported Python versions.

## License

Licensed under the Apache License 2.0. See `LICENSE`.
