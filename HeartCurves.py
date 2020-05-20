from manimlib.imports import *
import numpy as np

#TODO change VMobject to GraphScene
# class HeartCurve1(GraphScene):
#     CONFIG = {
#         "x_max": 6,
#         "x_min": -6,
#         "y_max": 2,
#         "y_min": -3,
#         "graph_origin": ORIGIN,
#         "x_labeled_nums": range(-7,7,2),
#         "y_labeled_nums": range(-3,2,1)
#     }
#     def construct(self):
        
#         grid = NumberPlane()
#         self.play(
#             ShowCreation(grid, run_time = 3, lag_ratio = 0.1)
#         )

#         self.setup_axes(animate = True)

class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))

# Plot screen grid
class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)

class LoveCurve1(VMobject):
    def generate_points(self):
        x_up = np.linspace(-2,2,4096)
        x_down = np.linspace(-2,2,4096)
        # print(x_up[-1])
        # print(x_down[-1])
        y_up = np.sqrt(2*np.sqrt(x_up**2)-x_up**2) 
        y_down = -2.14 * np.sqrt(np.sqrt(2) - np.sqrt(np.abs(x_down)))
        upper = np.vstack((x_up,y_up,np.zeros_like(x_up))).T  
        down = np.vstack((x_down, y_down,np.zeros_like(x_down))).T
        # print(upper.shape)
        # print(down.shape)
        self.points = np.concatenate((upper,down,upper[-256:]),axis=0) # adding up the last 256 points to fill up the gap of LOVE!!!
        # print(self.points.shape)

class LoveCurve2(VMobject):
    def generate_points(self):
        x_up = np.linspace(-2,2,4096)
        x_down = np.linspace(-2,2,4096)
        # print(x_up[-1])
        # print(x_down[-1])
        y_up = np.sqrt(2*np.sqrt(x_up**2)-x_up**2) 
        y_down = np.arcsin(np.abs(x_down)-1) - np.pi/2
        upper = np.vstack((x_up,y_up,np.zeros_like(x_up))).T  
        down = np.vstack((x_down, y_down,np.zeros_like(x_down))).T
        # print(upper.shape)
        # print(down.shape)
        self.points = np.concatenate((upper,down,upper[-256:]),axis=0) # adding up the last 256 points to fill up the gap of LOVE!!!
        # print(self.points.shape)

#TODO find a better way to show screen grid
class HeartCurve(Scene):
    CONFIG = {
        "curve1_color": PINK,
        "curve2_color": MAROON_C
    }
    def construct(self):
        title = TextMobject("Heart Curves").set_color(RED) \
                                            .to_corner(UL, LARGE_BUFF) \
                                            .scale(1.5)

        curve1 = LoveCurve1().set_color(self.curve1_color)
        curve1_tex_up = TexMobject(r"f(x)=\sqrt{2 \cdot \sqrt{x^{2}}-x^{2}}").move_to(3 * LEFT + 2 * UP) \
            .set_color(BLUE)
        curve1_tex_down = TexMobject(r"g(x)=-2.14 \cdot \sqrt{\sqrt{2}-\sqrt{|x|}}").move_to(4 * LEFT + 2 * DOWN) \
                    .set_color(YELLOW)

        curve2 = LoveCurve2().set_color(self.curve2_color)
        curve2_tex_down = TexMobject(r"g(x)=\sin ^{-1}(|x|-1)-\frac{\pi}{2}").move_to(curve1_tex_down) \
            .set_color(MAROON_B)

        grid = ScreenGrid()
        self.add(grid)

        self.play(
            Write(title)
        )
        self.wait()
        self.play(
            ShowCreation(curve1, run_time = 2, lag_ratio = 0.1),
        )
        self.wait()
        self.play(
            Write(curve1_tex_up),
            Write(curve1_tex_down),
        )
        self.wait()
        self.play(
            Transform(curve1,curve2),
            Transform(curve1_tex_down, curve2_tex_down),
        )
        self.wait()
        #TODO Simplify FadeOut
        self.play(
            FadeOut(curve1_tex_down),
            FadeOut(curve1_tex_up),
            FadeOut(curve1),
            FadeOut(title),
            FadeOut(grid),
        )

class SMBHB520(Scene):
    def  construct(self):
        title = TextMobject("Today's Thought").to_corner(UL) \
            .set_color(RED_C)
        s1 = TextMobject("A pair of lovers").set_color(GOLD_A)
        s2 = TextMobject("is like a Super Massive Black Hole Binary system,").set_color(GOLD_A)
        s3 = TextMobject("once they entangled with each other from the galaxy merger,").set_color(GOLD_B)
        s4 = TextMobject("their fate is decided.").set_color(GOLD_C)
        s5 = TextMobject("Throughout the interaction with each other,").set_color(GOLD_D)
        s6 = TextMobject("inspiraling, evolving and radiating.").set_color(GOLD_D)
        s7 = TextMobject("No one can escape the other's gravity").set_color(GOLD_E)
        s8 = TextMobject("and will end up with a coalescence, emitting enormous power:").set_color(GOLD_E)
        s9 = TextMobject("LOVE").set_color(RED_E)
        sentence = VGroup(s1,s2,s3,s4,s5,s6,s7,s8,s9).arrange(DOWN)
        self.play(
            Write(title),
        )
        self.wait()
        self.play(
            Write(sentence),
            run_time = 10
        )
