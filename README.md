# wuji-description

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/wuji-technology/wuji-description)](https://github.com/wuji-technology/wuji-description/releases)

Robot model description package for the Wuji Hand and related accessories. Provides URDF, MuJoCo (MJCF), and USD assets for simulation and visualization, plus STEP/CAD files for mechanical integration. Includes a ROS2 launch and RViz configuration for quick inspection of left and right hand models.

**Get started with [Quick Start](#quick-start). For detailed documentation, refer to [Wuji Hand Description Guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/wuji-hand-description-guide/) on Wuji Docs Center.**

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
│   │   ├── meshes/{left,right}/             // STL meshes, incl. soft-pad and simplified collision meshes
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
│   └── body/                                // Wuji Hand 2 model
│       ├── meshes/{left,right}/             // STL meshes with anatomical names (thumb, index_finger, ...)
│       ├── mjcf/{left,right}.xml            // MuJoCo XML models
│       ├── urdf/{left,right}.urdf           // URDF models (plus {left,right}-ros.urdf with package:// paths)
│       └── usd/{left,right}/                // Isaac Sim USD assets
├── glove/
│   └── body/                                // Wuji Glove model (hand motion tracking)
│       ├── urdf/{left,right}.urdf           // URDF skeletons (21 revolute DOF per hand)
│       ├── mesh/base_link_{TX,RX}.STL       // Transmitter base and fingertip receiver coil
│       └── step/EMFTXC_topcover.{step,pdf}  // Transmitter top-cover STEP and assembled drawing
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

`hand/body-with-soft/` is a variant of the hand body with a soft pad fixed to the thumb (`finger1_link2_softbody`). Every format also ships a `_simplified` variant that replaces the collision geometry of each finger's `link4` and the thumb soft pad with decimated meshes for faster contact simulation; visual geometry is identical.

```bash
# Full collision meshes
python -m mujoco.viewer --mjcf=hand/body-with-soft/mjcf/right.xml

# Simplified collision meshes
python -m mujoco.viewer --mjcf=hand/body-with-soft/mjcf/right_simplified.xml
```

For Isaac Sim, load `hand/body-with-soft/usd/{left,right}/wujihand.usd` or the `{left,right}_simplified` counterparts.

### Wuji Hand 2

`hand2/body/` provides the Wuji Hand 2 model. Each hand has 20 revolute joints named after hand anatomy (for example `r_thumb_cmc_flex`, `r_index_finger_mcp_abd`, `r_middle_finger_pip`), with URDF models in relative-path (`hand2/body/urdf/{left,right}.urdf`) and `package://` (`{left,right}-ros.urdf`) variants, MuJoCo XML models at `hand2/body/mjcf/{left,right}.xml`, Isaac Sim USD assets at `hand2/body/usd/{left,right}/`, and STL meshes at `hand2/body/meshes/{left,right}/`.

Preview in MuJoCo:

```bash
python -m mujoco.viewer --mjcf=hand2/body/mjcf/right.xml
```

For Isaac Sim, load `hand2/body/usd/{left,right}/wujihand.usd` directly.

URDF preview with a non-ROS viewer such as `urdf-viz`:

```bash
urdf-viz hand2/body/urdf/right.urdf
```

### Hand Attachments

`hand/attachment/` ships optional components for the Wuji Hand. They are not loaded by the default display launch file; attach them via a fixed joint when composing a full robot description.

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

`glove/body/` provides the Wuji Glove model used for hand motion tracking. Each hand is described by a URDF skeleton (`glove/body/urdf/{left,right}.urdf`) with 21 revolute joints across the five fingers, an electromagnetic transmitter base on the wrist (`base_link_TX.STL`), and a receiver coil on every fingertip (`base_link_RX.STL`). The transmitter top-cover STEP file and assembled drawing are under `glove/body/step/`.

Preview a glove model with a non-ROS URDF viewer such as `urdf-viz`:

```bash
urdf-viz glove/body/urdf/right.urdf
```

## Contact

For any questions, please contact [support@wuji.tech](mailto:support@wuji.tech).
