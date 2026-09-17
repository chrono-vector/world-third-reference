"""Local ArtifactRef verification reference.

This verifier is intentionally local-only and does not fetch remote content.

Artifact bytes verified != independently verified result.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import re


_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")


@dataclass(frozen=True)
class ArtifactRef:
    relative_path: str
    sha256: str
    byte_length: int


@dataclass(frozen=True)
class ArtifactVerification:
    state: str
    reason: str


def _is_safe_relative_path(value: str) -> bool:
    if not value:
        return False
    if "\\" in value:
        return False
    if _WINDOWS_DRIVE_RE.match(value):
        return False
    if value.startswith("/"):
        return False

    path = PurePosixPath(value)
    if path.is_absolute():
        return False
    if any(part in {"", ".", ".."} for part in path.parts):
        return False
    return True


def verify_artifact_ref(ref: ArtifactRef, *, local_root: Path) -> ArtifactVerification:
    if not _is_safe_relative_path(ref.relative_path):
        return ArtifactVerification("NOT_VERIFIABLE", "UNSAFE_PATH")
    if ref.byte_length < 0:
        return ArtifactVerification("NOT_VERIFIABLE", "INVALID_REFERENCE")
    if len(ref.sha256) != 64 or any(ch not in "0123456789abcdef" for ch in ref.sha256):
        return ArtifactVerification("NOT_VERIFIABLE", "INVALID_REFERENCE")

    try:
        root = local_root.resolve()
        target = (root / ref.relative_path).resolve()
        target.relative_to(root)
    except (OSError, RuntimeError, ValueError):
        return ArtifactVerification("NOT_VERIFIABLE", "UNSAFE_PATH")

    if not target.is_file():
        return ArtifactVerification("NOT_VERIFIABLE", "FILE_NOT_FOUND")

    try:
        data = target.read_bytes()
    except OSError:
        return ArtifactVerification("NOT_VERIFIABLE", "READ_ERROR")

    if len(data) != ref.byte_length:
        return ArtifactVerification("TAMPERED_REF", "BYTE_LENGTH_MISMATCH")

    digest = hashlib.sha256(data).hexdigest()
    if digest != ref.sha256:
        return ArtifactVerification("TAMPERED_REF", "HASH_MISMATCH")

    return ArtifactVerification("VERIFIED_REF", "OK")
