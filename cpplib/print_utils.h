#ifndef __PRINT_UTILS_H
#define __PRINT_UTILS_H

#include <vector>
#include <list>
#include <forward_list>
#include <array>
#include <deque>
#include <set>
#include <unordered_set>
#include <map>
#include <unordered_map>

#include "commons.h"

// print vectors, lists, forward_lists, arrays, sets, maps, pairs
// This also works for nested containers like std::vector<std::list<T>>
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec) {
	os << '[' << commons::join(vec.cbegin(), vec.cend(), ", ") << ']';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::list<T>& list) {
	os << '[' << commons::join(list.cbegin(), list.cend(), ", ") << ']';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::forward_list<T>& list) {
	os << '[' << commons::join(list.cbegin(), list.cend(), ", ") << ']';
	return os;
}
template <typename T, size_t N>
std::ostream& operator<<(std::ostream& os, const std::array<T, N>& arr) {
	os << '(' << commons::join(arr.cbegin(), arr.cend(), ", ") << ')';
	return os;
}
template <typename T>
std::ostream& operator<<(std::ostream& os, const std::deque<T>& deque) {
  os << '[' << commons::join(deque.cbegin(), deque.cend(), ",") << ']';
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
template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::pair<T1, T2>& p) {
	os << '<' << p.first << ", " << p.second << '>';
	return os;
}
template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::map<T1, T2>& m) {
	os << '{' << commons::join(m.cbegin(), m.cend(), ", ") << '}';
	return os;
}
template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::multimap<T1, T2>& m) {
	os << '{' << commons::join(m.cbegin(), m.cend(), ", ") << '}';
	return os;
}
template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::unordered_map<T1, T2>& m) {
	os << '{' << commons::join(m.cbegin(), m.cend(), ", ") << '}';
	return os;
}
template <typename T1, typename T2>
std::ostream& operator<<(std::ostream& os, const std::unordered_multimap<T1, T2>& m) {
	os << '{' << commons::join(m.cbegin(), m.cend(), ", ") << '}';
	return os;
}

#endif
