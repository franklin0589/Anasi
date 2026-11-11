from scipy.io import wavfile
from typing import Protocol
import cairo as c
from PIL import Image
import cv2
from numpy import array
from itertools import batched
import moviepy as mp

import math

read_audio_data = lambda path: wavfile.read(path) # samplerate, data


class Pen:
    def __init__(self):
        self.surface = None
        
    def build_surface(self, width, height):
        self.surface = c.ImageSurface(c.Format.RGB24, width, height)
        self.context = c.Context(self.surface)

    def background(self, color):
        self.context.save()
        self.context.set_source_rgb(*color)
        self.context.paint()
        self.context.restore()

    def line(self, x, y, dx, dy, color):
        self.context.save()
        self.context.set_source_rgb(*color)
        self.context.move_to(x, y)
        self.context.line_to(dx, dy)
        self.context.stroke()
        self.context.restore()
        

    def export_image(self) -> Image:
        format = self.surface.get_format()
        size = (self.surface.get_width(), self.surface.get_height())
        stride = self.surface.get_stride()

        with self.surface.get_data() as memory:
            if format == c.Format.RGB24:
                return Image.frombuffer(
                    "RGB", size, memory.tobytes(),
                    'raw', "BGRX", stride)
            else:
                raise NotImplementedError(repr(format))


class VisualizationStrategy(Protocol):
    def visualize(self, width, height, data) -> Image:...

class Visualizer():
    def __init__(self, file:str, strategy: VisualizationStrategy):
        self.width = 500
        self.height = 500
        self.file_name = file.split(".")[0]
        self.sample_rate, self.data = read_audio_data(file)
        self.strategy = strategy
        self.frame_rate = 60
    
    def reattach_audio(self):
        my_clip = mp.VideoFileClip(f'{self.file_name}.avi')
        audio_background = mp.AudioFileClip(f'{self.file_name}.wav')
        finished:mp.VideoClip = my_clip.with_audio(audio_background)
        finished.write_videofile(f"./{self.file_name}.mp4")


    def renderFrame(self, data) -> Image:
        return self.strategy.visualize(self.width, self.height, data)
    
    def render(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')    
        video = cv2.VideoWriter(f"{self.file_name}.avi",fourcc, 60,(self.width,self.height))
        
        samples_per_frame = self.sample_rate//self.frame_rate
        for frame_data in batched(self.data, samples_per_frame):
            frame = self.renderFrame(frame_data)
            video.write(cv2.cvtColor(array(frame), cv2.COLOR_RGB2BGR))
  
        video.release()
        self.reattach_audio()

    def debug_render(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')    
        video = cv2.VideoWriter(f"{self.file_name}.avi",fourcc, 60,(self.width,self.height))
        
        samples_per_frame = self.sample_rate//self.frame_rate
        for frame_data in batched(self.data, samples_per_frame):
            frame = self.renderFrame(frame_data)
            video.write(cv2.cvtColor(array(frame), cv2.COLOR_RGB2BGR))
            break
        video.release()
        # self.reattach_audio()
            

class ClassicLine():
    def visualize(self, width, height, data)->Image:        
        p = Pen()
        p.build_surface(width, height)
        p.background((0,0,0))
        
        sample_step = 1
        past_y = 0
        cursor_x = 0
        for d in data:
            delta = d/500
            p.line(cursor_x, height/2+past_y, cursor_x+sample_step, height/2+delta, (1,1,1))
            cursor_x += sample_step
            past_y = delta        
        return p.export_image()

class ClassicCircle():
    def visualize(self, width, height, data)->Image:        
        p = Pen()
        p.build_surface(width, height)
        p.background((0,0,0))
        
        sample_step = 1
        center = (width/2, height/2)
        
        base_radius = 100
        
        past_y = 0
        past_x = base_radius
        
        
        duration = len(data)
        for i, d in enumerate(data):
            t = i/duration
            ang = t*360
            
            delta = d/500
            x = math.cos(math.radians(ang))*(delta+base_radius)
            y = math.sin(math.radians(ang))*(delta+base_radius)
            
            p.line(center[0]+past_x, center[1]+past_y, center[0]+x, center[1]+y, (1,1,1))    
            past_x = x
            past_y = y
              
        return p.export_image()