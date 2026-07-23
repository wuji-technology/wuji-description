# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses calendar versioning (YYYY.M.D).

## [Unreleased]

## [2026.7.23]

### Added

- Added the Wuji Hand 2 (Beta 1) delivery under `hand2/hand2_beta1/body/` — the first revision recalibrated under the new coordinate-system rules. The following coordinate conventions — integer unit joint axes, anatomical link/joint naming (for example `r_thumb_cmc_flex`), the `{l,r}_wrist` root link, and the actuator naming scheme (`{l,r}_{THJ|FFJ|MFJ|RFJ|LFJ}{0-3}`, J0 = flexion … J3 = DIP) — follow this recalibration and are fixed from this revision on. Later revisions stay compatible and only update physical parameters and geometry details. Each hand has 20 actuated revolute joints (5 fingers × 4 joints).
- Added URDF models at `hand2/hand2_beta1/body/urdf/{left,right}.urdf` (relative mesh paths) and `{left,right}-ros.urdf` (`package://wuji_hand2_description` paths), MuJoCo MJCF models at `hand2/hand2_beta1/body/mjcf/{left,right}.xml` whose collision geometry is the convex hull of each link mesh, layered Isaac Sim USD assets at `hand2/hand2_beta1/body/usd/{left,right}/` (base/physics/robot/sensor sublayers plus the logo texture, with drive gains that hold the pose on bare Play), and anatomically named STL meshes at `hand2/hand2_beta1/body/meshes/{left,right}/`. The kp/kv drive gains are carried over from the Wuji Hand platform calibration and will be updated once system identification on the Wuji Hand 2 hardware is complete.
- Added five fingertip query sites per hand (`{l,r}_{finger}_tip`, display group 3) for grasp-point queries and fingertip trajectory evaluation.
- Added full-hand STEP CAD assemblies at `hand2/hand2_beta1/body/step/WUJI-hand2_beta1_{left,right}_STEP.STEP` for mechanical integration and fixture design.
- Added the standalone ROS2 package `wuji_hand2_description` rooted at `hand2/hand2_beta1/body/` (`CMakeLists.txt` + `package.xml`), so the Wuji Hand 2 (Beta 1) ROS URDFs resolve their meshes independently of the Wuji Hand `wuji_description` package.

### Changed

- Changed the collision policy of the Wuji Hand 2 (Beta 1): every link participates in collision (uniform contype/conaffinity 1/1) with only 10 assembly-overlap pairs excluded (each finger's proximal / proximal_abd against the wrist). Inter-finger and fingertip–palm contacts stay live. Display layers are group 1 visual (silver), group 2 collision (translucent light purple), and group 3 fingertip sites. The fingertip soft-pad meshes (`*_tip.STL`) ship with the package but are not attached as collision geometry yet — fingertip contact is carried by the distal-segment geometry, so the contact point sits slightly off the real finger pad.

### Removed

- Removed the previous Wuji Hand 2 (Beta) revision `hand2_beta/body/` (rooted at `{l,r}_base_link`). It is superseded by the recalibrated `hand2/hand2_beta1/body/` revision. This also retires the earlier structural STEP assemblies (`Wuji-Hand2-Beta1-{left,right}.step`) and the arm-flange adapter mount (`Wuji-Hand2-Adapter-Mount-Beta1.step`) that shipped under `hand2_beta/body/step/`.

## [2026.7.14]

### Added

- Added glove mounting attachments under `glove/attachment/`: `Wuji-glove-attachment.STEP` (Wuji Glove mounting interface) and `Pico-tracker-attachment.STEP` (adapter for mounting a PICO tracker), both STEP AP214 CAD assemblies for mechanical integration.

### Fixed

- Fixed the ROS `package://` mesh paths in the Wuji Hand 2 (Beta) (`hand2_beta/body/urdf/{left,right}-ros.urdf`) and soft-pad hand (`hand/body-with-soft/urdf/{left,right}-ros.urdf`) URDFs, which previously resolved into the standalone hand's mesh directory and failed to load. The `wuji_description` package now installs both models into its share directory, and each URDF points at its own mesh path — `package://wuji_description/hand2_beta/body/meshes/` for the Wuji Hand 2 (Beta) and `package://wuji_description/body-with-soft/meshes/` for the soft-pad hand.

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
- Added simplified-collision variants of the soft-pad hand at `hand/body-with-soft/urdf/{left,right}_simplified.urdf`, `hand/body-with-soft/mjcf/{left,right}_simplified.xml`, and `hand/body-with-soft/usd/{left,right}_simplified/`. They replace the collision geometry of each finger's `link4` and the thumb soft pad with decimated meshes for faster contact simulation. Visual geometry is unchanged.
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

[Unreleased]: https://github.com/wuji-technology/wuji-description/compare/v2026.7.23...HEAD
[2026.7.23]: https://github.com/wuji-technology/wuji-description/compare/v2026.7.14...v2026.7.23
[2026.7.14]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.27...v2026.7.14
[2026.6.27]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.12...v2026.6.27
[2026.6.12]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.11...v2026.6.12
[2026.6.11]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.10...v2026.6.11
[2026.6.10]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.8...v2026.6.10
[2026.6.8]: https://github.com/wuji-technology/wuji-description/compare/v2026.05.19...v2026.6.8
[2026.05.19]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.19
[2026.05.18]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.18
