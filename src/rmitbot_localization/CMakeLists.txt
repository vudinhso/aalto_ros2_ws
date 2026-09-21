cmake_minimum_required(VERSION 3.8)
project(rmitbot_localization)

find_package(ament_cmake REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)



ament_package()
