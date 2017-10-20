#include "rand_float.hpp"

double rand_float(double lower, double upper){
  return lower + static_cast<double>(rand()) / static_cast<double>(RAND_MAX/(upper-lower));
}
