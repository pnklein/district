#include <iostream>
#include <fstream>
#include "redistrict.hpp"
#include "print_out_solution.hpp"

using namespace std;

int main(int argc, char *argv[]){
  int num_centers = atoi(argv[1]);
  //  string client_filename = argv[2];
  std::ifstream inf(argv[2]);
  vector<Point> clients;
  vector<long> populations_vec;
  double x, y;
  int population;
  while (inf >> x >> y >> population){
    if (population > 0){
      clients.push_back(Point(x,y));
      populations_vec.push_back(population);
    }
  }
  auto [centers, assignment, weights ] = choose_centers(clients, &populations_vec[0], num_centers);
  if (centers.size() == 0){
    cout << "FAILURE TO CONVERGE\n";
    return -1;
  }
  print_out(centers, weights, clients, assignment);
}
