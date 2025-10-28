from manim import *
from networkx import layout
from CQ import *
from database import *
from Homomorphism import *
from Rules import *
from bestDiGraph import *
from flexible_dashed_line import *
from render_emoji import *
from math import sqrt
from copy import copy
from sound_effects import *

import Style

varu = '{u}'
varv = '{v}'
varw = '{w}'
varx = '{x}'
vary = '{y}'
varry = '{{y}}'
varz = '{z}'

hp_concept = '\\mathsf{HappyPot}\\quad{{.}}'
db_layout = {'a':[0,0,0], 'b':[3,0,0], 'c':[6,0,0], 'd':[1.5,-sqrt(6),0]}
chase_layout = {'k': [0,0,0], 'p':[-2,0,0], 'b': [2,1, 0], 'c': [2,-1, 0], '?': [0,0,0]}

def get_univ_emojis(univ_model):
    config = {"opacity": False,
      "position": True,
      "scale": False}

    violet = '#400040'
    kiki_ill = Emoji("k", ("😾", "sad_cat.png", violet),univ_model["k"], update_config=config)
    potion = Emoji("p", ("🧪", "potion.png", None) , univ_model["p"], update_config=config)
    basil = Emoji("b", ("🪴", "basil.png", None) ,univ_model["b"],update_config=config)
    catnip = Emoji("c", ("🌿", "catnip.png", None) ,univ_model["c"], update_config=config)
    emojis = Group(kiki_ill, potion, basil, catnip)
    return emojis

def get_q_emojis(univ_model):
    config = {"opacity": False,
      "position": True,
      "scale": False}

    violet = '#400040'
    kiki_ill = Emoji("k", ("😾", "sad_cat.png", violet),univ_model["k"], update_config=config)
    potion = Emoji("p", ("🧪", "potion.png", None) , univ_model["p"], update_config=config)
    emojis = Group(kiki_ill, potion)
    return emojis

def get_rule_emojis(univ_model):
    config = {"opacity": False,
      "position": True,
      "scale": False}

    violet = '#400040'
    kiki_ill = Emoji("k", ("😾", "sad_cat.png", violet),univ_model["k"], update_config=config)
    emojis = Group(kiki_ill)
    return emojis


def abstract_query1():
    query = CQ([varx, vary, varz], [], [('r', varx, vary), ('s', varx, varz)])
    (q_tex, _) = query.to_mathtex(return_parts=True)
    q_graph = query.to_digraph()
    q_graph.change_layout({varx:[0,0,0], vary:[-2,0,0], varz:[2,0,0]})
    q_graph.update(q_graph)
    return q_tex, q_graph

def abstract_query2():
    q_verts = [varx, vary, varry]
    q_graph = CoolDiGraph(q_verts, [], layout={varx: [0,0,0], vary: [2,0,0], varry: [2,0,0]})
    q_graph.add_edges(*[('r', (varx, vary))], edge_config={'path_arc':-1})
    q_graph.add_edges(*[('s', (varx, varry))], edge_config={'path_arc':1})
    q_graph.update_edge_labels()
    return q_graph


def abstract_database():
    db = Group(RoleTable([('b', 'c'), ('d', 'a'), ('d', 'b')], 's').shift([-2.2,0,0]), RoleTable([('b','a')], 'r').shift([2.2,0,0])).scale(0.8).move_to([3.5,0,0])
    db_verts = ['a','b', 'c', 'd']
    db_edges = [('s', 'b','c'), ('s', 'd','a'), ('s', 'd','b'), ('r', 'b','a')]
    db_graph = CoolDiGraph(vertices=db_verts, edges=db_edges,layout=copy(db_layout))
    return db, db_graph


def abstract_rule():

    body_verts = [varx, vary, varz]
    body_eges = [('s', varx, vary), ('s', vary, varz)]
    body_graph = CoolDiGraph(body_verts, body_eges, layout={varx: [-2,0,0], vary : [0,0,0], varz: [2,0,0]})
 
    head_verts = [vary, varz, varu, varv]
    head_edges = [('s', varz, varu), ('r', vary, varv)]
    head_graph = CoolDiGraph(head_verts, head_edges, layout = {vary: [0,0,0], varz:[2,0,0], varu:[4,0,0], varv:[-sqrt(2), sqrt(2),0]}, edge_type=FlexibleDashedLine)
 
    rule = Rule(body_graph, head_graph)
    rule_loop = RuleLoopAnimation(rule)
    rule_loop.pause_anim()
    head_graph.add_updater(rule_loop.update_rule)

    rule_tex = MathTex('{s(x,y)','\\land', 's(y,z)', '\\rightarrow','\\exists u,v','\\ r(y,v)','\\land','s(z,u)}')
    rule_tex.submobjects[0].set_color(Style.body)
    rule_tex.submobjects[1].set_color(Style.body)
    rule_tex.submobjects[2].set_color(Style.body)

    rule_tex.submobjects[4].set_color(Style.head)
    rule_tex.submobjects[5].set_color(Style.head)
    rule_tex.submobjects[6].set_color(Style.head)
    rule_tex.submobjects[7].set_color(Style.head)

 
    return (body_graph, head_graph, rule, rule_loop, rule_tex)

