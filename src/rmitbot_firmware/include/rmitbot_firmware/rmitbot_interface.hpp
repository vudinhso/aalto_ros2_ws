// These prevent the file from being included more than once during compilation
#ifndef RMITBOT_INTERFACE_HPP
#define RMITBOT_INTERFACE_HPP

// Include necessary headers
#include <rclcpp/rclcpp.hpp>
#include <hardware_interface/system_interface.hpp>
#include <libserial/SerialPort.h>
#include <rclcpp_lifecycle/state.hpp>
#include <rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp>

// Standard C++ Libraries
#include <vector>
#include <string>
#include <sstream>    // Required for std::stringstream
#include <algorithm>  // Required for std::remove
#include <iomanip>    // Required for std::setprecision
namespace rmitbot_firmware
{
  using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

  class RmitbotInterface : public hardware_interface::SystemInterface
  {
  public:
    RmitbotInterface();
    virtual ~RmitbotInterface();

    CallbackReturn on_init(const hardware_interface::HardwareComponentInterfaceParams & params) override;
    CallbackReturn on_activate(const rclcpp_lifecycle::State &) override;
    CallbackReturn on_deactivate(const rclcpp_lifecycle::State &) override;
    
    std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
    std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
    hardware_interface::return_type read(const rclcpp::Time &, const rclcpp::Duration &) override;
    hardware_interface::return_type write(const rclcpp::Time &, const rclcpp::Duration &) override;

  private:
    LibSerial::SerialPort arduino_;
    std::string port_;
    std::vector<double> velocity_commands_;
    std::vector<double> position_states_;
    std::vector<double> velocity_states_;
    std::vector<double> orientation_;
    std::vector<double> ang_vel_;
    std::vector<double> lin_acc_;

    rclcpp::Time last_run_;
  };
} 

#endif 