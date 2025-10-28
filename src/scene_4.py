from bestDiGraph import *
from Rules import *
from manim import *
from copy import deepcopy
from scene_3 import apply_r1_multiple_times, apply_r2_multiple_times, create_rule1, create_rule2, rule_heading_offset
from sound_effects import *
import Style


class Scene4(Scene):
    def play_first_part(self):
        config_rule = {"opacity": False,
                       "position": True,
                       "scale": False}

        vampireparent = VGroup(MathTex(r'\cdot'))
        vampire = Emoji(r'\cdot', ("🧛🏻", "vampire.png", None), vampireparent, update_config=config_rule,
                        scale_factor=12)
        vampire.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        ownerparent = VGroup(MathTex(r'\cdot'))
        owner = Emoji(r'\cdot', ("🧙", "owner.png", None), ownerparent, update_config=config_rule, scale_factor=12)
        owner.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        apprenticeparent = VGroup(MathTex(r'\cdot'))
        apprentice = Emoji(r'\cdot', ("🧑‍🎓", "apprentice.png", None), apprenticeparent, update_config=config_rule,
                           scale_factor=12)
        apprentice.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        mrwparent = VGroup(MathTex(r'\cdot'))
        mrw = Emoji(r'\cdot', ("🧑‍💼", "misterrealworld.png", None), mrwparent, update_config=config_rule,
                    scale_factor=12)
        mrw.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        sleepparent = VGroup(MathTex(r'\cdot'))
        sleep = Emoji(r'\cdot', ("😴", "sleep.png", None), sleepparent, update_config=config_rule, scale_factor=12)
        sleep.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        bellparent = VGroup(MathTex(r'\cdot')).move_to(3 * UP + 8 * RIGHT)
        bell = Emoji(r'\cdot', ("🔔", "bell.png", None), bellparent, update_config=config_rule, scale_factor=12)
        bell.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        g2 = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], layout={'a': [0, 0, 0], 'b': [2, 0, 0]}).shift([0, 0, 0])
        g2._add_vertex(vertex='z1', position=(4, 0, 0), label=False)
        g2._add_edge(('z1', 'b'), role_name='p', edge_config={"path_arc": 2.0})
        g2._add_edge(('b', 'z1'), role_name='p')

        for i in range(2, 10):
            new_vertex = f'z{i}'
            g2._add_vertex(vertex=new_vertex, position=(2 + (i*2), 0, 0), label=False)
            g2._add_edge((f'z{i-1}', f'z{i}'), role_name='p')
            g2._add_edge((f'z{i}', f'z{i-1}'), role_name='p', edge_config={"path_arc": 2.0})
        g2.shift((7, 0, 0))

        apprenticeparent.shift(2 * DOWN + 9 * LEFT)
        apprentice.shift(2 * DOWN + 8 * LEFT)

        ownerparent.shift(2 * DOWN + 8 * LEFT)
        owner.shift(2 * DOWN + 8 * LEFT)

        vampireparent.shift(1 * DOWN + 8 * RIGHT)
        vampire.shift(DOWN + 8 * RIGHT)

        mrwparent.shift(2 * DOWN + 8 * RIGHT)
        mrw.shift(2 * DOWN + 8 * RIGHT)

        self.add(apprentice, owner, vampire, mrw)

        self.add(bell)
        bellparent.shift(2 * LEFT)
        self.play(bell.animate.shift(2 * LEFT), run_time=.5)

        bell_sound(self)

        self.add_sound("../recordings/Final/Scene4-final.flac", time_offset=1.5)

        ownerparent.shift(3 * RIGHT)
        apprenticeparent.shift(3 * RIGHT)
        mrwparent.shift(3 * LEFT)

        self.play(Succession(Rotate(bell, -PI / 7,
                                    rate_func=rate_functions.ease_out_quad),
                             Rotate(bell, 2 * PI / 7,
                                    rate_func=rate_functions.ease_in_out_quad),
                             Rotate(bell, -2 * PI / 7,
                                    rate_func=rate_functions.ease_in_out_quad),
                             Rotate(bell, 2 * PI / 7,
                                    rate_func=rate_functions.ease_in_out_quad),
                             Rotate(bell, -2 * PI / 7,
                                    rate_func=rate_functions.ease_in_out_quad),
                             Rotate(bell, 2 * PI / 7,
                                    rate_func=rate_functions.ease_in_out_quad),
                             Rotate(bell, -PI / 7,
                                    rate_func=rate_functions.ease_in_quad)),
                  owner.animate.shift(3 * RIGHT),
                  apprentice.animate.shift(3 * RIGHT),
                  mrw.animate.shift(3 * LEFT),
                  run_time=2)

        bellparent.shift(2 * RIGHT)
        self.play(bell.animate.shift(2 * RIGHT), run_time=.5)

        self.remove(bell, bellparent)

        apprenticeparent.shift(.5 * UP)
        self.play(apprentice.animate.shift(.5 * UP), run_time=.25)
        apprenticeparent.shift(.5 * DOWN)
        self.play(apprentice.animate.shift(.5 * DOWN), run_time=.25)

        self.wait(2.5)

        mrwparent.shift(.5 * UP)
        self.play(mrw.animate.shift(.5 * UP), run_time=.25)
        mrwparent.shift(.5 * DOWN)
        self.play(mrw.animate.shift(.5 * DOWN), run_time=.25)

        self.wait(1.5)

        vampireparent.shift(2 * LEFT)
        self.play(AnimationGroup(vampire.animate.shift(2 * LEFT), g2.animate.shift((-5, 0, 0)), run_time=1.5))
        self.wait(1)
        vampireparent.shift(2 * RIGHT)
        self.play(AnimationGroup(vampire.animate.shift(2 * RIGHT), FadeOut(g2, shift=(5, 0, 0)), run_time=1.5))

        self.remove(vampire, vampireparent)

        # self.wait(1)

        mrwparent.shift(5 * LEFT)
        self.play(mrw.animate.shift(5 * LEFT), run_time=2)

        ################################################################################
        ################################## First Part ##################################
        ################################################################################

        #name_string = MathTex(r'\text{Previous rules}', color=YELLOW).scale(.7).shift((-3, 2.5, 0))
        name_string = Style.create_heading('Rule 1')
        name_string2 = Style.create_heading('Rule 2')


        (body, head, r1) = create_rule1()
        (body2, head2, r2) = create_rule2()

        mrwparent.shift(.5 * UP)
        self.play(mrw.animate.shift(.5 * UP), run_time=.25)
        mrwparent.shift(.5 * DOWN)


        name_string.move_to(body.vertices['y'].get_center()+rule_heading_offset)
        name_string2.move_to(body2.get_center()+rule_heading_offset)


        self.play(FadeIn(name_string),FadeIn(name_string2),
                  FadeIn(body, shift=UP),
                  FadeIn(body2, shift=UP),
                  AnimationGroup(mrw.animate.shift(.5 * DOWN), run_time=.25)
                  )

        self.add(head)
        self.add(head2)

        ra1 = RuleLoopAnimation(r1)
        head.add_updater(ra1.update_rule)
        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)

        self.play(Wait(abs(1), frozen_frame=False))
        self.wait()

        mrwparent.shift(8 * LEFT)
        ownerparent.shift(3 * LEFT)
        apprenticeparent.shift(3 * LEFT)
        self.play(mrw.animate.shift(8 * LEFT), owner.animate.shift(3 * LEFT), apprentice.animate.shift(3 * LEFT),
                  run_time=3)

        self.remove(apprentice, apprenticeparent, owner, ownerparent, mrw, mrwparent)

        vert1 = ['a', 'b']
        edges1 = [('p', 'a', 'b')]
        g1 = BestDiGraph(vert1, edges1, layout={'a': [0, 0, 0], 'b': [2, 0, 0], 'c': [4, 0, 0]}).shift([-3, -1.5, 0])
        self.play(Create(g1))

        anims_to_play = apply_r1_multiple_times(g1,
                                                self,
                                                first_body_vertex='a',
                                                second_body_vertex='b',
                                                new_element_index=1,
                                                num_applications=4,
                                                rule=r1,
                                                rule_loop_animation=ra1,
                                                shorter_animation=True)

        target_time = 23.00
        
        for i in range(4):
            pop_sound(self, wait_time=((i+POP_PROP)/4.)*(target_time-self.time), volume=POP_GAIN-4*i)
        self.play(Succession(*anims_to_play), run_time=target_time-self.time)

        
        anims_to_play = apply_r2_multiple_times(g1, self, first_body_vertex='a', second_body_vertex='b',
                                                third_body_vertex='z1',
                                                num_applications=4, rule=r2, rule_loop_animation=ra2, apply=True)
        target_time = 26.00
        
        for i in range(4):
            pop_sound(self, wait_time=((i+POP_PROPrule2)/4.)*(target_time-self.time), volume=POP_GAIN-16-4*i)
        self.play(Succession(*anims_to_play), run_time=target_time - self.time)

        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))
        ra1.finish()
        ra2.finish()

    def play_second_part(self):
        ################################################################################
        ################################## Second Part #################################
        ################################################################################

        theorem1 = MathTex(r"\mathcal{R}, \mathcal{D} \models q\text{ is }",r"\textbf{undecidable.}", font_size=Style.explanation_font_size, ).move_to(
            (-1, 1, 0))
        theorem1.set_color_by_tex(r'\textbf{undecidable.}', Style.undecidable_border)
        theorem1.add_background_rectangle(color=Style.undecidable_border, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1, buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)

        theorem2 = Tex(r"Termination of the chase is ",r"\textbf{undecidable.}", font_size=Style.explanation_font_size).move_to(
            (0, -0.2, 0))
        theorem2.set_color_by_tex(r'\textbf{undecidable.}', Style.undecidable_border)
        theorem2.add_background_rectangle(color=Style.undecidable_border, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1, buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)
        theorem2.align_to(theorem1, LEFT)

        # self.add(theorem1, theorem2)

        #terminating_string = MathTex(r'\text{Terminating rules}', color=YELLOW).scale(.7).shift((-3, 2.5, 0))
        #terminating_string = Text('Terminating rules',  font_size=34, color=WHITE).shift((-3,2.5,0))
        terminating_string = Style.create_heading('Terminating rules').shift((-3,2.5,0))

        r1_syntax = MathTex(r'p(x, y) \rightarrow \exists z ~ q(y, z)').shift((-3, 1, 0))
        r2_syntax = MathTex(r'p(x, y) \wedge q(y, z) \rightarrow q(z, y)').shift((-3, -.7, 0))

        vert1 = ['a', 'b']
        edges1 = [('p', 'a', 'b')]
        g1 = BestDiGraph(vert1, edges1, layout={'a': [0, 0, 0], 'b': [2, 0, 0], 'c': [4, 0, 0]}).shift([-3, -1.5, 0])

        vert_body1 = ['x', 'y']
        edge_body1 = [('p', 'x', 'y')]
        body1 = BestDiGraph(vert_body1, edge_body1, layout={'x': [0, 0, 0], 'y': [2, 0, 0]}).next_to(r1_syntax, RIGHT).shift(2 * RIGHT)

        vert_head1 = ['y', 'z']
        edge_head1 = [('q', 'y', 'z')]
        head1 = BestDiGraph(vert_head1, edge_head1, layout={'y': [2, 0, 0], 'z': [4, 0, 0]}, edge_type=FlexibleDashedLine)
        r1 = Rule(body1, head1).align_head()

        vert_body2 = ['x', 'y', 'z']
        edge_body2 = [('p', 'x', 'y'), ('q', 'y', 'z')]
        body2 = BestDiGraph(vert_body2, edge_body2, layout={'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}).next_to(r1_syntax, RIGHT).shift(1.7 * DOWN).shift(2 * RIGHT)
        vert_head2 = ['z', 'y']
        edge_head2 = []
        head2 = BestDiGraph(vert_head2, edge_head2, layout={'z': [4, 0, 0], 'y': [2, 0, 0]}, edge_type=FlexibleDashedLine)
        head2._add_edge(('z', 'y'), role_name='q', edge_config={"path_arc": 2.0}, edge_type=FlexibleDashedLine)

        r2 = Rule(body2, head2).align_head()

        self.play(FadeIn(terminating_string, shift=RIGHT),
                  FadeIn(r1_syntax, shift=RIGHT),
                  FadeIn(body1, shift=RIGHT),
                  FadeIn(r2_syntax, shift=RIGHT),
                  FadeIn(body2, shift=RIGHT)
                  )

        self.add(head1)
        self.add(head2)

        ra1 = RuleLoopAnimation(r1)
        head1.add_updater(ra1.update_rule)

        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)

        self.wait(4)
        self.play(FadeOut(r1_syntax),
                  FadeOut(r2_syntax),
                  r1.body_graph.animate.shift(-body1.vertices['x'].get_center()+[-5,1.8,0]),
                  r2.body_graph.animate.shift(-body2.vertices['y'].get_center()+[2+1,1.8,0]),
                  terminating_string.animate.move_to([-3,1.8,0]+rule_heading_offset),
                  Create(g1))

        # self.play(Wait(1, frozen_frame=False))
        # dt = ra1.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))
        (r3, anims) = g1.apply_rule(r1,
                                    ra1,
                                    [('x', 'a'), ('y', 'b')],
                                    [('y', 'b'), ('z', 'c')],
                                    self,
                                    {'z': ('y', (2, 0, 0))},
                                    synchronous_rules=False,
                                    hom_time=1,
                                    shorter_animation=True,
                                    introduction_time=2)  # is the rule applicable
        pop_sound(self, wait_time=POP_PROP*3)
        self.play(anims)

        # dt = ra2.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))

        (r4, anims) = g1.apply_rule(r2,
                                          ra2,
                                          [('x', 'a'), ('y', 'b'), ('z', 'c')],
                                          [('z', 'c'), ('y', 'b')],
                                          self,
                                          {},
                                          synchronous_rules=False,
                                          hom_time=1,
                                          shorter_animation=True,
                                          introduction_time=2)  # is the rule applicable
        pop_sound(self, wait_time=POP_PROPrule2*3-.3)

        self.play(anims)



        
        config_rule = {"opacity": False,
                       "position": True,
                       "scale": False}
        
        thinkingparent = VGroup(MathTex(r'\cdot')).move_to(0.5*RIGHT+2.5*DOWN)
        thinking = Emoji(r'\cdot', ("🤔", "thinking.png", None) , thinkingparent, update_config=config_rule, scale_factor = 12)
        thinking.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        q1parent = VGroup(MathTex(r'\cdot')).next_to(thinking, UP+LEFT)
        q1 = Emoji(r'\cdot', ("❔", "question1.png", None) , q1parent, update_config=config_rule, scale_factor = 6).rotate(PI/5)
        q1.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        q2parent = VGroup(MathTex(r'\cdot')).next_to(thinking, UP).shift(.2*UP)
        q2 = Emoji(r'\cdot', ("❔", "question2.png", None) , q2parent, update_config=config_rule, scale_factor = 6)
        q2.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        q3parent = VGroup(MathTex(r'\cdot')).next_to(thinking, UP+RIGHT)
        q3 = Emoji(r'\cdot', ("❔", "question3.png", None) , q3parent, update_config=config_rule, scale_factor = 6).rotate(-PI/5)
        q3.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        q4parent = VGroup(MathTex(r'\cdot')).next_to(thinking, DOWN+RIGHT)
        q4 = Emoji(r'\cdot', ("❔", "question4.png", None) , q4parent, update_config=config_rule, scale_factor = 6).rotate(PI+PI/5)
        q4.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        q5parent = VGroup(MathTex(r'\cdot')).next_to(thinking, DOWN).shift(.2*DOWN)
        q5 = Emoji(r'\cdot', ("❔", "question5.png", None) , q5parent, update_config=config_rule, scale_factor = 6).rotate(PI)
        q5.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        q6parent = VGroup(MathTex(r'\cdot')).next_to(thinking, DOWN+LEFT)
        q6 = Emoji(r'\cdot', ("❔", "question6.png", None) , q6parent, update_config=config_rule, scale_factor = 6).rotate(PI-PI/5)
        q6.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])


        target_time = 56.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))
        self.play(r1.body_graph.animate.shift((0, 8, 0)),
                  r2.body_graph.animate.shift((0, 8, 0)),
                  terminating_string.animate.shift((0, 8, 0)),
                  g1.animate.shift((0, -8, 0)))

        self.wait(1)
        self.play(FadeIn(theorem1))
        self.play(FadeIn(thinking, shift=2*UP))
        
        self.wait()
        self.play(FadeIn(q1, target_position=thinking))
        self.play(FadeIn(q2, target_position=thinking))
        self.play(FadeIn(q3, target_position=thinking))
        

        target_time = 68.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))
        self.play(FadeIn(theorem2))
        self.wait(2)
        self.play(FadeIn(q4, target_position=thinking))
        self.play(FadeIn(q5, target_position=thinking))
        self.play(FadeIn(q6, target_position=thinking))
        self.wait()
        qmarks = Group(q1, q2, q3, q4, q5, q6)
        self.play(Wiggle(qmarks))
        

    def play_third_part(self):
        ################################################################################
        ################################## Third Part ##################################
        ################################################################################

        # setup
        (body1, head, r1) = create_rule1()
        (body2, head2, r2) = create_rule2()
 
        self.play(FadeIn(body1, shift=RIGHT), FadeIn(body2, shift=RIGHT))
        self.add(head)
        self.add(head2)

        ra1 = RuleLoopAnimation(r1)
        head.add_updater(ra1.update_rule)

        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)

        vert1 = ['a', 'b']
        edges1 = [('p', 'a', 'b')]
        g1 = BestDiGraph(vert1, edges1, layout={'a': [0, 0, 0], 'b': [2, 0, 0], 'c': [4, 0, 0]}).shift([-2, -1.5, 0])
        self.play(FadeIn(g1, shift=RIGHT))

        # first rule application
        target_time = 80.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        (r4, anims) = g1.apply_rule(r1,
                                    ra1,
                                    [('x', 'a'), ('y', 'b')],
                                    [('y', 'b'), ('z', 'z1')],
                                    self,
                                    {'z': ('y', (2, 0, 0))},
                                    hom_time=1,
                                    introduction_time=2,
                                    change_graph_layout=False,
                                    apply=True,  # should the rule be applied
                                    # application_successful=True,
                                    shorter_animation=True)  # is the rule applicable
        pop_sound(self, wait_time=5)

        # dt = ra1.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))
        self.play(anims)

        # second rule application
        target_time = 84.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        (r3, anims) = g1.apply_rule(r2,
                                    ra2,
                                    [('x', 'a'), ('y', 'b'), ('z', 'z1')],
                                    [('y', 'b'), ('z', 'z1')],
                                    self,
                                    {},
                                    hom_time=1,
                                    introduction_time=2,
                                    change_graph_layout=False,
                                    apply=True,  # should the rule be applied
                                    # application_successful=True,
                                    shorter_animation=True)  # is the rule applicable
        pop_sound(self, wait_time=3)

        # dt = ra2.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))
        self.play(anims)

        ################################################################################
        ################################# Homomorphisms ################################
        ################################################################################

        # ####################################### 1 ######################################
        #
        # r_mock_verts = ['x', 'y', 'z']
        # r_mock_edges = [('p', 'x', 'y')]
        # r_mock = BestDiGraph(r_mock_verts, r_mock_edges, layout={'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}).shift([-5, 2, 0])
        # r_mock._add_edge(('y', 'z'), edge_config={'path_arc': 0.0}, role_name='p', edge_type=FlexibleDashedLine)
        # self.wait(2)
        #
        # self.add(g1, r_mock)
        #
        # h = Homomorphism(r_mock, g1, [('x', 'a'), ('y', 'b'), ('z', 'z1')], check_hom=True)
        #
        # ha = HomomorphismAnimation(r_mock, h, run_time=2)
        #
        # self.play(ha)
        # g1.suspend_updating()
        # self.play(Indicate(g1.edges[('b', 'z1')]))
        # g1.resume_updating()
        #
        # ####################################### 2 ######################################
        #
        # r_mock_verts = ['x', 'y', 'z']
        # r_mock_edges = [('p', 'x', 'y')]
        # r_mock = BestDiGraph(r_mock_verts, r_mock_edges, layout={'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}).shift(
        #     [-5, 2, 0])
        # r_mock._add_edge(('y', 'z'), role_name='p', edge_config={'path_arc': 0.0}, edge_type=FlexibleDashedLine)
        #
        # self.add(g1, r_mock)
        #
        # h = Homomorphism(r_mock, g1, [('x', 'b'), ('y', 'z1'), ('z', 'b')], check_hom=True)
        #
        # ha = HomomorphismAnimation(r_mock, h, run_time=2)
        #
        # self.play(ha)
        # g1.suspend_updating()
        # self.play(Indicate(g1.edges[('z1', 'b')]))
        # g1.resume_updating()
        #
        # ####################################### 3 ######################################
        #
        # r_mock_verts = ['x', 'y', 'z']
        # r_mock_edges = [('p', 'x', 'y')]
        # r_mock = BestDiGraph(r_mock_verts, r_mock_edges, layout={'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}).shift(
        #     [-5, 2, 0])
        # r_mock._add_edge(('y', 'z'), role_name='p', edge_config={'path_arc': 0.0}, edge_type=FlexibleDashedLine)
        #
        # self.add(g1, r_mock)
        #
        # h = Homomorphism(r_mock, g1, [('x', 'z1'), ('y', 'b'), ('z', 'z1')], check_hom=True)
        #
        # ha = HomomorphismAnimation(r_mock, h, run_time=2)
        #
        # self.play(ha)
        # g1.suspend_updating()
        # self.play(Indicate(g1.edges[('b', 'z1')]))
        # g1.resume_updating()

        ####################################### 1 ######################################

        # g1_mock = deepcopy(g1)
        #
        # (r4, anims) = g1_mock.apply_rule(r1,
        #                                  ra1,
        #                                  [('x', 'a'), ('y', 'b')],
        #                                  [('y', 'b'), ('z', 'z2')],
        #                                  self,
        #                                  {'z': ('y', (2, -1, 0))},
        #                                  hom_time=1,
        #                                  introduction_time=1.5,
        #                                  change_graph_layout=False,
        #                                  apply=True,  # should the rule be applied
        #                                  # application_successful=True,
        #                                  shorter_animation=True)  # is the rule applicable
        #
        # # dt = ra1.finish()
        # # self.play(Wait(abs(dt), frozen_frame=False))
        # self.play(anims)
        #
        # g1_mock.remove_edges(('a', 'b'), ('b', 'z1'), ('z1', 'b'))
        # g1_mock.remove_vertices('a', 'z1')
        #
        # h = Homomorphism(g1_mock, g1, [('b', 'b'), ('z2', 'z1')], check_hom=True)
        #
        # ha = HomomorphismAnimation(g1_mock, h, run_time=1.25)
        #
        # self.play(ha)
        # g1.suspend_updating()
        # self.play(Indicate(g1.edges[('b', 'z1')]))
        # g1.resume_updating()

        ####################################### 2 ######################################

        g1_mock = deepcopy(g1)

        (r4, anims) = g1_mock.apply_rule(r1,
                                    ra1,
                                    [('x', 'b'), ('y', 'z1')],
                                    [('y', 'z1'), ('z', 'z2')],
                                    self,
                                    {'z': ('y', (2, 0, 0))},
                                    hom_time=.5,
                                    introduction_time=1,
                                    change_graph_layout=False,
                                    apply=True,  # should the rule be applied
                                    # application_successful=True,
                                    shorter_animation=True)  # is the rule applicable
        pop_sound(self, wait_time=5.7)

        # dt = ra1.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))

        self.play(anims)

        g1_mock.remove_edges(('a', 'b'), ('b', 'z1'), ('z1', 'b'))
        g1_mock.remove_vertices('a', 'b')

        h = Homomorphism(g1_mock, g1, [('z1', 'z1'), ('z2', 'b')], check_hom=True)

        ha = HomomorphismAnimation(g1_mock, h, run_time=.5)

        g1.suspend_updating()
        hom_sound(self, duration=.5)
        self.play(ha, Indicate(g1.edges[('z1', 'b')], color=Style.fresh_elem))
        g1.resume_updating()

        ####################################### 3 ######################################

        rc_criteria = Tex(
            r"\textbf{Restricted chase:}", r" Don't apply a rule if its head is already satisfied!",
            font_size=Style.explanation_font_size).move_to((0, -3, 0))
        rc_criteria.set_color_by_tex(r'\textbf{Restricted chase:}', color=Style.restricted_chase_border)
        rc = Group(rc_criteria).add_background_rectangle(color=Style.restricted_chase_border, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1,
                                                         buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)

        g1_mock = deepcopy(g1)

        (r4, anims) = g1_mock.apply_rule(r1,
                                         ra1,
                                         [('x', 'z1'), ('y', 'b')],
                                         [('y', 'b'), ('z', 'z2')],
                                         self,
                                         {'z': ('y', (2, -1, 0))},
                                         hom_time=.5,
                                         introduction_time=1,
                                         shorter_animation=True)  # is the rule applicable


        # dt = ra1.finish()
        # self.play(Wait(abs(dt), frozen_frame=False))
        pop_sound(self, wait_time=4.8)

        self.play(anims)

        g1_mock.remove_edges(('a', 'b'), ('b', 'z1'), ('z1', 'b'))
        g1_mock.remove_vertices('a', 'z1')

        h = Homomorphism(g1_mock, g1, [('b', 'b'), ('z2', 'z1')], check_hom=True)

        ha = HomomorphismAnimation(g1_mock, h, run_time=.5)

        # self.play()
        g1.suspend_updating()
        
        hom_sound(self, duration=.5)
        self.play(ha,
                  Indicate(g1.edges[('b', 'z1')]), color=Style.fresh_elem)

        g1.resume_updating()

        ####################################### 4 ######################################

        r2_body_mock = deepcopy(r2.body_graph)

        h = Homomorphism(r2_body_mock, g1, [('x', 'b'), ('y', 'z1'), ('z', 'b')], check_hom=True)

        ha = HomomorphismAnimation(r2_body_mock, h, run_time=.5)

        g1.suspend_updating()
        self.play(ha)
        self.play(Indicate(g1.edges[('b', 'z1')], color=Style.fresh_elem))
        g1.resume_updating()

        ####################################### 5 ######################################

        r2_body_mock = deepcopy(r2.body_graph)

        h = Homomorphism(r2_body_mock, g1, [('x', 'z1'), ('y', 'b'), ('z', 'z1')], check_hom=True)

        ha = HomomorphismAnimation(r2_body_mock, h, run_time=.5)

        seal = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(PI / 7).shift(3 * LEFT + 1.5 * DOWN)

        g1.suspend_updating()
        self.play(ha)
        seal_sound(self, wait_time=SEAL_PROP)
        self.play(Indicate(g1.edges[('z1', 'b')]), FadeIn(seal, scale=2))
        g1.resume_updating()

        ###

        # print(self.renderer.time)

        target_time = 95.00
        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        self.play(FadeIn(rc, shift=UP))

        ################################################################################
        ################################## Fifth Part ##################################
        ################################################################################
        config_rule = {"opacity": False,
                       "position": True,
                       "scale": False}

        ownerparent = VGroup(MathTex(r'\cdot'))
        owner = Emoji(r'\cdot', ("🧙", "owner.png", None), ownerparent, update_config=config_rule, scale_factor=12)
        owner.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        apprenticeparent = VGroup(MathTex(r'\cdot'))
        apprentice = Emoji(r'\cdot', ("🧑‍🎓", "apprentice.png", None), apprenticeparent, update_config=config_rule,
                           scale_factor=12)
        apprentice.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        mrwparent = VGroup(MathTex(r'\cdot'))
        mrw = Emoji(r'\cdot', ("🧑‍💼", "misterrealworld.png", None), mrwparent, update_config=config_rule,
                    scale_factor=12)
        mrw.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        apprenticeparent.shift(9 * LEFT)
        apprentice.shift(9 * LEFT)

        ownerparent.shift(10 * LEFT)
        owner.shift(10 * LEFT)

        mrwparent.shift(8 * LEFT)
        mrw.shift(8 * LEFT)

        target_time = 134.00
        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        g2 = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], layout={'a': [0, 0, 0], 'b': [2, 0, 0]}).shift([0, 0, 0])
        g2._add_vertex(vertex='z1', position=(4, 0, 0), label=False)
        g2._add_edge(('z1', 'b'), role_name='p', edge_config={"path_arc": 2.0})
        g2._add_edge(('b', 'z1'), role_name='p')

        for i in range(2, 10):
            new_vertex = f'z{i}'
            g2._add_vertex(vertex=new_vertex, position=(2 + (i * 2), 0, 0), label=False)
            g2._add_edge((f'z{i - 1}', f'z{i}'), role_name='p')
            g2._add_edge((f'z{i}', f'z{i - 1}'), role_name='p', edge_config={"path_arc": 2.0})
        g2.shift((-2, 0, 0))

        seal2 = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(PI / 7).shift(3 * LEFT + 0 * DOWN)
        self.play(FadeIn(g2, seal2))
        self.wait(2)

        target_time = 147.00
        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        h = Homomorphism(g2, g1, [('a', 'a'), ('b', 'b'), ('z1', 'z1'), ('z2', 'b'), ('z3', 'z1'), ('z4', 'b'), ('z5', 'z1'),
                                  ('z6', 'b'), ('z7', 'z1'), ('z8', 'b'), ('z9', 'z1')], check_hom=True)

        ha = HomomorphismAnimation(g2, h, run_time=2)
        hom_sound(self, wait_time=.1, duration=1.9)
        self.play(ha, FadeOut(seal2))

        ownerparent.shift((4, 0, 0))
        apprenticeparent.shift((4, 0, 0))
        mrwparent.shift((6, 0, 0))
        self.play(owner.animate.shift((4, 0, 0)), apprentice.animate.shift((4, 0, 0)), mrw.animate.shift((6, 0, 0)))

        target_time = 151.00
        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))

        mrwparent.shift(.5 * UP)
        self.play(mrw.animate.shift(.5 * UP), run_time=.25)
        mrwparent.shift(.5 * DOWN)
        self.play(mrw.animate.shift(.5 * DOWN), run_time=.25)

        self.wait(2)

        mrwparent.shift(12 * RIGHT)
        self.play(mrw.animate.shift(12 * RIGHT), seal.animate.shift(12 * RIGHT), g1.animate.shift(12 * RIGHT), run_time=2)


        target_time = 150.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))
        ra1.finish()
        ra2.finish()
        self.wait(2)
        head.remove_updater(r1.align_head)
        head2.remove_updater(r2.align_head)
        self.play(*[FadeOut(mob) for mob in self.mobjects], FadeOut(head), FadeOut(head2))
        self.clear()


    def construct(self):
        # self.add_sound("../recordings/Final/Scene4-final.flac")

        # self.next_section('a', skip_animations=True)
        self.play_first_part()

        target_time = 30.00
        current_time = self.renderer.time
        wait_duration = max(0.1, target_time - current_time)
        self.wait(abs(wait_duration))
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # self.next_section('a', skip_animations=False)
        self.play_second_part()
        # self.next_section('a', skip_animations=True)

        # back to the problematic rules, apply smartly
        target_time = 80.00
        current_time = self.renderer.time  # not always accurate, see note below
        wait_duration = max(0.1, target_time - current_time)

        self.wait(abs(wait_duration))
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.clear()

        # self.next_section('a', skip_animations=False)
        self.play_third_part()
