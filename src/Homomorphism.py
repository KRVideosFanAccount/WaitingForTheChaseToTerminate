from typing import *
from math import sin, pi

from manim import *
from flexible_dashed_line import FlexibleDashedLine
from math_utils import rotate
from coolerDiGraph import CoolDiGraph

from Style import err as err_color

import numpy as np

from ChangeGraphLayout import ChangeGraphLayout

class Homomorphism:
    """ Class representing a mapping of the vertices of g_dom to the vertices of g_img. Can be used to represent a homomorphism, should also be used to represent a mapping that is not a homomorphism. 

    Parameters
    ----------

    g_dom
        The domain of the homomorphism
    g_img
        The range/image of the homomorphism
    hom
        the mapping, represented as a set of (ordered) tuples of(v_dom, v_img)
    check_hom
        toggles, whether the __init__ should check if hom is a homomorphism. Defaults to not checking, should be used for actual homomorphisms.
    edge_attribs
        list of attributes in g_dom and g_img that represent edges. Used to check validity of the homomorphism.

    Methods
    -------

    apply
        applies the homomorphism to the given vertex v. Returns the first u such that (v,u) is in hom. Doesn't check whether there are multiple such u. Doesn't check whether u is in the vertices of g_img.

    check_hom
        checks whether hom is an homomorphism. Uses edge_attribs to iterate over all edges
    
    create_organized_graph
        creates a copy of g_dom which has a layout analogously to g_img. If multiple vertices of g_dom are mapped to the same vertex in g_img, these nodes are arranged in a circle.
    """
    def __init__(self, g_dom:DiGraph, g_img:DiGraph, hom:Sequence[tuple[Hashable, Hashable]]|None, check_hom = False, edge_attribs=['edges']):

        self.g_dom = g_dom
        self.g_img = g_img
        if hom:
            self.hom = hom
        else:
            self.hom = [] #TODO write a function that finds a homomorphism
        self.edge_attribs = edge_attribs

        if check_hom:
            err = self.check_hom()
            if err:
                raise RuntimeError(err)


    def apply(self, *varr) -> Hashable|list[Hashable] |None:
        ret = []
        for vertex in varr:
            for (x,y) in self.hom:
                if x == vertex:
                    ret.append(y)
        if len(ret) == 1:
            return ret[0]
        else:
            return ret

    def check_edge_maps(self, edge, edge_attrib):
        edge_img = []
        for vert in edge:
            edge_img.append(self.apply(vert))

        if tuple(edge_img) not in getattr(self.g_img, edge_attrib):
            return False

        l_dom_label = self.g_dom.edge_labels[edge].get_tex_string()

        l_img_label = self.g_img.edge_labels[tuple(edge_img)].get_tex_string()

        if l_dom_label != l_img_label:
            return False

        return True


    def check_hom(self) -> str|None:
        for (x,y) in self.hom:
            if x not in self.g_dom.vertices:
                return "Homomorphism cannot be applied because " + str(x) + " is not a vertex of g_dom"
            if y not in self.g_img.vertices:
                return "Homomorphism cannot be applied because " + str(y) + " is not a vertex of g_img"

        for x in self.g_dom.vertices:
            for (y,z) in self.hom:
                if x==y:
                    break
            else:
                return "Homomorphism is incomplete. Missing image for " + str(x)

        for p in self.edge_attribs:
            for edge in getattr(self.g_dom, p):
                for vert in edge:
                    if vert not in self.g_dom.vertices:
                        return "Homomorphism cannot be applied because " + str(vert) + " is not a vertex of g_dom"
                    if self.apply(vert) not in self.g_img.vertices:
                        return "Homomorphism cannot be applied because " + str(self.apply(vert)) + " is not a vertex of g_img"

                if not self.check_edge_maps(edge, p):
                    return "Homomorphism cannot be applied because (" + str(self.apply(edge)[0]) +"," + str(self.apply(edge)[1]) + ") is not an edge in g_img for edge" +str(edge) + "."
                


    def create_organized_graph(self, graph_offset = None, space_same=0.15):
        org_graph = self.g_dom.copy()

        if not graph_offset:
            graph_offset = self.g_dom.get_center() - self.g_img.get_center()

        inverse_hom = dict()
        for v_dom in org_graph.vertices:
            v_img = self.apply(v_dom)
            if v_img not in inverse_hom.keys():
                inverse_hom[v_img] = []
            inverse_hom[v_img].append(v_dom)

        layout = dict()
        for (v_img, v_doms) in inverse_hom.items():
            c = len(v_doms)
            if c == 1:
                v_dom = v_doms[0]
                layout[v_dom] = self.g_img.vertices[v_img].get_center()+graph_offset
            else:
                circumference = c*space_same #contains the required circumference
                orientation = dict() #contains the angle of each v_dom with respect to (1,0)
                sum_orientation = 0.0

                for v_dom in v_doms:
                    circumference = circumference + 2*self.g_dom.vertices[v_dom].radius
                    rel_pos = self.g_dom.vertices[v_dom].get_center() - self.g_dom.get_center()
                    orientation[v_dom] = np.angle(1 , rel_pos[0] + rel_pos[1]*1j)
                    sum_orientation = sum_orientation + orientation[v_dom]

                #This is the radius of a circle that if you space c points evenly then they have a distance of 2*.radius + space_same.
                #Two points on this circle form an isosceles triangle, using half of .radius + space_same results in a right triangle and an angle of half of 2pi/c
                alpha = 2*pi/c
                radius = circumference/(2*c*sin(alpha/2))
                
                #fix orientation
                for (v_dom,o) in orientation.items():
                    o = o - (sum_orientation/c)
                    orientation[v_dom] = o

                verts_dom = orientation.keys()
                verts_dom = sorted(verts_dom, key=lambda vert : orientation[vert])
                

                d = rotate((radius, 0), orientation[verts_dom[0]])

                

                for i in range(len(inverse_hom[v_img])):
                    v_dom = verts_dom[i]
                    d2 = rotate(d, i*alpha)
                    d2 = (d2[0], d2[1], 0)
                    layout[v_dom] = self.g_img.vertices[v_img].get_center() + d2 + graph_offset

        org_graph.change_layout(layout)

        return org_graph


