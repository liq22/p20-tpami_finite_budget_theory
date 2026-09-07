#!/usr/bin/env python3
"""Set up PaperTrace Core and optionally enable the pinned ARIS backend."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import Any, Sequence

try:
    import yaml
except ImportError:  # bootstrapped into .venv below
    yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DIR = ROOT / ".papertrace"
LOCAL_STATE = LOCAL_DIR / "setup.json"
VENV_DIR = ROOT / ".venv"
ARIS_PATH = ROOT / "external/aris"
PROFILE_PATH = ROOT / "integrations/aris/profile.yaml"
PROFILE_ORDER = ("core", "execution", "review")


class SetupError(RuntimeError):
    """Raised when setup cannot continue without changing its meaning."""


def run(
    command: Sequence[str],
    *,
    cwd: Path = ROOT,
    check: bool = True,
    quiet: bool = False,
) -> subprocess.CompletedProcess[str]:
    if not quiet:
        print("$", " ".join(command))
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE if quiet else None,
            stderr=subprocess.STDOUT if quiet else None,
            check=False,
        )
    except FileNotFoundError as exc:
        raise SetupError(f"未找到命令：{command[0]}") from exc
    if check and result.returncode != 0:
        detail = f"\n{result.stdout.strip()}" if quiet and result.stdout else ""
        raise SetupError(f"命令执行失败：{' '.join(command)}{detail}")
    return result


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts/python.exe"
    return VENV_DIR / "bin/python"


def ensure_papertrace_directory() -> None:
    if not (ROOT / "paper/paper.yaml").is_file():
        raise SetupError(f"请在 PaperTrace 目录中运行；未找到 {ROOT / 'paper/paper.yaml'}")


def ensure_git_repository() -> None:
    if shutil.which("git") is None:
        raise SetupError("该模式需要 Git 以初始化固定版本的 ARIS 子模块。")
    result = run(["git", "rev-parse", "--show-toplevel"], quiet=True, check=False)
    if result.returncode != 0 or not result.stdout.strip():
        raise SetupError(
            "Research Execution / Advanced Review 需要 Git clone。Core 模式可直接在普通目录中使用；"
            "需要 ARIS 时请用 `git clone https://github.com/liq22/PaperTrace.git`。"
        )
    root = Path(result.stdout.strip()).resolve()
    if root != ROOT:
        raise SetupError(f"请在 PaperTrace 仓库中运行；当前 Git 根目录为 {root}")


def ensure_venv(*, recreate: bool = False) -> Path:
    python = venv_python()
    if recreate and VENV_DIR.exists():
        shutil.rmtree(VENV_DIR)
    if not python.is_file():
        print("\n创建隔离的 Python 环境 .venv ...")
        try:
            venv.EnvBuilder(with_pip=True, clear=False).create(VENV_DIR)
        except (OSError, subprocess.SubprocessError) as exc:
            raise SetupError(
                "无法创建 Python 虚拟环境。Debian/Ubuntu 请先运行 "
                "`sudo apt install python3-venv`；Windows/macOS 请确认安装的是包含 "
                "venv 和 pip 的完整 Python 3.10+。"
            ) from exc
    if not python.is_file():
        raise SetupError(f"虚拟环境创建失败：未找到 {python}")
    return python


def install_dependencies(python: Path) -> None:
    requirements = ROOT / "requirements-dev.txt"
    print("\n安装 PaperTrace 最小依赖 ...")
    run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(requirements),
        ]
    )


def bootstrap_yaml(argv: list[str], *, recreate_venv: bool, skip_deps: bool) -> int | None:
    """Re-run inside .venv when the host Python does not yet provide PyYAML."""
    if yaml is not None:
        return None
    python = ensure_venv(recreate=recreate_venv)
    if not skip_deps:
        install_dependencies(python)
    forwarded = [arg for arg in argv if arg != "--recreate-venv"]
    if "--skip-deps" not in forwarded:
        forwarded.append("--skip-deps")
    return run([str(python), str(Path(__file__).resolve()), *forwarded], check=False).returncode


def load_profiles() -> dict[str, dict[str, Any]]:
    if yaml is None:  # pragma: no cover - handled by bootstrap_yaml
        raise SetupError("PyYAML is unavailable after environment bootstrap.")
    try:
        config = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SetupError(f"无法读取 {PROFILE_PATH}: {exc}") from exc
    profiles = config.get("profiles") if isinstance(config, dict) else None
    if not isinstance(profiles, dict):
        raise SetupError("ARIS profile.yaml 缺少 profiles mapping。")
    result: dict[str, dict[str, Any]] = {}
    for name in PROFILE_ORDER:
        value = profiles.get(name)
        if not isinstance(value, dict):
            raise SetupError(f"ARIS profile.yaml 缺少 {name!r} profile。")
        result[name] = value
    return result


def choose_profile(profiles: dict[str, dict[str, Any]]) -> str:
    print("\n请选择使用模式：\n")
    for index, name in enumerate(PROFILE_ORDER, start=1):
        profile = profiles[name]
        suffix = "（默认）" if name == "core" else ""
        print(f"  {index}. {profile.get('label', name)}{suffix}")
        print(f"     {profile.get('description', '')}\n")
    try:
        answer = input("选择 [1]: ").strip() or "1"
    except EOFError as exc:
        raise SetupError(
            "当前终端不支持交互输入。请添加 `--non-interactive`，或显式指定 "
            "`--profile core|execution|review`。"
        ) from exc
    mapping = {str(index): name for index, name in enumerate(PROFILE_ORDER, start=1)}
    if answer not in mapping:
        raise SetupError("请输入 1、2 或 3。")
    return mapping[answer]


def initialize_aris() -> None:
    print("\n初始化可选 ARIS 后端（固定到 PaperTrace 记录的版本）...")
    run(["git", "submodule", "sync", "--", "external/aris"])
    shallow = run(
        [
            "git",
            "-c",
            "protocol.version=2",
            "submodule",
            "update",
            "--init",
            "--depth",
            "1",
            "--",
            "external/aris",
        ],
        check=False,
    )
    if shallow.returncode != 0:
        print("浅克隆未能取得固定 commit，改用完整子模块获取 ...")
        run(
            [
                "git",
                "-c",
                "protocol.version=2",
                "submodule",
                "update",
                "--init",
                "--",
                "external/aris",
            ]
        )
    if not (ARIS_PATH / "AGENT_GUIDE.md").is_file():
        raise SetupError("ARIS 子模块初始化后仍缺少 AGENT_GUIDE.md。")


def write_local_state(profile: str, profiles: dict[str, dict[str, Any]]) -> None:
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "schema_version": 1,
        "profile": profile,
        "aris_enabled": bool(profiles[profile].get("initialize_submodule")),
        "aris_host_skills_exposed": False,
        "venv": ".venv",
    }
    LOCAL_STATE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def run_checks(python: Path, profile: str, profiles: dict[str, dict[str, Any]]) -> None:
    print("\n检查安装结果 ...")
    command = [
        str(python),
        str(ROOT / "scripts/check_aris_backend.py"),
        "--profile",
        profile,
    ]
    if bool(profiles[profile].get("initialize_submodule")):
        command.append("--require-initialized")
    run(command)
    run([str(python), str(ROOT / "src/S03_Scripts/validate_project.py")])


def activation_command() -> str:
    if os.name == "nt":
        return r".venv\Scripts\Activate.ps1"
    return "source .venv/bin/activate"


def print_success(profile: str, profiles: dict[str, dict[str, Any]]) -> None:
    label = str(profiles[profile].get("label", profile))
    print("\n" + "=" * 68)
    print(f"PaperTrace 已就绪：{label}")
    print("=" * 68)
    print("\n以后进入目录后，可先激活环境：")
    print(f"  {activation_command()}")
    print("\n然后直接告诉 Agent：")
    print(
        "  读取 paper/paper.yaml，选择当前最重要的一个研究或实现问题，\n"
        "  直接修改主要产物并运行最小验证；不要只输出计划、状态报告或审查材料。"
    )
    if profile == "execution":
        print("\nARIS 仅作为内部执行后端；不会新增用户需要学习的 slash command。")
    elif profile == "review":
        print("\n独立审查能力已启用，但只有明确提出“独立核验/审查”时才会调用。")
    else:
        print("\n需要外部实验或图表后端时，再显式运行：")
        print("  python scripts/setup_papertrace.py --profile execution")


def saved_profile() -> str:
    if not LOCAL_STATE.is_file():
        return "core"
    try:
        data = json.loads(LOCAL_STATE.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SetupError(
            f"无法读取本地状态 {LOCAL_STATE}: {exc}。请修复或删除该文件后显式选择 profile。"
        ) from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise SetupError(f"本地状态 {LOCAL_STATE} 必须是 schema_version: 1 mapping。")
    profile = data.get("profile")
    if profile not in PROFILE_ORDER:
        raise SetupError(f"本地状态 {LOCAL_STATE} 包含无效 profile：{profile!r}")
    return str(profile)


def check_only(profile: str | None, profiles: dict[str, dict[str, Any]]) -> int:
    python = venv_python() if venv_python().is_file() else Path(sys.executable)
    selected = profile or saved_profile()
    command = [
        str(python),
        str(ROOT / "scripts/check_aris_backend.py"),
        "--profile",
        selected,
    ]
    if bool(profiles[selected].get("initialize_submodule")):
        command.append("--require-initialized")
    return run(command, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="一条命令完成 PaperTrace Core 初始化，并可显式启用 ARIS。"
    )
    parser.add_argument("--profile", choices=PROFILE_ORDER)
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--skip-deps", action="store_true")
    parser.add_argument("--recreate-venv", action="store_true")
    args = parser.parse_args(raw_argv)

    try:
        ensure_papertrace_directory()
        bootstrapped = bootstrap_yaml(
            raw_argv,
            recreate_venv=args.recreate_venv,
            skip_deps=args.skip_deps,
        )
        if bootstrapped is not None:
            return bootstrapped

        profiles = load_profiles()
        if args.check_only:
            return check_only(args.profile, profiles)

        profile = args.profile
        if profile is None:
            profile = "core" if args.non_interactive else choose_profile(profiles)
        selected = profiles[profile]

        print(f"\n模式：{selected.get('label', profile)}")
        print(selected.get("description", ""))

        if bool(selected.get("initialize_submodule")):
            ensure_git_repository()

        python = ensure_venv(recreate=args.recreate_venv)
        if not args.skip_deps:
            install_dependencies(python)
        if bool(selected.get("initialize_submodule")):
            initialize_aris()

        write_local_state(profile, profiles)
        run_checks(python, profile, profiles)
        print_success(profile, profiles)
        return 0
    except KeyboardInterrupt:
        print("\n已取消安装；未完成的本地环境可以安全删除后重新运行。")
        return 130
    except SetupError as exc:
        print(f"\nERROR: {exc}")
        print("\n可显式检查 Core 状态：")
        print("  python scripts/setup_papertrace.py --check-only --profile core")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
