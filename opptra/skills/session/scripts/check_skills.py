#!/usr/bin/env python3
"""Check origin/main and update a clean installed skills checkout."""

from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check, capture_output=True, text=True, timeout=15,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )


def checkout_state() -> tuple[str, str, str]:
    return (
        git("rev-parse", "HEAD").stdout.strip(),
        git("symbolic-ref", "--quiet", "--short", "HEAD", check=False).stdout.strip(),
        git("status", "--porcelain", "--untracked-files=normal").stdout.strip(),
    )


def relink() -> None:
    subprocess.run(
        ["bash", str(ROOT / "install.sh"), "--skills-only"],
        check=True, capture_output=True, text=True, timeout=30,
    )


def check_skills() -> dict:
    result = {"status": "unverified", "checkout": str(ROOT), "updated": False}
    try:
        repository = git("rev-parse", "--show-toplevel", check=False)
        if repository.returncode != 0:
            return {**result, "status": "managed-install",
                    "message": "This skill has no Git checkout. Use the host's plugin updater."}
        top = Path(repository.stdout.strip()).resolve()
        if top != ROOT:
            return {**result, "status": "managed-install",
                    "message": "This skill is not in its own Git checkout. Use the host's plugin updater."}
        before, branch, dirty = checkout_state()
        result["commit"] = before
        remote = git("ls-remote", "--exit-code", "origin", "refs/heads/main").stdout.split()[0]
        result["latest_commit"] = remote
        if branch != "main" or dirty:
            return {
                **result, "status": "local-development", "current": before == remote and not dirty,
                "message": "Skills checkout has local changes or is off main. Continue with the local version and report it.",
            }
        if before == remote:
            relink()
            return {**result, "status": "current", "current": True}

        # Share the lock between worktrees. The OS releases it if the process exits.
        common = Path(git("rev-parse", "--git-common-dir").stdout.strip())
        if not common.is_absolute():
            common = ROOT / common
        with (common / "opptra-skills-update.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return {**result, "status": "busy",
                        "message": "Another skills update is running. Recheck before using the skill."}
            git("fetch", "--no-tags", "origin", "+refs/heads/main:refs/remotes/origin/main")
            latest = git("rev-parse", "refs/remotes/origin/main").stdout.strip()
            result["latest_commit"] = latest
            head, branch, dirty = checkout_state()
            if branch != "main" or dirty:
                return {**result, "status": "local-development",
                        "message": "Checkout changed during the check. Continue with its local version and report it."}
            ancestor = git("merge-base", "--is-ancestor", head, latest, check=False)
            if ancestor.returncode != 0:
                return {**result, "status": "local-development",
                        "message": "Local main has commits outside origin/main. Keep them and report the local version."}
            git("merge", "--ff-only", latest)
            result.update(commit=latest, updated=latest != before)
            relink()
        return {**result, "status": "updated", "current": True}
    except subprocess.TimeoutExpired:
        if result["updated"]:
            return {**result, "status": "relink-required",
                    "message": "Skills updated, but linking timed out. Run install.sh --skills-only before proceeding."}
        return {**result, "message": "Skills check timed out. Continue with the installed version and report it as unverified."}
    except (OSError, subprocess.CalledProcessError, IndexError):
        if result["updated"]:
            return {**result, "status": "relink-required",
                    "message": "Skills were updated, but linking failed. Run install.sh --skills-only before proceeding."}
        return {**result, "message": "Could not verify or update skills. Continue with the installed version and report it as unverified."}


def main() -> int:
    result = check_skills()
    print(json.dumps(result))
    return 1 if result["status"] in ("busy", "relink-required") else 0


if __name__ == "__main__":
    sys.exit(main())
