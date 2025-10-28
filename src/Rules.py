import logging
from manim import *
from manim.utils import debug
from coolerDiGraph import *
from Homomorphism import *
from ChangeGraphLayout import *
from manim import there_and_back, smooth

from math import ceil, floor
from copy import deepcopy
from numpy import clip
from flexible_dashed_line import FlexibleDashedLine

'''Animation that only calls rule_loop_animation.finish()'''
class FinishRuleLoop(Wait):
    def __init__(self, rule_loop_animation, run_time=0.01, *args, **kwargs):
        super().__init__(*args, **kwargs, run_time=run_time)
        self.rule_loop_animation = rule_loop_animation

    def begin(self, *args, **kwargs):
        super().begin(*args, **kwargs)
        self.rule_loop_animation.finish()

'''Animation that only calls rule_loop_animation.reset()'''
class ResetRuleLoop(Wait):
    def __init__(self, rule_loop_animation, run_time=0.01, *args, **kwargs):
        super().__init__(*args, **kwargs, run_time=run_time)
        self.rule_loop_animation = rule_loop_animation

    def begin(self, *args, **kwargs):
        super().begin(*args, **kwargs)
        self.rule_loop_animation.reset()


class Rule():
    '''
    Class representing and managing the application of rules.
    It copies rule_head and uses it as an reference object head_graph. rule_head itself will be used for animations and stored in overlay, that is, rule_head will be in intermediate states.
    All updaters of the rule_head graph will be removed! Never add self.head_graph to the scene. rule_head shoud be added to the scene.
    The frontier of the head will be hidden, the frontier of the body should be visible but won't be changed.
    '''

    def __init__(self, rule_body: DiGraph, rule_head: DiGraph, add_updater=True, edge_attribs=['edges'],
                 hide_head_frontier=True, anchor_points:dict[Hashable, Hashable]|None = None):
        super().__init__()
        
        """
        This is a variable that may be left empty.
        Is used to provide anchor variables of the frontier for every "real_head" variable giving us the ability
          to retain the relative positions that are given by the vertice position of body_graph and head_graph.
          elements should be as follows ("real_head_variable": "frontier_variable"). 
            (Note that this will impair performace)
        """
        self.anchor_points = anchor_points

        """
        These are the values that represtent the (animation) state of the current rule. 
        
        """
        self.alpha = 0
        self.inv_wait=0
        self.create=0.6
        self.vis_wait=0.1
        self.perm_or_fade=0.3,
        self.stay_permanent=False, 
        self.transition_to_solid_line=True
        self.show_arrow_tips = True




        self.body_graph = rule_body
        self.overlay = rule_head  # drawn head graph
        self.head_graph = rule_head.copy()  # head reference, will always be invisible
        self.edge_attribs = edge_attribs
        self.hide_head_frontier = hide_head_frontier

        for up in self.head_graph.updaters:
            self.head_graph.remove_updater(up)

        for up in self.overlay.updaters:
            self.overlay.remove_updater(up)

        if add_updater:
            self.add_head_updater()

        # Compute frontier and make it invisible in the head
        self.frontier = []
        for (h_vert, dot) in rule_head.vertices.items():
            if h_vert in rule_body.vertices:
                self.frontier.append(h_vert)

        # The inverse of frontier, head vertices that do not appear in the body
        self.pure_head = []
        for (h_vert, dot) in rule_head.vertices.items():
            if h_vert not in rule_body.vertices:
                self.pure_head.append(h_vert)

        self.set_graph_opacity(self.overlay, 1)
        if hide_head_frontier:
            self.set_frontier_opacity(self.overlay, 0)

    def set_frontier_opacity(self, graph, opacity):
        for h_vert in self.frontier:
            dot = graph.vertices[h_vert]
            dot.set_opacity(opacity)
            for subm in dot.submobjects:
                if isinstance(subm, MathTex):
                    subm.set_opacity_by_tex(subm.get_tex_string(), opacity)

    def add_head_updater(self):
        self.overlay.add_updater(
            self.align_head)  # the overlay is added to the scene so it triggers the update of the invisible head_graph reference

    def change_layout(self, layout):
        self.body_graph.change_layout(layout)
        self.head_graph.change_layout(layout)
        return self

    '''This function shifts and changes the layout of the head_graph and the overlay such that the frontier is aligned to the body'''
    def align_head(self, *args):
        frontier_size = len(self.frontier)

        if not frontier_size == 0:

            frontier_diff = np.array([0, 0, 0])
            frontier_difference_dict = {}

            for front in self.frontier:
                frontier_difference_dict[front] = (self.body_graph.vertices[front].get_center() - self.head_graph.vertices[front].get_center())
                frontier_diff = frontier_diff + frontier_difference_dict[front]

            frontier_diff = frontier_diff / frontier_size
            if any(abs(frontier_diff) > 0.0001) and self.anchor_points is None:

                head_layout = dict()

                for (index, vert) in self.head_graph.vertices.items():
                    head_layout[index] = vert.get_center() + frontier_diff

                for front in self.frontier:
                    head_layout[front] = self.body_graph[front].get_center()

                self.head_graph.change_layout(head_layout)
                self.head_graph.update_edges(self.head_graph)

            elif self.anchor_points is not None:
                # if anchors are specified, they will be used to retain the relative positioning of the head_graph
                # if the anchor is not specified, the first frontier will be used. 

                head_layout = dict()
                
                for (index, vert) in self.head_graph.vertices.items():
                    if index not in self.frontier:
                        head_layout[index] = vert.get_center() + frontier_difference_dict.get(self.anchor_points.get(index, self.frontier[0]), (0,0,0))
                    else: 
                        head_layout[index] = self.body_graph[index].get_center()
                
                self.head_graph.change_layout(head_layout)
                self.head_graph.update_edges(self.head_graph)
                    

                

        self.align_overlay()
        return self

    def align_overlay(self):
        overlay_misaligned = False

        for (index, vert) in self.overlay.vertices.items():
            if any(abs(vert.get_center() - self.head_graph.vertices[index].get_center()) > 0.001):
                overlay_misaligned = True
                break

        if overlay_misaligned:
            layout = dict()
            for (index, vert) in self.head_graph.vertices.items():
                layout[index] = vert.get_center()
            self.overlay.change_layout(layout)
            for i in range(UPDATER_ITERATION):            
                self.overlay.update_edges(self.overlay)
                #for ((u,v),edge) in self.overlay.edges.items():
                #    if isinstance(edge, FlexibleDashedLine):
                #        edge.update_dashes()
        self.set_interpolate_without_align(self.alpha,
                                           self.inv_wait,
                                           self.create,
                                           self.vis_wait,
                                           self.perm_or_fade,
                                           self.stay_permanent,
                                           self.transition_to_solid_line 
                                         )
        
        

    '''This function sets the state of the introduction animation. stay_permanent toggles wether the lines are made undashed or wether the head is faded out.'''
    def set_interpolate(self, alpha, inv_wait=0, create=0.6, vis_wait=0.1, perm_or_fade=0.3, stay_permanent=False, transition_to_solid_line=True):
        self.alpha = alpha
        self.inv_wait = inv_wait
        self.create = create 
        self.vis_wait = vis_wait
        self.perm_or_fade = perm_or_fade
        self.stay_permanent = stay_permanent
        self.transition_to_solid_line = transition_to_solid_line
        self.align_head()
    
    def set_interpolate_without_align(self, alpha, inv_wait=0, create=0.6, vis_wait=0.1, perm_or_fade=0.3, stay_permanent=False, transition_to_solid_line=True):
        if alpha <= inv_wait:
            self.set_interpolate_params(0,0)
        elif inv_wait <= alpha and alpha < create + inv_wait:
            alpha = (alpha - inv_wait) / create
            self.set_interpolate_params(smooth(clip(1.8*alpha, 0, 1)), smooth(alpha))
        elif inv_wait + create <= alpha and alpha < inv_wait + create + vis_wait:
            self.set_interpolate_params(1, 1)
        else:
            alpha = (alpha - inv_wait - create - vis_wait) / perm_or_fade
            if stay_permanent:
                if transition_to_solid_line:
                    self.set_interpolate_params(1, 1, smooth(alpha))
                else:
                    self.set_interpolate_params(1, None, None)
            else:
                self.set_interpolate_params(smooth(1 - alpha))


    def set_interpolate_params(self, head_opacity, partial_head_edges = None, dashed_line_stretch = None):
