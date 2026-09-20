#!/usr/bin/env python3
"""Small synthetic-only process boundary for the EML parser experiment."""

from __future__ import annotations

import ctypes
import hashlib
import multiprocessing
import os
import resource
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping

import hardening


WALL_TIMEOUT_SECONDS = 2.5
CPU_LIMIT_SECONDS = 1
MEMORY_LIMIT_BYTES = 64 * 1024 * 1024
FILE_LIMIT_BYTES = 1024 * 1024
OPEN_FILE_LIMIT = 32

LIMIT_PROFILE: Dict[str, Any] = {
    "cpu_seconds": CPU_LIMIT_SECONDS,
    "memory_bytes": MEMORY_LIMIT_BYTES,
    "wall_seconds": WALL_TIMEOUT_SECONDS,
}


@dataclass(frozen=True)
class IsolationEvidence:
    parent_pid: int
    worker_pid: int | None
    source_sha256: str
    termination: str
    temporary_root: str | None
    temporary_root_removed: bool
    peak_resident_bytes: int | None = None


@dataclass(frozen=True)
class IsolatedParseResult:
    artifacts: Dict[str, bytes]
    evidence: IsolationEvidence
    occurrences: List[Dict[str, Any]]
    record: Dict[str, Any]

    def parser_tuple(self):
        return self.record, self.occurrences, self.artifacts


def _marker() -> Dict[str, Any]:
    return {
        "limits": dict(LIMIT_PROFILE),
        "mode": "one-source-per-process",
    }


def _quarantine(
    item: Mapping[str, Any], recorded_at: str, failure: str
) -> Dict[str, Any]:
    return {
        "failure": failure,
        "isolation": _marker(),
        "provenance": {
            "event": "derive",
            "event_id": f"prov-derive-{item['id'].lower()}",
            "input_event_id": item["provenance"]["event_id"],
            "recorded_at": recorded_at,
            "rule": hardening.PROCESSING_RULE,
            "tool": {
                "name": hardening.TOOL_NAME,
                "version": hardening.TOOL_VERSION,
            },
        },
        "source_id": item["id"],
        "source_sha256": item["sha256"],
        "status": "quarantined",
        "warnings": [],
    }


def _failure_result(
    item: Mapping[str, Any],
    recorded_at: str,
    failure: str,
    evidence: IsolationEvidence,
) -> IsolatedParseResult:
    return IsolatedParseResult(
        artifacts={},
        evidence=evidence,
        occurrences=[],
        record=_quarantine(item, recorded_at, failure),
    )


def _synthetic_mode(raw: bytes) -> str | None:
    headers = raw.replace(b"\r\n", b"\n").split(b"\n\n", 1)[0]
    for line in headers.split(b"\n"):
        name, separator, value = line.partition(b":")
        if separator and name.strip().lower() == b"x-mneme-synthetic-isolation":
            mode = value.strip().lower()
            if mode in {b"memory", b"timeout"}:
                return mode.decode("ascii")
    return None


def _apply_child_limits() -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_LIMIT_SECONDS, CPU_LIMIT_SECONDS))
    resource.setrlimit(resource.RLIMIT_FSIZE, (FILE_LIMIT_BYTES, FILE_LIMIT_BYTES))
    resource.setrlimit(resource.RLIMIT_NOFILE, (OPEN_FILE_LIMIT, OPEN_FILE_LIMIT))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    try:
        resource.setrlimit(
            resource.RLIMIT_DATA, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES)
        )
    except (OSError, ValueError):
        # macOS rejects this finite value for the recorded Python runtime. The
        # parent enforces the same ceiling from the child's resident size.
        pass


class _DarwinTaskInfo(ctypes.Structure):
    _fields_ = [
        (name, ctypes.c_uint64)
        for name in (
            "virtual_size",
            "resident_size",
            "total_user",
            "total_system",
            "threads_user",
            "threads_system",
        )
    ] + [
        (name, ctypes.c_int32)
        for name in (
            "policy",
            "faults",
            "pageins",
            "copy_on_write_faults",
            "messages_sent",
            "messages_received",
            "mach_syscalls",
            "unix_syscalls",
            "context_switches",
            "thread_count",
            "running_thread_count",
            "priority",
        )
    ]


def _resident_bytes(pid: int) -> int | None:
    if sys.platform == "darwin":
        try:
            library = ctypes.CDLL("/usr/lib/libproc.dylib")
            task_info = _DarwinTaskInfo()
            size = library.proc_pidinfo(
                pid,
                4,
                0,
                ctypes.byref(task_info),
                ctypes.sizeof(task_info),
            )
            if size == ctypes.sizeof(task_info):
                return int(task_info.resident_size)
        except (AttributeError, OSError):
            pass
    elif sys.platform.startswith("linux"):
        try:
            fields = Path(f"/proc/{pid}/statm").read_text(encoding="ascii").split()
            return int(fields[1]) * os.sysconf("SC_PAGE_SIZE")
        except (IndexError, OSError, ValueError):
            pass
    return None


