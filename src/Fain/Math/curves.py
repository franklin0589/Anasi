from __future__ import annotations
from typing import Protocol, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

# Linear interpolation
def lerp(a, b, t):
        return (1-t)*a + b*t
    
class Linterp:
    def __init__(self, A:Point, B:Point):
        self.parameters = [A, B]
        
    def get_point(self, t)->Point:
        x_interp = lerp(self.parameters[0].x, self.parameters[1].x, t)
        y_interp = lerp(self.parameters[0].y, self.parameters[1].y, t)
        return Point(x_interp, y_interp)

class Qinterp:
    def __init__(self, A:Point, B:Point, C:Point):
        self.parameters = [A, B, C]
        
    def get_point(self, t)->Point:
        self.ab_line = Linterp(self.parameters[0], self.parameters[1])
        self.bc_line = Linterp(self.parameters[1], self.parameters[2])
        abx, aby = self.ab_line.get_point(t)
        bcx, bcy = self.bc_line.get_point(t)
        return Point(lerp(abx, bcx, t), lerp(aby, bcy, t))
    
class Cinterp:
    def __init__(self, A:Point,B:Point,C:Point,D:Point):
        self.parameters = [A,B,C,D]
        
    def get_point(self, t):
        self.abc_quad_curve = Qinterp(self.parameters[0], self.parameters[1], self.parameters[2])    
        self.bcd_quad_curve = Qinterp(self.parameters[1], self.parameters[2], self.parameters[3])
        abx, aby = self.abc_quad_curve(t)
        bcx, bcy = self.bcd_quad_curve(t)
        return Point(lerp(abx, bcx,t), lerp(aby, bcy,t))

class Fast_CInterp:
    def __init__(self, A:Point,B:Point,C:Point,D:Point):
        self.parameters = [A,B,C,D]
       
    def get_point(self, t):
        berstein_eq = lambda t, a, b, c, d: a*(-t**3 + 3*t**2 - 3*t+1) + b*(3*t**3-6*t**2+3*t)+c*(-3*t**3+3*t**2)+d*t**3
        dimen = lambda i: [point[i] for point in self.parameters]
        return [berstein_eq(t, *dimen(i)) for i in range(2)]
    
class Poly_CInterp:
    def __init__(self, A:Point, B:Point, C:Point, D:Point):
        self.parameters = [A,B,C,D]
        
    def get_point(self, t):
        poly_eq = lambda t, a, b, c, d: a + t*(-3*a +3*b) + t**2 *(3*a - 6*b+ c*3) + t**3 * (-a + 3*b - 3*c + d)        
        dimen = lambda i: [point[i] for point in self.parameters]
        return [poly_eq(t, *dimen(i)) for i in range(2)]
    
class Derv_CInterp:
    def __init__(self, A:Point, B:Point, C:Point, D:Point):
        self.parameters = [A, B, C, D]

    def get_point(self, t):        
        poly_eq = lambda t, a, b, c, d:  (-3*a +3*b) + 2*t * (3*a - 6*b+ c*3) + 3*t**2 * (-a + 3*b - 3*c + d)
        dimen = lambda i: [point[i] for point in self.parameters]
        return [poly_eq(t, *dimen(i)) for i in range(2)]

class InterpolationStrategy(Protocol):
    parameters:list[Point]
    def get_point(self, t) -> Point: ...

class Curve:
    def __init__(self, _points:list[Point],cindex:int=2, step:int =35):
        self.points = _points
        interpolate_strat = [Linterp, Qinterp, Cinterp, Fast_CInterp, Poly_CInterp, Derv_CInterp]
        self.i_strat = interpolate_strat[cindex](*self.points)
        self.step = 35

    def interpolate(self, t) -> Point:
        return self.i_strat.get_point(t)

    def trace(self):
        for i in range(self.steps):
            t = i/self.steps 
            yield self.interpolate(t)

class Spline:
    def __init__(self, ox, oy):
        self.origin = [ox, oy]
        self.endpoint = [ox, oy]
        self.curves = []
    def add_curve(self, bx, by, cx,cy, dx, dy):
        self.curves += [PCubicBezier(*self.endpoint, bx, by, cx, cy, dx, dy)]
        self.endpoint = [dx, dy]
    def get_point(self, u):
        curve_index = int(u)
        t = u-curve_index
        if curve_index >= len(self.curves):
            raise IndexError("Attempting to use curve out of index")
        return self.curves[curve_index].get_point(t)
    def trace(self, step_count):
        return [self.get_point(i/step_count) for i in range(0, len(self.curves)*step_count)] + [self.endpoint]
            
    
# class MCubicBezier:
# Matrix Form
#     def __init__(self, ax, ay,bx,by,cx,cy,dx,dy):
#         self.a = [ax, ay]
#         self.b = [bx, by]
#         self.c = [cx, cy]
#         self.d = [dx, dy]
        
#     def get_point(self, t):
#         poly_eq = lambda t, a, b, c, d: a + t*(-3*a +3*b) + t**2 *(3*a - 6*b+ c*3) + t**3 * (-a + 3*b - 3*c + d)        
#         return [poly_eq(t, self.a[i], self.b[i], self.c[i], self.d[i]) for i in range(2)]
    
#     def get_derivative(self, t):        
#         poly_eq = lambda t, a, b, c, d:  (-3*a +3*b) + 2*t * (3*a - 6*b+ c*3) + 3*t**2 * (-a + 3*b - 3*c + d)
#         return [poly_eq(t, self.a[i], self.b[i], self.c[i], self.d[i]) for i in range(2)]
    
    

