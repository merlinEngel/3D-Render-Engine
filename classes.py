from math import sqrt
from pygameManager import HEIGHT, WIDTH
from dataclasses import dataclass, field
from typing import List


@dataclass
class Vec3d:
    x:float = 0
    y:float = 0
    z:float = 0
    w:float = 1

    outside:bool = False

    def getScreenCoordinate(self):
        return (WIDTH - self.x, HEIGHT-self.y)
    
    def normalise(self):
        l = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        if l > 0:
            self.x /= l
            self.y /= l
            self.z /= l

@dataclass
class Triangle:
    p: List[Vec3d] = field(default_factory=lambda: [Vec3d(), Vec3d(), Vec3d()])
    col = (255, 255, 255)

    def onlyXY(self):
        return [point.getScreenCoordinate() for point in self.p]


@dataclass
class Mesh:
    tris:List[Triangle]

@dataclass
class Mat4x4:
    m:List[List[float]] = field(default_factory=lambda: [[0.0 for _ in range(4)] for _ in range(4)])