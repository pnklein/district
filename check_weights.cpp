#include "check_weights.hpp"

using namespace std;

bool check_weights(const vector<Point> & clients, const vector<Point> & centers, const Assignment & assignment, const vector<double> & weights){
  const double tolerance= 1e-6;
  for (int i = 0; i < clients.size(); ++i){
    for (AssignmentElement ae : assignment[i]){

      double client_to_assigned_center_weighted_dist_sq = centers[ae.center].dist_sq(clients[i]) + weights[ae.center];
      for (int j = 0; j < centers.size(); ++j){

        if (client_to_assigned_center_weighted_dist_sq > centers[j].dist_sq(clients[i]) + weights[j]+tolerance){
          cerr << "ERROR: client " << i << " closer to center " << j << " than to assigned center " << ae.center << "\n";
          cerr << "assigned cost: " << client_to_assigned_center_weighted_dist_sq << " other cost: " << centers[j].dist_sq(clients[i]) + weights[j] << "\n";//debugging
          return false;
        }
      }
    }
  }
  return true;
}

bool check_weights(long * costs, int num_clients, int num_centers, const Assignment & assignment, const vector<long> & weights){
  for (int i = 0; i < num_clients; ++i){
    for (AssignmentElement ae : assignment[i]){
      double assigned_cost = costs[i*num_centers+ae.center] + weights[ae.center];
      for (int j = 0; j < num_centers; ++j){
        if (assigned_cost > costs[i*num_centers+j] + weights[j]){
          
          cerr << "ERROR: client " << i << " closer to center " << j << " than to assigned center " << ae.center << "\n";
          return false;
        }
      }
    }
  }
  return true;
}