def abstract_models():
    
    m_arc = -0.5
    m1_verts =['a','b', 'c', 'd','{b}','{c}','e', '{e}']
    m1_straight_edges = [('s', 'd','a'), ('s', 'd','b'), ('r', 'b','a')]
    m1_bend_edges = [('r', 'b', '{c}', m_arc), ('s', 'b', 'c', -m_arc),('r', 'c', 'e', m_arc), ('s', 'c', '{e}', -m_arc),('r', '{e}', 'b', m_arc), ('s', 'e', '{b}', -m_arc),]
    m1_layout = copy(db_layout)
    m1_layout['{c}'] = m1_layout['c']
    m1_layout['{b}'] = m1_layout['b']
    m1_layout['e'] =np.array([0.5*(m1_layout['b'][0]+m1_layout['c'][0]), m1_layout['d'][1], 0])
    m1_layout['{e}'] = m1_layout['e']

    m1_graph = CoolDiGraph(m1_verts, m1_straight_edges, layout=m1_layout)
    for r,x,y,a in m1_bend_edges:
        m1_graph.add_edges((r, (x,y)), edge_config={'path_arc' : a})

    m_scale = 0.7
    m1_graph.scale(m_scale)

    m2_verts = ['a','b', 'c', 'd','e', 'f']
    m2_edges = [('s', 'b','c'), ('s', 'd','a'), ('s', 'd','b'), ('r', 'b','a'),('s', 'c', 'e'), ('r', 'c', 'f'), ('r', 'e', 'f')]
    m2_layout = copy(db_layout)
    m2_layout['e'] = [9,0,0]
    m2_layout['f'] = [7.5, sqrt(6), 0]
    m2_graph = CoolDiGraph(m2_verts, m2_edges, layout=m2_layout)
    m2_graph.add_edges(('s', ('e', 'b')), edge_config={'path_arc':2*m_arc})
    m2_graph.scale(m_scale)

    return m1_graph, m2_graph

def chase_result():
    vertices = ['k', 'p', 'b', 'c', ]
    edges = [('\\mathsf{affects}', 'p', 'k'),
                  ('\\mathsf{allergicTo}', 'k', 'c'),
                  ('\\mathsf{allergicTo}', 'k','b'),
                  #('\\mathsf{contains}','p','c'),
                 ]
    concepts = [('k', '\\mathsf{Cat}', UP), ('p', hp_concept, LEFT), ('p', '\\mathsf{PlantBased}', DR), ('c', '\\mathsf{PlantBased}', DOWN)]
    layout = {'k': [0,0,0], 'p':[-2.5,-sqrt(3)*2.5,0], 'b': [2.5,0, 0], 'c': [2.5,-sqrt(3)*2.5, 0]}
    graph = BestDiGraph(vertices, edges, concepts, vertex_color = '#000000', layout=layout)
    graph.concept_labels[('p', hp_concept)][0].set_opacity_by_tex('.',0)

    graph.add_vertices('?',positions={'?':[0.01,-sqrt(3)/1.5*2.5,0]},  labels=False)
    graph.vertices['?'].submobjects[0].set_color("#FFFFFF")
    graph.add_concept_labels( ('?', '\\mathsf{PlantBased}', DOWN),)
    graph.add_edges(('\\mathsf{contains}',('?', 'c')), label_config={'labelOffset': -0.15})
    graph.add_edges(('\\mathsf{contains}', ('p', '?')))
    graph.add_edges(('\\mathsf{contains}', ('p', 'c')))
    graph.add_edges( ('\\mathsf{likes}', ('k',  '?')), label_config={'labelOffset': -0.15})

    return graph

def allergic_query():
    
    verts = ['p', 'y', 'k']
    edges = [('\\mathsf{allergicTo}', 'k', 'y')]
    layout = dict()
    layout['p'] = [-3.5,0,0]#univ_layout['p']
    layout['y'] = [-1.5,0,0]#univ_layout['c']
    layout['k'] = [1,0,0]#univ_layout['k']
    graph = BestDiGraph(verts, edges, vertex_color= '#000000', layout = layout)
    graph.add_edges(('\\mathsf{contains}', ('p', 'y')))
    graph.vertices['y'].submobjects[0].set_color("#FFFFFF")


    return graph

