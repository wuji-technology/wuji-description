# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2026.6.27]

### Added

- Added the Wuji Hand 2 (Beta) model under `hand2_beta/body/`, replacing the previous `hand2/body/` directory. Each hand has 20 anatomically named revolute joints rooted at a dedicated base link, and ships in URDF, MuJoCo MJCF, Isaac Sim USD, STL, and STEP formats.

### Changed

- Normalized Isaac Sim USD config codenames for consistent naming.
- Switched Wuji Hand 2 USD configurations to relative paths so they load on any machine.

### Removed

- Removed the previous `hand2/body/` Wuji Hand 2 directory. Its assets now live under `hand2_beta/body/`.

### Fixed

- Fixed self-collision in the hand USD models for Isaac Sim.

## [2026.6.12]

### Added

- Added structural STEP assemblies of the left and right Wuji Hand 2 at `hand2/body/step/Wuji-Hand2-Beta1-{left,right}.step` (Beta1 revision).
- Added the Wuji Hand 2 adapter mount at `hand2/body/step/Wuji-Hand2-Adapter-Mount-Beta1.step`, a Beta1 STEP source file for mounting the Wuji Hand 2 on a robotic arm flange.

## [2026.6.11]

### Added

- Added MuJoCo MJCF models for the Wuji Hand 2 at `hand2/body/mjcf/{left,right}.xml`, using the RK4 integrator with a 0.002 s timestep, the Newton solver, and per-joint armature and actuator force ranges.
- Added Isaac Sim USD assets for the Wuji Hand 2 at `hand2/body/usd/{left,right}/`, each shipping the `wujihand.usd` entry point with base/physics/robot/sensor sublayers under `configuration/`, position-drive joint gains, and the logo texture under `textures/`.

## [2026.6.10]

### Added

- Added the Wuji Hand soft-pad variant at `hand/body-with-soft/`, a hand body model with a soft pad fixed to the thumb (`finger1_link2_softbody`). Ships URDF models at `hand/body-with-soft/urdf/{left,right}.urdf` (relative mesh paths) and `{left,right}-ros.urdf` (`package://` paths), MuJoCo MJCF models at `hand/body-with-soft/mjcf/{left,right}.xml`, Isaac Sim USD assets at `hand/body-with-soft/usd/{left,right}/`, STL meshes at `hand/body-with-soft/meshes/{left,right}/`, and actuator parameters at `hand/body-with-soft/params.csv`.
- Added simplified-collision variants of the soft-pad hand at `hand/body-with-soft/urdf/{left,right}_simplified.urdf`, `hand/body-with-soft/mjcf/{left,right}_simplified.xml`, and `hand/body-with-soft/usd/{left,right}_simplified/`. They replace the collision geometry of each finger's `link4` and the thumb soft pad with decimated meshes for faster contact simulation; visual geometry is unchanged.
- Added the Wuji Hand 2 model under `hand2/body/`: left and right URDF models at `hand2/body/urdf/{left,right}.urdf` (relative mesh paths) and `{left,right}-ros.urdf` (`package://` paths), each with 20 revolute joints using anatomical naming (`thumb`, `index_finger`, `middle_finger`, `ring_finger`, `pinky` with `cmc`/`mcp` flexion and abduction plus `pip`/`dip` or `mcp`/`ip` joints), and STL meshes at `hand2/body/meshes/{left,right}/`.

## [2026.6.8]

### Added

- Added the Wuji Hand RL open-source base at `hand/attachment/wuji-hand-rl-open-source-base/`, an open-source mounting base for reinforcement-learning setups, shipping the 3D-printable `Base.3mf`, the `Assembly.STEP` CAD assembly, an assembled `Assembly.pdf` drawing, and a `BOM.xlsx` bill of materials.
- Added the Wuji Glove model under `glove/body/`: left and right URDF skeletons at `glove/body/urdf/{left,right}.urdf`, each with 21 revolute joints across the five fingers, an electromagnetic transmitter base on the wrist, and a receiver coil on every fingertip for hand motion tracking.
- Added the glove transmitter and receiver coil meshes at `glove/body/mesh/base_link_TX.STL` and `glove/body/mesh/base_link_RX.STL`.
- Added the transmitter top-cover STEP file and assembled PDF drawing at `glove/body/step/EMFTXC_topcover.step` and `glove/body/step/EMFTXC_topcover.pdf`.

### Removed

- Removed the standalone glove mounting-interface STEP `glove/attachment/glove-attachment.step`. Glove assets now live under `glove/body/`.

## [2026.05.19]

### Fixed

- Corrected the left palm inertia of the Wuji Hand so that the center of mass and inertia tensor are a proper XZ-plane mirror of the right palm. Updated `hand/body/urdf/left.urdf`, `hand/body/urdf/left-ros.urdf`, `hand/body/mjcf/left.xml`, and `hand/body/usd/left/wujihand.usd`.

## [2026.05.18]

### Added

- Added the `wuji_description` ROS2 package under `hand/body/`, with `launch/display.launch.py`, RViz presets, `CMakeLists.txt`, and `package.xml` for left and right Wuji Hand visualization.
- Added URDF models for the left and right Wuji Hand at `hand/body/urdf/{left,right}.urdf` (relative mesh paths) and `hand/body/urdf/{left,right}-ros.urdf` (`package://` paths for ROS2).
- Added MuJoCo MJCF models at `hand/body/mjcf/{left,right}.xml` and STL visual/collision meshes at `hand/body/meshes/{left,right}/`.
- Added Isaac Sim USD assets at `hand/body/usd/{left,right}/`, including fused meshes, PBR materials, physics properties, and collision filter pairs.
- Added simplified structural STEP files of the hand frame at `hand/body/step/`.
- Added the impact-resistant docking attachment at `hand/attachment/impact-resistant-attachment/` with STL, URDF, MJCF, and USD assets, including the ROS URDF that references `package://wuji_description/attachment/impact-resistant-attachment/meshes/hand_docking_link.STL`.
- Added the Unitree G1 mounting adapter at `hand/attachment/unitree-g1-attachment/unitree-g1-docking-adapter.stl`.
- Added adapter STEP files, assembled PDF drawings, and installation notes at `hand/attachment/step/`.
- Added the Glove mounting interface STEP asset at `glove/attachment/glove-attachment.step`.
- Added the top-level `README.md`, `LICENSE` (MIT), and this `CHANGELOG.md`.

[Unreleased]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.27...HEAD
[2026.6.27]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.12...v2026.6.27
[2026.6.12]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.11...v2026.6.12
[2026.6.11]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.10...v2026.6.11
[2026.6.10]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.8...v2026.6.10
[2026.6.8]: https://github.com/wuji-technology/wuji-description/compare/v2026.05.19...v2026.6.8
[2026.05.19]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.19
[2026.05.18]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.18
