import shapefile
from shapely.geometry import shape
import sys
'''
Call with first argument being the two-letter state abbreviation
and second argument being a filename of a shape record file,
 e.g. "/Users/klein/Downloads/cb_2016_us_state_500k/cb_2016_us_state_500k"
'''

#This will print out a sequence of line segments
sf = shapefile.Reader(sys.argv[2])
x = next(x for x in sf.iterShapeRecords()  if x.record[4]==sys.argv[1])
for i in range(1,len(x.shape.points)):
    if i in x.shape.parts:
        print()
    pt = x.shape.points[i]
    print(pt[0], pt[1])

    
