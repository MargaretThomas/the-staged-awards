"""Checks for browser links derived from Git origin remotes."""

import subprocess
import tempfile
import unittest
from pathlib import Path


PROFILE = (
    Path(__file__).resolve().parents[1]
    / "skills/the-staged-awards/scripts/repository_profile.py"
)


class RepositoryLinkTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.repo = Path(self.temp_dir.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def profile_link(self):
        result = subprocess.run(
            ["python3", str(PROFILE), str(self.repo)],
            capture_output=True,
            text=True,
            check=True,
        )
        return next(
            line.removeprefix("repository_link=")
            for line in result.stdout.splitlines()
            if line.startswith("repository_link=")
        )

    def test_no_remote_uses_fallback(self):
        self.assertEqual(self.profile_link(), "Repository link unavailable")

    def test_hosted_remotes_become_browser_links(self):
        cases = {
            "https://github.com/example/repo.git": "https://github.com/example/repo",
            "git@github.com:example/repo.git": "https://github.com/example/repo",
            "ssh://git@gitlab.com/example/repo.git": "https://gitlab.com/example/repo",
            "https://user:secret@gitlab.example:8443/team/repo.git": (
                "https://gitlab.example:8443/team/repo"
            ),
        }
        for remote, expected in cases.items():
            with self.subTest(remote=remote):
                subprocess.run(
                    ["git", "remote", "remove", "origin"],
                    cwd=self.repo,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "remote", "add", "origin", remote],
                    cwd=self.repo,
                    check=True,
                )
                self.assertEqual(self.profile_link(), expected)

    def test_local_remote_uses_fallback(self):
        subprocess.run(
            ["git", "remote", "add", "origin", "../another-repo.git"],
            cwd=self.repo,
            check=True,
        )
        self.assertEqual(self.profile_link(), "Repository link unavailable")


if __name__ == "__main__":
    unittest.main()
