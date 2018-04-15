#include "rand_point.hpp"
#include "rand_float.hpp"
#include "random.hpp"

Point rand_point(){
  return Point(rand_float(-1,1), rand_float(-1,1));
}

