"""Exact-byte mboxrd segmentation and escaping for the synthetic MBOX experiment.

Python's ``mailbox.mbox`` is not used for preservation: it keeps no bytes before
the first envelope line, trims the separator line from each message, and does
not reverse mboxrd escaping. This module partitions a container into segments
that cover every byte exactly once, so the container is reconstructible from
its preserved segments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


MBOX_RULE = "synthetic-mboxrd-segmentation-v1"
MAX_RECORD_BYTES = 128 * 1024  # Matches the engine's per-source parser limit.

# A boundary is any line that begins with "From " (mboxrd escapes body lines).
BOUNDARY_PATTERN = re.compile(rb"(?m)^From ")
ENVELOPE_PATTERN = re.compile(
    rb"From [!-~]+ "
    rb"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) "
    rb"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
    rb"[ 0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [0-9]{4}\n"
)
ESCAPED_FROM_PATTERN = re.compile(rb"(?m)^>(>*From )")
NEEDS_ESCAPE_PATTERN = re.compile(rb"(?m)^(>*From )")


@dataclass(frozen=True)
class Segment:
    """One contiguous byte range of a container."""

    offset: int
    length: int
    kind: str  # "record" or "preamble"
    ordinal: int  # 1-based position among the container's segments
    starts_after_blank_line: bool

    def as_span(self) -> dict:
        return {
            "kind": self.kind,
            "length": self.length,
            "offset": self.offset,
            "ordinal": self.ordinal,
            "starts_after_blank_line": self.starts_after_blank_line,
        }


def segment_container(data: bytes) -> List[Segment]:
    """Partition container bytes at every line that begins with ``From ``."""

    if not data:
        return []
    edges = sorted({0, *(match.start() for match in BOUNDARY_PATTERN.finditer(data))})
    edges.append(len(data))
    segments = []
    for ordinal, (start, end) in enumerate(zip(edges, edges[1:]), start=1):
        segments.append(
            Segment(
                offset=start,
                length=end - start,
                kind="record" if data.startswith(b"From ", start) else "preamble",
                ordinal=ordinal,
                starts_after_blank_line=start == 0 or data[:start].endswith(b"\n\n"),
            )
        )
    return segments


def _envelope_end(segment: bytes) -> int:
    newline = segment.find(b"\n")
    return -1 if newline < 0 else newline + 1


def segment_defects(segment: bytes, kind: str, starts_after_blank_line: bool) -> List[str]:
    """Return the reasons a segment must be quarantined; empty means parseable."""

    if kind == "preamble":
        return ["preamble-before-first-envelope"]
    defects = []
    envelope_end = _envelope_end(segment)
    if envelope_end < 0:
        return ["malformed-envelope", "truncated-record"]
    if ENVELOPE_PATTERN.fullmatch(segment[:envelope_end]) is None:
        defects.append("malformed-envelope")
    if not starts_after_blank_line:
        defects.append("ambiguous-boundary")
    if not segment.endswith(b"\n"):
        defects.append("truncated-record")
    elif len(segment) < envelope_end + 1 or not segment.endswith(b"\n\n"):
        defects.append("unterminated-record")
    if len(segment) > MAX_RECORD_BYTES:
        defects.append("oversized-record")
    if not defects and envelope_end + 1 == len(segment):
        defects.append("empty-record")
    return sorted(defects)


def envelope_line(segment: bytes) -> bytes:
    return segment[: _envelope_end(segment)]


def unescape_record(segment: bytes) -> bytes:
    """Return the RFC 5322 message carried by a well-formed mboxrd record."""

    if segment_defects(segment, "record", True):
        raise ValueError("only well-formed records can be unescaped")
    body = segment[_envelope_end(segment) : -1]
    return ESCAPED_FROM_PATTERN.sub(rb"\1", body)


def escape_message(message: bytes) -> bytes:
    if not message.endswith(b"\n"):
        raise ValueError("message must end with a newline")
    return NEEDS_ESCAPE_PATTERN.sub(rb">\1", message)


def build_record(envelope: bytes, message: bytes) -> bytes:
    """Build one well-formed mboxrd record, including its separator line."""

    if ENVELOPE_PATTERN.fullmatch(envelope) is None:
        raise ValueError("envelope line is malformed")
    return envelope + escape_message(message) + b"\n"
