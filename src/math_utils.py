from math import sin, cos
from manim.typing import *

def rotate(vector: Point2DLike, alpha: float) ->Point2D:
    x = vector[0]
    y = vector[1]

    x2 = cos(alpha)*x -sin(alpha)*y
    y2 = sin(alpha)*x + cos(alpha) *y

    return (x2,y2)