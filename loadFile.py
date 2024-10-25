from classes import *
import os

def __meshFromObjectFile(path:str):
    verts = []
    tris = []
    with open(path, 'r') as file:
        for line in file:
            parts = line.split()
            junk = parts[0]
            if junk.__contains__('v'):
                verts.append(Vec3d(float(parts[1]), float(parts[2]), float(parts[3])))
            if junk.__contains__('f'):
                tris.append(Triangle([verts[int(parts[1])-1], verts[int(parts[2])-1], verts[int(parts[3])-1]]))
                
    return Mesh(tris)

meshes = []
def init():
    global meshes
    for file in os.listdir("objects"):
        meshes.append(__meshFromObjectFile("objects/" + file))