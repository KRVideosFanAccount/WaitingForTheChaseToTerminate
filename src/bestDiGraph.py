from manim import *
from Rules import *
from Homomorphism import *
from coolerDiGraph import *
from typing import (Sequence, Hashable, override)
import itertools as it
from manim.typing import (
        Point3D,
        Point3DLike,
        Vector3D,
    )
from Style import fresh_elem
import numpy as np
'''
Small Animation that ensures that a mobject gets introduced

'''




class Appear(Animation):
    def __init__(self, mobject):
        # A tiny positive run_time
        super().__init__(mobject, run_time=0.0001)
        self.introducer = True
    def interpolate_mobject(self, alpha):
        # Do nothing: object remains as it is
        pass
'''
Small Animation that ensures that a mobject gets introduced

'''
class DisAppear(Animation):
    def __init__(self, mobject):
        # A tiny positive run_time
        super().__init__(mobject, run_time=0.0001)
        self.remover = True
        self.introducer = False
    def interpolate_mobject(self, alpha):
        # Do nothing: object remains as it is
        pass

'''
Small Animation that resets the animation state of a rule

'''
class ResetInterpolate(Wait):

    def __init__(self, rule):
        super().__init__(run_time=0.01)
        self.rule = rule
        self.remover = True
        self.introducer = False

    def begin(self):
        self.rule.set_interpolate(0)
        self.rule.align_head()
    
    def interpolate_mobject(self, alpha):
        # Do nothing: object remains as it is
        pass


'''
Write Animation that leaves Dot invisible
'''
class WriteGraph(Write):

    def get_outline(self) -> Mobject:
        outline =  super().get_outline()
        out_f = outline.get_family()
        mob_f = self.mobject.get_family()

        # We just have to fix the stroke_rgbas attribute
        for i in range(len(out_f)):
            if isinstance(out_f[i], Dot):
                out_f[i].stroke_rgbas = np.array([[0,0,0,1]])
                mob_f[i].stroke_rgbas = np.array([[0,0,0,1]])

        return outline
    

