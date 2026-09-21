from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
import os

def generate_launch_description():
    # ==========================================
    # 1. Capture the 'is_sim' configuration
    is_sim = LaunchConfiguration('is_sim')

    # ==========================================
    # 2. Declare the launch argument (this shows up in --help)
    declare_is_sim_arg = DeclareLaunchArgument(
        'is_sim',
        default_value=  'false',
        description=    'Use Gazebo or hardware interface'
    )
    
    # ==========================================
    # 3. EKF
    rmit_dir = get_package_share_directory('rmitbot_localization')
    ekf_config = os.path.join(rmit_dir, 'config', 'ekf.yaml')
    robot_localization = Node(
        package=    "robot_localization",
        executable= "ekf_node",
        name=       "ekf_filter_node",
        output=     "screen",
        parameters=[
            ekf_config, 
            {'use_sim_time': is_sim},
            ],
        remappings=[('/odometry/filtered', '/odom_ekf')], 
    )

    return LaunchDescription([
        declare_is_sim_arg, 
        robot_localization,
    ])