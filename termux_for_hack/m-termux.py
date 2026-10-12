#!/usr/bin/env python3
"""Interactive, opt-in package setup helper for Termux."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import TextIO


BASE_PROFILES: dict[str, tuple[str, ...]] = {
    "basic": ("curl", "git", "python", "wget"),
    "developer": ("clang", "cmake", "git", "make", "pkg-config", "python"),
    "security": (
        "curl",
        "git",
        "nmap",
        "openssh",
        "openssl",
        "perl",
        "php",
        "python",
        "ruby",
        "wget",
    ),
}

PROFILE_PACKAGES: dict[str, tuple[str, ...]] = {
    **BASE_PROFILES,
    "all": tuple(sorted({package for values in BASE_PROFILES.values() for package in values})),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Preview a curated Termux package profile. Installation is opt-in "
            "and requires the --install flag."
        )
    )
    parser.add_argument(
        "--profile",
        choices=tuple(PROFILE_PACKAGES),
        default="basic",
        help="Package profile to use (default: basic).",
    )
    parser.add_argument(
        "--list",
        dest="list_profiles",
        action="store_true",
        help="List available profiles and their package lists, then exit.",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Run pkg update and pkg upgrade before installing packages.",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install the selected packages after confirmation.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt (requires --install).",
    )
    return parser


def print_profiles(stream: TextIO) -> None:
    print("Available Termux package profiles:", file=stream)
    for name, packages in PROFILE_PACKAGES.items():
        print(f"  {name:<10} {', '.join(packages)}", file=stream)


def is_termux(environment: Mapping[str, str]) -> bool:
    """Return whether the supplied environment looks like a Termux session."""
    return "com.termux" in environment.get("PREFIX", "") or bool(
        environment.get("TERMUX_VERSION")
    )


def planned_commands(pkg_path: str, packages: Sequence[str], upgrade: bool) -> list[list[str]]:
    """Build the commands that would be run, without executing a shell."""
    commands: list[list[str]] = []
    if upgrade:
        commands.extend(([pkg_path, "update"], [pkg_path, "upgrade", "-y"]))
    commands.append([pkg_path, "install", "-y", *packages])
    return commands


def main(
    argv: Sequence[str] | None = None,
    *,
    run: Callable[..., object] = subprocess.run,
    input_fn: Callable[[str], str] = input,
    output: TextIO | None = None,
    environment: Mapping[str, str] | None = None,
    which: Callable[[str], str | None] = shutil.which,
) -> int:
    """Run the setup CLI; injected I/O and environment make it testable."""
    stream = sys.stdout if output is None else output
    current_environment = os.environ if environment is None else environment
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.yes and not args.install:
        parser.error("--yes can only be used together with --install.")

    if args.list_profiles:
        print_profiles(stream)
        return 0

    packages = PROFILE_PACKAGES[args.profile]
    print(f"Selected profile: {args.profile}", file=stream)
    print(f"Packages ({len(packages)}): {', '.join(packages)}", file=stream)

    if args.upgrade:
        print("Planned updates: pkg update, then pkg upgrade -y", file=stream)
    print(f"Planned install: pkg install -y {' '.join(packages)}", file=stream)

    if not args.install:
        print("Dry run only; no changes were made. Add --install to continue.", file=stream)
        return 0

    if not is_termux(current_environment):
        print(
            "Refusing to install: run this command from inside the Termux Android app.",
            file=stream,
        )
        return 1

    pkg_path = which("pkg")
    if not pkg_path:
        print("Could not find the Termux 'pkg' command in PATH.", file=stream)
        return 1

    commands = planned_commands(pkg_path, packages, args.upgrade)
    if not args.yes:
        try:
            answer = input_fn("Proceed with the displayed Termux package operations? [y/N] ")
        except EOFError:
            print("No confirmation received; installation cancelled.", file=stream)
            return 1

        if answer.strip().lower() not in {"y", "yes"}:
            print("Installation cancelled; no changes were made.", file=stream)
            return 0

    for command in commands:
        print(f"$ {' '.join(command)}", file=stream)
        try:
            result = run(command, check=False)
        except OSError as exc:
            print(f"Could not start {' '.join(command)}: {exc}", file=stream)
            return 1

        return_code = getattr(result, "returncode", 1)
        if return_code != 0:
            print(f"Command failed with status {return_code}. Stopping.", file=stream)
            return return_code if isinstance(return_code, int) and return_code > 0 else 1

    print("Termux package setup completed.", file=stream)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
