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
│   ├── hand2_beta1/
│   │   ├── body/                            // ROS2 package wuji_hand2_beta1_description: Wuji Hand 2 (Beta 1), coordinate conventions frozen
│   │   │   ├── meshes/{left,right}/         // STL meshes with anatomical names (+ {l,r}_mount.STL for the with-mount variant)
│   │   │   ├── mjcf/{left,right}.xml        // MuJoCo XML models (plus {left,right}_with_mount.xml)
│   │   │   ├── step/                        // Full-hand STEP CAD assemblies
│   │   │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// and _with_mount variants)
│   │   │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2.usd; plus {left,right}_with_mount/)
│   │   │   ├── CMakeLists.txt               // ROS2 package install rules
│   │   │   └── package.xml                  // ROS2 package manifest
│   │   └── attachment/                      // Palm mounting-interface STEP + A3 dimensioned drawing, one pair per hand
│   └── hand2_beta2/
│       ├── body/                            // ROS2 package wuji_hand2_beta2_description: Wuji Hand 2 (Beta 2), Beta 1 + one tactile sensor pad per fingertip
│       │   ├── meshes/{left,right}/         // STL meshes with anatomical names (+ tip sensor pads, + {l,r}_mount.STL)
│       │   ├── mjcf/{left,right}.xml        // MuJoCo XML models (plus {left,right}_with_mount.xml)
│       │   ├── step/                        // Full-hand with-mount STEP CAD assemblies
│       │   ├── urdf/{left,right}.urdf       // URDF models (plus -ros.urdf package:// and _with_mount variants)
│       │   ├── usd/{left,right}/            // Isaac Sim USD assets (layered wujihand2_beta2.usd; plus {left,right}_with_mount/)
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

### Wuji Hand 2 (Beta 1)

`hand2/hand2_beta1/body/` provides the Wuji Hand 2 (Beta 1) model — the first revision with the coordinate conventions frozen: anatomical link/joint naming (for example `r_thumb_cmc_flex`, `r_index_finger_mcp_abd`, `r_middle_finger_pip`), integer unit joint axes, and the `{l,r}_wrist` root link are fixed from this revision on. Later revisions stay compatible and only update physical parameters and geometry details. Each hand has 20 actuated revolute joints (5 fingers × 4 joints) and five fingertip query sites (`{l,r}_{finger}_tip`).

Shipped formats:

- URDF models in relative-path (`hand2/hand2_beta1/body/urdf/{left,right}.urdf`) and `package://` (`{left,right}-ros.urdf`) variants
- MuJoCo XML models at `hand2/hand2_beta1/body/mjcf/{left,right}.xml` — convex-hull collision geometry, every link collides, with 10 assembly-overlap pairs excluded
- Layered Isaac Sim USD assets at `hand2/hand2_beta1/body/usd/{left,right}/`
- Anatomically named STL meshes at `hand2/hand2_beta1/body/meshes/{left,right}/`
- A with-mount variant of every model format, for the hand already bolted to an arm (see below)

Known Beta limitations: the fingertip soft-pad meshes (`*_tip.STL`) ship with the package but are not attached as collision geometry yet, and the kp/kv drive gains are carried over from the Wuji Hand platform calibration pending Wuji Hand 2 system identification.

Preview in MuJoCo (press 1/2 to toggle the visual/collision display groups):

```bash
python -m mujoco.viewer --mjcf=hand2/hand2_beta1/body/mjcf/right.xml
```

