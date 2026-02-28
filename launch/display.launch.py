"""WUJI Description RViz Display Launch File.

Launch robot_state_publisher and RViz for visualizing WUJI robot models.

Usage:
    ros2 launch wuji_description display.launch.py robot:=left
    ros2 launch wuji_description display.launch.py robot:=right
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot",
            default_value="left",
            description="Robot model to display (left or right)",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_gui",
            default_value="true",
            description="Use joint_state_publisher_gui",
        )
    )

    # Initialize arguments
    robot = LaunchConfiguration("robot")
    use_gui = LaunchConfiguration("use_gui")

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("wuji_description"),
                    "robots",
                    "hand",
                    "urdf",
                    PythonExpression(["'", robot, "-ros.urdf'"]),
                ]
            ),
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # RViz config path (use left.rviz or right.rviz based on robot arg)
    rviz_config_file = PathJoinSubstitution(
        [
            FindPackageShare("wuji_description"),
            "rviz",
            PythonExpression(["'", robot, ".rviz'"]),
        ]
    )

    # Nodes
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        condition=IfCondition(use_gui),
    )

    joint_state_publisher_node_no_gui = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        condition=UnlessCondition(use_gui),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    nodes = [
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_node_no_gui,
        rviz_node,
    ]

    return LaunchDescription(declared_arguments + nodes)
