#pragma once
#include <vector>
#include "point.hpp"
#include <utility>
#include <tuple> // C++11, for std::tie
#include "assignment.hpp"

using namespace std;


tuple<vector<Point>, Assignment, vector<double> > choose_centers(const vector<Point> &clients, long * populations, int num_centers);
