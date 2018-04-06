#!/usr/bin/env python3
import numpy as np
import sys
import scipy.spatial as sp
import shapely.geometry as sg
from shapely.geometry.polygon import Polygon
import shapely.ops 
import shapely.wkt

def Parse_boundary(filename):
    f = open(filename, "r")
    lines = f.readlines()
    boundaries = []
    i = 0
    points = []
    for l in lines:
        if l == "\n" :
            boundaries.append(Polygon(points))
            points = []
            continue
        s = l.split()
        x = float(s[0])
        y = float(s[1])
        points.append([x,y])
    boundaries.append(Polygon(points))
    f.close()
    return boundaries
    

        
def Parse(filename):
    f            = open(filename, "r")
    lines        = f.readlines()
    s            = lines[0].split()
    nb_centers   = int(s[0])
    nb_clients   = int(s[1])
    x_min, y_min = (float("inf"),float("inf"))
    x_max, y_max = (-float("inf"),-float("inf"))
    
    C = []
    for i in range(1, nb_centers+1):
        s     = lines[i].split()
        x     = float(s[0])
        y     = float(s[1])
        color = s[2]
        C.append([x,y,color])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        

    assign_pairs = {}
    A = []
    for i in range(nb_centers+1, nb_centers+nb_clients+1):
        s     = lines[i].split()
        x     = float(s[0])
        y     = float(s[1])
        color = s[2]
        A.append([x,y,color])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)

    polygons = []
    for i in range(nb_centers+nb_clients+1, len(lines)):
        points_unsplit = lines[i].split()
        points = [[float(points_unsplit[j].split(",")[0]),
                       float(points_unsplit[j].split(",")[1])]
                    for j in range(len(points_unsplit))]
        polygons.append(Polygon(points))
        # print(polygons[-1].exterior.xy)
    f.close()
    return C,A,polygons,[[x_min,y_min],[x_max,y_max]]

def clip(polygons, boundary):
    new_clipped = []
    for p in polygons:
        new_poly = []
        for b in boundary:
            pclean = p.buffer(0)
            bclean = b.buffer(0)
            if blcean.contains(pclean):
                new_poly.append(pclean)
            elif pclean.intersects(blcean) :
                new_poly.append(pclean.intersection(blcean))
        new_clipped.append(shapely.ops.cascaded_union(new_poly))
    return new_clipped
    
if __name__ == '__main__':
    if len(sys.argv)!=3:
        print("Use: ", sys.argv[0], "[voronoi boundary file] [state boundary file]")
        exit(-1)

    voronoi_file   = sys.argv[1]
    state_boundary = sys.argv[2]

    C_3D, A, polygons, bbox = Parse(voronoi_file)

    boundary = Parse_boundary(state_boundary)

    clipped_polygons = clip(polygons, boundary)

    for cp in clipped_polygons:
        print(shapely.wkt.dumps(cp))