def more_kiki_models():
    m1_verts = ['k', 'p', 'b', 'c', '{c}']
    m1_edges = [('\\mathsf{affects}', 'p', 'k'),
                  ('\\mathsf{allergicTo}', 'k', 'c'),
                  ('\\mathsf{allergicTo}', 'k','b'),
                ]

    m1_layout = chase_layout.copy()
    m1_layout['{c}'] = m1_layout['c']+np.array([-0.02,-0.02,0])
    m1_layout.pop('?')
    m1_concepts = [('k', '\\mathsf{Cat}', UP), ('p', hp_concept, LEFT), ('p', '\\mathsf{PlantBased}', UL), ('c', '\\mathsf{PlantBased}', UR)]
    m1_digraph = BestDiGraph(m1_verts, m1_edges,m1_concepts, vertex_color = '#000000', layout = m1_layout)
    m1_digraph.concept_labels[('p', hp_concept)][0].set_opacity_by_tex('.', 0)
    m1_digraph.add_edges(('\\mathsf{contains}', ('p', '{c}')), edge_config={'path_arc': 1})
    l = m1_digraph.add_edges(('\\mathsf{contains}', ('p', 'c')), edge_config={'path_arc': 1})
    l[0].set_opacity(0)
    m1_digraph.edge_labels[('p', '{c}')].set_opacity_by_tex('\\mathsf{contains}', 0)
    m1_digraph.edge_labels[('p', '{c}')].update()
    m1_digraph.edge_labels[('p', '{c}')].suspend_updating()

    m1_digraph.add_edges(('\\mathsf{contains}', ('{c}', 'c')), edge_config={'path_arc': 5}, label_config={'labelOffset': -0.15})
    l = m1_digraph.add_edges(('\\mathsf{likes}', ('k', '{c}')), label_config={'labelOffset': -0.15})
    l[0].set_opacity(0)
    m1_emojis = get_univ_emojis(m1_digraph)

    m2_verts = ['k', 'p', 'b','{b}', 'c']
    m2_edges = m1_edges
    m2_layout = chase_layout.copy()
    m2_layout['{b}'] = m2_layout['b']
    m2_layout.pop('?')
    m2_concepts = m1_concepts + [('b', '\\mathsf{PlantBased}', UP)]
    m2_concepts[3]= (m2_concepts[3][0], m2_concepts[3][1], DR)
    m2_digraph = BestDiGraph(m2_verts, m2_edges, m2_concepts, vertex_color = '#000000', layout = m2_layout)
    m2_digraph.concept_labels[('p', hp_concept)][0].set_opacity_by_tex('.', 0)
    m2_digraph.add_edges(('\\mathsf{contains}', ('p', 'c')), edge_config={'path_arc': 1})
    m2_digraph.add_edges(('\\mathsf{contains}', ('p', 'b')), edge_config={'path_arc': -1})
    m2_digraph.add_edges(('\\mathsf{contains}', ('b', 'c')), )#label_config={'labelOffset': -0.15})
    l = m2_digraph.add_edges(('\\mathsf{likes}', ('k', '{b}')), label_config={'labelOffset': -0.15})
    l[0].set_opacity(0)
    m2_emojis = get_univ_emojis(m2_digraph)

    
    rule_body = BestDiGraph(['k'], [],[('k','\\mathsf{Cat}' , UP)], vertex_color='#000000')
    rule_body.add_vertices('?', labels=False, positions={'?': [0.01,-2,0]})
    rule_body.add_edges(('\\mathsf{likes}', ('k', '?')), label_config={'labelOffset': -0.15})
    rule_body.add_concept_labels( ( '?', '\\mathsf{PlantBased}',DL ))



    return m1_digraph, m1_emojis, m2_digraph, m2_emojis, rule_body

def basil_model():
    
    verts = ['k', 'p', 'b','{b}', 'c']
    edges = [('\\mathsf{affects}', 'p', 'k'),
                  ('\\mathsf{allergicTo}', 'k', 'c'),
                  ('\\mathsf{allergicTo}', 'k','b'),
                ]
    layout = chase_layout.copy()
    layout['{b}'] = layout['b']
    layout.pop('?')
    concepts = [('k', '\\mathsf{Cat}', UP), ('p', hp_concept, LEFT), ('p', '\\mathsf{PlantBased}', UL), ('c', '\\mathsf{PlantBased}', UR),('b', '\\mathsf{PlantBased}', UP)]
    concepts[3]= (concepts[3][0], concepts[3][1], DR)
    graph = BestDiGraph(verts, [], concepts, vertex_color = '#000000', layout = layout)
    for (e1,e2,e3) in edges:
        graph.add_edges((e1,(e2,e3)), label_config={'labelOffset':0.2})
    graph.concept_labels[('p', hp_concept)][0].set_opacity_by_tex('.', 0)
    graph.add_edges(('\\mathsf{contains}', ('p', 'c')), edge_config={'path_arc': 1}, label_config={'labelOffset':0.2})
    graph.add_edges(('\\mathsf{contains}', ('p', 'b')), edge_config={'path_arc': -1}, label_config={'labelOffset':0.2})
    graph.add_edges(('\\mathsf{contains}', ('b', 'c')), label_config={'labelOffset': 0.20})
    l = graph.add_edges(('\\mathsf{likes}', ('k', '{b}')), label_config={'labelOffset': -0.2})
    l[0].set_opacity(0)

    emojis = get_univ_emojis(graph)

    graph.move_to([0,0,0])
    graph.scale(1.5)
    graph.remove_edges(('b', 'c'))
    graph.remove_edges(('p', 'c'))
    graph.remove_edges(('p', 'b'))
    emojis.update()

    return graph, emojis


