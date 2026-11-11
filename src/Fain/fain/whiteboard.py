from __future__ import annotations
from .context import *
from enum import IntEnum

class PEN_STATE(IntEnum):
    UP = 0
    DOWN = 1
    IS_ERASER = 2 # Whether Or Not the Pen is currently marking
    COLOR_L = 4
    COLOR_H = 8

FILL_COLORS = ["Black", "Blue", "Red", "Green"]

# Whiteboard
class Whiteboard:
    def __init__(self, canvas, pen):
        self.set_pen_state(pen)
        self.canvas = canvas
        self.objects = []
        self.background_color = "white"
        self.mark = lambda x, y: create_circle(self.canvas, x,y, 4, fill = self.fill_color)
        self.erase = lambda x, y: create_circle(self.canvas, x,y, 4, fill = self.background_color)
    
    def set_pen_state(self, pen): 
        self.color_bits = pen.state >> 2
        self.fill_color = FILL_COLORS[self.color_bits]
        self.state_bits = pen.state % 4
        
    def mark_pen(self, x, y):
        if self.state_bits % 2 == 1:
            tool = self.erase if self.state_bits == 3 else self.mark
            tool(x,y)
    
    def write_text(self, x,y, text):
        self.canvas.create_text(x, y, text=text, fill=self.fill_color, font=('Helvetica 15 bold'))
    
    


# Pen
class Pen:
    def __init__(self, state:int):
        self.state = state


class Equation:
    parameters: list[int]
    base_str: str

    def __init__(self, base):
        self.base_str = base
        self.parameters = []
        
    def set_parameters(self, p):
        self.parameters = p
        return self
    
    def __str__(self):
        return self.base_str.format(*self.parameters).replace("TTT", "{0}")

circle = lambda r,x,y: str(Equation("{0}*sine(TTT)+{1},{0}*cosine(TTT)+{2}").set_parameters([r, x, y]))
square =lambda l, w, x, y: str(Equation("{0}*(abs(cosine(TTT))*cosine(TTT) + abs(sine(TTT))*sine(TTT))+{2}, {1}*(abs(cosine(TTT))*cosine(TTT) - abs(sine(TTT))*sine(TTT))+{3}").set_parameters([l, w, x, y]))

line  = lambda x,y,x2,y2, scale = 200: Equation("lerp({0},{2},TTT/{4}), lerp({1},{3},TTT/{4})").set_parameters([x,y,x2,y2,scale])


class CurveTracer():
    def __init__(self, curve):
        self.curve = curve
        self.magnitude = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.magnitude < self.curve.length:
            self.magnitude += 1
            return self.eval_curve() 
        else:
            raise StopIteration()
    def eval_curve(self):
        return eval(self.curve.equation.format(self.magnitude))

create_curve = lambda s, eq, len, white: [updateattr(s, {"equation":eq, "length":len, "whiteboard":white}), None][-1]
Curve = type("Curve", (object,), {"__init__":create_curve, "__iter__": lambda self: CurveTracer(self)})
draw_curve = lambda curve: [curve.whiteboard.mark_pen(x,y) for x,y in curve]

# Shape
class Shape:
    def __init__(self, eqs, base_mgn = 200):
        self.set_equations(eqs)
        self.base_mgn = base_mgn
        
    def set_equations(self, eqs):
        self.equations = eqs
    def add_equations(self, eq):
        self.equations += [eq]
    
    def draw(self, whiteboard):
        for eq in self.equations:
            draw_curve(Curve(str(eq), self.base_mgn, whiteboard))


class Triangle:
    def __init__(self, p1, p2, p3):
        self.equations = [line(*p1, *p2), line(*p2, *p3), line(*p3, *p1)]
    def draw(self, whiteboard):
        Shape(self.equations).draw(whiteboard)
        
class Horizon:
    def __init__(self, horizon_level):
        self.horizon_level = horizon_level
        
    def draw(self, whiteboard):
        max_whiteboard_width = 800
        equations = [line(0, self.horizon_level, max_whiteboard_width, self.horizon_level)]
        Shape(equations).draw(whiteboard)
class OTriangle(Triangle):
    def __init__(self, px, py, d1, d2, d3, d4):
        origin = (px, py)
        r1_origin = (px+d1, py+d2)
        r2_origin = (px+d3, py+d4)
        super().__init__(origin, r1_origin, r2_origin)

class Isoceles(Triangle):
    def __init__(self, px, py, height, base):
        self.top_point =(px,py)
        self.left_bottom = (px-base, py+height)
        self.right_bottom = (px+base, py+height)
        super().__init__(self.top_point, self.left_bottom, self.right_bottom)

class Equilateral(Triangle):
    def __init__(self, px, py, rot_ang, len):
        point1  =(px,py)
        point2 = vec_add(point1, polar_cast(len, rot_ang))
        point3 = vec_add(point2, polar_cast(len, rot_ang+120))
        super().__init__(point1, point2, point3)

class Right(Triangle):
    def __init__(self, px, py, base, height):
        p1 = (px,py)
        p2 = (px, py+height)
        p3 = (px+base, py+height)
        super().__init__(p1, p2, p3)


class Quadrilateral:
    def __init__(self, p1, p2, p3, p4):
        self.equations = [line(*p1, *p2), line(*p2, *p3), line(*p3, *p4), line(*p4, *p1) ]
    def draw(self, whiteboard):
        Shape(self.equations).draw(whiteboard)
    
class Rectangle(Quadrilateral):
    def __init__(self, x, y, l, w, ang = 0):
        p1 = (x,y)
        p2 = vec_add((x,y), polar_cast(l, ang))
        p3 = vec_add(p2, polar_cast(w, ang+90))
        p4 = vec_add(p3, polar_cast(l, ang+180))
        super().__init__(p1,p2,p3,p4)
        
class Square(Quadrilateral):
    def __init__(self, x, y, l, ang = 0):
        p1 = (x,y)
        p2 = vec_add((x,y), polar_cast(l, ang))
        p3 = vec_add(p2, polar_cast(l, ang+90))
        p4 = vec_add(p3, polar_cast(l, ang+180))
        super().__init__(p1,p2,p3,p4)
