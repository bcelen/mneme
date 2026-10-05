"""Fixed, wholly fictional threading fixtures: one EML set and one mboxrd container."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple


EXPERIMENT_ROOT = Path(__file__).resolve().parent
MBOXRD_PATH = EXPERIMENT_ROOT.parent / "mneme-local-prototype-3" / "mboxrd.py"


def _load_mboxrd():
    name = "mneme_threads_mboxrd"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, MBOXRD_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MBOXRD = _load_mboxrd()


def _message(lines: Iterable[str]) -> bytes:
    return ("\n".join(lines) + "\n").encode("utf-8")


def _headers(sender: str, recipient: str, date: str, message_id: str, subject: str) -> list:
    return [
        f"From: {sender}",
        f"To: {recipient}",
        f"Date: {date}",
        f"Message-ID: {message_id}",
        f"Subject: {subject}",
    ]


TAIL = ['MIME-Version: 1.0', 'Content-Type: text/plain; charset="us-ascii"', "Content-Transfer-Encoding: 7bit", ""]
ARIN = "Arin Vale <arin.vale@example.test>"
NILA = "Nila Hart <nila.hart@example.test>"
MIRA = "Mira Sol <mira.sol@example.test>"
ROWAN = "Rowan Pike <rowan.pike@example.test>"

ROOT = _message(
    _headers(ARIN, NILA, "Mon, 03 Nov 2025 09:00:00 +0000", "<dome-repair-301@example.test>", "Dome repair plan")
    + TAIL + ["The north dome hinge needs repair before the winter season."]
)
REPLY = _message(
    _headers(NILA, ARIN, "Mon, 03 Nov 2025 10:00:00 +0000", "<dome-repair-302@example.test>", "Re: Dome repair plan")
    + ["In-Reply-To: <dome-repair-301@example.test>", "References: <dome-repair-301@example.test>"]
    + TAIL + ["Agreed; the hinge parts arrive on Tuesday."]
)
# References is folded over two lines.
REPLY_TO_REPLY = _message(
    _headers(ARIN, NILA, "Tue, 04 Nov 2025 08:00:00 +0000", "<dome-repair-303@example.test>", "Re: Dome repair plan")
    + ["In-Reply-To: <dome-repair-302@example.test>",
       "References: <dome-repair-301@example.test>",
       " <dome-repair-302@example.test>"]
    + TAIL + ["Tuesday works; I will hold the dome closed."]
)
# Replies to a message that is not in the archive.
REPLY_TO_MISSING = _message(
    _headers(MIRA, ARIN, "Tue, 04 Nov 2025 12:00:00 +0000", "<dome-repair-304@example.test>", "Re: Dome repair costs")
    + ["In-Reply-To: <dome-repair-399@example.test>",
       "References: <dome-repair-301@example.test> <dome-repair-399@example.test>"]
    + TAIL + ["The cost estimate you forwarded looks reasonable."]
)
MALFORMED_REFERENCES = _message(
    _headers(NILA, MIRA, "Wed, 05 Nov 2025 09:00:00 +0000", "<observing-log-306@example.test>", "Observing log")
    + ["In-Reply-To: not a message id", "References: garbage without brackets"]
    + TAIL + ["Clear skies over the east dome tonight."]
)
LOOP_A = _message(
    _headers(ROWAN, NILA, "Thu, 06 Nov 2025 09:00:00 +0000", "<loop-a-307@example.test>", "Loop A")
    + ["In-Reply-To: <loop-b-308@example.test>"]
    + TAIL + ["This message claims to reply to loop B."]
)
LOOP_B = _message(
    _headers(NILA, ROWAN, "Thu, 06 Nov 2025 10:00:00 +0000", "<loop-b-308@example.test>", "Loop B")
    + ["In-Reply-To: <loop-a-307@example.test>"]
    + TAIL + ["This message claims to reply to loop A."]
)
# Same subject as the dome thread, but no reply headers: must not be threaded.
SUBJECT_ONLY = _message(
    _headers(MIRA, NILA, "Fri, 07 Nov 2025 09:00:00 +0000", "<subject-only-309@example.test>", "Re: Dome repair plan")
    + TAIL + ["Shares a subject with the dome thread but cites no message."]
)
MBOX_REPLY = _message(
    _headers(ROWAN, NILA, "Wed, 05 Nov 2025 16:00:00 +0000", "<dome-repair-305@example.test>", "Re: Dome repair plan")
    + ["In-Reply-To: <dome-repair-302@example.test>",
       "References: <dome-repair-301@example.test> <dome-repair-302@example.test>"]
    + TAIL + ["I can lend the spare hinge from the west dome."]
)
THREAD_MBOX = MBOXRD.build_record(b"From rowan.pike@example.test Wed Nov 05 16:00:00 2025\n", MBOX_REPLY)


@dataclass(frozen=True)
class ThreadFixture:
    fixture_id: str
    filename: str
    data: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


THREAD_FIXTURES: Tuple[ThreadFixture, ...] = (
    ThreadFixture("THR-301", "31-dome-repair-plan.eml", ROOT),
    ThreadFixture("THR-302", "32-re-dome-repair-plan.eml", REPLY),
    ThreadFixture("THR-303", "33-re-re-dome-repair-plan.eml", REPLY_TO_REPLY),
    ThreadFixture("THR-304", "34-reply-to-missing-parent.eml", REPLY_TO_MISSING),
    ThreadFixture("THR-306", "36-malformed-references.eml", MALFORMED_REFERENCES),
    ThreadFixture("THR-307", "37-loop-a.eml", LOOP_A),
    ThreadFixture("THR-308", "38-loop-b.eml", LOOP_B),
    ThreadFixture("THR-309", "39-subject-only.eml", SUBJECT_ONLY),
    ThreadFixture("THR-MBOX", "thread-replies.mbox", THREAD_MBOX),
)

EXPECTED_HASHES: Dict[str, str] = {
    "THR-301": "c00c8c74894e18e25fd21f0a179887313652cee4bbaf8f4d3f165ec6444597ca",
    "THR-302": "154462eeea08aea8005ab55f6dd5811eedcdd6e61b66975e2074cedd8bb484f7",
    "THR-303": "adfaf78c379898ae7f76210dcf967e54df8f13a97c453c7d873d89a2d1af40ef",
    "THR-304": "2819e8286c70f64afaf48011329dcb59e83119e38b43dc04f7cc987d8d69b7f5",
    "THR-306": "02c13f60532b5bc2384996b5920eacc9e3e3f6c01d20c05d7df77d664ee868a9",
    "THR-307": "04819bfbd0898710cb1b4b7e2a10cc08363df7bb5c60a30eec23591c473100e3",
    "THR-308": "92b5435f51a9d81ed08c452692b5ad1ccc611f464cbd41ca3aa0a71f67a85373",
    "THR-309": "d252f30243619f3bec87b6d94b11da413d8b33a3c63b1819a4c755e7e80c0bae",
    "THR-MBOX": "98295f7a7136e2636aae0f86b34c8d6b32dd321f04ab0a2605860b2b4118eabc",
}


def members() -> Tuple[Tuple[str, bytes], ...]:
    return tuple((fixture.filename, fixture.data) for fixture in THREAD_FIXTURES)


def reviewed_digests() -> Dict[str, str]:
    """Pinned digest -> family for every threading fixture."""

    return {
        EXPECTED_HASHES[f.fixture_id]: ("mbox" if f.filename.endswith(".mbox") else "eml")
        for f in THREAD_FIXTURES
    }
