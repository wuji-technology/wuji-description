# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Restructured the repository into a multi-product layout. Hand body assets moved from the repository root into `hand/body/`; hand accessories consolidated under `hand/attachment/`.
- Moved the docking link (formerly `docking/`) to `hand/attachment/impact-resistant-attachment/`.
- Moved adapter STEP files, assembled PDF drawings, and installation notes from `step/adapter/` to `hand/attachment/step/`.
- Moved simplified structural STEP files from `step/simplified-structural/` to `hand/body/step/`.
- Renamed the ROS2 package from `wuji_hand_description` to `wuji_description`. Updated `package.xml`, `CMakeLists.txt`, `display.launch.py`, and all `package://` references in the `-ros.urdf` models.
- Normalized directory and file names to use hyphens instead of spaces, and standardized STEP file extensions to lowercase `.step`:
  - `impact-resistant attachment/` → `impact-resistant-attachment/`
  - `Unitree G1 attachment/` → `unitree-g1-attachment/`
  - `Unitree G1 docking adapter.stl` → `unitree-g1-docking-adapter.stl`
  - `glove attachment.stp` → `glove-attachment.step`
- `hand/body/CMakeLists.txt` now installs the sibling `hand/attachment/` directory under the package share so that `package://wuji_description/attachment/...` URLs resolve after `colcon build`.

### Added

- Added `hand/attachment/unitree-g1-attachment/unitree-g1-docking-adapter.stl` for mounting the Wuji Hand on a Unitree G1 humanoid.
- Added `glove/attachment/glove-attachment.step` as the initial Wuji Glove mounting interface asset.

### Fixed

- Bumped `hand/body/package.xml` `<version>` from `0.2.4` to `2026.04.27` to match the most recent CHANGELOG release.
- Updated `docking-ros.urdf` mesh path to `package://wuji_description/attachment/impact-resistant-attachment/meshes/hand_docking_link.STL` (the previous `package://wuji_hand_description/docking/meshes/...` path no longer existed after the restructure).
- Removed the now-empty `docking` entry from the `hand/body/CMakeLists.txt` install list.

## [2026.04.27] - 2026-04-27

### Added

- Added adapter STEP files, assembled PDF drawings, and installation instructions under `step/adapter/` for the direct adapter and the impact-resistant adapter.
- Added simplified structural STEP files for the left and right hand frames (with temporary fingertips) under `step/simplified-structural/`.

### Removed

- Removed the legacy top-level `step/left_hand.STEP` and `step/right_hand.STEP` files in favor of the new `step/adapter/` and `step/simplified-structural/` layout.
### Fixed

- Fixed thumb mesh vertices on both hands (`finger1_link1`, `finger1_link2`, `finger1_tip_link`); URDF, MJCF, and USD updated accordingly to match the new thumb geometry.

## [2026.04.16] - 2026-04-16

### Fixed

- Unified left/right hand joint <limit> bounds across all four URDF files using averaged calibrated values.

## [0.2.5] - 2026-04-10

### Added

- Added docking module assets including URDF, MJCF, STL mesh, and USD files.

### Fixed

- Replaced all URDF, MJCF, and mesh files with sysid-calibrated outputs, fixing left-right inconsistencies in joint axes, inertials, and kinematics.
- Corrected joint axis directions for consistent rotation conventions.
- Updated actuator parameters, joint limits, and inertial properties from sysid results.
- Regenerated ROS URDF variants to match calibrated versions.
- Removed spurious <limit> elements from fixed joints in right-hand URDFs.
- Fixed wrong ROS package path in docking-ros.urdf.

### Changed

- CMakeLists.txt now installs mjcf/ and usd/ directories for ROS consumers.
- README documents docking module preview usage.

## [0.2.4] - 2026-03-23

### Added

- Added USD assets for NVIDIA Isaac Sim with fused meshes, PBR materials, physics properties, and collision filter pairs.
- Added README guidance for loading the USD assets in Isaac Sim.
- Added an MIT license file for the public repository.

### Changed

- Standardized the MCP2 joint limits of the four non-thumb fingers to `-0.37` to `0.37` across the URDF, MJCF, and USD models.
- Refreshed the README structure and usage examples to match the current repository contents.

### Fixed

- Corrected repository metadata and package links for the current `wuji-hand-description` repository.
- Corrected package version metadata for the `0.2.4` release.

## [0.2.3] - 2026-03-19

### Fixed

- Standardized left and right hand joint limits using averaged calibrated values across the hand models.

## [0.2.2] - 2026-02-02

### Fixed

- Fixed mesh references in the URDF models so left and right hand assets load correctly in local tools.

## [0.2.1] - 2026-01-20

### Fixed

- Fixed the robot name in the left-hand models.
- Fixed inertia values.
- Fixed joint motion range limits.
- Fixed joint torque limits.
- Fixed self-collision groups.
- Fixed the RViz fixed frame for right hand visualization.

## [0.2.0] - 2026-01-19

### Changed

- Removed the version suffix from the robot name.
- Unified the left and right hand ROS2 visualization entry points behind a single launch interface with a `hand` selector.
- Streamlined the ROS2 package installation layout for visualization workflows.

### Fixed

- Fixed the RViz robot description topic handling so visualization works correctly inside a ROS2 namespace.

## [0.1.0] - 2025-11-27

### Added

- Added URDF models for Wuji Hand left and right hands.
- Added MJCF models for MuJoCo simulation.
- Added high-quality STL meshes for visualization and collision.
- Added ROS2 launch files for left and right hands.
- Added RViz configuration files for robot display.
- Added ROS2 package build configuration.

[Unreleased]: https://github.com/wuji-technology/wuji-hand-description/compare/v2026.04.27...HEAD
[2026.04.27]: https://github.com/wuji-technology/wuji-hand-description/compare/v2026.04.16...v2026.04.27
[2026.04.16]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.5...v2026.04.16
[0.2.5]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/wuji-technology/wuji-hand-description/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/wuji-technology/wuji-hand-description/releases/tag/v0.1.0
