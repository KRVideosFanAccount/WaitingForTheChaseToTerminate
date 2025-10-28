from manim import *
from manim.typing import *
from typing import Any, override
from functools import reduce
import operator as op


'''This class describes a DashedLine that supports recomputing the dashes and their length. We also override some methods regarding the tip such that these methods do not modify the start and end point.'''
class FlexibleDashedLine(DashedLine):

    def __init__(
        self,
        *args: Any,
        dash_length: float = DEFAULT_DASH_LENGTH,
        dashed_ratio: float = 0.5,
        **kwargs: Any,
    ) -> None:
        self.num_dashes = None #We have to set it to None first so get_end in the __init__ works
        self._last_update_start = [0,0,0]
        self._last_update_end = [0,0,0]
        self._last_update_path_arc = 0
        self._last_update_dashed_ratio = 0
        super().__init__(*args, dash_length=dash_length, dashed_ratio=dashed_ratio, **kwargs)
        self.dash_length = dash_length
        self.num_dashes = self._calculate_num_dashes()
        self.dashed_ratio = dashed_ratio
        self.update_dashes(force_recalculate=True)


    def add_tip(self,*args, **kwargs):
        r = super().add_tip(*args, **kwargs)
        return r

    def get_curve_functions(self, *args, **kwargs):
        if not (self.points is None or len(self.points) == 0):
            self.generate_points()
        ret = list(super().get_curve_functions(*args, **kwargs))
        self.clear_points()
        return ret

    def reset_endpoints_based_on_tip(self, *args, **kwargs):
        return self

    def put_start_and_end_on(self, start, end, *args, **kwargs):
        r = super().put_start_and_end_on(start, end, *args, **kwargs)
        self.start = self.submobjects[0].points[0].copy()
        self.end = self.submobjects[self.num_dashes-1].points[-1].copy()

        return r

    def set_points_by_ends(self, start: Point3DLike | Mobject, end: Point3DLike | Mobject, buff: float = 0, path_arc= None) -> None:
        if not path_arc:
            path_arc = self.path_arc
        ret = super().set_points_by_ends(start, end, buff, path_arc)
        if self.num_dashes and hasattr(self, 'submobjects') and len(self.submobjects) > 0:
            self._update_dashes()
        #elif self.num_dashes:
        #    self.update_dashes()
        return ret

    def set_path_arc(self, new_value:float):
        self.path_arc = new_value
        self.update_dashes()


    def get_end(self):
        if self.num_dashes:
            return self.submobjects[self.num_dashes-1].points[-1].copy()
        else:
            return self.end

    def get_start(self) -> Point3D:
        if hasattr(self, 'submobjects') and len(self.submobjects) > 0:
            return self.submobjects[0].points[0].copy()
        else:
            return super().get_start()

    def update_dashes(self, force_recalculate=False):
        self.start = self.get_start()
        self.end = self.get_end()
        self.generate_points()
        self._update_dashes(force_recalculate = force_recalculate)
        self.clear_points()

    def shift(self, vectors):
        total_vector = reduce(op.add, vectors)
        for mob in self.family_members_with_points():
            mob.points = mob.points.astype("float")
            mob.points += total_vector

        self._last_update_start += total_vector
        self._last_update_end += total_vector
        return self

    def _update_dashes(self, force_recalculate=False):
        start_diff = self.start - self._last_update_start
        end_diff = self.end - self._last_update_end

        #start and end moved the same; we can just move the dashes
        if all(abs(start_diff - end_diff) < 0.00001) and self._last_update_path_arc == self.path_arc and self._last_update_dashed_ratio == self.dashed_ratio and not force_recalculate:
            if not all(abs(start_diff)==0):
                for dash in self.submobjects:
                    dash.points = dash.points + start_diff

        else:
            if not len(self.points) == 0:

                dashes = DashedVMobject(
                    self,
                    num_dashes=self.num_dashes,
                    dashed_ratio=self.dashed_ratio,
                )
                for index in range(min(len(dashes), self.num_dashes)): # we have to take the min of _ and self.num_dashes since sometimes we get another dash. Probably if dashed_ratio is set to 1
                    self.submobjects[index].set_points_by_ends(dashes[index].get_start(), dashes[index].get_end())
                    self.submobjects[index].path_arc = dashes[index].path_arc
                    self.submobjects[index].points = dashes[index].points

        self._last_update_start = self.get_start()
        self._last_update_end = self.get_end()
        self._last_update_path_arc = self.path_arc
        self._last_update_dashed_ratio = self.dashed_ratio

class MarvinsPlayground(Scene):
    def construct(self):
        line = FlexibleDashedLine((-1, 0,0), (1,0,0))
        self.add(line)
        line2 = FlexibleDashedLine((-1, 0,0), (1,0,0))

        alpha = 0.5
        
        self.wait()
        
        for index in range(len(line2.submobjects)):
            sub_alpha = np.clip((alpha - (index / len(line2.submobjects))) * len(line2.submobjects))

            line.submobjects[index].pointwise_become_partial(line2.submobjects[index], 0, sub_alpha)
        self.wait()
        self.add(line)
        print(len(line.submobjects))
        #line.put_start_and_end_on((-1, 0,0), (1,0,0))
        self.wait()
        line2.add_tip(StealthTip())
        line.add_tip(StealthTip())

        alpha=1.0
        for index in range(len(line2.submobjects)):
            sub_alpha = np.clip((alpha - (index / len(line2.submobjects))) * len(line2.submobjects))

            line.submobjects[index].pointwise_become_partial(line2.submobjects[index], 0, sub_alpha)
        line.dashed_ratio = line2.dashed_ratio + alpha*(1-line2.dashed_ratio) + alpha*0.05
        line.update_dashes()
        line.set_opacity(0) 

        tip = line.get_tips()[0]
        line_fade_in = [line.animate(rate_function=rate_functions.smooth).set_stroke(WHITE, opacity=1.0)]
        tip_fade_in = tip.animate(rate_function=rate_functions.smooth).set_opacity(1.0)
        self.play(Succession(Succession(tip_fade_in, Indicate(tip)), AnimationGroup(line_fade_in )))
        
        
        line.set_stroke(WHITE, opacity = 0.5)
        self.wait()
        self.play(Indicate(tip)) 
        self.wait()
        alpha=0.5
        for index in range(len(line2.submobjects)):
            sub_alpha = np.clip((alpha - (index / len(line2.submobjects))) * len(line2.submobjects))

            line.submobjects[index].pointwise_become_partial(line2.submobjects[index], 0, sub_alpha)
        
        self.wait()
                
