cmake_minimum_required(VERSION 3.8)
project(rmitbot_gazebosim)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch world models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()