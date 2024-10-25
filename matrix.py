from classes import Mat4x4, Vec3d
from math import *
from vector import *

def matrixMultiplyVector(m:Mat4x4, i:Vec3d):
    v:Vec3d = Vec3d()
    v.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + i.w * m.m[3][0]
    v.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + i.w * m.m[3][1]
    v.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + i.w * m.m[3][2]
    v.w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + i.w * m.m[3][3]
    return v

def matrixMakeIdentity():
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = 1
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    return matrix

def matrixMakeTranslation(x:float, y:float, z:float):
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = 1
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    matrix.m[3][0] = x
    matrix.m[3][1] = y
    matrix.m[3][2] = z
    return matrix

def matrixMakeRotationX(fAngleRad:float):
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = cos(fAngleRad)
    matrix.m[1][2] = sin(fAngleRad)
    matrix.m[2][1] = -sin(fAngleRad)
    matrix.m[2][2] = cos(fAngleRad)
    matrix.m[3][3] = 1
    return matrix

def matrixMakeRotationZ(fAngleRad:float):
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = cos(fAngleRad)
    matrix.m[0][1] = sin(fAngleRad)
    matrix.m[1][0] = -sin(fAngleRad)
    matrix.m[1][1] = cos(fAngleRad)
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    return matrix

def matrixMakeRotationY(fAngleRad:float):
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = cos(fAngleRad)
    matrix.m[0][2] = sin(fAngleRad)
    matrix.m[2][0] = -sin(fAngleRad)
    matrix.m[1][1] = 1
    matrix.m[2][2] = cos(fAngleRad)
    matrix.m[3][3] = 1
    return matrix

def matrixMakeProjection(fFovDegrees:float, fAspectRatio:float, fNear:float, fFar:float):
    fFovRad:float = 1/tan(fFovDegrees*0.5/180*pi)
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = 1/fAspectRatio*fFovRad
    matrix.m[1][1] = fFovRad
    matrix.m[2][2] = fFar/(fFar-fNear)
    matrix.m[3][2] = (-fFar*fNear)/(fFar-fNear)
    matrix.m[2][3] = 1
    matrix.m[3][3] = 0

    #  x y z w
    #x 0 0 0 0
    #y 0 0 0 0
    #z 0 0 0 0
    #w 0 0 0 0
    return matrix

def matrixMultiplyMatrix(m1:Mat4x4, m2:Mat4x4):
    matrix:Mat4x4 = Mat4x4()
    for c in range(4):
        for r in range(4):
            matrix.m[r][c] = (
                m1.m[r][0] * m2.m[0][c] +
                m1.m[r][1] * m2.m[1][c] +
                m1.m[r][2] * m2.m[2][c] +
                m1.m[r][3] * m2.m[3][c]
            )

    return matrix

def matrixPointAt(pos:Vec3d, target:Vec3d, up:Vec3d):
    newForward:Vec3d = vecSub(target, pos)
    newForward.normalise()

    a:Vec3d = vecMul(newForward, vecDotProduct(up, newForward))
    newUp:Vec3d = vecSub(up, a)
    newUp.normalise()

    newRight:Vec3d = vecCrossProduct(newUp, newForward)

    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = newRight.x
    matrix.m[1][0] = newUp.x
    matrix.m[2][0] = newForward.x
    matrix.m[3][0] = pos.x

    matrix.m[0][1] = newRight.y
    matrix.m[1][1] = newUp.y
    matrix.m[2][1] = newForward.y
    matrix.m[3][1] = pos.y

    matrix.m[0][2] = newRight.z
    matrix.m[1][2] = newUp.z
    matrix.m[2][2] = newForward.z
    matrix.m[3][2] = pos.z

    matrix.m[0][3] = 0
    matrix.m[1][3] = 0
    matrix.m[2][3] = 0
    matrix.m[3][3] = 1
    return matrix


def matrixQuickInverse(m:Mat4x4):
    matrix:Mat4x4 = Mat4x4()
    matrix.m[0][0] = m.m[0][0] 
    matrix.m[0][1] = m.m[1][0]
    matrix.m[0][2] = m.m[2][0] 
    matrix.m[0][3] = 0
    matrix.m[1][0] = m.m[0][1] 
    matrix.m[1][1] = m.m[1][1]
    matrix.m[1][2] = m.m[2][1] 
    matrix.m[1][3] = 0
    matrix.m[2][0] = m.m[0][2] 
    matrix.m[2][1] = m.m[1][2]
    matrix.m[2][2] = m.m[2][2] 
    matrix.m[2][3] = 0
    matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] * matrix.m[1][0] + m.m[3][2] * matrix.m[2][0])
    matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] * matrix.m[1][1] + m.m[3][2] * matrix.m[2][1])
    matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] * matrix.m[1][2] + m.m[3][2] * matrix.m[2][2])
    matrix.m[3][3] = 1
    return matrix
