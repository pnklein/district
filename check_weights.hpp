#pragma once

#include "assignment.hpp"
#include "point.hpp"

bool check_weights(const std::vector<Point> & clients, const std::vector<Point> & centers, const Assignment & assignment, const std::vector<double> & weights);

bool check_weights(long * costs, int num_clients, int num_centers, const Assignment & assignment, const std::vector<long> & weights);
