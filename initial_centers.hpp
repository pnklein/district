#pragma once

#include <vector>
#include "point.hpp"

std::vector<Point> choose_initial_centers(const std::vector<Point> &clients, const long *const populations, int num_centers);
