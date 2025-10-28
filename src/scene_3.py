from PIL import Image
from manim import *
from Rules import *
from render_emoji import render_emoji_to_png
from bestDiGraph import BestDiGraph
from sound_effects import *

import Style

# turning up this number might fix some things but also increases compile time by a lot
# UPDATER_ITERATION = 10

def invLukas(y):
    if y < .5:
        return(pow((y/4.), 1./3.))
    else:
        return(1-(pow(-2*y+2, 1./3.)/2.))

class ChangeColor(Animation):

    def __init__(self, mobject, c1, c2,scale, rule=None, *args, **kwargs ):
        super().__init__(mobject, *args, **kwargs)
        self.c1 = c1
        self.c2 = c2
        self.scale = scale-1
        self.last_scale = 1
        self.rule = rule

    def interpolate(self, alpha):
        if self.c1 is not None and self.c2 is not None:
            self.mobject.set_color(interpolate_color(self.c1, self.c2, self.rate_func(alpha)))
        self.mobject.scale(1/self.last_scale)
        self.mobject.scale(1+self.rate_func(alpha)*self.scale)
        self.last_scale = 1+self.rate_func(alpha)*self.scale

    def clean_up_from_scene(self, scene: Scene) -> None:
        self.mobject.update()
        return super().clean_up_from_scene(scene)


class Queue:
    """
    A visual queue structure that displays elements vertically with separators.
    The freshest element is at the bottom and gets popped first.
    """
    def __init__(self, position=ORIGIN, width=1.5, height=4, max_elements=8):
        self.position = position
        self.width = width
        self.height = height
        self.max_elements = max_elements
        self.elements = []
        
        # Create the main queue box
        self.box = Rectangle(
            width=width, height=height,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.1
        ).move_to(position)
        
        # Create separators (horizontal lines)
        self.separators = []
        element_height = height / max_elements
        for i in range(1, max_elements):
            y_pos = position[1] + height/2 - i * element_height
            separator = Line(
                start=[position[0] - width/2, y_pos, 0],
                end=[position[0] + width/2, y_pos, 0],
                stroke_color=GRAY, stroke_width=1, stroke_opacity=0.5
            )
            self.separators.append(separator)
        
        # Create the queue group
        self.queue_group = VGroup(self.box, *self.separators)
        
        # Add a label
        self.label = Style.create_heading('Queue').move_to(
            position + UP * (height/2 + 0.5)
        )
        
    def add_element(self, element, scene=None):
        """
        Add an element to the queue (at the bottom).
        element should be a Manim object (like a small rule representation)
        """
        if len(self.elements) >= self.max_elements:
            print(f"Queue is full! Max elements: {self.max_elements}")
            return False
            
        # Calculate position for the new element
        element_height = self.height / self.max_elements
        y_pos = self.position[1] - self.height/2 + (len(self.elements) + 0.5) * element_height
        element.move_to([self.position[0], y_pos, 0])
        
        self.elements.append(element)
        
        if scene:
            scene.play(FadeIn(element, shift=UP * 0.3), run_time=0.5)
        else:
            return element
            
    def pop_element(self, scene=None):
        """
        Remove and return the freshest element (bottom of queue).
        """
        if not self.elements:
            print("Queue is empty!")
            return None
            
        element = self.elements.pop(0)  # Remove from bottom (index 0)
        
        # Animate the removal
        if scene:
            scene.play(
                element.animate.scale(0.8).set_color(RED).shift(DOWN * 0.5),
                run_time=0.3
            )
            scene.play(FadeOut(element), run_time=0.2)
            
            # Reposition remaining elements
            if self.elements:
                reposition_anims = []
                for i, elem in enumerate(self.elements):
                    element_height = self.height / self.max_elements
                    new_y = self.position[1] - self.height/2 + (i + 0.5) * element_height
                    reposition_anims.append(
                        elem.animate.move_to([self.position[0], new_y, 0])
                    )
                scene.play(*reposition_anims, run_time=0.5)
        else:
            return element
            
    def create_rule_representation(self, rule_name, rule_color=BLUE):
        """
        Create a small visual representation of a rule for the queue.
        """
        # Create a small rectangle with the rule name
        rule_rep = Rectangle(
            width=self.width * 0.8, height=self.height / self.max_elements * 0.6,
            fill_color=rule_color, fill_opacity=0.7,
            stroke_color=WHITE, stroke_width=1
        )
        
        # Add rule name text
        rule_text = Text(rule_name, font_size=16, color=WHITE)
        rule_text.move_to(rule_rep.get_center())
        
        return VGroup(rule_rep, rule_text)
        
    def get_all_objects(self):
        """Return all visual objects of the queue."""
        return VGroup(self.queue_group, self.label, *self.elements)
        
    def get_freshest_empty_position(self):
        """
        Return the position of the freshest empty cell (bottom-most available slot).
        Returns None if the queue is full.
        """
        if len(self.elements) >= self.max_elements:
            return None
            
        # Calculate position for the next element (bottom-most available slot)
        element_height = self.height / self.max_elements
        y_pos = self.position[1] - self.height/2 + (len(self.elements) + 0.5) * element_height
        
        return [self.position[0], y_pos, 0]
        
    def manual_add_element(self):
        """
        Manually increment the queue count without adding a visual element.
        Useful when you want to manually position objects in the queue.
        """
        if len(self.elements) < self.max_elements:
            # Add a placeholder to track the count
            self.elements.append(None)
            return True
        else:
            print(f"Queue is full! Max elements: {self.max_elements}")
            return False
            
    def manual_pop_element(self):
        """
        Manually decrement the queue count without removing a visual element.
        Useful when you want to manually remove objects from the queue.
        """
        if self.elements:
            self.elements.pop(0)  # Remove from bottom (index 0)
            return True
        else:
            print("Queue is empty!")
            return False
            
    def get_queue_count(self):
        """
        Return the current number of elements in the queue.
        """
        return len(self.elements)
        
    def is_full(self):
        """
        Check if the queue is full.
        """
        return len(self.elements) >= self.max_elements
        
    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return len(self.elements) == 0

# Alternative: Reusable checkmark function for your scenes
def create_animated_checkmark(color=Style.checkmark, stroke_width=8, scale=1):
    """
    Create a checkmark that can be easily added to any scene
    
    Args:
        color: Color of the checkmark (default: GREEN)
        stroke_width: Width of the stroke (default: 8)
        scale: Scale factor for the checkmark size (default: 1)
    
    Returns:
        VMobject: The checkmark object
    """
    points = [
        [-1, -0.3, 0],
        [-0.2, -1, 0],
        [1.2, 0.8, 0]
    ]
    
    checkmark = VMobject()
    checkmark.set_points_as_corners(points)
    checkmark.set_stroke(color, width=stroke_width)
    # Note: Line caps are handled automatically in most Manim versions
    checkmark.scale(scale)
    
    return checkmark

def rush_in_out(t):
    """
    Custom rate function that is fast at the beginning and end but slow in the middle.
    This is the inverse of a smooth ease function.
    
    Args:
        t: Time parameter between 0 and 1
        
    Returns:
        float: Transformed time value
    """
    # Use a sigmoid-like function that creates a plateau in the middle
    # We use 1 - smooth(abs(2*t - 1)) to create the rush effect
    middle_slowdown = 1 - rate_functions.smooth(abs(2*t - 1))
    
    # Blend with linear to ensure we still progress
    return 0.3 * t + 0.7 * middle_slowdown * t

