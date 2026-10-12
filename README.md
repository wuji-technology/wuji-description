# wuji-description

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/wuji-technology/wuji-description)](https://github.com/wuji-technology/wuji-description/releases)

Robot model description package for the Wuji Hand and related accessories. Provides URDF, MuJoCo (MJCF), and USD assets for simulation and visualization, plus STEP/CAD files for mechanical integration. Includes a ROS2 launch and RViz configuration for quick inspection of left and right hand models.

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
│   │   │   ├── meshes/{left,right}/         // 27 STL files per hand, 22 referenced by URDF/MJCF
│   │   │   ├── mjcf/{left,right}.xml        // MuJoCo XML models
│   │   │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// versions)
│   │   │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2_1.usd)
│   │   │   ├── CMakeLists.txt               // ROS2 package install rules
│   │   │   └── package.xml                  // ROS2 package manifest
│   │   └── attachment/                      // Palm mounting-interface STEP + A3 dimensioned drawing, one pair per hand
│   └── hand2_2/
│       ├── body/                            // ROS2 package wuji_hand2_2_description: Wuji Hand 2.2, Hand 2.1 + one tactile sensor pad per fingertip
│       │   ├── meshes/{left,right}/         // 32 STL files per hand, 27 referenced by URDF/MJCF
│       │   ├── mjcf/{left,right}.xml        // MuJoCo XML models
│       │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// versions)
│       │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2_2.usd)
│       │   ├── CMakeLists.txt               // ROS2 package install rules
│       │   └── package.xml                  // ROS2 package manifest
│       └── attachment/                      // Palm mounting-interface STEP + A3 dimensioned drawing, one pair per hand
├── glove/
│   ├── body/                                // Wuji Glove model (hand motion tracking)
│   │   ├── urdf/{left,right}.urdf           // URDF skeletons (21 revolute DOF per hand)
│   │   ├── mesh/base_link_{TX,RX}.STL       // Transmitter base and fingertip receiver coil
│   │   └── step/EMFTXC_topcover.{step,pdf}  // Transmitter top-cover STEP and assembled drawing
│   └── attachment/                          // Glove mounting attachments (STEP CAD assemblies)
│       ├── Wuji-glove-attachment.STEP       // Wuji Glove mounting interface
│       ├── Pico-tracker-attachment.STEP     // Adapter for mounting a PICO tracker
│       └── Pico-controller-attachment.STEP  // Adapter for mounting a PICO 4 Ultra controller
├── CHANGELOG.md
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

`hand2/hand2_1/body/` provides Wuji Hand 2.1 models for both hands. Each hand keeps the frozen Wuji Hand 2 coordinate contract: 20 actuated revolute joints (five fingers with four joints each), integer unit joint axes, and anatomical link and joint names such as `r_thumb_cmc_flex`, `r_index_finger_mcp_abd`, and `r_middle_finger_pip`. The model includes two features:

- The arm-flange mount is part of the hand: the model root is `{l,r}_mount` (69 g), with the wrist shell fixed-welded onto it via `{l,r}_wrist_fixed`. There is no separate no-mount model.
- A massless wrist IMU frame `{l,r}_wrist_imu_frame` is fixed-welded onto the wrist shell via `{l,r}_wrist_imu_frame_fixed` at the CAD-delivered pose, so IMU readings can be expressed in the hand's frames.

