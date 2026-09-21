# Launch this file for navigation
# ros2 launch rmitbot_navigation nav.launch.py

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    is_sim = LaunchConfiguration('is_sim')
    declare_is_sim_arg = DeclareLaunchArgument(
            'is_sim',
            default_value='false',
            description='Use Gazebo or hardware interface'
        )
    
    nav_pkg_path = get_package_share_directory("rmitbot_navigation")
    nav_config_file = os.path.join(nav_pkg_path, 'config', 'agbot_nav2_rpp.yaml')
    
    nav2_dir = get_package_share_directory('nav2_bringup')
    rmit_dir = get_package_share_directory('rmitbot_navigation')
    nav2_launch = os.path.join(nav2_dir, 'launch', 'navigation_launch.py')
    nav2_config = os.path.join(rmit_dir, 'config', 'nav2_params.yaml')

    nav2_planner = Node(
        package=    'nav2_planner',
        executable= 'planner_server',
        name=       'planner_server',
        output=     'screen',
        parameters=[{'use_sim_time': True}, nav2_config]
    )
    
    nav2_controller = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[{'use_sim_time': is_sim}, nav2_config,],
        remappings=[('/cmd_vel', '/cmd_vel_navigation_unstamped')],
    )
        
    nav2_bt_navigator = Node(
        package=    'nav2_bt_navigator',
        executable= 'bt_navigator',
        name=       'bt_navigator',
        output=     'screen',
        parameters=[{'use_sim_time': is_sim}, nav2_config]
    )
    
    nav2_behavior_server = Node(
        package=    'nav2_behaviors',
        executable= 'behavior_server',
        name=       'behavior_server',
        output=     'screen',
        parameters=[{'use_sim_time': is_sim}, nav2_config], 
        remappings=[('/cmd_vel', '/cmd_vel_navigation_unstamped')]
    )
    
    nav2_smoother_server = Node(
        package=    'nav2_smoother',
        executable= 'smoother_server',
        name=       'smoother_server',
        output=     'screen',
        parameters=[{'use_sim_time': is_sim}, nav2_config]
    )

    nav2_lifecycle_manager = Node(
        package=    'nav2_lifecycle_manager',
        executable= 'lifecycle_manager',
        name=       'lifecycle_manager_navigation',
        output=     'screen',
        parameters=[{
            'use_sim_time': is_sim,
            'autostart': True,
            'node_names': [
                'planner_server',
                'controller_server',
                'bt_navigator', 
                'behavior_server', 
                'smoother_server', 
            ]
        }]
    )
    
    twist_stamper_node = Node( 
        package=    'twist_stamper', 
        executable= 'twist_stamper', 
        name=       'twist_stamper_navigation', 
        parameters=[ 
            {'frame_id': 'base_footprint'},  
            {"use_sim_time": is_sim}, ],  
        remappings=[ 
            ('/cmd_vel_in', '/cmd_vel_navigation_unstamped'), 
            ('/cmd_vel_out','/cmd_vel_navigation'), ],  
    ) 
    
    return LaunchDescription([ 
        declare_is_sim_arg, 
        nav2_planner, 
        nav2_controller,
        nav2_bt_navigator, 
        nav2_behavior_server,
        nav2_smoother_server, 
        nav2_lifecycle_manager, 
        twist_stamper_node, 
        ])