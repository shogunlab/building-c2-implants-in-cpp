/*
 * This file is subject to the terms and conditions defined in
 * file 'LICENSE', which is part of this source code package.
 *
 * The original author of this code is Josh Lospinoso (@jalospinoso).
 * The unmodified source code can be found here: https://github.com/JLospinoso/cpp-implant
*/
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#endif

#include "results.h"


// Result object returned by all tasks
// Includes the task ID, result contents and success status (true/false)
Result::Result(const boost::uuids::uuid& id,
	std::string contents,
	const bool success)
	: id(id), contents{ std::move(contents) }, success(success) {}
