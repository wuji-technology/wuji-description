cmake_minimum_required(VERSION 3.10)
project(wuji_hand2_description)

find_package(ament_cmake REQUIRED)

# Asset-only package: URDF references resolve as
# package://wuji_hand2_description/meshes/{left,right}/<link>.STL
install(
    DIRECTORY meshes mjcf step urdf usd
    DESTINATION share/${PROJECT_NAME}
)

ament_package()
