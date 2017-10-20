#pragma once
#include <vector>

class AssignmentElement {
public:
  int center, //which center is assigned?
    flow; //how much weight of this point is assigned to the center?
  AssignmentElement(int center_arg, int flow_arg) : center(center_arg), flow(flow_arg) {}
  bool operator==(const AssignmentElement ae) const {return center==ae.center && flow == ae.flow;}
};


typedef std::vector<std::vector<AssignmentElement> > Assignment;
  
