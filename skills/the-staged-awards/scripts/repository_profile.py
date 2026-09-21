#!/usr/bin/env python3
"""Measure a Git repository for size-aware Staged Awards inspection."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


EXCLUDED_DIRECTORIES = {
    ".git",
    ".next",
    ".nuxt",
    "bin",
    "build",
    "coverage",
    "dist",
    "generated",
    "node_modules",
    "obj",
    "out",
    "target",
    "vendor",
}

EXCLUDED_FILENAMES = {
    "Cargo.lock",
    "Gemfile.lock",
    "composer.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "yarn.lock",
}

SENSITIVE_FILENAMES = {
    "credentials.json",
    "id_dsa",
    "id_ed25519",
    "id_rsa",
    "secrets.json",
}

EXCLUDED_SUFFIXES = (
    ".jks",
    ".key",
    ".keystore",
    ".map",
    ".min.css",
    ".min.js",
    ".p12",
    ".pem",
    ".pfx",
)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def repository_root(path: Path) -> Path:
    result = git(path, "rev-parse", "--show-toplevel", check=False)
    if result.returncode != 0:
        raise ValueError(f"not a Git repository: {path}")
    return Path(os.fsdecode(result.stdout).strip()).resolve()


def is_structurally_excluded(relative_path: Path) -> bool:
    name = relative_path.name
    normalized_name = name.casefold()
    environment_file = (
        normalized_name == ".env"
        or normalized_name.startswith(".env.")
        or normalized_name.endswith(".env")
        or ".env." in normalized_name
    )
    return (
        any(part in EXCLUDED_DIRECTORIES for part in relative_path.parts[:-1])
        or name in EXCLUDED_FILENAMES
        or normalized_name in SENSITIVE_FILENAMES
        or name.endswith(EXCLUDED_SUFFIXES)
        or environment_file
    )


def looks_binary(path: Path) -> bool:
    with path.open("rb") as stream:
        return b"\0" in stream.read(8192)


def count_lines(path: Path) -> int:
    with path.open("rb") as stream:
        return sum(1 for _ in stream)


def classify_repository(file_count: int, line_count: int) -> str:
    if file_count <= 100 and line_count <= 20_000:
        return "small"
    if file_count <= 500 and line_count <= 100_000:
        return "medium"
    return "large"


def history_revisions(root: Path) -> list[str]:
    revisions = ["--all"]
    if git(root, "rev-parse", "--verify", "HEAD", check=False).returncode == 0:
        revisions.append("HEAD")
    return revisions


def history_profile(root: Path) -> tuple[int, str, str]:
    revisions = history_revisions(root)
    hashes = git(root, "rev-list", *revisions, check=False)
    commit_ids = {line for line in hashes.stdout.splitlines() if line}
    if not commit_ids:
        return 0, "N/A", "N/A"

    date_output = git(root, "log", *revisions, "--format=%cI").stdout
    dated_commits: list[tuple[datetime, str]] = []
    for raw_date in date_output.splitlines():
        date_text = os.fsdecode(raw_date).strip()
        if date_text:
            dated_commits.append((datetime.fromisoformat(date_text), date_text[:10]))

    if not dated_commits:
        return len(commit_ids), "N/A", "N/A"

    dated_commits.sort(key=lambda item: item[0])
    return len(commit_ids), dated_commits[0][1], dated_commits[-1][1]


def author_profile(root: Path, commit_count: int) -> str:
    if commit_count == 0:
        return "Repository contributors"

    author_output = git(
        root, "log", *history_revisions(root), "--format=%an%x00"
    ).stdout
    author_counts = Counter(
        os.fsdecode(name).strip()
        for name in author_output.split(b"\0")
        if name.strip()
    )
    if not author_counts:
        return "Repository contributors"
    ranked_authors = sorted(
        author_counts, key=lambda name: (-author_counts[name], name.casefold(), name)
    )
    return ", ".join(ranked_authors[:3])


def repository_link(root: Path) -> str:
    remote = git(root, "config", "--get", "remote.origin.url", check=False)
    if remote.returncode != 0:
        return "Repository link unavailable"

    remote_url = os.fsdecode(remote.stdout).strip()
    try:
        parsed = urlsplit(remote_url)
        hostname = parsed.hostname
    except ValueError:
        return "Repository link unavailable"
    if parsed.scheme in {"http", "https", "ssh", "git"} and hostname:
        scheme = parsed.scheme if parsed.scheme in {"http", "https"} else "https"
        host = (
            parsed.netloc.rsplit("@", 1)[-1]
            if scheme in {"http", "https"}
            else hostname
        )
        path = parsed.path
    else:
        scp_remote = re.fullmatch(r"[^@/:]+@([^@/:]+):(.+)", remote_url)
        if not scp_remote:
            return "Repository link unavailable"
        scheme = "https"
        host, path = scp_remote.groups()

    path = path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if not path or path == "/":
        return "Repository link unavailable"
    return urlunsplit((scheme, host, "/" + path.lstrip("/"), "", ""))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report Git history and eligible text size for a repository."
    )
    parser.add_argument("repository", nargs="?", default=".")
    args = parser.parse_args()

    try:
        root = repository_root(Path(args.repository).resolve())
    except ValueError as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    tracked_output = git(root, "ls-files", "-z").stdout
    tracked_paths = [
        Path(os.fsdecode(item)) for item in tracked_output.split(b"\0") if item
    ]

    eligible_file_count = 0
    eligible_line_count = 0
    excluded_file_count = 0

    for relative_path in tracked_paths:
        absolute_path = root / relative_path
        if (
            is_structurally_excluded(relative_path)
            or absolute_path.is_symlink()
            or not absolute_path.is_file()
        ):
            excluded_file_count += 1
            continue
        try:
            if looks_binary(absolute_path):
                excluded_file_count += 1
                continue
            eligible_line_count += count_lines(absolute_path)
            eligible_file_count += 1
        except OSError:
            excluded_file_count += 1

    commit_count, first_commit_date, latest_commit_date = history_profile(root)
    branch_result = git(root, "branch", "--show-current", check=False)
    branch = os.fsdecode(branch_result.stdout).strip() or "detached HEAD"
    shallow_result = git(root, "rev-parse", "--is-shallow-repository", check=False)
    is_shallow = os.fsdecode(shallow_result.stdout).strip() == "true"

    print(f"repository_root={root}")
    print(f"repository_link={repository_link(root)}")
    print(f"branch={branch}")
    print(f"repository_size={classify_repository(eligible_file_count, eligible_line_count)}")
    print(f"tracked_file_count={len(tracked_paths)}")
    print(f"eligible_file_count={eligible_file_count}")
    print(f"eligible_line_count={eligible_line_count}")
    print(f"excluded_file_count={excluded_file_count}")
    print(f"commit_count={commit_count}")
    print(f"author={author_profile(root, commit_count)}")
    print(f"first_commit_date={first_commit_date}")
    print(f"latest_commit_date={latest_commit_date}")
    history_scope = "HEAD and all locally available refs"
    if is_shallow:
        history_scope += " (incomplete shallow history)"
    print(f"history_scope={history_scope}")
    print(f"shallow_repository={'yes' if is_shallow else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