#        self.set_graph_opacity(self.head_graph, 0, not self.hide_head_frontier)
        self.set_graph_opacity(self.overlay, head_opacity, show_arrow_tips=self.show_arrow_tips)
        if partial_head_edges is not None:
            self.interpolate_create(partial_head_edges)
        if dashed_line_stretch is not None:
            self.set_dashed_line_stretch(dashed_line_stretch)
        
        
        

    def set_dashed_line_stretch(self, alpha):
        
        for edge_attrib in self.edge_attribs:
            for (index, line) in getattr(self.head_graph, edge_attrib).items():
                ov_line = getattr(self.overlay, edge_attrib)[index]
                if isinstance(ov_line, FlexibleDashedLine):
                    ov_line.dashed_ratio = line.dashed_ratio + alpha*(1-line.dashed_ratio) + alpha*0.05
                    ov_line.update_dashes(force_recalculate=True)


    def interpolate_create(self, alpha):
        
        for edge_attrib in self.edge_attribs:
            for (index, line) in getattr(self.head_graph, edge_attrib).items():
                ov_line = getattr(self.overlay, edge_attrib)[index]
                if not self.show_arrow_tips and index[1] not in self.frontier:
                    alpha = clip(alpha, 0, 0.85)
                if isinstance(ov_line, DashedLine):
                    for index in range(len(ov_line.submobjects)):
                        sub_alpha = np.clip((alpha - (index / len(ov_line.submobjects))) * len(ov_line.submobjects))
                        ov_line.submobjects[index].pointwise_become_partial(line.submobjects[index], 0, sub_alpha)
                elif isinstance(ov_line, Line):
                    ov_line.pointwise_become_partial(line, 0, alpha)
                else:
                    raise RuntimeError("Unknown Line object received")

        label_alpha = np.clip((alpha - 0.3) / 0.4, 0, 1)
        for (index, label) in self.overlay.edge_labels.items():
            label.set_opacity_by_tex(label.get_tex_string(), label_alpha)
        
            

    def set_graph_opacity(self, graph, alpha, ignore_frontier=True, show_arrow_tips=True):
        for edge_attrib in self.edge_attribs:
            for (index, line) in getattr(graph, edge_attrib).items():
                if isinstance(line, DashedLine):
                    line.set_opacity(0)
                    for sm in line.submobjects:
                        sm.set_opacity(alpha)
                        if isinstance(sm, ArrowTip): 
                            sm.set_fill(sm.get_fill_color(), opacity=smooth(clip(alpha*5,0,1)))
                            if not show_arrow_tips:
                                sm.set_opacity(0)
                                sm.set_fill(sm.get_fill_color(), opacity=0.0)
                else:
                    line.set_opacity(alpha)
        for (index, label) in graph.edge_labels.items():
            label.set_opacity_by_tex(label.get_tex_string(), alpha)
        for ((vertex, concept_string), (concept_mob, dir)) in graph.concept_labels.items():
            concept_mob.set_opacity_by_tex(concept_mob.get_tex_string(), rate_functions.ease_in_circ(alpha))

            #if alpha > 0 and alpha < 1:
            #    concept_mob.scale(1 + 0.8*(alpha - 0.5))
        for (index, dot) in graph.vertices.items():
            if not ignore_frontier or index not in self.frontier:
                dot.set_stroke(opacity=alpha)
                for subm in dot.submobjects:
                    if isinstance(subm, MathTex):
                        subm.set_opacity_by_tex(subm.get_tex_string(), alpha)

    '''Returns an animation that introduces the head once'''
    def introduce_head(self, show_arrow_tips = True,**kwargs):
        self.show_arrow_tips = show_arrow_tips
        return RuleIntroductionAnimation(rule=self, mobject=None, **kwargs)

    '''Reference implementation for rule application.'''
    def setup_application_animation(self, rule_loop_animation, homomorphism, scene, hom_time=3, introduction_time=5, application_successful=True, alt_rule_head=None, change_graph_layout=False):
        #Create a copy of the rule. Use these graphs for homomorphism animation

        rule_loop_animation.pause_anim()
        self.interpolate_create(1) #deepcopy should not copy partial objects!
        r2 = deepcopy(self)
        r2.align_overlay()
        if alt_rule_head == None:
            pass
        else:
            r2.head_graph.change_vertex_name(self.pure_head[0], alt_rule_head)
            r2 = Rule(r2.body_graph, r2.head_graph)

        remove_rule_loop_animation(r2)
        self.set_graph_opacity(r2.overlay, 0, ignore_frontier=False)
        self.set_graph_opacity(r2.head_graph, 0, ignore_frontier=False)
        self.set_graph_opacity(r2.body_graph, 0, ignore_frontier=False)
        scene.add(r2.overlay)
        scene.add(r2.body_graph)

        # Movement and Reorganizing
        cgl = ChangeGraphLayout(self.body_graph, homomorphism.create_organized_graph(), suspend_mobject_updating=False)

        if change_graph_layout:
            # after cgl the loop animation will be in state (rule_loop_animation.state + cgl.run_time*rule_loop_animation.speed)
            wait_time = (1 - (
                        rule_loop_animation.state + cgl.run_time * rule_loop_animation.speed) % 1) / rule_loop_animation.speed
            frl = FinishRuleLoop(rule_loop_animation, frozen_frame=False,
                                 run_time=wait_time)  # we need this animation to stop the rule loop animation
        else:
            wait_time = (1 - (
                    rule_loop_animation.state + rule_loop_animation.speed) % 1) / rule_loop_animation.speed
            frl = FinishRuleLoop(rule_loop_animation, frozen_frame=False,
                                 run_time=wait_time)  # we need this animation to stop the rule loop animation

        # Now we can find a homomorphism from the body to the graph
        ha = HomomorphismAnimation(r2.body_graph, homomorphism, run_time=hom_time)
        # And apply the rule there. We will also play the animation at the rule
        ih = AnimationGroup(
            [self.introduce_head(stay_permanent=False), r2.introduce_head(stay_permanent=application_successful)],
            run_time=introduction_time)

        # Resume the RuleLoopAnimation
        rl = ResetRuleLoop(rule_loop_animation)

        if change_graph_layout:
            return r2, Succession(cgl, frl, ha, ih, rl, suspend_mobject_updating=False)
        return r2, Succession(frl, ha, ih, rl, suspend_mobject_updating=False)

