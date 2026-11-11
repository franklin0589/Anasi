from __future__ import annotations
import PIL.Image as Image
import cairo
import math
import random
import numpy as np

from PIL import Image, ImageDraw, ImageFont, ImageOps
from itertools import batched
from enum import IntEnum

class Color:
    BLACK = [0, 0, 0, 1]
    BROWN = [150/255,75/255,0,1]
    WHITE = [1, 1, 1, 1]
    RED = [1, 0, 0, 1]
    ORANGE = [1, 0.6, 0, 1]
    YELLOW = [1, 1, 0, 1]
    GREEN = [0, 1, 0, 1]
    CYAN = [0, 1, 1, 1]
    BLUE = [0, 0, 1, 1]
    MAGENTA = [1, 0, 1, 1]
    PURPLE = [0.5, 0, 1, 1]
    TAN = [1, 5/7, 3/6, 1]

class ActionTypes(IntEnum):
    WAIT = 0
    ACTION = 1
    DIALOGUE = 2
    SCENE_ENTER = 3
    SCENE_EXIT = 4
    TRANSITION = 5

class CameraLens(IntEnum):
    Wide = 15
    Close = 50
    Normal = 80
    Zoom = 200        

#  Vector
Vector2D = lambda x, y: np.array([[x],[y]])
Vector3D = lambda x, y, z: np.array([[x],[y],[z]])
Vector2i = lambda x, y: np.array([[x],[y],[1]])
Vector3i = lambda x, y, z: np.array([[x],[y],[z],[1]])
rVector2D = lambda sx,sy,ex,ey: Vector2D(random.randrange(sx,ex),random.randrange(sy,ey))

def unwrap(s):return [int(i[0]) for i in s]
def u_hvec(s): return ([int(i[0]) for i in s])[:-1] 
def h_vec2(s): return Vector3D(*unwrap(s), 1)
def h_vec3(s): return Vector3i(*unwrap(s))


ORIGIN = Vector2D(0,0)
CENTER = Vector2D(50,50)

mat_translate = lambda vec, x, y: np.matrix([[1,0,x],[0,1,y],[0,0,1]])*h_vec2(vec)
mat3D_translate = lambda vec, x, y, z: np.matrix([[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]])*vec
hookes = lambda k,x : k*x
sine = lambda x: math.sin(x/180*math.pi)
cosine = lambda x: math.cos(x/180*math.pi)
sqrt = lambda x: math.sqrt(x) if x>=0 else 0
slope = lambda pa, pb: (pb[1]-pa[1])/(pb[0]-pa[0]) if pb[0] != pa[0] else 500
intercept = lambda pa, slope: -(pa[1] - slope*pa[0])
slope_intercept = lambda pa, slope,x: slope*x+intercept(pa, slope)
rod = lambda pa, pb, offset: lambda x: slope_intercept(pa, slope(pa,pb), x)+offset 
magnitude = lambda p,q: sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
normal_vector = lambda p,q: [(p[0]-q[0])/magnitude(p,q),(p[1]-q[1])/magnitude(p,q)]
perspective = lambda focal_length, depth: focal_length / (focal_length + depth)
persp_scal = lambda persp, sc_callback: sc_callback(persp, persp)


def translate(value, lmin, lmax, rmin, rmax):
    return rmin + ((float(value - lmin) / float(lmax - lmin)) * (rmax - rmin))

deg_to_rad = lambda deg: deg/180*math.pi
lerp = lambda x, a, b: a*(1-x) + b*x 
polar = lambda x,y, rlen, ang: (x+rlen*math.cos(ang),y+rlen*math.sin(ang))
clamp = lambda x, min_, max_: max(min(x, max_), min_)
retrn = lambda obj, ret: [None, ret][-1]


def convert_from_pil(im: Image, alpha: float=1.0, format: cairo.Format=cairo.FORMAT_ARGB32) -> cairo.ImageSurface:
    if 'A' not in im.getbands():
        im.putalpha(int(alpha * 256.))
    arr = bytearray(im.tobytes('raw', 'BGRa'))
    return cairo.ImageSurface.create_for_data(arr, format, im.width, im.height)

