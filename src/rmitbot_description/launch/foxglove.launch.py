import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# use docker container: sudo docker run --name foxglove_web -d --restart unless-stopped -p 8080:8080 ghcr.io/lichtblick-suite/lichtblick:latest
# ros2 launch rmitbot_description foxglove.launch.py
# connect to http://127.0.0.1:8080/

def generate_launch_description():
    # Replace with your actual package name where config/foxglove_bridge.yaml lives
    rmit_dir = get_package_share_directory('rmitbot_description')

    foxglove_config_path = os.path.join(
        rmit_dir,
        'config',
        'foxglove.yaml'
    )

    config_file_arg = DeclareLaunchArgument(
        'foxglove_config',
        default_value=foxglove_config_path,
        description='Full path to the foxglove_bridge YAML parameters file'
    )

    foxglove_node = Node(
        package='foxglove_bridge',
        executable='foxglove_bridge',
        name='foxglove_bridge',
        output='screen',
        parameters=[LaunchConfiguration('foxglove_config')]
    )

    return LaunchDescription([
        config_file_arg,
        foxglove_node
    ])