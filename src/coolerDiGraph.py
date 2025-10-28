from manim import *
from typing import (Sequence, Hashable, override)
import itertools as it

from manim.typing import (
        Point3D,
        Point3DLike,
        Vector3D,
    )
import render_emoji
UPDATER_ITERATION = 8

class CoolerLine(Line):
    """
    line class to unify the behavior of lines across data-graphs and rules
    You do not need this if you do not need the rule class
    """
    def reset_endpoints_based_on_tip(self, tip, at_start: bool):
        return self



class CoolDiGraph(DiGraph):
    def __init__(
        self,
        vertices: Sequence[Hashable],
        edges: Sequence[tuple[str,Hashable,Hashable]],
        concepts: Sequence[tuple[Hashable, str, Vector3D]] = [],
        edge_config: dict | None = None,
        vertex_config: dict | None = None,
        edge_label_config: dict | None = None,
        conceptlabelOffset:float = 0.25,
        conceptLabelScale:int = 24,
        conceptLabelFontSize: float = 1.0,
        layout="circular",
        labels=True,
        layout_scale=1.5,
        vertex_color: str | dict[Hashable, str] = "#FFFFFF",
        edge_type = CoolerLine,
        dot_offset = 0.2,
        labeled_dot_offset = 0.02,
        **kwargs
    ):
        """
            Manim-class to represent Graphs with relation and concept labels

            Parameters:
            -----------

            vertices
                    sequence (preferably string sequence) of the graphs vertices, each representing a vertice name (these will be used as vertex-labels)
            edges
                    sequence of tuples consisting of a string and two vertex names, each representing an (labeled) edge of the graph
            concepts 
                    sequence of tuples consisting of a vertex name, a string that represents the concept label itself and a directional vector that positions the label relative to the vertex 
            edge_config
                    config dict specifying configurations for the edge lines 
                    (see DiGraph class)
            vertex_config
                    config dict specifying configurations for the vertices
                    (see DiGraph class)
            edge_label_config
                    config dict specifying configurations for the edge labels
            conceptlabelOffset
                    distance between concept label and vertex
            conceptLabelScale
                    size of concept labels
            conceptLabelFontSize
                    font size of concept labels
            layout
                    layout of the graph
            labels
                    specifies wether the vertices are labeled
            vertex_color
                    color of the vertices
            edge_type
                    line-type of the edges
            dot_offset
                    size of bounding box around unlabeled vertices 
            labeled_dot_offset
                    size of bounding box around labeled vertices (offset to label)
        
        """
        
       
        
        # set internal parameters
        self.dot_offset = dot_offset
        self.labeled_dot_offset = labeled_dot_offset
        self.role_data = edges
        self.concept_data = concepts
        self.conceptlabelOffset = conceptlabelOffset
        self.conceptLabelScale = conceptLabelScale
        self.conceptLabelFontSize = conceptLabelFontSize
        self.edge_labels = {}
        self.concept_labels = {}
        self.edge_type = edge_type

        # collect all edges of all roles
        allEdges = []
        for (role, u, v) in edges:
            allEdges += [(u, v)]

        if edge_label_config is None:
            self.edge_label_config = {}
        else:
            self.edge_label_config = edge_label_config
        if edge_config is None:
            edge_config = {}

        if vertex_config is None:
            vertex_config = {}
        
        self.default_edge_label_config = {
                e: v for e, v in self.edge_label_config.items() if e not in allEdges
            }


        # populate the config - dicts

        if type(vertex_color) == str:
            vertex_color = {v : vertex_color for v in vertices}
        self.default_tip_config =  {
                            "tip_shape": StealthTip,
                            "tip_length": 0.15,
                            "tip_width": 0.1,
            }
        global_edge_config = {"stroke_width": 2, 
                                "tip_config": self.default_tip_config} 
        new_edge_config = {}
        for (u,v) in allEdges:
            new_edge_config.update( {(u,v): global_edge_config | edge_config.get((u,v), {})} )
        global_edge_config.update( new_edge_config)
        
        self.global_vertex_config = {"fill_opacity":0.0,"stroke_width": 0, "radius":None} | vertex_config

        new_vertex_config = {"fill_opacity": 0.0, 
                           "radius": 0.15,
                           "stroke_width": 1} 
        new_vertex_config.update({v: {"label": MathTex(v, color=vertex_color.get(v,"#FFFFFF") ), "color": vertex_color.get(v, "#FFFFFF")} | self.global_vertex_config 
                                  for v in vertices} if labels==True else {}) 

      
        


        super().__init__(
            vertices,
            allEdges,
            layout=layout,
            layout_scale=layout_scale,
            labels=False, #internals dont work the appropriate way, thus we need to circumvene them
            vertex_type=LabeledDot if labels == True else Dot,
            edge_type=edge_type,
            edge_config=global_edge_config,
            vertex_config=new_vertex_config,
            **kwargs
        )
        for ((u,v), edge) in self.edges.items():
            edge.set_stroke(edge.stroke_color,width=new_edge_config[(u,v)].get("stroke_width", 2)  )

        

    
        # The following act as "bounding boxes" around all vertices (this is not a nice way of doing this, but gets the job done)
        # [We do this to prevent the arrow-tips from penetrating the vertices]

        for v in vertices:

            if isinstance(self[v], LabeledDot):
                self[v].add(Dot(point=self[v].get_center(), fill_opacity=0.0, radius=self[v].width/2 + self.labeled_dot_offset))
            else:
                self[v].add(Dot(point=self[v].get_center(),fill_opacity=0.0, radius=self[v].width/2 + self.dot_offset))


            for mob in self[v].submobjects:
                if isinstance(mob, MathTex): 
                    mob.set_opacity_by_tex(mob.get_tex_string(),1.0)
        
        # Recalculate the edge Endpoints
        for i in range(UPDATER_ITERATION):
            self.update_edges(self)
        
        
        
        
        # Add concept Labels if provided
        self.createConceptLabels(concepts, conceptLabelScale, conceptLabelFontSize)
        #self.add(*[x[0] for x in self.concept_labels.values()])
        
        # Add edge labels if provided
        
        self.createEdgeLabels(edges)
        #self.add(*self.edge_labels.values())
        self.update()
        
        
    


    def createSingleConceptLabel(self, concept:str, vertex:Hashable, dir:Vector3D, labelScale:float|None, labelFontSize:int|None, color:int | None):
        """
        Function to add a single concept label to the graph

        Parameters:
        -----------
        concept
                the text of the concept as tex-string
        vertex
                the vertex that should hold the concept label
        dir
                the direction (starting from the vertex that holds this concept) where the concept is placed
        labelScale
                the size of the concept label
        labelFontSize
                the font size of the label
        color
                the color of the label
        
        """
        
        if  labelScale is None:
            labelScale = self.conceptLabelScale
        if labelFontSize is None:
            labelFontSize = self.conceptLabelFontSize
        if color is None:
            color = "#FFFFFF"
        self.concept_data = self.concept_data + [(vertex, concept, dir)] if (vertex, concept, dir) not in self.concept_data else self.concept_data
        text = MathTex(concept, font_size=labelFontSize, color=color)
        text.scale(labelScale)
        self.concept_labels.update({(vertex, concept):(text,dir)})
        self.add(text)

    def createConceptLabels(self, concepts, labelScale:float, labelFontSize: int):
        """
        Function to add a single concept label to the graph

        Parameters:
        -----------
        concepts
                the concepts as tuples (vertex, concept_string, anchor_direction)
        labelScale
                the scale of the created concepts
        labelFontSize
                the font size of the labels
        """
        for v, c, dir in concepts:
            self.createSingleConceptLabel(c, v, dir, labelScale, labelFontSize, None)

    def createSingleEdgeLabel(self, edge:tuple[Hashable,Hashable], role_name:str, labelFontSize:int = 24, labelScale:int= 1.0, 
                              labelOffset: float = 0.15):
        """
        Function to create a single edge-label 

        Parameters:
        -----------
        edge
                the edge where the label should be attached
        role_name
                the label itself as (tex) string
        labelFontSize
                the font size of the label
        labelScale
                the scale of the label
        labelOffset 
                the offset from the edge
        """
        (u,v) = edge
        text = MathTex(str(role_name), font_size=labelFontSize)
        text.scale(labelScale)
        self.edge_label_config.update({edge: {"labelFontSize": labelFontSize, 
                                              "labelScale": labelScale, 
                                              "labelOffset": labelOffset }})
        self.edge_labels.update({(u,v):text})
        line = Line([0,0,0],[0.01,0,0],stroke_width = 0)
        line.tex_string = ''
        text.add(line) #we add a line to store the rotation of the Text (somehow not all Mobjects store a rotation)
        self.add(text)
        self.role_data = self.role_data + [(role_name,u,v)] if (role_name,u,v) not in self.role_data else self.role_data
        return VGroup(*text)
    
    def createEdgeLabels(self, edges):
        """
        Function to create edge labels

        Parameters:
        -----------
        edges
                edge labels as tuples (edge_label, u_edge, v_edge)
        
        """
        # create Edge Labels (positioned orthogonal to line, rotated appropriately)
        for (role_name, u,v) in edges:
            config =  self.default_edge_label_config|  self.edge_label_config.get((u,v), {}) 
            self.createSingleEdgeLabel((u,v),role_name,**config)

    def update_edge_labels(self):
        """
        updates the edge labels to make them follow their assigned edge
    
        """
        for (u,v), text in self.edge_labels.items():
                edge = self.edges[(u,v)]
                if not (edge.get_tips()[0].has_no_points() or (edge.has_no_points() and (type(edge)==Line or type(edge)==CoolerLine))):
                    start = edge.get_start()
                    end = edge.get_end()
                    mid_point = (start + end) / 2 
                
                    # calculate line normal and angle to rotate
                    direction = end - start
                    ndirection = direction / np.linalg.norm(direction)
                    

                    normal = np.array([-ndirection[1], ndirection[0],0])
                    angle = np.arctan2(direction[1], direction[0])
                    
                    if len(text.submobjects) > 1:
                        angle -= text.submobjects[1].get_angle()
                    else:
                        angle = 0
                    if np.dot( normal, UP) < -0.01:
                        normal = - normal
                        angle  = angle + PI

                    # calculate the right mid_point if we deal with a path_arc
                    if edge.get_path_arc() is not None:
                        tip = edge.pop_tips()[0]
                        curve_functions = list(edge.get_curve_functions())
                        if len(curve_functions)%2 == 0:
                            mid_point = curve_functions[int(len(curve_functions)/2)](0)
                        else:
                            mid_point = curve_functions[int((len(curve_functions)-1)/2)](0.5)
                        edge.add_tip(tip)
                    #apply everything
                    text.rotate(angle,about_point=text.get_center())
                    text.move_to(mid_point + normal * self.edge_label_config[(u,v)].get("labelOffset", 
                                                                                        self.edge_label_config.get("labelOffset", 1.5)))
    def update_vertex_labels(self):
        """
        Update vertex labels to follow their parent vertex
        """
        for (v, concept), (text,dir) in self.concept_labels.items():
            ndir = dir/ np.linalg.norm(dir)
            radius = self[v].width/2
            text.move_to(self[v].get_center() + (radius+ self.conceptlabelOffset) * ndir)
            for mob in self[v].submobjects:
                if isinstance(mob, MathTex): 
                    text.set_opacity_by_tex(text.get_tex_string(),mob.get_part_by_tex(mob.get_tex_string()).get_stroke_opacity())
                    text.update()
    def update_arrows(self, graph):
        """
        Updates the edges to stick at their corresponding vertices.

        Arrow tips need to be repositioned since otherwise they can be
        deformed.
        """
        for (u, v), edge in graph.edges.items():
            if not (edge.get_tips()[0].has_no_points() or (edge.has_no_points() and (type(edge)==Line or type(edge)==CoolerLine))): # this check is done to ensure that the transform method works well
                tip = edge.pop_tips()[0]
                # Passing the Mobject instead of the vertex makes the tip
                # stop on the bounding box of the vertex.
                
                upos = graph[u].get_center()
                vpos = graph[v].get_center()

                urad = graph[u].get_width() / 2
                vrad = graph[v].get_width() / 2 

                # if the line has a arc, we need to calculate the tangent of this arc at the start and entpoint
                if edge.get_path_arc() is None:
                    direction_start = vpos - upos
                    direction_end = - direction_start
                else: 
                    direction_start = edge.get_first_handle().copy() - edge.get_start().copy()
                    direction_end = edge.get_last_handle().copy() - edge.get_end().copy()

                # calculate the start and end points using the tangents of the start and end points
                ndirection_start = direction_start / (np.linalg.norm(direction_start) if np.linalg.norm(direction_start) > 0 else 1)
                ndirection_end = direction_end /(np.linalg.norm(direction_end) if np.linalg.norm(direction_end) > 0 else 1)
                uintersection = upos + urad * ndirection_start
                vintersection = vpos + vrad * ndirection_end
                if not all(uintersection == vintersection):

                    edge.set_points_by_ends(
                        uintersection,
                        vintersection,
                        path_arc = edge.path_arc
                    )
                
                
                edge.add_tip(tip)

                

    def change_vertex_name(self, old:str, new:str):
        """
        Change the vertex name of some vertex

        Parameters:
        -----------
        old
                vertex to be changed
        new 
                new vertex name
        
        """
        pos = self[old].get_center()
        
        self.add_vertices(new, 
                          positions={new:pos}, 
                          labels=(type(self[old]) is LabeledDot),
                          vertex_config=self._vertex_config.get(old, {}))

        for (role, u, v) in self.role_data.copy():
            if v == old:
                self.remove_edges((u, v))
                self.add_edges((role, (u, new)), edge_type=self.edge_type, label_config=self.edge_label_config)
            elif u == old:
                self.remove_edges((u, v))
                self.add_edges((role, (new, v)), edge_type=self.edge_type, label_config=self.edge_label_config)

        self.update_arrows(self)
        self.update_vertex_labels()
        self.update_edge_labels()

        for (v, concept, dir) in self.concept_data:
            if v == old:
                self.remove_concept_labels((v, concept))
                self.add_concept_labels((new, concept, dir))
        
        self.remove_vertices(old)

        self.update()

    @override
    def update_edges(self, graph):
        """
        Updater function acting as the parent of the underlying updaters
        """
        self.update_arrows(graph)
        self.update_vertex_labels()
        self.update_edge_labels()

   
    @override
    def _add_edge(self,
        edge: tuple[Hashable, Hashable],
        edge_type: type[Mobject] = CoolerLine,
        edge_config: dict | None = None,
        role_name: str = "",
        edge_label_config: dict | None = None
        ) -> Mobject:
        """
        adds an edge to the graph

        Parameters:
        -----------
        edge
                the edge as tuple
        edge_type
                the line-type of the edge
        role_name
                the corresponding edge label
        edge_label_config
                configuration file for the labels
        """
        
        edge_mobject = super()._add_edge(edge, edge_type=edge_type,edge_config=edge_config)
        if edge_config is None:
            edge_config = self.default_tip_config.copy()
        if edge_label_config is None:
            edge_label_config = self.default_edge_label_config.copy()


        self.edges[edge].add_tip(**(self.default_tip_config.copy()
                                                    | (edge_config.get("tip_config",{})) 
                                    ) )
        label_mobject = self.createSingleEdgeLabel(edge,role_name, **edge_label_config)
        self.update()
        for i in range(UPDATER_ITERATION):
            self.update_edges(self)
        self.update()
        return VGroup(*edge_mobject,*label_mobject)

    @override
    def _add_vertex(
        self,
        vertex: Hashable,
        position: Point3DLike | None = None,
        label: bool = True,
        vertex_color = "#FFFFFF",
        vertex_config: dict | None = None,
        vertex_mobject: dict | None = None,
    ) -> Mobject:
        """
        adds a vertex to the graph

        Parameters:
        -----------
        vertex
                the vertex name
        position 
                the position where the new vertex is placed
        label
                should this be a labeled vertex
        vertex_color
                the color of the vertex
        vertex_config
                config dict of the vertex parameters
        vertex_mobject
                if provided, adds this object as vertex
        
        """
        
        if vertex_config == None:
            vertex_config = {}

        super()._add_vertex(vertex, 
                            position = position, 
                            label= False, 
                            label_fill_color= BLACK, 
                            vertex_type=LabeledDot if label == True else Dot,
                            vertex_config = (vertex_config if label==False else  
                            {"label": MathTex(vertex, color= vertex_color )} | self.global_vertex_config ) | {"color": vertex_color}, 
                            vertex_mobject = vertex_mobject)
        for mob in self[vertex].submobjects:
                if isinstance(mob, MathTex): 
                    mob.set_opacity_by_tex(mob.get_tex_string(),1.0)
        if isinstance(self[vertex], LabeledDot):
            self[vertex].add(Dot(point=self[vertex].get_center(),fill_opacity=0.0, radius=self[vertex].width/2 + self.labeled_dot_offset))
        else:
            self[vertex].add(Dot(point=self[vertex].get_center(),fill_opacity=0.0, radius=self[vertex].width/2 + self.dot_offset))
        def updater(mob):
            self.update_arrows(self)
        self[vertex].add_updater(updater)
        return VGroup(*self.vertices[vertex])
    
    def _add_concept_label(self, 
                          concept:str, 
                          vertex:Hashable, 
                          direction:Vector3D = UR, 
                          color: str | None=None,
                          labelScale : float | None= None,
                          labelFontSize: int | None = None) -> Mobject:
        """
        add a concept label to the graph

        Parameters:
        -----------
        concept
                the concept as string
        vertex
                the vertex to which the concept is assigned to
        direction
                the direction to which the concept is placed (from the center of the vertex)
        color
                the color of the concept
        labelScale
                the scale of the concept
        labelFontSize
                the font size of the concept

        
        """
        
        self.createSingleConceptLabel(concept, vertex, direction,labelScale, labelFontSize, color)
        self.update_vertex_labels()
        return VGroup(*self.concept_labels[(vertex,concept)][0])
    
    def add_concept_labels(self, 
                           *concept_labels: tuple[Hashable, str, Vector3D]):
        """
        adds concept labels to the graph

        Parameters:
        -----------
        concept_labels
                the labels as tuples (parent_vertex, concept, direction)
        """
        return [self._add_concept_label(concept, v, direction=dir) for (v,concept, dir) in concept_labels]
    def get_tips(self)-> Sequence[ArrowTip]:
        """
        returns all tips that are hold by the edges of this graph
        """
        tips = []
        for edge in self.edges.values():
            tips.append(edge.get_tips()[0])
        return tips
    @override 
    def add_vertices(self,
        *vertices: Hashable,
        positions: dict | None = None,
        labels: bool = True,
        vertex_colors: dict = {},
        vertex_config: dict | None = None,
        vertex_mobjects: dict | None = None
        ):
        """
        adds vertices to the graph, can be animated

        Parameters:
        -----------
        *vertices
                vertex names of the vertices to add
        positions 
                dict that specifies the positions of the vertices (vert -> pos)
        labels 
                specifies if the added vertices should be labeled
        vertex_colors 
                dict that specifies colors for the added vertices
        vertex_config
                config dict specifying properties for the vertices
        vertex_mobject
                dict giving already created mobjects as vertices
        
        
        """
        return [ self._add_vertex(v,position=positions.get(v, None) if positions != None else None,
                                 label = labels,
                                 vertex_config= vertex_config, 
                                 vertex_mobject= vertex_mobjects, 
                                 vertex_color = vertex_colors.get(v,"#FFFFFF"),) for v in vertices ]
    @override
    def add_edges(self, 
                  *edges: tuple[str,tuple[Hashable,Hashable]],
                  edge_type:type[Mobject] = CoolerLine,
                  edge_config: dict | None = None,
                  label_config: dict | None = None, 
                  **kwargs):
        """
        adds edges to the graph. Vertices that are not present yet will be added aswell.
        Can be animated.

        Parameters:
        -----------
        edges
                edge list of tuples consisting of (str, vert_name, vert_name)
        edge_type
                line type of the added edges
        edge_config
                configuration dict for the edges
        label_config
                configuration dict for the edge labels
        
        """
        
        # this function is in its base the exact same as in the parent class, however taking the additional role_name into account
        if edge_config is None:
            edge_config = {}
        if label_config is None:
            label_config = {}
        
        # remove edges that are already present
        new_edges = []
        for (role, e) in edges:
            if e not in self.edges:
                new_edges.append((role, e))
        edges = new_edges
        if len(edges) == 0:
            raise RuntimeError("All edges are already present. There is nothing to add. Try removing them first and then adding them back in.")


        pure_edges = [e for (role, e) in edges]
        non_edge_settings = {k: v for (k, v) in edge_config.items() if k not in pure_edges}
        base_edge_config = self.default_edge_config.copy()
        base_edge_config.update(non_edge_settings)
        base_edge_config = {e: base_edge_config.copy() for e in pure_edges}

        for e in pure_edges:
            base_edge_config[e].update(edge_config.get(e, {}))
        edge_config = base_edge_config

        edge_vertices = set(it.chain(*pure_edges))
        new_vertices = [v for v in edge_vertices if v not in self.vertices]
        added_vertices = self.add_vertices(*new_vertices, **kwargs)

        added_mobjects = sum(
            (
                self._add_edge(
                    edge,
                    role_name = role_name,
                    edge_type=edge_type,
                    edge_config=edge_config[edge],
                    edge_label_config=label_config
                ).submobjects
                for (role_name, edge) in edges
            ),
            added_vertices,
        )
        return VGroup(*added_mobjects)


    """
    
    The animation functions for the "add_something function"
    [ Note: adding multiple vertices / edges comes with the cost of less configurability for their appearance ] 

    """
    @override_animate(add_concept_labels)
    def _add_concept_labels_animation(self, *args, anim_args=None, **kwargs):
        """
        function to animate adding concept labels to the graph,
        see add_concept_labels
        """
        if anim_args is None:
            anim_args = {}

        animation = anim_args.pop("animation", Create)

        vertex_mobjects = self.add_concept_labels(*args, **kwargs)

        return AnimationGroup(
            *(animation(v[-1], **anim_args) for v in vertex_mobjects),
            group=self
        )
    
    @override_animate(add_vertices)
    def _add_vertices_animation(self, *args, anim_args=None, **kwargs):
        """
        function to animate adding vertices to the graph,
        see add_vertices
        """
        if anim_args is None:
            anim_args = {}

        animation = anim_args.pop("animation", Create)

        vertex_mobjects = self.add_vertices(*args, **kwargs)

        return AnimationGroup(
            *(animation(v[-1], **anim_args) for v in vertex_mobjects),
            group=self
        )
    
    @override_animate(add_edges)
    def _add_edges_animation(self, *args, anim_args=None, **kwargs):
        """
        function to animate adding edges to the graph,
        see add_edges
        """
        if anim_args is None:
            anim_args = {}
        animation = anim_args.pop("animation", Create)

        mobjects = self.add_edges(*args, **kwargs)
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects), group=self
        )
    
    @override_animate(_add_edge)
    def _add_edge_animation(self, *args, anim_args=None, **kwargs):
        """
        function to animate adding an edge to the graph,
        see _add_edge
        """
        if anim_args is None:
            anim_args = {}
        animation = anim_args.pop("animation", Create)
        mobjects = self._add_edge(*args, **kwargs).submobjects
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects), group=self
        )
    
    @override_animate(_add_concept_label)
    def _add_concept_label_animation(self, *args, anim_args=None, **kwargs):
        """
        function to animate adding a concept label to the graph,
        see _add_concept_label
        """
        if anim_args is None:
            anim_args = {}
        animation = anim_args.pop("animation", Create)
        mobjects = self._add_concept_label(*args, **kwargs).submobjects
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects), group=self
        )
    
    """
    
    removal functions for the additional stuff
    
    """

    @override 
    def _remove_edge(self, edge: tuple[Hashable]) -> Mobject:  
        """
        function to remove an edge from the graph

        Parameters:
        -----------
        edge
                the edge as a tuple (u,v) of vertices
        
        """       
        mobject_edge = super()._remove_edge(edge)

        mobject_label = self.edge_labels.pop(edge)

        self.remove(mobject_label)
        for (role, *edge) in self.role_data:
            self.role_data.remove((role, *edge)) 
        return VGroup(mobject_edge, mobject_label)
    
    @override
    def _remove_vertex(self, vertex):
        """
        function to remove a vertice from the graph

        Parameters:
        -----------
        vertex
                vertex name
        
        """  
        mobs = []
        for (u,v) in self.edge_labels.keys():
            if vertex in (u,v):
                mobs.append(self.remove_edges((u,v)))
        return VGroup(super()._remove_vertex(vertex), *mobs)
    def _remove_concept_label(self,vertex:Hashable, label:str ) -> Mobject:
        """
        function to remove a concept label from the graph

        Parameters:
        -----------
        vertex
                the vertex that holds the concept label that is to be removed
        label
                the concept label to remove
        
        """  
        (label_mobject, direction) = self.concept_labels.pop((vertex, label))
        self.remove(label_mobject)
        for (vertice, label, direction) in self.concept_data:
            self.concept_data.remove((vertice, label, direction))
        return VGroup(label_mobject)
    
    def remove_concept_labels(self, *labels: tuple[Hashable,str]) -> Mobject:
        """
        function to remove a concept labels from the graph

        Parameters:
        -----------
        labels
                the concept labels to remove as tuple (vertex, concept_label)
        
        """  
        mobjects = []
        for (vertex, label) in labels:
            mobjects.extend(self._remove_concept_label(vertex, label).submobjects)
        return VGroup(* mobjects)
    
    def _remove_label(self, vertex:str) -> Mobject:
        """
        removes the label of a vertex

        Parameters:
        -----------
        vertex
                the vertex-label to be removed
        
        """   
        mobject = VGroup()
        if self[vertex].submobjects:
            mobject = self[vertex].submobjects[0]
            self[vertex].remove(self[vertex].submobjects[0])
        return mobject
    
    def remove_labels(self, *vertices:str) -> Mobject:
        """
        removes the labels of the given vertices

        Parameters:
        -----------
        vertices
                the vertices for which the labels will be removed
        
        """   
        mobjects = []
        for vertex in vertices:
            mobjects.append(self._remove_label(vertex))
        return VGroup(*mobjects)
    
    def remove_all_labels(self) -> Mobject:
        """
        removes the labels all vertices
        """   
        return self.remove_labels(*self.vertices.keys())
    
    """
    
    removal animations
    
    """

    @override_animate(remove_concept_labels)
    def _remove_concept_labels_animation(self, *labels:tuple[Hashable,str], anim_args=None):
        """
        function to animate removing concept labels from the graph,
        see remove_concept_labels
        """
        if anim_args is None:
            anim_args = {}

        animation = anim_args.pop("animation", Uncreate)

        mobjects = self.remove_concept_labels(*labels)
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects)
        )
    @override_animate(remove_labels)
    def _remove_labels_animation(self, *vertices, anim_args=None):
        """
        function to animate removing vertex labels from the graph,
        see remove_labels
        """
        if anim_args is None:
            anim_args = {}

        animation = anim_args.pop("animation", Uncreate)

        mobjects = self.remove_labels(*vertices)
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects)
        )
    @override_animate(remove_all_labels)
    def _remove_all_labels_animation(self, anim_args=None):
        """
        function to animate removing all vertex labels from the graph,
        see remove_all_labels
        """
        if anim_args is None:
            anim_args = {}

        animation = anim_args.pop("animation", Uncreate)

        mobjects = self.remove_all_labels()
        return AnimationGroup(
            *(animation(mobj, **anim_args) for mobj in mobjects)
        )
    


