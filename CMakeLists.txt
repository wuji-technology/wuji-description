cmake_minimum_required(VERSION 3.8)
project(wuji_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install robot model directories
install(
  DIRECTORY robots/
  DESTINATION share/${PROJECT_NAME}/robots
)

# Install launch files
install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install rviz configs
install(
  DIRECTORY rviz/
  DESTINATION share/${PROJECT_NAME}/rviz
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
