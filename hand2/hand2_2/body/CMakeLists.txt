cmake_minimum_required(VERSION 3.10)
project(wuji_hand2_2_description)

find_package(ament_cmake REQUIRED)

# Asset-only package: URDF references resolve as
# package://wuji_hand2_2_description/meshes/{left,right}/<link>.STL
# A distinct package name per revision (Hand 2.1: wuji_hand2_1_description,
# Hand 2.2: wuji_hand2_2_description) so revisions can coexist in one workspace.
#
# This package provides left and right models without covers, rooted at the
# arm-flange mount {l,r}_mount. Hardware meshes live in meshes/{left,right}/.
# Keep each usd/{left,right}/ directory intact.
# Mechanical mounting-interface files live in ../attachment/ outside this
# package root and are not installed by this rule.
install(
    DIRECTORY meshes mjcf urdf usd
    DESTINATION share/${PROJECT_NAME}
)

ament_package()
