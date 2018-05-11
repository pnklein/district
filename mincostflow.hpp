#pragma once

#include <vector>
#include "types_cs2.h"
#include "assignment.hpp"

void find_assignment(long * costs, long * populations, int num_clients, int num_centers, Assignment &assignment, std::vector<long> &weights);
