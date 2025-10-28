from manim import *
from bestDiGraph import *
import numpy as np
from scene_3 import apply_r1_multiple_times
from sound_effects import *
import Style

# To navigate to the 4 parts of the animation, search for 
# Chase Panel 
# Fairness Panel 
# Termination Panel 
# Core Panel
    
style_factor = 9/8 #scale everything that depends on a size from style.py by this factor
class Scene6(MovingCameraScene):

    def __init__(self, **args):
        super().__init__(**args)
        self.rect_width = 16
        self.rect_height = 9


    def construct(self):
        self.add_sound("../recordings/Final/Scene6-final.flac")

        panels = [
            self.init_chase(),
            self.init_fairness(),
            self.init_termination(),
            self.init_core(),
        ]

        # Place panels in grid
        grid = Group(*panels).arrange_in_grid(buff=0)
        self.add(grid)

        # Four panels
        c = panels[0] # chase
        f = panels[1] # fairness
        t = panels[2] # termination
        o = panels[3] # core
        c.set_stroke(width=0)
        f.set_stroke(width=0)
        t.set_stroke(width=0)
        o.set_stroke(width=0)


        # Camera
        self.camera.auto_zoom(c, animate=False)
        c_center = c.get_center() # (-8,  4.5, 0)
        f_center = f.get_center() # ( 8,  4.5, 0)
        t_center = t.get_center() # (-8, -4.5, 0)
        o_center = o.get_center() # ( 8, -4.5, 0)




        # Chase Panel
        ###
        c_title = Style.create_heading('The Chase').next_to(c.get_top(), DOWN, buff=0.5).scale(style_factor)

        self.play(Write(c_title))

        chasealgo = Tex(r"The chase algorithm applies ",r"\textbf{existential rules }","to data.", font_size = Style.explanation_font_size)
        chasealgo.set_color_by_tex(r'\textbf{existential rules }', Style.app_ex_data)

        
        box_blue = SurroundingRectangle(chasealgo, color=Style.app_ex_data, buff=Style.bg_rect_buff, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius) 

        VGroup(chasealgo, box_blue).scale(style_factor).move_to(c_center + (0,2.2,0))

        self.next_section("A", skip_animations=False)
        graph = BestDiGraph(["k", "p", "b", "c"],[], vertex_color =  "#000000" )
        graph['k'].move_to(c_center + (0,0,0))
        graph['p'].move_to(c_center + (-2,0,0))
        graph['b'].move_to(c_center + (2,1,0))
        graph['c'].move_to(c_center + (2,-1,0))
        graph.move_to(c_center + (0,-0.5,0))
        graph.scale(1.5)

        self.add(graph)
        config = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        kiki_ill = Emoji("k", ("😾", "sad_cat.png", "#400040"),graph["k"], update_config=config)
        potion = Emoji("p", ("🧪", "potion.png", None) ,graph["p"], update_config=config)
        basil = Emoji("b", ("🪴", "basil.png", None) ,graph["b"],update_config=config)
        catnip = Emoji("c", ("🌿", "catnip.png", None) ,graph["c"], update_config=config)

        emojis = Group(kiki_ill,  potion, basil, catnip)

        emojis.suspend_updating()

        
        graph.add_concept_labels(("k", r"\mathsf{Cat}",DL )),
        graph.add_concept_labels(("p", r"\mathsf{HappyPotion}",DL))
        
        graph.add_edges((r"\mathsf{affects}",("p","k")))
        graph.add_concept_labels(("p", r"\mathsf{PlantBased}", UL))
        graph.add_edges((r"\mathsf{allergicTo}", ("k", "c")),
                                          (r"\mathsf{allergicTo}",("k","b" )))
        
        self.play(LaggedStart(WriteGraph(graph),
                    AnimationGroup( FadeIn(kiki_ill), 
                                    FadeIn(potion),
                                    FadeIn(catnip),
                                    FadeIn(basil)), lag_ratio=0.2))
        
        # move graph to the right
        self.play(graph.animate.move_to(c_center + (3,-0.5,0)), run_time=0.5)

        vertices_body = ["x","y"]
        edges_body = [(r"\mathsf{affects}", "x","y")]
        concepts_body = [("x",r"\mathsf{HappyPot}", UL)]
        body_1 = BestDiGraph(vertices_body,
            edges_body,
            concepts=concepts_body,
            labels =  True).move_to(c_center + (-5,-1,0))
        body_1["x"].move_to(c_center + (-6,-0.5,0))
        body_1["y"].move_to(c_center + (-4,1,0))
        body_1.update()

        vertices_head = ["x","y","z"]
        edges_head = [(r"\mathsf{contains}","x","z"),(r"\mathsf{likes}", "y","z")]
        head_1 = BestDiGraph(vertices_head,
            edges_head,
            labels =  True,
            edge_type=FlexibleDashedLine).move_to(c_center + (-3,0,0))
        head_1["z"].move_to(c_center + (-2,-1,0))
        rule_1 = Rule(body_1, head_1)
        rule_1.anchor_points = {"z":"y"}
        rule_1.align_head()
        self.play(WriteGraph(body_1), run_time=0.7)
        self.add(head_1)
        
        
        
        ra = RuleLoopAnimation(rule_1, speed = 0.6)
        
        head_1.add_updater(ra.update_rule)


        self.play(FadeIn(chasealgo), Create(box_blue), run_time=2)

        (r, animations) = graph.apply_rule(rule_1, 
                                     ra, 
                                     [("x","p"),("y","k")],
                                     [("z", "i"),("x","p"),("y","k")],
                                     self,
                                     relative_positions={"z":("y",(0,-3,0))},
                                     hom_time=1.5,
                                     introduction_time=1.5,
                                     transition_to_solid_line=True,
                                     apply = True)
        target_time = 11.189
        hom_sound(self, duration=1)
        pop_sound(self, wait_time=POP_PROPrule2 * (target_time - self.time) + 0.1)

        kiki_ill.set_z_index(20)
        potion.set_z_index(20)
        basil.set_z_index(20)
        catnip.set_z_index(20)

        self.play(animations)
        self.remove(r)


        ###
        self.wait_until(11.189)



        # Fairness Panel
        ###
        self.play(self.camera.auto_zoom(f))

        # Remove chase panel so its not visible during transition from fairness to termination
        head_1.remove_updater(ra.update_rule)   
        self.remove(chasealgo, box_blue, graph, kiki_ill, potion, basil, catnip, body_1, head_1)      

        # Continue with Fairness panel
        f_title = Style.create_heading("Fairness").next_to(f.get_top(), DOWN, buff=0.5).scale(style_factor)

        self.play(Write(f_title))

        line = Tex(r"Fairness requires that every applicable rule is ", r"\textbf{applied eventually.}", font_size=Style.explanation_font_size)
        line.set_color_by_tex(r'\textbf{applied eventually.}', Style.fair_border)

        box_green = SurroundingRectangle(line, color=Style.fair_border, buff=Style.bg_rect_buff, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius) 

        VGroup(line, box_green).scale(style_factor).move_to(f_center + (0,2.2,0))

        logo_fair = ImageMobject("assets/fair_trade.png").scale(0.5).scale(0.35)
        target_fair = f.get_corner(DL) + RIGHT*3 + UP*3.5
        logo_fair.move_to(target_fair + UP*7)

        logo_univ = ImageMobject("assets/seal-of-universality.png").scale(0.5).scale(0.35)
        target_univ = f.get_corner(DR) + LEFT*3 + UP*3.5
        logo_univ.move_to(target_univ + RIGHT*7)


        
        self.play(logo_fair.animate.move_to(target_fair).scale(1.2), run_time=2, rate_func=rate_functions.ease_in_quad)
        self.play(logo_fair.animate.scale(0.9), run_time=0.5, rate_func=rate_functions.ease_out_bounce)
        self.play(Flash(logo_fair.get_center(), color=GREEN_A, line_length=0.2, num_lines=8, flash_radius=0.4), run_time=0.3)


        self.play(FadeIn(line), Create(box_green), run_time=2)

        implication = MathTex(r"\Longrightarrow", font_size=160)
        midpoint = (target_fair + target_univ) / 2
        implication.move_to(midpoint)
        self.wait(1.2)
        self.play(FadeIn(implication), run_time=1.7)

        self.play(logo_univ.animate.move_to(target_univ).scale(1.2), run_time=1.3, rate_func=rate_functions.ease_in_quad)
        self.play(logo_univ.animate.scale(0.9), run_time=0.5, rate_func=rate_functions.ease_out_bounce)
        self.play(Flash(logo_univ.get_center(), color=GREEN_A, line_length=0.2, num_lines=8, flash_radius=0.4), run_time=0.3)
        ###
        self.wait_until(23.560)


        # Termination panel
        ###
        self.play(self.camera.auto_zoom(t))

        t_title = Style.create_heading('Termination')
        t_title.next_to(t.get_top(), DOWN, buff=0.5).scale(style_factor)
        self.play(Write(t_title))

        start_left    = t_center + (-5.5, +1, 0)
        end_right    = t_center + (+5.5, +1, 0)
        start_right    = t_center + (+5.5, -1, 0)
        end_left    = t_center + (-5.5, -1, 0)

        arrow_right = Arrow(start_left, end_right, buff=0, stroke_width=15, tip_length=0.8)
        arrow_left  = Arrow(start_right, end_left, buff=0, stroke_width=15, tip_length=0.8)


        lab_right = Tex(r"\textsc{extended termination}", font_size=50)
        lab_right.move_to(arrow_right.get_center() + UP * 0.5)

        lab_left = Tex(r"\textsc{efficient computation}", font_size=50)
        lab_left.move_to(arrow_left.get_center() + DOWN * 0.5)

        oblivious       = Tex(r"\textsf{\textbf{Oblivious}}", font_size=45, color=Style.chase_variants).scale(style_factor).move_to(start_left + (+0.5, -1, 0))

        restricted      = Tex(r"\textsf{\textbf{Restricted}}", font_size=45, color=Style.chase_variants).scale(style_factor).move_to((start_left+start_right)/2)

        core            = Tex(r"\textsf{\textbf{Core}}", font_size=45, color=Style.chase_variants).scale(style_factor).move_to(start_right + (-0.5, 1, 0))

        
        variants = VGroup(
            oblivious, restricted, core,
            arrow_right, arrow_left,
            lab_right, lab_left,
        )
        variants.scale(0.8).shift(DOWN*0.45)
        
        tria_right = arrow_right.submobjects[0]
        arrow_right.remove(tria_right)

        tria_left = arrow_left.submobjects[0]
        arrow_left.remove(tria_left)


        self.wait(1)
        for label in (oblivious, restricted, core):
            label.scale(1)
            self.play(label.animate.scale(1.0), FadeIn(label), run_time=3)


        self.play(
            AnimationGroup(
                AnimationGroup(
                AnimationGroup(Create(arrow_right, run_time=1.6, rate_func=rate_functions.ease_in_out_sine), Succession(Wait(1.5), FadeIn(tria_right, run_time=0.5)), run_time=2),
                Write(lab_right,  run_time=1.2),
                lag_ratio=0.3,
                ),
                AnimationGroup(
                AnimationGroup(Create(arrow_left, run_time=1.6, rate_func=rate_functions.ease_in_out_sine), Succession(Wait(1.5), FadeIn(tria_left, run_time=0.5)), run_time=2),
                Write(lab_left,  run_time=1.2),
                lag_ratio=0.3,
                ),
                lag_ratio=0,
            )
        )

        self.add(arrow_left, arrow_right, lab_right,lab_left)

        undecidability = Tex(r"Termination of the chase is ", r"\textbf{undecidable.}", font_size = Style.explanation_font_size)
        undecidability.set_color_by_tex(r'\textbf{undecidable.}', Style.undecidable_border)
        
        box_red = SurroundingRectangle(undecidability, color=Style.undecidable_border, buff = Style.bg_rect_buff, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)

        VGroup(undecidability, box_red).scale(style_factor).move_to(t_center + (0,2.2,0))

        lt = {'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}
        ir_vert_body = ['x', 'y']
        ir_edge_body = [('p', 'x', 'y')]
        ir_vert_head = ['y', 'z']
        ir_edge_head = [('p', 'y', 'z')]
        ir_body = BestDiGraph(ir_vert_body, ir_edge_body, edge_type=Line, layout=lt).move_to(t_center+(-5.25, -2.3, 0))

        ir_head = BestDiGraph(ir_vert_head, ir_edge_head, edge_type=FlexibleDashedLine, layout=lt)

        ir = Rule(ir_body, ir_head)
        
        self.play(FadeIn(ir_body))

        
        self.add(ir_head)
        self.add(ir.overlay)
        ira = RuleLoopAnimation(ir, speed=0.6)
        ir_head.add_updater(ira.update_rule)
        
                
        
        db_lt = {'a': [0, 0, 0], 'b': [2, 0, 0]}       
        db = BestDiGraph(['a', 'b'], [('p', 'a', 'b')], edge_type=Line, layout=db_lt).next_to(ir_body, DOWN*1.5)
        
        self.play(FadeIn(db), run_time=.5)
        
        
        
        anims_to_play = apply_r1_multiple_times(db, self, first_body_vertex='a', second_body_vertex='b', new_element_index=2, 
                                                num_applications=15, rule=ir, rule_loop_animation=ira, shorter_animation=True, relative_positions={'z': ('y', (2,0,0))})
        

        total = sum(a.run_time for a in anims_to_play)
        scale = 6 / total
        for a in anims_to_play:
            a.run_time *= scale
        anims_sequence = Succession(*anims_to_play)

        undec_group = Succession(
            Wait(1),
            FadeIn(undecidability),
            Create(box_red)
        )

        o_title = Style.create_heading('The Core Chase').next_to(o.get_top(), DOWN, buff=0.5).scale(style_factor)

        zoom_anim = Succession(Wait(4),self.camera.auto_zoom(o, animate=True),Write(o_title))  

        rt_single_animation = anims_to_play[0].run_time
        total = 15
        n_quieter = 10
        n_louder = 10
        for i in range(n_quieter):
            pop_sound(self, wait_time= (i+POP_PROP-0.2) / total * 6, volume=POP_GAIN-3*i)

        for i in range(n_louder):
            pop_sound(self, wait_time= (i+ n_quieter + POP_PROP-0.2) / total * 6, volume=POP_GAIN-15-3*i)
        

        self.play(
            anims_sequence, 
            undec_group,              
            zoom_anim,              
        )

        ###
        self.wait_until(42.263)



        # Core panel
        ###
        # self.play(self.camera.auto_zoom(o)) # is now part of the infinite chase from the previous panel

        # Remove the rule in termination panel so the zoomed out screen looks less crowded
        ir_head.remove_updater(ira.update_rule)
        self.remove(ir_body,ir_head,ir.overlay)
        # Add stuff from the chase panel again so its visible in the zoomed out screen
        self.add(chasealgo, box_blue, graph, kiki_ill, potion, basil, catnip, body_1, head_1)
        head_1.add_updater(ra.update_rule) 

        # Continue with the actual Core panel

        # o_title = Style.create_heading('The Core Chase').next_to(o.get_top(), DOWN, buff=0.5).scale(style_factor)
        # self.play(Write(o_title)) # is now part of the infinite chase from the previous panel

        hardcore = Tex(r"The ", r"\textbf{core chase terminates }","iff there exists a ",r"\textbf{finite universal model.}", font_size = Style.explanation_font_size)
        hardcore.set_color_by_tex(r'\textbf{core chase terminates }', Style.core_conclusion)
        hardcore.set_color_by_tex(r'\textbf{finite universal model.}', Style.core_conclusion)

        box_yellow = SurroundingRectangle(hardcore, color=Style.core_conclusion, buff=Style.bg_rect_buff, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)

        VGroup(hardcore, box_yellow).scale(style_factor).move_to(o_center + (0,2.2,0))

        self.play(FadeIn(hardcore), Create(box_yellow), run_time=2)

        ###
        self.wait_until(49.875)



        # Zoom out to show all panels
        ###
        # Cross
        top_cross  = c.get_corner(UR)
        bot_cross  = t.get_corner(DR)
        left_cross = c.get_corner(DL)
        right_cross= f.get_corner(DR)

        vline = Line(bot_cross, top_cross).set_stroke(width=1)
        hline = Line(left_cross, right_cross).set_stroke(width=1)

        self.add(vline, hline)

        self.play(self.camera.auto_zoom(grid, margin=0))

        ###
        self.wait_until(55.814)


    def init_chase(self):
        rect = Rectangle(width=self.rect_width, height=self.rect_height)
        return rect
    def init_fairness(self):
        rect = Rectangle(width=self.rect_width, height=self.rect_height)
        return rect
    def init_termination(self):
        rect = Rectangle(width=self.rect_width, height=self.rect_height)
        return rect
    def init_core(self):
        rect = Rectangle(width=self.rect_width, height=self.rect_height)
        return rect

    def wait_until(self, target_time):
        now = self.renderer.time
        dt = target_time - now
        print(f"{now:.2f}, {target_time:.2f}, {dt:.2f}")
        if dt > 0:
            self.wait(dt)