For Isaac Sim, load `hand2/hand2_beta1/body/usd/{left,right}/wujihand2.usd` directly (or `usd/{left,right}_with_mount/wujihand2.usd` for the with-mount variant). Each `usd/<variant>/` folder is one self-contained unit — don't split it. Drive gains are configured so the hand holds its pose on bare Play. At runtime they are overridden by your ArticulationCfg.

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand2/hand2_beta1/body/urdf/right.urdf
```

#### Assembly variants

Each hand ships in two assembly variants, side by side in the same package directory and told apart by a `_with_mount` filename suffix:

| | Root link | URDF | MuJoCo | Isaac Sim |
|---|---|---|---|---|
| No-mount | `{l,r}_wrist` | `urdf/{left,right}.urdf`, `{left,right}-ros.urdf` | `mjcf/{left,right}.xml` | `usd/{left,right}/` |
| With-mount | `{l,r}_mount` | `urdf/{left,right}_with_mount.urdf`, `{left,right}_with_mount-ros.urdf` | `mjcf/{left,right}_with_mount.xml` | `usd/{left,right}_with_mount/` |

The with-mount variant adds the arm-flange mount link (`{l,r}_mount`, 69 g) as the model root, with the wrist shell fixed-welded onto it via `{l,r}_wrist_fixed`. Use it to bolt the hand onto an arm, and the no-mount model when the wrist is the attachment point. Joint names, axes, limits and actuators are identical between the variants, and both `-ros.urdf` files resolve meshes through the same `package://wuji_hand2_beta1_description/meshes/...` prefix — so one installed package serves both, and either can be loaded at any time.

The variants share all 26 hand meshes in `meshes/{left,right}/` byte for byte; the with-mount variant adds only `{l,r}_mount.STL`, bringing each directory to 27. The variants stay kinematically equivalent: with the fixed mount offset taken out, their fingertip poses agree to within 0.006 mm, so which variant you load does not change where the fingers go.

#### ROS2

`hand2/hand2_beta1/body/` is a standalone ROS2 package (`wuji_hand2_beta1_description`). Its `{left,right}-ros.urdf` reference meshes via `package://wuji_hand2_beta1_description/meshes/...`, independent of the Wuji Hand `wuji_description` package:

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
colcon build --packages-select wuji_hand2_beta1_description
source install/setup.bash

# Verify resolution, then load from your own launch file / robot_state_publisher
check_urdf $(ros2 pkg prefix wuji_hand2_beta1_description)/share/wuji_hand2_beta1_description/urdf/right-ros.urdf
```

#### STEP Files

`hand2/hand2_beta1/body/step/` ships full-hand CAD assemblies of the Beta 1 revision (`wuji-hand2-description-{left,right}_beta1_with_mount_step.STEP`) for mechanical integration and fixture design (not required for simulation).

### Wuji Hand 2 (Beta 2)

`hand2/hand2_beta2/body/` provides the Wuji Hand 2 (Beta 2) model. It keeps the frozen Beta 1 coordinate contract unchanged — the same 20 actuated revolute joints (5 fingers × 4 joints), integer unit joint axes, anatomical link/joint naming, and `{l,r}_wrist` root link — and adds one tactile-sensor pad link per fingertip (`{l,r}_{finger}_tip_sensor_frame`, fixed-welded onto the distal segment, shown light blue against the silver body). The five fingertip query sites (`{l,r}_{finger}_tip`, MJCF `<site>` elements in display group 3) carry over from Beta 1 unchanged. The robot names are `wujihand2-beta2-{left,right}`.

Shipped formats:

- URDF models in relative-path (`hand2/hand2_beta2/body/urdf/{left,right}.urdf`) and `package://` (`{left,right}-ros.urdf`) variants
- MuJoCo XML models at `hand2/hand2_beta2/body/mjcf/{left,right}.xml` — convex-hull collision geometry, every link collides, with 10 assembly-overlap pairs excluded
- Layered Isaac Sim USD assets at `hand2/hand2_beta2/body/usd/{left,right}/` (entry point `wujihand2_beta2.usd`)
- Anatomically named STL meshes at `hand2/hand2_beta2/body/meshes/{left,right}/`, including the fingertip sensor pads
- A with-mount variant of every model format, for the hand already bolted to an arm (see below)
- Full-hand with-mount STEP CAD assemblies at `hand2/hand2_beta2/body/step/`