def create_red_bowtie(center_point=ORIGIN, size=1.0):
    """Creates a red bowtie shape pointing upwards at the given coordinates."""
    s = size
    
    # Create bowtie wings
    left_wing = Polygon(
        [-0.8*s, 0.4*s, 0], [-0.2*s, 0.1*s, 0], 
        [-0.2*s, -0.1*s, 0], [-0.8*s, -0.4*s, 0],
        fill_color=RED, fill_opacity=0.8, stroke_color=RED_D, stroke_width=2
    )
    
    right_wing = Polygon(
        [0.8*s, 0.4*s, 0], [0.2*s, 0.1*s, 0], 
        [0.2*s, -0.1*s, 0], [0.8*s, -0.4*s, 0],
        fill_color=RED, fill_opacity=0.8, stroke_color=RED_D, stroke_width=2
    )
    
    # Center knot and highlights
    center_knot = Rectangle(
        width=0.3*s, height=0.4*s,
        fill_color=RED_D, fill_opacity=0.9, stroke_color=RED_E, stroke_width=2
    )
    
    highlights = VGroup(
        Line([-0.7*s, 0.3*s, 0], [-0.3*s, 0.05*s, 0], color=WHITE, stroke_width=1, stroke_opacity=0.6),
        Line([0.7*s, 0.3*s, 0], [0.3*s, 0.05*s, 0], color=WHITE, stroke_width=1, stroke_opacity=0.6)
    )
    
    return VGroup(left_wing, right_wing, center_knot, highlights).move_to(center_point)


def wrap_digraph_as_present(digraph, wrapping_color=BLUE, ribbon_color=GOLD, bowtie_scale=0.8):
    """Creates wrapping paper around a digraph with a bowtie on top."""
    # Get dimensions and center
    bounding_rect = SurroundingRectangle(digraph, buff=0)
    padding = 0.5
    box_width = bounding_rect.width + 2 * padding
    box_height = bounding_rect.height + 2 * padding
    center = digraph.get_center()
    
    # Create wrapping components
    wrapping_paper = Rectangle(
        width=box_width, height=box_height,
        fill_color=wrapping_color, fill_opacity=0.2,
        stroke_color=interpolate_color(wrapping_color, BLACK, 0.5), stroke_width=4
    ).move_to(center)
    
    ribbon_config = {
        "fill_color": ribbon_color, "fill_opacity": 0.7,
        "stroke_color": interpolate_color(ribbon_color, BLACK, 0.5), "stroke_width": 2
    }
    
    horizontal_ribbon = Rectangle(width=box_width + 0.2, height=0.2, **ribbon_config).move_to(center)
    vertical_ribbon = Rectangle(width=0.2, height=box_height + 0.2, **ribbon_config).move_to(center)
    
    # Position bowtie on top
    bowtie_position = center + UP * (box_height/2 + 0.1)
    bowtie = create_red_bowtie(bowtie_position, bowtie_scale)
    
    return VGroup(wrapping_paper, horizontal_ribbon, vertical_ribbon, bowtie)

def apply_r1_multiple_times(database, scene, first_body_vertex, second_body_vertex, new_element_index, num_applications, rule, rule_loop_animation, apply=True, shorter_animation=False, relative_positions={'z': ('y', (2,0,0))}):
    """
    Apply rule r1 multiple times by creating multiple db.apply_rule calls and generating animations.
    
    Args:
        database: The database graph to apply the rule to
        scene: The scene to add animations to
        first_body_vertex: The first vertex for the body homomorphism
        second_body_vertex: The second vertex for the body homomorphism
        new_element_index: The starting index for naming new vertices (e.g., 2 for z2, z3, etc.)
        num_applications: Number of times to apply the rule
        rule: The rule to apply (r1)
        rule_loop_animation: The RuleLoopAnimation instance for the rule (ra1)
        apply: Whether to actually apply the rule or just show the mapping (default: True)
    
    Returns:
        list: List of animations to be played
    """
    anims_to_play = []
    
    current_first = first_body_vertex
    current_second = second_body_vertex
    
    for i in range(num_applications):
        # Calculate the new vertex name
        new_vertex = f'z{new_element_index + i}'
        
        # Create body and head homomorphisms
        body_hom = [('x', current_first), ('y', current_second)]
        head_hom = [('y', current_second), ('z', new_vertex)]
        
        # Apply the rule and get animations
        (_, anims) = database.apply_rule(
            rule=rule,
            rule_loop_animation=rule_loop_animation,
            body_hom=body_hom,
            head_hom=head_hom,
            scene=scene,
            synchronous_rules=False,
            relative_positions=relative_positions,
            apply=apply,
            shorter_animation=shorter_animation
        )
        
        anims_to_play.append(anims)
        
        # Update for next iteration
        current_first = current_second
        current_second = new_vertex
    
    return anims_to_play

def apply_r2_multiple_times(database, scene, first_body_vertex, second_body_vertex, third_body_vertex, num_applications, rule, rule_loop_animation, apply=True, shorter_animation=False):
    """
    Apply rule r2 multiple times by creating multiple db.apply_rule calls and generating animations.
    
    Args:
        database: The database graph to apply the rule to
        scene: The scene to add animations to
        first_body_vertex: The first vertex for the body homomorphism (x)
        second_body_vertex: The second vertex for the body homomorphism (y)
        third_body_vertex: The third vertex for the body homomorphism (z)
        num_applications: Number of times to apply the rule
        rule: The rule to apply (r2)
        rule_loop_animation: The RuleLoopAnimation instance for the rule (ra2)
        apply: Whether to actually apply the rule or just show the mapping (default: True)
    
    Returns:
        list: List of animations to be played
    """
    anims_to_play = []
    
    current_first = first_body_vertex
    current_second = second_body_vertex
    current_third = third_body_vertex
    
    for i in range(num_applications):
        # Create body and head homomorphisms
        body_hom = [('x', current_first), ('y', current_second), ('z', current_third)]
        head_hom = [('z', current_third), ('y', current_second)]
        
        # Apply the rule and get animations
        (_, anims) = database.apply_rule(
            rule=rule,
            rule_loop_animation=rule_loop_animation,
            body_hom=body_hom,
            head_hom=head_hom,
            scene=scene,
            apply=apply,
            shorter_animation=shorter_animation,
            synchronous_rules=False
        )
        
        anims_to_play.append(anims)
        
        # Update for next iteration
        # Extract number from current_third (e.g., "z1" -> 1)
        if current_third.startswith('z'):
            current_number = int(current_third[1:])
            next_vertex = f'z{current_number + 1}'
        else:
            # raise an error
            raise ValueError(f"Current third vertex {current_third} does not follow the expected format 'z1', 'z2', etc.")
        
        current_first = current_second
        current_second = current_third
        current_third = next_vertex
    
    return anims_to_play

