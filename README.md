# WUJI Description

WUJI 机器人官方模型描述包，提供多种格式的机器人模型文件，支持 ROS2、MuJoCo、MJX 和 Isaac Sim。

## 支持的模型

| 模型 | 格式 | 说明 |
|------|------|------|
| Hand | URDF, MJCF, MJX, USD | 五指灵巧手（左/右） |

## 安装

### 方式一：Sparse Checkout（推荐，仅下载单个模型）

```bash
git clone --filter=blob:none --sparse https://github.com/wuji-technology/wuji-description.git
cd wuji-description
git sparse-checkout set robots/hand
```

### 方式二：完整克隆

```bash
git clone https://github.com/wuji-technology/wuji-description.git
```

### 方式三：ROS2 Workspace

```bash
cd ~/ros2_ws/src
git clone https://github.com/wuji-technology/wuji-description.git
cd ..
colcon build --packages-select wuji_description
source install/setup.bash
```

## 使用方法

### ROS2 + RViz 可视化

```bash
# 查看右手模型
ros2 launch wuji_description view_hand.launch.py hand:=right

# 查看左手模型
ros2 launch wuji_description view_hand.launch.py hand:=left

# 无 GUI 模式
ros2 launch wuji_description view_hand.launch.py gui:=false
```

### MuJoCo

```python
import mujoco

# 加载右手模型
model = mujoco.MjModel.from_xml_path("robots/hand/mjcf/right.xml")
data = mujoco.MjData(model)

# 仿真
for _ in range(1000):
    mujoco.mj_step(model, data)
```

### MJX (JAX 加速)

```python
import mujoco
from mujoco import mjx
import jax

# 加载 MJX 优化模型
model = mujoco.MjModel.from_xml_path("robots/hand/mjx/right_mjx.xml")
mjx_model = mjx.put_model(model)
mjx_data = mjx.make_data(mjx_model)

# JIT 编译
@jax.jit
def step(model, data):
    return mjx.step(model, data)

# 仿真
for _ in range(1000):
    mjx_data = step(mjx_model, mjx_data)
```

### Isaac Sim

```python
from omni.isaac.core.utils.stage import add_reference_to_stage

# 加载 USD 模型
add_reference_to_stage("robots/hand/usd/right.usd", "/World/RightHand")
```

## 目录结构

```
wuji-description/
├── robots/
│   └── hand/
│       ├── urdf/           # ROS2 兼容 URDF
│       │   ├── left.urdf
│       │   └── right.urdf
│       ├── mjcf/           # MuJoCo XML
│       │   ├── left.xml
│       │   └── right.xml
│       ├── mjx/            # MJX 优化版（简化碰撞体）
│       │   ├── left_mjx.xml
│       │   └── right_mjx.xml
│       ├── usd/            # Isaac Sim USD
│       │   ├── left.usd
│       │   └── right.usd
│       └── meshes/         # STL 网格文件
│           ├── left/
│           └── right/
├── launch/                 # ROS2 启动文件
├── rviz/                   # RViz 配置
├── CMakeLists.txt          # ROS2 构建
└── package.xml             # ROS2 包定义
```

## 模型规格

### Hand（五指灵巧手）

| 参数 | 值 |
|------|------|
| 自由度 | 20 DOF（每手） |
| 关节类型 | 旋转关节 |
| 驱动方式 | 位置控制（PD） |
| 碰撞组 | palm, link1-4, tip |

## 许可证

Apache-2.0

## 链接

- [GitHub Issues](https://github.com/wuji-technology/wuji-description/issues)
- [WUJI Technology](https://wuji.tech)
