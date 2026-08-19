cmake_minimum_required(VERSION 3.10)
project(wuji_hand2_beta2_description)

find_package(ament_cmake REQUIRED)

# Asset-only package: URDF references resolve as
# package://wuji_hand2_beta2_description/meshes/{left,right}/<link>.STL
# A distinct package name from Beta 1's wuji_hand2_beta1_description so both
# revisions can coexist in one workspace (their mesh sets differ — Beta 2
# adds the per-finger *_tip_sensor_frame pads).
#
# Both assembly variants live in these same directories, told apart by a
# _with_mount filename suffix (no-mount {left,right}.* rooted at {l,r}_wrist,
# with-mount {left,right}_with_mount.* rooted at {l,r}_mount; USD gets its own
# {left,right}_with_mount/ subdirectory since its entry filename is fixed). They
# share the 31 hand meshes; the with-mount variant adds only
# {l,r}_mount.STL. One install rule, no path escaping the package root,
# and both variants usable from a single installed package.
install(
    DIRECTORY meshes mjcf step urdf usd
    DESTINATION share/${PROJECT_NAME}
)

ament_package()
