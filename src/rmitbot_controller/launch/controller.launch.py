# ros2 launch rmitbot_controller controller.launch.py is_sim:=true

import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import UnlessCondition

from launch_ros.actions import Node

def generate_launch_description():
    # ==========================================
    # 1. Capture the 'is_sim' configuration
    is_sim = LaunchConfiguration('is_sim')

    # ==========================================
    # 2. Declare the launch argument (this shows up in --help)
    declare_is_sim_arg = DeclareLaunchArgument(
        'is_sim',
        default_value='false',
        description='Use Gazebo or hardware interface'
    )

    # ==========================================
    # 3. Controller Manager
    ctrl_dir = get_package_share_directory("rmitbot_controller")
    ctrl_config = os.path.join(ctrl_dir, 'config', 'rmitbot_controller.yaml')


    # ==========================================
    # 4. Compile xacro file
    urdf_dir = get_package_share_directory("rmitbot_description")
    urdf_file = os.path.join(urdf_dir, 'urdf', 'rmitbot.urdf.xacro')
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file, ' is_sim:=', is_sim, ' controller_yaml:=', ctrl_config,]),
        value_type=str
    )

    # ==========================================
    # 4. Controller Manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        condition=UnlessCondition(is_sim),
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": is_sim},
                    ctrl_config,
                    ],
    )

    # ==========================================
    # 5. joint_state_broadcaster (jsb): position, velocity from the robot hardware
    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{"use_sim_time": is_sim}]  # Sync clock
    )

    # ==========================================
    # 6. Controller 
    controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            'diff_drive_controller', '--param-file', ctrl_config, 
            '--controller-ros-args','-r /diff_drive_controller/cmd_vel:=/cmd_vel',
            '--controller-ros-args','-r /diff_drive_controller/odom:=/odom',],
        parameters=[{"use_sim_time": is_sim}]  # Sync clock
    )

    # controller must be spawned after the jsb
    controller_spawner_delayed = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=jsb_spawner,
            on_exit=[controller_spawner],
        )
    )

    # ==========================================
    # 7. IMU
    imu_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            'imu_sensor_broadcaster',
            '--param-file', ctrl_config,
            "--controller-ros-args", "-r /imu_sensor_broadcaster/imu:=/imu/data",
        ],
        parameters=[{"use_sim_time": is_sim}]  # Sync clock
    )

    imu_broadcaster_delayed = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=controller_spawner,
            on_exit=[imu_broadcaster],
        )
    )
    
    # ==========================================
    # 8. Twiststamper
    twist_stamper_node = Node( 
            package=    'twist_stamper', 
            executable= 'twist_stamper', 
            name=       'twist_stamper_foxglove', 
            parameters=[ 
                {'frame_id': 'base_footprint'},  
                {"use_sim_time": is_sim}, ],  
            remappings=[ 
                ('/cmd_vel_in', '/cmd_vel_foxglove_unstamped'), 
                ('/cmd_vel_out','/cmd_vel_foxglove'), 
                # ('/cmd_vel_in', '/cmd_vel_foxglove_unstamped'), 
                # ('/cmd_vel_out','/cmd_vel'), 
                ],  
        ) 
    
    # ==========================================
    # 9. Twist Mux
    twistmux_params = os.path.join(get_package_share_directory("rmitbot_controller"), "config", "twistmux.yaml") 
    twistmux_node = Node( 
        package=    'twist_mux', 
        executable= 'twist_mux', 
        name=       'twist_mux_node', 
        output='screen', 
        parameters=[
            twistmux_params,  
            {"use_sim_time": is_sim},
        ], 
        remappings=[ 
            ('/cmd_vel_out', '/cmd_vel')], 
    ) 

    # ==========================================
    return LaunchDescription(
        [
            declare_is_sim_arg,
            controller_manager,
            jsb_spawner,
            controller_spawner_delayed,
            imu_broadcaster_delayed,
            twist_stamper_node, 
            twistmux_node, 
        ]
    )
