#pragma once
#include <vector>
#include "point.hpp"
#include <utility>
#include <tuple> // C++11, for std::tie
#include "assignment.hpp"

using namespace std;


void choose_centers(const vector<Point> &clients, long * populations, int num_centers, std::vector<Point> &centers, Assignment &assignment, std::vector<double> &weights);
