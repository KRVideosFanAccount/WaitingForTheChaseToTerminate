from manim import *
from manim.typing import *
from math import pi
import numpy as np
import math_utils as mu

class ChangeGraphLayout(Animation):
    """ Animation that transforms a graph g_dom into a graph g_img with the same set of vertices. This animation tries to prevent vertices getting close during the animation (If vertices get too close and there is a tip in between, the tip will wiggle unpleasantly).
    This class interpolates the graph centers, and for each vertex it's distance to the center and angle wrt. the center
    
    Parameters
    ----------
    g_dom
        graph to be transformed
    g_img
        graph to be transformed into
    suspend_mobject_updating
        parameter of the base class animation. Should be set to False, otherwise the edges won't update during the animation.
    args, use_override, kwargs:
        parameters of the base class animation.
    """

    def __init__(self, g_dom, g_img, suspend_mobject_updating = False, *args, use_override=True, **kwargs):
        super().__init__(mobject = g_dom, suspend_mobject_updating = suspend_mobject_updating, args = args, use_override = use_override, kwargs = kwargs)
        self.g_img = g_img
        self.g_dom = g_dom

        if not set(g_img.vertices) == set(g_dom.vertices):
            raise RuntimeError("ChangeGraphLayout requires the same set of vertices")

    
    def _setup_scene(self, scene):
        super()._setup_scene(scene)
        self.g_dom = self.g_dom.copy()


    def interpolate(self,alpha: float):
        alpha = self.rate_func(alpha)
        p1 = self.g_dom.vertices
        p2 = self.g_img.vertices     

        layout = dict()

        for vert in p1:
            dir1 = p1[vert].get_center()-self.g_dom.get_center()
            angle1 = np.angle(dir1[0] + dir1[1]*(1j))
            len1 = np.linalg.norm(dir1)

            dir2 = p2[vert].get_center() - self.g_img.get_center()
            angle2 = np.angle(dir2[0] + dir2[1]*(1j))
            len2 = np.linalg.norm(dir2)

            if angle2 - angle1 > pi:
                angle2 = angle2 - 2*pi
            elif angle1 - angle2 > pi:
                angle1 = angle1 - 2*pi

            direction = mu.rotate([1,0], (1-alpha)*angle1 + alpha*angle2)
            direction = ((1-alpha)*len1+alpha* len2)*np.array(direction)
            direction = (alpha*self.g_img.get_center() + (1-alpha) * self.g_dom.get_center() + [direction[0], direction[1], 0])
            layout[vert] = direction


        self.mobject.change_layout(layout)

