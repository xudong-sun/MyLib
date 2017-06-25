#ifndef __COMMONS_H
#define __COMMONS_H

namespace commons {

	void pause() {
		system("pause");
	}

	// join
	template <typename T>
	std::string join(std::vector<T> vec, std::string separator = " ") {
		if (vec.size() == 0) return "";
		std::stringstream ss;
		ss << vec[0];
		for (size_t i = 1; i < vec.size(); i++) ss << separator << vec[i];
		return ss.str();
	}

}

#endif