from coolerDiGraph import *
from manim import *
from typing import *
import numpy as np
from copy import deepcopy
from manim.typing import (
        Point3D,
        Point3DLike,
        Vector3D,
    )
class RoleTable(Table):
    def __init__(self, table,role:str, emojis : dict[str, Mobject] | None = None, **kwargs):
        """
        Manim-Mobject that defines the Table for a given binary relation

        Parameters:
        -----------
        table
                the relation itself
        role
                the name of the relation

        emojis
                possible emojis used as symbols for elements in the relation

        
        """
        
        super().__init__(table, 
                         include_outer_lines=True,
                         element_to_mobject=MathTex,
                         col_labels= [MathTex("1"),MathTex("2")], 
                         include_background_rectangle=True,
                         **kwargs
                         )
        self.role_name = role
        anchor_bot = self.get_rows().get_bottom()[1] - 0.5 * self.v_buff
        anchor_top = self.get_rows()[1].get_top()[1] + 0.5 * self.v_buff
        anchor = self.vertical_lines.submobjects[2].get_center()[0]

        mid_line = Line( (anchor,anchor_top,0), (anchor,anchor_bot,0), **self.line_config)

        self.role_label = MathTex(r"\underline{" +role + r"}" )
        self.role_label.move_to((anchor,self.get_entries((1,1))[0].get_center()[1], 0 ) )

        self.get_entries((1,1))[0].become(VGroup())
        self.get_entries((1,2))[0].become(VGroup())

        self.vertical_lines.submobjects[2].become(mid_line)
        self.elements.add(self.role_label)

        if not emojis is None:
            ent = self.get_entries_without_labels()
            for k in range(len(ent)):
                ent[k].set_opacity(0.0).scale(3.0)
                


class ConceptTable(Table):
    def __init__(self, table, concept:str, emojis: dict[str, Mobject]|None = None, **kwargs):
        """
        Manim-Mobject that defines the Table for a given unary relation

        Parameters:
        -----------
        table
                the relation itself
        concept
                the name of the relation

        emojis
                possible emojis used as symbols for elements in the relation

        
        """
        
        super().__init__(table, 
                         include_outer_lines=True,
                         element_to_mobject=MathTex,
                         col_labels=[MathTex(r"\underline{" +concept + r"}" )],
                         **kwargs,
                         include_background_rectangle=True,
                         )
        self.label = concept
        if not emojis is None:
            ent = self.get_entries_without_labels()
            for k in range(len(ent)):
                ent[k].set_opacity(0.0).scale(3.0)

class Database(VGroup):
    def __init__(self,  roles: Sequence[tuple[str,Hashable,Hashable]],
        concepts: Sequence[tuple[Hashable, str, Vector3D]] = [],  
        z_indices: dict[str, int] = {},
        emojis : dict[str, Mobject] | None = None,
        buff = -0.2,
        **kwargs):
        """
        Manim-Mobject that represents a database consiting of binary (roles) and unary (concepts) relations

        Parameters:
        -----------
        roles
                the binary relations as a sequence of tuples (relation_name, element_1, element_2)
        concepts
               the unary relations as a sequence of tuples (relation_name, element) 
        z_indices
                dict to say which table is in front of another (usefull for negative buff)
        emojis
                possible emojis that replace elements
        buff 
                margin between the created tables
        
        """

        self.role_data = roles
        self.concept_data = concepts


        concept_tables = self.sort_concepts_to_tables(concepts)
        self.concept_table_mobjects = []
        
        role_tables = self.sort_roles_to_tables(roles)
        self.role_table_mobjects = []

        if z_indices == {}:
            none_set_z = 5
        else:
            none_set_z = max( z_indices.values()) + 5

        for (role, individuals) in role_tables.items():
            self.role_table_mobjects.append(RoleTable(individuals, 
                                                      role, 
                                                      z_index = z_indices.get(role, 
                                                                                (none_set_z:= none_set_z + 1)),
                                                      emojis=emojis,
                                                      **kwargs))
            
        for (concept, individuals) in concept_tables.items():
            self.concept_table_mobjects.append(ConceptTable(individuals, 
                                                            concept, 
                                                            z_index = z_indices.get(concept, 
                                                                                    (none_set_z:= none_set_z + 1)),
                                                            emojis = emojis,
                                                            **kwargs))
        
        
        super().__init__(* self.role_table_mobjects, *self.concept_table_mobjects)
        self.scale(0.5)
        self.arrange_in_grid(buff=buff, cols= 3)

    @classmethod
    def fromCoolDiGraph(self, graph: CoolDiGraph, **kwargs):
        """
        Construct a table from a CoolDiGraph

        Parameters:
        -----------
        graph
                the graph from which the DB is constructed
        
        """
        roles = graph.get_role_data()
        concepts = graph.get_concept_data()
        return Database(roles, concepts, **kwargs)
    
    
    def sort_roles_to_tables(self,roles: Sequence[tuple[str,Hashable,Hashable]]) -> dict[str, Sequence[tuple[str, str]]]:
        """
        function to sort a sequence of binary relations into a dict (relation_name -> sequence)
        
        Parameters:
        -----------
        roles
                the binary relations that should be sorted
        """
        tables = {}
        for (role, u ,v) in roles:
            tables.update({role: tables.get(role, []) + [(u,v)]})

        return tables
    
    def sort_concepts_to_tables(self,concepts: Sequence[tuple[Hashable, str, Vector3D]] = []) -> dict[str, Sequence[str]]:
        """
        function to sort a sequence of unary relations into a dict (relation_name -> sequence)
        
        Parameters:
        -----------
        concepts
                the unary relations that should be sorted
        """
        tables = {}
        for (v, concept, direction) in concepts:
            tables.update({concept: tables.get(concept, []) + [[v]]})

        return tables

