"""Exercise skill updates against local Git remotes without touching installations."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPER = Path("opptra/skills/session/scripts/check_skills.py")


class SkillFreshnessTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        self.origin = self.base / "origin.git"
        self.author = self.base / "author"
        self.client = self.base / "client"
        self.home = self.base / "home"
        self.home.mkdir()
        self.env = dict(os.environ, HOME=str(self.home), GIT_TERMINAL_PROMPT="0",
                        GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
        self.git(self.base, "init", "--bare", "--initial-branch=main", str(self.origin))
        self.git(self.base, "clone", str(self.origin), str(self.author))
        (self.author / HELPER).parent.mkdir(parents=True)
        shutil.copy2(ROOT / HELPER, self.author / HELPER)
        shutil.copy2(ROOT / "install.sh", self.author / "install.sh")
        (self.author / "bin").mkdir()
        shutil.copy2(ROOT / "bin/odlc", self.author / "bin/odlc")
        (self.author / "opptra/skills/session/SKILL.md").write_text("Shared reference\n")
        sample = self.author / "opptra/skills/sample"
        sample.mkdir()
        (sample / "SKILL.md").write_text("Version one\n")
        self.publish("initial")
        self.git(self.base, "clone", str(self.origin), str(self.client))

    def git(self, directory, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(directory), "-c", "user.name=Skill fixture",
             "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", *args],
            env=self.env, check=check, capture_output=True, text=True,
        ).stdout.strip()

    def publish(self, message):
        self.git(self.author, "add", ".")
        self.git(self.author, "commit", "-m", message)
        self.git(self.author, "push", "origin", "main")
        return self.git(self.author, "rev-parse", "HEAD")

    def run_check(self):
        run = subprocess.run(
            [sys.executable, str(self.client / HELPER)],
            env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        return json.loads(run.stdout)

    def test_current_and_every_request_rechecks_upstream(self):
        current = self.run_check()
        self.assertEqual(current["status"], "current")
        self.assertFalse(current["updated"])
        (self.author / "opptra/skills/sample/SKILL.md").write_text("Version two\n")
        latest = self.publish("update sample")
        updated = self.run_check()
        self.assertEqual(updated["status"], "updated")
        self.assertEqual(updated["commit"], latest)
        self.assertEqual((self.client / "opptra/skills/sample/SKILL.md").read_text(), "Version two\n")
        self.assertEqual((self.home / ".codex/skills/sample").resolve(),
                         self.client / "opptra/skills/sample")
        self.assertFalse((self.home / ".cache/opptra/sdlc-resources.git").exists())

    def test_dirty_checkout_keeps_changes(self):
        target = self.client / "opptra/skills/sample/SKILL.md"
        target.write_text("Local edits\n")
        before = self.git(self.client, "rev-parse", "HEAD")
        (self.author / "opptra/skills/sample/SKILL.md").write_text("Remote edits\n")
        latest = self.publish("upstream change")
        result = self.run_check()
        self.assertEqual(result["status"], "local-development")
        self.assertEqual(result["latest_commit"], latest)
        self.assertEqual(self.git(self.client, "rev-parse", "HEAD"), before)
        self.assertEqual(target.read_text(), "Local edits\n")

    def test_feature_branch_is_preserved(self):
        self.git(self.client, "checkout", "-b", "skill/local")
        result = self.run_check()
        self.assertEqual(result["status"], "local-development")
        self.assertEqual(self.git(self.client, "branch", "--show-current"), "skill/local")

    def test_divergent_main_is_preserved(self):
        local = self.client / "opptra/skills/sample/SKILL.md"
        local.write_text("Committed local edits\n")
        self.git(self.client, "add", ".")
        self.git(self.client, "commit", "-m", "local work")
        before = self.git(self.client, "rev-parse", "HEAD")
        (self.author / "opptra/skills/sample/SKILL.md").write_text("Upstream edits\n")
        self.publish("upstream work")
        result = self.run_check()
        self.assertEqual(result["status"], "local-development")
        self.assertEqual(self.git(self.client, "rev-parse", "HEAD"), before)

    def test_offline_reports_unverified(self):
        self.git(self.client, "remote", "set-url", "origin", str(self.base / "missing.git"))
        result = self.run_check()
        self.assertEqual(result["status"], "unverified")
        self.assertFalse(result["updated"])

    def test_renamed_skill_refreshes_owned_links_only(self):
        self.run_check()
        unrelated = self.home / ".codex/skills/unrelated"
        unrelated.symlink_to(self.base / "unrelated-target")
        self.git(self.author, "mv", "opptra/skills/sample", "opptra/skills/renamed")
        self.publish("rename sample")
        result = self.run_check()
        self.assertEqual(result["status"], "updated")
        self.assertFalse((self.home / ".codex/skills/sample").is_symlink())
        self.assertEqual((self.home / ".codex/skills/renamed").resolve(),
                         self.client / "opptra/skills/renamed")
        self.assertTrue(unrelated.is_symlink())

    def test_managed_install_reports_host_update_path(self):
        install = self.base / "managed"
        helper = install / HELPER
        helper.parent.mkdir(parents=True)
        shutil.copy2(ROOT / HELPER, helper)
        run = subprocess.run([sys.executable, str(helper)], env=self.env,
                             check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(run.stdout)["status"], "managed-install")

    def test_relink_failure_after_update_requires_repair(self):
        (self.author / "install.sh").write_text("#!/bin/sh\nexit 31\n")
        latest = self.publish("broken link setup")
        run = subprocess.run([sys.executable, str(self.client / HELPER)], env=self.env,
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "relink-required")
        self.assertEqual(result["commit"], latest)
        self.assertTrue(result["updated"])

    def test_every_skill_has_the_preflight(self):
        for skill in (ROOT / "opptra/skills").glob("*/SKILL.md"):
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text()
                self.assertIn("Skill freshness" if skill.parent.name == "session" else "## Skill version check", text)


if __name__ == "__main__":
    unittest.main()
