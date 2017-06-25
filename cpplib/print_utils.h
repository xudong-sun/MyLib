#ifndef __PRINT_UTILS_H
#define __PRINT_UTILS_H

#include "commons.h"

// print a vector
// This also works for nesting containers like std::vector<std::vector<T>>
template <typename T>
std::ostream& operator<<(std::ostream& os, std::vector<T> vec) {
	os << '[' << commons::join(vec, ", ") << ']';
	return os;
}

#endif