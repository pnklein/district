#include <iostream>
#include <fstream>
#include <time.h>
#include "assignment.hpp"
#include "redistrict.hpp"
#include "print_out_solution.hpp"

using namespace std;

int main(int argc, char *argv[]){
  srand(time(NULL));

  if(argc!=3){
    cout<<"Syntax: "<<argv[0]<<"<Number of Districts> <Population Data>"<<std::endl;
    return -1;
  }

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

  std::vector<Point> centers;
  Assignment assignment;
  std::vector<double> weights;

  choose_centers(clients, &populations_vec[0], num_centers, centers, assignment, weights);

  if (centers.size() == 0){
    cout << "FAILURE TO CONVERGE\n";
    return -1;
  }
  print_out(centers, weights, clients, assignment);
}
