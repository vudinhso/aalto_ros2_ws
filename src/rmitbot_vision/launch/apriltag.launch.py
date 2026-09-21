import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

# ros2 launch rmitbot_vision apriltag.launch.py


def generate_launch_description():
    image_proc_node = Node(
        package="image_proc",
        executable="rectify_node",
        name="rectify_node",
        # namespace="camera",   # so it uses /camera/image and /camera/camera_info
        output="screen",
        remappings=[
            ('/image', '/camera/image'),
            ('/camera_info', '/camera/camera_info'),
            ('/image_rect', '/camera_image_rect'),],
    )

    apriltag_params = os.path.join(get_package_share_directory(
        "rmitbot_vision"), "config", "apriltag_params.yaml")
    apriltag_node = Node(
        package='apriltag_ros',
        executable='apriltag_node',
        name='apriltag_node',
        output='screen',
        parameters=[
            apriltag_params,
            {"use_sim_time": False},
        ],
        remappings=[
            # ("image_rect", "/image_raw"),
            # ("camera_info", "/camera_info"),
            ("image_rect", "/camera/image"),
            ("camera_info", "/camera/camera_info"),
        ],
    )

    tf_apriltag_0 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        # arguments=['3.8', '2.0', '0.5', '-1.5708', '0.0', '1.5708', 'map', 'apriltag_0']
        arguments=[
                '--x', '3.8','--y', '2.0','--z', '0.5',
                '--yaw', '-1.5708','--pitch', '0.0','--roll', '1.5708',
                '--frame-id', 'map','--child-frame-id', 'apriltag_0'
        ]
    )

    return LaunchDescription([
        # image_proc_node,
        apriltag_node,
        tf_apriltag_0,
    ])
