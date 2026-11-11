import cairo
import math
from PIL import Image, ImageOps
from .protocol import iBoard, iColor, iCFont

def to_pil(surface: cairo.ImageSurface):
    format = surface.get_format()
    size = (surface.get_width(), surface.get_height())
    stride = surface.get_stride()

    with surface.get_data() as memory:
        if format == cairo.Format.RGB24:
            return Image.frombuffer(
                "RGB", size, memory.tobytes(),
                'raw', "BGRX", stride)
        elif format == cairo.Format.ARGB32:
            return Image.frombuffer(
                "RGBA", size, memory.tobytes(),
                'raw', "BGRa", stride)
        else:
            raise NotImplementedError(repr(format))

class Font:
    def __init__(self, name, size, slant=cairo.FONT_SLANT_NORMAL, weight= cairo.FONT_WEIGHT_NORMAL):
        self.size = size

        self.name = name 
        self.slant = slant
        self.weight = weight
    
class Board:
    def __init__(self:iBoard, width, height):
        self.dimension = (width, height)
        self.surface = cairo.ImageSurface(
            cairo.Format.ARGB32, width, height)
        self.context = cairo.Context(self.surface)
        self.setup()
    
    def setup(self):
        self._normalize_scale()
        self.border_size =0.16
        self.outline_size = 0.18
        self.point_size = 0.5

    def _normalize_scale(self):
        self.context.scale(*self.dimension)
        aspect = self.dimension[1]/self.dimension[0]
        self.context.scale(1/100, 1/100)
    
    def fill_drag(self):
        self.context.paint()
   
    def fill(self):
        self.context.fill()

    def ink(self):
        self.context.stroke()
 
    def fill_ink(self, ink_color:iColor, brd_size:float):
        self.context.fill_preserve()
        self.set_color(ink_color)
        self.set_width(brd_size)
        self.context.stroke()

    def set_origin(self, x:int, y):
        self.context.translate(x, y)

    def set_scale(self, scale_fac_x:float, scale_fac_y:float):
        self.context.scale(scale_fac_x, scale_fac_y)

    def set_font(self, font:iCFont):
        self.context.select_font_face(font.name, font.slant, font.weight)
        self.context.set_font_size(font.size)

    def set_color(self, color:iColor):
        self.context.set_source_rgba(*color.values)
    
    def set_width(self, brd):
        self.context.set_line_width(brd)

    def lift(self,x,y):
        self.context.move_to(x,y)

    def start_drag(self):
        self.context.save()

    def finish_drag(self):
        self.context.restore()
        
    def translate(self, x:int, y:int):
        self.context.translate(x, y)
    
    def rotate(self, ang:float):
        self.context.rotate(math.radians(ang))
        
    
    def modify_basis(self, pivot, scale, rotation):
        self.context.move_to(*pivot)
        self.context.scale(scale)
        self.context.rotate(rotation)

    def render_image(self):
        return to_pil(self.surface)
    
    
def get_board(width, height) -> iBoard:
    return Board(width, height)

