# This file contains the definitions of our used colors
# See Paul Tol's light color theme: https://sronpersonalpages.nl/~pault/


from manim import ManimColor, Tex
from manim.utils.color import WHITE

# _orange = ManimColor.from_hex("#EE7733")
# _cyan = ManimColor.from_hex("#33BBEE")
# _teal = ManimColor.from_hex("#009988")


_orange = ManimColor.from_hex("#EE7733")
_cyan = ManimColor.from_hex("#77AADD")
#_teal = ManimColor.from_hex("#BBCC33")
_teal = ManimColor.from_hex("#CCEE44")

err = _orange
success = _teal
text = WHITE

headings = _orange  # 8:53

logic = _cyan
logic2 = _teal
fresh_elem = _teal
predicate = _cyan

eval_border = _cyan
hom_border = _cyan
chase_expl_border = _teal

hom1 = _orange
hom2 = _teal
hom3 = _cyan

body = _orange
head = _teal

fair_border = _teal
univ_border = _orange

queue_pick = _cyan
checkmark = _teal
undecidable_border = _orange
termination_border = _orange
restricted_chase_border = _teal
finite_border = _orange
core_border = _teal

bij_yes = _teal
bij_no = _orange

check_highlight = _teal
expensive = _orange

app_ex_data = _cyan
chase_variants = _orange
core_conclusion = _cyan


# global variables used for styling
highlight_corner_radius = 0.0

bg_rect_buff = 0.2
bg_stroke_width = 3
bg_corner_radius = 0
explanation_font_size = 40
explanation_font_size_small = 30

def create_heading(text, font_size = 60):
    return Tex(r"\textsf{\textbf{" + text + r"}}", font_size=font_size)

