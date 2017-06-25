#ifndef __COMMONS_H
#define __COMMONS_H

namespace commons {

	void pause() {
		system("pause");
	}

	// similar join function as in python
	template <typename T>
	std::string join(std::vector<T> vec, std::string separator = " ") {
		if (vec.size() == 0) return "";
		std::stringstream ss;
		ss << vec[0];
		for (size_t i = 1; i < vec.size(); i++) ss << separator << vec[i];
		return ss.str();
	}

	// convert any type to std::string
	// for any type that has no built-in operator<< with std::ostream, please first checkout helpers in "print_utils.h"
	template <typename T>
	std::string toString(T v) {
		std::stringstream ss;
		ss << v;
		return ss.str();
	}

}

#endif