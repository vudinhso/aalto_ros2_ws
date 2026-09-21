#include "rmitbot_firmware/rmitbot_interface.hpp"
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include <pluginlib/class_list_macros.hpp>

namespace rmitbot_firmware
{
  // Constructor
  RmitbotInterface::RmitbotInterface() {}

  // Destructor
  RmitbotInterface::~RmitbotInterface()
  {
    if (arduino_.IsOpen())
    {
      try
      {
        arduino_.Close();
      }
      catch (...)
      {
        RCLCPP_FATAL_STREAM(rclcpp::get_logger("RmitbotInterface"), "Something went wrong while closing connection with port " << port_);
      }
    }
  }

  // on_init function: Initialize the hardware interface
  // CallbackReturn RmitbotInterface::on_init(const hardware_interface::HardwareInfo &hardware_info) {
  CallbackReturn RmitbotInterface::on_init(const hardware_interface::HardwareComponentInterfaceParams &params)
  {
    CallbackReturn result = hardware_interface::SystemInterface::on_init(params);
    if (result != CallbackReturn::SUCCESS)
      return result;
    try
    {
      port_ = info_.hardware_parameters.at("port");
    }
    catch (const std::out_of_range &e)
    {
      RCLCPP_FATAL(rclcpp::get_logger("RmitbotInterface"), "No Serial Port provided! Aborting");
      return CallbackReturn::FAILURE;
    }

    // Size our buffers to match the number of joints
    velocity_commands_.assign(info_.joints.size(), 0.0);
    velocity_states_.assign(info_.joints.size(), 0.0);
    position_states_.assign(info_.joints.size(), 0.0);

    orientation_.assign(4, 0.0);
    orientation_[3] = 1.0;
    ang_vel_.assign(3, 0.0);
    lin_acc_.assign(3, 0.0);

    return CallbackReturn::SUCCESS;
  }

  // on_activate function: Open the serial port
  CallbackReturn RmitbotInterface::on_activate(const rclcpp_lifecycle::State &)
  {
    RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Starting robot hardware ...");

    // Reset commands and states
    velocity_commands_ = {0.0, 0.0};
    position_states_ = {0.0, 0.0};
    velocity_states_ = {0.0, 0.0};
    orientation_ = {0.0, 0.0, 0.0, 1.0};
    ang_vel_ = {0.0, 0.0, 0.0};
    lin_acc_ = {0.0, 0.0, 0.0};
    last_run_ = rclcpp::Clock().now();

    try
    {
      arduino_.Open(port_);
      arduino_.SetBaudRate(LibSerial::BaudRate::BAUD_115200);
    }
    catch (...)
    {
      RCLCPP_FATAL_STREAM(rclcpp::get_logger("RmitbotInterface"), "Something went wrong while interacting with port " << port_);
      return CallbackReturn::FAILURE;
    }

    RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Hardware started, ready to take commands");
    return CallbackReturn::SUCCESS;
  }

  // on_deactivate function: Close the serial port
  CallbackReturn RmitbotInterface::on_deactivate(const rclcpp_lifecycle::State &)
  {
    RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Stopping robot hardware ...");

    if (arduino_.IsOpen())
    {
      try
      {
        arduino_.Close();
      }
      catch (...)
      {
        RCLCPP_FATAL_STREAM(rclcpp::get_logger("RmitbotInterface"), "Something went wrong while closing connection with port " << port_);
      }
    }

    RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Hardware stopped");
    return CallbackReturn::SUCCESS;
  }

  // Export the state interfaces
  std::vector<hardware_interface::StateInterface> RmitbotInterface::export_state_interfaces()
  {
    std::vector<hardware_interface::StateInterface> state_interfaces;

    // Provide position and velocity interfaces for each wheel
    for (size_t i = 0; i < info_.joints.size(); i++)
    {
      state_interfaces.emplace_back(hardware_interface::StateInterface(
          info_.joints[i].name, hardware_interface::HW_IF_POSITION, &position_states_[i]));
      state_interfaces.emplace_back(hardware_interface::StateInterface(
          info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &velocity_states_[i]));
    }

    // Provide IMU state interfaces
    std::string imu_name = info_.sensors[0].name;
    // Orientation (quaternion)
    state_interfaces.emplace_back(imu_name, "orientation.x", &orientation_[0]);
    state_interfaces.emplace_back(imu_name, "orientation.y", &orientation_[1]);
    state_interfaces.emplace_back(imu_name, "orientation.z", &orientation_[2]);
    state_interfaces.emplace_back(imu_name, "orientation.w", &orientation_[3]);

    // Angular velocity
    state_interfaces.emplace_back(imu_name, "angular_velocity.x", &ang_vel_[0]);
    state_interfaces.emplace_back(imu_name, "angular_velocity.y", &ang_vel_[1]);
    state_interfaces.emplace_back(imu_name, "angular_velocity.z", &ang_vel_[2]);

    // Linear acceleration
    state_interfaces.emplace_back(imu_name, "linear_acceleration.x", &lin_acc_[0]);
    state_interfaces.emplace_back(imu_name, "linear_acceleration.y", &lin_acc_[1]);
    state_interfaces.emplace_back(imu_name, "linear_acceleration.z", &lin_acc_[2]);

    return state_interfaces;
  }

