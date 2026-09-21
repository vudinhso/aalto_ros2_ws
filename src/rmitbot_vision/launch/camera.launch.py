# Launch this file for using the camera hardware
# ros2 launch rmitbot_vision camera.launch.py
# check connected camera: v4l2-ctl --list-devices

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    # 1. Path to your calibration file
    # Ensure ost.yaml is in your package's config folder
    pkg_share = get_package_share_directory('rmitbot_vision')
    calib_file_path = 'file://' + \
        os.path.join(pkg_share, 'config', 'ostwebcam.yaml')
    camera_config = os.path.join(pkg_share, 'config', 'camera_param.yaml')

    camera_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_cam_node_exe',
        output='screen',
        parameters=[
            camera_config,
            {'camera_info_url': calib_file_path, }
        ],
    )

    return LaunchDescription([
        camera_node,
    ])
