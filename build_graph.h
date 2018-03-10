#pragma once

#include "types_cs2.h"

typedef struct graph_struct {
  node* nodes;
  arc* arcs;
  long n, m; // num vertices, num arcs
} graph;

//  graph build_graph(long** costs, long populations[], long num_clients, long num_centers);

graph build_graph(long* costs, long* populations, long num_clients, long num_centers, long **cap_ad){
    long total_supply = 0;
    for (long i = 0; i < num_clients; ++i){
      total_supply += populations[i];
    }
    long capacity = total_supply/num_centers;
    long remainder = total_supply - num_centers*capacity;
    //Each center receives a flow of value *capacity*
    // except that the first *remainder* centers receive one extra unit of flow.
    graph G;
    G.n = num_clients + num_centers;
    G.m = num_clients * num_centers;
    G.nodes = (node *) calloc(G.n+2, sizeof(node));
    G.arcs = (arc *) calloc(2*G.m+1, sizeof(arc));
    long * cap = (long*) calloc ( 2*G.m, sizeof(long) ); 

    //set up nodes corresponding to centers
    for (long j=0; j < num_centers; ++j){
      long center_index = num_clients + j;
      G.nodes[center_index].excess = - (capacity + (j < remainder? 1 : 0));
      G.nodes[center_index].first = G.arcs + G.m + j*num_clients;
    }
    for (long i=0; i < num_clients; ++i){
      G.nodes[i].excess = populations[i];
      G.nodes[i].first = G.arcs + i*num_centers;
      for (long j=0; j < num_centers; ++j){
	long client_to_center_index = i*num_centers + j;
	long center_to_client_index = G.m + j*num_clients + i;
	//darts from clients to centers
	G.arcs[client_to_center_index].head = G.nodes + num_clients + j;
	G.arcs[client_to_center_index].sister = G.arcs + center_to_client_index;
	G.arcs[client_to_center_index].cost = costs[i*num_centers+j];
	G.arcs[client_to_center_index].r_cap = populations[i];
	cap[client_to_center_index] = populations[i];
	//darts from centers to clients
	G.arcs[center_to_client_index].head = G.nodes + i;
	G.arcs[center_to_client_index].sister = G.arcs + client_to_center_index;
	G.arcs[center_to_client_index].cost = - costs[i*num_centers+j];
	G.arcs[center_to_client_index].r_cap = 0;//not necessary since memory is zeroed by calloc
	cap[center_to_client_index] = 0;//not necessary since memory is zeroed by calloc
      }
    }
    *cap_ad   = cap;
    return G;
}


