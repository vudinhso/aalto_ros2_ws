# ros2 launch rmitbot_bringup rpi.launch.py

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    rsp_launch =        os.path.join(get_package_share_directory("rmitbot_description"),"launch", "rsp.launch.py")
    foxglove_launch =   os.path.join(get_package_share_directory("rmitbot_description"),"launch", "foxglove.launch.py")
    ctrl_launch =       os.path.join(get_package_share_directory("rmitbot_controller"),"launch", "controller.launch.py")
    ekf_launch =        os.path.join(get_package_share_directory("rmitbot_localization"),"launch","localization.launch.py"),
    rplidar_launch =    os.path.join(get_package_share_directory("rmitbot_mapping"),"launch", "rplidar.launch.py")
    slam_launch =       os.path.join(get_package_share_directory("rmitbot_mapping"),"launch", "slam.launch.py")
    nav2_launch =       os.path.join(get_package_share_directory("rmitbot_navigation"),"launch","nav.launch.py")

    rsp =           IncludeLaunchDescription(rsp_launch)
    foxglove =      IncludeLaunchDescription(foxglove_launch)
    controller =    IncludeLaunchDescription(ctrl_launch)    
    localization =  IncludeLaunchDescription(ekf_launch)
    rplidar =       IncludeLaunchDescription(rplidar_launch)    
    slamtoolbox =   IncludeLaunchDescription(slam_launch)
    navigation =    IncludeLaunchDescription(nav2_launch)
    
    navigation_delayed = TimerAction(
        period = 5., 
        actions=[navigation]
    )

    return LaunchDescription([
        rsp, 
        foxglove, 
        controller,
        localization,
        rplidar, 
        slamtoolbox, 
        navigation_delayed, 
    ])