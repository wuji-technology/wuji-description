# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses calendar versioning (YYYY.M.D).

## [Unreleased]

## [2026.8.19]

### Changed

- Renamed the Wuji Hand 2 Beta 1 ROS 2 package from `wuji_hand2_description` to `wuji_hand2_beta1_description`. When upgrading, update `colcon --packages-select` arguments, `package://` URIs, dependent `package.xml` entries, launch configuration, and package lookup calls. Remove the workspace `build/`, `install/`, and `log/` directories before rebuilding.
- Marked the Wuji Hand 2 Beta 1 and Beta 2 description packages as architecture-independent resources.

## [2026.8.14]

### Added

- Added the Wuji Hand 2 (Beta 2) delivery — Beta 1 plus one tactile-sensor pad link per fingertip, shipped for both hands as a no-mount robot model rooted at `{l,r}_wrist`.
  - Tactile-sensor pads: each pad (`{p}_{finger}_tip_sensor_frame`) is fixed-welded onto the distal segment via `{p}_{finger}_tip_sensor_frame_fixed` and shown light blue against the silver body. Each pad carries its measured mass — 6.3 g for the thumb pad and 3.0 g for each of the other four fingertip pads — and the distal-segment masses were re-measured to match, dropping to 10.9 g for the thumb distal and 5.0 g for each other-finger distal.
  - Coordinate contract: unchanged from Beta 1 and verified — the same 20 revolute joints with identical integer unit axes, and zero-position fingertip spacing matched left/right within 0.56 mm. The five fingertip query sites (`{l,r}_{finger}_tip`) carry over from Beta 1 unchanged and remain available as MJCF `<site>` elements in display group 3.
  - Formats: URDF (plus `package://wuji_hand2_beta2_description` ROS variants), MuJoCo MJCF, layered Isaac Sim USD, and anatomically named STL meshes (31 per hand), plus a with-mount full-hand STEP CAD assembly per hand (`hand2/hand2_beta2/body/step/wuji-hand2-description-{left,right}_beta2_with_mount_step.STEP`) for mechanical integration. These STEP files are byte-identical to the Beta 1 assemblies and don't yet include the fingertip tactile-sensor pads, so use them for envelope and mounting-interface work and take the models under `body/` as the reference for the pads.
