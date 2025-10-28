from coolerDiGraph import *
from bestDiGraph import *
from database import *
from Homomorphism import * 
from Rules import *
from manim import *
from CQ import *
from math import sqrt
from scene_1_audio import timestamps, delta_sounds
from sound_effects import *

import Style

PLACE_FOR_CURRENT_RULE = (0,3,0)
PLACE_FOR_CURRENT_RULE_GRAPH = (-4.3,0.8,0)
PLACE_FOR_GRAPH_ACTIVE = (3,1,0)
PLACE_FOR_GRAPH_INACTIVE = (3.5, -2.3, 0)
PLACE_FOR_RULES_INACTIVE = (-5.5, -2.5, 0)
PLACE_FOR_QUERY_INACTIVE = (-3,-3, 0)
SCALE_ACTIVE_RULE = 1.5

PLACE_FOR_APPLY = (-3, 0.5, 0)

RENDER_TIME_START_SOUND = 9.2
def calculate_wait_time(scene:Scene, stamp:str):
    """
    function to calculate the waiting time wrt. a dictionary that contains the
    timestamps of certain words or phrases in the audio
    
    """
    current_time = scene.renderer.time - RENDER_TIME_START_SOUND
    target_time = timestamps[stamp]
    if (target_time - current_time) < 0:
        raise Exception("You do not have enough time: " + str(current_time) + ", " + str(target_time) )
    print("Waiting for (" + stamp + "): " + str(target_time - current_time) )
    if target_time - current_time == 0:
        return 0.000000000000001
    else:
        return abs(target_time - current_time)