def apply_r1_and_r2_multiple_times(database, scene, first_body_vertex, second_body_vertex, third_body_vertex, new_element_index, num_applications, rule1, rule2, rule_loop_animation1, rule_loop_animation2, apply=True):
    """
    Apply rule r1 and r2 alternately multiple times by creating multiple db.apply_rule calls and generating animations.
    
    Args:
        database: The database graph to apply the rules to
        scene: The scene to add animations to
        first_body_vertex: The first vertex for the body homomorphism (x)
        second_body_vertex: The second vertex for the body homomorphism (y)
        third_body_vertex: The third vertex for the body homomorphism (z)
        new_element_index: The starting index for naming new vertices (e.g., 2 for z2, z3, etc.)
        num_applications: Number of times to apply the rule pair (r1 then r2)
        rule1: The first rule to apply (r1)
        rule2: The second rule to apply (r2)
        rule_loop_animation1: The RuleLoopAnimation instance for rule1 (ra1)
        rule_loop_animation2: The RuleLoopAnimation instance for rule2 (ra2)
        apply: Whether to actually apply the rules or just show the mapping (default: True)
    
    Returns:
        list: List of animations to be played
    """
    anims_to_play = []
    
    current_first = first_body_vertex
    current_second = second_body_vertex
    current_third = third_body_vertex
    
    for i in range(num_applications):
        # Calculate the new vertex name for r1
        new_vertex_r1 = f'z{new_element_index + 1*i}'
        
        # Apply r1 first
        body_hom_r1 = [('x', current_second), ('y', current_third)]
        head_hom_r1 = [('y', current_third), ('z', new_vertex_r1)]
        
        (_, anims_r1) = database.apply_rule(
            rule=rule1,
            rule_loop_animation=rule_loop_animation1,
            body_hom=body_hom_r1,
            head_hom=head_hom_r1,
            scene=scene,
            relative_positions={'z': ('y', (2, 0, 0))},
            apply=apply,
            shorter_animation=True,
            synchronous_rules=False
        )
        
        anims_to_play.append(anims_r1)
        
        # Apply r2 using the three vertices from the previous step
        body_hom_r2 = [('x', current_first), ('y', current_second), ('z', current_third)]
        head_hom_r2 = [('z', current_third), ('y', current_second)]
        
        (_, anims_r2) = database.apply_rule(
            rule=rule2,
            rule_loop_animation=rule_loop_animation2,
            body_hom=body_hom_r2,
            head_hom=head_hom_r2,
            scene=scene,
            apply=apply,
            shorter_animation=True,
            synchronous_rules=False
        )
        
        anims_to_play.append(anims_r2)
        
        # Update for next iteration
        current_first = current_second
        current_second = current_third
        current_third = new_vertex_r1
    
    return anims_to_play

def create_vibration_animation(digraph, amplitude=0.15, frequency=20, direction=UP, distance=0.2):
    """
    Creates vibration animations for all vertices and edges in a digraph.
    
    Args:
        digraph: The BestDiGraph to create vibrations for
        amplitude: The amplitude of the vibration (default: 0.15)
        frequency: The frequency of the vibration (default: 20)
        direction: The direction to vibrate in (default: UP)
        distance: The distance to shift (default: 0.2)
    
    Returns:
        list: List of vibration animations
    """
    vibration_animations = []
    
    # Vibrate each vertex
    for vertex in digraph.vertices.values():
        vibration_animations.append(
            vertex.animate(rate_func=lambda t: np.sin(frequency * t) * amplitude).shift(direction * distance)
        )
    
    # Vibrate each edge
    for edge in digraph.edges.values():
        vibration_animations.append(
            edge.animate(rate_func=lambda t: np.sin(frequency * t) * amplitude).shift(direction * distance)
        )
    
    return vibration_animations

def create_rule_highlight_square(rule_body, color=Style.queue_pick, buff=0.3):
    """
    Creates a yellow highlighting square around a rule body.
    
    Args:
        rule_body: The rule body to highlight
        color: The color of the highlight (default: YELLOW)
        buff: The buffer space around the rule (default: 0.3)
    
    Returns:
        Rectangle: The highlighting square
    """
    return SurroundingRectangle(
        rule_body, 
        buff=buff, 
        color=color, 
        stroke_width=1.5,
        stroke_opacity=0.6
    )

def create_rule1():
    vert_body1 = ['x', 'y']
    edge_body1 = [('p', 'x', 'y')]
    body1 = BestDiGraph(vert_body1, edge_body1, layout={'x': [0, 0, 0], 'y': [2, 0, 0]}).shift([-5, 1.8, 0])

    vert_head1 = ['y', 'z']
    edge_head1 = [('p', 'y', 'z')]
    head1 = BestDiGraph(vert_head1, edge_head1, 
                       layout={'y': [2, 0, 0], 'z': [4, 0, 0]}, 
                       edge_type=FlexibleDashedLine,
                       edge_config={"path_arc": 1.0}).shift([-5, 1.8, 0])
    r1 = Rule(body1, head1).align_head()
    return (body1, head1, r1)


def create_rule2():
    vert_body2 = ['x', 'y', 'z']
    edge_body2 = [('p', 'x', 'y'), ('p', 'y', 'z')]
    body2 = BestDiGraph(vert_body2, edge_body2, layout={'x': [0, 0, 0], 'y': [2, 0, 0], 'z': [4, 0, 0]}).shift([1, 1.8, 0])
    vert_head2 = ['y', 'z']
    edge_head2 = [('p', 'z', 'y')]
    head2 = BestDiGraph(vert_head2, edge_head2, 
                        layout={'y': [2, 0, 0], 'z': [4, 0, 0]}, 
                        edge_type=FlexibleDashedLine,
                        edge_config={("z","y"):{"path_arc": 2}}).shift([1, 1.8, 0])
    r2 = Rule(body2, head2).align_head()
    return (body2, head2, r2)

rule_heading_offset = 1.4*UP


