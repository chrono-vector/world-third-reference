"""Minimal append-only Work Trace reference.

This module demonstrates integrity semantics only.

Nonclaims:
- record validity != external truth
- append success != authorization
- append success != execution
- append success != verification
- append success != human acceptance
- append success != canonical status
- append success != publication
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable


class AppendConflict(RuntimeError):
    """Raised when optimistic CAS expectations are stale."""


class TraceIntegrityError(ValueError):
    """Raised when a trace violates deterministic chain rules."""


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically for content identity."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class WorkTraceRecord:
    work_id: str
    sequence: int
    record_type: str
    author_component: str
    payload: dict[str, Any]
    previous_record_digest: str | None
    payload_sha256: str
    canonical_record_sha256: str

    @classmethod
    def build(
        cls,
        *,
        work_id: str,
        sequence: int,
        record_type: str,
        author_component: str,
        payload: dict[str, Any],
        previous_record_digest: str | None,
    ) -> "WorkTraceRecord":
        if not work_id:
            raise ValueError("work_id is required")
        if sequence < 0:
            raise ValueError("sequence must be >= 0")
        if not record_type or not author_component:
            raise ValueError("record_type and author_component are required")

        payload_digest = sha256_hex(canonical_json_bytes(payload))
        identity = {
            "work_id": work_id,
            "sequence": sequence,
            "record_type": record_type,
            "author_component": author_component,
            "payload": payload,
            "previous_record_digest": previous_record_digest,
            "payload_sha256": payload_digest,
        }
        record_digest = sha256_hex(canonical_json_bytes(identity))
        return cls(
            work_id=work_id,
            sequence=sequence,
            record_type=record_type,
            author_component=author_component,
            payload=payload,
            previous_record_digest=previous_record_digest,
            payload_sha256=payload_digest,
            canonical_record_sha256=record_digest,
        )

    def verify_self(self) -> None:
        if sha256_hex(canonical_json_bytes(self.payload)) != self.payload_sha256:
            raise TraceIntegrityError("PAYLOAD_DIGEST_MISMATCH")

        identity = {
            "work_id": self.work_id,
            "sequence": self.sequence,
            "record_type": self.record_type,
            "author_component": self.author_component,
            "payload": self.payload,
            "previous_record_digest": self.previous_record_digest,
            "payload_sha256": self.payload_sha256,
        }
        if sha256_hex(canonical_json_bytes(identity)) != self.canonical_record_sha256:
            raise TraceIntegrityError("RECORD_DIGEST_MISMATCH")


class WorkTrace:
    """In-memory educational append-only trace with optimistic CAS."""

    def __init__(self, work_id: str):
        if not work_id:
            raise ValueError("work_id is required")
        self.work_id = work_id
        self._records: list[WorkTraceRecord] = []

    @property
    def records(self) -> tuple[WorkTraceRecord, ...]:
        return tuple(self._records)

    @property
    def head_digest(self) -> str | None:
        return self._records[-1].canonical_record_sha256 if self._records else None

    def append(
        self,
        *,
        record_type: str,
        author_component: str,
        payload: dict[str, Any],
        expected_previous_digest: str | None,
    ) -> WorkTraceRecord:
        if expected_previous_digest != self.head_digest:
            raise AppendConflict("APPEND_CONFLICT")

        record = WorkTraceRecord.build(
            work_id=self.work_id,
            sequence=len(self._records),
            record_type=record_type,
            author_component=author_component,
            payload=payload,
            previous_record_digest=self.head_digest,
        )
        self._records.append(record)
        return record


def verify_trace(records: Iterable[WorkTraceRecord]) -> tuple[WorkTraceRecord, ...]:
    items = tuple(records)
    if not items:
        return items

    work_id = items[0].work_id
    previous: str | None = None

    for expected_sequence, record in enumerate(items):
        record.verify_self()

        if record.work_id != work_id:
            raise TraceIntegrityError("CROSS_WORK_MISMATCH")
        if record.sequence != expected_sequence:
            raise TraceIntegrityError("SEQUENCE_GAP")
        if record.previous_record_digest != previous:
            raise TraceIntegrityError("PREVIOUS_DIGEST_MISMATCH")

        previous = record.canonical_record_sha256

    return items
