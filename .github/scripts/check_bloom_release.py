#!/usr/bin/env python3
"""Gate a public source tag before Bloom changes remote release state.

The public workflow runs this file from the trusted default branch. It checks
the synchronized release configuration, source package versions, per-distro
ignored packages, Bloom track fields, and retry phase. Matrix print modes also
resolve the configured Ubuntu container. The script does not initialize tracks
or run Bloom.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, NamedTuple

import yaml


VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROS_DISTRO_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
CONTAINER_IMAGE_PATTERN = re.compile(r"^ubuntu:[a-z0-9][a-z0-9._-]*$")
EXPECTED_REPOSITORY_NAME = "wuji_description"
EXPECTED_SOURCE_REPOSITORY = (
    "https://github.com/wuji-technology/wuji-description.git"
)
EXPECTED_RELEASE_REPOSITORY = (
    "https://github.com/wuji-technology/wuji-description-release.git"
)
EXPECTED_RELEASE_REPOSITORY_URLS = {
    EXPECTED_RELEASE_REPOSITORY,
    "git@github.com:wuji-technology/wuji-description-release.git",
}
EXPECTED_ROSDISTRO_FORK_OWNER = "wuji-technology"
# Treat Bloom's generated command list as part of the trusted track contract.
# A Bloom upgrade must update this tuple and its regression tests together.
# This tuple matches bloom 0.14.3 ACTION_LIST_HISTORY[-1].
EXPECTED_BLOOM_ACTIONS = (
    "bloom-export-upstream :{vcs_local_uri} :{vcs_type} --tag "
    ":{release_tag} --display-uri :{vcs_uri} --name :{name} "
    "--output-dir :{archive_dir_path}",
    "git-bloom-import-upstream :{archive_path} :{patches} "
    "--release-version :{version} --replace",
    "git-bloom-generate -y rosrelease :{ros_distro} --source upstream "
    "-i :{release_inc}",
    "git-bloom-generate -y rosdebian --prefix release/:{ros_distro} "
    ":{ros_distro} -i :{release_inc} --os-name ubuntu",
    "git-bloom-generate -y rosdebian --prefix release/:{ros_distro} "
    ":{ros_distro} -i :{release_inc} --os-name debian --os-not-required",
    "git-bloom-generate -y rosrpm --prefix release/:{ros_distro} "
    ":{ros_distro} -i :{release_inc} --os-name fedora",
    "git-bloom-generate -y rosrpm --prefix release/:{ros_distro} "
    ":{ros_distro} -i :{release_inc} --os-name rhel",
    "git-bloom-generate -y rosdynrpm --prefix release/:{ros_distro} "
    ":{ros_distro} -i :{release_inc} --require-os fedora rhel",
)


class RosDistro(NamedTuple):
    name: str
    container_image: str


class BloomRelease(NamedTuple):
    repository_name: str
    version: str
    published_packages: tuple[str, ...]


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping")
    return value


def _string(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _load_config(config_path: Path | str) -> dict[str, Any]:
    try:
        document = yaml.safe_load(Path(config_path).read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(
            f"invalid release configuration: {config_path}"
        ) from error
    return _mapping(document, "config")


def _ros_distros(config: dict[str, Any]) -> tuple[RosDistro, ...]:
    values = config.get("ros_distros")
    if not isinstance(values, list) or not values:
        raise ValueError("ros_distros must be a non-empty list")

    result: list[RosDistro] = []
    names: set[str] = set()
    for index, value in enumerate(values):
        item = _mapping(value, f"ros_distros[{index}]")
        name = item.get("name")
        container_image = item.get("container_image")
        if not isinstance(name, str) or not ROS_DISTRO_PATTERN.fullmatch(name):
            raise ValueError(
                f"ROS distribution entry {index} name must be a lowercase ROS name"
            )
        if (
            not isinstance(container_image, str)
            or not CONTAINER_IMAGE_PATTERN.fullmatch(container_image)
        ):
            raise ValueError(
                f"ROS distribution {name} container_image must be an official "
                "ubuntu:<tag> image"
            )
        if name in names:
            raise ValueError(f"duplicate ROS distribution: {name}")
        names.add(name)
        result.append(RosDistro(name, container_image))
    return tuple(result)


def _safe_package_path(root: Path, raw_path: Any) -> tuple[str, Path]:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("package path must be a non-empty string")
    relative = Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"package path escapes source root: {raw_path}")
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"package path escapes source root: {raw_path}") from error
    return relative.as_posix(), resolved


def _manifest_fields(manifest_path: Path) -> tuple[str, str]:
    try:
        package = ET.parse(manifest_path).getroot()
    except (OSError, ET.ParseError) as error:
        raise ValueError(f"invalid package manifest: {manifest_path}") from error
    names = package.findall("name")
    versions = package.findall("version")
    if len(names) != 1 or not names[0].text:
        raise ValueError(f"package manifest must contain one name: {manifest_path}")
    if len(versions) != 1 or not versions[0].text:
        raise ValueError(f"package manifest must contain one version: {manifest_path}")
    return names[0].text.strip(), versions[0].text.strip()


def _ignored_packages(path: Path) -> set[str]:
    try:
        lines = path.read_text().splitlines()
    except OSError as error:
        raise ValueError(f"missing Bloom ignored file: {path}") from error
    return {
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    }


def _check_track(
    release_root: Path,
    rosdistro: str,
    release_tag: str,
    version: str,
    *,
    pull_request_only: bool,
    prepare_only: bool,
) -> None:
    tracks_path = release_root / "tracks.yaml"
    try:
        tracks_document = yaml.safe_load(tracks_path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(
            f"Bloom track {rosdistro!r} is not initialized"
        ) from error
    tracks_document = _mapping(tracks_document, "tracks.yaml")
    release_repo_url = tracks_document.get("release_repo_url")
    if (
        release_repo_url is not None
        and release_repo_url not in EXPECTED_RELEASE_REPOSITORY_URLS
    ):
        raise ValueError(
            "tracks.yaml release_repo_url must point to the Wuji release repository"
        )
    tracks = _mapping(tracks_document.get("tracks"), "tracks")
    track = tracks.get(rosdistro)
    if not isinstance(track, dict) or track.get("ros_distro") != rosdistro:
        raise ValueError(f"Bloom track {rosdistro!r} is not initialized")

    # Validate every field that controls where Bloom reads source, writes
    # release history, and generates packaging branches.
    expected_fields = {
        "name": EXPECTED_REPOSITORY_NAME,
        "vcs_type": "git",
        "vcs_uri": EXPECTED_SOURCE_REPOSITORY,
        "version": ":{auto}",
        "release_tag": release_tag,
        "devel_branch": "main",
        "ros_distro": rosdistro,
        "patches": None,
        "release_repo_url": None,
        "actions": list(EXPECTED_BLOOM_ACTIONS),
    }
    for field, expected in expected_fields.items():
        actual = track.get(field)
        if actual != expected:
            raise ValueError(
                f"track field {field} must be {expected!r}, got {actual!r}"
            )

    last_version = track.get("last_version")
    last_release = track.get("last_release")
    release_inc = track.get("release_inc")
    if last_version is None and last_release is None:
        if release_inc != 0:
            raise ValueError(
                "an initialized unreleased track must have integer release_inc 0"
            )
        if pull_request_only:
            raise ValueError(
                "pull-request-only requires an existing Bloom release"
            )
        return
    if not isinstance(release_inc, str) or not re.fullmatch(r"[0-9]+", release_inc):
        raise ValueError("track field release_inc must contain only digits")
    if not isinstance(last_version, str) or not VERSION_PATTERN.fullmatch(last_version):
        raise ValueError(
            "track field last_version must contain the initialized release version"
        )
    if last_release != f"v{last_version}":
        raise ValueError(
            f"track field last_release must be 'v{last_version}', "
            f"got {last_release!r}"
        )
    version_key = tuple(int(part) for part in version.split("."))
    last_version_key = tuple(int(part) for part in last_version.split("."))
    if prepare_only:
        if version_key < last_version_key:
            raise ValueError(
                f"release version {version} must not be older than last_version "
                f"{last_version}"
            )
        return
    # Retry mode is phase-aware. It may recreate only the rosdistro PR after
    # the target version already exists in the release repository.
    if pull_request_only:
        if last_version != version:
            raise ValueError(
                "pull-request-only requires release repository last_version "
                f"{version}, got {last_version!r}"
            )
        return

    if version_key == last_version_key:
        raise ValueError(
            f"release version {version} already exists; use pull-request-only "
            "to retry only the rosdistro pull request"
        )
    if version_key < last_version_key:
        raise ValueError(
            f"release version {version} must be newer than last_version {last_version}"
        )


def check_bloom_release(
    config_path: Path | str,
    source_root: Path | str,
    release_root: Path | str,
    tag: str,
    ros_distro: str,
    *,
    pull_request_only: bool = False,
    prepare_only: bool = False,
) -> BloomRelease:
    """Validate source manifests, the release tag, ignore set, and Bloom track."""

    source = Path(source_root).resolve()
    release = Path(release_root).resolve()
    config = _load_config(config_path)
    if prepare_only and pull_request_only:
        raise ValueError(
            "prepare-only cannot be combined with pull-request-only"
        )

    ros_distros = _ros_distros(config)
    ros_distro_names = tuple(distro.name for distro in ros_distros)
    if ros_distro not in ros_distro_names:
        raise ValueError(
            f"ROS distribution {ros_distro!r} is not configured; "
            f"expected one of {list(ros_distro_names)!r}"
        )
    rosdistro = ros_distro
    repository_name = _string(config, "repository_name")
    if repository_name != EXPECTED_REPOSITORY_NAME:
        raise ValueError(
            f"repository_name must be {EXPECTED_REPOSITORY_NAME}, "
            f"got {repository_name!r}"
        )
    source_repository = _string(config, "source_repository")
    if source_repository != EXPECTED_SOURCE_REPOSITORY:
        raise ValueError(
            f"source_repository must be {EXPECTED_SOURCE_REPOSITORY}, "
            f"got {source_repository!r}"
        )
    release_repository = _string(config, "release_repository")
    if release_repository != EXPECTED_RELEASE_REPOSITORY:
        raise ValueError(
            f"release_repository must be {EXPECTED_RELEASE_REPOSITORY}, "
            f"got {release_repository!r}"
        )
    rosdistro_fork_owner = _string(config, "rosdistro_fork_owner")
    if rosdistro_fork_owner != EXPECTED_ROSDISTRO_FORK_OWNER:
        raise ValueError(
            "rosdistro_fork_owner must be "
            f"{EXPECTED_ROSDISTRO_FORK_OWNER}, got {rosdistro_fork_owner!r}"
        )
    release_tag = _string(config, "release_tag")
    if release_tag != "v:{version}":
        raise ValueError("release_tag must be v:{version}")

    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
        raise ValueError(f"{tag!r} does not match release tag vX.Y.Z")
    version = tag[1:]
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"invalid release version: {version}")

    raw_packages = config.get("packages")
    if not isinstance(raw_packages, list) or not raw_packages:
        raise ValueError("packages must be a non-empty list")

    configured_paths: set[str] = set()
    configured_names: set[str] = set()
    published: list[str] = []
    excluded: set[str] = set()

    for index, raw_package in enumerate(raw_packages):
        package = _mapping(raw_package, f"packages[{index}]")
        name = _string(package, "name")
        relative, package_path = _safe_package_path(source, package.get("path"))
        publish = package.get("publish")
        if not isinstance(publish, bool):
            raise ValueError(f"publish must be a boolean for package {name}")
        if name in configured_names or relative in configured_paths:
            raise ValueError(f"duplicate package entry: {name}")
        configured_names.add(name)
        configured_paths.add(relative)

        manifest_name, manifest_version = _manifest_fields(package_path / "package.xml")
        if manifest_name != name:
            raise ValueError(
                f"manifest name {manifest_name!r} does not match configured name {name!r}"
            )
        if publish:
            if manifest_version != version:
                raise ValueError(
                    f"{name} version {manifest_version} does not match "
                    f"release version {version}"
                )
            published.append(name)
        else:
            excluded.add(name)

    discovered_paths = {
        path.parent.relative_to(source).as_posix()
        for path in source.rglob("package.xml")
    }
    if discovered_paths != configured_paths:
        raise ValueError(
            "package manifest set does not match configuration: "
            f"configured={sorted(configured_paths)}, discovered={sorted(discovered_paths)}"
        )
    if not published:
        raise ValueError("release configuration contains no published packages")

    ignored = _ignored_packages(release / f"{rosdistro}.ignored")
    if ignored != excluded:
        raise ValueError(
            "ignored package set does not match configuration: "
            f"expected={sorted(excluded)}, actual={sorted(ignored)}"
        )

    _check_track(
        release,
        rosdistro,
        release_tag,
        version,
        pull_request_only=pull_request_only,
        prepare_only=prepare_only,
    )
    return BloomRelease(repository_name, version, tuple(sorted(published)))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--release-root", type=Path)
    parser.add_argument("--tag")
    parser.add_argument("--ros-distro")
    parser.add_argument("--pull-request-only", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--print-repository", action="store_true")
    parser.add_argument("--print-ros-distros", action="store_true")
    parser.add_argument("--print-ros-distro-matrix", action="store_true")
    parser.add_argument("--print-rosdistro-fork-owner", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        if (
            args.print_ros_distros
            or args.print_ros_distro_matrix
            or args.print_rosdistro_fork_owner
        ):
            config = _load_config(args.config)
            if args.print_rosdistro_fork_owner:
                owner = _string(config, "rosdistro_fork_owner")
                if owner != EXPECTED_ROSDISTRO_FORK_OWNER:
                    raise ValueError(
                        "rosdistro_fork_owner must be "
                        f"{EXPECTED_ROSDISTRO_FORK_OWNER}, got {owner!r}"
                    )
                print(owner)
                return 0
            ros_distros = _ros_distros(config)
            if args.print_ros_distro_matrix:
                print(
                    json.dumps(
                        [
                            {
                                "ros_distro": distro.name,
                                "container_image": distro.container_image,
                            }
                            for distro in ros_distros
                        ]
                    )
                )
            else:
                for ros_distro in ros_distros:
                    print(ros_distro.name)
            return 0
        missing = [
            flag
            for flag, value in (
                ("--root", args.root),
                ("--release-root", args.release_root),
                ("--tag", args.tag),
                ("--ros-distro", args.ros_distro),
            )
            if value is None
        ]
        if missing:
            raise ValueError(f"required arguments missing: {', '.join(missing)}")
        result = check_bloom_release(
            args.config,
            args.root,
            args.release_root,
            args.tag,
            args.ros_distro,
            pull_request_only=args.pull_request_only,
            prepare_only=args.prepare_only,
        )
    except ValueError as error:
        print(f"Bloom release preflight failed: {error}", file=sys.stderr)
        return 1
    if args.print_repository:
        print(result.repository_name)
    else:
        packages = ", ".join(result.published_packages)
        print(
            f"Bloom release preflight passed for {result.repository_name} "
            f"{result.version}: {packages}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