class BestDiGraph(CoolDiGraph):
    """
    Check if an edge uses vertices of a given set of 'new vertices'
    
    """
    def isEdgeWithNewVertices(self,edge: Line, new_vertices:set):
        for ((u,v), e) in self.edges.items():
            if e is edge:
                return (u in new_vertices) or (v in new_vertices)
        

        print("Edge is not in Graph")
        return False

    def apply_rule_no_succession(self,rule:Rule,
                   rule_loop_animation:RuleLoopAnimation,
                   body_hom:Sequence[tuple[Hashable, Hashable]], # the body homomorphism as list
                   head_hom:Sequence[tuple[Hashable, Hashable]], # the head homomorphis. Use vertex names not in ''self'' to introduce new elements, Use vertex names in ''self'' to do the restricted chase
                   scene:Scene,
                   relative_positions:dict[Hashable, (Hashable,Point3D)] = {},   # the positions of the respective new introduced elements as directions relative to another vertice of the body
                   apply:bool = True,
                   hom_time=3,
                   introduction_time=5,
                   create_elements_time = 1.2,
                   application_successful=True,
                   change_graph_layout=False,
                   transition_to_solid_line = True,
                    shorter_animation=False,
                    synchronous_rules =True
                                 ):
        """
        Apply a given rule to this graph.

        Parameters
        ----------
        rule:Rule
                rule object that should get applied
        rule_loop_animation
                the rule-loop-animation of the rule
        body_hom
                the homomorphism of the body into this graph
        head_hom
                the homomorphism of the head into this graph (after the rule is applied)
                --> if this homomorphism specifies vertices not present in this graph they get introduced
        scene
                the scene where everything is playing
        relaive_positions
                the positions of the respective new introduced elements as directions relative to another vertice of the body
                [(introduced_vertex, (body_anchor_vertex, direction_from_anchor))]
        apply
                specifies if the rule should get applied to this graph
        application_successful
                specifies if the rule can be applied this way
        transition_to_solid_line
                specifies if the rule-introduction animation transition to a solid line
        change_graph_layout
                specifies if the graph layout is changed during the homomorphism animation
        shorter_animation
                specifies if some unecessary animations are not played
        synchronous_rules 
                specifies if the introduction of the rule at this graph and the original rule-loop should be sychronous
                (if set to true, do not change the play speed afterwards)
        hom_time
                time the homomorphism_animation should play
        introduction_time
                time the rule application takes
        create_elements_time
                time the introduction of the new elements takes
        
        """        
        
        # convert the input homomorphisms from list to function (aka dict)
        dict_body_hom = dict(body_hom)
        dict_head_hom = dict(head_hom)

        


        # copy the rule itself. This will be used to play the introduction of the actual new Elements
        # --> decouple and reset the loop animation
        r2 = deepcopy(rule)
        remove_rule_loop_animation(r2)      
        r2.set_interpolate(0)

        # create the homomorphism from body to the graph using the given homomorphism
        homomorphism = Homomorphism(r2.body_graph, self, body_hom, check_hom=True)


        # rearrange the head of the rule-copy to match the given relative positioning  
        anchor_points = {}
        for (var, (anchor_var, direction)) in relative_positions.items():
            r2.head_graph[var].move_to(r2.body_graph[anchor_var].get_center() + direction)
            anchor_points[var] = anchor_var

        r2.align_overlay()

        for i in range(UPDATER_ITERATION):
            r2.overlay.update_edges(r2.overlay)

        r2.anchor_points = anchor_points

        # add the rule-copy to the scene and make everything invisible
        r2.set_graph_opacity(r2.overlay, 0, ignore_frontier=False)
        r2.set_graph_opacity(r2.head_graph, 0, ignore_frontier=False)
        r2.set_graph_opacity(r2.body_graph, 0, ignore_frontier=False)
        scene.add(r2.overlay)
        scene.add(r2.body_graph)
        



        

        if change_graph_layout:
            # Movement and Reorganizing -- Animation
            cgl = ChangeGraphLayout(rule.body_graph, homomorphism.create_organized_graph(), suspend_mobject_updating=False)
            # after cgl the loop animation will be in state (rule_loop_animation.state + cgl.run_time*rule_loop_animation.speed)
            wait_time = (1 - (
                        rule_loop_animation.state + cgl.run_time * rule_loop_animation.speed) % 1) / rule_loop_animation.speed
            frl = FinishRuleLoop(rule_loop_animation, frozen_frame=False,
                                 run_time=wait_time)  # we need this animation to stop the rule loop animation
        elif synchronous_rules:
            wait_time = (1 - (
                    rule_loop_animation.state + rule_loop_animation.speed) % 1) / rule_loop_animation.speed
            frl = FinishRuleLoop(rule_loop_animation, frozen_frame=False,
                                 run_time=wait_time)  # we need this animation to stop the rule loop animation
        else:
            frl = Wait(0.01)

        # Resume the RuleLoopAnimation
        if synchronous_rules:
            rl = AnimationGroup(ResetRuleLoop(rule_loop_animation), Appear(self), ResetInterpolate(r2))
        else:
            rl = AnimationGroup(Appear(self), ResetInterpolate(r2))

        # Now we can find a homomorphism from the body to the graph
        if application_successful:
            ha = Succession(ResetInterpolate(r2), HomomorphismAnimation(r2.body_graph, homomorphism, run_time=hom_time), ResetInterpolate(r2))
            '''homomorphism is on rule not r2 -- Is this a Problem?'''
        else:
            ha = ErrHomAnimation(rule.body_graph, homomorphism,run_time=hom_time)
            if change_graph_layout:
                return r2, [cgl, frl, ha,rl]
            else:
                return r2, [frl, ha, rl]



        create_elements = None
        if apply:
            # If the rule should be applied

            image_head_hom = set([dict_head_hom.get(v) for v in r2.pure_head])
            dict_inv_head_hom = {v : k for (k,v) in dict_head_hom.items()}

            # calculate the edges + vertices and concepts that will need to apper
            new_edges = []
            for (r,u,v) in rule.head_graph.role_data:
                new_edges.append((r, (dict_head_hom.get(u), dict_head_hom.get(v))))

            new_vertices =  image_head_hom - set(self.vertices.keys())

            concepts = []
            for v in r2.head_graph.vertices.keys():
                for (w, concept), (text,dir) in r2.head_graph.concept_labels.items():
                    if v == w:
                        concepts.append((dict_head_hom.get(w),concept,dir))


            # scale the frontier-vertices of the rule-copy according to the corresponding ones (their images) in the graph
            for front in r2.frontier:
                r2.head_graph[front].scale_to_fit_width(self[dict_body_hom.get(front)].width )
                r2.overlay[front].scale_to_fit_width(self[dict_body_hom.get(front)].width )


            # copy the path_arc config of the rule into a new edge-config 
            # (used to match the path arc of the introduced edges to that of the rule itself)
            edge_config = {}
            for ((u,v), edge) in r2.head_graph.edges.items():
                edge_config[(dict_head_hom.get(u), dict_head_hom.get(v))] = {"path_arc" : edge.path_arc}


            # add the new mobjects that get introduced by the rule
            new_elements = []
            if len(new_edges) > 0:
                new_elements = self.add_edges(*new_edges, labels = False, edge_config=edge_config)
                # this also includes newly added vertices

            new_concepts = []
            if len(concepts) > 0:
                new_concepts = self.add_concept_labels(*concepts)

            # the introduced variable is not shown in the application
            if shorter_animation:
                for v in r2.overlay.vertices:
                    r2.overlay.vertices[v].set_color(BLACK)

            # scale and position the new introduced vertices of rule-copy and the graph itself uniformly (corresponding to the relative positions)
            for v in image_head_hom:

                r2.head_graph[dict_inv_head_hom.get(v)].scale_to_fit_width(self[v].width )
                r2.overlay[dict_inv_head_hom.get(v)].submobjects[1].scale_to_fit_width(self[v].width)
                anchor = anchor_points.get(dict_inv_head_hom.get(v, "ValueError"), (list(r2.body_graph.vertices.keys())[0]) )
                if v in new_vertices:
                    anchor_pos = r2.body_graph[anchor].get_center()
                    relative_dir =  r2.head_graph[dict_inv_head_hom.get(v)].get_center() - anchor_pos
                    self[v].move_to(self[dict_body_hom.get(anchor)].get_center() + relative_dir)
            r2.head_graph.update()
            r2.overlay.update()

            # Yes this should be N updaters, this is to center the arced lines
            '''
            Explanation: the positioning of lines with path arc is a (continous) fixpoint operation, 
            this is due to the internal handling of path_arc lines in manim itself which is not faithful to the given value of path_arc itself.
            '''
            for i in range(UPDATER_ITERATION):
                self.update()


            # define fade animations for the newly introduced elements (this has to be done differently for each and every type)
            '''
            Explanation: Every Mobject-Subclasss handles opacity differently. 
            '''
            fade_animations = []
            create_elements2 = []

            for element in new_elements:
                if isinstance(element, Line):
                    element.set_opacity(0.0)
                    line_fade_in = [element.animate(rate_function=rate_functions.smooth).set_stroke(WHITE, opacity=1.0)]
                    tip_fade_in=None
                    if len(element.get_tips()) > 0:
                        tip_fade_in = element.get_tips()[0].animate(rate_function=rate_functions.smooth).set_opacity(1.0)


                        # Only indicate the tip of the line, if the vertices are not newly created
                        if not self.isEdgeWithNewVertices(element, new_vertices):
                           add_tip_animation = Succession(tip_fade_in, Indicate(element.get_tips()[0], scale_factor=1.5, color=fresh_elem))
                        else:
                            add_tip_animation = tip_fade_in
                        if shorter_animation:
                            create_elements2.append(add_tip_animation)
                            fade_animations.append(LaggedStart(*line_fade_in, tip_fade_in, lag_ratio=0.001))

                        else:
                            fade_animations.append(LaggedStart(*line_fade_in, add_tip_animation, lag_ratio=0.001))
                    else:
                        if tip_fade_in is not None:
                            line_fade_in.append(tip_fade_in)
                        fade_animations.append(AnimationGroup(*line_fade_in))

                elif isinstance(element, SingleStringMathTex):
                    element.set_opacity(0.0)
                    element.update()
                    fade_animations.append(element.animate(rate_functions=rate_functions.smooth).set_opacity(1.0))
                elif isinstance(element, VGroup):
                    if shorter_animation:
                        element.set_stroke(WHITE, opacity=0.0)
                        create_elements2.append(Succession(
                            element.animate(rate_functions=rate_functions.smooth).set_stroke(WHITE, opacity=1.0),
                            Indicate(element, color=fresh_elem)
                            ))
                    else:
                        element.set_stroke(WHITE, opacity=0.0)
                        fade_animations.append(Succession(element.animate(rate_functions=rate_functions.smooth).set_stroke(WHITE,opacity=1.0),
                                                          Indicate(element, color=fresh_elem)
                                                          ))
            for concept in new_concepts:
                concept.set_opacity(0.0)
                concept.update()
                if not shorter_animation:
                    fade_animations.append(Succession(concept.animate(rate_functions=rate_functions.ease_in_circ).set_opacity(1.0), Indicate(concept, scale_factor=1.5,color=fresh_elem)))
                    #fade_animations.append(Succession(AnimationGroup(GrowFromPoint(concept,concept.get_center())), Indicate(concept)))

            create_elements = AnimationGroup(FadeOut(r2.overlay), *fade_animations, run_time=create_elements_time)

        else:
            create_elements = AnimationGroup(FadeOut(r2.overlay), run_time=create_elements_time)

        animation_apply_rule_at_graph = r2.introduce_head(stay_permanent=apply,show_arrow_tips=not shorter_animation, transition_to_solid_line=transition_to_solid_line)
        if synchronous_rules:
            ih = AnimationGroup(
            [rule.introduce_head(stay_permanent=False), animation_apply_rule_at_graph],
            run_time=introduction_time)
        else:
            ih = AnimationGroup(
            [animation_apply_rule_at_graph],
            run_time=introduction_time)


        

        """
        Need to add the graph add edge and vertice animation here (delete the unused stuff and let the dashed line gently fade out)
        """

        # Resume the RuleLoopAnimation
        #rl = AnimationGroup(ResetRuleLoop(rule_loop_animation), Appear(self))
        if shorter_animation:
            return r2, [frl, ha, AnimationGroup(ih, create_elements2), create_elements, rl]
        if change_graph_layout:
            return r2, [cgl, frl, ha, ih, create_elements, rl]
        return r2, [frl, ha, ih, create_elements, rl]

    def apply_rule(self,rule:Rule,
                   rule_loop_animation:RuleLoopAnimation,
                   body_hom:Sequence[tuple[Hashable, Hashable]], # the body homomorphism as list
                   head_hom:Sequence[tuple[Hashable, Hashable]], # the head homomorphis. Use vertex names not in ''self'' to introduce new elements, Use vertex names in ''self'' to do the restricted chase
                   scene:Scene,
                   relative_positions:dict[Hashable, (Hashable,Point3D)] = {},   # the positions of the respective new introduced elements as directions relative to another vertice of the body
                   apply:bool = True,
                   hom_time=3,
                   introduction_time=5,
                   create_elements_time=1.2,
                   application_successful=True,
                   transition_to_solid_line = True,
                   change_graph_layout=False,
                   shorter_animation=False,
                   synchronous_rules=True):
        """
        Apply a given rule to this graph.

        Parameters
        ----------
        rule:Rule
                rule object that should get applied
        rule_loop_animation
                the rule-loop-animation of the rule
        body_hom
                the homomorphism of the body into this graph
        head_hom
                the homomorphism of the head into this graph (after the rule is applied)
                --> if this homomorphism specifies vertices not present in this graph they get introduced
        scene
                the scene where everything is playing
        relaive_positions
                the positions of the respective new introduced elements as directions relative to another vertice of the body
                [(introduced_vertex, (body_anchor_vertex, direction_from_anchor))]
        apply
                specifies if the rule should get applied to this graph
        application_successful
                specifies if the rule can be applied this way
        transition_to_solid_line
                specifies if the rule-introduction animation transition to a solid line
        change_graph_layout
                specifies if the graph layout is changed during the homomorphism animation
        shorter_animation
                specifies if some unecessary animations are not played
        synchronous_rules 
                specifies if the introduction of the rule at this graph and the original rule-loop should be sychronous
                (if set to true, do not change the play speed afterwards)
        hom_time
                time the homomorphism_animation should play
        introduction_time
                time the rule application takes
        create_elements_time
                time the creation of the new elements takes
        
        """        


        (r2, animations) = self.apply_rule_no_succession(rule,
                   rule_loop_animation,
                   body_hom,
                   head_hom,
                   scene,
                   relative_positions=relative_positions,
                   apply=apply,
                   hom_time=hom_time,
                   introduction_time=introduction_time,
                   create_elements_time=create_elements_time,
                   application_successful=application_successful,
                   change_graph_layout=change_graph_layout,
                   transition_to_solid_line=transition_to_solid_line,
                    shorter_animation=shorter_animation,
                    synchronous_rules=synchronous_rules)
        return (r2, Succession(*animations, suspend_mobject_updating=False))
    
