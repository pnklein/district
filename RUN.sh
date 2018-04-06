#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Syntax: $0 <Population File> <State Name> <States Outline> <District Num> <Output Name>"
  exit 1
fi

#Get the script's directory
dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

pop_file=$1
state_name=$2
state_shapefile=$3
district_num=$4
output_name=$5

rand_str=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c 20` #Prevents issues when using parallelism
temp_out_pop="temp_census_data_${state_name}_${rand_str}"
temp_out_power="temp_power_diag_${state_name}_${rand_str}"
temp_out_state="temp_state_boundary_${state_name}_${rand_str}"
temp_out_voronoi="temp_voronoi_boundary_${state_name}_${rand_str}"
temp_out_gnuplot="temp_gnuplot_${state_name}_${rand_str}"

echo "Reading census blocks..."
python3 $dir/read_census_blocks.py $pop_file $temp_out_pop

echo "Reading state boundaries..."
python3 $dir/read_state_shapefile.py $state_name $state_shapefile > $temp_out_state

echo "Generating power diagram..."
$dir/do_redistrict.exe $district_num $temp_out_pop > $temp_out_power

echo "Generating Voronoi boundaries..."
python3 $dir/Voronoi_boundaries.py $temp_out_power $temp_out_voronoi

echo "Extracting districting boundaries..."
python3 $dir/extract_district_boundaries.py $temp_out_voronoi $temp_out_state > "$output_name"
#python3 plotGNUPlot.py $temp_out_voronoi $temp_out_state $temp_out_gnuplot False
#gnuplot < $temp_out_gnuplot

#rm -f $temp_out_pop $temp_out_power $temp_out_state $temp_out_voronoi $temp_out_gnuplot