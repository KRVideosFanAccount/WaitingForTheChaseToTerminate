from bestDiGraph import BestDiGraph
from database import *
from Rules import *
from scene_3 import apply_r1_multiple_times
from sound_effects import *

import Style


def doorbell_animation(scene:Scene, run_time=3):
    
        bellparent = VGroup(MathTex(r'\cdot')).move_to(3*UP+8*RIGHT)
        config_rule = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        bell = Emoji(r'\cdot', ("🔔", "bell.png", None) , bellparent, update_config=config_rule, scale_factor = 10)
        bell.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        scene.add(bell)
        bellparent.shift(2*LEFT)
        scene.play(bell.animate.shift(2*LEFT), run_time=.5)
        
        bell_sound(scene)
        
        scene.play(Succession(Rotate(bell, -PI/7, 
                                    rate_func=rate_functions.ease_out_quad), 
                              Rotate(bell, 2*PI/7, 
                                    rate_func=rate_functions.ease_in_out_quad), 
                              Rotate(bell, -2*PI/7, 
                                    rate_func=rate_functions.ease_in_out_quad), 
                              Rotate(bell, 2*PI/7, 
                                    rate_func=rate_functions.ease_in_out_quad), 
                              Rotate(bell, -2*PI/7, 
                                    rate_func=rate_functions.ease_in_out_quad), 
                              Rotate(bell, 2*PI/7, 
                                    rate_func=rate_functions.ease_in_out_quad), 
                              Rotate(bell, -PI/7, 
                                    rate_func=rate_functions.ease_in_quad)),
                  run_time=2)
        
        bellparent.shift(2*RIGHT)
        scene.play(bell.animate.shift(2*RIGHT), run_time=.5)
        
        scene.remove(bell, bellparent)
        
        return()


