#!/usr/bin/env python3
"""Initialize missing Bloom tracks through the pinned git-bloom-config CLI.

The release-preparation workflow runs this trusted wrapper in a clean clone of
the Bloom release repository. Existing tracks are never edited. Configuration
drift is handled later by the read-only Bloom preflight.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import pexpect
import yaml


ROS_DISTRO_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
# Match only the final Bloom input line. Unrelated logs may also end in ": ".
BLOOM_PROMPT_PATTERN = re.compile(r"\r\n  [^\r\n]*\][^\r\n]*: ")


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration field {key!r} must be a string")
    return value.strip()


def _load_config(config_path: Path) -> tuple[str, str, str, tuple[str, ...]]:
    try:
        document = yaml.safe_load(config_path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"Invalid release configuration: {error}") from error
    if not isinstance(document, dict):
        raise ValueError("Release configuration must be a mapping")

    repository_name = _required_string(document, "repository_name")
    source_repository = _required_string(document, "source_repository")
    release_tag = _required_string(document, "release_tag")
    raw_distros = document.get("ros_distros")
    if not isinstance(raw_distros, list) or not raw_distros:
        raise ValueError("ros_distros must be a non-empty list")

    ros_distros: set[str] = set()
    for index, raw_distro in enumerate(raw_distros):
        if not isinstance(raw_distro, dict):
            raise ValueError(f"ros_distros[{index}] must be a mapping")
        name = raw_distro.get("name")
        if not isinstance(name, str) or not ROS_DISTRO_PATTERN.fullmatch(name):
            raise ValueError(
                f"ros_distros[{index}].name must be a lowercase ROS name"
            )
        if name in ros_distros:
            raise ValueError(f"Duplicate ROS distribution: {name}")
        ros_distros.add(name)
    return (
        repository_name,
        source_repository,
        release_tag,
        tuple(sorted(ros_distros)),
    )


def _existing_tracks(release_root: Path) -> set[str]:
    tracks_path = release_root / "tracks.yaml"
    if not tracks_path.exists():
        return set()
    try:
        document = yaml.safe_load(tracks_path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"Invalid Bloom tracks file: {error}") from error
    if not isinstance(document, dict) or not isinstance(document.get("tracks"), dict):
        raise ValueError("tracks.yaml must contain a tracks mapping")
    return set(document["tracks"])


def initialize_missing_tracks(
    config_path: Path,
    release_root: Path,
) -> tuple[str, ...]:
    """Create every configured-but-missing track with git-bloom-config."""
    release_root = release_root.resolve()
    if not (release_root / ".git").exists():
        raise ValueError(f"Release root is not a Git repository: {release_root}")
    if shutil.which("git-bloom-config") is None:
        raise ValueError("git-bloom-config is not installed")

    repository_name, source_repository, release_tag, ros_distros = _load_config(
        config_path
    )
    existing = _existing_tracks(release_root)
    initialized: list[str] = []
    for ros_distro in ros_distros:
        if ros_distro in existing:
            continue
        responses = (
            repository_name,
            source_repository,
            "git",
            ":{auto}",
            release_tag,
            "main",
            ros_distro,
            "None",
            "None",
        )
        child = pexpect.spawn(
            "git-bloom-config",
            ["new", ros_distro],
            cwd=str(release_root),
            encoding="utf-8",
            timeout=30,
        )
        try:
            for response in responses:
                child.expect(BLOOM_PROMPT_PATTERN)
                child.sendline(response)
            child.expect(pexpect.EOF)
            child.close()
        except pexpect.ExceptionPexpect as error:
            child.close(force=True)
            raise ValueError(
                "git-bloom-config interaction failed for ROS distribution "
                f"{ros_distro}: {error}"
            ) from error
        if child.exitstatus != 0:
            print(child.before, file=sys.stderr)
            raise ValueError(
                f"git-bloom-config failed for ROS distribution {ros_distro}"
            )
        initialized.append(ros_distro)
        existing.add(ros_distro)
    return tuple(initialized)


def main() -> int:
    """Run Bloom-native initialization for all configured ROS distributions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--release-root", type=Path, required=True)
    args = parser.parse_args()

    try:
        initialized = initialize_missing_tracks(args.config, args.release_root)
    except ValueError as error:
        parser.error(str(error))
    if initialized:
        for ros_distro in initialized:
            print(f"Initialized Bloom track: {ros_distro}")
    else:
        print("All configured Bloom tracks are already initialized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
