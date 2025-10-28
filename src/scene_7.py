from manim import *
from coolerDiGraph import *
from bestDiGraph import *
from database import *
from Homomorphism import * 
from Rules import *
from manim import *
from CQ import *
from sound_effects import *
from manim.animation.animation import prepare_animation


class SceneCredits(Scene):

    def construct(self):

    
        VERTSHIFT = .07

        writing = MathTex(r'\textrm{Writing}', font_size=25).move_to(3.2*UP)
        writters = MathTex(r'\textrm{Simon Hosemann} \qquad \textrm{Quentin Manière}', font_size=40).next_to(writing, 1.5*DOWN)
        
        
        animations = MathTex(r'\textrm{Animations}', font_size=25).next_to(writters, 3*DOWN)
        animator1 = MathTex(r'\textrm{Marvin Großer}', font_size=40).next_to(animations, 1.5*DOWN)
        animator0 = MathTex(r'\textrm{Matti Berthold}', font_size=40).next_to(animator1, LEFT).shift(1.3*LEFT).align_to(animator1, DOWN)
        animator2 = MathTex(r'\textrm{Simon Hosemann}', font_size=40).next_to(animator1, RIGHT).shift(1.3*RIGHT).align_to(animator1, DOWN)
        animators = Group(animator0, animator1, animator2)
        
        animator5 = MathTex(r'\textrm{Moritz Schönherr}', font_size=40).next_to(animators, 1.5*DOWN)
        animator4 = MathTex(r'\textrm{Quentin Manière}', font_size=40).next_to(animator0, 1.5*DOWN).align_to(animator5, UP)
        animator6 = MathTex(r'\textrm{Lukas Schulze}', font_size=40).next_to(animator2, 1.5*DOWN).align_to(animator5, DOWN)
        animators2 = Group(animator4, animator5, animator6)
        
        
        voice = MathTex(r'\textrm{Voices (by order of appearance)}', font_size=25).next_to(animations, 9*DOWN)
        
        voicer = MathTex(r'\textrm{Quentin Manière}', font_size=40).next_to(voice, 1.5*DOWN).shift(2*RIGHT)
        role = MathTex(r'\textsc{The Shopkeeper}', font_size=30).next_to(voice, DOWN).shift(2*LEFT).align_to(voicer, DOWN).shift(VERTSHIFT*UP)
        
        voicer2 = MathTex(r'\textrm{Simon Hosemann}', font_size=40).next_to(voicer, DOWN).align_to(voicer, LEFT).shift(VERTSHIFT*UP)
        role2 = MathTex(r'\textsc{The Apprentice}', font_size=30).next_to(voicer, DOWN).align_to(role, RIGHT).align_to(voicer2, DOWN)
        
        voicer3 = MathTex(r'\textrm{Marvin Großer}', font_size=40).next_to(voicer2, DOWN).align_to(voicer2, LEFT)
        role3 = MathTex(r'\textsc{The Vampire}', font_size=30).next_to(voicer2, DOWN).align_to(role2, RIGHT).align_to(voicer3, DOWN)
        
        voicer4 = MathTex(r'\textrm{Moritz Schönherr}', font_size=40).next_to(voicer3, DOWN).align_to(voicer3, LEFT)
        role4 = MathTex(r'\textsc{Mr Real-World}', font_size=30).next_to(voicer3, DOWN).align_to(role3, RIGHT).align_to(voicer4, DOWN)
        
        
        editing = MathTex(r'\textrm{Sound editing}', font_size=25).next_to(voice, 12.5*DOWN)
        editors = MathTex(r'\textrm{Simon Hosemann}', font_size=40).next_to(editing, 1.5*DOWN)
        
        
        
        # video = MathTex(r'\textrm{Final video editing}', font_size=25).next_to(editors, 3*DOWN)
        # videoers = MathTex(r'\textrm{Matti Berthold}', font_size=40).next_to(video, 1.5*DOWN)
        
        
        made_with = MathTex(r'\textrm{Animations created using}', font_size=25).next_to(editors, 3*DOWN)
        manim_cite = MathTex(r'\textrm{Manim: https://www.manim.community/}', font_size=30).next_to(made_with, 2*DOWN).shift(RIGHT)
        banner = ManimBanner().scale(.2).next_to(manim_cite, 1.5*LEFT)
        
        
        # affiliation1 = MathTex(r'\begin{array}{c}\textrm{Center for Scalable Data Analytics and Artificial Intelligence (ScaDS.AI),} \\ \textrm{Dresden/Leipzig} \end{array}', font_size=20).move_to(2.8*DOWN)
        # affiliation2 = MathTex(r' \textrm{Universität Leipzig}', font_size=20).next_to(affiliation1, DOWN)
        # affs = Group(affiliation1, affiliation2)
        
        made_with = MathTex(r'\textrm{Animations created using}', font_size=25).next_to(editors, 3.5*DOWN)
        
        
        copyr = MathTex(r'\textrm{Fair use of copyrighted material}', font_size=25).next_to(made_with, 6*DOWN)
        copyrights = MathTex(r'\textrm{Emojis by }\textsc{Apple Color Emoji}', font_size=30).next_to(copyr, 1.5*DOWN)
        copyrights1 = MathTex(r'\textrm{Doorbell chime by } \textsc{BBC Sound Effects}', font_size=30).next_to(copyrights, 1.5*DOWN)

        
        
        afftitle = MathTex(r'\textrm{Affiliations}', font_size=25).next_to(copyrights1, 3*DOWN)
        
        scads_logo = ImageMobject("assets/Scads-final.png").scale(.07)
        ul_logo = ImageMobject("assets/UL-final-cropped.png").scale(.1).next_to(scads_logo, LEFT).shift(.4*LEFT)
        secai_logo = ImageMobject("assets/secai.png").scale(.45).next_to(scads_logo, RIGHT).shift(.8*RIGHT)
        
        affiliations = Group(scads_logo, ul_logo, secai_logo).next_to(afftitle, .8*DOWN)
        
        
        note = MathTex(r'\textrm{No cats were harmed during the making of this video.}', font_size=25).next_to(affiliations, 2.5*DOWN)
        
        
        
        CREDITS = Group(
            writing,
            writters,
            animations,
            animators,
            animators2,
            made_with,
            manim_cite,
            banner,
            voice,
            voicer,
            role,
            voicer2,
            role2,
            voicer3,
            role3,
            voicer4,
            role4,
            editing,
            editors,
            # video,
            # videoers,
            copyr,
            copyrights,
            copyrights1,
            afftitle,
            affiliations,
            note
            ).move_to([0, 0 ,0])
        
        
        self.add(CREDITS)
        
        
        
        def setting_kiki(POSITION_KIKI=(0,0,0), col1="#000000", col2="#400040"):
            config_rule = {"opacity": False, 
                  "position": True, 
                  "scale": False}
            kiki_happy = VGroup(MathTex(r"\cdot")).move_to(POSITION_KIKI)
            kiki_happy.set_opacity(0)
            kiki_happy_emoji = Emoji(r"\cdot", ("😽", "kiki_happy.png", col2) ,kiki_happy, update_config=config_rule, scale_factor=18)
            kiki_sad = VGroup(MathTex(r"\cdot")).move_to(POSITION_KIKI)
            kiki_sad.set_opacity(0)
            kiki_sad_emoji = Emoji(r"\cdot", ("😽", "sad_cat.png", col1) ,kiki_sad, update_config=config_rule, scale_factor=18)
            antidote = VGroup(MathTex(r"\cdot")).move_to(POSITION_KIKI + .9*(LEFT+DOWN))
            antidote.set_opacity(0)
            antidote_emoji = Emoji(r"\cdot", ("💉", "antidote.png", None) ,antidote, update_config=config_rule, scale_factor=15)
            kiki_happy_emoji.set_z_index(20)

            kiki_sad_emoji.fade(1)
            kiki_happy_emoji.fade(1)
            antidote_emoji.fade(1)
            kiki_happy_emoji.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

            def newFade(mob, alpha):
                mob.fade(1 - alpha)
            anims = [Appear(antidote_emoji),
                     Appear(kiki_sad_emoji),
                     Appear(kiki_happy_emoji),
                AnimationGroup(UpdateFromAlphaFunc(antidote_emoji, newFade),
                     UpdateFromAlphaFunc(kiki_sad_emoji, newFade)),
                prepare_animation(antidote.animate.shift(.15*(UP + RIGHT))),
                AnimationGroup(prepare_animation(antidote.animate.shift(.1*(DOWN + LEFT))), FadeOut(kiki_sad_emoji),UpdateFromAlphaFunc(kiki_happy_emoji,newFade)),
                AnimationGroup(Wiggle(kiki_happy_emoji),FadeOut(antidote_emoji)),
                AnimationGroup(FadeOut(kiki_happy_emoji))
                ]
            return(Succession(*anims, run_time=2))
        
        
        
        CREDITS.shift(13*DOWN).set_z_index(20)
        
        kiki1 = Succession(Wait(1), setting_kiki(1*UP + 1*RIGHT), Wait(17))
        kiki2 = Succession(Wait(4), setting_kiki(3*UP + 5*LEFT, col1="#400040", col2="#004000"), Wait(14))
        kiki3 = Succession(Wait(7), setting_kiki(1*DOWN + 5.5*RIGHT, col1="#004000", col2="#000040"), Wait(11))
        kiki4 = Succession(Wait(10), setting_kiki(2*DOWN + 5*LEFT, col1="#000040", col2="#404000"), Wait(8))
        kiki5 = Succession(Wait(13), setting_kiki(2*UP + 5.5*RIGHT, col1="#404000", col2="#400000"), Wait(5))
        kiki6 = Succession(Wait(16), setting_kiki(1*DOWN + 0*RIGHT, col1="#400000", col2="#000000"), Wait(2))
        
        POPWAIT = .6
        pop_sound(self, wait_time=1+POPWAIT)
        pop_sound(self, wait_time=4+POPWAIT)
        pop_sound(self, wait_time=7+POPWAIT)
        pop_sound(self, wait_time=10+POPWAIT)
        pop_sound(self, wait_time=13+POPWAIT)
        pop_sound(self, wait_time=16+POPWAIT)
        
        self.play(CREDITS.animate.shift(26*UP), kiki1, kiki2, kiki3, kiki4, kiki5, kiki6,
                     rate_func=rate_functions.linear, run_time=20)
            

        
        self.remove(CREDITS)

        
