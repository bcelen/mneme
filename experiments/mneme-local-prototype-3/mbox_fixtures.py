"""Fixed, wholly fictional mboxrd fixtures for the synthetic MBOX experiment."""

from __future__ import annotations

import base64
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple


PROTOTYPE_ROOT = Path(__file__).resolve().parent
if str(PROTOTYPE_ROOT) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_ROOT))

import mboxrd  # noqa: E402


def _message(lines: Iterable[str]) -> bytes:
    return ("\n".join(lines) + "\n").encode("utf-8")


# -- Ordinary records ---------------------------------------------------------

ROTA_ENVELOPE = b"From arin.vale@example.test Mon Oct 27 08:00:00 2025\n"
ROTA_MESSAGE = _message(
    [
        "From: Arin Vale <arin.vale@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Mon, 27 Oct 2025 08:00:00 +0000",
        "Message-ID: <lantern-rota-101@example.test>",
        "Subject: Lantern observatory rota",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "The observatory lantern rota for November is settled.",
    ]
)

ROTA_ATTACHMENT_TEXT = b"Fictional rota: north dome Mondays, east dome Thursdays.\n"
ATTACHMENT_ENVELOPE = b"From nila.hart@example.test Mon Oct 27 09:15:00 2025\n"
ATTACHMENT_MESSAGE = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Arin Vale <arin.vale@example.test>",
        "Date: Mon, 27 Oct 2025 09:15:00 +0000",
        "Message-ID: <rota-attachment-102@example.test>",
        "Subject: Observatory rota attachment",
        "MIME-Version: 1.0",
        'Content-Type: multipart/mixed; boundary="rota-102"',
        "",
        "--rota-102",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "The rota table is attached as plain text.",
        "--rota-102",
        'Content-Type: text/plain; name="rota.txt"',
        'Content-Disposition: attachment; filename="rota.txt"',
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(ROTA_ATTACHMENT_TEXT).decode("ascii"),
        "--rota-102--",
    ]
)

# Same Message-ID as accepted fixture EML-001, but different bytes.
FORWARDED_ENVELOPE = b"From mira.sol@example.test Mon Oct 27 11:30:00 2025\n"
FORWARDED_MESSAGE = _message(
    [
        "From: Mira Sol <mira.sol@example.test>",
        "To: Nila Hart <nila.hart@example.test>",
        "Date: Tue, 14 Oct 2025 09:30:00 +0000",
        "Message-ID: <duplicate-anchor@example.test>",
        "Subject: Forwarded observatory lantern schedule",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "Forwarded copy: the north observatory lantern is ready for Friday.",
    ]
)

# -- mboxrd escaping, written out literally (not produced by escape_message) ----

QUOTED_FROM_RECORD = (
    b"From rowan.pike@example.test Mon Oct 27 10:05:00 2025\n"
    b"From: Rowan Pike <rowan.pike@example.test>\n"
    b"To: Mira Sol <mira.sol@example.test>\n"
    b"Date: Mon, 27 Oct 2025 10:05:00 +0000\n"
    b"Message-ID: <quoted-from-103@example.test>\n"
    b"Subject: Quoted From lines\n"
    b"MIME-Version: 1.0\n"
    b'Content-Type: text/plain; charset="us-ascii"\n'
    b"Content-Transfer-Encoding: 7bit\n"
    b"\n"
    b"Observers wrote:\n"
    b">From the north dome, the lantern was visible.\n"
    b">>From the archive: an older quoted line.\n"
    b">>>From three levels down.\n"
    b"Fromage is not a boundary.\n"
    b">Fromage stays quoted.\n"
    b" From with a leading space is not a boundary.\n"
    b"\n"
)
QUOTED_FROM_MESSAGE = (
    b"From: Rowan Pike <rowan.pike@example.test>\n"
    b"To: Mira Sol <mira.sol@example.test>\n"
    b"Date: Mon, 27 Oct 2025 10:05:00 +0000\n"
    b"Message-ID: <quoted-from-103@example.test>\n"
    b"Subject: Quoted From lines\n"
    b"MIME-Version: 1.0\n"
    b'Content-Type: text/plain; charset="us-ascii"\n'
    b"Content-Transfer-Encoding: 7bit\n"
    b"\n"
    b"Observers wrote:\n"
    b"From the north dome, the lantern was visible.\n"
    b">From the archive: an older quoted line.\n"
    b">>From three levels down.\n"
    b"Fromage is not a boundary.\n"
    b">Fromage stays quoted.\n"
    b" From with a leading space is not a boundary.\n"
)

CLOSING_ENVELOPE = b"From arin.vale@example.test Thu Oct 30 17:45:00 2025\n"
CLOSING_MESSAGE = _message(
    [
        "From: Arin Vale <arin.vale@example.test>",
        "To: Nila Hart <nila.hart@example.test>",
        "Date: Thu, 30 Oct 2025 17:45:00 +0000",
        "Message-ID: <dome-closing-106@example.test>",
        "Subject: East dome closing notice",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "The east dome closes early on Friday.",
    ]
)

ROTA_RECORD = mboxrd.build_record(ROTA_ENVELOPE, ROTA_MESSAGE)
ATTACHMENT_RECORD = mboxrd.build_record(ATTACHMENT_ENVELOPE, ATTACHMENT_MESSAGE)
FORWARDED_RECORD = mboxrd.build_record(FORWARDED_ENVELOPE, FORWARDED_MESSAGE)
CLOSING_RECORD = mboxrd.build_record(CLOSING_ENVELOPE, CLOSING_MESSAGE)

