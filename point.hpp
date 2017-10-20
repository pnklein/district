#pragma once
#include <iostream>
//#include <utility>
#include "rand_float.hpp"

class Point {
public:
  double x,y;
  Point(double x_arg, double y_arg) : x(x_arg), y(y_arg) {}
  double dist_sq(Point other) const{
    return (x-other.x)*(x-other.x)+(y-other.y)*(y-other.y);
  }
  Point scale(double alpha) const{
    return Point(alpha*x,alpha*y);
  }
  Point add(Point other) const{
    return Point(x+other.x,y+other.y);
  }
  bool operator==(const Point &other) const{
    return x == other.x && y == other.y;
  }
  bool operator!=(const Point &other) const{
    return x != other.x || y != other.y;
  }
  Point() : x(0), y(0) {}
};

std::ostream &operator<<(std::ostream & output, const Point &p);
