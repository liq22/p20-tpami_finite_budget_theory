"""Small LibreOffice subprocess helper for normal research environments."""
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
    env = {key: os.environ[key] for key in _SOFFICE_ENV_KEYS if key in os.environ}
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["soffice", *args], env=get_soffice_env(), **kwargs)