def constant_0(t):
    return 0

def err_movement_rate(t, inflection = 10.0):
    if t < 0.5:
        return rate_functions.smooth(t*2, inflection)
    if t>0.7:
        return rate_functions.smooth((1-t)/0.3)
    else:
        return 1
    #shift = 0.7
    #new_t =  t/shift if t < shift else (1 - t)/(1-shift)
    #return rate_functions.smooth(new_t, inflection)

#interpolating polynomial {0,0} {0.2,1} {0.5,1}, {0.6,0.6}, {0.7,1}, {1,0}
def err_delay_rate(t, delay_percentage = 0.2):
    l = -18.9464*t + 239.69*t**2 - 777.292*t**3 + 970.238*t**4 - 413.69*t**5
    return delay_percentage * np.clip(l, 0, 1)

def err_highlight_rate(t):
    if t < 0.2:
        return np.clip(0.5* (sin(2*pi*10*t- pi/2)+1), 0,1)
    elif t > 0.45 and t < 0.75:
        return err_movement_rate((t-0.45)/ 0.3)
    else:
        return 0

def err_wiggle_rate(t, wiggles = 16, angle = 2*pi/64):
    if t< 0.5 or t > 0.7:
        return 0
    else:
        t = t-0.5
        return angle*sin(10*pi*t*wiggles)



