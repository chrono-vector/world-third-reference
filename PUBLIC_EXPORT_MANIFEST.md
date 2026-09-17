# WORLD THIRD — Public Export Manifest

This manifest defines the public-safe scope of the WORLD THIRD Public Reference.

## Included scope

### Architecture and nonclaims
- concise WORLD THIRD overview
- authority-lane separation
- Human/IW/Canonical/Publication distinctions
- explicit security and identity nonclaims

### Deterministic integrity reference
- canonical JSON encoding
- SHA-256 content identity
- payload digest
- record digest
- previous-record digest
- sequence validation
- cross-work rejection
- optimistic CAS conflict behavior

### Local ArtifactRef reference
- safe relative-path validation
- parent/absolute/Windows/backslash path rejection
- local-root confinement after resolution
- SHA-256 validation
- byte-length validation
- missing/read/hash/length result states

This does not claim production-grade junction/reparse or TOCTOU protection.

### Read-only reconstruction
The reference reconstruction:
- verifies the trace before reporting
- reports authority presence as PRESENT / NOT_PRESENT
- does not repair invalid history
- does not infer Human/IW/Canonical/Publication decisions
- does not convert verification results into higher authority
- does not perform publication

### Synthetic tests
Tests cover:
- valid append chain
- stale CAS
- payload and record digest tampering
- record reordering
- cross-work mismatch
- parent/absolute/Windows/backslash unsafe paths
- invalid digest/length references
- missing file
- hash and byte-length mismatch
- reconstruction no-promotion
- publication presence not equal to publication performed

## Explicitly excluded
This public package does not include:
- full Job Agent authority bridges
- EIG PEP/policy mapping
- internal enforcement receipts/topology
- real authority-instance artifacts
- real Human/IW/Canonical/Publication records
- checkpoints, audit/freeze packs, generated evidence
- local backup registries or developer paths
- credentials/private keys
- raw private Git history
