Balanced Centroidal Power Diagram Redistricting
===============================================

Compilation
-----------

Compile the code by running:

    make


Running the Code: Short Version
-------------------------------

The code can be run using:

    ./RUN.sh <Population File> <State Name> <States Outline> <District Num> <Output Name>

where

 * `<Population File>` is a census block shapefile. These have names like `tabblock2010_44_pophu` (see below).
 * `<State Name>` is the FIPS code of the state to be processed. In this example, this is `44`.
 * `<States Outline>` is the name of a state boundary shapefile. This is a file like `cb_2016_us_state_500k` (see below).
 * `<District Num>` is the number of districts to generate
 * `<Output Name>` is the name of the output file.

Output will a representation of the districts in well-known text (WKT) format.
This is suitable for interoperation with many standard GIS programs.



Running the Code: Long Version
------------------------------

Extract census blocks and populations

    python3  read_census_blocks.py <input directory name> <output_filename>

where `<input directory name>` contains shape file specifying census blocks,
e.g.

    abblock010_44_pophu/tabblock2010_44_pophu

which can be downloaded from https://www.census.gov/geo/maps-data/data/tiger-data.html
(Select Population & Housing Unit Counts -- Blocks, then select a state.)

The output file written has one line per client point. It specifies the x
coordinate (longitude), the y coordinate (latitude), and the population assigned
to that point. The script selects the point to be the centroid of the census
block shape.  (WHAT HAPPENS IF THE SHAPE CONSISTS OF MULTIPLE POLYGONS?)

Also, extract the boundary polygons of a state:

    python3 read_state_shapefile.py <ST> <input directory name>

here `<ST>` is the two-letter abbreviation for a state, and `<input directory name>`

is the name of a directory (not including suffix) giving shape records for state
boundaries, e.g. cb_2016_us_state_500k as downloaded from
https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html

Next, compute the clustering using

    do_redistrict <k> <input_filename>

where the first argument is the number of clusters to find, and the input file
is in the format of the output of the `read_census_blocks.py` script. This program
sends some text indicating progress to standard err, and, when it terminates,
sends the output to standard out.

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

to produce a file that specifies: the client points, with colors reflecting the
assignment to centers, and the boundaries of the convex polygons that form the
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

where <boundary filename> is the name of a file specifying the boundaries of the state, given in the format

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

where each sequence of x-y lines specifes the coordinates of polygon vertices of
some polygon that is part of the boundary of the state.

The output is a file with gnuplot commands.  Running gnuplot on that file shows
the client points according to the color assignment, and also the state
boundaries, and also the boundaries of the power-diagram cells (clipped against
the state boundaries).
