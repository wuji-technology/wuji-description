# wuji-description

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/wuji-technology/wuji-description)](https://github.com/wuji-technology/wuji-description/releases)

Robot model description package for WUJI robots. Provides URDF, MuJoCo (MJCF), MJX, and USD models with calibrated dynamics for simulation and visualization. Includes ROS2 launch files and RViz configuration.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [1. MuJoCo](#1-mujoco)
  - [2. MJX (JAX)](#2-mjx-jax)
  - [3. Isaac Sim](#3-isaac-sim)
  - [4. ROS2 and RViz](#4-ros2-and-rviz)
- [Model Specifications](#model-specifications)
- [Contact](#contact)

## Repository Structure

```text
wuji-description/
├── robots/
│   └── hand/
│       ├── urdf/           # URDF models
│       │   ├── left.urdf / right.urdf          # Relative paths (local tools)
│       │   └── left-ros.urdf / right-ros.urdf  # Package paths (ROS2)
│       ├── mjcf/           # MuJoCo XML
│       │   ├── left.xml
│       │   └── right.xml
│       ├── mjx/            # MJX optimized (simplified collision)
│       │   ├── left_mjx.xml
│       │   └── right_mjx.xml
│       ├── usd/            # Isaac Sim USD
│       │   ├── left.usd
│       │   └── right.usd
│       └── meshes/         # STL mesh files
│           ├── left/
│           └── right/
├── launch/                 # ROS2 launch files
├── rviz/                   # RViz configuration
├── CMakeLists.txt          # ROS2 build
└── package.xml             # ROS2 package definition
```

### Directory Description

| Directory | Description |
|-----------|-------------|
| `robots/hand/urdf/` | URDF files for left/right hands. `*.urdf` use relative paths for local tools; `*-ros.urdf` use package paths for ROS2. |
| `robots/hand/mjcf/` | MuJoCo XML model files for simulation. |
| `robots/hand/mjx/` | MJX-optimized models with simplified collision for JAX-accelerated simulation. |
| `robots/hand/usd/` | USD models for NVIDIA Isaac Sim. |
| `robots/hand/meshes/` | STL mesh files for visualization and collision. |
| `launch/` | Python launch scripts for RViz visualization. |
| `rviz/` | Default RViz configuration files. |

## Installation

### Option 1: Sparse Checkout (recommended, download single model only)

```bash
git clone --filter=blob:none --sparse https://github.com/wuji-technology/wuji-description.git
cd wuji-description
git sparse-checkout set robots/hand
```

### Option 2: Full Clone

```bash
git clone https://github.com/wuji-technology/wuji-description.git
```

### Option 3: ROS2 Workspace

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select wuji_description
source install/setup.bash
```

## Usage

### 1. MuJoCo

If you only want to view the model in MuJoCo, no ROS2 installation is needed.

```bash
pip install mujoco
```

#### View in MuJoCo Viewer

```bash
python -m mujoco.viewer --mjcf=robots/hand/mjcf/right.xml
```

#### Load in Python

```python
import mujoco

model = mujoco.MjModel.from_xml_path("robots/hand/mjcf/right.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    mujoco.mj_step(model, data)
```

### 2. MJX (JAX)

MJX-optimized models for hardware-accelerated simulation with JAX.

```python
import mujoco
from mujoco import mjx
import jax

model = mujoco.MjModel.from_xml_path("robots/hand/mjx/right_mjx.xml")
mjx_model = mjx.put_model(model)
mjx_data = mjx.make_data(mjx_model)

@jax.jit
def step(model, data):
    return mjx.step(model, data)

for _ in range(1000):
    mjx_data = step(mjx_model, mjx_data)
```

### 3. Isaac Sim

```python
from omni.isaac.core.utils.stage import add_reference_to_stage

add_reference_to_stage("robots/hand/usd/right.usd", "/World/RightHand")
```

### 4. ROS2 and RViz

After installing as a ROS2 package (see [Option 3](#option-3-ros2-workspace)):

```bash
# Visualize left hand (default)
ros2 launch wuji_description display.launch.py

# Visualize right hand
ros2 launch wuji_description display.launch.py robot:=right

# Without GUI
ros2 launch wuji_description display.launch.py use_gui:=false
```

## Model Specifications

### Hand

| Parameter | Value |
|-----------|-------|
| DOF | 20 per hand |
| Joint type | Revolute |
| Actuation | Position control (PD) |
| Collision groups | palm, link1-4, tip |

## License

[MIT](LICENSE)

## Contact

For any questions, please contact [support@wuji.tech](mailto:support@wuji.tech).
