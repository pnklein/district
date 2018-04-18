import shapefile
from shapely.geometry import shape

'''Provides a procedure to read a shape file specifying census blocks,
   and write a file giving the clients.  For each census block, the client
   is located at the centroid of the block shape, and its weight is the
   population of the census block.
   Each line of the output consists of:
      the x coordinate,
      the y coordinate, and
      the population.
   Only census blocks with positive population are represented in the output.
'''


def write_client_file(input_filename, output_filename):
    sf = shapefile.Reader(input_filename)
    of = open(output_filename, 'w')
    for shape_rec in sf.iterShapeRecords():
        pop = shape_rec.record[7]
        if pop > 0:
            cent = shape(shape_rec.shape).centroid
            of.write(str(cent.x)+" "+str(cent.y)+" "+str(pop)+"\n")


import sys
write_client_file(sys.argv[1],sys.argv[2])
