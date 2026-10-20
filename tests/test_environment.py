"""Smoke tests for the development environment (F1-T00f).

They prove that pytest runs in CI and that the interpreter matches the
version pinned in .python-version (ADR-016).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_python_matches_pinned_version() -> None:
    pinned = (REPO_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    running = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert running == pinned


def test_env_example_has_no_real_passwords() -> None:
    lines = (REPO_ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
    names = ("PASSWORD", "KEY")
    secrets = [line for line in lines if line.split("=", 1)[0].endswith(names)]
    assert secrets, "expected password and key placeholders in .env.example"
    for line in secrets:
        assert line.split("=", 1)[1] == "change-me", line
