import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.spatial as sp
import shapely.geometry as sg
from matplotlib import colors as mcolors
color_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
# colors = [x for x in color_dict if x not in {"w",'aliceblue','antiquewhite','azure','beige','bisque','blanchedalmond'}]
colors = [
'red',                #ff0000 = 255   0   0
'web-green',          #00c000 =   0 192   0
'web-blue',         #0080ff =   0 128 255
'dark-magenta',       #c000ff = 192   0 255
'dark-cyan',         #00eeee =   0 238 238
'dark-orange',        #c04000 = 192  64   0
'dark-yellow',        #c8c800 = 200 200   0
'royalblue',          #4169e1 =  65 105 225
'goldenrod',          #ffc020 = 255 192  32
'dark-spring-green',  #008040 =   0 128  64
'purple',             #c080ff = 192 128 255
'steelblue',          #306080 =  48  96 128
'dark-red',           #8b0000 = 139   0   0
'dark-chartreuse',    #408000 =  64 128   0
'orchid',             #ff80ff = 255 128 255
'aquamarine',         #7fffd4 = 127 255 212
'brown',              #a52a2a = 165  42  42
'yellow',          #ffff00 = 255 255   0
'turquoise'
'light-red',        #f03232 = 240  50  50
'light-green',        #90ee90 = 144 238 144
'light-blue',         #add8e6 = 173 216 230
'light-magenta',      #f055f0 = 240'85 240
'light-cyan',         #e0ffff = 224 255 255
'light-goldenrod',    #eedd82 = 238 221 130
'light-pink',         #ffb6c1 = 255 182 193
'light-turquoise',    #afeeee = 175 238 238
'gold',               #ffd700 = 255 215   0
'green',              #00ff00 =   0 255   0
'dark-green',         #006400 =   0 100   0
'spring-green',       #00ff7f =   0 255 127
'forest-green',     #228b22 =  34 139  34
'sea-green',          #2e8b57 =  46 139  87
'blue',               #0000ff =   0   0 255
'dark-blue',          #00008b =   0   0 139
'midnight-blue',      #191970 =  25  25 112
'navy',               #000080 =   0   0 128
'medium-blue',        #0000cd =   0   0 205
'skyblue',            #87ceeb = 135 206 235
'cyan',               #00ffff =   0 255 255
'magenta',            #ff00ff = 255   0 255
'dark-turquoise',     #00ced1 =   0 206 209
'dark-pink',          #ff1493 = 255  20 147
'coral',              #ff7f50 = 255 127  80
'light-coral',        #f08080 = 240 128 128
'orange-red',         #ff4500 = 255  69   0
'salmon',             #fa8072 = 250 128 114
'dark-salmon',        #e9967a = 233 150 122
'khaki',              #f0e68c = 240 230 140
'dark-khaki',         #bdb76b = 189 183 107
'dark-goldenrod',     #b8860b = 184 134  11
'beige',              #f5f5dc = 245 245 220
'olive',              #a08020 = 160 128  32
'orange',             #ffa500 = 255 165   0
'violet',             #ee82ee = 238 130 238
'dark-violet',        #9400d3 = 148   0 211
'plum',               #dda0dd = 221 160 221
'dark-plum',          #905040 = 144  80  64
'dark-olivegreen',    #556b2f =  85 107  47
'orangered4',         #801400 = 128  20   0
'brown4',             #801414 = 128  20  20
'sienna4',            #804014 = 128  64  20
'orchid4',            #804080 = 128  64 128
'mediumpurple3'      #8060c0 = 128  96 192
    ]

    

        
        
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

def PlotAll(C, A, assignment, bounded_regions, bbox, output):
    diagram = sp.Voronoi(C)
    f = open(output, "w")
    # sp.voronoi_plot_2d(diagram)
    f.write(str(len(C))+" "+str(len(A))+"\n")
    for i in range(len(C)):
        f.write(str(C[i][0])+" "+str(C[i][1])+" "+str(colors[i])+"\n")
    for j in range(len(A)):
        f.write(str(A[j][0])+" "+str(A[j][1])+" "+str(colors[assignment[j]])+"\n")


    for r in bounded_regions:
        if bounded_regions[r] == []: continue
        region = bounded_regions[r]
        convex_hull = sg.MultiPoint(region).convex_hull
        x,y = convex_hull.exterior.xy
        for i in range(len(x)):
            f.write(str(x[i])+","+str(y[i])+" ")
        f.write("\n") #x, y, color = 'black')
    Plot_extra_lines(C, f)
    f.close()
    # plt.axis([bbox[0][0],bbox[1][0], bbox[0][1],bbox[1][1]])
    # plt.show(block=True)



def find_bounding_box(S):
    return [[f(p[i] for p in S) for i in [0,1,2]] for f in [min, max]]

def find_extent(bbox):
    minpt, maxpt = bbox
    return [maxpt[i] - minpt[i] for i in range(3)]

def EuclidExample2(ncenters):
    vec_centers = np.random.randn(3, ncenters)

    C = np.array([[vec_centers[0][i],vec_centers[1][i],vec_centers[2][i]]
                  for i in range(len(vec_centers[0]))])

    bbox = find_bounding_box(C)

    def unbounded(input_region): return any(x==-1 for x in input_region)
    ## insert points to remove
    ## infinite regions
    minpt, maxpt = bbox
    extent = find_extent([minpt,maxpt])
    smallpt, bigpt = [minpt[i]-extent[i] for i in range(3)], [maxpt[i]+extent[i] for i in range(3)]
    # print(boundary)
    boundary = np.array([smallpt, [bigpt[0],smallpt[1],smallpt[2]],
                         [smallpt[0],bigpt[1],smallpt[2]],
                         [smallpt[0],smallpt[1],bigpt[2]],
                         [bigpt[0],bigpt[1],smallpt[2]],
                         [smallpt[0],bigpt[1],bigpt[2]],
                         [bigpt[0],smallpt[1],bigpt[2]],
                         bigpt])
    print(boundary)
    print(C)
    diagram = sp.Voronoi(np.concatenate((C,boundary)))
    bounded_regions = [[diagram.vertices[j] for j in region] for region in diagram.regions if region != [] and not unbounded(region)]
    return bounded_regions # OrderRegions(C,
                        
    # return sp.Voronoi(C)

def find_proj(bounded_regions):
    proj_regions = {}
    # print(bounded_regions)
    for i in range(len(bounded_regions)):
        region = bounded_regions[i]
        proj_regions[i] = []
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

def plot_regions(proj_regions):

    for r in proj_regions:
        if proj_regions[r] == []: continue
        region = proj_regions[r]
        convex_hull = sg.MultiPoint(region).convex_hull
        x,y = convex_hull.exterior.xy
        plt.plot(x, y, color = 'black')


def Plot_extra_lines(C,f):
    diagram = sp.Voronoi(C)
    
    

def unbounded(input_region): return any(x==-1 for x in input_region)
## insert points to remove
## infinite regions

def plot_helper(C_3D, A, assign_pairs,bbox, outputfile):
    C = [[p[0],p[1]] for p in C_3D]
    # bbox = find_bounding_box(C_3D)
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
    PlotAll(C,A,assign_pairs, proj_regions, bbox, outputfile)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Use: ", sys.argv[0], "[file name] [output file name]")
        exit(-1)
    C_3D, A, assign_pairs, box = Parse(sys.argv[1])
    # Parse_and_plot_boundary(sys.argv[2])
    plot_helper(C_3D, A, assign_pairs, box, sys.argv[2])
    
