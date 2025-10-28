from manim import *
from stretch_sounds import *


POP_PROP=.61
POP_PROPrule2 =.82
POP_GAIN=-15

def pop_sound(scene:Scene,wait_time = 0,volume=POP_GAIN):
    scene.add_sound("./assets/pop.wav",time_offset=wait_time, gain=volume)

def bell_sound(scene:Scene,wait_time = 0,volume=-5):
    scene.add_sound("./assets/bell_sounds.wav",time_offset=wait_time, gain=volume)
    

def hom_sound(scene:Scene,wait_time = 0,volume=-10, duration=1.1):
    scene.add_sound(stretch_sound("assets/flute.wav", duration),time_offset=wait_time, gain=volume)

def trans_graph_table_sound(scene:Scene, wait_time = 0):
    scene.add_sound("assets/swoosh-05.wav", gain=-10, time_offset=wait_time)

def fail_sound(scene:Scene, wait_time = 0,volume=-10):
    scene.add_sound("./assets/wrong.wav", time_offset=wait_time, gain=volume)

def success_sound(scene:Scene, wait_time=0,volume=-20):
    scene.add_sound("./assets/correct.wav", time_offset=wait_time, gain=volume)

def meow(scene:Scene, wait_time= 0):
    scene.add_sound("./assets/meow.wav", time_offset=wait_time, gain=0)



SEAL_PROP=.2
def seal_sound(scene:Scene,wait_time = 0,volume=-5):
    scene.add_sound("./assets/stamp.wav",time_offset=wait_time, gain=volume)

def wow_sound(scene:Scene,wait_time = 0,volume=-10):
    scene.add_sound("./assets/wow.wav",time_offset=wait_time, gain=volume)
