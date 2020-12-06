/*
 * This file is subject to the terms and conditions defined in
 * file 'LICENSE', which is part of this source code package.
 *
 * The original author of this code is Josh Lospinoso (@jalospinoso).
 * The unmodified source code can be found here: https://github.com/JLospinoso/cpp-implant
*/
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