class Scene3_part1(MovingCameraScene):
    def construct(self):
        self.add_sound("../recordings/Final/Scene3-final-part1.flac")
        weird_time_offset = 1

        width = self.camera.frame_width
        height = self.camera.frame_height
        margin = 0.5

        (body1, head1, r1) = create_rule1()
        (body2, head2, r2) = create_rule2()
        

        # rules as mathtex - split into parts for highlighting
       #r1_parts = [
       #    MathTex('p'), MathTex('('), MathTex('x'), MathTex(','), MathTex('y'), MathTex(')'),
       #    MathTex(r'\rightarrow'),
       #    MathTex('p'), MathTex('('), MathTex('y'), MathTex(','), MathTex('z'), MathTex(')')
       #]
        r1_tex = MathTex('p', '(', 'x', ',', 'y', ')', '\\rightarrow\\exists z\\ ', 'p', '(', 'y', ',', 'z', ')')
        r1_parts = r1_tex.submobjects
        r1_syntax = r1_tex.move_to(body1.vertices['y'].get_center())
        
        #r2_parts = [
        #    MathTex('p'), MathTex('('), MathTex('x'), MathTex(','), MathTex('y'), MathTex(')'),
        #    MathTex(r'\land'),
        #    MathTex('p'), MathTex('('), MathTex('y'), MathTex(','), MathTex('z'), MathTex(')'),
        #    MathTex(r'\rightarrow'),
        #    MathTex('p'), MathTex('('), MathTex('z'), MathTex(','), MathTex('y'), MathTex(')')
        #]
        r2_tex = MathTex('p', '(', 'x', ',', 'y', ')', '\\land', 'p', '(', 'y', ',', 'z',')', '\\rightarrow', 'p', '(', 'z', ',', 'y', ')')
        r2_parts = r2_tex.submobjects
        r2_syntax =r2_tex.move_to(body2.get_center())

        # hightlight every 'p' in both rules
        # Get all 'p' characters from both equations and indicate them
        p_indicators = []
        
        # Find 'p' in r1_parts (indices 0 and 7)
        p_indicators.append(Indicate(r1_parts[0], color=Style.predicate))
        p_indicators.append(Indicate(r1_parts[7], color=Style.predicate))
        
        # Find 'p' in r2_parts (indices 0, 7, and 14)
        p_indicators.append(Indicate(r2_parts[0], color=Style.predicate))
        p_indicators.append(Indicate(r2_parts[7], color=Style.predicate))
        p_indicators.append(Indicate(r2_parts[14], color=Style.predicate))

        # 2. "The Chase" from previous scene fades out
        # TODO: use "The Chase" label from previous scene
        # chase_title = Text("The Chase (placeholder)", font_size=32, color=YELLOW).shift(UP * 2.5)
        # self.add(chase_title)

        config_rule = {"opacity": False, 
                  "position": False, 
                  "scale": False}

        
        bellparent = VGroup(MathTex(r'\cdot'))
        bell = Emoji(r'\cdot', ('🔔', "bell.png", None) , bellparent, update_config=config_rule, scale_factor = 12)
        bell.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    
        ownerparent = VGroup(MathTex(r'\cdot'))
        owner = Emoji(r'\cdot', ('🧙', "owner.png", None) , ownerparent, update_config=config_rule, scale_factor = 12)
        owner.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        appparent = VGroup(MathTex(r'\cdot'))
        app = Emoji(r'\cdot', ('🧑‍🎓', "vampire.png", None) , appparent, update_config=config_rule, scale_factor = 12)
        app.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        
        vampireparent = VGroup(MathTex(r'\cdot'))
        vampire = Emoji(r'\cdot', ("🧛🏻", "vampire.png", None) , vampireparent, update_config=config_rule, scale_factor = 12)
        vampire.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])

        bell_sound(self)
        # self.add_sound("../assets/bell_sounds.flac")
        bell.move_to([width/2-margin-bell.width/2, height/2-margin-bell.height/2, 0])
        owner.move_to(2*DOWN+8*LEFT)
        app.move_to(2*DOWN+12*LEFT)
        vampire.move_to(2*DOWN+8*RIGHT)
        self.add(owner)
        self.play(FadeIn(bell, shift=2*LEFT), run_time = 1)
        self.play(owner.animate.move_to(2*DOWN+4*LEFT), app.animate.move_to(2*DOWN+5*LEFT),Succession(Rotate(bell, -PI/7,
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
                                     rate_func=rate_functions.ease_in_quad)), run_time=2)
        self.add(vampire)
        self.play(FadeOut(bell, shift=2*RIGHT), vampire.animate.move_to(2*DOWN+4*RIGHT))

        #self.play(FadeIn(door_frame), FadeIn(door), Create(door_handle), run_time=1)
        # Create door opening animation
       # door_left_edge = door.get_left()
       # handle_offset = door_handle.get_center() - door.get_center()
        
       # self.play(
       #     door.animate.scale([0.1, 1, 1]).move_to(door_left_edge + RIGHT * (door.width * 0.1 / 2)),
       #     door_handle.animate.scale([0.1, 1, 1]).move_to(door_left_edge + RIGHT * (door.width * 0.1 / 2) + handle_offset * [0.1, 1, 1]),
       #     run_time=2.5,
       #     rate_func=smooth
       # )
        #self.wait(1)
        # self.play(FadeOut(chase_title))

        #target_time = 7
        #self.wait(target_time-self.time)

        # add fair trade logo left of the fairness definition
        #alchemy_table = ImageMobject("assets/alchemy_table.png").scale(0.2)
        #alchemy_table.move_to(door_frame.get_center() + RIGHT * 0.1)
        #self.play(FadeIn(alchemy_table))

        self.wait(6-self.time)
        self.play(vampire.animate.shift(.5*UP), run_time=.2)
        self.play(vampire.animate.shift(.5*DOWN), run_time=.2)

        self.wait(8.7-self.time)

        self.play(vampire.animate.shift(.5*UP), run_time=.2)
        self.play(vampire.animate.shift(.5*DOWN), run_time=.2)


        self.wait(10.3-self.time)
        self.play(vampire.animate.shift(.5*UP), run_time=.2)
        self.play(vampire.animate.shift(.5*DOWN), run_time=.2)

        target_time = 11
        self.wait(target_time-self.time)
