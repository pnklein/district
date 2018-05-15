import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
import shapely.geometry as sg
from matplotlib import colors as mcolors
 
def Parse(filename):
    f = open(filename, "r")
    lines = f.readlines()
    s = lines[0].split()
    nb_centers = int(s[0])
    nb_clients = int(s[1])
    x_min, y_min, z_min = (float("inf"),float("inf"),float("inf"))
    x_max, y_max, z_max = (-float("inf"),-float("inf"),-float("inf"))
    
    C = []
    for i in range(1, nb_centers+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        z = float(s[2])
        C.append([x,y,z])
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        z_max = max(z_max, z)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        z_min = min(z_min, z)
        
    assign_pairs = {}
    A = []
    j = 0
    for i in range(nb_centers+1, nb_centers+nb_clients+1):
        s = lines[i].split()
        x = float(s[0])
        y = float(s[1])
        A.append([x,y])
        assign_pairs[j] = int(s[2])
        j+=1
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
    f.close()
    return C,A,assign_pairs, [[x_min,y_min,z_min],[x_max,y_max,z_max]]

def find_extent(bbox):
    minpt, maxpt = bbox
    return [maxpt[i] - minpt[i] for i in range(3)]

def unbounded(input_region): return any(x==-1 for x in input_region)

def find_proj(bounded_regions):
    proj_regions = []
    # print(bounded_regions)
    for i in range(len(bounded_regions)):
        region = bounded_regions[i]
        proj_regions.append([])
        for p1 in region:
            if p1[2] < 0: continue
            for p2 in region:
                if p2[2] > 0: continue
                v = [p2[0]-p1[0],
                     p2[1]-p1[1],
                     p2[2]-p1[2]]
                t = -p1[2]/v[2]
                proj_point = [p1[0] + t*v[0],
                              p1[1] + t*v[1]]
                proj_regions[i].append(proj_point)
    return proj_regions

def power_cells(C_3D, bbox):
    minpt, maxpt = bbox
    extent = find_extent([minpt,maxpt])
    smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    boundary = np.array([smallpt, [bigpt[0],smallpt[1],smallpt[2]],
                     [smallpt[0],bigpt[1],smallpt[2]],
                     [smallpt[0],smallpt[1],bigpt[2]],
                     [bigpt[0],bigpt[1],smallpt[2]],
                     [smallpt[0],bigpt[1],bigpt[2]],
                     [bigpt[0],smallpt[1],bigpt[2]],
                     bigpt])
    diagram = sp.Voronoi(np.concatenate((C_3D,boundary)))
    bounded_regions = [[diagram.vertices[j] for j in region]
                       for region in diagram.regions
                       if region != [] and not unbounded(region)]
    proj_regions = find_proj(bounded_regions)
    return [sg.MultiPoint(region).convex_hull for region in proj_regions
            if region != []]

def power_cells_fromfile(filename):
    C_3D, A, assign_pairs, bbox = Parse(filename)
    return power_cells(C_3D, bbox)

    
# if __name__ == '__main__':
#     if len(sys.argv) < 3:
#         print("Use: ", sys.argv[0], "[file name] [output file name]")
#         exit(-1)
#     C_3D, A, assign_pairs, bbox = Parse(sys.argv[1])
#     # Parse_and_plot_boundary(sys.argv[2])
#     plot_helper(C_3D, A, assign_pairs, bbox, sys.argv[2])
    