Preview in MuJoCo (press 1/2 to toggle the visual/collision display groups):

```bash
python -m mujoco.viewer --mjcf=hand2/hand2_beta2/body/mjcf/right.xml
```

For Isaac Sim, load `hand2/hand2_beta2/body/usd/{left,right}/wujihand2_beta2.usd` directly (or `usd/{left,right}_with_mount/wujihand2_beta2.usd` for the with-mount variant). Each `usd/<variant>/` folder is one self-contained unit — don't split it.

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand2/hand2_beta2/body/urdf/right.urdf
```

#### Assembly variants

As with Beta 1, each hand ships in two assembly variants side by side in the same package directory, told apart by a `_with_mount` filename suffix:

| | Root link | URDF | MuJoCo | Isaac Sim |
|---|---|---|---|---|
| No-mount | `{l,r}_wrist` | `urdf/{left,right}.urdf`, `{left,right}-ros.urdf` | `mjcf/{left,right}.xml` | `usd/{left,right}/` |
| With-mount | `{l,r}_mount` | `urdf/{left,right}_with_mount.urdf`, `{left,right}_with_mount-ros.urdf` | `mjcf/{left,right}_with_mount.xml` | `usd/{left,right}_with_mount/` |

The with-mount variant adds the arm-flange mount link (`{l,r}_mount`, 69 g) as the model root, with the wrist shell fixed-welded onto it via `{l,r}_wrist_fixed`. Joint names, axes, limits and actuators are identical between the variants, and both `-ros.urdf` files resolve meshes through the same `package://wuji_hand2_beta2_description/meshes/...` prefix, so one installed package serves both. The two variants share all 31 hand meshes byte for byte; the with-mount variant adds only `{l,r}_mount.STL`, bringing `meshes/{left,right}/` to 32 meshes per hand.

#### ROS2

`hand2/hand2_beta2/body/` is a standalone ROS2 package (`wuji_hand2_beta2_description`) — a distinct package name from Beta 1's `wuji_hand2_beta1_description`, so both revisions can coexist in one workspace. Its `{left,right}-ros.urdf` reference meshes via `package://wuji_hand2_beta2_description/meshes/...`:

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
colcon build --packages-select wuji_hand2_beta2_description
source install/setup.bash

# Verify resolution, then load from your own launch file / robot_state_publisher
check_urdf $(ros2 pkg prefix wuji_hand2_beta2_description)/share/wuji_hand2_beta2_description/urdf/right-ros.urdf
```

### Wuji Hand 2 Palm Mounting Interface

`hand2/hand2_beta1/attachment/` and `hand2/hand2_beta2/attachment/` ship the palm mounting interface, for machining your own arm-side adapter or fixture. One pair of files per hand:

- `wuji-hand2-description-{left,right}-mount_beta{1,2}_step.STEP` — a STEP assembly of the palm together with its wire harness. This is the palm only, not the full hand; for the full-hand assembly use `body/step/`.
- `wuji-hand2-description-{left,right}-mount_beta{1,2}.pdf` — a single-page A3 drawing dimensioning the threaded holes your adapter bolts into: one M3×0.5 fine-pitch 6H hole (thread depth > 5.5 mm, ⌀4 (0/+0.05) counterbore 2.35 ±0.03 deep) and two M4×0.5 fine-pitch 6H holes (thread depth > 4 mm, ⌀7 (0/+0.06) counterbore 1 mm deep), located by the 28.00 (0/−0.05) and 5.15 (+0.15/−0.05) reference dimensions.

The left and right files are mirror images of each other, and the Beta 1 and Beta 2 files are identical because the palm mounting interface did not change between the two revisions. These files are for mechanical integration only — they are not needed for simulation, and `attachment/` sits outside the ROS2 package root at `body/`, so `colcon` does not install it. To simulate the hand already bolted to an arm, load the `_with_mount` model variants inside `hand2/hand2_beta1/body/` or `hand2/hand2_beta2/body/` instead.

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