  // Export the command interfaces
  std::vector<hardware_interface::CommandInterface> RmitbotInterface::export_command_interfaces()
  {
    std::vector<hardware_interface::CommandInterface> command_interfaces;

    // Provide only a velocity Interafce
    for (size_t i = 0; i < info_.joints.size(); i++)
    {
      command_interfaces.emplace_back(hardware_interface::CommandInterface(
          info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &velocity_commands_[i]));
    }

    return command_interfaces;
  }

  // =======================================================================
  // Read function: Receive the states from the microcontroller
  // =======================================================================
  hardware_interface::return_type RmitbotInterface::read(const rclcpp::Time &,
                                                         const rclcpp::Duration &)
  {
    // Interpret the string from Arduino, e.g.: "<1.24\t-2.36>"
    // It is much better to use starting and ending delimiters, because serial will fail
    // Usually because Arduino is sending too fast, or the buffer is not empty
    if (arduino_.IsDataAvailable())
    {
      auto dt = (rclcpp::Clock().now() - last_run_).seconds();
      std::string message;
      arduino_.ReadLine(message);
      // RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Message Received: %s", message.c_str());

      // Remove only the newline and carriage return characters (i.e., \n, \r)
      message.erase(std::remove(message.begin(), message.end(), '\n'), message.end());
      message.erase(std::remove(message.begin(), message.end(), '\r'), message.end());
      // RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Trimmed message: '%s'", message.c_str());

      // Check for proper start and end delimiters
      if (!message.empty() && message.front() == '<' && message.back() == '>')
      {
        // Remove the start '<' and end '>'
        std::string data = message.substr(1, message.size() - 2);
        std::stringstream ss(data);
        std::string token;
        // std::vector<float> velocities;
        std::vector<float> states_data;
        // RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Data Received: %s", data.c_str());

        while (std::getline(ss, token, '\t'))
        {
          states_data.push_back(std::stof(token)); // Store the right_vel and left_vel in the vector
          // RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "Parsed velocities: %.2f, %.2f", velocity_states_.at(0), velocity_states_.at(1));
        }
        if (states_data.size() == 12)
        {
          velocity_states_.at(0) = states_data.at(0); // front right wheel
          velocity_states_.at(1) = states_data.at(1); // front left wheel
          
          position_states_.at(0) += velocity_states_.at(0) * dt;
          position_states_.at(1) += velocity_states_.at(1) * dt;

          orientation_.at(0) = states_data.at(2); // imu orientation x
          orientation_.at(1) = states_data.at(3); // imu orientation y
          orientation_.at(2) = states_data.at(4); // imu orientation z
          orientation_.at(3) = states_data.at(5); // imu orientation w

          ang_vel_.at(0) = states_data.at(6);  // imu angular velocity x
          ang_vel_.at(1) = states_data.at(7);  // imu angular velocity y
          ang_vel_.at(2) = states_data.at(8); // imu angular velocity z

          lin_acc_.at(0) = states_data.at(9); // imu linear acceleration x
          lin_acc_.at(1) = states_data.at(10); // imu linear acceleration y
          lin_acc_.at(2) = states_data.at(11); // imu linear acceleration z
        }
        else
        {
          RCLCPP_WARN(rclcpp::get_logger("RmitbotInterface"), "Malformed packet received, expected 12 values, got %zu", states_data.size());
        }
      }
      last_run_ = rclcpp::Clock().now();
    }
    // RCLCPP_INFO(rclcpp::get_logger("RmitbotInterface"), "read() was called");
    return hardware_interface::return_type::OK;
  }

  // =======================================================================
  // Write function: Send the commands from ROS2 to the microcontroller
  // =======================================================================
  hardware_interface::return_type RmitbotInterface::write(const rclcpp::Time &,
                                                          const rclcpp::Duration &)
  {
    std::stringstream message_stream;
    // Add starting delimiter
    message_stream << "<";
    // Add the velocity data, separated by tab
    message_stream << std::fixed << std::setprecision(2)
                   << velocity_commands_.at(0) << "\t" // front Right wheel
                   << velocity_commands_.at(1); 
    // Add ending delimiter
    message_stream << ">\n"; // Optionally include newline for easy serial monitor reading

    try
    {
      arduino_.Write(message_stream.str());
    }
    catch (...)
    {
      RCLCPP_ERROR_STREAM(rclcpp::get_logger("RmitbotInterface"), "Something went wrong while sending the message " << message_stream.str() << " to the port " << port_);
      return hardware_interface::return_type::ERROR;
    }

    return hardware_interface::return_type::OK;
  }
} // namespace rmitbot_firmware

PLUGINLIB_EXPORT_CLASS(rmitbot_firmware::RmitbotInterface, hardware_interface::SystemInterface)