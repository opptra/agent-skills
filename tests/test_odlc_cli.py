"""Offline checks for the installed agent CLI and legacy-link migration."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OdlcInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / 'agent-skills'
        (self.repo / 'bin').mkdir(parents=True)
        shutil.copy2(ROOT / 'bin/odlc', self.repo / 'bin/odlc')
        shutil.copy2(ROOT / 'install.sh', self.repo / 'install.sh')
        (self.repo / 'opptra/skills/session').mkdir(parents=True)
        (self.repo / 'opptra/skills/session/SKILL.md').write_text('test skill')
        self.home = self.base / 'home'
        self.commands = self.home / '.local/bin'
        self.commands.mkdir(parents=True)
        mocks = self.base / 'mocks'
        mocks.mkdir()
        (mocks / 'git').write_text('#!/bin/sh\nexit 0\n')
        (mocks / 'git').chmod(0o755)
        (self.home / '.cache/opptra/sdlc-resources.git').mkdir(parents=True)
        self.env = dict(os.environ, HOME=str(self.home), PATH=f'{mocks}:/usr/bin:/bin')

    def install(self):
        subprocess.run(['bash', str(self.repo / 'install.sh')], env=self.env,
                       check=True, capture_output=True, text=True)

    def test_installs_odlc_and_removes_old_owned_link_idempotently(self):
        # Also migrate installations pointing at another clone.
        old = self.base / 'old-clone/bin/opptra'
        old.parent.mkdir(parents=True)
        old.write_text('#!/bin/bash\n# Unified Opptra SDLC CLI for both developers and AI agents.\n')
        (self.commands / 'opptra').symlink_to(old)
        self.install()
        self.install()
        self.assertFalse((self.commands / 'opptra').is_symlink())
        result = subprocess.run([str(self.commands / 'odlc'), '--help'], env=self.env,
                                check=True, capture_output=True, text=True)
        self.assertIn('Usage: odlc ', result.stdout)
        self.assertEqual((self.commands / 'odlc').resolve(), self.repo / 'bin/odlc')

    def test_removes_dangling_old_link_from_same_checkout(self):
        (self.commands / 'opptra').symlink_to(self.repo / 'bin/opptra')
        self.install()
        self.assertFalse((self.commands / 'opptra').is_symlink())

    def test_preserves_unrelated_command_and_symlink(self):
        command = self.commands / 'opptra'
        command.write_text('unrelated command')
        self.install()
        self.assertEqual(command.read_text(), 'unrelated command')
        command.unlink()
        other = self.base / 'other-command'
        other.write_text('unrelated target')
        command.symlink_to(other)
        self.install()
        self.assertEqual(command.resolve(), other)

    def test_delegates_to_odlc_engine_and_preserves_arguments(self):
        engine = self.base / 'engine/scripts'
        engine.mkdir(parents=True)
        (engine / 'odlc.py').write_text('import sys\nprint(repr(sys.argv[1:]))\n')
        env = dict(self.env, OPPTRA_SDLC_PATH=str(engine.parent))
        result = subprocess.run(['bash', str(self.repo / 'bin/odlc'), 'next', 'app with spaces', '--json'],
                                env=env, check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "['next', 'app with spaces', '--json']")


if __name__ == '__main__':
    unittest.main()
