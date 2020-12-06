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