def generate_sketch(num_lines, num_points, error_constant=1.2):
    for i in range(num_lines):
        error = int(error_constant*7/((i+1)))
        error_vecs = [unwrap(rVector2D(-error,-error,error,error)) for _ in range(num_points)]
        yield error_vecs, error  

load_image =  lambda img1: Image.open(img1)
load_image_png =  lambda img1: Image.open(img1, formats=["PNG"])
scale_image = lambda img1, width, height: ImageOps.fit(img1, (width, height), )


class Ease:
    ease_none = lambda x:x
    ease_cubic_in_out = lambda x: 4*x**3 if x<0.5 else 1 - math.pow(-2 * x + 2, 3) / 2;
    ease_sine_in = lambda x: 1 - math.cos((x * math.pi) / 2);
    ease_sine_out = lambda x: math.sin((x * math.pi) / 2);
    ease_sine_in_out = lambda x: -(math.cos(math.pi * x) - 1) / 2;
    
def ease(origin, target, speed, frame, easing = Ease.ease_none):
    s = translate(frame, 0,200, 0, 1)
    delta = target - origin
    ease_res = easing(s)
    rush_delta = (ease_res * speed) * delta 
    return origin + clamp(rush_delta, 0, delta)

class Board:
    def __init__(self, width, height):
        self.dimensions = [width, height]
        self.reset_board()

    def reset_board(self):
        self.surface = cairo.ImageSurface(cairo.Format.ARGB32, *self.dimensions) 
        self.pen = cairo.Context(self.surface)
        self.normalize_scale()

    def normalize_scale(self):
        self.pen.scale(*self.dimensions)
        self.pen.scale(1/100, 1/100)
    
    def fill_clip(self):
        self.pen.paint()
   
    def fill(self):
        self.pen.fill()
    def ink(self):
        self.pen.stroke()
 
    def fill_ink(self):
        self.pen.fill_preserve()
        self.set_pen_color((0,0,0,1))
        self.set_pen_width(0.2)
        
        self.pen.stroke()
   
    def set_pen_origin(self, origin):
        self.pen.translate(*unwrap(origin))
    def set_pen_scale(self, sx, sy):
        self.pen.scale(sx, sy)
    def set_pen_font(self, size):
        self.pen.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.pen.set_font_size(size)
    
    def set_pen_color(self, color):
        self.pen.set_source_rgba(*color)
    def set_pen_width(self, brd):
        self.pen.set_line_width(brd)
    def set_pen(self, color, brd):
        self.set_pen_color(color)
        self.set_pen_width(brd)    
    def pen_line(self, dx, dy):
        self.pen.rel_line_to(dx,dy)
    def pen_close(self):
        self.pen.close_path()
    def lift_pen(self,x,y):
        self.pen.move_to(x,y)
    def start_pen(self):
        self.pen.save()
    def finish_pen(self):
        self.pen.restore()
    
    def extract_page(self):
        _surface = self.surface
        self.reset_board()
        return _surface

    def background(self, color):
        self.start_pen()
        self.set_pen_color(color)
        self.fill_clip()
        self.finish_pen()

    def circle(self, center, radius, color):
        self.start_pen()
        self.set_pen_color(color)
        self.pen.arc(*unwrap(center), radius, deg_to_rad(0), deg_to_rad(360))
        self.fill_ink()
        self.finish_pen()

    def point(self, origin, color):
        self.circle(origin, 3, color)
        
    def line(self, origin, dest, color, brd = 0.18):
        self.start_pen()
        self.set_pen(color, brd)
        self.lift_pen(*unwrap(origin))
        self.pen.line_to(*unwrap(dest))
        self.ink()
        self.finish_pen()

    def curve(self, origin, controlA, controlB, dest, color, brd = 0.17):
        self.start_pen()
        self.set_pen(color, brd)
        self.lift_pen(*unwrap(origin))
        self.pen.curve_to(*unwrap(controlA),*unwrap(controlB),*unwrap(dest))
        self.ink()
        self.finish_pen() 
    
    def rect(self, origin, w, h, color, brd = 0.17):
        self.start_pen()
        self.set_pen(color, brd)
        self.lift_pen(*unwrap(origin))
        self.pen_line(w,0)
        self.pen_line(0,h)
        self.pen_line(-w,0)
        self.pen_close()
        self.fill_ink()
        self.finish_pen()
        
    def box(self, origin,w,h, color):
        self.start_pen()
        self.set_pen_color(color)
        self.lift_pen(*unwrap(origin))
        self.pen_line(w, 0)
        self.pen_line(0, h)
        self.pen_line(-w, 0)
        self.pen_close()
        self.ink()
        self.finish_pen()
        
    def polygon(self, points:list, color, brd = 0.18):
        self.start_pen()
        self.set_pen(color, brd)
        origin = points.pop(0)
        self.lift_pen(*unwrap(origin))
        for p in points:
            self.pen.line_to(*unwrap(p))
        self.pen_close()
        self.fill_ink()
        self.finish_pen()

    def triangle(self, t1, t2, t3, color):
        self.polygon([t1,t2,t3], color)  

    def text(self, origin, text, color, size = 12):
        self.start_pen()
        self.set_pen_color(color)
        self.lift_pen(*unwrap(origin))
        self.set_pen_font(size)
        self.pen.text_path(text)
        self.fill()
        self.finish_pen()
        
    def text_bb(self, text, size=12):
        self.set_pen_font(size)
        return self.pen.text_extents(text)

    def linear_gradient(self, origin,w,h, start_color, end_color):
        t = Texture()
        t.linear_gradient(*unwrap(origin), w, h)
        t.color_stop(0,*start_color)
        t.color_stop(1,*end_color)
        self.pen.set_source(t())
        self.fill_clip()

    def set_image(self, img, origin):
        self.pen.set_source_surface(convert_from_pil(img), *unwrap(origin))

    def draw_image(self, origin, width, height, image):
        self.start_pen()
        imsc = scale_image(image, width, height)
        self.set_pen_scale(1/4,1/4)
        self.pen.set_source_surface(convert_from_pil(imsc), *unwrap(origin))
        self.fill_clip()
        self.finish_pen()


    def draw_shape(self, origin, points, color, offset=0, scale=1):
        n_webs = 16
        x, y = unwrap(origin)
        get_line = lambda index, lines: index * (360//lines) + offset
        get_line_point = lambda line_index, height: (x+height*math.cos(get_line(line_index, n_webs)/180*math.pi), y+height*math.sin(get_line(line_index, n_webs)/180*math.pi))
        
        self.start_pen()
        self.set_pen(color, 0.13)
        self.lift_pen(*get_line_point(0, scale*points[0]))
        
        for i, l in enumerate(points[1:]):
            self.pen.line_to(*get_line_point(i+1, l*scale))
        self.pen_close()
        self.fill_ink()
        # self.ink()
        self.finish_pen()

    def horizon(self, level, color):
        self.rect(Vector2D(0, level), self.dimensions[0], self.dimensions[1]-level, color)
    
    def wall(self, ltwall,rtwall, rbwall, lbwall, color):
        self.polygon([ltwall,rtwall,rbwall,lbwall], color)

    def sketch_line(self, origin, final, color):
        for ev, err in generate_sketch(7, 2):
            org = mat_translate(h_vec2(origin), *ev[0])
            fnl = mat_translate(h_vec2(final), *ev[1])
            color[-1] = err//14 + 0.25
            self.line(*u_hvec(org), *u_hvec(fnl), color)
    def sketch_curve(self, origin, controlA, controlB, final, color, error_constant = 1.2):
        for ev, err in generate_sketch(7, 4, error_constant):
            org = mat_translate(h_vec2(origin),  *ev[0])
            cA = mat_translate(h_vec2(controlA), *ev[1] )
            cB = mat_translate(h_vec2(controlB), *ev[2])
            fnl = mat_translate(final,   *ev[3])
            color[-1] = err//14 + 0.25
            self.curve(*u_hvec(org), *u_hvec(cA), *u_hvec(cB), *u_hvec(fnl), color)

    def sketch_shape(self, origin, points, color, offset=0, scale=1):
        n_webs = 16
        x,y = unwrap(origin)
        get_line = lambda index, lines: index * (360//lines) + offset
        get_line_point = lambda line_index, height: (x+height*math.cos(get_line(line_index, n_webs)/180*math.pi), y+height*math.sin(get_line(line_index, n_webs)/180*math.pi))
        points = [Vector2D(*get_line_point(i, scale*points[i])) for i in range(len(points))]
        origin = points.pop(0)
        start = origin
        self.lift_pen(*unwrap(start))
        for ca, cb, f in batched(points, 3):
            self.sketch_curve(start, ca, cb, f, color, 1.6)
            start = f
        self.sketch_curve(points[-3], points[-2], points[-1], origin, color, 1.6)



    def __call__(self):
        return self.pen

class Texture():
    def __init__(self):
        self.pat = None
    def linear_gradient(self, x,y,w,h):   
        self.pat = cairo.LinearGradient(x, y, w, h)
    def radial_gradient(self, x,y,r,sx,sy,sr):   
        self.pat = cairo.RadialGradient(x, y, r, sx,sy,sr)
    def color_stop(self, index,color):
        self.pat.add_color_stop_rgba(index, *color)
    def __call__(self):
        return self.pat

paste_image  = lambda img1, img2, x,y: img1.paste(img2, (x,y))
paste_png_image  = lambda img1, img2, x,y: img1.alpha_composite(img2, (x,y))
paste_image_scaled = lambda img1, img2, x,y, width, height: img1.paste(ImageOps.fit(img2, (width, height)), (x,y,x+width, y+height))

class Shapes:
    right_eye = lambda theta: 1/math.sqrt(sine(theta))*sine(theta)
    left_eye = lambda theta: -1/math.sqrt(sine(theta))*sine(theta)
    torso = lambda theta: (sine(theta)-1.8)
    apple = lambda theta: -(sine(theta)-1)
    circle = lambda x: lambda theta: x 
    ellispe = lambda a,b,c: lambda theta:(b**2/a)/(1+c/a*sine(theta))
    arm = ellispe (1.2,1.4,1)
    pelvis = lambda theta: -sqrt(sine(theta))
    bumblebee_wings = lambda theta:math.sqrt(sine(theta))*sine(theta)
    get_font = lambda font_name, size: ImageFont.truetype(font_name, size)


class CameraDepth:
    def __init__(self, board: Board, fl, z):
        self.board = board
        self.focal = fl
        self.z = z
    def __enter__(self):
        self.board.start_pen()
        _persp= perspective(self.focal, self.z)
        self.board.set_pen_scale(_persp, _persp)
    def __exit__(self,*args):
        self.board.finish_pen()

class WorldPoint:
    def __init__(self,board:Board, x, y, z):
        self.board = board
        self.x = x
        self.y = y
        self.z = z
        ...
    def __enter__(self):
        self.cd = CameraDepth(self.board, CameraLens.Normal, self.z)
        self.cd.__enter__()
        origin = Vector2D(self.x,self.y)
        self.board.set_pen_origin(origin)

    def __exit__(self, *args):
        self.cd.__exit__()

class Object:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z
    def draw (self,  board):
        with WorldPoint(board, self.x, self.y, self.z):
            self.render(board)
    def render(self, board):
        ...



from __future__ import annotations
import PIL.Image as Image
import cairo
import math
import random
import numpy as np

from PIL import Image, ImageFont, ImageOps


#  Matrix Vector
def Vector2(x, y):
    return np.array([[x], [y]])

def Vector2i(x, y): 
    return np.array([[x], [y], [1]])

def Vector3(x, y, z): 
    return np.array([[x], [y], [z]])

def Vector3i(x, y, z): 
    return np.array([[x], [y], [z], [1]])


def Random2(sx, sy, width, height):
    A =  random.randrange(sx, sx+width)
    B =  random.randrange(sy, sy+height)
    return Vector2(A,B)


def Arrange(s): 
    return [int(i[0]) for i in s]
def u_hvec(s): 
    return ([int(i[0]) for i in s])[:-1]
def h_vec2(s): 
    return Vector3(*Arrange(s), 1)
def h_vec3(s): 
    return Vector3i(*Arrange(s))


# ORIGIN = Vector2D(0, 0)
# CENTER = Vector2D(50, 50)


def mat_translate(vec, x, y): 
    return np.matrix([[1, 0, x], [0, 1, y], [0, 0, 1]])*h_vec2(vec)


def mat3D_translate(vec, x, y, z): 
    return np.matrix(
    [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])*vec


def hookes(k, x): return k*x
def sine(x): return math.sin(x/180*math.pi)
def cosine(x): return math.cos(x/180*math.pi)


def sqrt(x): 
    return math.sqrt(x) if x >= 0 else 0
def slope(A, B): 
    mtop = B[1]-A[1]
    mbottom = (B[0]-A[0]) if B[0] != A[0] else 500
    return  mtop/mbottom

def intercept(pa, slope): 
    return -(pa[1] - slope*pa[0])

def slope_intercept(pa, slope, x): 
    return slope*x+intercept(pa, slope)

def rod(pa, pb, offset): 
    return lambda x: slope_intercept(pa, slope(pa, pb), x)+offset

def magnitude(A, B): 
    return sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)


def normal_vector(A, B): 
    X = (A[0]-B[0]) / magnitude(A, B)
    Y = (A[1]-B[1])/magnitude(A, B)
    return [X,Y]

def perspective(focal_length, depth): 
    return focal_length / (focal_length + depth)

def persp_scal(persp, sc_callback): 
    return sc_callback(persp, persp)

def translate(value, lmin, lmax, rmin, rmax):
    return rmin + ((float(value - lmin) / float(lmax - lmin)) * (rmax - rmin))


def deg_to_rad(deg): 
    return deg/180*math.pi
def lerp(x, a, b): 
    return a*(1-x) + b*x


def polar(x, y, rlen, ang): 
    return (x+rlen*math.cos(ang), y+rlen*math.sin(ang))
def clamp(x, min_, max_): 
    return max(min(x, max_), min_)
def retrn(obj, ret): 
    return [None, ret][-1]


def convert_from_pil(im: Image, alpha: float = 1.0, format: cairo.Format = cairo.FORMAT_ARGB32) -> cairo.ImageSurface:
    if 'A' not in im.getbands():
        im.putalpha(int(alpha * 256.))
    arr = bytearray(im.tobytes('raw', 'BGRa'))
    return cairo.ImageSurface.create_for_data(arr, format, im.width, im.height)


# def generate_sketch(num_lines, num_points, error_constant=1.2):
#     for i in range(num_lines):
#         error = int(error_constant*7/((i+1)))
#         error_vecs = [unwrap(rVector2D(-error, -error, error, error))
#                       for _ in range(num_points)]
#         yield error_vecs, error

def get_font(font_name, size): 
    return ImageFont.truetype(font_name, size)

def load_image(img1): 
    return Image.open(img1)

def load_image_png(img1): 
    return Image.open(img1, formats=["PNG"])

def scale_image(img1, width, height): return ImageOps.fit(
    img1, (width, height), )

def paste_image(img1, img2, x, y): 
    return img1.paste(img2, (x, y))

def paste_png_image(img1, img2, x, y): 
    return img1.alpha_composite(img2, (x, y))

def apply_layer(composite, layer):
    return paste_image(composite, layer, 0, 0)

def paste_image_scaled(img1, img2, x, y, width, height): 
    crop = ImageOps.fit(img2, (width, height))
    return img1.paste(crop, (x, y, x+width, y+height))


# class Shapes:
#     def right_eye(theta): return 1/math.sqrt(sine(theta))*sine(theta)
#     def left_eye(theta): return -1/math.sqrt(sine(theta))*sine(theta)
#     def torso(theta): return (sine(theta)-1.8)
#     def apple(theta): return -(sine(theta)-1)
#     def circle(x): return lambda theta: x
#     def ellispe(a, b, c): return lambda theta: (b**2/a)/(1+c/a*sine(theta))
#     arm = ellispe(1.2, 1.4, 1)
#     def pelvis(theta): return -sqrt(sine(theta))
#     def bumblebee_wings(theta): return math.sqrt(sine(theta))*sine(theta)


