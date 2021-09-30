import numpy as np
from manimlib import *


# from manimlib.once_useful_constructs.graph_scene import GraphScene


class Animate(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        self.play(ShowCreation(poly_graph))
        left_dot = Dot(color=RED)
        right_dot = Dot(color=RED)
        left_dot.move_to(axes.i2gp(2, poly_graph))
        right_dot.move_to(axes.i2gp(2, poly_graph))

        left_line = always_redraw(lambda: axes.get_v_line(left_dot.get_bottom()))
        right_line = always_redraw(lambda: axes.get_v_line(right_dot.get_bottom()))

        self.play(FadeIn(left_dot, scale=0.5), FadeIn(right_dot, scale=0.5))
        self.play(ShowCreation(left_line), ShowCreation(right_line))

        left_tracker = ValueTracker(2)
        right_tracker = ValueTracker(2)
        f_always(
            left_dot.move_to,
            lambda: axes.i2gp(left_tracker.get_value(), poly_graph)
        )
        f_always(
            right_dot.move_to,
            lambda: axes.i2gp(right_tracker.get_value(), poly_graph)
        )
        self.play(left_tracker.animate.set_value(1), right_tracker.animate.set_value(5), run_time=2)
        # self.embed()
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("Linear"))
        poly_label = axes.get_graph_label(poly_graph, Text("Poly"), x=4)
        left_dot.clear_updaters()
        right_dot.clear_updaters()
        self.play(ReplacementTransform(poly_graph, sin_graph), FadeIn(sin_label, RIGHT),
                  left_dot.animate.move_to(axes.i2gp(1, sin_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, sin_graph)))
        self.wait()
        self.play(ReplacementTransform(sin_graph, relu_graph), FadeTransform(sin_label, relu_label),
                  left_dot.animate.move_to(axes.i2gp(1, relu_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, relu_graph)))
        self.wait()
        poly_graph = axes.get_graph(
            self.poly_func,
            color=GREEN,
        )
        self.play(ReplacementTransform(relu_graph, poly_graph), FadeTransform(relu_label, poly_label),
                  left_dot.animate.move_to(axes.i2gp(1, poly_graph)),
                  right_dot.animate.move_to(axes.i2gp(5, poly_graph)))

        # self.play(left_tracker.animate.set_value(-2), right_tracker.animate.set_value(0), run_time=3)
        self.wait()
        dx_list = [1, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01]
        rects_list = VGroup(
            *[
                axes.get_riemann_rectangles(graph=poly_graph, x_range=[1, 5.01], stroke_width=0.05, stroke_color=GREEN, dx=dx)
                for dx in dx_list
            ]
        )
        first_approx = rects_list[0]
        self.play(Write(first_approx))
        for k in range(1, len(dx_list)):
            new_approx = rects_list[k]
            self.play(Transform(first_approx, new_approx), run_time = 1)
            self.wait(0.5)
        self.wait()

    def poly_func(self, x):
        return (x ** 3 - 5 * x ** 2 + 2 * x + 30) / 8
