import copy
from classes import Vec3d
from math import *


def vecAdd(v1:Vec3d, v2:Vec3d):
    return Vec3d(v1.x+v2.x, v1.y+v2.y, v1.z+v2.z)
def vecSub(v1:Vec3d, v2:Vec3d):
    return Vec3d(v1.x-v2.x, v1.y-v2.y, v1.z-v2.z)
def vecDiv(v1:Vec3d, k:float):
    v = copy.deepcopy(v1)
    return Vec3d(v.x / k, v.y / k, v.z / k, v.w)
def vecMul(v1:Vec3d, k:float):
    return Vec3d(v1.x*k, v1.y*k, v1.z*k)
def vecNormalise(v:Vec3d):
    vec:Vec3d = copy.deepcopy(v)
    l = sqrt(vec.x*vec.x + vec.y*vec.y + vec.z*vec.z)
    if l > 0:
        vec.x /= l
        vec.y /= l
        vec.z /= l
    return vec
def vecDotProduct(v1:Vec3d, v2:Vec3d):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
def vecCrossProduct(v1:Vec3d, v2:Vec3d):
    v:Vec3d = Vec3d()
    v.x = v1.y * v2.z - v1.z * v2.y
    v.y = v1.z * v2.x - v1.x * v2.z
    v.z = v1.x * v2.y - v1.y * v2.x
    return v
def vecIntersectPlane(planeP:Vec3d, planeN:Vec3d, lineStart:Vec3d, lineEnd:Vec3d):
    planeN.normalise()
    planeD:float = -vecDotProduct(planeN, planeP)
    ad:float = vecDotProduct(lineStart, planeN)
    bd:float = vecDotProduct(lineEnd, planeN)
    t:float = (-planeD - ad)/(bd - ad)
    lineStartToEnd:Vec3d = vecSub(lineEnd, lineStart)
    lineToIntersect:Vec3d = vecMul(lineStartToEnd, t)
    return vecAdd(lineStart, lineToIntersect)
