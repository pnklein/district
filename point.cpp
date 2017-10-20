#include "point.hpp"

std::ostream &operator<<(std::ostream & output, const Point &p){
  output << "(" << p.x << ", " << p.y << ")";
  return output;
}
