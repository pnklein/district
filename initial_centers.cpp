#include <cstdlib>
#include <numeric>
#include <limits>
#include "initial_centers.hpp"
#include "rand_float.hpp"
#include "rand_point.hpp"

using namespace std;

vector<Point> choose_initial_centers(const vector<Point> &clients, long * populations, int num_centers){
  vector<int> rand_values(clients.size());
  long population = accumulate(populations, populations+clients.size(), 0);
  long r = rand() % population;
  vector<Point> centers(num_centers);
  for (int i=0; i < clients.size(); ++i){
    r -= populations[i];
    if (r <= 0) {
      centers[0] = clients[i];
      break;
    }
  }
  vector<double> distances_sq(clients.size(), numeric_limits<double>::infinity());
  for (int j = 1; j < centers.size(); ++j){
    double weighted_sum_dist_sq = 0.;
    for (int i = 1; i < clients.size(); ++i){
      distances_sq[i] = min(distances_sq[i], centers[j-1].dist_sq(clients[i]));
      weighted_sum_dist_sq += distances_sq[i]*populations[i];
    }
    double choice = rand_float(0, weighted_sum_dist_sq);
    for (int i = 0; i < clients.size(); ++i) {
      choice -= distances_sq[i]*populations[i];
      if (choice <= 0){
	centers[j] = clients[j];
	break;
      }
    }
  }
  return centers;
}