def _worker(connection, item, raw: bytes, recorded_at: str, working_root: str) -> None:
    try:
        os.chdir(working_root)
        _apply_child_limits()
        mode = _synthetic_mode(raw)
        if mode == "timeout":
            while True:
                pass
        if mode == "memory":
            try:
                allocation = bytearray(MEMORY_LIMIT_BYTES * 2)
            except MemoryError:
                connection.send({"kind": "memory-limit", "pid": os.getpid()})
                return
            for offset in range(0, len(allocation), 4096):
                allocation[offset] = 1
            time.sleep(WALL_TIMEOUT_SECONDS * 2)
        record, occurrences, artifacts = hardening._parse_source(
            item, raw, recorded_at
        )
        connection.send(
            {
                "artifacts": artifacts,
                "kind": "ok",
                "occurrences": occurrences,
                "pid": os.getpid(),
                "record": record,
            }
        )
    except (OSError, TypeError, ValueError) as error:
        connection.send({"failure": str(error), "kind": "error", "pid": os.getpid()})
    finally:
        connection.close()


def run_isolated_parse(
    item: Mapping[str, Any], raw: bytes, recorded_at: str
) -> IsolatedParseResult:
    parent_pid = os.getpid()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != item.get("sha256") or len(raw) > hardening.MAX_SOURCE_BYTES:
        mismatch = digest != item.get("sha256")
        failure = (
            "source hash mismatch"
            if mismatch
            else f"source size {len(raw)} exceeds limit {hardening.MAX_SOURCE_BYTES}"
        )
        evidence = IsolationEvidence(
            parent_pid=parent_pid,
            worker_pid=None,
            source_sha256=digest,
            termination=(
                "preflight-hash-mismatch" if mismatch else "preflight-size-limit"
            ),
            temporary_root=None,
            temporary_root_removed=True,
        )
        return _failure_result(item, recorded_at, failure, evidence)

    mode = _synthetic_mode(raw)
    payload = None
    peak_resident = 0
    termination = "worker-exit"
    worker_pid: int | None = None
    temporary_root_text: str | None = None
    with tempfile.TemporaryDirectory(prefix="mneme-parser-isolation-") as directory:
        os.chmod(directory, 0o700)
        temporary_root_text = directory
        context = multiprocessing.get_context("fork")
        receiver, sender = context.Pipe(duplex=False)
        process = context.Process(
            target=_worker,
            args=(sender, dict(item), raw, recorded_at, directory),
        )
        process.start()
        worker_pid = process.pid
        sender.close()
        deadline = time.monotonic() + WALL_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            resident = _resident_bytes(process.pid)
            if resident is not None:
                peak_resident = max(peak_resident, resident)
                if resident > MEMORY_LIMIT_BYTES:
                    termination = "memory-limit"
                    process.kill()
                    break
            if receiver.poll(0.005):
                try:
                    payload = receiver.recv()
                    termination = "completed"
                except EOFError:
                    termination = "worker-exit"
                break
            if not process.is_alive():
                break
        else:
            termination = "wall-time-limit"
            process.kill()
        process.join(timeout=1.0)
        if process.is_alive():
            process.kill()
            process.join()
        receiver.close()

    evidence = IsolationEvidence(
        parent_pid=parent_pid,
        worker_pid=worker_pid,
        source_sha256=digest,
        termination=termination,
        temporary_root=temporary_root_text,
        temporary_root_removed=(
            temporary_root_text is not None
            and not Path(temporary_root_text).exists()
        ),
        peak_resident_bytes=peak_resident,
    )
    if termination == "memory-limit" or (
        isinstance(payload, dict) and payload.get("kind") == "memory-limit"
    ):
        return _failure_result(
            item, recorded_at, "parser memory limit exceeded", evidence
        )
    if termination == "wall-time-limit" or (mode == "timeout" and payload is None):
        return _failure_result(
            item, recorded_at, "parser time limit exceeded", evidence
        )
    if not isinstance(payload, dict) or payload.get("kind") != "ok":
        return _failure_result(
            item, recorded_at, "parser worker failed closed", evidence
        )
    if payload.get("pid") != worker_pid or worker_pid == parent_pid:
        return _failure_result(
            item, recorded_at, "parser worker identity mismatch", evidence
        )
    record = payload["record"]
    record["isolation"] = _marker()
    return IsolatedParseResult(
        artifacts=payload["artifacts"],
        evidence=evidence,
        occurrences=payload["occurrences"],
        record=record,
    )


def isolated_parser(item: Mapping[str, Any], raw: bytes, recorded_at: str):
    return run_isolated_parse(item, raw, recorded_at).parser_tuple()
