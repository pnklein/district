import shapefile
from shapely.geometry import shape
import sys
'''
Call with first argument being the two-letter state abbreviation
and second argument being a filename of a shape record file,
 e.g. "/Users/klein/Downloads/cb_2016_us_state_500k/cb_2016_us_state_500k"
'''

if len(sys.argv)!=3:
  print("Syntax: {0} <State Name> <Shapefile of State Outlines>")
  sys.exit(-1)

#This will print out a sequence of line segments
sf = shapefile.Reader(sys.argv[2])

for state in sf.iterShapeRecords():
  if state.record[2]==sys.argv[1]:
    break
else:
  raise Exception("Could not find state!")

for i in range(1,len(state.shape.points)):
    if i in state.shape.parts:
        print()
    pt = state.shape.points[i]
    print(pt[0], pt[1])

    
