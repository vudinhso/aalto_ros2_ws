# ros2 launch rmitbot_mapping slam.launch.py use_sim_time:=true

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

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
    # 3. Slamtoolbox
    slam_dir = get_package_share_directory('slam_toolbox')
    rmit_dir = get_package_share_directory("rmitbot_mapping")
    slam_launch = os.path.join(slam_dir,"launch","online_async_launch.py")
    slam_config = os.path.join(rmit_dir, "config", "slam.yaml")
    
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch),
        launch_arguments={
            'use_sim_time': is_sim, 
            'params_file':  slam_config,
            }.items()
    )
    
    return LaunchDescription([
        declare_is_sim_arg, 
        slam,
    ])
    