#        self.play(FadeOut(door_group), FadeOut(alchemy_table), run_time=1)

        # Create labels for the rules
        rule1_label = Style.create_heading('Rule 1').move_to(body1.vertices['y'].get_center() + rule_heading_offset)
        rule2_label = Style.create_heading('Rule 2').move_to(body2.get_center() + rule_heading_offset)

        # 1. Existential Rules Appear 
        self.play(FadeIn(r1_syntax, shift=DOWN), Write(rule1_label), run_time = 2)
        self.play(FadeIn(r2_syntax, shift=DOWN), Write(rule2_label), run_time = 2)
        
        # Play the indication animations
        target_time = 17.3
        self.wait(target_time-self.time)
        self.play(*p_indicators, run_time=2)

        self.wait(20-self.time)
        self.play(FadeOut(vampire), FadeOut(app), FadeOut(owner))
        
        target_time = 22.5
        self.wait(target_time-self.time)
        self.play(ReplacementTransform(r1_syntax, body1), ReplacementTransform(r2_syntax, body2))
        self.remove(r1_syntax, r2_syntax)
        self.add(head1)
        self.add(head2)

        ra1 = RuleLoopAnimation(r1)
        head1.add_updater(ra1.update_rule)

        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)

        # 3. Small database {p(a, b)} appears 
        # TODO: goofy effect
        db_x = -6
        db_y = -1
        db_z = 0
        db_verts = ['a', 'b']
        db_edges = [('p', 'a', 'b')]
        db = BestDiGraph(db_verts, db_edges, layout={'a': [db_x, db_y, db_z], 'b': [db_x+2, db_y, db_z]})
        db_label = Style.create_heading('Database').move_to(db.get_center() + UP * 1.25)

        target_time = 27.5
        self.wait(target_time-self.time)
        self.play(Create(db))

        target_time = 29.3
        self.wait(target_time-self.time)
        self.play(Write(db_label))

        target_time = 32.5
        self.wait(target_time-self.time)

        target_time = 34
        # 4.1 Apply the first rule once
        (_, anims) = db.apply_rule(rule=r1, 
                                rule_loop_animation=ra1, 
                                body_hom=[('x', 'a'), ('y', 'b')], 
                                head_hom=[('y', 'b'), ('z', 'z1')],
                                scene=self,
                                relative_positions={'z': ('y', (2,0,0))},
                                shorter_animation=True)
        
        pop_sound(self, wait_time=POP_PROP*(target_time-self.time))
        self.play(Succession(FadeOut(db_label), anims), run_time = target_time-self.time)

        # 4.2 Apply the first rule a second time
        target_time = 39
        (_, anims2) = db.apply_rule(rule=r1, 
                                rule_loop_animation=ra1, 
                                body_hom=[('x', 'b'), ('y', 'z1')], 
                                head_hom=[('y', 'z1'), ('z', 'z2')],
                                scene=self,
                                relative_positions={'z': ('y', (2,0,0))},
                                shorter_animation=True)
        pop_sound(self, wait_time =POP_PROP*(target_time-self.time))
        self.play(anims2, run_time = target_time-self.time)

        target_time = 41 + weird_time_offset
        self.wait(target_time-self.time)


        # 5.1 Short pause, second rule wiggles (eager to be appllied) but we immediately apply the first rule again
        target_time = 43
        self.play(Wiggle(body2), run_time = target_time-self.time)

        
        target_time = 44
        (_, anims3) = db.apply_rule(rule=r1, 
                                rule_loop_animation=ra1, 
                                body_hom=[('x', 'z1'), ('y', 'z2')], 
                                head_hom=[('y', 'z2'), ('z', 'z3')],
                                scene=self,
                                relative_positions={'z': ('y', (2,0,0))},
                                shorter_animation=True)
        pop_sound(self, wait_time =POP_PROP*(target_time-self.time))
        self.play(anims3,
        run_time = target_time-self.time)

        # and again
        target_time = 45
        (_, anims) = db.apply_rule(rule=r1, 
                                    rule_loop_animation=ra1, 
                                    body_hom=[('x', 'z2'), ('y', 'z3')], 
                                    head_hom=[('y', 'z3'), ('z', 'z4')],
                                    scene=self,
                                    relative_positions={'z': ('y', (2,0,0))},
                                    shorter_animation=True)
        pop_sound(self, wait_time =POP_PROP*(target_time-self.time))
        self.play(anims, run_time = target_time-self.time)

        # and again
        target_time = 45.5
        (_, anims) = db.apply_rule(rule=r1, 
                                    rule_loop_animation=ra1, 
                                    body_hom=[('x', 'z3'), ('y', 'z4')], 
                                    head_hom=[('y', 'z4'), ('z', 'z5')],
                                    scene=self,
                                    relative_positions={'z': ('y', (2,0,0))},
                                    shorter_animation=True)
        pop_sound(self, wait_time =POP_PROP*(target_time-self.time))
        self.play(anims, run_time = target_time-self.time)
        
        # 5.2 Apply Rule 1 multiple times in a loop
        anims_to_play = apply_r1_multiple_times(db, self, first_body_vertex='z4', second_body_vertex='z5', new_element_index=6, 
                                                num_applications=12, rule=r1, rule_loop_animation=ra1,
                                                shorter_animation=True)
        # Zoom out while playing the animations
        target_time = 68
        for i in range(12):
            pop_sound(self, wait_time=invLukas((i+POP_PROP)/12.)*(target_time-self.time), volume=POP_GAIN-3*i)

        self.play(
            Succession(*anims_to_play),
            self.camera.frame.animate.scale(1.35).move_to([db_x + 24, db_y, db_z]),
            run_time=target_time-self.time,
            rate_func=rate_functions.ease_in_out_cubic
        )
 
        # move rules out of view
        # body and label group
        body_and_label_1 = VGroup(body1, rule1_label)
        body_and_label_2 = VGroup(body2, rule2_label)
        body_and_label_1.shift(LEFT * 10)
        body_and_label_2.shift(LEFT * 10)

        
        
        # Create a subtle vibration effect for each component
        self.play(*create_vibration_animation(db), run_time=0.8)
        
        
        # 6. Gift wrap the database graph
        wrapped_present = wrap_digraph_as_present(db, BLUE, GOLD, 0.6)
        
        # Animate wrapping process
        target_time = 70.5
        self.play(FadeIn(wrapped_present[0]), # paper
                Create(wrapped_present[1]), # ribbons
                Create(wrapped_present[2]), # bowtie
                DrawBorderThenFill(wrapped_present[3]),
                self.camera.frame.animate.scale(1.4).move_to(db.get_center()),
                run_time=target_time-self.time)  
        

        
        # 7. Gift paper unwraps (optional), the second rule is not happy: it vibrates
        target_time = 73
        body1_taget_pos = db.get_center() + LEFT * 3.5 + UP * 2
        body2_taget_pos = db.get_center() + RIGHT * 3.5 + UP * 2
        self.play(FadeOut(wrapped_present[0]), # paper
                FadeOut(wrapped_present[1]), # ribbons
                FadeOut(wrapped_present[2]), # bowtie
                FadeOut(wrapped_present[3]),
                body1.animate.move_to(body1_taget_pos),
                body2.animate.move_to(body2_taget_pos),
                rule1_label.animate.move_to(body1_taget_pos-body1.get_center()+body1.vertices['y'].get_center() + rule_heading_offset),
                rule2_label.animate.move_to(body2_taget_pos + rule_heading_offset),
                self.camera.frame.animate.scale(0.7).move_to(db.get_center()),
                run_time=target_time-self.time)
            
            
        self.play(Wiggle(body2, n_wiggles=8, run_time = 1.6))
        target_time = 75.3
        head1.remove_updater(ra1.update_rule)
        head1.remove_updater(r1.align_head)
        head2.remove_updater(ra2.update_rule)
        head2.remove_updater(r2.align_head)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=target_time-self.time)
        self.clear()
        # remove all objects from scene

        # 8. Reset to the starting database, apply the first rule, animate the body of the second one mapping but don’t apply it.
        # TODO: copy second scene here?