def remove_rule_loop_animation(rule):
    #We have to collect all updaters first without removing, since mobject.remove_upder() alters the mobject.updaters array.
    updaters = []
    for method in rule.overlay.updaters:
        if method.__func__.__qualname__ == 'RuleLoopAnimation.update_rule':
            updaters.append(method)

    for up in updaters:
        rule.overlay.remove_updater(up)
        up.__self__.pause_anim()

    if len(updaters) == 0:
        logging.log(logging.INFO, "Rules: couldn't not remove rule loop animation from " + str(rule.overlay))
    rule.set_interpolate(0)
    return rule


class RuleIntroductionAnimation(Animation):

    def __init__(self, rule, stay_permanent=True, suspend_mobject_updating=False, transition_to_solid_line=True,*args, **kwargs):
        
        super().__init__(*args, suspend_mobject_updating=suspend_mobject_updating, **kwargs)
        self.rule = rule

        self.stay_permanent = stay_permanent
        self.transition_to_solid_line = transition_to_solid_line
        

    def begin(self):


        super().begin()
        self.rule.set_interpolate(0)

    def interpolate(self, alpha):


        self.rule.set_interpolate(alpha, stay_permanent=self.stay_permanent, transition_to_solid_line = self.transition_to_solid_line)


'''
This class provides an animation that introduces a rule repeatedly. Please add update_rule to the updaters of the body or overlay graph
This class supports pausing, resumings, and resetting this animation.
'''
class RuleLoopAnimation():

    def __init__(self, rule, speed=0.2):
        self.state = 0
        self.rule = rule
        self.rule.set_interpolate(0)
        self.speed = speed
        self.should_finish = False
        self.pause = False
        self.stop_time = 0

    def update_rule(self, mobject, dt):
        #logging.log(logging.INFO, "RLA update for" + str(id(self.rule.overlay)))
        if not self.pause:
            self.state = self.state + dt * self.speed
            if self.should_finish and self.state > self.stop_time:
                self.state = self.stop_time
                self.pause = True
                self.should_finish = False
            elif self.state > 1:
                self.state = self.state - 1
                self.stop_time -= 1

            self.state = float(self.state)
            self.rule.set_interpolate(self.state, stay_permanent=False)

    def set_state(self, state):
        self.state = state
        self.update_rule(None, 0)

    def finish(self, stop_time = 1.0):
        self.should_finish = True
        if self.state > stop_time:
            stop_time +=1
        self.stop_time = stop_time
        return (stop_time - self.state) / self.speed

    def pause_anim(self):
        self.pause = True

    def reset(self):
        self.pause = False
        self.should_finish = None
        self.state = 0
        self.rule.set_interpolate(self.state, stay_permanent = False)