class Scene5(Scene):
    
    def construct(self):
        
        self.add_sound("../recordings/Final/Scene5-final.flac")
                
        myTemplate = TexTemplate()

        remark = Tex(r"A ", r"\textbf{finite}",r" universal model doesn't always exist.", font_size=Style.explanation_font_size_small).move_to((-3.3, 3, 0)) 
        remark.set_color_by_tex(r'\textbf{finite}', Style.finite_border)
        remark.add_background_rectangle(color=Style.finite_border, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1, buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)
        
        ir_syntax = MathTex(r'p(x, y) \rightarrow \exists z ~ p(y, z)').next_to(remark, DOWN).shift(.5*DOWN+.3*RIGHT)
        
        self.wait(2)
        
        
        self.play(FadeIn(remark, shift=DOWN))
        
        self.wait(5)
        
        
        
        lt = {'x': [0, 0, 0], 'y': [1.5, 0, 0], 'z': [3, 0, 0]}
        ir_vert_body = ['x', 'y']
        ir_edge_body = [('p', 'x', 'y')]
        ir_vert_head = ['y', 'z']
        ir_edge_head = [('p', 'y', 'z')]
        # ir_body = BestDiGraph(ir_vert_body, ir_edge_body, edge_type=Line, layout=lt).next_to(ir_syntax, RIGHT).shift(1.5*RIGHT)
        ir_body = BestDiGraph(ir_vert_body, ir_edge_body, edge_type=Line, layout=lt).next_to(ir_syntax, RIGHT).shift(1*LEFT)

        ir_head = BestDiGraph(ir_vert_head, ir_edge_head, edge_type=FlexibleDashedLine, layout=lt)

        ir = Rule(ir_body, ir_head)
        
        # self.play(FadeIn(ir_syntax, shift=DOWN), FadeIn(ir_body, shift=RIGHT))
        self.play(FadeIn(ir_body, shift=DOWN+RIGHT))

        
        self.add(ir_head)
        self.add(ir.overlay)
        ira = RuleLoopAnimation(ir, speed=.4)
        ir_head.add_updater(ira.update_rule)
        
        self.wait(2.5, frozen_frame=False)
        
        # self.play(FadeOut(ir_syntax, shift=LEFT), ir.body_graph.animate.shift(2*LEFT))
        
        
        db_lt = {'a': [0, 0, 0], 'b': [2, 0, 0]}       
        db = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).next_to(ir_syntax, DOWN).shift(DOWN)
        
        self.play(FadeIn(db, shift=8*RIGHT), run_time=.5)
        
        
        for i in range(5):
            pop_sound(self, wait_time=(i+POP_PROP)*4/5, volume=POP_GAIN-4*i)
        
        anims_to_play = apply_r1_multiple_times(db, self, first_body_vertex='a', second_body_vertex='b', new_element_index=2, 
                                                  num_applications=5, rule=ir, rule_loop_animation=ira, shorter_animation=True)
        
        self.play(Succession(*anims_to_play), run_time=4)
        
        seal = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(PI/7).next_to(db, LEFT).shift(-LEFT+.4*UP)
        
        self.play(ApplyWave(db), run_time=1)

        remove_rule_loop_animation(ir)
        
        self.play(db.animate.shift(13*RIGHT), FadeOut(ir.body_graph), run_time=1)
        
        
        
        self.remove(db)
        
        
        
        problem = MathTex(r"{{ \rightarrow ~ \textbf{If it does, } }}{{ \text{how to find one?} }}", font_size=Style.explanation_font_size_small).next_to(remark, RIGHT)
        how_to = problem.submobjects[1]
        no_solution = MathTex(r"{{\text{find it with the } }}{{ \text{restricted chase?} }}", font_size=Style.explanation_font_size_small).align_to(problem, UP).align_to(how_to, LEFT)
        solution = MathTex(r"{{\text{find it with the } }}{{ \text{\textbf{core} chase!} }}", font_size= Style.explanation_font_size_small).align_to(problem, UP).align_to(how_to, LEFT)
        core_chase = solution.submobjects[1]
        
        self.play(Write(problem, shift=LEFT), run_time=2)
        
        self.wait(1, frozen_frame=False)
        
        self.play(FadeOut(how_to, shift=DOWN), FadeIn(no_solution, shift=DOWN), run_time=2)
        
        self.wait(3, frozen_frame=False)
        
        self.play(Unwrite(no_solution.submobjects[1]), run_time=5)
        
        self.wait(1, frozen_frame=False)
        
        self.play(Write(core_chase), run_time=3)

        self.play(ApplyWave(core_chase), run_time=1)
        
        ir_syntax = MathTex(r'p(x, y) \rightarrow \exists z ~ p(y, z)').next_to(remark, DOWN).shift(.8*DOWN)
        cr_syntax = MathTex(r'p(x, y) \land p(y, z) \rightarrow p(y, x)').next_to(ir_syntax, DOWN).shift(.3*DOWN)

        lt = {'x': [0, 0, 0], 'y': [1.5, 0, 0], 'z': [3, 0, 0]}
        ir_vert_body = ['x', 'y']
        ir_edge_body = [('p', 'x', 'y')]
        ir_vert_head = ['y', 'z']
        ir_edge_head = [('p', 'y', 'z')]
        ir_body = BestDiGraph(ir_vert_body, ir_edge_body, edge_type=Line, layout=lt).next_to(ir_syntax, RIGHT).shift(1.5*RIGHT)
        ir_head = BestDiGraph(ir_vert_head, ir_edge_head, edge_type=FlexibleDashedLine, layout=lt)

        ir = Rule(ir_body, ir_head)
        
        
        lt = {'x': [0, 0, 0], 'y': [1.5, 0, 0], 'z': [3, 0, 0]}
        cr_vert_body = ['x', 'y', 'z']
        cr_edge_body = [('p', 'x', 'y'), ('p', 'y', 'z')]
        cr_vert_head = ['x', 'y', 'z']
        cr_edge_head = []
        cr_body = BestDiGraph(cr_vert_body, cr_edge_body, edge_type=Line, layout=lt).next_to(cr_syntax, RIGHT).align_to(ir_body, LEFT)
        cr_head = BestDiGraph(cr_vert_head, cr_edge_head, edge_type=Line, layout=lt)
        cr_head._add_edge(('y', 'x'), role_name='p', edge_config={"path_arc": 2.0}, edge_type=FlexibleDashedLine)

        cr = Rule(cr_body, cr_head)
        
        
        ira = RuleLoopAnimation(ir, speed=.4)
        ir_head.add_updater(ira.update_rule)
        cra = RuleLoopAnimation(cr, speed=.4)
        cr_head.add_updater(cra.update_rule)
                
        slide = ir.body_graph.get_center() - cr.body_graph.get_center()
        
        ir.body_graph.shift(6*LEFT)
        cr.body_graph.shift(slide)

        
        # self.play(FadeIn(ir_syntax, shift=RIGHT), 
        #           FadeIn(ir_body, shift=RIGHT),
        #           FadeIn(cr_syntax, shift=RIGHT), 
        #           FadeIn(cr_body, shift=RIGHT)
        #           )
        
        self.play(FadeIn(ir_body, shift=RIGHT),
                  FadeIn(cr_body, shift=RIGHT)
                  )
        

        self.add(ir_head, cr_head)
        self.add(ir.overlay, cr.overlay)
        
        

        self.wait(3, frozen_frame=False)
        
        # self.play(FadeOut(ir_syntax), FadeOut(cr_syntax))
        
        
        # self.play(ir.body_graph.animate.shift(6*LEFT), cr.body_graph.animate.shift(slide))
        
        db_lt = {'a': [0, 0, 0], 'b': [2, 0, 0]}       
        db = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).next_to(cr_syntax, DOWN).shift(.5*DOWN+1*RIGHT)
        
        self.play(FadeIn(db, shift=8*RIGHT), run_time=.5)
        
        attempt1 = MathTex(r"{{ \text{Attempt~1}}", font_size=Style.explanation_font_size).next_to(db, LEFT).shift(.2*UP)
        attempt2 = MathTex(r"{{ \text{Attempt~2}}", font_size=Style.explanation_font_size).next_to(db, LEFT).shift(2*DOWN)
        
        
        
        db2 = deepcopy(db)
        
        self.add(db2)
        
        self.play(db2.animate.shift(2*DOWN + RIGHT), db.animate.shift(RIGHT+.2*UP), FadeIn(attempt1), FadeIn(attempt2), run_time=.5)
        
        RTIME=.8
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','a'),('y','b')],
            head_hom=[('y','b'),('z','c')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','a'),('y','b')],
            head_hom=[('y','b'),('z','c')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
            
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN)

        self.play(anims, anims2, run_time=RTIME)
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','b'),('y','c')],
            head_hom=[('y','c'),('z','d')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','a'),('y','b'),('z','c')],
            head_hom=[('y','b'),('x','a')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-3)

        self.play(anims, anims2, run_time=RTIME)
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','c'),('y','d')],
            head_hom=[('y','d'),('z','e')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','b'),('y','c')],
            head_hom=[('y','c'),('z','d')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-6)

        self.play(anims, anims2, run_time=RTIME)
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','b'),('y','c'),('z','d')],
            head_hom=[('y','c'),('x','b')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','c'),('y','d')],
            head_hom=[('y','d'),('z','e')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-9)

        self.play(anims, anims2, run_time=RTIME)
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','a'),('y','b'),('z','c')],
            head_hom=[('y','b'),('x','a')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','d'),('y','e')],
            head_hom=[('y','e'),('z','f')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-12)

        self.play(anims, anims2, run_time=RTIME)
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','d'),('y','e')],
            head_hom=[('y','e'),('z','f')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','d'),('y','e'),('z', 'f')],
            head_hom=[('y','e'),('x','d')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-15)

        self.play(anims, anims2, run_time=RTIME)
        
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','c'),('y','d'),('z', 'e')],
            head_hom=[('y','d'),('x','c')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','b'),('y','c'),('z', 'd')],
            head_hom=[('y','c'),('x','b')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-18)

        self.play(anims, anims2, run_time=RTIME)
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','d'),('y','e'),('z', 'f')],
            head_hom=[('y','e'),('x','d')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','c'),('y','d'),('z', 'e')],
            head_hom=[('y','d'),('x','c')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-21)

        self.play(anims, anims2, run_time=RTIME)
        
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','e'),('y','f')],
            head_hom=[('y','f'),('z','g')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','e'),('y','f')],
            head_hom=[('y','f'),('z','g')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
            
        # self.play(anims, anims2, run_time=2)
        
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','e'),('y','f'),('z', 'g')],
            head_hom=[('y','f'),('x','e')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        (_, anims2) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','e'),('y','f'),('z', 'g')],
            head_hom=[('y','f'),('x','e')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        # anims2 = Succession(*anims2, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=RTIME*POP_PROP, volume=POP_GAIN-24)

        self.play(anims, anims2, run_time=RTIME)

        

        self.play(Wiggle(db), Wiggle(db2), run_time=.5)
        # self.play(db.animate.shift(10*RIGHT), db2.animate.shift(10*RIGHT))
        # self.remove(db, db2)
        
        db1 = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).next_to(cr_syntax, DOWN).shift(.5*DOWN+.5*RIGHT)
        db1.shift(1.5*LEFT)
        self.play(FadeOut(attempt1), FadeOut(attempt2), FadeOut(db), FadeOut(db2), FadeIn(db1, shift=8*RIGHT), run_time=.5)     
        # self.play(FadeIn(db, shift=8*RIGHT))
        
        db = db1
        
        
        univ_lt = {'a': [0, 0, 0], 'b': [2, 0, 0]}      
        univ = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).next_to(db, RIGHT).shift(3*RIGHT)
        univ._add_edge(('b', 'a'), role_name='p', edge_config={"path_arc": 2.0}, edge_type=Line)
        
        seal = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(-PI/7).next_to(univ, RIGHT).shift(LEFT+.4*UP)
        
        self.wait(1.5, frozen_frame=False)
        

        self.play(Create(univ))
        
        seal_sound(self, wait_time=.3)

        
        self.play(FadeIn(seal, scale=2))
        
        self.wait(2, frozen_frame=False)
        
        self.play(
            LaggedStart(
                    univ.animate.shift(5*DOWN), 
                    seal.animate.shift(5*DOWN), 
                AnimationGroup(
                    ir.body_graph.animate.shift(7*LEFT), 
                    cr.body_graph.animate.shift(9*RIGHT), 
                    db.animate.shift(7*LEFT)
                    ),
                    lag_ratio=.5)
            )
        
        self.remove(univ, seal)
        
        db.shift(1.5*RIGHT)
        
        
        #cc_criteria = MathTex(r"{{ \text{Core chase: } }}{{ \text{After each rule application, } }}{{ \text{apply } }}{{ \text{all } }}{{ \text{non-bijective endomorphisms} }}", font_size=30).move_to((0, -3, 0))
        
        #We need a tex template, since this label is 'very' large
        cc_tex_template = TexTemplate()
        cc_tex_template.add_to_preamble(r'\usepackage[a3paper]{geometry}')
        cc_criteria = Tex(r"\textbf{Core chase:} ", r"After each rule application, ", r"apply ", r"all ", r"non-bijective endomorphisms.", font_size=Style.explanation_font_size_small, tex_template=cc_tex_template).move_to((0,-3,0))
        cc_criteria.set_color_by_tex(r'\textbf{Core chase:}', Style.core_border)
        cc = Group(cc_criteria).add_background_rectangle(color=Style.core_border, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1, buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius).align_to(remark, LEFT)
        
        
        after_each = cc_criteria.submobjects[1]
        apply = cc_criteria.submobjects[2]
        all_text = cc_criteria.submobjects[3]
        non_bij = cc_criteria.submobjects[4]
        
        self.wait()
        
        self.play(FadeIn(cc, shift=UP))
        
        
        
        
        
        
        
        
        
        
        
        
        
        # CORE CHASE
        # Definition of a core


        lt = {'a': [0, 0, 0], 'b': [1.5, 0, 0], 'c': [3, 0, 0], 'd': [4.5, 0, 0], 'e': [5.5, 1, 0], 'f': [5.5,-1, 0]}
        core_db = BestDiGraph(['a', 'b', 'c', 'd', 'e', 'f'], [], layout=lt).move_to([0, 0, 0])
        core_db._add_edge(('a', 'b'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('b', 'a'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('b', 'c'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('c', 'd'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('d', 'c'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('d', 'e'), edge_config={"path_arc": 2.0}, edge_type=Line)
        core_db._add_edge(('d', 'f'), edge_config={"path_arc": 2.0}, edge_type=Line)
        
        self.wait(3)
        
        self.play(ApplyWave(after_each))
        
        self.wait()
        
        self.play(Create(core_db))
        
        
        self.wait()
        
        copy_db = deepcopy(core_db)
        self.add(copy_db)
        self.play(core_db.animate.shift(1*UP+1.2*LEFT), copy_db.animate.shift(1.3*DOWN + 1.2*RIGHT))
        
        self.wait()
        
        h = Homomorphism(copy_db, core_db, [('a','a'),('b','b'), ('c','c'), ('d','d'), ('e','e'), ('f','e')], check_hom=False)
        
        hom_sound(self, duration=3)
        self.play(HomomorphismAnimation(copy_db, h), run_time=3.0)
        
        self.remove(copy_db)
        
        self.play(
            Indicate(core_db.vertices['a'], color=Style.bij_yes),
            Indicate(core_db.vertices['b'], color=Style.bij_yes),
            Indicate(core_db.vertices['c'], color=Style.bij_yes),
            Indicate(core_db.vertices['d'], color=Style.bij_yes),
            Indicate(core_db.vertices['e'], color=Style.bij_yes),
            Indicate(core_db.vertices['f'], color=Style.bij_no),
            Wiggle(core_db.vertices['f']),
            ApplyWave(non_bij),
            run_time=2
            )
        
        self.wait()
        
        
        copy_db = deepcopy(core_db)
        self.add(copy_db)
        h = Homomorphism(copy_db, core_db, [('a','a'),('b','b'), ('c','c'), ('d','d'), ('e','e'), ('f','e')], check_hom=False)
        core_db._remove_edge(('d', 'f'))
        core_db._remove_vertex('f')
        
        hom_sound(self, duration=1)
        self.play(HomomorphismAnimation(copy_db, h), ApplyWave(apply), run_time=1.0)
        
        self.wait(.5)
        
        
        copy_db = deepcopy(core_db)
        self.add(copy_db)
        self.play(copy_db.animate.shift(1.3*DOWN + 2.4*RIGHT), run_time=.5)
        
        h = Homomorphism(copy_db, core_db, [('a','c'),('b','d'), ('c','c'), ('d','d'), ('e','c')], check_hom=False)
        nice_placement = h.create_organized_graph().scale(1.5)
        self.play(ChangeGraphLayout(copy_db, nice_placement), run_time=1)
        
        self.wait()
        
        hom_sound(self, duration=.5)
        self.play(HomomorphismAnimation(copy_db, h), run_time=.5)
        
        self.remove(copy_db) 
        
        self.play(
            Indicate(core_db.vertices['a'], color=Style.bij_no),
            Wiggle(core_db.vertices['a']),
            Indicate(core_db.vertices['b'], color=Style.bij_no),
            Wiggle(core_db.vertices['b']),
            Indicate(core_db.vertices['c'], color=Style.bij_yes),
            Indicate(core_db.vertices['d'], color=Style.bij_yes),
            Indicate(core_db.vertices['e'], color=Style.bij_no),
            Wiggle(core_db.vertices['e']),
            ApplyWave(non_bij),
            run_time=1
            )
        
        self.wait()
        
        
        copy_db = deepcopy(core_db)
        self.add(copy_db)
        h = Homomorphism(copy_db, core_db, [('a','c'),('b','d'), ('c','c'), ('d','d'), ('e','c')], check_hom=False)
        core_db._remove_edge(('a', 'b'))
        core_db._remove_edge(('b', 'a'))
        core_db._remove_edge(('b', 'c'))
        core_db._remove_edge(('d', 'e'))
        core_db._remove_vertex('a')
        core_db._remove_vertex('b')
        core_db._remove_vertex('e')
        
        hom_sound(self, duration=.5)
        self.play(HomomorphismAnimation(copy_db, h), ApplyWave(apply), run_time=.5)
        
        
        self.wait(1.5)
        
        self.play(Wiggle(core_db))
        
        self.wait(1)
        
        
        self.play(FadeOut(core_db))
        
        self.wait(.5)
        
        
        
        
        # CORE CHASE
        # On an example
        
        
        self.play(ir.body_graph.animate.shift(7*RIGHT), cr.body_graph.animate.shift(9*LEFT), db.animate.shift(7*RIGHT))
        
        
        self.wait(1.5, frozen_frame=False)
        
        self.add(db)
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','a'),('y','b')],
            head_hom=[('y','b'),('z','z2')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        pop_sound(self, wait_time=POP_PROP*3-.2)

        # anims = Succession(*anims, suspend_mobject_updating=False)
        
        self.play(anims, run_time=3)
        
        self.wait(2.5, frozen_frame=False)
        
        fail_sound(self)
        self.play(Wiggle(db), run_time=1)
        
        self.wait(2, frozen_frame=False)
        
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','a'),('y','b'),('z','z2')],
            head_hom=[('x','a'),('y','b')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
            
        
        # anims = Succession(*anims, suspend_mobject_updating=False)
        
        
        pop_sound(self, wait_time=POP_PROP*3+.1)

        self.play(anims, run_time=3)
        
        self.wait(1, frozen_frame=False)
        
        copy_db = deepcopy(db)
        self.add(copy_db)
        self.play(db.animate.shift(.2*UP+1.2*LEFT), copy_db.animate.shift(1.2*DOWN + 1.2*RIGHT), run_time=1)
        
        h = Homomorphism(copy_db, db, [('a','a'),('b','b'), ('z2','a')], check_hom=False)
        
        hom_sound(self, duration=2)
        self.play(HomomorphismAnimation(copy_db, h), run_time=2)
        
        self.remove(copy_db)
        
        self.play(
            Indicate(db.vertices['a'], color=Style.bij_yes),
            Indicate(db.vertices['b'], color=Style.bij_yes),
            Indicate(db.vertices['z2'], color=Style.bij_no),
            Wiggle(db.vertices['z2']),
            ApplyWave(non_bij),
            run_time=1
            )
        
        self.wait(4, frozen_frame=False)
        
        
        copy_db = deepcopy(db)
        self.add(copy_db)
        h = Homomorphism(copy_db, db, [('a','a'),('b','b'), ('z2','a')], check_hom=False)
        db._remove_edge(('b', 'z2'))
        db._remove_vertex('z2')
        
        hom_sound(self, duration=1)
        self.play(HomomorphismAnimation(copy_db, h), ApplyWave(apply), run_time=1)
        
        seal = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(-PI/7).next_to(db, RIGHT).shift(LEFT+.4*UP)
                
        self.wait(.5, frozen_frame=False)
        
        seal_sound(self, wait_time=.3)

        self.play(FadeIn(seal, scale=2))
        
        self.wait(1.5, frozen_frame=False)
        
#        remove_rule_loop_animation(ir)
#       remove_rule_loop_animation(cr)

        ira.pause_anim()
        ir.overlay.remove_updater(ir.align_head)
        cra.pause_anim()
        cr.overlay.remove_updater(cr.align_head)
        
        
        
        self.play(FadeOut(ir.body_graph, ir.overlay, cr.body_graph, cr.overlay, db, cc, seal))
        
        
    
        self.wait(.5)
        
        
        # CORE CHASE
        # Main property!
        
        
        cc_lemma = Tex(r"The ", r"\textbf{core chase terminates }", r"iff there exists a ", r"\textbf{finite universal model.}", font_size=Style.explanation_font_size_small)
        cc_lemma.set_color_by_tex(r'\textbf{core chase terminates }', color=Style.core_border)
        cc_lemma.set_color_by_tex(r'\textbf{finite universal model.}', color=Style.core_border)
        cc_lemma.add_background_rectangle(color=Style.core_border, opacity=0, stroke_width=2, stroke_opacity=1, buff=.2)
        #cc_box = SurroundingRectangle(cc_lemma, color=Style.core_border, opacity=0, stroke_width=Style.bg_stroke_width, buff= Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)
        
        self.play(FadeIn(cc_lemma, shift=6*UP), run_time=3)
        
        self.play(ApplyWave(cc_lemma), run_time=3)
        
        self.play(cc_lemma.animate.next_to(remark, DOWN).align_to(remark, LEFT).shift(DOWN), run_time=3)

        #scale = (self.camera.frame_width - 2*(self.camera.frame_width/2 - cc_lemma.get_critical_point(LEFT)))/cc_lemma.get_width()
        scale = -2*cc_lemma.get_critical_point(LEFT)[0]/cc_lemma.get_width() #scale such that left and right margin are the same.
        
        self.play(Succession(cc_lemma.animate.align_to(remark, UP), ApplyMethod(cc_lemma.scale, scale, {'about_point': remark.get_critical_point(UP+LEFT)})), #we use remark.get... instead of cc_lemma since cc_lemma is at the old position right now. remark has the right position right now
                  Succession(Group(remark, no_solution.submobjects[0], core_chase, problem.submobjects[0]).animate.shift(2*UP), Wait(frozen_frame=False)),
                  run_time=2)
        
        self.remove(remark, problem, solution)
        
        self.wait(5)
        
        
        
        # CORE CHASE
        # Difference with the restricted chase
        
        
        self.play(FadeIn(ir_body, shift=RIGHT),
                  FadeIn(cr_body, shift=RIGHT)
                  )
        

        ir_head.add_updater(ir.align_head)
        cr_head.add_updater(cr.align_head)

        ira.reset()
        cra.reset()
        
        self.add(ir_head, cr_head)
        self.add(ir.overlay, cr.overlay)
        
        
        db_lt = {'a': [0, 0, 0], 'b': [2, 0, 0]}       
        db = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).move_to(db.get_center()).shift(.2*DOWN+2.5*RIGHT)
        
        self.play(FadeIn(db))
        
        
        
        caption_restricted = MathTex(r"\text{Restricted chase}", font_size=Style.explanation_font_size).next_to(db, LEFT).shift(.5*LEFT)
        
        db2 = deepcopy(db)
        
        caption_core = MathTex(r"\text{Core chase}", font_size=Style.explanation_font_size).align_to(caption_restricted, DOWN).align_to(caption_restricted, RIGHT).shift(2*DOWN)
        
        self.add(db2)
        self.play(db2.animate.shift(2*DOWN), FadeIn(caption_restricted, shift=4*RIGHT), FadeIn(caption_core, shift=4*RIGHT))
        
        self.wait(5, frozen_frame=False)
        
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','a'),('y','b')],
            head_hom=[('y','b'),('z','c')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        # anims = Succession(anims, suspend_mobject_updating=False)
        
        
        pop_sound(self, wait_time=POP_PROP*3)

        self.play(anims, run_time=3)
        
        local_check=MathTex(r"\text{Local check}", font_size=Style.explanation_font_size).next_to(db, RIGHT).shift(.8*RIGHT)
        self.play(Indicate(db.edges[('b','c')], color=Style.check_highlight),
                  Wiggle(db.edges[('a','b')]), 
                  #Indicate(local_check, color=WHITE),
                  Succession(FadeIn(local_check), Indicate(local_check, color=WHITE), FadeOut(local_check)),
                  run_time=1.5)
        #self.remove(local_check)
        
        (_, anims) = db.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','a'),('y','b'),('z','c')],
            head_hom=[('y','b'),('x','a')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        # anims = Succession(anims, suspend_mobject_updating=False)
        
        
        pop_sound(self, wait_time=POP_PROP*1)

        self.play(anims, run_time=1)
        
        # local_check=MathTex(r"\text{Local check}", font_size=30).next_to(db, RIGHT).shift(.3*RIGHT)
        self.play(Indicate(db.edges[('b','a')], color=Style.check_highlight),
                  Wiggle(db.edges[('a','b')]), 
                  Wiggle(db.edges[('b','c')]), 
                  #Indicate(local_check, color=WHITE),
                  Succession(FadeIn(local_check), Indicate(local_check, color=WHITE), FadeOut(local_check)),
                  run_time=1.5)
        self.remove(local_check)
        
        
        (_, anims) = db.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','b'),('y','c')],
            head_hom=[('y','c'),('z','d')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        # anims = Succession(anims, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=POP_PROP*1)

        self.play(anims, run_time=1)
        self.play(Indicate(db.edges[('c','d')], color=Style.check_highlight),
                  Wiggle(db.edges[('a','b')]), 
                  Wiggle(db.edges[('b','a')]), 
                  Wiggle(db.edges[('b','c')]), 
                  run_time=1.5)
        
        
        self.play(db.animate.shift(12*RIGHT), caption_restricted.animate.shift(14*RIGHT), caption_core.animate.shift(1*UP), db2.animate.shift(1*UP))
        self.remove(db, caption_restricted)
        
        
        
        
        self.wait(.5, frozen_frame=False)
        
        
        (_, anims) = db2.apply_rule(
            rule=ir,
            rule_loop_animation=ira,
            body_hom=[('x','a'),('y','b')],
            head_hom=[('y','b'),('z','c')],
            relative_positions={'z':('y', 2*RIGHT)}, 
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        # anims = Succession(anims, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=POP_PROP*3)

        self.play(anims, run_time=3)
        local_check=MathTex(r"\text{Global check}", font_size=Style.explanation_font_size).next_to(db2, RIGHT).shift(.8*RIGHT)
        self.play(Wiggle(db2),
                  # Indicate(db2.edges[('b','c')], color=Style.check_highlight),
                  # Indicate(db2.edges[('a','b')], color=Style.check_highlight), 
                  #Indicate(local_check, color=WHITE),
                  Succession(FadeIn(local_check), Indicate(local_check, color=WHITE), FadeOut(local_check)),
                  run_time=1.5)
        self.remove(local_check)
        
        (_, anims) = db2.apply_rule(
            rule=cr,
            rule_loop_animation=cra,
            body_hom=[('x','a'),('y','b'),('z','c')],
            head_hom=[('y','b'),('x','a')],
            scene=self,
            # apply=True,
            shorter_animation=True,
            # synchronous_rules =False
            )
        
        anims = Succession(anims, suspend_mobject_updating=False)
        
        pop_sound(self, wait_time=POP_PROP*1)

        self.play(anims, run_time=1)
        # local_check=MathTex(r"\text{Local check}", font_size=Style.explanation_font_size).next_to(db2, RIGHT).shift(.3*RIGHT)
        self.play(Indicate(db2.edges[('b','a')], color=Style.check_highlight),
                  Indicate(db2.edges[('a','b')], color=Style.check_highlight),
                  Indicate(db2.edges[('b','c')], color=Style.check_highlight),
                  #Indicate(local_check, color=WHITE),
                  Succession(FadeIn(local_check), Indicate(local_check, color=WHITE), FadeOut(local_check)),
                  run_time=.5)
        self.remove(local_check)
        
        
        
        expensive=MathTex(r"\text{Expensive step!}", font_size=Style.explanation_font_size).next_to(db2, RIGHT).shift(1.6*RIGHT)
        copy_db = deepcopy(db2)
        self.add(copy_db)
        self.play(db2.animate.shift(.8*UP+.5*RIGHT), copy_db.animate.shift(.8*DOWN + 2*RIGHT), FadeIn(expensive), run_time=.5)
        
        self.wait()
        
        h = Homomorphism(copy_db, db2, [('a','a'),('b','b'), ('c','a')], check_hom=False)
        
        
        hom_sound(self, duration=.5)
        self.play(HomomorphismAnimation(copy_db, h), run_time=.5)
        
        self.remove(copy_db)
        
        self.play(
            Indicate(db2.vertices['a'], color=Style.bij_yes),
            Indicate(db2.vertices['b'], color=Style.bij_yes),
            Indicate(db2.vertices['c'], color=Style.bij_no),
            Wiggle(db2.vertices['c']),
            run_time=.5
            )
        
        self.wait()
        
        
        copy_db = deepcopy(db2)
        self.add(copy_db)
        h = Homomorphism(copy_db, db2, [('a','a'),('b','b'), ('c','a')], check_hom=False)
        db2._remove_edge(('b', 'c'))
        db2._remove_vertex('c')
        
        
        hom_sound(self, duration=.5)
        self.play(HomomorphismAnimation(copy_db, h), FadeOut(expensive), run_time=.5)
        
        seal = ImageMobject("assets/seal-of-universality.png").scale(.1).rotate(-PI/7).next_to(db2, RIGHT).shift(LEFT+.4*UP).shift(-.8*UP-.5*RIGHT)
                
        self.wait(.5, frozen_frame=False)
        
        seal_sound(self, wait_time=.3)

        self.play(db2.animate.shift(-.8*UP-.5*RIGHT), FadeIn(seal, scale=2))
        
        self.wait(1, frozen_frame=False)
        
        
       #remove_rule_loop_animation(ir)
       #remove_rule_loop_animation(cr)
        ira.pause_anim()
        ir.overlay.remove_updater(ir.align_head)
        cra.pause_anim()
        cr.overlay.remove_updater(cr.align_head)
 
        
        self.play(FadeOut(ir.body_graph, ir.overlay, cr.body_graph, cr.overlay, db2, caption_core, seal))
        
        
        
        
        # CONCLUSION ON THE CORE CHASE
        
        cost=Tex(r"But it is computationally ", r"\textbf{expensive!}", font_size=Style.explanation_font_size).move_to([0, -1, 0])
        cost.set_color_by_tex(r'\textbf{expensive!}', Style.expensive)
        cost.add_background_rectangle(color=Style.expensive, buff=Style.bg_rect_buff, opacity=0, stroke_opacity=1, stroke_width=Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)

        
        self.play(FadeIn(cost, shift=3*UP), cc_lemma.animate.move_to([0, 0.2, 0]))
        
        
        self.wait(2)
        
        self.play(FadeOut(cost), FadeOut(cc_lemma))

        
        self.remove(*self.mobjects)
        
