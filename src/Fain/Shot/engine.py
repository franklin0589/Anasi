from PIL import Image
import ffmpy
import cairo
import os

def get_image_canvas(width, height, background):
    return Image.new("RGBA", (width, height), background)

def convert_to_pil(surface: cairo.ImageSurface):
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


def export_to_gif(filename, frames, duration):
    frames[0].save(filename,format="GIF", append_images=frames, save_all=True, duration=duration, loop=0)

def convert_gif_to_mp4(filename, output_path):
    ff = ffmpy.FFmpeg(inputs={filename: None},outputs={output_path: None})
    ff.run()


load_image = lambda x: ...

def get_Image_Cache():
    image_Cache = {}
    def get_image(image):
        if image not in image_Cache:
            image_Cache[image] = load_image(f"data\\Images\\{image}")
        return image_Cache[image] 
    return get_image


class Destination:
    PNG = 0
    JPEG = 1
    GIF = 10
    GIF_FTIME = 11
    MP4 = 30
    
class Engine:
    def __init__(self, callback, dest = Destination.PNG):
        self.callback = callback
        self.dest = dest
    
    def set_frames(self, fc, dur):
        self.frame_count = fc
        self.duration = dur
        return self

    def render_png(self, PNG_Name):
        surface = self.callback()
        image = convert_to_pil(surface)
        image.save(f"dist/{PNG_Name}.png")
    
    def render_jpeg(self, JPG_Name):
        surface = self.callback()
        image = convert_to_pil(surface)
        image.save(f"dist/{JPG_Name}.jpg")
        
    def render_gif(self, name):
        frames = []
        scene_duration = self.frame_count//len(self.callback)
        for scene_draw in self.callback:
            frames += [convert_to_pil(scene_draw(nbr)) for nbr in range(scene_duration)]
        export_to_gif("dist/"+name+".gif",frames, self.duration)

    def render_mp4(self, name):
        self.render_gif(name)
        convert_gif_to_mp4("dist/"+name+".gif", f"dist/{name}.mp4")
        os.remove("dist/"+name+".gif")
    
    def render_gif_ftime(self, name):
        frames = []
        durations = [1]
        frame_duration = self.frame_count//len(self.callback)
        for df in self.callback:
            for nbr in range(frame_duration):
                duration, frame = df(nbr)
                durations += [duration]
                frames += [convert_to_pil(frame)]
        export_to_gif("dist/"+name+".gif",frames, durations)

    def render(self, output_name):
        match self.dest:
            case Destination.PNG:
                self.render_png(output_name)
            case Destination.JPEG:
                self.render_jpeg(output_name)
            case Destination.GIF:
                self.render_gif(output_name)
            case Destination.GIF_FTIME:
                self.render_gif_ftime(output_name)
            case Destination.MP4:
                self.render_mp4(output_name)
    ...
    from PIL import Image, ImageOps
import ffmpy
import cairo
import os
from inspect import signature

def get_image_canvas(width, height, background):
    return Image.new("RGBA", (width, height), background)
def get_new_image(width, height):
    return Image.new("RGBA", (width, height))

def convert_to_pil(surface: cairo.ImageSurface):
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
    
def paste_image(img1:Image, img2:Image, x, y):
    return img1.paste(img2, (x, y))

def paste_png_image(img1, img2, x, y): 
    return img1.alpha_composite(img2, (x, y))

def apply_layer(composite, layer):
    return paste_png_image(composite, layer, 0, 0)

def paste_image_scaled(img1, img2, x, y, width, height): 
    crop = ImageOps.fit(img2, (width, height))
    return img1.paste(crop, (x, y, x+width, y+height))

def export_to_gif(filename, frames, duration):
    frames[0].save(filename,format="GIF", append_images=frames, save_all=True, duration=duration, loop=0)

def convert_gif_to_mp4(filename, output_path):
    ff = ffmpy.FFmpeg(inputs={filename: None},outputs={output_path: None})
    ff.run()

class Destination:
    PNG = 0
    JPEG = 1
    GIF = 10
    MP4 = 30
    
class ImageStack:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface_functions = []
        self.layers = []
        self.surface_image = {}

    def add_surf_layer(self, surface_callback):
        self.surface_functions.append(surface_callback)
        return self

    def render(self, t = -1):
        for index, func in enumerate(self.surface_functions):
            if t != -1 and len(signature(func).parameters) > 0:
                surf_layer = func(t) 
            elif index in self.surface_image:
                continue
            else:
                surf_layer = func()
            image = convert_to_pil(surf_layer)
            self.layers += [index]
            self.surface_image[index] = image
    
    def composite(self):
        comp_image = get_new_image(self.width, self.height)
        for layer in self.layers:
            next_layer = self.surface_image[layer]
            apply_layer(comp_image, next_layer)
        return comp_image
    
    def generate(self, t=-1):
        self.render(t)
        img = self.composite()
        return img

class Stitcher:
    def __init__(self):
        
        ...
    def indexed_load(self, foldername, filetype = ".png"):
        indexed = lambda x: int(x.split("_")[0])
        filenames = [os.path.join(foldername, file) for file in sorted(os.listdir(foldername), key = indexed) if filetype in file] 

        return [Image.open(file) for file in filenames]
    def load(self, foldername, filetype = ".png"):
        filenames = [os.path.join(foldername, file) for file in sorted(os.listdir(foldername)) if ".png" in file] 
        return [Image.open(file) for file in filenames]
    
    def stitch(self, filename, frames, duration):
        frames[0].save(filename,format="GIF", append_images=frames, save_all=True, duration=duration, loop=0)        
    
    def process(self, filename):
        convert_gif_to_mp4(filename+".gif", filename+".mp4")
        os.remove(filename+".gif")

class Engine:
    def __init__(self, callback_list, width, height, dest = Destination.PNG):
        
        self.image_stack  = ImageStack(width, height)
        for callback in callback_list:
            self.image_stack.add_surf_layer(callback)
        self.dest = dest
    
    def set_frames(self, time, fps):
        self.frame_count = time*fps
        self.duration = 1000//fps
        return self

    def render_png(self, PNG_Name):
        self.image_stack.generate().save(f"dist/{PNG_Name}.png")
    
    def render_jpeg(self, JPG_Name):
        self.image_stack.generate().save(f"dist/{JPG_Name}.jpg")
        
    def render_gif(self, name):
        frames = [self.image_stack.generate(nbr) for nbr in range(self.frame_count)]
        export_to_gif("dist/"+name+".gif",frames, self.duration)

    def render_mp4(self, name):
        self.render_gif(name)
        convert_gif_to_mp4("dist/"+name+".gif", f"dist/{name}.mp4")
        os.remove("dist/"+name+".gif")
    
    def render(self, output_name):
        match self.dest:
            case Destination.PNG:
                self.render_png(output_name)
            case Destination.JPEG:
                self.render_jpeg(output_name)
            case Destination.GIF:
                self.render_gif(output_name)
            case Destination.MP4:
                self.render_mp4(output_name)