#ifndef __COMMONS_H
#define __COMMONS_H

namespace commons {

	void pause() {
		system("pause");
	}

	template <typename T>
	void print(T v) {
		std::cout << v << std::endl;
	}

	// similar join function as in python
	template <typename _InIt>
	std::string join(_InIt first, _InIt last, std::string separator = " ") {
		if (first == last) return "";
		std::stringstream ss;
		ss << *first;
		for (auto it = first + 1; it != last; it++) ss << separator << *it;
		return ss.str();
	}

	// convert any type to std::string
	// for any type that has no built-in operator<< with std::ostream, please first checkout helpers in "print_utils.h"
	template <typename T>
	std::string toString(const T& v) {
		std::stringstream ss;
		ss << v;
		return ss.str();
	}

}

#endif