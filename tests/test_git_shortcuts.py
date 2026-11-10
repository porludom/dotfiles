"""Exercise the Git shortcut against disposable local repositories."""

import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


class GitShortcutTests(unittest.TestCase):
    def test_gud_refuses_unmerged_branch_and_deletes_merged_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            remote, checkout = root / "remote.git", root / "checkout"

            def git(*args, cwd=root):
                return subprocess.check_output(
                    ["git", *args], cwd=cwd, text=True, stderr=subprocess.STDOUT
                )

            git("init", "--bare", "--initial-branch=main", str(remote))
            git("clone", str(remote), str(checkout))
            git("config", "user.name", "Fixture", cwd=checkout)
            git("config", "user.email", "fixture@example.test", cwd=checkout)
            (checkout / "file").write_text("base\n")
            git("add", "file", cwd=checkout)
            git("commit", "-m", "base", cwd=checkout)
            git("push", "-u", "origin", "main", cwd=checkout)
            git("switch", "-c", "feature", cwd=checkout)
            (checkout / "file").write_text("unmerged\n")
            git("commit", "-am", "unmerged", cwd=checkout)
            tip = git("rev-parse", "feature", cwd=checkout)
            script = '_exists() { return 1; }; source "$1"; gud'

            def gud():
                return subprocess.run(
                    ["zsh", "-f", "-c", script, "fixture", str(SOURCE / "home/.aliases.zsh")],
                    cwd=checkout,
                    check=False,
                    text=True,
                    capture_output=True,
                )

            result = gud()
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(git("rev-parse", "feature", cwd=checkout), tip)
            self.assertEqual(git("branch", "--show-current", cwd=checkout).strip(), "main")
            git("merge", "--ff-only", "feature", cwd=checkout)
            git("switch", "feature", cwd=checkout)
            result = gud()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(git("branch", "--list", "feature", cwd=checkout), "")
