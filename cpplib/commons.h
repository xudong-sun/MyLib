#ifndef __COMMONS_H
#define __COMMONS_H

namespace commons {

	void pause() {
		system("pause");
	}

	// a group of overloaded print functions that is able to print any number of arguments using operator<<
	template <typename T>
	void print(const T& v) {
		std::cout << v << std::endl;
	}
	template <typename T, typename... Types>
	void print(const T& v, Types&&... args) {
		std::cout << v << ' ';
		print(std::forward<Types>(args)...);
	}

	// similar join function as in python
	template <typename _InIt>
	std::string join(_InIt first, _InIt last, std::string separator = " ") {
		if (first == last) return "";
		std::stringstream ss;
		ss << *first;
		auto it = first;
		for (it++; it != last; it++) ss << separator << *it;
		return ss.str();
	}

	// convert any type to std::string
	// extends std::to_string function
	// for any type that has no built-in operator<< with std::ostream, please first checkout helpers in "print_utils.h"
	template <typename T>
	std::string to_string(const T& v) {
		std::stringstream ss;
		ss << v;
		return ss.str();
	}

}

#endif
