import copy
from math import *
from typing import List
from pygame import *
import pygame
from classes import *
import loadFile
from loadFile import *
from matrix import *
from pygameManager import *

pygame.init()
loadFile.init()

#functions
def drawTriangle(tri:Triangle, width:float, col=(-1,-1,-1)):
    if col == (-1,-1,-1):
        col = tri.col
    draw.line(SCREEN, col, (WIDTH - tri.p[0].x, HEIGHT-tri.p[0].y), (WIDTH - tri.p[1].x, HEIGHT-tri.p[1].y), width)
    draw.line(SCREEN, col, (WIDTH - tri.p[0].x, HEIGHT-tri.p[0].y), (WIDTH - tri.p[2].x, HEIGHT-tri.p[2].y), width)
    draw.line(SCREEN, col, (WIDTH - tri.p[1].x, HEIGHT-tri.p[1].y), (WIDTH - tri.p[2].x, HEIGHT-tri.p[2].y), width)
def fillTriangle(tri:Triangle, col=(-1,-1,-1)):
    if col == (-1,-1,-1):
        col = tri.col
    draw.polygon(SCREEN, col, tri.onlyXY())

def triangleClipAgainstPlane(planeP:Vec3d, planeN:Vec3d, inTri:Triangle):
    outTri1:Triangle = Triangle()
    outTri2:Triangle = Triangle()

    planeN.normalise()

    def dist(p:Vec3d):
        return (planeN.x * p.x + planeN.y * p.y + planeN.z * p.z - vecDotProduct(planeN, planeP))
    
    insidePoints:Vec3d = [Vec3d(), Vec3d(), Vec3d()]
    outsidePoints:Vec3d = [Vec3d(), Vec3d(), Vec3d()]
    nInsidePointCount = 0
    nOutsidePointCount = 0

    d0:float = dist(inTri.p[0])
    d1:float = dist(inTri.p[1])
    d2:float = dist(inTri.p[2])

    if d0 > 0:
        insidePoints[nInsidePointCount] = inTri.p[0]
        inTri.p[0].outside = False
        nInsidePointCount +=1
    else:
        outsidePoints[nOutsidePointCount] = inTri.p[0]
        inTri.p[0].outside = True
        nOutsidePointCount +=1

    if d1 > 0:
        insidePoints[nInsidePointCount] = inTri.p[1]
        inTri.p[1].outside = False
        nInsidePointCount +=1
    else:
        outsidePoints[nOutsidePointCount] = inTri.p[1]
        inTri.p[1].outside = True
        nOutsidePointCount +=1
    
    if d2 > 0:
        insidePoints[nInsidePointCount] = inTri.p[2]
        inTri.p[2].outside = False
        nInsidePointCount +=1
    else:
        outsidePoints[nOutsidePointCount] = inTri.p[2]
        inTri.p[2].outside = True
        nOutsidePointCount +=1
    x = 1
    if nInsidePointCount == 0:
        return 0, [] #no returned triangles are valid
    if nInsidePointCount == 3:
        outTri1 = inTri
        return 1, [outTri1] # just the one returned original triangle is valid
    
    if nInsidePointCount == 1 and nOutsidePointCount == 2:
        outTri1.col = "RED"
        outTri1.p[0] = insidePoints[0]
        outTri1.p[1] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])
        outTri1.p[2] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[1])
        return 1, [copy.deepcopy(outTri1)]
    
    if nInsidePointCount == 2 and nOutsidePointCount == 1:
        outTri1.col = "GREEN"
        outTri2.col = "PURPLE"

        outTri1.p[0] = insidePoints[0]
        outTri1.p[1] = insidePoints[1]
        outTri1.p[2] = vecIntersectPlane(planeP, planeN, insidePoints[0], outsidePoints[0])

        outTri2.p[0] = insidePoints[1]
        outTri2.p[1] = outTri1.p[2]
        outTri2.p[2] = vecIntersectPlane(planeP, planeN, insidePoints[1], outsidePoints[0])
        return 2, [copy.deepcopy(outTri1), copy.deepcopy(outTri2)] #both returned triangles are valid

    #lighting functions
def luminanceToGreyscale(lum:float):
    lum = math.clamp(lum, 0, 1)
    value = int(lum*255)
    return (value, 0, 0)

#Meshes
videoShip = meshes[0]

#camera
vCamera:Vec3d = Vec3d(0, 0, 0)
vLookDir:Vec3d = Vec3d(0, 0, 1)
fYaw:float = 0
# fRoll:float = 0

#matrices
matProj = matrixMakeProjection(90, HEIGHT / WIDTH_, 0.1, 1000)

fTheta = 0
def updateTheta():
    global fTheta
    fTheta += 0.0001
    return fTheta

#Debug Variables
showWireframe = True

matWorld:Mat4x4 = Mat4x4()



