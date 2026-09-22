# ros2 launch rmitbot_gazebosim gazebo.launch.py
# xvfb-run -a ros2 launch rmitbot_gazebosim gazebo.launch.py

import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue



def generate_launch_description():
    # Path to the package
    pkg_path_description =  get_package_share_directory("rmitbot_description")
    pkg_path_gazebosim =    get_package_share_directory("rmitbot_gazebosim")
    
    combined_path = ":".join([
    str(Path(pkg_path_description).parent.resolve()),
    str(Path(pkg_path_gazebosim).parent.resolve())
])
    
    # Path to the world file
    world_path = os.path.join(pkg_path_gazebosim, 'world', 'room_8x8.sdf')

    gz_resource_path = SetEnvironmentVariable(
    name="GZ_SIM_RESOURCE_PATH",
    value=combined_path
)
   
    # Launch Gazebo 
    gz_sim = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [os.path.join(get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
        launch_arguments={"gz_args": f"-s -r -v 1 {world_path}"}.items()
    )
    
    # Spawn the robot in Gazebo
    gz_spawn_entity = Node(
        package=    "ros_gz_sim",
        executable= "create",
        output=     "screen",
        arguments=["-topic", "robot_description","-name", "rmitbot"],
    )
    
    # Spawn AprilTag
    spawn_apriltag_0 = Node(
        package=    "ros_gz_sim",
        executable= "create",
        output=     "screen",
        arguments=[
            "-file", os.path.join(pkg_path_gazebosim, "models", "apriltag_0",  "model.sdf"),
            "-name", "apriltag_0",
            "-x", "3.8", "-y", "2.0", "-z", "0.5", "-R", "1.5708", "-P", "0.0", "-Y", "-1.5708", 
    ],
)



    gz_ros2_bridge = Node(
        package=    "ros_gz_bridge",
        executable= "parameter_bridge",
        arguments=[ "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock", 
                    # "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU", 
                    "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                    # "/camera/image@sensor_msgs/msg/Image[gz.msgs.Image",
                    # "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo", 
                    ], 
    )

    return LaunchDescription([
        gz_resource_path,
        gz_sim,
        gz_spawn_entity,
        spawn_apriltag_0, 
        gz_ros2_bridge,
    ])