class Emoji(ImageMobject):
    def __init__(self, label: Hashable, emoji:tuple[str,str,str|None], parent: MathTex, update_config: dict | None= None,scale_factor = 2.1, **kwargs):
        """
        Class to Render and load Emojis into manim

        Parameters:
        -----------
        label
                substring of the Mathtex where the emoji will be attached
        emoji
                specifies the emoji by (UNICODE, filename, COLOR)
        parent
                parent MathTex Mobject
        update_config
                configuration which attributes should get updated wrt. parent
        scale_factor
                scale of emoji
        
        """
        path = render_emoji.render_emoji_to_png(emoji[0], emoji[1], emoji[2])
        super().__init__(path,image_mode='RGBA',**kwargs)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["lanczos"])
        self.scale_factor = scale_factor
        self.move_to(parent.submobjects[0].get_part_by_tex(label).get_center()).scale_to_fit_width( parent.submobjects[0].get_part_by_tex(label).width*scale_factor)

        parent.submobjects[0].get_part_by_tex(label).set_opacity( 1.0)
        parent.submobjects[0].get_part_by_tex(label).set_color("#000000")
        if update_config is None:
            update_config = {}

        self.update_scale = update_config.get("scale", True)
        self.update_opacity = update_config.get("opacity", True)
        self.update_position = update_config.get("position", True)
        self.emoji_updater( parent,label)

    def emoji_updater( self,vertex: MathTex, label:str):
        """
        updater function for the emoji wrt. the parent/vertex mobject.
        Which parameters (opacity, scale, position) are updated depends on the config (self.update_opacity, self.update_scale, self.update_position)

        Parameters:
        -----------
        vertex
                the parent mobject that dictates the behavior of the emoji
        label
                the label of the parent mobject that should get replaced by the emoji
        
        """
        def updater_emoji(emoji):
            if self.update_scale:
                self.scale_to_fit_width(vertex.submobjects[0].get_part_by_tex(label).width * self.scale_factor)
            if self.update_position:
                self.move_to(vertex.submobjects[0].get_part_by_tex(label).get_center())
        
            opacity = vertex.submobjects[0].get_part_by_tex(label).get_stroke_opacity()
        
            if opacity is None:
                opacity = 0.0
            if self.update_opacity:
                emoji.set_opacity(opacity)
        def updater_vertex(vert):
            self.update()

        self.add_updater(updater_emoji)
        vertex.add_updater(updater_vertex)
    

