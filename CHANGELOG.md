# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- README rewritten in English with standardized format (badges, TOC, directory table, numbered usage sections)
- Fixed incorrect launch file references (`display.launch.py` with `robot:=` arg)
- Fixed license reference from Apache-2.0 to MIT (matching LICENSE file)
- Workflow `auto-release-on-pr.yml` renamed to `create_release_tag.yaml`
  - Simplified trigger: only checks `release/v*` branch (no label required)
  - Version extraction from branch name instead of PR title

## [1.0.0] - 2026-02-11

Initial public release.

### Added

- URDF models for WUJI Hand (left/right) with calibrated dynamics
- MJCF models for MuJoCo simulation
- MJX models optimized for JAX-based simulation (Brax)
- ROS2 package structure with launch files and RViz config
- Sparse checkout support for downloading individual models
- GitHub Actions CI/CD workflows
  - `sync_public.yaml`: Tag push syncs to public repo
  - `ci_test.yaml`: MuJoCo/MJX/Isaac Sim validation tests
  - `auto-release.yml`: Automatic GitHub Release creation

### Notes

- USD models for Isaac Sim are planned for future releases
- Model parameters are based on CAD data and real-world measurements

[Unreleased]: https://github.com/wuji-technology/wuji-description/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/wuji-technology/wuji-description/releases/tag/v1.0.0