# Ordinary mailbox: five records, the last an exact-byte copy of the first.
INBOX = ROTA_RECORD + ATTACHMENT_RECORD + QUOTED_FROM_RECORD + FORWARDED_RECORD + ROTA_RECORD
INBOX_MESSAGES = (
    ROTA_MESSAGE,
    ATTACHMENT_MESSAGE,
    QUOTED_FROM_MESSAGE,
    FORWARDED_MESSAGE,
    ROTA_MESSAGE,
)

# The same mailbox after one more message was appended.
INBOX_APPENDED = INBOX + CLOSING_RECORD

# Reviewed negative fixture: the second record's attachment text was edited,
# so the record at an existing offset has different bytes.
INBOX_CHANGED = (
    ROTA_RECORD
    + mboxrd.build_record(
        ATTACHMENT_ENVELOPE,
        ATTACHMENT_MESSAGE.replace(
            base64.b64encode(ROTA_ATTACHMENT_TEXT),
            base64.b64encode(ROTA_ATTACHMENT_TEXT.replace(b"Thursdays", b"Fridays")),
        ),
    )
    + QUOTED_FROM_RECORD
    + FORWARDED_RECORD
    + ROTA_RECORD
)

# -- Malformed and unsafe records ---------------------------------------------

SURVIVOR_MESSAGE = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Tue, 28 Oct 2025 09:00:00 +0000",
        "Message-ID: <survivor-201@example.test>",
        "Subject: Survivor record between damaged records",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "This lantern note is intact although its neighbours are damaged.",
    ]
)


def _short_message(subject: str, body: str) -> bytes:
    return _message(
        [
            "From: Nila Hart <nila.hart@example.test>",
            "To: Mira Sol <mira.sol@example.test>",
            f"Subject: {subject}",
            "",
            body,
        ]
    )


MALFORMED = (
    b"This synthetic preamble is not an mbox record.\n\n"
    + mboxrd.build_record(b"From nila.hart@example.test Tue Oct 28 09:00:00 2025\n", SURVIVOR_MESSAGE)
    # Envelope line lacks the asctime date.
    + b"From nobody-without-a-date\n"
    + mboxrd.escape_message(_short_message("Malformed envelope", "Envelope has no date."))
    + b"\n"
    # No blank separator line before the next envelope.
    + b"From nila.hart@example.test Tue Oct 28 10:00:00 2025\n"
    + mboxrd.escape_message(_short_message("Unterminated record", "No separator follows."))
    # Therefore this boundary is ambiguous.
    + b"From nila.hart@example.test Tue Oct 28 10:05:00 2025\n"
    + mboxrd.escape_message(_short_message("Ambiguous boundary", "Maybe body, maybe message."))
    + b"\n"
    # Larger than the per-record parser limit.
    + b"From nila.hart@example.test Tue Oct 28 11:00:00 2025\n"
    + mboxrd.escape_message(
        _short_message("Oversized record", "lantern " * (17 * 1024))
    )
    + b"\n"
    # Cut off mid-line at the end of the container.
    + b"From nila.hart@example.test Tue Oct 28 12:00:00 2025\n"
    + b"From: Nila Hart <nila.hart@example.test>\nSubject: Truncated record\n\nThis record stops mid-li"
)
MALFORMED_EXPECTED_DEFECTS: Tuple[Tuple[str, ...], ...] = (
    ("preamble-before-first-envelope",),
    (),
    ("malformed-envelope",),
    ("unterminated-record",),
    ("ambiguous-boundary",),
    ("oversized-record",),
    ("truncated-record",),
)


@dataclass(frozen=True)
class MboxFixture:
    fixture_id: str
    filename: str
    data: bytes
    purpose: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


MBOX_FIXTURES: Tuple[MboxFixture, ...] = (
    MboxFixture("MBOX-001", "observatory-inbox.mbox", INBOX, "ordinary mailbox"),
    MboxFixture(
        "MBOX-002", "observatory-inbox.mbox", INBOX_APPENDED, "same mailbox with one appended record"
    ),
    MboxFixture(
        "MBOX-003", "observatory-inbox.mbox", INBOX_CHANGED, "negative: changed bytes at an existing offset"
    ),
    MboxFixture("MBOX-004", "damaged.mbox", MALFORMED, "malformed, truncated, and unsafe records"),
)


EXPECTED_HASHES: Dict[str, str] = {
    "MBOX-001": "2f008aab90a5d7dd4ac68a6277b3e994a8ca4783a73f967695c449777f8259a7",
    "MBOX-002": "2749de8a0c0a572a34d324fe6631c221090cac1d178ada4ef37faa7785f36073",
    "MBOX-003": "bf198ca3d53ceb492891ca5a2faadabc28ab8ca372f3e74c35b84e811c6a9a79",
    "MBOX-004": "2561e9e24eb50568ef11cdbfb61e06947b7346f858bdbaeccbf7446ab1f54bf7",
}


def fixture(fixture_id: str) -> MboxFixture:
    return next(item for item in MBOX_FIXTURES if item.fixture_id == fixture_id)