class MyGraphScene(Scene):
    def construct(self):
        """
        
        Small teach by example on how to use the class functions
        
        """

        vertices = ["a", "b", "c"]
        edges = [("role","a", "b"), ("role2","b", "c"), ("role", "c", "a")]
        concepts = [("a", "A", UR),  ("b", "A", UP), ("b", "D", UR)]

        graph = CoolDiGraph(
            vertices,
            edges,
            concepts=concepts,
            edge_label_config={"labelFontSize":12, "labelOffset":0.15, ("a","b"):{"labelFontSize":24, "labelOffset":0.15,}},
            labels =  True
        )

        
        
        
        emojis = Emoji("a",("😾", "sad_cat.png", "#B100B1"),graph["a"])


        self.play(Create(graph),FadeIn(emojis, scale= 2.0))


        self.wait()
        self.play(graph["a"].animate.move_to([1,-1,0]))
        self.play(graph.animate.add_vertices("g", labels=False))
        graph.change_vertex_name("g", "m")
        self.play(graph.animate.remove_concept_labels(("a", "A")))
        self.play(graph.animate().add_vertices("f", vertex_colors={"f": "#FF00FF"}))

        graph.suspend_updating()
        self.play(Wiggle(graph.edges[("a","b")]))
        graph.resume_updating()

        self.wait()

        # Notice the * before the array!
        self.play(graph.animate().add_edges(*[("arc1",("a","d")), ("arc2",("c","d"))], edge_config={"path_arc": 1.0}, edge_type=DashedLine))
        graph.update()
        self.wait()
        self.play(graph.animate._add_edge(("a","c"), role_name="newrole"))
        self.wait()
        self.play(graph.animate().remove_edges(("a","c")))
        self.play(graph["a"].animate.move_to([-2,-2,0]))

        self.play(graph.animate.add_concept_labels(("f","F",UR)))
        self.play(graph["f"].animate.move_to([2,-1,0]))
        self.play(FadeOut(emojis))
        self.play(Uncreate(graph))
        self.wait()

