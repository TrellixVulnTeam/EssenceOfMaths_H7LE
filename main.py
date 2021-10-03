import math

import numpy as np
from manimlib import *


# from manimlib.once_useful_constructs.graph_scene import GraphScene


class Animate(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8), axis_config={
            "include_tip": False,
        })
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        exp_sin_graph = axes.get_graph(
            lambda x: math.exp(math.sin(x)),
            color=YELLOW
        )
        exp_sin_graph_semi = axes.get_graph(
            lambda x: math.exp(0.5 * math.sin(x)),
            color=PURPLE
        )
        const_graph = axes.get_graph(
            lambda x: 3,
            color=ORANGE
        )
        self.play(ShowCreation(poly_graph))
        left_dot = Dot(color=RED)
        right_dot = Dot(color=RED)
        left_dot.move_to(axes.i2gp(3, poly_graph))
        right_dot.move_to(axes.i2gp(3, poly_graph))

        left_line = always_redraw(lambda: axes.get_v_line(left_dot.get_bottom()))
        right_line = always_redraw(lambda: axes.get_v_line(right_dot.get_bottom()))

        self.play(FadeIn(left_dot, scale=0.5), FadeIn(right_dot, scale=0.5))
        self.play(ShowCreation(left_line), ShowCreation(right_line))

        left_tracker = ValueTracker(3)
        right_tracker = ValueTracker(3)
        f_always(
            left_dot.move_to,
            lambda: axes.i2gp(left_tracker.get_value(), poly_graph)
        )
        f_always(
            right_dot.move_to,
            lambda: axes.i2gp(right_tracker.get_value(), poly_graph)
        )
        left_end = 2
        right_end = 6
        self.play(left_tracker.animate.set_value(left_end), right_tracker.animate.set_value(right_end), run_time=2)
        # self.embed()
        left_dot.clear_updaters()
        right_dot.clear_updaters()
        graph_list = [poly_graph, sin_graph, exp_sin_graph, exp_sin_graph_semi, const_graph]
        for i in range(len(graph_list) - 1):
            self.play(ReplacementTransform(graph_list[i], graph_list[i + 1]),
                      left_dot.animate.move_to(axes.i2gp(left_end, graph_list[i + 1])),
                      right_dot.animate.move_to(axes.i2gp(right_end, graph_list[i + 1])))
            self.wait()

        const_rect = axes.get_riemann_rectangles(const_graph, [left_end, right_end], dx=3.75, stroke_color=WHITE,
                                                 colors=(ORANGE, BLUE), fill_opacity=0.4)
        right_brace = Brace(const_rect, RIGHT)
        top_brace = Brace(const_rect, UP)
        right_brace_label = right_brace.get_text(
            "Height", font_size=24, gradient=(BLUE, GREEN)
        )
        top_brace_label = top_brace.get_text(
            "Width", font_size=24, gradient=(BLUE, GREEN)
        )
        in_label = Tex(r"\text{Area}=\text{Height}\times\text{Width}").scale(0.7)
        in_label.move_to(const_rect)
        self.play(GrowFromCenter(right_brace), Write(right_brace_label))
        self.play(GrowFromCenter(top_brace), Write(top_brace_label))
        self.play(Write(const_rect), Write(in_label))

        self.wait()
        self.play(
            *[FadeOut(x) for x in [const_rect, right_brace, right_brace_label, top_brace_label, top_brace, in_label]])
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        self.play(ReplacementTransform(const_graph, poly_graph),
                  left_dot.animate.move_to(axes.i2gp(left_end, poly_graph)),
                  right_dot.animate.move_to(axes.i2gp(right_end, poly_graph)))

        # self.play(left_tracker.animate.set_value(-2), right_tracker.animate.set_value(0), run_time=3)
        self.wait()
        dx_list = [1, 0.5, 0.25, 0.1, 0.05, 0.025]
        rects_list = VGroup(
            *[
                axes.get_riemann_rectangles(graph=poly_graph, x_range=[left_end, right_end + .01], stroke_width=0.05,
                                            stroke_color=GREEN,
                                            dx=dx, fill_opacity=0.6)
                for dx in dx_list
            ]
        )
        first_approx = rects_list[0]
        start_rect = first_approx[0]
        pieces = VGroup()
        for left_x in range(2, 6):
            y = poly_graph.underlying_function(left_x)
            line = Line(axes.c2p(left_x, y), axes.c2p(left_x + 1, y))
            line.set_stroke(color=YELLOW, opacity=0.7)
            pieces.add(line)
        self.play(ShowCreation(pieces), run_time=2)
        self.play(FadeIn(start_rect), run_time=1)

        f_brace = Brace(start_rect, LEFT, buff=0).set_color(YELLOW)
        dx_brace = Brace(start_rect, DOWN, buff=0).set_color(ORANGE)
        f_brace.label = f_brace.get_tex(r'f(x_1)', buff=0).scale(0.8).set_color(f_brace.get_color())
        dx_brace.label = dx_brace.get_tex(r'\Delta x').scale(0.8).set_color(dx_brace.get_color())

        area_in_text = Tex(r'A_1').move_to(start_rect).scale(0.7)
        show_area_text, a1, a2, a3, a4 = Tex(r'\text{Area}\approx ', '+A_1', '+A_2', '+A_3', '+A_4')
        area_tex_list = [show_area_text, a1, a2, a3, a4]
        for x in area_tex_list:
            x.scale(0.7)
        show_area_text.to_corner(UP)
        for i in range(0, len(area_tex_list) - 1):
            area_tex_list[i + 1].next_to(area_tex_list[i])
        self.play(*list(map(GrowFromCenter, [f_brace, dx_brace])),
                  *list(map(Write, [f_brace.label, dx_brace.label])),
                  FadeIn(area_in_text), FadeIn(show_area_text),
                  FadeInFromPoint(area_tex_list[1], area_in_text.get_center()))
        dx_brace_group = VGroup(dx_brace, dx_brace.label)
        last_brace = f_brace
        last_area_in_text = area_in_text
        for idx, rect in enumerate(first_approx[1:], 2):
            new_area_in_text = Tex(r'A_%d' % idx).move_to(rect).scale(0.7)
            f_next_brace = Brace(rect, LEFT, buff=0).set_color(f_brace.get_color())
            f_next_brace.label = f_next_brace.get_tex(r'f(x_%d)' % idx, buff=0).scale(0.8).set_color(
                f_brace.get_color())
            self.play(FadeIn(rect), dx_brace_group.animate.next_to(rect, DOWN, buff=0),
                      ReplacementTransform(last_brace, f_next_brace),
                      ReplacementTransform(last_brace.label, f_next_brace.label),
                      ReplacementTransform(last_area_in_text, new_area_in_text),
                      FadeInFromPoint(area_tex_list[idx], last_area_in_text.get_center())
                      )
            last_brace = f_next_brace
            last_area_in_text = new_area_in_text
        # for k in range(1, len(dx_list)):
        #     new_approx = rects_list[k]
        #     self.play(Transform(first_approx, new_approx), run_time=1)
        #     self.wait(0.5)
        self.wait()

    def poly_func(self, x):
        return ((x - 1) ** 3 - 5 * (x - 1) ** 2 + 2 * (x - 1) + 30) / 8