class Scene3_part2(MovingCameraScene):
    def construct(self):
        self.add_sound("../recordings/Final/Scene3-final-part2.flac")
        
        (body1, head1, r1) = create_rule1()
        (body2, head2, r2) = create_rule2()
        # Create labels for the rules
        rule1_label = Style.create_heading('Rule 1').move_to(body1.vertices['y'].get_center()+ rule_heading_offset)
        rule2_label = Style.create_heading('Rule 2').move_to(body2.get_center() + rule_heading_offset)

        db_x = -6
        db_y = -1
        db_z = 0
        db_verts = ['a', 'b']
        db_edges = [('p', 'a', 'b')]
        db = BestDiGraph(db_verts, db_edges, layout={'a': [db_x, db_y, db_z], 'b': [db_x+2, db_y, db_z]})
        
        db_label = Style.create_heading('Database').move_to(db.get_center() + UP * 1.25)

       
        # 8. Reset to the starting database
        target_time = 1
        self.play(FadeIn(body1), FadeIn(body2), FadeIn(rule1_label), FadeIn(rule2_label), FadeIn(db), FadeIn(db_label), shift=RIGHT, run_time=target_time-self.time)
        self.add(head1)
        self.add(head2)
        ra1 = RuleLoopAnimation(r1)
        head1.add_updater(ra1.update_rule)

        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)


        # Apply the 1st rule once
        target_time = 1.5
        (_, anims) = db.apply_rule_no_succession(rule=r1, 
                                   rule_loop_animation=ra1, 
                                   body_hom=[('x', 'a'), ('y', 'b')], 
                                   head_hom=[('y', 'b'), ('z', 'z1')],
                                   synchronous_rules=False,
                                   scene=self,
                                   relative_positions={'z': ('y', (2,0,0))},
                                                 shorter_animation=True)
        pop_sound(self, wait_time =POP_PROP*(target_time-self.time), volume=POP_GAIN)
        self.play(Succession(FadeOut(db_label), anims, run_time=target_time-self.time))

        # show how 2nd rule would map
        target_time = 3.3
        (_, anims2) = db.apply_rule(rule=r2, 
                                   rule_loop_animation=ra2, 
                                   body_hom=[('x', 'a'), ('y', 'b'), ('z', 'z1')], 
                                   head_hom=[('z', 'z1'), ('y', 'b')],
                                   scene=self,
                                   synchronous_rules=False, 
                                   apply=False)
        self.play(anims2, run_time=target_time-self.time) 
        
        # Apply 1st rule multiple times in a loop
        anims_to_play = apply_r1_multiple_times(db, self, first_body_vertex='b', second_body_vertex='z1', new_element_index=2, 
                                                 num_applications=12, rule=r1, rule_loop_animation=ra1, shorter_animation=True)

        # remove head2 from scene
        #head2.remove_updater(ra2.update_rule)
        #self.remove(head2)
        ra2.finish(0.65)
        
        # Zoom out while playing the animations
        target_time = 8
        r2.set_graph_opacity(r2.head_graph, 0, ignore_frontier=False)

        for i in range(12):
            pop_sound(self, wait_time=invLukas((i+POP_PROP)/12.)*(target_time-self.time), volume=POP_GAIN-3*i)
        self.play(
            Succession(*anims_to_play),
            self.camera.frame.animate.scale(1.35).move_to([db_x + 18, db_y, db_z]).set_color(RED),
            body2.animate.shift(RIGHT * 9).set_color(Style.err).scale(1.75),
            #head2.animate.set_color(RED),
            ChangeColor(head2,WHITE,Style.err,1.75, suspend_mobject_updating=False),
            ChangeColor(r2.head_graph,None, None, 1.75, suspend_mobject_updating=False),

            #ScaleInPlace(list(head2.edge_labels.items())[0][1], 1.75, suspend_mobject_updating=False),
            rule2_label.animate.shift(RIGHT * 9),

            # Wiggle(body2, n_wiggles=24),
            run_time=target_time-self.time,
            rate_func=rate_functions.ease_in_out_cubic
        )
        r2.set_graph_opacity(r2.head_graph,0, ignore_frontier=False)

        ra1.finish(0.65)
        target_time = 10.3
        self.play(Wiggle(body2), run_time=target_time-self.time)
        
        # go back to initial position, and add head2 back
        target_time = 11
        self.play(
            self.camera.frame.animate.scale(1/1.35).move_to([0, 0, 0]),
            body2.animate.shift(LEFT * 9).set_color(WHITE).scale(1/1.75),
            ChangeColor(head2, Style.err, WHITE,1/1.75, suspend_mobject_updating=False),
            ChangeColor(r2.head_graph,None, None,1/1.75, suspend_mobject_updating=False),

            #ScaleInPlace(list(head2.edge_labels.items())[0][1], 1/1.75, suspend_mobject_updating=False),
            rule2_label.animate.shift(LEFT * 9)
        )
#        self.add(head2)

#        head2.add_updater(ra2.update_rule)
        r2.set_graph_opacity(r2.head_graph,0, ignore_frontier=False)
        ra2.pause = False
        ra1.pause = False
        # map body of rule 2 on first three applicable spots
        target_time = 14.9
        anims_to_play = apply_r2_multiple_times(db, self, first_body_vertex='a', second_body_vertex='b', third_body_vertex='z1', 
                                                 num_applications=3, rule=r2, rule_loop_animation=ra2, apply=False)
        
        fail_sound(self, wait_time=0.8)
        fail_sound(self, wait_time=1.85)
        fail_sound(self, wait_time=2.9)
        self.play(Succession(*anims_to_play), run_time=target_time-self.time)
        
        # fade in a definition of fairness (If a rule can be applied, then it will be applied at some point) surrounded by a box
        fairness_definition = MathTex(r"{{\textbf{Fairness:}}}\text{A rule application cannot be postponed forever.}", font_size=Style.explanation_font_size, color=Style.text).shift(DOWN * 2.5 + RIGHT * 1.1)
        fairness_definition.set_color_by_tex(r"Fairness:", color=Style.fair_border)
        fairness_box = SurroundingRectangle(fairness_definition, buff=Style.bg_rect_buff, color=Style.fair_border, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)
        # add fair trade logo left of the fairness definition
        fair_trade_logo = ImageMobject("assets/fair_trade.png").scale(0.15)
        fair_trade_logo.move_to(fairness_box.get_left() + LEFT * 1.2)
        
        target_time = 19.7
        self.wait(target_time-self.time)

        target_time = 20.4
        self.play(FadeIn(fairness_definition, scale=0.5),
                  Create(fairness_box), run_time=target_time-self.time)
        # wow_sound(self)
        self.play(FadeIn(fair_trade_logo))
        
        # apply rule 2 for real 3 times
        target_time = 31.2
        
        anims_to_play = apply_r2_multiple_times(db, self, first_body_vertex='a', second_body_vertex='b', third_body_vertex='z1', 
                                                 num_applications=6, rule=r2, rule_loop_animation=ra2, apply=True)
        for i in range(6):
            pop_sound(self, wait_time=((i+POP_PROPrule2)/6.)*(target_time-self.time), volume=POP_GAIN-4*i)
        self.play(Succession(*anims_to_play), run_time=target_time-self.time)
        
        target_time = 33
        head1.remove_updater(ra1.update_rule)
        head1.remove_updater(r1.align_head)
        head2.remove_updater(ra2.update_rule)
        head2.remove_updater(r2.align_head)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=target_time-self.time)
        self.clear()




