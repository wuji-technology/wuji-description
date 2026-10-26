# wuji-description

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/wuji-technology/wuji-description)](https://github.com/wuji-technology/wuji-description/releases)

Robot model description package for the Wuji Hand and related accessories. Provides URDF, MuJoCo (MJCF), and USD assets for simulation and visualization, plus STEP/CAD files for mechanical integration. The `hand/body/` package includes a ROS2 launch file and RViz presets for the first-generation Wuji Hand. Hand 2 packages provide model assets for use with your own launch configuration.

Hand 2.1 and Hand 2.2 each provide left and right models in bare, cover, and glove appearance variants. Common hardware uses shared collision meshes, and all variants use the same ROS2 package for their revision.

**Get started with [Quick Start](#quick-start). For detailed documentation, please refer to [Wuji Description](https://docs.wuji.tech/docs/en/wuji-description/latest/) on Wuji Docs Center.**

## Repository Structure

```text
.
├── hand/
│   ├── body/                                // ROS2 package: simulation and visualization assets for the hand body
│   │   ├── launch/display.launch.py         // ROS2 launch file (selects left or right hand)
│   │   ├── meshes/{left,right}/             // STL meshes for visual and collision geometry
│   │   ├── mjcf/{left,right}.xml            // MuJoCo XML models
│   │   ├── rviz/{left,right}.rviz           // RViz presets
│   │   ├── step/                            // Simplified structural STEP files of the hand frame
│   │   ├── urdf/{left,right}.urdf           // URDF models (relative mesh paths, for local tools)
│   │   ├── urdf/{left,right}-ros.urdf       // URDF models (package:// paths, for ROS2)
│   │   ├── usd/{left,right}/                // Isaac Sim USD assets
│   │   ├── CMakeLists.txt                   // ROS2 package install rules
│   │   └── package.xml                      // ROS2 package manifest
│   ├── body-with-soft/                      // Hand variant with a soft pad on the thumb
│   │   ├── meshes/{left,right}/             // STL meshes, including soft-pad and simplified collision meshes
│   │   ├── mjcf/{left,right}.xml            // MuJoCo XML models (plus {left,right}_simplified.xml)
│   │   ├── urdf/{left,right}.urdf           // URDF models (plus -ros and _simplified variants)
│   │   ├── usd/{left,right}/                // Isaac Sim USD assets (plus {left,right}_simplified/)
│   │   └── params.csv                       // Actuator parameters
│   └── attachment/
│       ├── impact-resistant-attachment/     // Impact-resistant docking link (STL, URDF, MJCF, USD)
│       ├── step/                            // Adapter STEP files, assembled PDFs, and installation notes
│       ├── unitree-g1-attachment/           // STL adapter for mounting on Unitree G1
│       └── wuji-hand-rl-open-source-base/   // Open-source mounting base for RL setups (3MF, STEP, PDF, BOM)
├── hand2/
│   ├── hand2_1/
│   │   ├── body/                            // ROS2 package wuji_hand2_1_description: Wuji Hand 2.1, rooted at the arm-flange mount, frozen Wuji Hand 2 coordinate contract
│   │   │   ├── meshes/{left,right}/         // Shared hardware and cover meshes, plus visual_nails/ for glove visuals
│   │   │   ├── mjcf/{left,right}.xml        // MuJoCo XML models
│   │   │   ├── mjcf/{left,right}_with_cover.xml // MuJoCo models with covers
│   │   │   ├── mjcf/{left,right}_with_glove.xml // MuJoCo models with black hardware and silver nail caps
│   │   │   ├── step/                            // Historical full-hand STEP assemblies (not installed by colcon)
│   │   │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// versions)
│   │   │   ├── urdf/{left,right}_with_cover.urdf // URDF models with covers (plus _with_cover-ros.urdf)
│   │   │   ├── urdf/{left,right}_with_glove.urdf // Glove appearance URDFs (plus _with_glove-ros.urdf)
│   │   │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2_1.usd)
│   │   │   ├── usd/{left,right}_with_cover/ // Layered wujihand2_1_cover.usd
│   │   │   ├── usd/{left,right}_with_glove/ // Layered wujihand2_1_glove.usd
│   │   │   ├── CMakeLists.txt               // ROS2 package install rules
│   │   │   └── package.xml                  // ROS2 package manifest
│   │   └── attachment/                      // Palm mounting interfaces, left/right adapter mounts, and adapter flange (STEP + PDF)
│   └── hand2_2/
│       ├── body/                            // ROS2 package wuji_hand2_2_description: Wuji Hand 2.2, Hand 2.1 + one tactile sensor pad per fingertip
│       │   ├── meshes/{left,right}/         // Shared hardware and cover meshes, plus visual_nails/ for glove visuals
│       │   ├── mjcf/{left,right}.xml        // MuJoCo XML models
│       │   ├── mjcf/{left,right}_with_cover.xml // MuJoCo models with covers
│       │   ├── mjcf/{left,right}_with_glove.xml // MuJoCo models with black hardware and silver nail caps
│       │   ├── step/                            // Historical full-hand STEP assemblies (not installed by colcon)
│       │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// versions)
│       │   ├── urdf/{left,right}_with_cover.urdf // URDF models with covers (plus _with_cover-ros.urdf)
│       │   ├── urdf/{left,right}_with_glove.urdf // Glove appearance URDFs (plus _with_glove-ros.urdf)
│       │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2_2.usd)
│       │   ├── usd/{left,right}_with_cover/ // Layered wujihand2_2_cover.usd
│       │   ├── usd/{left,right}_with_glove/ // Layered wujihand2_2_glove.usd
│       │   ├── CMakeLists.txt               // ROS2 package install rules
│       │   └── package.xml                  // ROS2 package manifest
│       └── attachment/                      // Palm mounting interfaces, left/right adapter mounts, and adapter flange (STEP + PDF)
├── glove/
│   ├── body/                                // Wuji Glove model (hand motion tracking)
│   │   ├── urdf/{left,right}.urdf           // URDF skeletons (21 revolute DOF per hand)
│   │   ├── mesh/base_link_{TX,RX}.STL       // Transmitter base and fingertip receiver coil
│   │   └── step/EMFTXC_topcover.{step,pdf}  // Transmitter top-cover STEP and assembled drawing
│   └── attachment/                          // Glove mounting attachments (STEP CAD assemblies)
│       ├── Wuji-glove-attachment.STEP       // Wuji Glove mounting interface
│       ├── Pico-tracker-attachment.STEP     // Adapter for mounting a PICO tracker
│       └── Pico-controller-attachment.STEP  // Adapter for mounting a PICO 4 Ultra controller
├── LICENSE
└── README.md
```

## Quick Start

### Installation

```bash
git clone https://github.com/wuji-technology/wuji-description.git
cd wuji-description
```

### Hand Body

#### MuJoCo

```bash
# Right hand
python -m mujoco.viewer --mjcf=hand/body/mjcf/right.xml

# Left hand
python -m mujoco.viewer --mjcf=hand/body/mjcf/left.xml
```

#### ROS2 and RViz

`hand/body/` is the ROS2 package source (`wuji_description`). The package installs `hand/attachment/` as a sibling resource, so clone the entire repository into your workspace `src/` rather than copying `hand/body/` in isolation:

```bash
# Source ROS2 environment, replace <distro> with your installed ROS2 distribution
source /opt/ros/<distro>/setup.bash

cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..

rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select wuji_description
source install/setup.bash

# Left hand (default)
ros2 launch wuji_description display.launch.py

# Right hand
ros2 launch wuji_description display.launch.py hand:=right
```

#### Isaac Sim (USD)

Load `hand/body/usd/left/wujihand.usd` or `hand/body/usd/right/wujihand.usd` directly in Isaac Sim.
For a complete simulation example, see [isaaclab-sim](https://github.com/wuji-technology/isaaclab-sim).

### Hand Body with Soft Pad

`hand/body-with-soft/` is a variant of the hand body with a soft pad fixed to the thumb (`finger1_link2_softbody`). Every format also ships a `_simplified` variant that replaces the collision geometry of each finger's `link4` and the thumb soft pad with decimated meshes for faster contact simulation. Visual geometry is identical.

```bash
# Full collision meshes
python -m mujoco.viewer --mjcf=hand/body-with-soft/mjcf/right.xml

# Simplified collision meshes
python -m mujoco.viewer --mjcf=hand/body-with-soft/mjcf/right_simplified.xml
```

For Isaac Sim, load `hand/body-with-soft/usd/{left,right}/wujihand.usd` or the `{left,right}_simplified` counterparts.

### Wuji Hand 2.1

`hand2/hand2_1/body/` provides Wuji Hand 2.1 models for both hands in bare, cover, and glove appearance variants. Each hand keeps the frozen Wuji Hand 2 coordinate contract: 20 actuated revolute joints (five fingers with four joints each), integer unit joint axes, and anatomical link and joint names such as `r_thumb_cmc_flex`, `r_index_finger_mcp_abd`, and `r_middle_finger_pip`. The model includes two features:

- The arm-flange mount is part of the hand: the model root is `{l,r}_mount` (69 g), with the wrist shell fixed-welded onto it via `{l,r}_wrist_fixed`. There is no separate no-mount model.
- A massless wrist IMU frame `{l,r}_wrist_imu_frame` is fixed-welded onto the wrist shell via `{l,r}_wrist_imu_frame_fixed` at the CAD-delivered pose, so IMU readings can be expressed in the hand's frames.

Without covers, each hand has 28 URDF links: 20 finger segments, the mount, the wrist shell, the IMU frame, and five fingertip query frames (`{l,r}_{finger}_tip`, also MJCF `<site>` elements in display group 3). Each hand has a configured mass of 687.8 g, including a 38.1 g thumb middle segment and an 11.7 g thumb distal segment. Robot names are `wujihand2_1-{left,right}`. Finger links are metal silver, and the mount and wrist shell are matte black. The cover and glove variants each add 21 fixed links, bringing the total to 49 links and 708.8 g per hand (see [Cover Variants](#wuji-hand-2-cover-variants)). STEP models and PDF drawings for the palm mounting interfaces, adapter mounts, and adapter flange are available under `hand2/hand2_1/attachment/` (see [Palm Mounting Interface](#wuji-hand-2-palm-mounting-interface) and [Adapter Mounts and Flange](#adapter-mounts-and-flange)).

Model formats without covers under `hand2/hand2_1/body/`:

- URDF: `urdf/{left,right}.urdf` (relative mesh paths) and `urdf/{left,right}-ros.urdf` (`package://`)
- MuJoCo: `mjcf/{left,right}.xml` — convex-hull collision geometry for the 22 links with meshes, 10 assembly-overlap pairs excluded
- Isaac Sim: layered USD at `usd/{left,right}/` (entry point `wujihand2_1.usd`, root prim `wujihand2_1_{left,right}`)
- Meshes: 48 canonical STL files per hand directly in `meshes/{left,right}/`, plus glove visual meshes in `visual_nails/`. URDF and MJCF reference 22 files without covers and 43 with covers
- Mechanical: STEP models and PDF drawings for the palm mounting interfaces, left/right adapter mounts, and adapter flange at `hand2/hand2_1/attachment/` (outside the ROS2 package root)

The five `*_tip.STL` files in each mesh directory are not referenced by the URDF or MJCF models. The five fingertip query frames and the IMU frame have no visual or collision mesh geometry.

Preview in MuJoCo (press 1/2 to toggle the visual/collision display groups):

```bash
python -m mujoco.viewer --mjcf=hand2/hand2_1/body/mjcf/right.xml
```

For Isaac Sim, load `hand2/hand2_1/body/usd/{left,right}/wujihand2_1.usd` directly. Keep each `usd/{left,right}/` directory intact. Drive gains hold the pose on bare Play and are overridden by your ArticulationCfg at runtime. Every massless frame (the five fingertip frames and the IMU frame) carries an explicit 1e-7 kg placeholder mass, so PhysX does not fall back to its 1 kg default for them.

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand2/hand2_1/body/urdf/right.urdf
```

#### ROS2

`hand2/hand2_1/body/` is a standalone ROS2 package (`wuji_hand2_1_description`). Its `{left,right}-ros.urdf` reference meshes via `package://wuji_hand2_1_description/meshes/...`, independent of the Wuji Hand `wuji_description` package:

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
colcon build --packages-select wuji_hand2_1_description
source install/setup.bash

# Verify resolution, then load from your own launch file / robot_state_publisher
check_urdf $(ros2 pkg prefix wuji_hand2_1_description)/share/wuji_hand2_1_description/urdf/right-ros.urdf
```

### Wuji Hand 2.2

`hand2/hand2_2/body/` provides Wuji Hand 2.2 models for both hands in bare, cover, and glove appearance variants. They share the Hand 2.1 joints, mount root, IMU frame, and coordinate contract. Each fingertip adds a matte black tactile-sensor pad link (`{l,r}_{finger}_tip_sensor_frame`) fixed to the distal segment through `{l,r}_{finger}_tip_sensor_frame_fixed`, bringing the URDF link count without covers to 33 per hand.

The thumb distal segment and pad weigh 5.7 g and 6.0 g. Each other distal segment and pad weigh 4.9 g and 2.9 g. Pad masses remain provisional pending measurement. Without covers, each hand totals 687.8 g, matching Hand 2.1, and retains the same five fingertip query sites. Robot names are `wujihand2_2-{left,right}`. The cover and glove variants each add 21 fixed links, bringing the total to 54 links and 708.8 g per hand (see [Cover Variants](#wuji-hand-2-cover-variants)).

Model formats without covers under `hand2/hand2_2/body/` mirror Hand 2.1:

- URDF: `urdf/{left,right}.urdf` (relative mesh paths) and `urdf/{left,right}-ros.urdf` (`package://`)
- MuJoCo: `mjcf/{left,right}.xml` — convex-hull collision geometry for the 27 links with meshes, 15 pairs excluded (the 10 assembly-overlap pairs plus each distal segment against its own pad)
- Isaac Sim: layered USD at `usd/{left,right}/` (entry point `wujihand2_2.usd`, root prim `wujihand2_2_{left,right}`)
- Meshes: 53 canonical STL files per hand directly in `meshes/{left,right}/`, plus glove visual meshes in `visual_nails/`. URDF and MJCF reference 27 files without covers and 48 with covers. All variants include five tactile-sensor pad meshes (`*_tip_sensor_frame.STL`)
- Mechanical: STEP models and PDF drawings for the palm mounting interfaces, left/right adapter mounts, and adapter flange at `hand2/hand2_2/attachment/` (outside the ROS2 package root)

As in Hand 2.1, each mesh directory also contains five unreferenced `*_tip.STL` files. These are separate from the five tactile-sensor pad meshes used by Hand 2.2. The fingertip query frames and the IMU frame have no visual or collision mesh geometry.

Preview in MuJoCo:

```bash
python -m mujoco.viewer --mjcf=hand2/hand2_2/body/mjcf/right.xml
```

For Isaac Sim, load `hand2/hand2_2/body/usd/{left,right}/wujihand2_2.usd` directly. Keep each `usd/{left,right}/` directory intact.

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand2/hand2_2/body/urdf/right.urdf
```

#### ROS2

`hand2/hand2_2/body/` is a standalone ROS2 package (`wuji_hand2_2_description`) — a distinct package name from Hand 2.1's `wuji_hand2_1_description`, so both revisions can coexist in one workspace:

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
colcon build --packages-select wuji_hand2_2_description
source install/setup.bash

check_urdf $(ros2 pkg prefix wuji_hand2_2_description)/share/wuji_hand2_2_description/urdf/right-ros.urdf
```

### Wuji Hand 2 Cover Variants

Choose a bare, cover, or glove appearance for either hand. All three variants use the same ROS2 package within each revision. The glove appearance describes the robot hand, while `glove/body/` contains the separate Wuji Glove motion-tracking model. The cover and glove variants retain 21 fixed rigid cover links and 20 actuated joints.

- **Bare:** exposes the silver finger hardware, with a black palm and mount. Hand 2.2 also includes black tactile pads. Use the filenames without a variant suffix.
- **Cover:** preserves the base colors and adds 10 black visual cylinders around the finger bodies. Fingertips and end joints remain exposed.
- **Glove:** uses black hardware with silver nail surfaces. It retains the logo, cover links, and Hand 2.2 tactile pads, with colors applied to the hardware surface meshes.

The cylinders and nail partitions affect visuals only. The cover and glove variants share mass, inertia, joints, and collision geometry. Each cover has a provisional mass of 1 g, so both variants have a configured mass of 708.8 g per hand. This is not a measured hand-and-glove mass. The models do not include deformable-body simulation or additional physical glove mass.

Canonical hardware and cover meshes remain in `meshes/{side}/`. The glove variant splits each distal visual into a silver nail surface and a black remainder under `meshes/{side}/visual_nails/`, adding 10 visual STL files per hand. These visual partitions cover the original triangles, while collisions use the complete original meshes. USD retains the complete hardware meshes and uses material subsets for the silver nail surfaces. The cover USD adds visual cylinders. Keep all shared meshes when copying a package.

| Revision | Variant | URDF Links per Hand | Configured Mass per Hand |
|----------|---------|---------------------|--------------------------|
| Hand 2.1 | Bare | 28 | 687.8 g |
| Hand 2.1 | Cover | 49 | 708.8 g |
| Hand 2.1 | Glove | 49 | 708.8 g |
| Hand 2.2 | Bare | 33 | 687.8 g |
| Hand 2.2 | Cover | 54 | 708.8 g |
| Hand 2.2 | Glove | 54 | 708.8 g |

Paths below are relative to either `hand2/hand2_1/body/` or `hand2/hand2_2/body/`. Set `{side}` to `left` or `right`.

| Format | Bare | Cover | Glove |
|--------|------|-----------|-----------|
| URDF | `urdf/{side}.urdf` | `urdf/{side}_with_cover.urdf` | `urdf/{side}_with_glove.urdf` |
| ROS URDF | `urdf/{side}-ros.urdf` | `urdf/{side}_with_cover-ros.urdf` | `urdf/{side}_with_glove-ros.urdf` |
| MuJoCo MJCF | `mjcf/{side}.xml` | `mjcf/{side}_with_cover.xml` | `mjcf/{side}_with_glove.xml` |
| Isaac Sim USD Directory | `usd/{side}/` | `usd/{side}_with_cover/` | `usd/{side}_with_glove/` |

Preview the cover and glove appearances in MuJoCo from the repository root:

```bash
python -m mujoco.viewer --mjcf=hand2/hand2_1/body/mjcf/right_with_cover.xml
python -m mujoco.viewer --mjcf=hand2/hand2_1/body/mjcf/right_with_glove.xml
python -m mujoco.viewer --mjcf=hand2/hand2_2/body/mjcf/right_with_cover.xml
python -m mujoco.viewer --mjcf=hand2/hand2_2/body/mjcf/right_with_glove.xml
```

Preview with a URDF viewer:

```bash
urdf-viz hand2/hand2_1/body/urdf/right_with_glove.urdf
urdf-viz hand2/hand2_2/body/urdf/right_with_glove.urdf
```

For Isaac Sim, load `usd/{side}_with_cover/wujihand2_1_cover.usd` or `usd/{side}_with_glove/wujihand2_1_glove.usd` from the Hand 2.1 package. Hand 2.2 uses `wujihand2_2_cover.usd` and `wujihand2_2_glove.usd` in the corresponding directories. Keep each USD directory intact, including `configuration/` and `textures/`.

Hand 2 packages install `meshes/`, `urdf/`, `mjcf/`, and `usd/`. They do not include a display launch file or RViz preset. Load the selected `-ros.urdf` through your own `robot_state_publisher` launch configuration. After building and sourcing the packages as described above, check the installed glove models:

```bash
check_urdf "$(ros2 pkg prefix wuji_hand2_1_description)/share/wuji_hand2_1_description/urdf/right_with_glove-ros.urdf"
check_urdf "$(ros2 pkg prefix wuji_hand2_2_description)/share/wuji_hand2_2_description/urdf/right_with_glove-ros.urdf"
```

Use `left` filenames for the left hand, or replace `_with_glove` with `_with_cover` to load the cover variant. URDF and MJCF robot names end in `-cover` or `-glove`, for example `wujihand2_2-right-glove`.

### Wuji Hand 2 Full-Hand STEP Assemblies

Each revision includes left and right full-hand STEP files under `hand2/hand2_{1,2}/body/step/`, named `wuji-hand2-description-{left,right}_hand2_{1,2}_step.STEP`. These files preserve the historical Beta assemblies with revision-specific filenames. They are not regenerated from the current bare, cover, or glove simulation models. Use the simulation assets above to inspect those appearances.

The STEP files remain available in the repository checkout. The Hand 2 ROS2 install rules do not install `step/`. For palm mounting interfaces, adapter mounts, and the adapter flange, use the STEP models and PDF drawings in the separate `attachment/` directories below.

### Wuji Hand 2 Palm Mounting Interface

`hand2/hand2_1/attachment/` and `hand2/hand2_2/attachment/` include palm mounting-interface files for designing arm-side adapters or fixtures. Each hand has one pair of `mount` files:

- `wuji-hand2-description-{left,right}-mount_hand2_{1,2}_step.STEP` — a STEP assembly of the palm together with its wire harness. This is the palm only, not the full hand.
- `wuji-hand2-description-{left,right}-mount_hand2_{1,2}.pdf` — a single-page A3 drawing dimensioning the threaded holes your adapter bolts into: one M3×0.5 fine-pitch 6H hole (thread depth > 5.5 mm, ⌀4 (0/+0.05) counterbore 2.35 ±0.03 deep) and two M4×0.5 fine-pitch 6H holes (thread depth > 4 mm, ⌀7 (0/+0.06) counterbore 1 mm deep), located by the 28.00 (0/−0.05) and 5.15 (+0.15/−0.05) reference dimensions.

The left and right `mount` files are mirror images of each other, and the corresponding Hand 2.1 and Hand 2.2 `mount` files are identical because the palm mounting interface did not change between the two revisions. These files are for mechanical integration only — they are not needed for simulation, and `attachment/` sits outside the ROS2 package root at `body/`, so `colcon` does not install it. To simulate the hand already bolted to an arm, load the models under `body/`: they are rooted at the mount link `{l,r}_mount`.

#### Adapter Mounts and Flange

The [Hand 2.1 attachment directory](hand2/hand2_1/attachment/) and [Hand 2.2 attachment directory](hand2/hand2_2/attachment/) also include a left adapter mount, a right adapter mount, and an adapter flange. Each component has a STEP model and a PDF drawing, adding six files per revision alongside the palm mounting-interface files:

| Component | STEP Model | PDF Drawing |
|-----------|------------|-------------|
| Left adapter mount | `wuji-hand2-description-left-adapter_hand2_{1,2}_step.STEP` | `wuji-hand2-description-left-adapter_hand2_{1,2}.pdf` |
| Right adapter mount | `wuji-hand2-description-right-adapter_hand2_{1,2}_step.STEP` | `wuji-hand2-description-right-adapter_hand2_{1,2}.pdf` |
| Adapter flange | `wuji-hand2-description-adapter-flange_hand2_{1,2}_step.STEP` | `wuji-hand2-description-adapter-flange_hand2_{1,2}.pdf` |

Use `hand2_1` or `hand2_2` in place of `hand2_{1,2}` to match the directory. Corresponding adapter files have identical contents across the two revisions. The adapter flange has one STEP/PDF pair per revision, without separate left and right filenames. These mechanical attachments are outside the ROS2 package root and are not installed by `colcon`.

### Hand Attachments

`hand/attachment/` ships optional components for the Wuji Hand. They are not loaded by the default display launch file. Attach them via a fixed joint when composing a full robot description.

- **`impact-resistant-attachment/`** — a docking link designed to absorb impacts before they reach the hand. Includes STL mesh, URDF (relative and `package://` variants), MJCF, and USD for full simulation integration.
- **`step/`** — STEP source files for two adapters that connect the hand to a robotic arm flange:
  - `Direct-Adapter-Mount.step` — rigid direct mount.
  - `Impact-Resistant-Adapter.step` — mechanical companion to the impact-resistant attachment above.
  - Each option ships with an assembled PDF drawing. See [Adapter-Installation-Instructions.md](hand/attachment/step/Adapter-Installation-Instructions.md) for step-by-step mounting guidance.
- **`unitree-g1-attachment/`** — STL adapter for mounting the Wuji Hand on a Unitree G1 humanoid.
- **`wuji-hand-rl-open-source-base/`** — an open-source mounting base for reinforcement-learning setups. Ships the 3D-printable `Base.3mf`, the `Assembly.STEP` CAD assembly, an assembled `Assembly.pdf` drawing, and a `BOM.xlsx` bill of materials for self-assembly.

Preview the impact-resistant attachment in MuJoCo:

```bash
python -m mujoco.viewer --mjcf=hand/attachment/impact-resistant-attachment/mjcf/docking.xml
```

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand/attachment/impact-resistant-attachment/urdf/docking.urdf
```

### Glove

`glove/body/` provides the Wuji Glove model used for hand motion tracking. Each hand is described by a URDF skeleton (`glove/body/urdf/{left,right}.urdf`) with 21 revolute joints across the five fingers, an electromagnetic transmitter base on the wrist (`base_link_TX.STL`), and a receiver coil on every fingertip (`base_link_RX.STL`). The transmitter top-cover STEP file and assembled drawing are under `glove/body/step/`. Mounting attachments are provided as STEP CAD assemblies under `glove/attachment/`: `Wuji-glove-attachment.STEP` (the Wuji Glove mounting interface), `Pico-tracker-attachment.STEP` (an adapter for mounting a PICO tracker), and `Pico-controller-attachment.STEP` (an adapter for mounting a PICO 4 Ultra controller).

Preview a glove model with a non-ROS URDF viewer such as `urdf-viz`:

```bash
urdf-viz glove/body/urdf/right.urdf
```

## Contact

For any questions, please contact [support@wuji.tech](mailto:support@wuji.tech).