class MyGraphScene(Scene):
    def construct(self):
        self.next_section("0", skip_animations=False)
        config_rule = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        
        vampireparent = VGroup(MathTex(r'\cdot'))
        vampire = Emoji(r'\cdot', ("🧛🏻", "vampire.png", None) , vampireparent, update_config=config_rule, scale_factor = 12)
        vampire.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        ownerparent = VGroup(MathTex(r'\cdot'))
        owner = Emoji(r'\cdot', ("🧙", "owner.png", None) , ownerparent, update_config=config_rule, scale_factor = 12)
        owner.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        apprenticeparent = VGroup(MathTex(r'\cdot'))
        apprentice = Emoji(r'\cdot', ("🧑‍🎓", "apprentice_1.png", None) , apprenticeparent, update_config=config_rule, scale_factor = 12)
        apprentice.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        mrwparent = VGroup(MathTex(r'\cdot'))
        mrw = Emoji(r'\cdot', ("🧑‍💼", "misterrealworld.png", None) , mrwparent, update_config=config_rule, scale_factor = 12)
        mrw.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        
        sleepparent = VGroup(MathTex(r'\cdot'))
        sleep = Emoji(r'\cdot', ("😴", "sleep.png", None) , sleepparent, update_config=config_rule, scale_factor = 12)
        sleep.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
    

        title = MathTex(r"\text{Waiting for the Chase to Terminate:}", font_size=Style.explanation_font_size).move_to((0, 1, 0)) 
        subtitle = MathTex(r"\text{Have You Tried This Other Variant?}", font_size=Style.explanation_font_size).next_to(title, 1.5*DOWN)
        titles = Group(title, subtitle)
        
        # titleshop = Tex(r'\calligra \Large KRaft Elixirs', font_size=40, tex_template=myTemplate).move_to((0, 1, 0)) 
        # subtitleshop = Tex(r'\calligra Computational Alchemy Since 1989', font_size=40, tex_template=myTemplate).next_to(titleshop, 1.5*DOWN)
        titleshop = Tex(r'\text{\Large KRaft Elixirs}', font_size=Style.explanation_font_size).move_to((0, 1, 0)) 
        subtitleshop = Tex(r'\textit{Computational Alchemy Since 1989}', font_size=Style.explanation_font_size).next_to(titleshop, 1.5*DOWN)
        titlesshop = Group(titleshop, subtitleshop)
        
        
        bellparent = VGroup(MathTex(r'\cdot')).move_to(3*UP+8*RIGHT)
        bell = Emoji(r'\cdot', ("🔔", "bell.png", None) , bellparent, update_config=config_rule, scale_factor = 12)
        bell.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        
        
        apprenticeparent.shift(2*DOWN + 1*LEFT)
        apprentice.shift(2*DOWN + 1*LEFT)
        
        sleepparent.shift(2*DOWN + 1*LEFT)
        sleep.shift(2*DOWN + 1*LEFT)
        
        
        
        self.add(titles)
        self.add(sleep)
        
        self.add_sound("assets/snoring.wav")
        
        self.play(Wiggle(sleep))
        self.play(Wiggle(sleep))
        self.play(Wiggle(sleep))
        
        
        self.add(bell)
        bellparent.shift(2*LEFT)
        self.play(bell.animate.shift(2*LEFT), run_time=.5)
        
        # self.add_sound("assets/bell_sounds.flac")
        bell_sound(self)

        
        ownerparent.move_to(2*DOWN+8*RIGHT)
        owner.move_to(2*DOWN+8*RIGHT)
        ownerparent.move_to(2*DOWN+5*RIGHT)
        
        self.play(Wiggle(sleep), 
                  Succession(Rotate(bell, -PI/7, 
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
                  owner.animate.shift(3*LEFT),
                  FadeOut(titles),
                  run_time=2)
        
        bellparent.shift(2*RIGHT)
        self.play(bell.animate.shift(2*RIGHT), Wiggle(sleep), run_time=.5)
        
        self.remove(bell, bellparent)
        
        self.add_sound("../recordings/Final/Scene1-final.flac")

        self.play(FadeOut(sleep), FadeIn(apprentice), run_time=.5)
        
        
        ownerparent.shift(.5*UP)
        self.play(owner.animate.shift(.5*UP), run_time=.25)
        ownerparent.shift(.5*DOWN)
        self.play(owner.animate.shift(.5*DOWN), run_time=.25)
        ownerparent.shift(.5*UP)
        self.play(owner.animate.shift(.5*UP), run_time=.25)
        ownerparent.shift(.5*DOWN)
        self.play(owner.animate.shift(.5*DOWN), run_time=.25)
        
        ownerparent.shift(3*LEFT)
        self.play(owner.animate.shift(3*LEFT), Write(titleshop), Write(subtitleshop), run_time=2.2)
        
        self.play(Wiggle(apprentice))
        self.play(Wiggle(apprentice))
        
        self.wait(4.8)
        
        ownerparent.shift(.5*UP)
        self.play(owner.animate.shift(.5*UP), run_time=.25)
        ownerparent.shift(.5*DOWN)
        self.play(owner.animate.shift(.5*DOWN), run_time=.25)
        
        
        ownerparent.shift(2*LEFT)
        self.play(owner.animate.shift(2*LEFT), run_time=2)
        
        ownerparent.shift(8*LEFT)
        apprenticeparent.shift(8*LEFT)
        self.play(owner.animate.shift(8*LEFT), apprentice.animate.shift(8*LEFT), Unwrite(titleshop), Unwrite(subtitleshop), run_time=3)
        
        self.remove(apprentice, apprenticeparent, owner, ownerparent)
        self.next_section("A", skip_animations=False)

        self.play(Wait(calculate_wait_time(self,"witch"), 
                       frozen_frame=False))
        graph = BestDiGraph(["k", "p", "b", "c"],[], vertex_color =  "#000000" )
        graph['k'].move_to((0,0,0))
        graph['p'].move_to((-2,0,0))
        graph['b'].move_to((2,1,0))
        graph['c'].move_to((2,-1,0))
        graph.move_to((0,0,0))


        self.add(graph)
        self.wait()
        config = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        kiki_ill = Emoji("k", ("😾", "sad_cat.png", "#400040"),graph["k"], update_config=config)
        kiki = Emoji("k", ("😼", "sad_cat.png", "#000000"),graph["k"], update_config=config)
        potion = Emoji("p", ("🧪", "potion.png", None) ,graph["p"], update_config=config, scale_factor=1.8)
        basil = Emoji("b", ("🪴", "basil.png", None) ,graph["b"],update_config=config)
        catnip = Emoji("c", ("🌿", "catnip.png", None) ,graph["c"], update_config=config)

        emojis = Group(kiki_ill,  potion, basil, catnip)

        emojis.suspend_updating()
        
        self.play(Wait(calculate_wait_time(self,"black cat"), 
                       frozen_frame=False))
        self.play(FadeIn(kiki, scale= 2.5,suspend_mobject_updating=True),
                  graph.animate.add_concept_labels(("k", r"\mathsf{Cat}",UL ))
                  )
        
        self.play(Wait(calculate_wait_time(self,"turned violet"), 
                       frozen_frame=False))
        self.play( FadeOut(kiki, scale=1.5), 
                  FadeIn(kiki_ill,scale=1.5)  )
        
        
        self.play(Wait(calculate_wait_time(self,"happiness potion"), 
                       frozen_frame=False))
        
        self.play(FadeIn(potion, scale= 2.5),
                  graph.animate.add_concept_labels(("p", r"\mathsf{HappyPotion}",DL )) ,
                  graph.animate.add_edges((r"\mathsf{affects}",("p","k"))))
        

        self.play(Wait(calculate_wait_time(self,"is plant based"), 
                       frozen_frame=False))
        
        
        self.play(graph.animate.add_concept_labels(("p", r"\mathsf{PlantBased}", UL)))
        self.play(Wait(calculate_wait_time(self,"allergic to"), 
                       frozen_frame=False))
        self.play(graph.animate.add_edges((r"\mathsf{allergicTo}", ("k", "c")),
                                          (r"\mathsf{allergicTo}",("k","b" ))), 
                    FadeIn(catnip, scale=2.5), 
                    FadeIn(basil, scale=2.5))
        self.play(Wait(calculate_wait_time(self,"allergic reaction"), 
                       frozen_frame=False))
        #text_allergic_reaction = Text("Is this an allergic reaction?").move_to(PLACE_FOR_CURRENT_RULE ).scale(0.8)
        text_allergic_reaction = Style.create_heading('Is this an allergic reaction?').move_to(PLACE_FOR_CURRENT_RULE )

        self.play(Write(text_allergic_reaction))
        self.wait()
        self.play(Unwrite(text_allergic_reaction, reverse=False))


        emojis.resume_updating()

        self.play(Wait(calculate_wait_time(self,"those facts"), 
                       frozen_frame=True))
        
        self.play(Wiggle(graph, run_time=1.8))

        emojis.suspend_updating()

        kiki_ill.update_position = False
        potion.update_position = False
        catnip.update_position = False
        basil.update_position = False

        db = EmojiDatabase([(r"\mathsf{affects}", "p","k"),
                            (r"\mathsf{allergicTo}", "k", "c"),
                            (r"\mathsf{allergicTo}", "k", "b")], 
                      [("k", r"\mathsf{Cat}",UL ), 
                            ("p", r"\mathsf{HappyPotion}",DL ),
                            ("p", r"\mathsf{PlantBased}", UL)],
                            emojis = {"k": ("😾", "sad_cat.png", "#400040"), 
                                  "p": ("🧪", "potion.png", None), 
                                  "c": ("🌿", "catnip.png", None), 
                                  "b": ("🪴", "basil.png", None)},
                      line_config = {"stroke_width" : 1}, 
                      buff = 0.2)
        
        '''
        
        Transform from graph to db and back. (This needs some tricks as emojis are not VMobjects)
        
        '''

        # emoji ''transform'' animations
        runtime = 0.6
        fade_emojis = []
        for emoji in emojis:
            fade_emojis.append( FadeOut(emoji, shift= graph.get_center() - emoji.get_center(),run_time = runtime))
            emoji.set_z_index(20)
        graph_copy = graph.copy()
        fade_db_emojis = []
        for db_emoji in db.emojis:
            db_emoji.update()
            db_emoji.clear_updaters()
            fade_db_emojis.append(FadeIn(db_emoji, shift= db_emoji.get_center() - db.get_center(),run_time = runtime))
        

        self.add(graph_copy)
        self.remove(graph)
        graph_copy.suspend_updating()
        graph.suspend_updating()
        self.play(Wait(calculate_wait_time(self,"database"), 
                       frozen_frame=True))
        trans_graph_table_sound(self, delta_sounds["graph to table"])
        self.play(ReplacementTransform(graph_copy, 
                                       VGroup(*db.database.role_table_mobjects, *db.database.concept_table_mobjects), run_time = runtime), 
                                       * fade_db_emojis, 
                                       * fade_emojis, 
                                       )
        
        # emoji ''transform'' animations
        self.play(Wait(1.8 - runtime * 2 ))
        runtime = 0.6
        fade_emojis = []
        for emoji in emojis:
            fade_emojis.append( FadeIn(emoji, shift=  - graph.get_center() + emoji.get_center(), run_time = runtime))
            fade_db_emojis = []
        for db_emoji in db.emojis:
            fade_db_emojis.append(FadeOut(db_emoji, shift= - db_emoji.get_center() + db.get_center(), run_time = runtime))
        
        
        
        table = VGroup(*db.database.role_table_mobjects, *db.database.concept_table_mobjects)
        trans_graph_table_sound(self, delta_sounds["table to graph"])  
        self.play( Transform(table,graph, run_time = runtime), 
                  * fade_db_emojis, 
                  * fade_emojis
                 )
        graph.resume_updating()
        
        '''
        
        We set everything such that the emojis will update according to the graph and the transform objects are discarded
        
        '''
        
        self.remove(table)
        emojis.resume_updating()
        
        for emoji in emojis:
            emoji.update_position = True
            emoji.update_scale = True
        
        '''
        
        Put everything to side to introduce the query

        '''
        config = {"opacity": False, 
                  "position": True, 
                  "scale": True}


        self.play(graph.animate(runtime= 0.7).move_to(PLACE_FOR_GRAPH_INACTIVE))

        self.next_section("A.1", skip_animations=False)
        """
            Heading:
            Query - Introduction + (creation rectangles query and rules)
        
        """

        def createRectangle(text,size_r=3, ratio = 1.41, num_lines = 4, l_ratio = (2/9), buffer = 1/9 ):
            size_r = 3 
            width = size_r * 1
            height = size_r * ratio
            buffer = width * buffer
            l = height * l_ratio * 0.5
            rectangle = RoundedRectangle(height=height , width=width)
            text = MathTex(text).move_to((0,l + height * abs(l_ratio) ,0)).scale_to_fit_width(width - 2*buffer)
            lines = []
            
            for i in range(num_lines):
                lines.append(Line((- (width/2 - buffer), l, 0), ((width/2 - buffer), l, 0) ) )
                l = l - height * (5/9) * (1/num_lines)
            

            return VGroup(rectangle, text, *lines)
        
        
        rules_r = createRectangle(r"\text{Rules} \quad \mathcal{R}").scale(0.8)

        query_r = createRectangle(r"\text{Query} \quad q", ratio=0.7, num_lines=1, l_ratio=-3/9, buffer = 1/9).scale(0.8)
        

        


        query_string = [r"q ", r"= \exists y \; \mathsf{contains} \bigl(", r"\;x\;", r", y\bigr) \land \mathsf{allergicTo}\bigl(", r"\;z\;", r", y\bigr)"]
        
        query = VGroup(MathTex(*query_string)).move_to(PLACE_FOR_CURRENT_RULE)
        query_introduction = deepcopy(query)
        
        kiki_query_introduction = Emoji(r"\;z\;", ("😾", "sad_cat.png", "#400040"),query_introduction, update_config=config)
        potion_query_introduction = Emoji(r"\;x\;", ("🧪", "potion.png", None) ,query_introduction, update_config=config)
        query_emojis_introduction = Group(kiki_query_introduction, potion_query_introduction)

        

        self.play(Wait(calculate_wait_time(self,"query"), 
                       frozen_frame=False))
        self.play(LaggedStart(Write(query_introduction), FadeIn(query_emojis_introduction), lag_ratio=0.75))
        
        kiki_query_introduction.set_z_index(20)
        potion_query_introduction.set_z_index(20)
        #fade_query = [q_part.animate.set_opacity(0.0) for q_part in query.submobjects[0].submobjects[1:]]
        all_but_q = VGroup(query_introduction.submobjects[0].submobjects[1:])
        self.play(Wait(2, 
                       frozen_frame=False))
        
        query_graph_c = CoolDiGraph(["k", "p", "y"], 
                                  [(r"\mathsf{contains}","p","y"), (r"\mathsf{allergicTo}","k","y")]
                                  )
        query_graph_c["k"].move_to((-2,-1,0))
        query_graph_c["p"].move_to((2,-1,0))
        query_graph_c["y"].move_to((0,1,0))

        query_graph_c.move_to((0,0,0))
        query_graph_c.update()


        kiki_ill_query_graph = Emoji("k", ("😾", "sad_cat.png", "#400040"),query_graph_c["k"], update_config={"opacity": False, 
                  "position": True, 
                  "scale": False})

        potion_query_graph = Emoji("p", ("🧪", "potion.png", None) ,query_graph_c["p"], update_config={"opacity": False, 
                  "position": True, 
                  "scale": False}, scale_factor=1.8)

       
        


        kiki_query_introduction.set_z_index(20)
        potion_query_introduction.set_z_index(20)
        kiki_ill_query_graph.set_z_index(20)
        potion_query_graph.set_z_index(20)
        #self.play(Transform(line,query, run_time = 1),
        #                      FadeIn(kiki_query, shift = kiki_query.get_center() - line.get_center(), run_time = 1), 
        #                      FadeIn(potion_query,shift = potion_query.get_center() - line.get_center(), run_time = 1))


        query_copy = query_introduction.copy()
        kiki_query_introduction_c = Emoji(r"\;z\;", ("😾", "sad_cat.png", "#400040"),query_copy, update_config=config)
        potion_query_introduction_c = Emoji(r"\;x\;", ("🧪", "potion.png", None) ,query_copy, update_config=config)
        
        self.play(FadeOut(kiki_query_introduction_c, shift = query_graph_c.get_center() - kiki_query_introduction.get_center(), run_time = 1), 
                FadeOut(potion_query_introduction_c, shift = query_graph_c.get_center() - potion_query_introduction.get_center(), run_time = 1), 
                Transform(query_copy,query_graph_c, run_time = 1), FadeIn(kiki_ill_query_graph, shift = query_graph_c.get_center() - kiki_query_introduction.get_center(), run_time = 1), 
                FadeIn(potion_query_graph,shift = query_graph_c.get_center() - potion_query_introduction.get_center() , run_time = 1))
        
        self.remove(query_copy)
        self.add(query_graph_c)
        self.add(potion_query_graph,kiki_ill_query_graph )


        self.play(query_graph_c.animate(run_time = 2).move_to((-4,0,0)), graph.animate(run_time = 2).move_to((3,0,0)))
        graph.add_vertices("n1", labels=False)
        graph["n1"].set_opacity(0)
        graph["n1"].move_to(graph["k"].get_center() + (0,-2,0))
        hom = Homomorphism(query_graph_c, graph, [("k","k"),("p","p"),("y","n1")])
        hom_animation = ErrHomAnimation(query_graph_c, hom, run_time = 1.5)
        kiki_ill_query_graph.set_z_index(20)
        potion_query_graph.set_z_index(20)

        kiki_ill_query_graph.update_opacity = True
        potion_query_graph.update_opacity = True
        hom_animation.run_time = 3

        config_rule_check = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        #bad_checkmark_parent = VGroup(MathTex(r'\cdot'))
        #bad_checkmark = Emoji(r'\cdot', ("❌", "bad_checkmark.png", None) , bad_checkmark_parent, update_config=config_rule_check, scale_factor = 12)
        #bad_checkmark.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        fail_sound(self, delta_sounds["no Element"]) 
        self.play(LaggedStart(hom_animation, 
                              #Succession(GrowFromPoint(bad_checkmark, bad_checkmark.get_center(), runtime=0.5),FadeOut(bad_checkmark, scale=0.01) ), 
                              lag_ratio=0.3))
        
        graph.remove_vertices("n1")
        self.play(graph.animate(run_time = 1.5).move_to(PLACE_FOR_GRAPH_INACTIVE))


        
        
        kiki_ill_query_graph.update_opacity = False
        potion_query_graph.update_opacity = False
        
        
        self.play(FadeOut(query_emojis_introduction, shift= (-4,0,0)),Transform(all_but_q, query_introduction.submobjects[0].submobjects[0]),
                  FadeOut(kiki_ill_query_graph, shift=(query_introduction.submobjects[0].submobjects[0].get_center()-kiki_ill_query_graph.get_center())), 
                  FadeOut(potion_query_graph,shift=(query_introduction.submobjects[0].submobjects[0].get_center()-potion_query_graph.get_center())), 
                  FadeOut(query_graph_c, shift=(query_introduction.submobjects[0].submobjects[0].get_center()-query_graph_c.get_center())))
        self.remove(all_but_q)
        
        
        
        
        
        
        self.play(Transform(query_introduction.submobjects[0].submobjects[0], query_r))
        self.remove(query_introduction.submobjects[0].submobjects[0])
        self.remove(query_introduction)
        self.remove(all_but_q)
        self.add(query_r)

        self.play(query_r.animate.move_to((PLACE_FOR_RULES_INACTIVE[0], PLACE_FOR_QUERY_INACTIVE[1], 0)).scale(0.6))





        self.play(Wait(calculate_wait_time(self,"onthology"), 
                       frozen_frame=False))
        
        a_config = config = {"opacity": False, 
                  "position": False, 
                  "scale": False}
        
        t_alchemy = VGroup(MathTex(r"\cdot")).move_to((0.5,-0.5,0))
        t_scroll = VGroup(MathTex(r"\cdot"))
        alchemy = Emoji(r"\cdot", ("⚗️", "potion.png", None) ,t_alchemy, update_config=a_config, scale_factor=16)
        scroll = Emoji(r"\cdot", ("📜", "potion.png", None) ,t_scroll, update_config=a_config, scale_factor=28)
        mag_config = config = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        t_mag = VGroup(MathTex(r"\cdot")).move_to((0.5,0.5,0))
        mag = Emoji(r"\cdot", ("🔍", "mag.png", None) ,t_mag, update_config=mag_config, scale_factor=20)
        mag.set_z_index(30)
        t_mag.set_opacity(0.0)
        alchemy.set_z_index(20)
        onthology = Group(scroll, alchemy)
        self.play(FadeIn(onthology, shift = 7* DOWN))
        self.play(FadeIn(mag))
        self.play(t_mag.animate.move_to((-0.5, -0.5,0)), runtime=2)
        self.play(FadeOut(mag), FadeOut(t_mag))



        
        



        self.next_section("A.2", skip_animations=False)
        """
        Introduce the Rules, 
         
        """

        r_scale = 0.5
        rule_1_string = [r"\mathsf{HappyPotion}",r"(",r" x ",r")", r" \land " ,r" \mathsf{affects}",r"(",r" x ",r",",r" y ",r")",
                          r" \; \rightarrow \;",
                          r" \exists z \;",r" \mathsf{contains}(x,z)", r" \land",r" \mathsf{likes}(y,z)"]
        rule_1_tex = VGroup(MathTex(*rule_1_string)).scale(r_scale)
        
        rule_2_string = [r"\mathsf{PlantBased}(x)\land \mathsf{contains}(x,y)", r" \; \rightarrow \;",r"\mathsf{PlantBased}(y)"]
        rule_2_tex = VGroup(MathTex(*rule_2_string)).scale(r_scale)

        
        rule_3_string = [r"\mathsf{Cat}(x)\land \mathsf{likes}(x,y) \land \mathsf{PlantBased}(y)", r" \; \rightarrow \;",r"\mathsf{contains}\bigl(y,", r"\;c\;",r"\bigr)"]
        rule_3_tex = VGroup(MathTex(*rule_3_string)).scale(r_scale)
        

        rule_4_string = [r"\mathsf{contains}(x,y) \land \mathsf{contains}(y,z)", r" \; \rightarrow \;",r"\mathsf{contains}(x,z)"]
        rule_4_tex = VGroup(MathTex(*rule_4_string)).scale(r_scale)
        

        #anim_1 = Indicate(rule_1_tex.submobjects[0].get_part_by_tex(r" \; \rightarrow \;"))
        #rule_1_tex.add_updater(anim_1)
        rules = VGroup(rule_1_tex, rule_2_tex, rule_3_tex, rule_4_tex)
        rules_2_4 = VGroup( rule_2_tex, rule_3_tex, rule_4_tex)
        rules.arrange_in_grid(cols=1).move_to((0,1,0))
        
        #align rules at arrows
        center_1 = rule_1_tex.get_center()
        dir_1 =  (0,center_1[1], 0) - rule_1_tex.submobjects[0].get_part_by_tex(r"\; \rightarrow \;").get_center()
        rule_1_tex.move_to((0,center_1[1],0 ) + dir_1)

        center_2 = rule_2_tex.get_center()
        dir_2 =  (0,center_2[1], 0) - rule_2_tex.submobjects[0].get_part_by_tex(r"\; \rightarrow \;").get_center()
        rule_2_tex.move_to((0,center_2[1],0 ) + dir_2)

        center_3 = rule_3_tex.get_center()
        dir_3 =  (0,center_3[1], 0) - rule_3_tex.submobjects[0].get_part_by_tex(r"\; \rightarrow \;").get_center()
        rule_3_tex.move_to((0,center_3[1],0 ) + dir_3)

        center_4 = rule_4_tex.get_center()
        dir_4 =  (0,center_4[1], 0) - rule_4_tex.submobjects[0].get_part_by_tex(r"\; \rightarrow \;").get_center()
        rule_4_tex.move_to((0,center_4[1],0 ) + dir_4)
        
        
        catnip_rule = Emoji(r"\;c\;", ("🌿", "catnip.png", None) ,rule_3_tex, update_config=config)


        rule_1_tex_copy = deepcopy(rule_1_tex).move_to(PLACE_FOR_CURRENT_RULE).scale(SCALE_ACTIVE_RULE)
        rule_2_tex_copy = deepcopy(rule_2_tex).move_to(PLACE_FOR_CURRENT_RULE).scale(SCALE_ACTIVE_RULE)
        rule_3_tex_copy = deepcopy(rule_3_tex).move_to(PLACE_FOR_CURRENT_RULE).scale(SCALE_ACTIVE_RULE)
        rule_4_tex_copy = deepcopy(rule_4_tex).move_to(PLACE_FOR_CURRENT_RULE).scale(SCALE_ACTIVE_RULE)


        

        self.play(Wait(calculate_wait_time(self,"take a look"), 
                       frozen_frame=False))
        self.play( LaggedStart(FadeOut(onthology, scale=3.0),Write(rules), FadeIn(catnip_rule), lag_ratio=0.4))

        self.play(Wait(calculate_wait_time(self,":"), 
                       frozen_frame=False))
        self.play(Transform(rules, rules_r, run_time = 0.9), FadeOut(catnip_rule, shift=(-1,0,0), run_time = 0.9), query_r.animate(run_time=0.9).move_to(PLACE_FOR_QUERY_INACTIVE))
        self.remove(rules)
        self.remove(catnip_rule)
        self.add(rules_r)

        rule_1_tex = rule_1_tex_copy
        rule_2_tex = rule_2_tex_copy
        rule_3_tex = rule_3_tex_copy
        rule_4_tex = rule_4_tex_copy
        catnip_rule = Emoji(r"\;c\;", ("🌿", "catnip.png", None) ,rule_3_tex, update_config=config)

        line_1 = rules_r.submobjects[2].copy()
        self.play(Wait(calculate_wait_time(self,"first one"), 
                       frozen_frame=False))
        self.play(rules_r.animate(run_time = 0.5).move_to(PLACE_FOR_RULES_INACTIVE).scale(0.6), Transform(line_1, rule_1_tex, run_time = 0.5))
        self.remove(line_1)
        self.add(rule_1_tex)


       



        self.next_section("A.3", skip_animations=False)
        """
        First rule,
        Apply in a naive manner and slowly
        
        """

        vertices_body = ["x","y"]
        edges_body = [(r"\mathsf{affects}", "x","y")]
        concepts_body = [("x",r"\mathsf{HappyPotion}", DL)]
        body_1 = BestDiGraph(vertices_body,
            edges_body,
            concepts=concepts_body,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True).move_to((-1,0,0))
        body_1["x"].move_to((-3,0,0))
        body_1["y"].move_to((-1,2,0))
        body_1.update()

        vertices_head = ["x","y","z"]
        edges_head = [(r"\mathsf{contains}","x","z"),(r"\mathsf{likes}", "y","z")]
        head_1 = BestDiGraph(vertices_head,
            edges_head,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True,
            edge_type=FlexibleDashedLine).move_to((3,0,0))
        head_1["z"].move_to((6,0,0))
        rule_1 = Rule(body_1, head_1).align_head()
        rule_1.anchor_points = {"z":"y"}

        """
        Create the Body Graph from the rule
        
        """
        body_vars = ["x","y"]
        roles = [(r"\mathsf{affects}", "x", "y")]
        concepts = [(r"\mathsf{HappyPotion}", "x")]
        var_mobs = []
        role_mobs = []
        concept_mobs = []
        role_graph_mobs = []
        concept_graph_mobs = []
        var_graph_mobs = []
        head_vars = ["z"]


        self.play(Wait(calculate_wait_time(self,"if x is ..."), 
                       frozen_frame=False))
        for var in body_vars:
            var_mob = rule_1_tex.submobjects[0].get_parts_by_tex(" " + var + " ").copy()
            var_mobs.append(VGroup(*var_mob))
            var_graph_mobs.append(body_1[var])
            move_animation = [mob.animate(run_time=0.7).move_to(var_graph_mobs[-1].get_center()) for mob in var_mob ]
            self.play(*move_animation)
            scale_animation = [mob.animate(run_time = 0.2).scale_to_fit_width(var_graph_mobs[-1].submobjects[0].width) for mob in var_mob ]
            self.play(*scale_animation)
        
        for concept, v in concepts:
            concept_mob = rule_1_tex.submobjects[0].get_part_by_tex(concept).copy()
            concept_mobs.append(concept_mob)
            concept_graph_mobs.append(body_1.concept_labels[(v,concept)][0])
            self.play(concept_mob.animate(run_time = 0.7).move_to(concept_graph_mobs[-1].get_center()).scale_to_fit_width(concept_graph_mobs[-1].width))
        
        for role, u, v in roles:
            role_mob = rule_1_tex.submobjects[0].get_part_by_tex(role).copy()
            role_mobs.append(role_mob)
            role_graph_mobs.append(VGroup(body_1.edges[(u,v)], body_1.edge_labels[(u,v)]))
            #self.play(role_mob.animate.move_to(role_graph_mobs[-1].get_center()))
            self.play(Transform(role_mob,role_graph_mobs[-1], run_time = 0.7))

        self.add(body_1)
        self.play(Wait(calculate_wait_time(self,"then x must ..."), 
                       frozen_frame=False))
        self.play(FadeOut(*var_mobs, run_time = 0.5),FadeOut(*concept_mobs, run_time = 0.5), 
                  FadeIn(*concept_graph_mobs, run_time = 0.5), 
                  FadeIn(*var_graph_mobs, run_time = 0.5),
                  FadeOut(* role_mobs, run_time = 0.5),
                  Circumscribe(rule_1_tex.submobjects[0].get_part_by_tex(r" \; \rightarrow \;"), run_time = 0.5, color = Style.logic))
        
        self.add(head_1)
        
        
        
        ra = RuleLoopAnimation(rule_1, speed=0.4)
        
        head_1.add_updater(ra.update_rule)
        
        
        contains = rule_1_tex.submobjects[0].get_part_by_tex(r" \mathsf{contains}(x,z)").copy()
        likes = rule_1_tex.submobjects[0].get_part_by_tex(r" \mathsf{likes}(y,z)").copy()
        exists_z = rule_1_tex.submobjects[0].get_part_by_tex(r" \exists z \;").copy()
        
        direction_z = rule_1.overlay["z"].get_center() - exists_z.get_center()

        line_contains = Line( *rule_1.overlay.edges[("x","z")].get_start_and_end(), stroke_width=0)
        line_likes = Line( *rule_1.overlay.edges[("y","z")].get_start_and_end(), stroke_width=0)

        transform_tex_to_graph = LaggedStart(FadeOut(exists_z, shift=direction_z, run_time = 0.5),
                  LaggedStart(Transform(contains, line_contains , run_time = 0.5), 
                                    Transform(likes, line_likes, run_time = 0.5), lag_ratio=0.2), lag_ratio=1.0)

        self.play( transform_tex_to_graph,
                  Wait(2.5, frozen_frame=False))
        self.remove(line_contains)
        self.remove(line_likes)
        self.remove(contains)
        self.remove(likes)

        rule_1.head_graph["z"].move_to(rule_1.body_graph["y"].get_center() + (2,-2,0))
        #self.remove(rule_1.head_graph["z"])
        print(rule_1.body_graph["x"].get_center())
        print(rule_1.body_graph["y"].get_center())
        print(rule_1.head_graph["z"].get_center())
        self.play(Unwrite(rule_1_tex), 
                  rule_1.body_graph.animate.move_to(PLACE_FOR_CURRENT_RULE_GRAPH),
                  #rule_1.body_graph.vertices["x"].animate.move_to((-5,0,0 )),
                  #rule_1.body_graph.vertices["y"].animate.move_to(),
                  graph.animate.move_to(PLACE_FOR_GRAPH_ACTIVE))
        
        #self.play(graph["k"].animate.move_to(graph["k"].get_center() + (0,2,0)))
        
        (r, animations) = graph.apply_rule_no_succession(rule_1, 
                                     ra, 
                                     [("x","p"),("y","k")],
                                     [("z", "i"),("x","p"),("y","k")],
                                     self,
                                     relative_positions={"z":("y",(0,-2,0))},
                                     transition_to_solid_line=False,
                                     apply = True)
        self.play(Wait(calculate_wait_time(self,"we know that x matches"), 
                       frozen_frame=False))
        hom_sound(self, wait_time=1, duration=1.5)
        self.play(Succession(*animations[:3], run_time = 6), suspend_mobject_updating = False)
        
        
      
        #tip_x = r.overlay.edges[("x","z")].get_tips()[0].copy()
        #tip_y = r.overlay.edges[("y","z")].get_tips()[0].copy()
        r.overlay.suspend_updating()
        self.add(r.overlay)
        def color_updater(mob, alpha):
            # alpha goes from 0 to 1 during the animation
            
            mob.set_stroke(interpolate_color(WHITE, Style.err, alpha ))
            for ((u,v), edge) in mob.edges.items():
                for edge_submob in edge.submobjects:
                    if isinstance(edge_submob, ArrowTip):
                        edge_submob.set_fill(interpolate_color(WHITE, RED, alpha ))
            
            for (role_name, u, v) in mob.role_data:
                mob.edge_labels[(u,v)].get_part_by_tex(role_name).set_color(interpolate_color(WHITE, Style.err, alpha ))
            for (label, vert) in mob.vertices.items():
                for submob in vert.submobjects:
                    if isinstance(submob, MathTex):
                        submob.get_part_by_tex(label).set_color(interpolate_color(WHITE, Style.err, alpha ))

            
        #self.add(Dot(r.overlay.edges[("x","z")].get_tips()[0].get_center()))

        #r.overlay.add_edges((r"\mathsf{contains}", ("x","z")), edge_type=FlexibleDashedLine)
        self.play(Wait(calculate_wait_time(self,"dont know any ingredient"), 
                       frozen_frame=False))
        wiggle_and_color = AnimationGroup(Wiggle(r.overlay, rotation_angle=0.02 * TAU), 
                                          UpdateFromAlphaFunc(r.overlay, color_updater)
                                          #r.overlay.animate.move_to((0,0,0))
                                          )
        #self.add(Dot(r.overlay.edges[("x","z")].get_tips()[0].get_center()))
        #print(r.overlay.edges[("x","z")].get_tips())
        fail_sound(self, delta_sounds["no Element 2"])
        r.overlay.resume_updating()
        self.play(wiggle_and_color, ResetRuleLoop(ra))
        self.play(Uncreate(r.overlay, run_time = 1))
        r.set_interpolate(0)
        self.add(r.overlay)
        self.play(Wait(calculate_wait_time(self,"fresh element"), 
                       frozen_frame=False))
        animations[3]= LaggedStart(*animations[3].animations[1:], lag_ratio=0.8, run_time = 2)
        animations[4] = AnimationGroup( Appear(graph), ResetInterpolate(r))
        pop_sound(self, delta_sounds["new element r1"])
        self.play(LaggedStart( Succession(*animations[3:], run_time = 2), lag_ratio=0.8))
        self.remove(r)
        self.play(Wait(0.9, frozen_frame=False))
        dt = ra.finish()
        self.play(Wait(abs(dt), frozen_frame=False))
        self.play(Wait(calculate_wait_time(self,"next rule?"), 
                       frozen_frame=False))
        self.play(Uncreate(body_1, run_time = 0.8))

        self.next_section("B", skip_animations=False)

        """
        Apply Rule 2, 
        
        """

        vertices_body = ["x","y"]
        edges_body = [(r"\mathsf{contains}", "x","y")]
        concepts_body = [("x",r"\mathsf{PlantBased}", UL)]
        body_2 = BestDiGraph(vertices_body,
            edges_body,
            concepts=concepts_body,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True).move_to((-2,-0.5,0))
        body_2["x"].move_to((-4.5,1.5,0))
        body_2["y"].move_to((-2.5,-0.5,0))
        #body_2.move_to(PLACE_FOR_CURRENT_RULE_GRAPH)
        body_2.update()

        vertices_head = ["x","y"]
        edges_head = []
        concepts_head = [(("y",r"\mathsf{PlantBased}", DR))]
        head_2 = BestDiGraph(vertices_head,
            edges_head,
            concepts=concepts_head,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True,
            edge_type=FlexibleDashedLine).move_to((2,-0.5,0))

        rule_2 = Rule(body_2, head_2).align_head()
        #rule_2.anchor_points = {"z":"y"}


        
        
        
        
        self.play(Wait(calculate_wait_time(self,"next one"), 
                       frozen_frame=False))
        line_2 = rules_r.submobjects[3].copy()
        self.play(Transform(line_2,rule_2_tex))
        self.remove(line_2)
        self.add(rule_2_tex)
        self.play(Wait(3, frozen_frame=False))
        self.play(Transform(rule_2_tex, body_2))
        self.add(body_2)
        self.add(head_2)
        self.add(rule_2.overlay)
        self.remove(rule_2_tex)

        ra_2 = RuleLoopAnimation(rule_2,speed = 0.6)
        head_2.add_updater(ra_2.update_rule)

        self.play(Wait(2, frozen_frame=False))
        
        (r, animations) = graph.apply_rule(rule_2, 
                                     ra_2, 
                                     [("x","p"),("y","i")],
                                     [("x","p"),("y","i")],
                                     self,
                                     #relative_positions={"z":("y",(0,0,0))},
                                     transition_to_solid_line=True,
                                     hom_time=3, 
                                     introduction_time=1,
                                     apply = True)
        self.play(Wait(calculate_wait_time(self,"So, following your logic"), 
                       frozen_frame=False))
        animations.run_time = 3.8
        hom_sound(self, wait_time=.5, duration=1.0)
        pop_sound(self, delta_sounds["new concept r2"])
        self.play(animations)
        self.remove(r)
        dt = ra_2.finish()
        print(dt)
        self.play(Wait(abs(dt), frozen_frame=False))

        self.play(Wait(calculate_wait_time(self,"Exactly"), 
                       frozen_frame=False))
        self.play(Uncreate(body_2))
        
        self.next_section("C", skip_animations=False)
        """
        Apply Rule 3
        
        """
        vertices_body = ["x","y"]
        edges_body = [(r"\mathsf{likes}", "x","y")]
        concepts_body = [("y",r"\mathsf{PlantBased}", UL),("x",r"\mathsf{Cat}", UL)]
        body_3 = BestDiGraph(vertices_body,
            edges_body,
            concepts=concepts_body,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True).move_to((-2,-0.5,0))
        body_3["x"].move_to((-5,-0.5,0))
        body_3["y"].move_to((-3,1.5,0))
        #body_3.move_to(PLACE_FOR_CURRENT_RULE_GRAPH)
        body_3.update()

        vertices_head = ["y","c"]
        edges_head = [(r"\mathsf{contains}", "y","c")]
        
        head_3 = BestDiGraph(vertices_head,
            edges_head,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True,
            edge_type=FlexibleDashedLine).move_to((-2,-0.5,0))
        head_3["c"].move_to((-1,-0.5,0))
        head_3["y"].move_to((-3,1.5,0))
        head_3.update()
        rule_3 = Rule(body_3, head_3).align_head()
        #rule_2.anchor_points = {"z":"y"}

        config_rule = {"opacity": True, 
                  "position": True, 
                  "scale": False}
        
        
        self.play(Wait(calculate_wait_time(self,"third rule"), 
                       frozen_frame=False))
        line_3 = rules_r.submobjects[4].copy()
        catnip_rule.set_z_index(20)
        self.play(Transform(line_3,rule_3_tex, run_time = 0.8), FadeIn(catnip_rule, run_time = 0.8, shift=5*UP+8*RIGHT))
        self.remove(line_3)
        self.add(rule_3_tex)

        self.play(Wait(1.2, frozen_frame=False))

        self.play(Transform(rule_3_tex, body_3, run_time = 0.8), FadeOut(catnip_rule, shift= (head_3["c"].get_center()- catnip_rule.get_center()), run_time = 0.8))
        self.add(body_3)
        self.add(head_3)
        self.add(rule_3.overlay)
        self.remove(rule_3_tex)
        ra_3 = RuleLoopAnimation(rule_3, speed=0.5)
        
        
        head_3.add_updater(ra_3.update_rule)
        catnip_rule_graph = Emoji("c", ("🌿", "catnip.png", None) ,rule_3.overlay["c"], update_config=config_rule, scale_factor=1.5)
        rule_3.overlay["c"].set_z_index(0)
        self.add(catnip_rule_graph)

        self.play(Wait(1, frozen_frame=False))
        graph.set_z_index(3)
        (r, animations) = graph.apply_rule_no_succession(rule_3, 
                                     ra_3, 
                                     [("x","k"),("y","i")],
                                     [("x","k"),("y","i"), ("c","c")],
                                     self,
                                     relative_positions={"c":("y", graph["c"].get_center() - graph["i"].get_center())},
                                     transition_to_solid_line=True,
                                     hom_time=1.3,
                                     introduction_time=1.4,
                                     apply = True)
        
        
        #catnip_rule_2 = Emoji("c", ("😎", "catnip.png", None) ,r.overlay["c"], update_config=config_rule)
        hom_sound(self,wait_time=.5, duration=1.1)
        pop_sound(self, delta_sounds["new role r3"])

        self.play(Succession(*animations[:-1], suspend_mobject_updating=False))

        catnip_rule_graph.update_opacity = False
        catnip_rule_graph.set_opacity(0.0)
        self.remove(catnip_rule_graph)
        self.play(animations[-1])
        self.remove(r)

        
        dt = ra_3.finish()
        catnip_rule_graph.scale(0.0)
        self.remove(rule_3.overlay)
        self.remove(catnip_rule_graph)
        self.play(Uncreate(body_3, run_time = 0.4))
        
        #print(r.overlay.edges[("x","z")].get_tips())
        #r.overlay.edges[("x","z")].update()
       

        self.next_section("D",skip_animations=False)
        """
        Apply Rule 4
        
        """

        vertices_body = ["x","y", "z"]
        edges_body = [(r"\mathsf{contains}", "x","y"),(r"\mathsf{contains}", "y","z")]

        body_4 = BestDiGraph(vertices_body,
            edges_body,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True).move_to((-1,0,0))
        body_4["x"].move_to((-6,1.5,0))
        body_4["y"].move_to((-4,-0.5,0))
        body_4["z"].move_to((-2,1.5,0))
        #body_4.move_to(PLACE_FOR_CURRENT_RULE_GRAPH)
        body_4.update()

        vertices_head = ["x","y","z"]
        edges_head = [(r"\mathsf{contains}", "x","z")]

        head_4 = BestDiGraph(vertices_head,
            edges_head,
            #edge_label_config={"labelFontSize":12, "labelOffset":0.15},
            labels =  True,
            edge_type=FlexibleDashedLine).move_to((3,-0.5,0))
        """ originally y is 0.0 """

        rule_4 = Rule(body_4, head_4).align_head()
        #rule_2.anchor_points = {"z":"y"}


        
        
        
        self.play(Wait(calculate_wait_time(self,"forth rule"), 
                       frozen_frame=False))
        line_4 = rules_r.submobjects[5].copy()
        self.play(Transform(line_4,body_4, run_time = 0.5))
        self.remove(line_4)
        self.add(body_4)
        self.add(rule_4.overlay)
        self.remove(rule_4_tex)
        ra_4 = RuleLoopAnimation(rule_4, speed=0.4)
        
        head_4.add_updater(ra_4.update_rule)
        s = 2.5
        new_center = graph["k"].get_center() + (-0.5,1,0)
        def label_updater(mob, alpha):
            value = abs(alpha - 1) * DR +  (0,alpha * (-1.5),0)
            mob.concept_labels[("i",r"\mathsf{PlantBased}")] = (mob.concept_labels[("i",r"\mathsf{PlantBased}")][0],value)
            for i in range(0, len(mob.concept_data)-1):
                if "i" == mob.concept_data[i][0]:
                    mob.concept_data[i] = ("i",r"\mathsf{PlantBased}", value)
        def label_updater2(mob, alpha):
            value = abs(alpha - 1) * UL +  alpha * (UL + LEFT)
            mob.concept_labels[("p",r"\mathsf{PlantBased}")] = (mob.concept_labels[("p",r"\mathsf{PlantBased}")][0],value)
            for i in range(0, len(mob.concept_data)-1):
                if "i" == mob.concept_data[i][0]:
                    mob.concept_data[i] = ("p",r"\mathsf{PlantBased}", value)
        def label_offset(mob, alpha):
            value = abs(alpha - 1) * 0.25 +  alpha * (0.4)
            mob.conceptlabelOffset = value
        self.play(Wait(2, frozen_frame=False), 
                  graph["k"].animate(run_time = 1.5).move_to( new_center ),
                  graph["p"].animate(run_time = 1.5).move_to( new_center + (-1*s, -sqrt(3)*s, 0)), 
                  graph["c"].animate(run_time = 1.5).move_to( new_center + ( 1*s, -sqrt(3)*s, 0)),
                  graph["i"].animate(run_time = 1.5).move_to( new_center + (0*s,( -sqrt(3) / 1.5) * s,0)),
                  graph["b"].animate(run_time = 1.5).move_to( new_center + (1*s, 0, 0)),
                  UpdateFromAlphaFunc(graph, label_updater, run_time = 1.5),
                   UpdateFromAlphaFunc(graph, label_updater2, run_time = 1.5),
                   UpdateFromAlphaFunc(graph, label_offset, run_time = 1.5)  
                  )
        
        (r, animations) = graph.apply_rule(rule_4, 
                                     ra_4, 
                                     [("x","p"),("y","i"), ("z","c")],
                                     [("x","p"),("y","i"), ("z","c")],
                                     self,
                                     hom_time=3,
                                     introduction_time=2,
                                     #relative_positions={"z":("y",(0,0,0))},
                                     transition_to_solid_line=True,
                                     apply = True)
        
        animations.run_time = 3.4
        hom_sound(self, wait_time=.5, duration=1.0)
        pop_sound(self, delta_sounds["new role r4"]+.2)
        self.play(animations)
        self.remove(r)
        
        self.play(Wait(calculate_wait_time(self,"meaning"), 
                       frozen_frame=False))
        dt = ra_4.finish()
        self.play(FadeOut(rule_4.overlay, run_time = 0.2), Uncreate(body_4, run_time = 0.3), Unwrite(rules_r,run_time = 0.3))

        

        self.next_section("E", skip_animations=False)
        """
        Reapply Query
        
        """

        query_graph = CoolDiGraph(["k", "p", "y"], 
                                  [(r"\mathsf{contains}","p","y"), (r"\mathsf{allergicTo}","k","y")]
                                  )
        query_graph["k"].move_to((-2,-1,0))
        query_graph["p"].move_to((2,-1,0))
        query_graph["y"].move_to((0,1,0))

        query_graph.move_to(PLACE_FOR_APPLY)
        query_graph.update()


        kiki_ill_query_graph = Emoji("k", ("😾", "sad_cat.png", "#400040"),query_graph["k"], update_config={"opacity": False, 
                  "position": True, 
                  "scale": False})

        potion_query_graph = Emoji("p", ("🧪", "potion.png", None) ,query_graph["p"], update_config={"opacity": False, 
                  "position": True, 
                  "scale": False}, scale_factor=1.8)

       
        
        kiki_query = Emoji(r"\;z\;", ("😾", "sad_cat.png", "#400040"),query, update_config={"opacity": False, 
                  "position": False, 
                  "scale": False})
        potion_query = Emoji(r"\;x\;", ("🧪", "potion.png", None) ,query, update_config={"opacity": False, 
                  "position": False, 
                  "scale": False})

        line = query_r.submobjects[2].copy()

        kiki_query.set_z_index(20)
        potion_query.set_z_index(20)
        
        #self.play(Transform(line,query, run_time = 1),
        #                      FadeIn(kiki_query, shift = kiki_query.get_center() - line.get_center(), run_time = 1), 
        #                      FadeIn(potion_query,shift = potion_query.get_center() - line.get_center(), run_time = 1))



        self.play(Transform(line,query_graph, run_time = 1),FadeIn(kiki_ill_query_graph, shift = query_graph.get_center() - line.get_center(), run_time = 1), 
                FadeIn(potion_query_graph,shift = query_graph.get_center() - line.get_center() , run_time = 1), 
                Unwrite(query_r, run_time = 1))
        self.remove(line)
        """
        self.play(FadeOut(kiki_query, shift = query_graph.get_center() - kiki_query.get_center(), run_time = 1), 
                FadeOut(potion_query, shift = query_graph.get_center() - potion_query.get_center(), run_time = 1), 
                Transform(query,query_graph, run_time = 1),FadeIn(kiki_ill_query_graph, shift = query_graph.get_center() - kiki_query.get_center(), run_time = 1), 
                FadeIn(potion_query_graph,shift = query_graph.get_center() - potion_query.get_center() , run_time = 1))
        """
        self.remove(query)
        self.add(query_graph)
        

        copy_query = deepcopy(query_graph).set_z_index(0)
        self.add(copy_query)
        hom = Homomorphism(copy_query, graph, [("k","k"),("p","p"),("y","c")])
        kiki_ill_query_graph_C = Emoji("k", ("😾", "sad_cat.png", "#400040"),copy_query["k"], update_config={"opacity": True, 
                  "position": True, 
                  "scale": False})

        potion_query_graph_C = Emoji("p", ("🧪", "potion.png", None) ,copy_query["p"], update_config={"opacity": True, 
                  "position": True, 
                  "scale": False}, scale_factor=1.8)
        kiki_ill_query_graph.set_z_index(30)
        potion_query_graph.set_z_index(30)
        kiki_ill_query_graph_C.set_z_index(20)
        potion_query_graph_C.set_z_index(20)
        hom_animation = HomomorphismAnimation(copy_query, hom, run_time = 2.5)
        text = copy_query.edge_labels[("p", "y")]
        angle = text.submobjects[-1].get_angle()
        text.rotate(-angle)
        text_h = text.get_height()
        text.rotate(angle)
        
        def label_updater(mob, alpha):
            turn_point = 0.3
            diff = smooth(clip(abs(turn_point - alpha)* 3,0,1))
            angle = mob.submobjects[-1].get_angle()
            mob.rotate(-angle)
            mob.stretch_to_fit_height(text_h * diff)
            mob.rotate(angle)

        hom_animation.run_time = 2.5
        self.add(kiki_ill_query_graph_C, potion_query_graph_C)
        
        config_rule_check = {"opacity": False, 
                  "position": True, 
                  "scale": False}
        checkmark_parent = VGroup(MathTex(r'\cdot'))
        checkmark = Emoji(r'\cdot', ("✅", "checkmark.png", None) , checkmark_parent, update_config=config_rule_check, scale_factor = 12)
        checkmark.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        
        
        hom_sound(self, wait_time=.5, duration=1.5)
        success_sound(self, delta_sounds["query match"])





        self.play(LaggedStart(AnimationGroup( UpdateFromAlphaFunc(text,label_updater, run_time=2.5), hom_animation), GrowFromPoint(checkmark, checkmark.get_center(), run_time=0.5), lag_ratio=0.8))
        self.play(Wait(calculate_wait_time(self,"indeed"), 
                       frozen_frame=False))
        
        catnip.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.play(Wiggle(graph["c"], scale_value=2,rotation_angle=0.04 * TAU ),
                   Wiggle(catnip,scale_value=2,rotation_angle=0.04 * TAU), 
                   Wiggle(query_graph["y"], scale_value=2,rotation_angle=0.04 * TAU ), 
                   FadeOut(checkmark, scale=0.01))

        

        self.next_section("F", skip_animations=False)
        """
        Create and apply the antidote
        
        """


        POSITION_KIKI = (0,0,0) 
        antidote = VGroup(MathTex(r"\cdot")).move_to((-2,-2,0))
        kiki_happy = VGroup(MathTex(r"\cdot")).move_to(POSITION_KIKI)
        kiki_happy_emoji = Emoji(r"\cdot", ("😽", "kiki_happy.png", "#000000") ,kiki_happy, update_config={"opacity": False, 
                  "position": True, 
                  "scale": False}, scale_factor=20)
        kiki_sad = VGroup(MathTex(r"\cdot")).move_to(POSITION_KIKI)
        kiki_sad_emoji = Emoji(r"\cdot", ("😾", "sad_cat.png", "#400040") ,kiki_sad, update_config={"opacity": False, 
                  "position": True, 
                  "scale": False}, scale_factor=20)
        antidote_emoji = Emoji(r"\cdot", ("💉", "antidote.png", None) ,antidote, update_config={"opacity": False, 
                  "position": True, 
                  "scale": False}, scale_factor=20)
        self.add(antidote, kiki_happy, kiki_ill)

        #trans_graph_table_sound(self, delta_sounds["to antidote"])
        self.play(FadeIn(antidote_emoji, shift =  antidote.get_center()- graph.get_center()), 
                  Transform(graph, antidote), 
                   FadeOut(kiki_ill, shift = antidote.get_center()- graph["k"].get_center()),
                    FadeOut(potion, shift = antidote.get_center()- graph["p"].get_center()),
                     FadeOut(catnip, shift = antidote.get_center()- graph["c"].get_center()),
                      FadeOut(basil, shift = antidote.get_center()- graph["b"].get_center()), 
                       Uncreate(query_graph), 
                        FadeOut(kiki_ill_query_graph), 
                         FadeOut(potion_query_graph))
        self.remove(graph, antidote)
        self.play(FadeIn(kiki_sad_emoji))

        self.play(antidote.animate.move_to((-0.9,-0.9,0)))
        kiki_happy_emoji.set_z_index(20)
        self.play(antidote.animate.move_to((-2,-2,0)), FadeOut(kiki_sad_emoji),FadeIn(kiki_happy_emoji)  )
        kiki_happy_emoji.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        meow(self, delta_sounds["meow"]) 
        self.play(Wiggle(kiki_happy), Wiggle(kiki_happy_emoji),FadeOut(antidote_emoji),FadeOut(antidote))
        self.play(kiki_happy.animate.move_to((0,-7,0)))


        
        
