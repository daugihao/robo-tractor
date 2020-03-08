from math import atan, sqrt, pi

OFFSET = -120.0
GAIN = 1.0/24.0
EPS = 1e-5


def convertAcc(raw, mode):
    g = tuple([GAIN*(axis + OFFSET) for axis in raw])
    if mode == 0:
        return g
    if mode == 1:
        pitch = 180*atan(g[0]/(sqrt(g[1]*g[1] + g[2]*g[2])+EPS))/pi
        roll = 180*atan(g[1]/(sqrt(g[0]*g[0] + g[2]*g[2])+EPS))/pi
        yaw = 0
        return tuple([pitch, roll, yaw])