class EmojiDatabase(Group):
  
    def __init__(self,  roles: Sequence[tuple[str,Hashable,Hashable]],
    concepts: Sequence[tuple[Hashable, str, Vector3D]] = [],  
    z_indices: dict[str, int] = {},
    emojis : dict[str, Mobject] | None = None,
    buff = -0.2,
    **kwargs):
        """
        Manim-Mobject that represents a database consiting of binary (roles) and unary (concepts) relations 
        and could contain emojis

        Parameters:
        -----------
        roles
                the binary relations as a sequence of tuples (relation_name, element_1, element_2)
        concepts
               the unary relations as a sequence of tuples (relation_name, element) 
        z_indices
                dict to say which table is in front of another (usefull for negative buff)
        emojis
                possible emojis that replace elements
        buff 
                margin between the created tables
        
        """
        super().__init__()
        self.database = Database(roles, concepts,z_indices, emojis, buff, **kwargs )
        self.add(self.database)
        self.emojis = []
        for table in self.database.role_table_mobjects + self.database.concept_table_mobjects:
            if not emojis is None:
                ent = table.get_entries_without_labels()
                for k in range(len(ent)):
                    emoji = Emoji(ent[k].get_tex_string(), 
                                emojis.get(ent[k].get_tex_string()), 
                                Group(ent[k]), 
                                z_index = ent[k].get_z_index() + 1, 
                                update_config = {"opacity": False}, 
                                scale_factor=1.0).move_to(ent[k].get_center())
                    self.emojis.append(emoji)
                    self.add(emoji)


"""

Some slower transform animations (these wont work with emojis)

"""
def transformDBToGraph(db: Database, graph: Graph, scene: Scene,**kwargs):
    """
    Function to play the animation transforming a database to a graph

    Parameters:
    -----------
    graph
            graph to be transformed into
    db
            database to be transformed 
    scene
            the scene wher the animations should be played
    """ 
    animations = []
    garbage = []
    
    graph.update()

    scene.remove(graph)     # the transform is only done on copies
    scene.remove(db)

    old_graph = graph
    
    graph = deepcopy(graph)
    db = deepcopy(db)
    scene.add(db)

    # create vertices from entries

    entries = VGroup()
    for table in db.role_table_mobjects + db.concept_table_mobjects:
        entries.add(table.get_entries_without_labels())
    
    all_entries = entries.copy()
    all_vertices = VGroup(graph.get_vertices().values())
    
    animations.append(Transform(all_entries,all_vertices ))
    garbage.append(all_entries)
    garbage.append(all_vertices)
    
    
    # create edges from entries
    for table in db.role_table_mobjects:
            for line in table.get_rows()[1:]:
                
                edge_u = line.submobjects[0].get_tex_string()
                edge_v = line.submobjects[1].get_tex_string()
                graph_edge_mobject = VGroup(graph.edges[(edge_u,edge_v)] , graph.edge_labels[(edge_u,edge_v)])
                table_edge_mobject = VGroup (line,table.role_label.copy())
                
                animations.append(Transform(table_edge_mobject, graph_edge_mobject))
                garbage.append(table_edge_mobject)
                garbage.append(graph_edge_mobject)

            all_lines = VGroup(table.role_label, table.get_horizontal_lines(), table.get_vertical_lines())
            animations.append(Uncreate(all_lines))
    # create concept labels from entries
    for table in db.concept_table_mobjects:
            for line in table.get_rows()[1:]:
                
                u = line.submobjects[0].get_tex_string()
                graph_concept_label_mobject = VGroup(graph.concept_labels[(u,table.get_label())][0])
                table_concept_label_mobject = VGroup(line, table.get_rows()[0].copy() )
                
                animations.append(Transform(table_concept_label_mobject, graph_concept_label_mobject))
                garbage.append(table_concept_label_mobject)
                garbage.append(table_concept_label_mobject)
            
            animations.append(Uncreate(VGroup(table.get_rows()[0], table.get_horizontal_lines(), table.get_vertical_lines())))
    
    
    scene.play( Succession(animations, **kwargs))

    scene.remove(*garbage)
    scene.remove(graph)
    scene.remove(db)
    scene.add(old_graph)


