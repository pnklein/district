#include <cstdlib>
#include <numeric>
#include <limits>
#include "initial_centers.hpp"
#include "rand_float.hpp"
#include "rand_point.hpp"
#include "random.hpp"

std::vector<Point> choose_initial_centers(
  const std::vector<Point> &clients, 
  const long *const populations, 
  int num_centers
){
  const long population = std::accumulate(populations, populations+clients.size(), 0);
  long r = rand() % population;
  std::vector<Point> centers(num_centers);
  
  //Choose a random initial centroid from the list of population points
  //weighting each one's probability of being chosen by its population
  for (unsigned int i=0; i < clients.size(); ++i){
    r -= populations[i];
    if (r <= 0) {
      centers.at(0) = clients[i];
      break;
    }
  }

  std::vector<double> distances_sq(clients.size(), std::numeric_limits<double>::infinity());
  for (unsigned int j = 1; j < centers.size(); ++j){
    double weighted_sum_dist_sq = 0.;
    for (unsigned int i = 1; i < clients.size(); ++i){
      distances_sq[i] = std::min(distances_sq[i], centers[j-1].dist_sq(clients[i]));
      weighted_sum_dist_sq += distances_sq[i]*populations[i];
    }
    double choice = rand_float(0, weighted_sum_dist_sq);
    for (unsigned int i = 0; i < clients.size(); ++i) {
      choice -= distances_sq[i]*populations[i];
      if (choice <= 0){
        centers[j] = clients[j];
        break;
      }
    }
  }
  
  return centers;
}