done = False
while not done:
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True

    vUp:Vec3d = Vec3d(0, 1, 0)

    vForward:Vec3d = vecMul(vLookDir, 0.1)
    vRight:Vec3d = vecCrossProduct(vUp, vForward)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        vCamera = vecAdd(vCamera, vForward)
    if keys[pygame.K_s]:
        vCamera = vecSub(vCamera, vForward)
    if keys[pygame.K_a]:
        vCamera = vecAdd(vCamera, vRight)
    if keys[pygame.K_d]:
        vCamera = vecSub(vCamera, vRight)
    if keys[pygame.K_LSHIFT]:
        vCamera.y -= .1
    if keys[pygame.K_SPACE]:
        vCamera.y += .1
    if keys[pygame.K_LEFT]:
        fYaw -= 0.01
    if keys[pygame.K_RIGHT]:
        fYaw += 0.01
    # if keys[pygame.K_UP]:
    #     fRoll -= 0.01
    # if keys[pygame.K_DOWN]:
    #     fRoll += 0.01

    #draw triangles
    trisToDraw = []
    for tri in videoShip.tris:
        triProjected:Triangle = Triangle()
        triTransformed:Triangle = Triangle()
        triViewed:Triangle = Triangle()

        matTrans:Mat4x4 = matrixMakeTranslation(0, 0, 6)
        
        matWorld = matrixMakeIdentity()
        matWorld = matrixMultiplyMatrix(matWorld, matTrans)

        vTarget:Vec3d = Vec3d(0, 0, 1)
        matCameraYaw:Mat4x4 = matrixMakeRotationY(fYaw)
        vLookDir = matrixMultiplyVector(matCameraYaw, vTarget)
        vTarget = vecAdd(copy.deepcopy(vCamera), vLookDir)

        matCamera:Mat4x4 = matrixPointAt(vCamera, vTarget, vUp)
        matView:Mat4x4 = matrixQuickInverse(matCamera)

        triTransformed.p[0] = matrixMultiplyVector(matWorld, tri.p[0])
        triTransformed.p[1] = matrixMultiplyVector(matWorld, tri.p[1])
        triTransformed.p[2] = matrixMultiplyVector(matWorld, tri.p[2])


        #get normal
        normal:Vec3d = Vec3d()
        line1:Vec3d = Vec3d()
        line2:Vec3d = Vec3d()

        line1 = vecSub(triTransformed.p[1], triTransformed.p[0])
        line2 = vecSub(triTransformed.p[2], triTransformed.p[0])

        normal = vecCrossProduct(line1, line2)
        normal.normalise()

        vCameraRay:Vec3d = vecSub(triTransformed.p[0], vCamera)

        if vecDotProduct(normal, vCameraRay) < 0:
            # Illumination: simple directional light
            lightDirection = Vec3d(0, 0, -1)
            lightDirection.normalise()
            dp = max(0.1, vecDotProduct(lightDirection, normal))  # Clamp minimum brightness
            triTransformed.col = luminanceToGreyscale(dp)

            # World space -> View space
            triViewed.p[0] = matrixMultiplyVector(matView, triTransformed.p[0])
            triViewed.p[1] = matrixMultiplyVector(matView, triTransformed.p[1])
            triViewed.p[2] = matrixMultiplyVector(matView, triTransformed.p[2])
            triViewed.col = triTransformed.col

            # Clip viewed triangle against the near plane
            clipped: List[Triangle] = [Triangle(), Triangle()]
            nClippedTriangles = 0
            nClippedTriangles, clipped = triangleClipAgainstPlane(Vec3d(0, 0, 0.2), Vec3d(0, 0, 1), triViewed)
            for n in range(nClippedTriangles):
                triClipped = copy.deepcopy(clipped[n])

                # Project the triangle from 3D -> 2D
                triProjected.p[0] = matrixMultiplyVector(matProj, triClipped.p[0])
                triProjected.p[1] = matrixMultiplyVector(matProj, triClipped.p[1])
                triProjected.p[2] = matrixMultiplyVector(matProj, triClipped.p[2])

                # Normalize points
                triProjected.p[0] = vecDiv(triProjected.p[0], triProjected.p[0].w)
                triProjected.p[1] = vecDiv(triProjected.p[1], triProjected.p[1].w)
                triProjected.p[2] = vecDiv(triProjected.p[2], triProjected.p[2].w)

                # Scale into view
                vOffsetView = Vec3d(1, 1, 0)
                triProjected.p[0] = vecAdd(vecMul(triProjected.p[0], 0.5 * WIDTH_), vOffsetView)
                triProjected.p[1] = vecAdd(vecMul(triProjected.p[1], 0.5 * WIDTH_), vOffsetView)
                triProjected.p[2] = vecAdd(vecMul(triProjected.p[2], 0.5 * WIDTH_), vOffsetView)

                # Store projected triangle for drawing
                triProjected.col = triClipped.col
                trisToDraw.append(copy.deepcopy(triProjected))
            
    
    trisToDraw.sort(key=lambda x: (x.p[0].z + x.p[1].z + x.p[2].z)/3, reverse=True)
    SCREEN.fill("WHITE")
    for tri in trisToDraw:
        clipped:List[Triangle] = [Triangle(), Triangle()]
        listTriangles = []
        listTriangles.append(tri)
        nNewTriangles = 1

        for p in range(4):
            listTrianglesNew = []
            for test in listTriangles:
                match p:
                    case 0: 
                        nTrisToAdd, clipped = triangleClipAgainstPlane(Vec3d(0, 0, 0), Vec3d(0, 1, 0), test)
                    case 1: 
                        nTrisToAdd, clipped = triangleClipAgainstPlane(Vec3d(0, HEIGHT - 1, 0), Vec3d(0, -1, 0), test)
                    case 2: 
                        nTrisToAdd, clipped = triangleClipAgainstPlane(Vec3d(0, 0, 0), Vec3d(1, 0, 0), test)
                    case 3:
                        nTrisToAdd, clipped = triangleClipAgainstPlane(Vec3d(WIDTH-1, 0, 0), Vec3d(-1, 0, 0), test)
                listTrianglesNew.extend(clipped[:nTrisToAdd])
            listTriangles = listTrianglesNew
        
        for tri in listTriangles:
            fillTriangle(tri)
            drawTriangle(tri, 3)


    display.set_caption("3D Render Engine | " + str(CLOCK.get_fps().__round__(0)) + "FPS")
    display.flip()
    CLOCK.tick(100)
