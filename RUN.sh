#!/bin/bash

echo "Syntax: $0 <Population File> <State Name> <States Outline> <District Num>"

pop_file=$1
state_name=$2
state_shapefile=$3
district_num=$4

temp_out_pop=/z/temp_out_pop
temp_out_power=/z/temp_out_power
temp_out_state=/z/temp_out_state
temp_out_voronoi=/z/temp_out_voronoi
temp_out_gnuplot=/z/temp_out_gnuplot
temp_out_districts=/z/temp_out_districts

echo "Reading census blocks..."
#python3 read_census_blocks.py $pop_file $temp_out_pop
echo "Reading state boundaries"
#python3 read_state_shapefile.py $state_name $state_shapefile > $temp_out_state
echo "Generating power diagrams"
#./do_redistrict $district_num $temp_out_pop > $temp_out_power
#python3 Voronoi_boundaries.py $temp_out_power $temp_out_voronoi
python3 extract_district_boundaries.py $temp_out_voronoi $temp_out_state > $temp_out_districts
#python3 plotGNUPlot.py $temp_out_voronoi $temp_out_state $temp_out_gnuplot False
#gnuplot < $temp_out_gnuplot