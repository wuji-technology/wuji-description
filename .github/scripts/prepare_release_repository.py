#!/usr/bin/env python3
"""Clone an existing or empty Bloom release repository on a fixed branch.

The script accepts an empty repository only when it has no remote branches.
For that case, it leaves the checkout on an unborn master branch so trusted
automation can create the first commit. Existing repositories must already
contain the requested branch.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import NamedTuple


class ReleaseRepositoryState(NamedTuple):
    """State of the prepared release-repository checkout."""

    empty: bool
    branch: str


def _run_git(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip() or str(error)
        raise ValueError(f"Git command failed: {detail}") from error


def _remote_branches(repository_url: str) -> tuple[str, ...]:
    result = _run_git("ls-remote", "--heads", repository_url)
    branches: list[str] = []
    for line in result.stdout.splitlines():
        _, reference = line.split(maxsplit=1)
        prefix = "refs/heads/"
        if not reference.startswith(prefix):
            raise ValueError(f"Unexpected remote reference: {reference}")
        branches.append(reference.removeprefix(prefix))
    return tuple(sorted(branches))


def prepare_release_repository(
    repository_url: str,
    destination: Path,
    branch: str = "master",
) -> ReleaseRepositoryState:
    """Prepare a release checkout and report whether the remote is empty."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError(f"Destination already exists: {destination}")

    branches = _remote_branches(repository_url)
    if branches and branch not in branches:
        raise ValueError(
            f"Release repository must be empty or contain branch {branch}; "
            f"found {list(branches)!r}"
        )

    if branches:
        _run_git(
            "clone",
            "--branch",
            branch,
            "--single-branch",
            repository_url,
            str(destination),
        )
        return ReleaseRepositoryState(False, branch)

    _run_git("clone", "--no-checkout", repository_url, str(destination))
    _run_git("symbolic-ref", "HEAD", f"refs/heads/{branch}", cwd=destination)
    return ReleaseRepositoryState(True, branch)


def main() -> int:
    """Run the release-repository checkout command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--branch", default="master")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    try:
        result = prepare_release_repository(
            args.repository,
            args.destination,
            args.branch,
        )
    except ValueError as error:
        parser.error(str(error))

    rendered_empty = str(result.empty).lower()
    print(f"release_repository_empty={rendered_empty}")
    if args.github_output is not None:
        with args.github_output.open("a") as output:
            output.write(f"release_repository_empty={rendered_empty}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
