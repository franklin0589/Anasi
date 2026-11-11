
from PIL import Image, ImageDraw, ImageFont, ImageOps

class Pen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw = ImageDraw.Draw(canvas)

    def draw_circle(self, x:int, y:int, size:int, fill:str):
        self.draw.ellipse((x, y, x + size, y + size), fill=fill)

    def draw_line(self, x:int, y:int, x2:int, y2:int, fill:str):
        self.draw.line((x, y, x2, y2), fill=fill)

    def draw_cline(self, x:int, y:int, x2:int, y2:int, fill:str):
        self.draw.line((x, y, x2, y2), fill=fill, joint="curve")

    def draw_rect(self, x:int, y:int, w:int, h:int, fill:str):   
        self.draw.rectangle((x, y, x + w, y + h), fill=fill)

    def draw_rounded_rect(self, x:int, y:int, w:int, h:int, fill:str):
        self.draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=fill)

    def draw_polygon(self, points:list, fill:str):
        self.draw.polygon(points, fill=fill)

    def write_text(self, x:int, y:int, text:str, fill:str, font:ImageFont.ImageFont, anchor:str="mm", align:str="center"):
        self.draw.text((x, y), text, fill=fill, anchor=anchor, align=align, font=font)

    def write_multiline_text(self, x:int, y:int, text:str, fill:str, font:ImageFont.ImageFont, anchor:str=None, align:str=None):
        self.draw.multiline_text((x, y), text, fill=fill, font=font, anchor=anchor, align=align)

class Pattern:
    @staticmethod
    def noise(size:tuple[int, int], fit:float):
        return Image.effect_noise(size, fit)

    @staticmethod
    def linear_gradient():
        return Image.linear_gradient()

    @staticmethod
    def radial_gradient():
        return Image.radial_gradient()

class PIL_Image:
    def __init__(self, img_path:str):
        self.image = Image.open(img_path)

    def paste(self, canvas, x:int, y:int):
        canvas.paste(self.image, (x, y))

    def paste_png(self, canvas, x:int, y:int):
        canvas.alpha_composite(self.image, (x, y))

    def paste_scaled(self, canvas, x:int, y:int, width:int, height:int):
        scaled_image = ImageOps.fit(self.image, (width, height))
        canvas.paste(scaled_image, (x, y, x + width, y + height))


class PIL_ImagePNG(PIL_Image):
    def __init__(self, img_path:str):
        super().__init__(img_path)
        self.image = Image.open(img_path, formats=["PNG"])