- Added revision-aware model naming for the Wuji Hand 2 (Beta 2): robot/model names are `wujihand2-beta2-{side}` for the no-mount model and `wujihand2-beta2-{side}-mount` for the with-mount model, the USD entry point is `wujihand2_beta2.usd` with `wujihand2_beta2_{base,physics,robot,sensor}.usd` sublayers, and the USD root prim is `wujihand2_beta2_{side}` — no more name collisions with Beta 1 assets.
- Added the standalone ROS2 package `wuji_hand2_beta2_description` rooted at `hand2/hand2_beta2/body/` (`CMakeLists.txt` + `package.xml`), with the Beta 2 `{left,right}-ros.urdf` resolving meshes via `package://wuji_hand2_beta2_description/meshes/...`. The distinct package name (compared with Beta 1's `wuji_hand2_description`) lets both revisions coexist in one workspace, since their mesh sets differ.
- Added palm mounting-interface CAD and dimensioned drawings for the Wuji Hand 2, one pair of files per hand under `hand2/hand2_beta1/attachment/` and `hand2/hand2_beta2/attachment/`.
  - STEP assembly (`wuji-hand2-description-{left,right}-mount_beta{1,2}_step.STEP`): the palm shell together with its wire harness, not the full hand.
  - A3 drawing (`wuji-hand2-description-{left,right}-mount_beta{1,2}.pdf`): a single page dimensioning the threaded holes a custom arm-side adapter bolts into — one M3×0.5 fine-pitch 6H hole (thread depth > 5.5 mm, ⌀4 (0/+0.05) counterbore 2.35 ±0.03 deep) and two M4×0.5 fine-pitch 6H holes (thread depth > 4 mm, ⌀7 (0/+0.06) counterbore 1 mm deep), located by the 28.00 (0/−0.05) and 5.15 (+0.15/−0.05) reference dimensions.
  - Scope: use these when machining a custom arm-flange adapter or fixture. The models under `body/` stay the reference for simulation.
  - Files: the left and right files are mirror images of each other, and the Beta 1 and Beta 2 files are byte-identical because the palm mounting interface did not change between the two revisions. `attachment/` sits outside the ROS2 package root at `body/`, so `colcon` doesn't install it.
- Added the with-mount variant of the Wuji Hand 2 for both revisions, which adds the arm-flange mount link (`{l,r}_mount`, 69 g) as the model root with the wrist shell fixed-welded onto it via `{l,r}_wrist_fixed`.
  - Which to load: the with-mount model bolts the hand onto an arm, and the no-mount model applies when the wrist is the attachment point. Joint names, axes, limits, and actuators are identical between the variants, so one installed package per revision serves both and either can be loaded at any time.
  - Layout: both variants ship side by side inside each revision's `body/` directory, told apart by a `_with_mount` filename suffix — `urdf/{left,right}_with_mount.urdf`, `urdf/{left,right}_with_mount-ros.urdf`, `mjcf/{left,right}_with_mount.xml`, and `usd/{left,right}_with_mount/`.
  - Beta 2 (`hand2/hand2_beta2/body/`): the ROS URDFs resolve via `package://wuji_hand2_beta2_description/meshes/...`, the same prefix the no-mount models use. The two variants share the 31 hand meshes in `meshes/{left,right}/` byte for byte, and the with-mount variant adds only `{l,r}_mount.STL`, bringing that directory to 32 meshes per hand.
  - Beta 1 (`hand2/hand2_beta1/body/`): the ROS URDFs resolve via `package://wuji_hand2_description/meshes/...`, the same prefix the no-mount models use, and the USD entry filename stays `wujihand2.usd` — only the containing directory differs. In the MJCF the wrist shell (`{l,r}_wrist`) is its own body under `{l,r}_mount` rather than fused into it, so the wrist flange frame stays addressable. All 26 hand meshes in `meshes/{left,right}/` are shared byte for byte and the with-mount variant adds only `{l,r}_mount.STL`, bringing each directory to 27. The two variants stay kinematically equivalent: with the fixed mount offset taken out, fingertip poses agree to within 0.006 mm.

### Changed

- Changed the Wuji Hand 2 (Beta 1) **right** hand to a new mechanical CAD export. Kinematics and dynamics are unchanged, and the left hand is byte-identical to the previous release.
  - Motion and mass: the same 20 revolute joints with identical integer unit axes, zero-position fingertip sites moving at most 0.0022 mm, body origins at most 0.0018 mm, and per-body and total mass identical to the digit (0.6207 kg for the no-mount model).
  - Thumb frames: the no-mount export now models `r_thumb_middle` in the same frame as the with-mount export — `r_thumb_mcp` and `r_thumb_ip` both carry zero roll, where the previous export applied +6.3186° on the first and took it back off on the second. Both variants share `r_thumb_middle.STL` byte for byte, and `meshes/right/` stays symmetric with `meshes/left/`.
  - Meshes: `r_thumb_middle.STL` is the only right-hand mesh this export changes. Every other mesh, including all distal and tip meshes, is byte-identical to the previous release, so MJCF collision geometry and rendering are untouched.
- Changed the Wuji Hand 2 (Beta 2) MJCF body tree so that each fingertip tactile-sensor pad is its own body (`{p}_{finger}_tip_sensor_frame`) instead of being fused into the distal segment.
  - Why: MuJoCo's URDF compiler merges zero-DOF welded links by default, which left the pads with no body of their own — no place to attach a `force`/`torque` sensor, no body-level pose query, and a body list that disagreed with the URDF and USD.
  - Masses: each pad now carries its own mass and inertia (thumb 6.3 g, other fingers 3.0 g) and the distal segments carry only theirs (thumb 10.9 g, others 5.0 g). The pads' collision geometry is unchanged and still participates in contact exactly as before.
  - Sites: the empty `{p}_{finger}_tip` frame links stay merged and remain available as MJCF `<site>` elements, which is the idiomatic MuJoCo form for a queryable frame.
  - Kinematics and dynamics: unchanged — total mass, fingertip site poses, whole-hand center of mass, composite inertia, and contact counts all match the previous models to within floating-point noise. The same applies to the with-mount variant, where the wrist shell (`{l,r}_wrist`) is likewise its own body under `{l,r}_mount` rather than fused into it, so the wrist flange frame is addressable.

## [2026.8.3]

### Added

- Added `glove/attachment/Pico-controller-attachment.STEP`, a STEP AP214 CAD assembly for mounting a PICO 4 Ultra controller on the Wuji Glove. It joins the existing Wuji Glove mounting interface and PICO tracker adapter in the same directory.

## [2026.7.23]

### Added

- Added the Wuji Hand 2 (Beta 1) delivery under `hand2/hand2_beta1/body/` — the first revision recalibrated under the new coordinate-system rules. The following coordinate conventions — integer unit joint axes, anatomical link/joint naming (for example `r_thumb_cmc_flex`), the `{l,r}_wrist` root link, and the actuator naming scheme (`{l,r}_{THJ|FFJ|MFJ|RFJ|LFJ}{0-3}`, J0 = flexion … J3 = DIP) — follow this recalibration and are fixed from this revision on. Later revisions stay compatible and only update physical parameters and geometry details. Each hand has 20 actuated revolute joints (5 fingers × 4 joints).
- Added URDF models at `hand2/hand2_beta1/body/urdf/{left,right}.urdf` (relative mesh paths) and `{left,right}-ros.urdf` (`package://wuji_hand2_description` paths), MuJoCo MJCF models at `hand2/hand2_beta1/body/mjcf/{left,right}.xml` whose collision geometry is the convex hull of each link mesh, layered Isaac Sim USD assets at `hand2/hand2_beta1/body/usd/{left,right}/` (base/physics/robot/sensor sublayers plus the logo texture, with drive gains that hold the pose on bare Play), and anatomically named STL meshes at `hand2/hand2_beta1/body/meshes/{left,right}/`. The kp/kv drive gains are carried over from the Wuji Hand platform calibration and will be updated once system identification on the Wuji Hand 2 hardware is complete.
- Added five fingertip query sites per hand (`{l,r}_{finger}_tip`, display group 3) for grasp-point queries and fingertip trajectory evaluation.
- Added full-hand STEP CAD assemblies at `hand2/hand2_beta1/body/step/wuji-hand2-description-{left,right}_beta1_with_mount_step.STEP` for mechanical integration and fixture design.
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

[Unreleased]: https://github.com/wuji-technology/wuji-description/compare/v2026.8.19...HEAD
[2026.8.19]: https://github.com/wuji-technology/wuji-description/compare/v2026.8.14...v2026.8.19
[2026.8.14]: https://github.com/wuji-technology/wuji-description/compare/v2026.8.3...v2026.8.14
[2026.8.3]: https://github.com/wuji-technology/wuji-description/compare/v2026.7.23...v2026.8.3
[2026.7.23]: https://github.com/wuji-technology/wuji-description/compare/v2026.7.14...v2026.7.23
[2026.7.14]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.27...v2026.7.14
[2026.6.27]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.12...v2026.6.27
[2026.6.12]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.11...v2026.6.12
[2026.6.11]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.10...v2026.6.11
[2026.6.10]: https://github.com/wuji-technology/wuji-description/compare/v2026.6.8...v2026.6.10
[2026.6.8]: https://github.com/wuji-technology/wuji-description/compare/v2026.05.19...v2026.6.8
[2026.05.19]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.19
[2026.05.18]: https://github.com/wuji-technology/wuji-description/releases/tag/v2026.05.18
