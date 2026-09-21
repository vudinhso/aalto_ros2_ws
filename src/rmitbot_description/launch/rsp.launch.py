import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration

# Launch the file
# ros2 launch rmitbot_description rsp.launch.py is_sim:=true

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
    # 3. Compile xacro file
    rmit_dir = get_package_share_directory('rmitbot_description')
    urdf_file = os.path.join(rmit_dir, 'urdf', 'rmitbot.urdf.xacro')
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file, ' is_sim:=', is_sim]), 
        value_type=str
    )
    
    # ==========================================
    # 4. rsp node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"use_sim_time": is_sim, 
                     "robot_description": robot_description}],
        )
    
    # ==========================================
    return LaunchDescription([
        declare_is_sim_arg,
        robot_state_publisher, 
    ])