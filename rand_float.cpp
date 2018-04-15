#include "rand_float.hpp"
#include "random.hpp"

double rand_float(double lower, double upper){
  return uniform_rand_real(lower, upper);
}
