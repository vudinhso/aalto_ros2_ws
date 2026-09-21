import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Launch the file
# ros2 launch rmitbot_description display.launch.py

def generate_launch_description():
    rsp_launch       = os.path.join(get_package_share_directory("rmitbot_description"), "launch", "rsp.launch.py")
    foxbridge_launch = os.path.join(get_package_share_directory("rmitbot_description"), "launch", "foxglove.launch.py")

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_launch),
        launch_arguments={'is_sim': 'true', }.items()
    )
    
    foxbridge = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(foxbridge_launch),
    )

    jsp = Node(
            package=    'joint_state_publisher',
            executable= 'joint_state_publisher',
        )

    return LaunchDescription([
        rsp,
        foxbridge,
        jsp, 
    ])