def transformGraphToDB(graph:CoolDiGraph, db:Database, scene:Scene, **kwargs):
    """
    Function to play the animation transforming a graph to a database

    Parameters:
    -----------
    graph
            graph to be transformed
    db
            database to be transformed into
    scene
            the scene wher the animations should be played
    """
    animations = []         
    garbage = []            # Mobject Garbage Collector

    scene.remove(graph)     # the transform is only done on copies
    scene.remove(db)

    old_db = db
    
    graph = deepcopy(graph)
    db = deepcopy(db)
    scene.add(graph)


    graph.update()
    # transform roles
    for table in db.role_table_mobjects:
        role_name = table.get_role_name()
        table_mask = VGroup(table.get_vertical_lines(), table.get_horizontal_lines(), table.get_role_label())
        garbage.append(table_mask)
        animations.append(Create(table_mask))

        for ((u, v), role_label_mobject) in graph.edge_labels.items():
            if role_label_mobject.get_tex_string() == role_name:
                edge_mobject = graph.edges[(u,v)]
                edge_and_role_mobject = VGroup(edge_mobject, role_label_mobject)
                garbage.append(edge_and_role_mobject)
                for line in table.get_rows():
                    edge_u = line.submobjects[0].get_tex_string()
                    edge_v = line.submobjects[1].get_tex_string()
                    if (edge_u, edge_v) == (u,v):
                        animations.append(Transform(edge_and_role_mobject, line ))
    
    # transform concepts
    for table in db.concept_table_mobjects:
        concept_name_table = table.get_label()
        mask = VGroup(table.get_vertical_lines(), table.get_horizontal_lines(), table.get_rows()[0])
        animations.append(Create(mask))
        garbage.append(mask)

        for ((u, concept_name_graph), (concept_label_mobject,directions)) in graph.concept_labels.items():
            if concept_name_graph == concept_name_table:

                for line in table.get_rows():
                    edge_u = line.submobjects[0].get_tex_string()
                    if edge_u == u:
                        animations.append(Transform(concept_label_mobject , line ))
                        garbage.append(concept_label_mobject)

    animations.append(Uncreate(VGroup(*graph.vertices.values())))

    scene.play( Succession(animations, **kwargs))   # apply the animations in succession, then revert everything to normal
    
    scene.remove(*garbage)
    scene.remove(graph)
    scene.remove(db)
    scene.add(old_db)

 


class MyGraphScene(Scene):
    def construct(self):

        """
        
        Working Examples: Graph and Database can be constructed from the same Data.
        
        """
        edges = [("role","a", "b"), ("role2","b", "c"), ("role", "c", "a")]
        concepts = [("a", "A", UR),  ("b", "A", UP), ("b", "D", UR)]
        vertices = ["a", "b", "c", "d", "e"]

        graph = CoolDiGraph(
            vertices,
            edges,
            concepts=concepts,
            edge_label_config={"labelFontSize":12, "labelOffset":0.15, ("a","b"):{"labelFontSize":24, "labelOffset":0.15,}},
            labels =  True
        ).move_to((-2,0,0))
        
        """
        
        constructing the Database works in the same manner. 
        ("buff" gives you the ability to introduce spacing between the individual tables. Set it < 0 to make the tables overlap)

        """
        db = Database(edges, concepts, line_config = {"stroke_width" : 1}, buff= 0.1).move_to((2,0,0))

        """

        You may also construct the Database directly from the graph with the following method. 
        This comes in handy if you altered the graph in some way or the other

        """
        db = Database.fromCoolDiGraph(graph, line_config = {"stroke_width" : 1}).move_to((2,0,0))


        
        """
            Slow Transform from Database to Graph (does not work with emojis)
            Cleanup is done in the function, you may continue using the given Database object (db)
        """


        

        self.play(Create(graph))
        transformGraphToDB(graph, db, self, rate_function=rate_functions.rush_from, run_time=5)
        self.play(db.animate.move_to((2,1,0)))

        

        

        """
            Slow Transform from Graph to Database (does not work with emojis)
            Cleanup is done in the function, you may continue using the given Graph object (graph)
        """

        transformDBToGraph(db, graph, self, rate_function=rate_functions.ease_in_quint, run_time=8)
       

        self.wait()
        self.remove(graph)
        self.wait()
        """
        
                The (usual) fast transformation
        
        """
        db_copy = deepcopy(db)
        self.play(ReplacementTransform( db,gcopy:=graph.copy()))
        self.wait()
        self.play(ReplacementTransform(gcopy, db_copy))
        self.wait(1)
        