class Scene3_part3(MovingCameraScene):
    def construct(self):
        self.add_sound("../recordings/Final/Scene3-final-part3.flac")
        

        (body1, head1, r1) = create_rule1()
        body1.shift([-1.5,0,0])
        head1.shift([-1.5,0,0])
        r1.head_graph.shift([-1.5,0,0])
        r1.align_head()
        (body2, head2, r2) = create_rule2()
        body2.shift([1.5,0,0])
        head2.shift([1.5,0,0])
        r2.head_graph.shift([1.5,0,0])
        r2.align_head()
        
        # Create labels for the rules
        rule1_label = Style.create_heading('Rule 1').move_to(body1.vertices['y'].get_center() + rule_heading_offset)
        rule2_label = Style.create_heading('Rule 2').move_to(body2.get_center() + rule_heading_offset)
        
        body_and_label_1 = VGroup(body1, rule1_label)
        body_and_label_2 = VGroup(body2, rule2_label)

        db_x = -6
        db_y = -1
        db_z = 0
        db_verts = ['a', 'b']
        db_edges = [('p', 'a', 'b')]
        db = BestDiGraph(db_verts, db_edges, layout={'a': [db_x, db_y, db_z], 'b': [db_x+2, db_y, db_z]})
        
        db_label = Style.create_heading("Database").move_to(db.get_center() + UP * 1.25)
        
        # Create the queue between the two rules
        queue = Queue(position=[0, 1.5, 0], width=2, height=2.25, max_elements=4)
        
        # Reset to the starting database
        self.play(FadeIn(body1), FadeIn(body2), FadeIn(rule1_label), FadeIn(rule2_label), FadeIn(db), FadeIn(db_label), shift=RIGHT, run_time=0.5)
        self.add(head1)
        self.add(head2)
        ra1 = RuleLoopAnimation(r1)
        head1.add_updater(ra1.update_rule)

        ra2 = RuleLoopAnimation(r2)
        head2.add_updater(ra2.update_rule)

        # Add the queue to the scene
        self.play(FadeOut(db_label))

        # potential r1 application
        (_, anims) = db.apply_rule(r1, ra1, 
                body_hom = [('x', 'a'), ('y', 'b')], 
                head_hom = [('y', 'b'), ('z', 'z1')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                apply=False)
        db_copy = db.copy()
        self.add(db_copy)

        target_time = 4.8
        self.play(Succession(anims, FadeIn(queue.get_all_objects()), db_copy.animate.move_to(queue.get_freshest_empty_position()).scale(0.4)), run_time=target_time-self.time)
        queue.manual_add_element()


        # pop freshest element from queue (apply r1)
        (_, anims) = db.apply_rule(r1, ra1, 
                body_hom = [('x', 'a'), ('y', 'b')], 
                head_hom = [('y', 'b'), ('z', 'z1')], 
                scene=self, 
                hom_time=3/5 * abs((target_time-self.time)),
                introduction_time=2/5* abs((target_time-self.time)),
                relative_positions = {"z": ("y", (2, 0, 0))},
                shorter_animation=True)
        db_copy_highlight = create_rule_highlight_square(db_copy, buff=0.1)
        target_time = 8.2
        pop_sound(self, POP_PROP*(target_time-self.time))
        self.play(Indicate(db_copy, color=Style.queue_pick), FadeIn(db_copy_highlight), anims, run_time=target_time-self.time)
        self.play(FadeOut(db_copy), FadeOut(db_copy_highlight))
        queue.manual_pop_element()
        self.remove(db_copy)

        # potential r1 application again
        (_, anims) = db.apply_rule(r1, ra1, 
                body_hom = [('x', 'b'), ('y', 'z1')], 
                head_hom = [('y', 'z1'), ('z', 'z2')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                apply=False)
        db_copy_r1 = db.copy()
        db_copy_r1.remove_edges(*[e for e in db_copy_r1.edges if e not in [('b', 'z1')]])
        db_copy_r1.remove_vertices(*[v for v in db_copy_r1.vertices if v not in ['b', 'z1']])
        target_time = (13.7-8.2)/2 + 8.2
        self.play(Succession(anims, db_copy_r1.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), run_time=target_time-self.time)
        queue.manual_add_element()

        # potential r2 application
        (_, anims) = db.apply_rule(r2, ra2, 
                body_hom = [('x', 'a'), ('y', 'b'), ('z', 'z1')], 
                head_hom = [('z', 'z1'), ('y', 'b')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                apply=False)
        db_copy_r2 = db.copy()
        db_copy_r2.remove_edges(*[e for e in db_copy_r2.edges if e not in [('a', 'b'), ('b', 'z1')]])
        db_copy_r2.remove_vertices(*[v for v in db_copy_r2.vertices if v not in ['a', 'b', 'z1']])
        target_time = 13.7
        self.play(Succession(anims, db_copy_r2.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), run_time=target_time-self.time)
        queue.manual_add_element()

        # apply r1 (latest element in queue)
        (_, anims) = db.apply_rule(r1, ra1, 
                body_hom = [('x', 'b'), ('y', 'z1')], 
                head_hom = [('y', 'z1'), ('z', 'z2')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                shorter_animation=True)
        db_copy_r1_highlight = create_rule_highlight_square(db_copy_r1, buff=0.1)
        target_time = 14.7
        pop_sound(self, POP_PROP*(target_time-self.time))
        self.play(Indicate(db_copy_r1, color=Style.queue_pick), FadeIn(db_copy_r1_highlight), anims, run_time=target_time-self.time)
        self.play(FadeOut(db_copy_r1), FadeOut(db_copy_r1_highlight), db_copy_r2.animate.move_to(db_copy_r1.get_center()), run_time=1)
        queue.manual_pop_element()
        self.remove(db_copy_r1)

        # potential r1 application
        (_, anims) = db.apply_rule(r1, ra1, 
                body_hom = [('x', 'z1'), ('y', 'z2')], 
                head_hom = [('y', 'z2'), ('z', 'z3')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                apply=False)
        db_copy_r1 = db.copy()
        db_copy_r1.remove_edges(*[e for e in db_copy_r1.edges if e not in [('z1', 'z2')]])
        db_copy_r1.remove_vertices(*[v for v in db_copy_r1.vertices if v not in ['z1', 'z2']])
        self.play(Succession(anims, db_copy_r1.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), run_time=1.5)
        queue.manual_add_element()

        universal_text = Tex(r"The potentially infinite result of a fair chase is a ",  r"\textbf{universal model.}", font_size=Style.explanation_font_size, color=Style.text).shift(DOWN * 2.75)
        universal_text.set_color_by_tex(r'universal model.', color=Style.univ_border)
        universal_box = SurroundingRectangle(universal_text, buff=0.2, color=Style.univ_border, stroke_width = Style.bg_stroke_width, corner_radius=Style.bg_corner_radius)
        target_time = 18
        self.wait(target_time-self.time)
        target_time = 20.5

        # potential r2 application
        (_, anims) = db.apply_rule(r2, ra2, 
                body_hom = [('x', 'b'), ('y', 'z1'), ('z', 'z2')], 
                head_hom = [('z', 'z2'), ('y', 'z1')], 
                scene=self, 
                relative_positions = {"z": ("y", (2, 0, 0))},
                apply=False)
        
        db_copy_r22 = db.copy()
        db_copy_r22.remove_edges(*[e for e in db_copy_r22.edges if e not in [('b', 'z1'), ('z1', 'z2')]])
        db_copy_r22.remove_vertices(*[v for v in db_copy_r22.vertices if v not in ['b', 'z1', 'z2']])
        self.play(Succession(anims, db_copy_r22.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), 
        FadeIn(universal_text, scale=0.5), Create(universal_box), run_time=target_time-self.time)
        queue.manual_add_element()

        # apply r2
        (_, anims) = db.apply_rule(r2, ra2, 
                body_hom = [('x', 'a'), ('y', 'b'), ('z', 'z1')], 
                head_hom = [('z', 'z1'), ('y', 'b')], 
                scene=self, 
                hom_time=3/5,
                introduction_time=2/5,
                relative_positions = {"z": ("y", (2, 0, 0))},
                shorter_animation=True)
        db_copy_r2_highlight = create_rule_highlight_square(db_copy_r2, buff=0.1)
        pop_sound(self, POP_PROPrule2*1)
        self.play(Indicate(db_copy_r2, color=Style.queue_pick), FadeIn(db_copy_r2_highlight), anims, run_time = 1)
        self.play(FadeOut(db_copy_r2), FadeOut(db_copy_r2_highlight),
                  db_copy_r1.animate.move_to(db_copy_r2.get_center()),
                  db_copy_r22.animate.move_to(db_copy_r1.get_center()), run_time=0.5)
        queue.manual_pop_element()
        self.remove(db_copy_r2)

        # # apply r1
        # (_, anims) = db.apply_rule(r1, ra1, 
        #         body_hom = [('x', 'z1'), ('y', 'z2')], 
        #         head_hom = [('y', 'z2'), ('z', 'z3')], 
        #         scene=self, 
        #         relative_positions = {"z": ("y", (2, 0, 0))})
        # db_copy_r1_highlight = create_rule_highlight_square(db_copy_r1, buff=0.1)
        # self.play(Indicate(db_copy_r1), FadeIn(db_copy_r1_highlight), anims, run_time=1)
        # self.play(FadeOut(db_copy_r1), FadeOut(db_copy_r1_highlight),
        #           db_copy_r22.animate.move_to(db_copy_r1.get_center()), run_time=1)
        # queue.manual_pop_element()
        # self.remove(db_copy_r1)

        # # potential r1 application
        # (_, anims) = db.apply_rule(r1, ra1, 
        #         body_hom = [('x', 'z2'), ('y', 'z3')], 
        #         head_hom = [('y', 'z3'), ('z', 'z4')], 
        #         scene=self, 
        #         relative_positions = {"z": ("y", (2, 0, 0))},
        #         apply=False)
        # db_copy_r1 = db.copy()
        # db_copy_r1.remove_edges(*[e for e in db_copy_r1.edges if e not in [('z2', 'z3')]])
        # db_copy_r1.remove_vertices(*[v for v in db_copy_r1.vertices if v not in ['z2', 'z3']])
        # self.play(Succession(anims, db_copy_r1.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), run_time=1)
        # queue.manual_add_element()

        # # potential r2 application
        # (_, anims) = db.apply_rule(r2, ra2, 
        #         body_hom = [('x', 'z1'), ('y', 'z2'), ('z', 'z3')], 
        #         head_hom = [('z', 'z3'), ('y', 'z2')], 
        #         scene=self, 
        #         relative_positions = {"z": ("y", (2, 0, 0))},
        #         apply=False)
        # db_copy_r23 = db.copy()
        # db_copy_r23.remove_edges(*[e for e in db_copy_r23.edges if e not in [('z1', 'z2'), ('z2', 'z3')]])
        # db_copy_r23.remove_vertices(*[v for v in db_copy_r23.vertices if v not in ['z1', 'z2', 'z3']])
        # self.play(Succession(anims, db_copy_r23.animate.scale(0.4).move_to(queue.get_freshest_empty_position())), run_time=1)
        # queue.manual_add_element()

        # # r2 application
        # (_, anims) = db.apply_rule(r2, ra2, 
        #         body_hom = [('x', 'b'), ('y', 'z1'), ('z', 'z2')], 
        #         head_hom = [('z', 'z2'), ('y', 'z1')], 
        #         scene=self, 
        #         relative_positions = {"z": ("y", (2, 0, 0))})
        # db_copy_r22_highlight = create_rule_highlight_square(db_copy_r22, buff=0.1)
        # self.play(Indicate(db_copy_r22), FadeIn(db_copy_r22_highlight), anims, run_time=1)
        # self.play(FadeOut(db_copy_r22), FadeOut(db_copy_r22_highlight),
        #           db_copy_r1.animate.move_to(db_copy_r22.get_center()),
        #           db_copy_r23.animate.move_to(db_copy_r1.get_center()))
        # queue.manual_pop_element()
        # self.remove(db_copy_r22)

        # apply r1 and r2 alternately
        anims_to_play = apply_r1_and_r2_multiple_times(db, self, first_body_vertex='b', second_body_vertex='z1', third_body_vertex='z2', new_element_index=3,
                                                 num_applications=16, rule1=r1, rule2=r2, rule_loop_animation1=ra1, rule_loop_animation2=ra2, apply=True)
        self.play(FadeOut(queue.queue_group), FadeOut(queue.label), FadeOut(db_copy_r1), FadeOut(db_copy_r22), body_and_label_1.animate.shift(RIGHT*1.5), body_and_label_2.animate.shift(LEFT*1.5))
        target_time = 25.6
        for i in range(16):
            pop_sound(self, wait_time=((2*i+POP_PROP))/32.*(target_time-self.time), volume=POP_GAIN-3*i)
            pop_sound(self, wait_time=((2*i+1+POP_PROPrule2)/32.)*(target_time-self.time), volume=POP_GAIN-3*i)
        self.play(Succession(*anims_to_play),
                  universal_text.animate.shift(2*LEFT),
                  universal_box.animate.shift(2*LEFT),
                  self.camera.frame.animate.scale(1.2).shift(RIGHT*14),
                  run_time=target_time-self.time)

        target_time = 26.5
        camera_pos = self.camera.frame.get_center()
        self.play(body_and_label_1.animate.move_to(camera_pos + UP * 2 + LEFT * 5), 
        body_and_label_2.animate.move_to(camera_pos + UP * 2 + RIGHT * 4), run_time=target_time-self.time)
        
        # add fair trade logo left of the fairness definition
        universality_logo = ImageMobject("assets/seal-of-universality.png").scale(0.15)
        universality_logo.move_to(camera_pos + DOWN * 2.5 + LEFT * 3)

        fair_trade_logo = ImageMobject("assets/fair_trade.png").scale(0.15)
        fair_trade_logo.move_to(camera_pos + DOWN * 2.5 + RIGHT * 3)

        # Add green checkmarks next to the rules to show they are satisfied
        # Create checkmark for rule 1
        checkmark1 = create_animated_checkmark(color=Style.success, scale=0.3)
        checkmark1.next_to(rule1_label, RIGHT, buff=0.2)

        checkmark2 = create_animated_checkmark(color=Style.success, scale=0.3)
        checkmark2.next_to(rule2_label, RIGHT, buff=0.2)
        
        # Animate the checkmark appearing
        target_time = 27
        
        self.play(Create(checkmark1), Create(checkmark2), FadeIn(universality_logo, scale=2), run_time=target_time-self.time)
        seal_sound(self, wait_time=SEAL_PROP*(target_time-self.time)-.3)
        target_time = 29
        self.wait(target_time-self.time)

        target_time=30.5
        # wow_sound(self, wait_time=1)
        self.play(
            FadeIn(fair_trade_logo),
            run_time=target_time-self.time
        )

        target_time = 33
        head1.remove_updater(ra1.update_rule)
        head1.remove_updater(r1.align_head)
        head2.remove_updater(ra2.update_rule)
        head2.remove_updater(r2.align_head)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=target_time-self.time)
        self.clear()
