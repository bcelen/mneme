"""Fixed, wholly fictional EML fixtures for the incremental-ingestion increment."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple


PROTOTYPE_ROOT = Path(__file__).resolve().parent
HARDENING_ROOT = PROTOTYPE_ROOT.parent / "synthetic-hardening-1"
if str(HARDENING_ROOT) not in sys.path:
    sys.path.insert(0, str(HARDENING_ROOT))

import fixtures as CORPUS  # noqa: E402


@dataclass(frozen=True)
class IncrementFixture:
    fixture_id: str
    filename: str
    data: bytes
    purpose: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


def _message(lines: Iterable[str], newline: str = "\n") -> bytes:
    return (newline.join(lines) + newline).encode("utf-8")


LANTERN_FOLLOW_UP = _message(
    [
        "From: Arin Vale <arin.vale@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Sat, 25 Oct 2025 09:00:00 +0000",
        "Message-ID: <lantern-follow-up-015@example.test>",
        "Subject: Observatory lantern follow-up",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "The north observatory lantern passed its Friday check.",
    ]
)

DOME_MAINTENANCE = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Arin Vale <arin.vale@example.test>",
        "Date: Sun, 26 Oct 2025 16:20:00 +0000",
        "Message-ID: <dome-maintenance-017@example.test>",
        "Subject: Dome maintenance window",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "The east dome shutter will be serviced on Tuesday.",
    ],
    newline="\r\n",
)


# The resent copy deliberately reuses the accepted EML-001 bytes under a new
# incoming name, so it is an exact-byte duplicate with a distinct source key.
INCREMENT_FIXTURES: Tuple[IncrementFixture, ...] = (
    IncrementFixture(
        "INC-015",
        "15-lantern-follow-up.eml",
        LANTERN_FOLLOW_UP,
        "new occurrence that matches the reviewed lantern observatory query",
    ),
    IncrementFixture(
        "INC-016",
        "16-resent-plain-lf-7bit.eml",
        CORPUS.PLAIN_LF,
        "exact-byte duplicate of EML-001 under a different source key",
    ),
    IncrementFixture(
        "INC-017",
        "17-dome-maintenance.eml",
        DOME_MAINTENANCE,
        "new occurrence that does not match the reviewed query",
    ),
)


EXPECTED_HASHES: Dict[str, str] = {
    "INC-015": "57da0246e8c6977f10005676264368d34eae5fffdceaaab44899614fda482482",
    "INC-016": "befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208",
    "INC-017": "132e520c3fb6eb4447a814f46f47b6306ad8e93c3dbdb40612ab8afbb1e1d7b9",
}


def reviewed_sha256_allowlist() -> Dict[str, Tuple[str, ...]]:
    """Map every reviewed synthetic digest to the fixture labels that carry it."""

    labels: Dict[str, list] = {}
    for fixture in CORPUS.FIXTURES:
        labels.setdefault(CORPUS.EXPECTED_HASHES[fixture.fixture_id], []).append(
            fixture.fixture_id
        )
    for fixture in INCREMENT_FIXTURES:
        labels.setdefault(EXPECTED_HASHES[fixture.fixture_id], []).append(
            fixture.fixture_id
        )
    return {digest: tuple(sorted(names)) for digest, names in sorted(labels.items())}


def materialize_files(destination: Path, members: Iterable[Tuple[str, bytes]]) -> None:
    """Write a disposable incoming batch; the destination must not exist."""

    if destination.exists():
        raise RuntimeError(f"fixture destination already exists: {destination}")
    destination.mkdir(parents=True, mode=0o700)
    for filename, data in members:
        path = destination / filename
        path.write_bytes(data)
        path.chmod(0o400)


def base_members() -> Tuple[Tuple[str, bytes], ...]:
    return tuple((fixture.filename, fixture.data) for fixture in CORPUS.FIXTURES)


def increment_members() -> Tuple[Tuple[str, bytes], ...]:
    return tuple((fixture.filename, fixture.data) for fixture in INCREMENT_FIXTURES)