class RulesExample(Scene):
    def construct(self):

        d00 = Dot([0,0,0],radius=0.01, fill_color=RED)
        self.add(d00)

        for i in range(-8,8):
            for j in range(-5,5):
                if i == 0 and j == 0:
                    continue
                else:
                    d = Dot([i,j,0], radius=0.01, fill_color=GREEN)
                    self.add(d)

        vert1 = ['a', 'b', 'c']
        edges1 = [('r', 'a', 'b'), ('r', 'b', 'c')]
        g1 = CoolDiGraph(vert1, edges1).shift([-3, 0, 0])
        self.play(Create(g1))

        vert_body = [1,2]
        edge_body = [('r', 1,2)]
        body = CoolDiGraph(vert_body, edge_body, layout={1: [0,-1,0], 2: [0,1,0]}).shift([0,2,0])

        vert_head = [3,2]
        edge_head = [('r', 2,3)]
        head = CoolDiGraph(vert_head, edge_head, edge_type=FlexibleDashedLine).shift([2,0,0])

#       vert_body = [1,2,3]
#       edge_body = [('r', 1,2), ('r', 2,3)]
#       body = CoolDiGraph(vert_body, edge_body, layout={3: [0,-1,0], 2: [0,1,0], 1: [2,1,0]}).shift([0,2,0])