class ErrHomAnimation(Animation):
    """
    Class animating a (un)successful homomorphism. It moves organized_graph to hom.g_img according to hom.

    Parameters
    ----------

    organized graph:
        The graph that will be moved. A copy is created so this object does not change
    
    hom:
        The homomorphism. This has to be a mapping of the vertices of organized_graph to hom.g_img
        hom.edge_attribs is used to check which edges are not present in g_img
    
    highlight_color:
        Edges that do not fit will be highlighted with this color
    
    suspend_mobject_updating:
        attribute of the base class Animation. Should be set to False, otherwise the edges won't update

    rate_func:
        function of the vertex movement. Default to sliding to g_img and jumping back to the original positions

    delay_rate_func:
        function that describes how far behind the non-mapping edges are.

    highlight_rate_func:
        function that describes the blinking of non-mapping edges
    """

    def __init__(self, organized_graph:DiGraph, hom:Homomorphism, highlight_color=err_color, suspend_mobject_updating = False,  rate_func = err_movement_rate, delay_rate_func = constant_0, highlight_rate_func = err_highlight_rate, wiggle_rate = err_wiggle_rate, edge_label_rate_func = rate_functions.ease_in_expo,  use_override=True,*args, **kwargs):
        super().__init__(mobject=organized_graph, suspend_mobject_updating=suspend_mobject_updating, *args, use_override=use_override, **kwargs)
        self.hom = hom
        self.highlight_color = highlight_color
        self.edge_attribs = self.hom.edge_attribs
        self.delay_rate_func = delay_rate_func
        self.highlight_rate_func = highlight_rate_func
        self.rate_func = rate_func
        self.edge_label_rate_func = edge_label_rate_func
        self.wiggle_rate = err_wiggle_rate

        self.missing_edges = []
        self.missing_edges2 = []
        for edge_attrib in self.edge_attribs:
            for edge in getattr(self.hom.g_dom, edge_attrib):
                if not self.hom.check_edge_maps(edge, edge_attrib):
                    self.missing_edges.append((edge_attrib, edge))
                    self.missing_edges2.append(edge)

    def begin(self):
        super().begin()
        self.hom.g_dom = self.hom.g_dom.copy()
        self.mobject.remove_updater(self.mobject.update_edges)
        #if type(self.mobject) == CoolDiGraph:
        #    self.mobject.remove_all_labels()

    def interpolate(self, alpha):
        layout = dict()

        #Set vertex position and label opacity
        for (vert,dot) in self.mobject.vertices.items():
            layout[vert] = interpolate(self.hom.g_dom.vertices[vert].get_center(), self.hom.g_img.vertices[self.hom.apply(vert)].get_center(), self.rate_func(alpha))
            dot.set_stroke(opacity = 1 - self.edge_label_rate_func(self.rate_func(alpha)), family =True)
            for sm in dot.submobjects:
                if isinstance(sm , MathTex):
                    sm.set_opacity_by_tex(sm.get_tex_string(), 1 - self.rate_func(alpha))
                    sm.update()
        #set concept label opacity:
        for (index, tex) in self.mobject.concept_labels.items():
            tex[0].set_opacity_by_tex(tex[0].get_tex_string(),1-self.rate_func(alpha)) #Do not change this rate_func since concepts of unnamed objects behave differently than concepts of named objects!

        self.mobject.change_layout(layout)
        self.mobject.update_edges(self.mobject)

        self.mobject.update()

        # set edge label opacity
        for (e, label) in self.mobject.edge_labels.items():
            if isinstance(label, MathTex):
                if e in self.missing_edges2:
                    label.set_opacity_by_tex(label.get_tex_string(), self.edge_label_rate_func(1 - self.rate_func(alpha)))
                else:
                    label.set_opacity_by_tex(label.get_tex_string(), 1 - self.edge_label_rate_func(self.rate_func(alpha)))
                label.update()

        # set edge opacity; interpolate arc_path
        for edge_attrib in self.edge_attribs:
            for (index, line) in getattr(self.mobject, edge_attrib).items():
                if index not in self.missing_edges2:
                    start_path_arc = getattr(self.hom.g_dom, edge_attrib)[index].path_arc
                    end_path_arc = getattr(self.hom.g_img, edge_attrib)[tuple(self.hom.apply(*index))].path_arc
                    line.set_stroke(opacity = 1 - self.edge_label_rate_func(self.rate_func(alpha)))
                    line.get_tip().set_opacity(1-self.edge_label_rate_func(self.rate_func(alpha)))
                    if (not start_path_arc is None) or (not end_path_arc is None):
                        if end_path_arc is None:
                            end_path_arc = 0
                        if start_path_arc is None:
                            start_path_arc = 0
                        if abs(end_path_arc - start_path_arc) > 0.0001:
                            line.set_path_arc(start_path_arc + self.rate_func(alpha)*(end_path_arc-start_path_arc))

                    line.update()

        # delay, wiggle, color misssing edges
        for (edge_attrib, edge) in self.missing_edges: 
            orig_color = getattr(self.hom.g_dom, edge_attrib)[edge].get_color()
            interpolated_color = interpolate_color(orig_color, self.highlight_color, self.highlight_rate_func(alpha))
            mobject_line = getattr(self.mobject, edge_attrib)[edge]
            mobject_line.set_color(interpolated_color)

            mobject_line.rotate(self.wiggle_rate(alpha))



            #*self.rate_func to be relative to the movement of the vertices
            diff = (self.hom.g_dom.get_center() - self.hom.g_img.get_center())*self.rate_func(alpha)*self.delay_rate_func(alpha)

            for i in range(len(mobject_line.points)):
                mobject_line.points[i] = mobject_line.points[i] + diff
            for i in range(len(mobject_line.submobjects[0].points)):
                mobject_line.submobjects[0].points[i] = mobject_line.submobjects[0].points[i] + diff

         
