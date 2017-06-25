#ifndef __PRINT_UTILS_H
#define __PRINT_UTILS_H

#include <vector>
#include <list>
#include <forward_list>
#include <set>
#include <unordered_set>

#include "commons.h"

// print vectors, lists, forward_lists
// This also works for nesting containers like std::vector<std::vector<T>>
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec) {
	os << '[' << commons::join(vec.cbegin(), vec.cend(), ", ") << ']';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::list<T>& vec) {
	os << '[' << commons::join(vec.cbegin(), vec.cend(), ", ") << ']';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::forward_list<T>& vec) {
	os << '[' << commons::join(vec.cbegin(), vec.cend(), ", ") << ']';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::set<T>& vec) {
	os << '{' << commons::join(vec.cbegin(), vec.cend(), ", ") << '}';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::multiset<T>& vec) {
	os << '{' << commons::join(vec.cbegin(), vec.cend(), ", ") << '}';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::unordered_set<T>& vec) {
	os << '{' << commons::join(vec.cbegin(), vec.cend(), ", ") << '}';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::unordered_multiset<T>& vec) {
	os << '{' << commons::join(vec.cbegin(), vec.cend(), ", ") << '}';
	return os;
}

#endif