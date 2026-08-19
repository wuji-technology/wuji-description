#!/usr/bin/env python3
"""Generate Bloom release-repository metadata from the public release contract.

The script creates the initial README from a trusted template and regenerates
one <ros_distro>.ignored file for every configured ROS distribution. It keeps
an existing README because Bloom prepends release history to that file.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from string import Template
from typing import Any

import yaml


VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROS_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration field {key!r} must be a string")
    return value.strip()


def _repository_url(value: str) -> str:
    return value.removesuffix(".git")


def _render_readme(
    config: dict[str, Any],
    template_path: Path,
    version: str,
    ros_distros: tuple[str, ...],
    published_packages: tuple[str, ...],
) -> str:
    try:
        template = Template(template_path.read_text())
    except OSError as error:
        raise ValueError(f"Cannot read README template {template_path}: {error}") from error

    values = {
        "repository_name": _required_string(config, "repository_name"),
        "ros_distributions": ", ".join(name.title() for name in ros_distros),
        "source_version": version,
        "source_repository": _repository_url(
            _required_string(config, "source_repository")
        ),
        "release_repository": _repository_url(
            _required_string(config, "release_repository")
        ),
        "published_packages": "\n".join(
            f"- `{name}`" for name in published_packages
        ),
    }
    try:
        return template.substitute(values)
    except (KeyError, ValueError) as error:
        raise ValueError(f"Invalid README template {template_path}: {error}") from error


def _release_inventory(
    config: dict[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    distro_items = config.get("ros_distros")
    if not isinstance(distro_items, list) or not distro_items:
        raise ValueError("ros_distros must be a non-empty list")

    ros_distros: set[str] = set()
    for index, item in enumerate(distro_items):
        if not isinstance(item, dict):
            raise ValueError(f"ros_distros[{index}] must be a mapping")
        name = item.get("name")
        if not isinstance(name, str) or not ROS_NAME_PATTERN.fullmatch(name):
            raise ValueError(f"ros_distros[{index}].name must be a lowercase ROS name")
        if name in ros_distros:
            raise ValueError(f"Duplicate ROS distribution: {name}")
        ros_distros.add(name)

    package_items = config.get("packages")
    if not isinstance(package_items, list) or not package_items:
        raise ValueError("packages must be a non-empty list")

    published: set[str] = set()
    ignored: set[str] = set()
    for index, item in enumerate(package_items):
        if not isinstance(item, dict):
            raise ValueError(f"packages[{index}] must be a mapping")
        name = item.get("name")
        publish = item.get("publish")
        if not isinstance(name, str) or not ROS_NAME_PATTERN.fullmatch(name):
            raise ValueError(f"packages[{index}].name must be a lowercase ROS name")
        if type(publish) is not bool:
            raise ValueError(f"packages[{index}].publish must be a boolean")
        target = published if publish else ignored
        if name in published or name in ignored:
            raise ValueError(f"Duplicate package: {name}")
        target.add(name)

    if not published:
        raise ValueError("At least one package must have publish: true")
    return tuple(sorted(ros_distros)), tuple(sorted(published)), tuple(sorted(ignored))


def _write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and path.read_text() == content:
        return False
    path.write_text(content)
    return True


def generate_release_repository(
    config_path: Path,
    source_root: Path,
    template_path: Path,
    release_root: Path,
    version: str,
) -> list[Path]:
    """Generate initial README and ROS distribution ignore files."""
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Invalid version {version!r}; expected numeric X.Y.Z")

    source_root = Path(source_root)
    if not source_root.is_dir():
        raise ValueError(f"Source root does not exist: {source_root}")

    try:
        config = yaml.safe_load(Path(config_path).read_text())
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"Invalid release configuration: {error}") from error
    if not isinstance(config, dict):
        raise ValueError("Release configuration must be a mapping")

    ros_distros, published, ignored = _release_inventory(config)
    release_root = Path(release_root)
    release_root.mkdir(parents=True, exist_ok=True)

    changed: list[Path] = []
    readme = release_root / "README.md"
    if not readme.exists():
        content = _render_readme(
            config,
            Path(template_path),
            version,
            ros_distros,
            published,
        )
        if _write_if_changed(readme, content):
            changed.append(readme)

    ignored_content = "".join(f"{name}\n" for name in ignored)
    for ros_distro in ros_distros:
        path = release_root / f"{ros_distro}.ignored"
        if _write_if_changed(path, ignored_content):
            changed.append(path)

    return sorted(changed)


def main() -> int:
    """Run the release-repository generator CLI."""
    parser = argparse.ArgumentParser(
        description="Generate Bloom release-repository metadata"
    )
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--release-root", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    try:
        changed = generate_release_repository(
            args.config,
            args.root,
            args.template,
            args.release_root,
            args.version,
        )
    except ValueError as error:
        parser.error(str(error))

    for path in changed:
        print(path.relative_to(args.release_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
