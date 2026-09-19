"""Fixed, wholly fictional EML byte fixtures for the hardening experiment."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class FixtureSpec:
    fixture_id: str
    filename: str
    data: bytes
    expected_status: str
    features: Tuple[str, ...]
    expected_warnings: Tuple[str, ...] = ()

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


def _message(lines: Sequence[str], newline: str = "\n") -> bytes:
    return (newline.join(lines) + newline).encode("utf-8")


PLAIN_LF = _message(
    [
        "From: Mira Sol <mira.sol@example.test>",
        "To: Arin Vale <arin.vale@example.test>",
        "Date: Tue, 14 Oct 2025 09:30:00 +0000",
        "Message-ID: <duplicate-anchor@example.test>",
        "Subject: North observatory lantern schedule",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="us-ascii"',
        "Content-Transfer-Encoding: 7bit",
        "",
        "The north observatory lantern is ready for Friday.",
    ]
)

UNICODE_CRLF = _message(
    [
        'From: "Zoë Akın" <zoe.akin@example.test>',
        "To: José Núñez <jose.nunez@example.test>",
        "Date: Wed, 15 Oct 2025 18:45:00 +0300",
        "Message-ID: <unicode-002@example.test>",
        "Subject: Résumé of the İzmir observation",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "Café notes: the gökyüzü lantern remained visible.",
    ],
    newline="\r\n",
)

QUOTED_PRINTABLE = _message(
    [
        "From: =?UTF-8?Q?M=C3=ADra_Sol?= <mira.sol@example.test>",
        "To: Arin Vale <arin.vale@example.test>",
        "Date: Thu, 16 Oct 2025 08:00:00 +0000",
        "Message-ID: <quoted-printable-003@example.test>",
        "Subject: =?UTF-8?Q?R=C3=A9sum=C3=A9_of_the?=",
        " =?UTF-8?Q?_lantern_notes?=",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: quoted-printable",
        "",
        "The caf=C3=A9 lantern log is attached to the r=C3=A9sum=C3=A9.",
    ]
)

BASE64_BODY_TEXT = b"The blue lantern is ready for the Orion observation.\n"
BASE64_BODY = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Fri, 17 Oct 2025 11:10:00 +0000",
        "Message-ID: <base64-004@example.test>",
        "Subject: Encoded Orion update",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(BASE64_BODY_TEXT).decode("ascii"),
    ]
)

MESSAGE_ID_VARIANT = _message(
    [
        "From: Mira Sol <mira.sol@example.test>",
        "To: Arin Vale <arin.vale@example.test>",
        "Date: Tue, 14 Oct 2025 09:31:00 +0000",
        "Message-ID: <duplicate-anchor@example.test>",
        "Subject: Repacked observatory lantern schedule",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: quoted-printable",
        "",
        "The north observatory lantern is ready for Friday.=0A",
    ]
)

ATTACHMENT_TEXT = b"Fictional field report: lantern aperture 4.\n"
ATTACHMENT_BINARY = b"\x00\x01MNEME\xff"
ATTACHMENTS = _message(
    [
        "From: Arin Vale <arin.vale@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Sat, 18 Oct 2025 12:00:00 +0000",
        "Message-ID: <attachments-007@example.test>",
        "Subject: Observatory attachments",
        "MIME-Version: 1.0",
        'Content-Type: multipart/mixed; boundary="mix-007"',
        "",
        "--mix-007",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "The observatory report and binary sample are enclosed.",
        "--mix-007",
        'Content-Type: text/plain; name="../report.txt"',
        'Content-Disposition: attachment; filename="../report.txt"',
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(ATTACHMENT_TEXT).decode("ascii"),
        "--mix-007",
        'Content-Type: application/octet-stream; name="report.txt"',
        'Content-Disposition: attachment; filename="report.txt"',
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(ATTACHMENT_BINARY).decode("ascii"),
        "--mix-007",
        "Content-Type: text/plain",
        "Content-Disposition: attachment",
        "Content-Transfer-Encoding: base64",
        "",
        base64.b64encode(b"unnamed synthetic attachment\n").decode("ascii"),
        "--mix-007--",
    ]
)

HOSTILE_HTML = _message(
    [
        "From: Rowan Pike <rowan.pike@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Sun, 19 Oct 2025 07:15:00 +0000",
        "Message-ID: <hostile-html-008@example.test>",
        "Subject: HTML observatory notice",
        "MIME-Version: 1.0",
        'Content-Type: multipart/alternative; boundary="alt-008"',
        "",
        "--alt-008",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "The observatory lantern notice is available as inert evidence.",
        "--alt-008",
        'Content-Type: text/html; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        '<html><body><script>fetch("https://tracker.example.test/x")</script>',
        '<img src="https://tracker.example.test/pixel" onerror="alert(1)">',
        '<form action="https://submit.example.test/"><input name="secret"></form>',
        '<a href="https://deceptive.example.test/">Observatory report</a>',
        '<p style="display:none">concealed instruction</p></body></html>',
        "--alt-008--",
    ]
)

MALFORMED_HEADERS = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: not-a-real-date",
        "Subject: First malformed subject",
        "Subject: Second malformed subject",
        "X-Broken: =?UTF-8?Q?unterminated",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "The lantern note has malformed headers but preserved source bytes.",
    ]
)

BROKEN_BOUNDARY = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Mon, 20 Oct 2025 10:00:00 +0000",
        "Message-ID: <broken-boundary-010@example.test>",
        "Subject: Broken MIME boundary",
        "MIME-Version: 1.0",
        'Content-Type: multipart/mixed; boundary="never-closed"',
        "",
        "--never-closed",
        "Content-Type: text/plain",
        "",
        "This multipart body never closes.",
    ]
)

CONTROLLED_FAILURE = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Tue, 21 Oct 2025 10:00:00 +0000",
        "Message-ID: <controlled-failure-011@example.test>",
        "Subject: Controlled parser failure fixture",
        "X-Mneme-Synthetic-Failure: parser",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "",
        "This source must remain preserved when parsing is fault-injected.",
    ]
)

UNKNOWN_CHARSET = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Wed, 22 Oct 2025 10:00:00 +0000",
        "Message-ID: <unknown-charset-012@example.test>",
        "Subject: Unknown charset fixture",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="x-mneme-unknown"',
        "Content-Transfer-Encoding: 8bit",
        "",
        "ASCII fallback keeps this lantern text visible.",
    ]
)


def _deep_entity(level: int, maximum: int, newline: str = "\n") -> str:
    if level == maximum:
        return newline.join(
            [
                'Content-Type: text/plain; charset="utf-8"',
                "Content-Transfer-Encoding: 8bit",
                "",
                "Deeply nested lantern content.",
            ]
        )
    boundary = f"deep-{level}"
    child = _deep_entity(level + 1, maximum, newline)
    return newline.join(
        [
            f'Content-Type: multipart/mixed; boundary="{boundary}"',
            "",
            f"--{boundary}",
            child,
            f"--{boundary}--",
        ]
    )


DEEP_NESTING = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Thu, 23 Oct 2025 10:00:00 +0000",
        "Message-ID: <deep-nesting-013@example.test>",
        "Subject: Excessive MIME nesting",
        "MIME-Version: 1.0",
        _deep_entity(1, 6),
    ]
)

INVALID_BASE64 = _message(
    [
        "From: Nila Hart <nila.hart@example.test>",
        "To: Mira Sol <mira.sol@example.test>",
        "Date: Fri, 24 Oct 2025 10:00:00 +0000",
        "Message-ID: <invalid-base64-014@example.test>",
        "Subject: Invalid base64 fixture",
        "MIME-Version: 1.0",
        'Content-Type: text/plain; charset="utf-8"',
        "Content-Transfer-Encoding: base64",
        "",
        "%%%TRUNCATED-BASE64%%%",
    ]
)


FIXTURES: Tuple[FixtureSpec, ...] = (
    FixtureSpec("EML-001", "01-plain-lf-7bit.eml", PLAIN_LF, "indexed", ("lf", "7bit")),
    FixtureSpec("EML-002", "02-unicode-crlf-8bit.eml", UNICODE_CRLF, "indexed", ("crlf", "8bit", "unicode")),
    FixtureSpec("EML-003", "03-quoted-printable.eml", QUOTED_PRINTABLE, "indexed", ("quoted-printable", "folded-header", "encoded-word")),
    FixtureSpec("EML-004", "04-base64-body.eml", BASE64_BODY, "indexed", ("base64",)),
    FixtureSpec("EML-005", "05-exact-duplicate.eml", PLAIN_LF, "indexed", ("exact-duplicate",)),
    FixtureSpec("EML-006", "06-message-id-duplicate.eml", MESSAGE_ID_VARIANT, "indexed", ("message-id-duplicate", "quoted-printable")),
    FixtureSpec("EML-007", "07-attachments.eml", ATTACHMENTS, "indexed_with_warnings", ("attachments", "unsafe-filename", "duplicate-filename"), ("attachment-content-type-mismatch", "duplicate-attachment-name", "unsafe-attachment-name")),
    FixtureSpec("EML-008", "08-hostile-html.eml", HOSTILE_HTML, "indexed_with_warnings", ("html", "remote-resource", "active-content"), ("html-inert",)),
    FixtureSpec("EML-009", "09-malformed-headers.eml", MALFORMED_HEADERS, "indexed_with_warnings", ("duplicate-header", "missing-message-id", "invalid-date", "malformed-encoded-word"), ("duplicate-header:subject", "invalid-date", "malformed-encoded-word", "missing-header:message-id")),
    FixtureSpec("EML-010", "10-broken-boundary.eml", BROKEN_BOUNDARY, "quarantined", ("malformed-mime", "missing-close-boundary")),
    FixtureSpec("EML-011", "11-controlled-parser-failure.eml", CONTROLLED_FAILURE, "quarantined", ("controlled-parser-failure",)),
    FixtureSpec("EML-012", "12-unknown-charset.eml", UNKNOWN_CHARSET, "indexed_with_warnings", ("unknown-charset",), ("unknown-charset:x-mneme-unknown",)),
    FixtureSpec("EML-013", "13-excessive-nesting.eml", DEEP_NESTING, "quarantined", ("excessive-nesting",)),
    FixtureSpec("EML-014", "14-invalid-base64.eml", INVALID_BASE64, "quarantined", ("invalid-transfer-encoding",)),
)


EXPECTED_HASHES: Dict[str, str] = {
    "EML-001": "befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208",
    "EML-002": "82a6bba4ab0b7cb5c29b8db4ec6c755d0e6f5694e4ab7a3f4f28ba5298e0f23a",
    "EML-003": "855df1de395bcda3f1b49f7951573b85d5462ab5643240732c76e69301c995a7",
    "EML-004": "7afcd03a25c0ca3b6af942916f7179ea6d8b246173739ebb5b3ef620220da121",
    "EML-005": "befec305981577844c8b233135125394886ffc26d7dedf589bbb152a0d51f208",
    "EML-006": "b6fe2178d33445a52b8b4f09fcc5c65483876df6a1ef2c5c8eb8e57b3b75bda2",
    "EML-007": "78e93f0ac3c122e9ad38c3f74ff89bb25704ec531deebdd44c83d3c92c07bbd0",
    "EML-008": "5858ca7dcc5ad2b5eb7b13a4785c483f8a7d88115eff67aa357154244ebb3726",
    "EML-009": "2027ede28398f83f6381418717cf186532d2d81425ac4af3461ae964e12cae1a",
    "EML-010": "79f58a4ca1dd972a93717074b41c8952f4ea929aaeecded0b7201c7ccd8f55f2",
    "EML-011": "5ec3b1c6783e095a33144bd9dc4aeb6885e61a7a674f0b4bf3ee0536d105039f",
    "EML-012": "4c98f370962a9d85b667be9d9ec084e5ad5f5775ba54840cdcb5ad61f938d299",
    "EML-013": "0aa7ed1418d120e07021cd7a763f1ca5710770f6791c88c534e36fd9ae2531ea",
    "EML-014": "12a994c79683eea8db343d6254d50b17ced5ece971a8acf48a828a80a9e7211f",
}


def materialize(destination: Path) -> Dict[str, Path]:
    if destination.exists():
        raise RuntimeError(f"fixture destination already exists: {destination}")
    destination.mkdir(parents=True, mode=0o700)
    paths: Dict[str, Path] = {}
    for fixture in FIXTURES:
        path = destination / fixture.filename
        path.write_bytes(fixture.data)
        path.chmod(0o400)
        paths[fixture.fixture_id] = path
    return paths


def catalog_rows() -> List[Dict[str, object]]:
    return [
        {
            "fixture_id": fixture.fixture_id,
            "filename": fixture.filename,
            "byte_count": len(fixture.data),
            "sha256": fixture.sha256,
            "expected_status": fixture.expected_status,
            "expected_warnings": list(fixture.expected_warnings),
            "features": list(fixture.features),
        }
        for fixture in FIXTURES
    ]
