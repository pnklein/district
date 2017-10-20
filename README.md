Note that the file  code incorporates an adapted version of CS2, Andrew
Goldberg and Boris Cherkassky's implementation of a min-cost flow
algorithm due to Goldberg.  See cs2-COPYRIGHT for the license
information, and also see cs2-README.

The rest of the code is subject to the following license:
Copyright 2017 Philip N. Klein and Vincent Cohen-Addad

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Extract census blocks and populations
  python3  read_census_blocks.py <input directory name> <output_filename>
where <input directory name> contains shape file specifying census blocks, e.g.
          abblock010_44_pophu/tabblock2010_44_pophu
which can be downloaded from https://www.census.gov/geo/maps-data/data/tiger-data.html
(Select Population & Housing Unit Counts -- Blocks, then select a state.)

The output file written has one line per client point.
It specifies the x coordinate (longitude), the y coordinate
(latitude), and the population assigned to that point.
The script selects the point to be the centroid of the census block
shape.  (WHAT HAPPENS IF THE SHAPE CONSISTS OF MULTIPLE POLYGONS?)

Also, extract the boundary polygons of a state:
  python3 read_state_shapefile.py <ST> <input directory name>
 where <ST> is the two-letter abbreviation for a state, and <input directory name>
is the name of a directory (not including suffix) giving shape records for
  state boundaries, e.g. cb_2016_us_state_500k as downloaded from https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html

Next, compute the clustering using
   do_redistrict <k> <input_filename>
where the first argument is the number of clusters to find, and the
input file is in the format of the output of the read_census_blocks.py script.
This program sends some text indicating progress to standard err, and,
when it terminates, sends the output to standard out.
 Output format:
    <num centers> <num clients>
    <center x> <center y> <center z>
    <center x> <center y> <center z>
    .
    .
    <center x> <center y> <center z>
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>
    .
    .
    <client x> <client y> <center id> <subpopulation> <center id> <subpopulation> ... <center id> <subpopulation>

Standard out should be piped into a file

Next, use
   python3 Voronoi_boundaries.py <input filename> <output filename>
to produce a file that specifies:
   the client points, with colors reflecting the assignment to
   centers, and the boundaries of the convex polygons that form the
   power diagram of the chosen centers.
   
Format:
     <num centers> <num clients>
     <center x> <center y> <color>
     <center x> <center y> <color>
      .
      .
      <center x> <center y> <color>
      <x> <y> <x> <y> ... <x> <y> 
      <x> <y> <x> <y> ... <x> <y> 
      .
      .
      <x> <y> <x> <y> ... <x> <y> 

Next, use
  python3 plotGNUPlot.py <input filename> <boundary filename> <output  GNUplot file>
where <boundary filename> is the name of a file specifying the
  boundaries of the state, given in the format
    <x> <y>
    <x> <y>
    .
    .
    <empty line>
    <x> <y>
    <x> <y>
    .
    .
   <empty line>
    <x> <y>
    <x> <y>
    .
    .

where each sequence of x-y lines specifes the coordinates of polygon
vertices of some polygon that is part of the boundary of the state.

The output is a file with gnuplot commands.  Running gnuplot on that
file shows the client points according to the color assignment, and
also the state boundaries, and also the boundaries of the
power-diagram cells (clipped against the state boundaries).
