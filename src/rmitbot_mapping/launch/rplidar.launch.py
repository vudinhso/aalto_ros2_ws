import os
from launch import LaunchDescription
from launch_ros.actions import Node

# ros2 launch rmitbot_mapping rplidar.launch.py

def generate_launch_description():
    # ==========================================
    # 1. Launch Lidar hardware
    rplidar = Node(
        package=    'rplidar_ros',
        executable= 'rplidar_composition',
        output=     'screen',
        parameters=[{
            # 'serial_port': '/dev/ttyUSB1',
            'serial_port': '/dev/rplidar',
            'frame_id': 'lidar_link',
            'angle_compensate': True,
            'scan_mode': 'Standard',
            'use_sim_time': False,
        }]
    )

    return LaunchDescription([
        rplidar, 
    ])
