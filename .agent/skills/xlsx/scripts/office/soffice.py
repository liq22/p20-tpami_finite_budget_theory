"""Small LibreOffice subprocess helper.

PaperTrace targets normal research environments with a working ``soffice``
installation. It does not compile or cache a custom socket shim for uncommon
sandbox restrictions.
"""
from __future__ import annotations

import os
import subprocess

_SOFFICE_ENV_KEYS = (
    "PATH",
    "HOME",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TMPDIR",
    "TMP",
    "TEMP",
    "USER",
)


def get_soffice_env() -> dict[str, str]:
    """Return a small environment suitable for headless LibreOffice."""
    env = {key: os.environ[key] for key in _SOFFICE_ENV_KEYS if key in os.environ}
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run ``soffice`` with the minimal environment above."""
    return subprocess.run(["soffice", *args], env=get_soffice_env(), **kwargs)
