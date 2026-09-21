"""Focused checks for the LinkedIn ceremony author value."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PROFILE = (
    Path(__file__).resolve().parents[1]
    / "skills/the-staged-awards/scripts/repository_profile.py"
)


class AuthorProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.repo = Path(self.temp_dir.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def commit(self, name, email, index):
        (self.repo / "entry.txt").write_text(f"commit {index}\n")
        subprocess.run(["git", "add", "entry.txt"], cwd=self.repo, check=True)
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": name,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_COMMITTER_NAME": name,
            "GIT_COMMITTER_EMAIL": email,
        })
        subprocess.run(
            ["git", "commit", "-q", "-m", f"commit {index}"],
            cwd=self.repo,
            env=env,
            check=True,
        )

    def profile_author(self):
        result = subprocess.run(
            ["python3", str(PROFILE), str(self.repo)],
            capture_output=True,
            text=True,
            check=True,
        )
        return next(
            line.removeprefix("author=")
            for line in result.stdout.splitlines()
            if line.startswith("author=")
        )

    def test_no_commits_uses_contributors_fallback(self):
        self.assertEqual(self.profile_author(), "Repository contributors")

    def test_single_name_omits_email_even_with_multiple_addresses(self):
        self.commit("Ada Lovelace", "ada@example.com", 1)
        self.commit("Ada Lovelace", "ada@work.example", 2)
        self.assertEqual(self.profile_author(), "Ada Lovelace")

    def test_multiple_names_lists_three_by_commit_count_then_name(self):
        authors = ["Zoe", "Ben", "Ada", "Zoe", "Ben", "Ada", "Mia", "Zoe"]
        for index, name in enumerate(authors, start=1):
            self.commit(name, f"{name.lower()}@example.com", index)
        self.assertEqual(self.profile_author(), "Zoe, Ada, Ben")


if __name__ == "__main__":
    unittest.main()