class Scene2(Scene):
    #We redefine our wait function such that RuleLoopAnimations won't get paused.
    def wait(self, *args, **kwargs):
        if 'frozen_frame' in kwargs:
            super().wait(*args, **kwargs)
        else:
            super().wait(*args, **kwargs, frozen_frame=False)

    def construct(self):
        self.add_sound("../recordings/Final/Scene2-final.flac")
        self.play_1()
        self.play_2()

    def play_1(self):
        height = (self.camera.frame_height)
        width = self.camera.frame_width
        margin = 0.5
        text_side_scale = 0.7 #Scale factor when we move text to the side

        #Speaking about ....
        coffee = Text('\uef59', font='Mononoki Nerd Font', font_size=300)
        loading = Style.create_heading('Loading coffee...').shift([0,-3,0])
        self.add_sound("./assets/coffee.wav", gain=5, time_offset=3)
        self.play(Write(coffee), Succession(Write(loading, run_time = 0.2), Wait(run_time=0.8)), run_time = 4-self.time)
        self.wait(1)
        self.play(Unwrite(coffee, reverse=False), Unwrite(loading, reverse=False), run_time = 7.29-self.time)
        self.wait(7.3-self.time)

        #We wanted to evaluate a query an a database
        query_t = Tex('Query $q$', font_size=Style.explanation_font_size).shift([0,3,0])
        database_t = Tex('Database $\\mathcal{D}$', font_size=Style.explanation_font_size).shift([0,2,0])
        evaluate_t = Tex('Evaluate $q$ on $\\mathcal{D}$.', font_size=Style.explanation_font_size).shift([0,-1,0])
        evaluate_tb = SurroundingRectangle(evaluate_t, color=Style.eval_border, buff=Style.bg_rect_buff, stroke_width=Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)
        self.play(Write(query_t), Write(database_t), Write(evaluate_t), Create(evaluate_tb))
        self.wait(11.6-self.time)

        #Our query was a bcq...
        query_tex, query_g = abstract_query1()
        query_tex.move_to(query_t)
        self.play(Write(query_tex), ScaleInPlace(query_t, text_side_scale),
                  MoveAlongPath(query_t, Line(query_t.get_center(), [-width/2+margin+text_side_scale*(query_t.width/2),2.5,0])),
                  database_t.animate.shift([0,-2,0]), FadeOut(evaluate_t), FadeOut(evaluate_tb)
                  )
        self.add(query_tex)
        self.wait(15.3-self.time) #such a query ask
        self.wait(17.5 - self.time) #conjunction of atomic
        self.play(Circumscribe(Group(*query_tex.submobjects[7:]), color=Style.logic), run_time = 1.5)
        self.wait(19.101-self.time) #with uspecified objects
        self.play(Circumscribe(Group(*query_tex.submobjects[:6]), color=Style.logic2), run_time = 1.5)
        self.wait(22.6-self.time)

        #The Database satisfies the query...
        db, db_g = abstract_database()
        sf = database_t.get_center() - 0.5*db[0].get_center() - 0.5*db[1].get_center()
        db[0].shift(sf)
        db[1].shift(sf)
        self.play(Create(db[0]), Create(db[1]),
                  ScaleInPlace(database_t, text_side_scale),
                  MoveAlongPath(database_t, Line(database_t.get_center(), [-width/2+margin+text_side_scale*(database_t.width/2), 2,0]))
                  )
        homomorphism_t = Tex('$\\mathcal{D}\\models q$', '\\quad if there exists a ', '\\textbf{homomorphism }', 'from $q$ to $\\mathcal{D}$.', font_size=Style.explanation_font_size)
        homomorphism_t.submobjects[0].set_color(Style.hom_border)
        homomorphism_t.submobjects[2].set_color(Style.hom_border)
        homomorphism_t.add_background_rectangle(color=Style.hom_border, buff=Style.bg_rect_buff, opacity=0, stroke_width=Style.bg_stroke_width, stroke_opacity=1, corner_radius=Style.bg_corner_radius)
        homomorphism_t.move_to([0,-height/2+margin+homomorphism_t.height-2, 0])
        self.play(homomorphism_t.animate.shift([0,2,0]))
        self.play(query_tex.animate.set_color_by_tex(varx, Style.hom1), db[0].get_entries((2,1)).animate.set_color(Style.hom1), db[1].get_entries((2,1)).animate.set_color(Style.hom1),)
        self.play(query_tex.animate.set_color_by_tex(vary, Style.hom2), db[1].get_entries((2,2)).animate.set_color(Style.hom2))
        self.play(query_tex.animate.set_color_by_tex(varz, Style.hom3), db[0].get_entries((2,2)).animate.set_color(Style.hom3))
        self.wait(32-self.time)
        self.play(homomorphism_t.animate.shift([0,-2,0]), db[0].animate.shift([0,-1,0]), db[1].animate.shift([0,-1,0]), query_tex.animate.shift([0,-1,0]), database_t.animate.shift([0,-1,0]), run_time = 1)
        self.remove(homomorphism_t)
        self.wait(33.8-self.time)

        #This is easily grasped...
        query_g.move_to(query_tex)
        db_g.move_to(db)
        self.play(Transform(query_tex, query_g), Uncreate(db[0]), Uncreate(db[1]), Create(db_g))
        self.add(query_g)
        self.remove(query_tex)
        h = Homomorphism(query_g, db_g, [(vary, 'a'), (varx, 'b'), (varz, 'c')], check_hom=True)
        self.play(query_g.vertices[varx].animate.set_color(Style.hom1), query_g.vertices[vary].animate.set_color(Style.hom2), query_g.vertices[varz].animate.set_color(Style.hom3), db_g.vertices['a'].animate.set_color(Style.hom2), db_g.vertices['b'].animate.set_color(Style.hom1), db_g.vertices['c'].animate.set_color(Style.hom3))
        hom_sound(self, duration=3)
        self.play(HomomorphismAnimation(query_g.copy(), h), run_time=3)
        self.wait(39.4-self.time)

        #Sure, but in practice...
        rule_t = Tex('Rules $\\mathcal{R}$', font_size=Style.explanation_font_size).scale(text_side_scale)
        rule_body_g, rule_head_g, rule, rule_loop, rule_tex = abstract_rule()
        rule_t.move_to([-width/2+margin+rule_t.width/2, query_t.get_center()[1],0])
        query_string_cp = query_t.copy()
        self.play(db_g.vertices['a'].animate.set_color(WHITE), db_g.vertices['b'].animate.set_color(WHITE), db_g.vertices['c'].animate.set_color(WHITE), Uncreate(query_g),
                  )
        rule_body_g.move_to(db_g).shift([0,3,0])
        #center mid y-z
        x_sf = -0.5* (rule_body_g.vertices[vary].get_center()[0] + rule_body_g.vertices[varz].get_center()[0])
        rule_body_g.shift([x_sf, 0,0])
        self.play(Create(rule_body_g),Transform(query_t, rule_t))
        self.add(rule_head_g)
        rule_loop.reset()

        #Such a rule is made of a body
        self.wait(51.1-self.time) 
        self.wait(53-self.time) #A BODY
        rule_head_g.remove_updater(rule.align_head)
        space = 0.1
        body_t = Tex('body', color=Style.body, font_size=Style.explanation_font_size).scale(text_side_scale)
        body_t.move_to([-width/2+margin+body_t.width/2,query_t.get_center()[1]-0.5,0])
        imp_arrow_t = Tex('$\\rightarrow$', font_size=Style.explanation_font_size).scale(text_side_scale)
        imp_arrow_t.move_to([-width/2+margin+body_t.width + imp_arrow_t.width/2+space,query_t.get_center()[1]-0.5,0])
        head_t = Tex('head', color=Style.head, font_size=Style.explanation_font_size).scale(text_side_scale)
        head_t.move_to([-width/2+margin+body_t.width + imp_arrow_t.width + head_t.width/2+2*space,query_t.get_center()[1]-0.5, 0]).align_to(body_t, UP)
        self.play(Indicate(rule_body_g, color=Style.body, scale_factor=1.1), Write(body_t))
        rule.add_head_updater()
        self.wait((0.64 - rule_loop.state)%1 / rule_loop.speed)
        rule_head_g.remove_updater(rule.align_head)
        rule_loop.pause_anim()

        self.wait(55.11-self.time)#A HEAD

        self.play(Indicate(rule_head_g, color=Style.head, scale_factor=1.1), Write(imp_arrow_t), Write(head_t))
        self.wait(56.5-self.time)

        rule_tex.scale(0.7).move_to(rule_body_g)
        x_sf = -rule_tex.get_center()[0]
        rule_tex.shift([x_sf, 0,0])
        rule_body_g_cp = rule_body_g.copy()
        self.add(rule_body_g_cp)
        self.remove(rule_body_g)
        self.play(Transform(rule_body_g_cp, rule_tex), FadeOut(rule_head_g))
        self.wait(5)
        self.play(rule_tex.submobjects[0].animate.set_color(WHITE),
                  rule_tex.submobjects[1].animate.set_color(WHITE),
                  rule_tex.submobjects[2].animate.set_color(WHITE),
                  rule_tex.submobjects[4].animate.set_color(WHITE),
                  rule_tex.submobjects[5].animate.set_color(WHITE),
                  rule_tex.submobjects[6].animate.set_color(WHITE),
                  rule_tex.submobjects[7].animate.set_color(WHITE),


                  FadeOut(body_t), FadeOut(head_t), FadeOut(imp_arrow_t))
        self.wait(63.6-self.time)
        self.play(Circumscribe(rule_tex.submobjects[1], color=Style.logic), Circumscribe(rule_tex.submobjects[6], color=Style.logic))#only conjunctions

        #And they are called existential rules...
        self.wait(65.2-self.time)
        self.remove(rule_body_g_cp)
        self.add(rule_tex)
        self.wait(1)
        self.play(Circumscribe(rule_tex.submobjects[4],run_time=3, color=Style.logic2))
        self.wait(1)
        old_c = rule_body_g.get_center()

        rule_body_g, rule_head_g,rule, rule_loop, _ = abstract_rule()
        rule_body_g.move_to(old_c)

        self.play(FadeOut(rule_tex), FadeIn(rule_body_g))
        self.add(rule_head_g)
        rule_loop.reset()
        dt = rule_loop.finish(0.65)
        self.wait(dt+0.1)
        dt = (1-rule_loop.state)/rule_loop.speed

        rule_loop.pause = False
        self.play(FadeOut(rule_body_g), run_time=dt)
        self.remove(rule_head_g)

        #I understand, but what does evaluating a query even mean in that context
        evaluate_t = Tex('How to evaluate $\\mathcal{R},\\mathcal{D}\\models q$?', font_size = Style.explanation_font_size)
        evaluate_t.move_to([0,rule_body_g.get_center()[1], 0])
        evaluate_tb = SurroundingRectangle(evaluate_t, color=Style.eval_border, stroke_width=Style.bg_stroke_width, buff=Style.bg_rect_buff, corner_radius=Style.bg_corner_radius)
        self.play(Succession(Write(evaluate_t), Create(evaluate_tb)), run_time = 1)
        self.wait(78.4-self.time)


        rule_body_g, rule_head_g,rule, rule_loop, _ = abstract_rule()
        rule_body_g.move_to(old_c)
        self.play(FadeOut(evaluate_t),FadeOut(evaluate_tb), FadeIn(rule_body_g))
        self.add(rule_head_g)
        rule_loop.reset()
        self.wait(79.5-self.time)

        #Well, since the data might...
        models_t = Tex('Models')
        models_t.scale(text_side_scale)
        models_t.move_to([-width/2+margin+models_t.width/2, database_t.get_center()[1], 0])

        model1_g, model2_g = abstract_models()
        hom1 = Homomorphism(rule_body_g, model1_g, [(varx, 'd'), (vary, 'b'), (varz, 'c')], check_hom=True)
        hom2 = Homomorphism(rule_body_g, model2_g, [(varx, 'b'), (vary, 'c'), (varz, 'e')], check_hom=True)
        model1_g.shift(db_g.vertices['a'].get_center() - model1_g.vertices['a'].get_center()).shift([4.5,-0.5,0])
        model2_g.shift(0.5*(db_g.vertices['a'].get_center() + db_g.vertices['d'].get_center()) - model2_g.vertices['e'].get_center()).shift([2.5,-0.5,0])

        rule_loop.finish(stop_time=0.65)
        self.play(FadeOut(db_g), FadeOut(database_t), FadeIn(models_t), FadeIn(model1_g), FadeIn(model2_g))
        self.add(model2_g)

        rt = 3
        highlight_edges = [model1_g.edges[(hom1.apply(varx), hom1.apply(vary))], model1_g.edges[(hom1.apply(vary), hom1.apply(varz))],
                           model2_g.edges[(hom2.apply(varx), hom2.apply(vary))], model2_g.edges[(hom2.apply(vary), hom2.apply(varz))]]
        rule.set_interpolate(0.65)
        model1_t=Tex('$M_1$')
        model1_t.move_to([-width/2+margin+model1_t.width/2, model1_g.get_center()[1]+0.5,0])
        model2_t = Tex('$M_2$')
        model2_t.move_to([width/2-margin-model2_t.width/2, model1_g.get_center()[1]-1.7,0])
        hom_sound(self, duration=rt)

        #all possible ways to complete the data
        self.play(HomomorphismAnimation(rule_body_g.copy(), hom1), HomomorphismAnimation(rule_body_g.copy(), hom2),
                  rule_body_g.edges[(varx,vary)].animate.set_color(Style.body), rule_body_g.edges[(vary, varz)].animate.set_color(Style.body), rule_head_g.edges[(vary, varv)].animate.set_color(Style.head), rule_head_g.edges[(varz, varu)].animate.set_color(Style.head),
                  *[e.animate.set_color(Style.body) for e in highlight_edges],
                   run_time = rt)
        rule.set_interpolate(0.65)

        cp1 = model2_g.edges[('c', 'f')].copy().set_color(Style.head)
        cp2 = model2_g.edges[('e', 'b')].copy().set_color(Style.head)
        cp3 = model1_g.edges[('b', 'a')].copy().set_color(Style.head)
        cp4 = model1_g.edges[('c', '{e}')].copy().set_color(Style.head)
        cps = [cp1,cp2,cp3,cp4]
        rf = lambda alpha: smooth(0.5*alpha)
        rt = 4
        model1_g.add(cp3, cp4)
        model2_g.add(cp1,cp2)
        tw = 4
        self.play(*[ShowPassingFlash(cp, tw, rate_function = rf, run_time = rt) for cp in cps], FadeIn(model1_t, run_time=rt), FadeIn(model2_t, run_time=rt))
        self.remove(cp1, cp2, cp3, cp4)
        model1_g.remove(cp3,cp4)
        model2_g.remove(cp1, cp2)
        self.wait(1)
        self.play(Uncreate(rule_body_g), Uncreate(rule_head_g), *[e.animate.set_color(WHITE) for e in highlight_edges])
        self.wait(90.15 - self.time)

        #Each possible completion is called a model
        query_g = abstract_query2()
        hom_query_model1 = Homomorphism(query_g, model1_g, [(varx, 'b'), (varry, 'c'), (vary, '{c}')], check_hom=True)
        hom_query_model2 = Homomorphism(query_g, model2_g, [(varx, 'b'), (vary, 'c'), (varry, 'c')], check_hom = False)
        query_g.move_to([0,2,0])
        query_cp1 = query_g.copy()
        query_cp2 = query_g.copy()
        self.play(Create(query_g), Transform(query_t, query_string_cp), run_time = 1)
        model1_not_q = MathTex('M_1\\not\\models q')
        model1_not_q.move_to([-width/2+margin+model1_not_q.width/2, model1_t.get_center()[1],0])
        model2_entails_q = MathTex('M_2\\models q')
        model2_entails_q.move_to([+width/2-margin-model2_entails_q.width/2, model2_t.get_center()[1],0])
        self.play(HomomorphismAnimation(query_cp1, hom_query_model1), ErrHomAnimation(query_cp2, hom_query_model2),
                  Succession(Transform(model1_t, model1_not_q, run_time=1), Wait(3, frozen_frame=False)),
                  Succession(Transform(model2_t, model2_entails_q, run_time=1), Wait(3, frozen_frame=False))
                  , run_time=4)
        not_entailed = Tex('$\\mathcal{R}, \\mathcal{D}$ {{$\\not\\models$}} $q$')
        not_entailed.submobjects[1].set_color(Style.err)
        not_entailed.add_background_rectangle(color=Style.err, buff=Style.bg_rect_buff, opacity=0, stroke_opacity=1, stroke_width=Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)
        not_entailed.move_to(query_g)
        self.play(model1_g.animate.set_color(Style.success), model2_g.animate.set_color(Style.err), FadeOut(query_g),FadeOut(query_cp1), FadeOut(query_cp2),FadeOut(query_t), FadeIn(not_entailed), FadeOut(model1_not_q), FadeOut(model2_entails_q),)
        self.wait(1)
        self.play(model1_g.animate.set_color(WHITE), model2_g.animate.set_color(WHITE))

        self.wait(98.3-self.time)
        self.play(FadeOut(*self.mobjects))
        self.wait(99.5-self.time)


    def play_2(self):
        #self.wait(99.5-self.time)
        height = (self.camera.frame_height)
        width = self.camera.frame_width
        margin = 0.5

        #Wait thats exactly not...
        chase_result_g = chase_result()
        chase_result_g.move_to([0,0,0]).shift([3.25,0,0])
        chase_result_e = get_univ_emojis(chase_result_g)

        query_g = allergic_query()
        query_g.move_to([0,0,0]).shift([-3,0,0])
        query_e = get_q_emojis(query_g)
        model_t = Style.create_heading('Model') 
        query_t = Style.create_heading('Query')
        model_t.move_to([chase_result_g.get_center()[0], height/2-margin-model_t.height/2,0])
        query_t.move_to([query_g.get_center()[0], height/2-margin-query_t.height/2,0])
        self.wait(99.6-self.time)
        self.play(FadeIn(chase_result_g), FadeIn(chase_result_e), FadeIn(query_g), FadeIn(query_e), Write(model_t), Write(query_t))
        self.wait(102.4-self.time)
        #FRESH ELEMENTS
        chase_result_g.suspend_updating()
        pop_sound(self, wait_time=.5)
        self.play(Indicate(chase_result_g.vertices['?'], color=Style.fresh_elem, scale_factor=1.5), run_time = 2)
        chase_result_g.resume_updating()
        #and only checked
        self.wait(104.5-self.time)
        query_g_cp = query_g.copy()
        query_e_cp = get_q_emojis(query_g_cp)
        self.add(query_g_cp, query_e_cp)
        hom_sound(self, duration=5)
        hom_query_chase_result = Homomorphism(query_g, chase_result_g, [('p', 'p'), ('k', 'k'), ('y', 'c')], check_hom=True)
        text = query_g_cp.edge_labels[("k", "y")]
        angle = text.submobjects[-1].get_angle()
        text.rotate(-angle)
        text_h = text.get_height()
        text.rotate(angle)
        
        def label_updater(mob, alpha):
            turn_point = 28/50
            diff = smooth(clip(abs(turn_point - alpha)* 3,0,1))
            angle = mob.submobjects[-1].get_angle()
            mob.rotate(-angle)
            mob.stretch_to_fit_height(text_h * diff)
            mob.rotate(angle)

        self.play(HomomorphismAnimation(query_g_cp,hom_query_chase_result), UpdateFromAlphaFunc(text,label_updater), run_time = 5)
        self.remove(query_g_cp, query_e_cp)
        self.wait(110.5-self.time)

        #but there were more models
        model1_g, model1_e, model2_g, model2_e, rule_body_g = more_kiki_models()
        model1_g.move_to(chase_result_g).shift([-6.75,-2,0])
        model1_g.update()
        model1_e.update()
        model2_g.move_to(chase_result_g).shift([-6.75,2,0])
        model2_g.update()
        model2_e.update()

        #THIS ONE
        self.play(FadeOut(query_g), FadeOut(query_e), FadeOut(query_t), FadeIn(model1_g), FadeIn(model1_e), run_time = 1.2)
        self.wait(112-self.time)
        models_t = Style.create_heading('Models').move_to(model_t)
        self.play(FadeIn(model2_g), FadeIn(model2_e), Transform(model_t, models_t), run_time=1.2)
        self.wait(116.1-self.time)

        #is called the chase
        model_t2 = Style.create_heading('Model').move_to(models_t)
        self.play(FadeOut(model2_g), FadeOut(model2_e), FadeOut(model1_g), FadeOut(model1_e), Transform(model_t, model_t2))
        the_chase_t = Style.create_heading('The Chase')
        chase_t = MathTex('\\mathsf{chase}(\\mathcal{R},\\mathcal{D})').move_to(model_t2)
        the_chase_t.move_to([-4,height/2-margin-the_chase_t.height/2,0])
        self.wait(122.4-self.time)
        self.play(Write(the_chase_t), Transform(model_t, chase_t))
        chase_explanation_t = MathTex('\\mathsf{chase}(\\mathcal{R}, \\mathcal{D})&\\models q\\\\\\text{implies \\qquad}\\mathcal{R},\\mathcal{D}&\\models q.', font_size=Style.explanation_font_size)
        chase_explanation_t.move_to([-4,1,0])
        self.wait(125.5-self.time)
        self.play(Write(chase_explanation_t))
        chase_explanation_tb = SurroundingRectangle(chase_explanation_t, color=Style.chase_expl_border, buff=Style.bg_rect_buff, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)
        self.play(Create(chase_explanation_tb))
        move_c = 5 #constant to move text out of frame
        self.wait(133.6-self.time)

        #Ahi I see
        self.wait(140-self.time)
        self.play(chase_explanation_t.animate.shift([0,move_c,0]), the_chase_t.animate.shift([0,move_c,0]), chase_explanation_tb.animate.shift([0,move_c,0]))
        self.wait(142-self.time)

        #take the body of a rule for example
        hom_rule_body_chase_result = Homomorphism(rule_body_g, chase_result_g, [('k', 'k'), ('?', '?')], check_hom=True)
        hom_chase_result_model1 = Homomorphism(chase_result_g, model1_g, [('p', 'p'), ('k', 'k'), ('b', 'b'), ('c', 'c'), ('?', '{c}')], check_hom=True)
        hom_rule_body_model1 = Homomorphism(rule_body_g, model1_g, [('k', 'k'), ('?', '{c}')], check_hom=True)

        rule_body_g.move_to(model2_g)
        rule_body_e = get_rule_emojis(rule_body_g)
        self.play(FadeIn(rule_body_g), FadeIn(rule_body_e), FadeIn(model1_g), FadeIn(model1_e))
        self.wait(144.5-self.time)

        rule_body_g_cp = rule_body_g.copy()
        rule_body_e_cp = get_rule_emojis(rule_body_g_cp)
        self.add(rule_body_g_cp, rule_body_e_cp)
        hom_sound(self, duration=148-self.time)
        self.play(HomomorphismAnimation(rule_body_g_cp, hom_rule_body_chase_result), run_time=148-self.time)
        self.remove(rule_body_g_cp, rule_body_e_cp)

        chase_result_g_cp = chase_result_g.copy()
        chase_result_e_cp = get_univ_emojis(chase_result_g_cp)
        self.add(chase_result_g_cp, chase_result_e_cp)
        hom_sound(self, duration=152.6-self.time)
        self.play(HomomorphismAnimation(chase_result_g_cp, hom_chase_result_model1), run_time=152.6-self.time)
        self.remove(chase_result_g_cp, chase_result_e_cp)

        rule_body_g_cp = rule_body_g.copy()
        rule_body_e_cp = get_rule_emojis(rule_body_g_cp)
        self.add(rule_body_g_cp, rule_body_e_cp)
        hom_sound(self, duration=156-self.time)
        self.play(HomomorphismAnimation(rule_body_g_cp, hom_rule_body_model1), run_time=156-self.time)
        self.remove(rule_body_g_cp, rule_body_e_cp)
        self.wait(157-self.time)

        #This means that even if the
        model2_g, model2_e = basil_model()
        self.play(FadeOut(rule_body_g), FadeOut(rule_body_e), FadeOut(model_t), FadeOut(model1_g), FadeOut(model1_e), FadeIn(model2_g), FadeIn(model2_e), FadeOut(chase_result_g),FadeOut(chase_result_e))
        self.wait(162.3-self.time)
        self.play(model2_g.animate.add_edges(('\\mathsf{contains}', ('p', 'b')), edge_config={'path_arc':-1}, label_config={'labelFontSize':36, 'labelOffset':0.2}), run_time=165.5-self.time)
        self.play(model2_g.animate.add_edges(('\\mathsf{contains}', ('b', 'c')), label_config={'labelFontSize':36, 'labelOffset':0.2}), run_time = 0.5*(172-self.time))
        self.play(model2_g.animate.add_edges(('\\mathsf{contains}', ('p', 'c')), edge_config={'path_arc':1}, label_config={'labelFontSize':36, 'labelOffset':0.2}), run_time = 172-self.time)
        self.wait(173-self.time)

        #Exactly:
        chase_result_g.move_to([0,0,0])
        chase_result_g.scale(1.2)
        for e in chase_result_e:
            e.scale(1.2)
        chase_result_e.update()
        self.play(FadeOut(model2_g), FadeOut(model2_e), FadeIn(chase_result_g), FadeIn(chase_result_e))
        sou = ImageMobject('assets/seal-of-universality.png').rotate(pi/6)
        sou.scale(0.25).move_to([-4,+2,0])
        seal_sound(self, wait_time=SEAL_PROP)
        self.play(FadeIn(sou, scale=2))
        self.wait(177-self.time)

        self.play(FadeOut(sou))
        self.play(ScaleInPlace(chase_result_g ,1/1.2, suspend_mobject_updating=False), ScaleInPlace(chase_result_e, 1/1.2, suspend_mobject_updating=False), FadeIn(chase_t))
        self.play(chase_result_g.animate.shift([3,0,0]))
        self.play(chase_explanation_t.animate.shift([0,-move_c,0]), the_chase_t.animate.shift([0,-move_c,0]), chase_explanation_tb.animate.shift([0,-move_c,0]))

        self.wait(186-self.time)
        self.play(FadeOut(the_chase_t), FadeOut(chase_explanation_t), FadeOut(chase_explanation_tb), FadeOut(chase_result_g), FadeOut(chase_result_e), FadeOut(chase_t))

