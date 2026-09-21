cmake_minimum_required(VERSION 3.8)
project(rmitbot_navigation)


find_package(ament_cmake REQUIRED)

# Folder to be added
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