Each hand has 28 URDF links: 20 finger segments, the mount, the wrist shell, the IMU frame, and five fingertip query frames (`{l,r}_{finger}_tip`, also MJCF `<site>` elements in display group 3). Each hand weighs 687.8 g, including a 38.1 g thumb middle segment and an 11.7 g thumb distal segment. Robot names are `wujihand2_1-{left,right}`. Finger links are metal silver, and the mount and wrist shell are matte black. The palm mounting interface is available as STEP files and drawings under `hand2/hand2_1/attachment/` (see [Palm Mounting Interface](#wuji-hand-2-palm-mounting-interface)).

Shipped formats under `hand2/hand2_1/body/`:

- URDF: `urdf/{left,right}.urdf` (relative mesh paths) and `urdf/{left,right}-ros.urdf` (`package://`)
- MuJoCo: `mjcf/{left,right}.xml` — convex-hull collision geometry for the 22 links with meshes, 10 assembly-overlap pairs excluded
- Isaac Sim: layered USD at `usd/{left,right}/` (entry point `wujihand2_1.usd`, root prim `wujihand2_1_{left,right}`)
- Meshes: 27 STL files per hand at `meshes/{left,right}/`, of which 22 are referenced by the URDF and MJCF models
- Mechanical: palm mounting-interface STEP assembly and A3 drawing per hand at `hand2/hand2_1/attachment/` (outside the ROS2 package root)

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

`hand2/hand2_2/body/` provides Wuji Hand 2.2 models for both hands. They share the Hand 2.1 joints, mount root, IMU frame, and coordinate contract. Each fingertip adds a matte black tactile-sensor pad link (`{l,r}_{finger}_tip_sensor_frame`) fixed to the distal segment through `{l,r}_{finger}_tip_sensor_frame_fixed`, bringing the URDF link count to 33 per hand.

The thumb distal segment and pad weigh 5.7 g and 6.0 g. Each other distal segment and pad weigh 4.9 g and 2.9 g. Pad masses remain provisional pending measurement. Each hand totals 687.8 g, matching Hand 2.1, and retains the same five fingertip query sites. Robot names are `wujihand2_2-{left,right}`.

Shipped formats under `hand2/hand2_2/body/` mirror Hand 2.1:

- URDF: `urdf/{left,right}.urdf` (relative mesh paths) and `urdf/{left,right}-ros.urdf` (`package://`)
- MuJoCo: `mjcf/{left,right}.xml` — convex-hull collision geometry for the 27 links with meshes, 15 pairs excluded (the 10 assembly-overlap pairs plus each distal segment against its own pad)
- Isaac Sim: layered USD at `usd/{left,right}/` (entry point `wujihand2_2.usd`, root prim `wujihand2_2_{left,right}`)
- Meshes: 32 STL files per hand at `meshes/{left,right}/`, of which 27 are referenced by the URDF and MJCF models, including five tactile-sensor pad meshes (`*_tip_sensor_frame.STL`)
- Mechanical: palm mounting-interface STEP assembly and A3 drawing per hand at `hand2/hand2_2/attachment/` (outside the ROS2 package root)

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

### Wuji Hand 2 Palm Mounting Interface

`hand2/hand2_1/attachment/` and `hand2/hand2_2/attachment/` ship the palm mounting interface, for machining your own arm-side adapter or fixture. One pair of files per hand:

- `wuji-hand2-description-{left,right}-mount_hand2_{1,2}_step.STEP` — a STEP assembly of the palm together with its wire harness. This is the palm only, not the full hand.
- `wuji-hand2-description-{left,right}-mount_hand2_{1,2}.pdf` — a single-page A3 drawing dimensioning the threaded holes your adapter bolts into: one M3×0.5 fine-pitch 6H hole (thread depth > 5.5 mm, ⌀4 (0/+0.05) counterbore 2.35 ±0.03 deep) and two M4×0.5 fine-pitch 6H holes (thread depth > 4 mm, ⌀7 (0/+0.06) counterbore 1 mm deep), located by the 28.00 (0/−0.05) and 5.15 (+0.15/−0.05) reference dimensions.

The left and right files are mirror images of each other, and the Hand 2.1 and Hand 2.2 files are identical because the palm mounting interface did not change between the two revisions. These files are for mechanical integration only — they are not needed for simulation, and `attachment/` sits outside the ROS2 package root at `body/`, so `colcon` does not install it. To simulate the hand already bolted to an arm, load the models under `body/`: they are rooted at the mount link `{l,r}_mount`.

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