#       vert_head = [3,1]
#       edge_head = [] #[('r', 3,1)]
#       head = CoolDiGraph(vert_head, edge_head, edge_type=FlexibleDashedLine).shift([2,0,0])
#       head.add_edges(*[('r', (3,1))], edge_type=FlexibleDashedLine, edge_config={'path_arc':1.0})

#       vert_body = [1,2,3]
#       edge_body = [('r', 1,2), ('r',2,3)]
#       body = CoolDiGraph(vert_body, edge_body, layout={3: [0,-1,0], 2: [0,1,0], 1: [1,1,0]}).shift([0,2,0])

#       vert_head = [1,3,4,5,6]
#       edge_head = [('r', 1,3), ('r', 1,4), ('r', 1,5), ('r', 4,5), ('s',4,6)]
#       head = CoolDiGraph(vert_head, edge_head, layout={1: [0,0,0], 3:[-1,-2,0], 4:[2,1,0], 5:[2,-1,0], 6:[3,1,0]}, edge_type=FlexibleDashedLine).shift([2,0,0])

        r = Rule(body, head).align_head()

        self.play(Create(body))
        self.add(head)
        #self.play(r.introduce_head(stay_permanent=True, transition_to_solid_line=True, suspend_mobject_updating=True))
        ra = RuleLoopAnimation(r, speed=0.2)
        
        
        head.add_updater(ra.update_rule)
        

        self.play(body.animate.shift([2, 0, 0]))
        self.play(Wait(1, frozen_frame=False))
        self.play( Wait(2, frozen_frame=False) )

        h = Homomorphism(body, g1, [(1, 'a'), (2, 'b'), (3, 'c')], check_hom=False)
        (r2, anims) = r.setup_application_animation(ra, h, self, introduction_time=1.0, hom_time=0.5)
        self.play(anims)

        self.play(Wait(7, frozen_frame=False))
        dt = ra.finish()
        self.play(Wait(abs(dt), frozen_frame=False))
        self.play(Uncreate(body))
