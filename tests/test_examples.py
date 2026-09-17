"""Platform-independent checks for synthetic example scripts."""

from __future__ import annotations

import importlib.util
import os
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPO_ROOT / "examples"
SRC = REPO_ROOT / "src"

FORBIDDEN_IMPORT_PREFIXES = (
    "urllib",
    "requests",
    "http.client",
    "httpx",
    "aiohttp",
    "ftplib",
)


def _run_example_subprocess(script_name: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(SRC), existing) if part
    )
    return subprocess.run(
        [sys.executable, str(EXAMPLES / script_name)],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _load_example_module(script_name: str):
    path = EXAMPLES / script_name
    spec = importlib.util.spec_from_file_location(f"examples_{path.stem}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_basic_flow_runs_and_keeps_higher_lanes_absent(capsys):
    module = _load_example_module("basic_flow.py")
    assert module.main() == 0
    output = capsys.readouterr().out

    assert "trace_integrity: VALID" in output
    assert "JOB_AGENT: PRESENT" in output
    assert "VECTOR: PRESENT" in output
    assert "EIG: PRESENT" in output
    assert "EXECUTOR: PRESENT" in output
    assert "WEAVER: PRESENT" in output
    assert "HUMAN: NOT_PRESENT" in output
    assert "EXTERNAL_IW: NOT_PRESENT" in output
    assert "CANONICAL: NOT_PRESENT" in output
    assert "PUBLICATION: NOT_PRESENT" in output
    assert "verification_does_not_equal_human_acceptance: true" in output


def test_publication_separation_shows_approval_without_publish(monkeypatch, capsys):
    source = (EXAMPLES / "publication_separation.py").read_text(encoding="utf-8")
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            for prefix in FORBIDDEN_IMPORT_PREFIXES:
                assert prefix not in stripped, stripped

    def _block_connect(*_args, **_kwargs):
        raise AssertionError("network access is not allowed in this demo")

    monkeypatch.setattr(socket.socket, "connect", _block_connect)

    def _block_urlopen(*_args, **_kwargs):
        raise AssertionError("network access is not allowed in this demo")

    monkeypatch.setattr(urllib.request, "urlopen", _block_urlopen)

    module = _load_example_module("publication_separation.py")
    assert module.main() == 0
    output = capsys.readouterr().out

    assert "publication_authority_record_present: true" in output
    assert "publication_performed: false" in output


@pytest.mark.parametrize(
    "script_name",
    ["basic_flow.py", "publication_separation.py"],
)
def test_examples_exit_zero_via_subprocess(script_name: str):
    completed = _run_example_subprocess(script_name)
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() != ""
