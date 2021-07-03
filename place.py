import sys
import numpy as np
import math
    
# 1. get the longest edge of the polygon
def shift_by_long_edge(points):
    edges = []
    for i in range(len(points)):
        x1,y1 = points[i]
        x2,y2 = points[(i+1)%len(points)]
        edges.append((x1-x2)**2 + (y1-y2)**2)
    index = np.argmax(edges)
    return points[index:] + points[:index]

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# I should first get it into standing position
def transform_horizon(points):
    theta = -math.atan2(points[1][1]-points[0][1], points[1][0]-points[0][0])
    res = [rotate(points[0], p, theta) for p in points]
    return res, theta

def untransform(points, theta, origin):
    return [rotate(origin, p, -theta) for p in points]

def intersect(y, points):
    res = []
    for i in range(len(points)):
        x1,y1 = points[i]
        x2,y2 = points[(i+1)%len(points)]
        if min(y1,y2) <= y <= max(y1,y2):
            x = (y-y1)/(y2-y1)*(x2-x1) + x1
            res.append(x)
    return sorted(res)

def place(points, width, height):
    h = points[0][1]
    prevxs = (points[0][0], points[1][0])
    pos = []
    while True:
        h -= height
        xs = intersect(h, points)
        if len(xs) != 2: break
#         print('intersects x:', xs)
        xstart = max(xs[0], prevxs[0])
        xend = min(xs[1], prevxs[1])
#         print('prevxs', prevxs)
        # compute the position
        for i in range(round((xend - xstart) // width)):
            offset = (xend - xstart) % width / 2
            pos.append((xstart + offset + i * width, h))
        prevxs = xs
    return pos

def place_solar_panel(polygon, w, h):
    points1 = shift_by_long_edge(polygon)
    points2, theta = transform_horizon(points1)
    pos = place(points2, w, h)
    # convert pos into rectangle points
    rects2 = [((x,y), (x+w,y), (x+w,y+h), (x,y+h)) for x,y in pos]
    rects1 = [untransform(r, theta, points1[0]) for r in rects2]
    return rects1

