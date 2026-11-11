from PIL import Image
import cairo

class Color:
    def __init__(self, r, g, b,a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.values =(r,g,b,a)
        
        

class ImageConverterService:
    def __init__(self):
        ...
        
    def cairo_to_pil(self, surface):
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

def get_color(r:float, g:float, b:float, a:float):
    return Color(r, g, b, a)
    

def get_image_converter()->ImageConverterService:
    return ImageConverterService()