#!/bin/bash

echo "Syntax: $0 <Population File> <State Name> <States Outline> <District Num>"

pop_file=$1
state_name=$2
state_shapefile=$3
district_num=$4

rand_str=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c 20`
temp_out_pop="tmp.census_data.${rand_str}"
temp_out_power="tmp.power_diag.${rand_str}"
temp_out_state="tmp.state_boundary.${rand_str}"
temp_out_voronoi="tmp.voronoi_boundary.${rand_str}"
temp_out_gnuplot="tmp.gnuplot.${rand_str}"
temp_out_districts="out_districts.${rand_str}"

echo "Reading census blocks..."
python3 read_census_blocks.py $pop_file $temp_out_pop
echo "Reading state boundaries"
python3 read_state_shapefile.py $state_name $state_shapefile > $temp_out_state
echo "Generating power diagrams"
for (( i=0 ; i < 1 ; i++ )) ; do 
  temp_out_gnuplot="/z/temp_out_gnuplot_${i}"
  ./do_redistrict $district_num $temp_out_pop > $temp_out_power
  python3 Voronoi_boundaries.py $temp_out_power $temp_out_voronoi
  python3 extract_district_boundaries.py $temp_out_voronoi $temp_out_state > "${temp_out_districts}_${i}"
  #python3 plotGNUPlot.py $temp_out_voronoi $temp_out_state $temp_out_gnuplot False
  #gnuplot < $temp_out_gnuplot
done

rm -f $temp_out_pop $temp_out_power $temp_out_state $temp_out_voronoi $temp_out_gnuplot