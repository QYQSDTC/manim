from manimlib.imports import *
import numpy as np

class LittleBaby(GraphScene):
    CONFIG ={
        "function": lambda x : np.sqrt(2*np.sqrt(x**2)-x**2),
        "function2": lambda x : -2.14 * np.sqrt(np.sqrt(2) - np.sqrt(np.abs(x))),
        "function_color": RED,
        "function_color2": BLUE,
       # "x_axis_width": 10,
        "x_min": -2,
        "x_max": 2,
        "x_tick_frequency": 0.5,
        "y_min": -3,
        "y_max": 1,
        "graph_origin": ORIGIN,
        "x_labeled_nums": range(-2,3,1)
    }
    def construct(self):
        self.setup_axes(animate=True)
        func_graph = self.get_graph(
            self.function,
            self.function_color
        )
        func_graph2 = self.get_graph(
            self.function2,
            self.function_color2
        )
        zdh = TextMobject("Z","D","H")
        zdh_color = [RED,GREEN,ORANGE]
        for letter,color in zip(zdh,zdh_color):
            letter.set_color(color)
        
        self.play(
            ShowCreation(func_graph),
            ShowCreation(func_graph2),
            GrowFromCenter(zdh),
            )

#TODO add other types of love curves
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

class IfuckSurya(Scene):
    def construct(self):
        x = LoveCurve1()
        x.set_color(RED)
        x.scale(2).shift(UP*1)
        zdh = TextMobject("Z","D","H").shift(RIGHT*5 + DOWN * 3)
        zdh_color = [RED,GREEN,ORANGE]
        for letter,color in zip(zdh,zdh_color):
            letter.set_color(color)
        happy = TextMobject("HAPPY","520")
        happy[0].set_color(PINK)
        happy[1].set_color(RED)
        happy[0].next_to(zdh.get_corner(LEFT+DOWN),DOWN)
        happy[1].next_to(happy[0], RIGHT)
        img = ImageMobject('baby.jpeg').scale(3)
        # x.surround(img)
        self.play(
            ShowCreation(img),
            ShowCreation(x),
            Write(zdh),
            FadeIn(happy),
            run_time = 5
            )