class MyGraphScene(Scene):
    def construct(self):
        """

        Small teach by example on how to use the class functions

        """

        """
        Bugs: 
            - change graph layout does somehow not update the concept labels

        
        """

        vertices = ["k", "p", "c", "b"]
        edges = [("affects","p", "k"), ("allegicTo","k", "c"), ("allegicTo", "k", "b")]
        concepts = [("k", "Cat", UR),  ("p", "HappyPot", UR), ("p", "PlantBased", UL)]

        graph = BestDiGraph(
            vertices,
            edges,
            concepts=concepts,
            edge_config={("p","k"): {"path_arc": 1.0} },
            edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True
        ).move_to((-2,0,0))

        graph.update_arrows(graph)
        self.play(Create(graph))
        graph.update()
        vertices_body = ["x","y"]
        edges_body = [("affects", "x","y"),("likes", "y","x")]
        concepts_body = [("x","HappyPot", UL)]
        body_1 = BestDiGraph(vertices_body,
            edges_body,
            concepts=concepts_body,
            edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True).move_to((2,0,0))

        vertices_head = ["x","y","z"]
        edges_head = [("likes", "y","z"), ("contains", "x","z")]
        concepts_head = [("z", "Plant", UR)]
        head_1 = BestDiGraph(vertices_head,
            edges_head,
            concepts=concepts_head,
            edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            edge_config={("y","z"):{"path_arc": 1.0, "stroke_width":2}},
            labels =  True,
            edge_type=FlexibleDashedLine).move_to((3,0,0))
        #head_1._add_edge(("x","z"), role_name="contains", edge_config={"path_arc": 1.0}, edge_type=FlexibleDashedLine)
        rule_1 = Rule(body_1, head_1).align_head()

        self.play(Create(body_1))
        self.add(head_1)

        ra = RuleLoopAnimation(rule_1)
        #self.play(rule_1.introduce_head())


        head_1.add_updater(ra.update_rule)

        self.play(Wait(2, frozen_frame=False))
        remove_rule_loop_animation(rule_1)      
        rule_1.set_interpolate(0)

        self.play(AnimationGroup(rule_1.introduce_head(stay_permanent=True),run_time=0.5))

        (r2, anims) = graph.apply_rule(
            rule_1,                             # rule itself
            ra,                                 # rule animation
            [("x","p"),("y","k")],              # body Homomorphism
            [("x","p"),("y","k"),("z","h")],    # head Homomorphism
            self,                               # the scene
            {"z": ("x",(2,1,0))},               # relative positioning of the new introduced elements
            change_graph_layout=False,
            apply = True,                      # should the rule be applied
            application_successful=True,
            hom_time=.5,
            introduction_time=1)        # is the rule applicable
        graph.update()

        self.play(anims)

        self.play(Wait(7, frozen_frame=False))

        (r2, anims) = graph.apply_rule(
            rule_1,                             # rule itself
            ra,                                 # rule animation
            [("x","p"),("y","h")],              # body Homomorphism
            [("x","p"),("y","h"),("z","h2")],    # head Homomorphism
            self,                               # the scene
            {"z": ("y",(-2,0,0))},               # relative positioning of the new introduced elements
            change_graph_layout=False,
            apply = True,                      # should the rule be applied
            application_successful=True,
            hom_time=.5,
            introduction_time=1)        # is the rule applicable
        graph.update()

        self.play(anims)
        r2.align_overlay()

        """
        For some reason we need to add the graph manually to the scene AFTER we played the animations
        
        """

        self.play(graph["h2"].animate.move_to((3,0,0)))


        self.play(Wait(7, frozen_frame=False))
        dt = ra.finish()
        self.play(Wait(dt, frozen_frame=False))
        self.play(Uncreate(body_1))







