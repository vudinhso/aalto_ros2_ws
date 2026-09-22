# ros2 launch rmitbot_bringup sim.launch.py

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    rsp_launch =        os.path.join(get_package_share_directory("rmitbot_description"),"launch", "rsp.launch.py")
    foxglove_launch =   os.path.join(get_package_share_directory("rmitbot_description"),"launch", "foxglove.launch.py")
    gsim_launch =       os.path.join(get_package_share_directory("rmitbot_gazebosim"),"launch", "gazebo.launch.py")
    ctrl_launch =       os.path.join(get_package_share_directory("rmitbot_controller"),"launch", "controller.launch.py")
    ekf_launch =        os.path.join(get_package_share_directory("rmitbot_localization"),"launch","localization.launch.py"),
    slam_launch =       os.path.join(get_package_share_directory("rmitbot_mapping"),"launch", "slam.launch.py")
    nav2_launch =       os.path.join(get_package_share_directory("rmitbot_navigation"),"launch","nav.launch.py")

    rsp =           IncludeLaunchDescription(rsp_launch, launch_arguments={'is_sim': 'true',}.items())
    foxglove =      IncludeLaunchDescription(foxglove_launch, launch_arguments={'is_sim': 'true',}.items())
    controller =    IncludeLaunchDescription(ctrl_launch, launch_arguments={'is_sim': 'true',}.items())
    localization =  IncludeLaunchDescription(ekf_launch,launch_arguments={'is_sim': 'true',}.items())
    slamtoolbox =   IncludeLaunchDescription(slam_launch,launch_arguments={'is_sim': 'true',}.items())
    navigation =    IncludeLaunchDescription(nav2_launch,launch_arguments={'is_sim': 'true',}.items())
    
    gz_sim = ExecuteProcess(
        cmd=['xvfb-run', '-a', 'ros2', 'launch', 'rmitbot_gazebosim', 'gazebo.launch.py', 'is_sim:=true'],
        output='screen'
    )
    
    nav_delayed = TimerAction(
        period = 5., 
        actions=[navigation]
    )
    
    return LaunchDescription([
        rsp, 
        foxglove, 
        gz_sim, 
        controller,
        localization,
        slamtoolbox, 
        nav_delayed, 
    ])