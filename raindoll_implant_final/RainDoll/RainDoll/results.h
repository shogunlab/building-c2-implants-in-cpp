#pragma once

#define _SILENCE_CXX17_C_HEADER_DEPRECATION_WARNING

#include <string>
#include <boost/uuid/uuid.hpp>

// Define our Result object
struct Result {
	Result(const boost::uuids::uuid& id,
		std::string contents,
		bool success);
	const boost::uuids::uuid id;
	const std::string contents;
	const bool success;
};
