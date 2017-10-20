#pragma once

#include <vector>
#include "assignment.hpp"

/* Output format:
    <num centers> <num clients>
    <center x> <center y> <center z>
    <center x> <center y> <center z>
    .
    .
    <center x> <center y> <center z>
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>
    .
    .
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>
 */
void print_out(const std::vector<Point> centers, const std::vector<double> &weights, const std::vector<Point> &clients,
               const Assignment &assignment);