class HomomorphismAnimation(ErrHomAnimation):
    def __init__(self, organized_graph:DiGraph, hom:Homomorphism, suspend_mobject_updating = False,  rate_func = rate_functions.smooth, delay_rate_func = constant_0, highlight_rate_func = constant_0, use_override=True, *args, **kwargs):
        super().__init__(organized_graph= organized_graph, hom = hom, suspend_mobject_updating=suspend_mobject_updating, rate_func=rate_func, delay_rate_func=delay_rate_func, highlight_rate_func = highlight_rate_func, use_override=use_override, *args, **kwargs)

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.remove(self.hom.g_dom)


class HomomorphismExample(Scene):

    def construct(self):

        #DiGraph
#       vertices1 = [1, 2, 3, 4]
#       edges1 = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
#       g1 = DiGraph(vertices1, edges1,  vertex_config={'radius':0.08})
#       vertices2 = [1,'2a','2b', '2c',3]
#       edges2 = [(1,'2a'), (1,'2b'), ( 1,'2c'), ( '2a',3)]
#       g2 = DiGraph(vertices2, edges2,  vertex_config={'radius':0.08})
        #CoolDigraph
        vertices1 = [1, 2, 3, 4]
        edges1 = [('r', 1, 2),  ('r', 3, 4), ('r', 1, 3), ('r', 1, 4)]
        g1 = CoolDiGraph(vertices1, edges1)
        g1.add_edges(('r', (2,3)), edge_config={'path_arc': 0.0})
        vertices2 = [1,'2a','2b', '2c',3]
        edges2 = [('r', 1,'2a'), ('r', 1,'2b'), ('r', 1,'2c')]
        g2 = CoolDiGraph(vertices2, edges2)
        g2.add_edges(('r', ('2a', 3)), edge_config={'path_arc': 1.0}, edge_type=FlexibleDashedLine)


        #vertex_config = {'2a': {'color': RED}, '2b': {'color': GREEN}, '2c': {'color': BLUE}}
        #edge_config={(1,'2a'): {'path_arc': 0.5, 'color':GREEN, 'buff': 0.05}}

        g1.shift(LEFT)
        g2.next_to(g1, RIGHT)

        # Mapping that is a homomorphism
        h = Homomorphism(g2, g1, [(1,1), ('2a',2), ('2b', 2), ('2c',2), (3,3)], check_hom=True)
        # Mapping that is not a homomorphism
        #h = Homomorphism(g2, g1, [(1,4), ('2a',2), ('2b', 2), ('2c',2), (3,3)], check_hom=False)

        self.play(Create(g1))
        self.play(Create(g2))
        self.wait(1)
        g3 = h.create_organized_graph()
        self.play(ChangeGraphLayout(g2, g3), run_time=2.0)
        self.wait(1)
        #self.play(HomomorphismAnimation(g2, h), run_time=10.0)
        self.play(ErrHomAnimation(g2, h), run_time=5.0)
        self.wait(3)
