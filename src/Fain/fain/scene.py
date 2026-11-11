from .whiteboard import *
from time import sleep


class Scene:
    def __init__(self, shapes, instructions, next_scene):
        self.shapes = shapes
        self.instructions = instructions
        self.next_scene = next_scene

add_layer = lambda scene, shape: scene.shapes.append(shape) 
remove_layer = lambda scene, index: scene.shapes.pop(index) 
        
        
class SceneContext:
    def __init__(self, whiteboard):
        self.halt_time = 1
        self.whiteboard = whiteboard
        self.instructions = []
        self.shapes = []
        self.current_scene = None
        
    def clear(self):
        clear_canvas(self.whiteboard.canvas)

    def halt_frame(self, sec):
        sleep(sec)

    def run_scene(self, scene):
        self.shapes = scene.shapes
        for instruction in scene.instructions:
            self.draw()
            instruction()
        self.current_scene = scene.next_scene
    
    def draw(self):
        self.clear()
        for shape in self.shapes:
            print("Draw ",shape)
            shape.draw(self.whiteboard)
        # self.halt_frame(self.halt_time)
        
    def update(self, can):
        self.run_scene(self.current_scene)
        if self.current_scene != None:
            can.after(400*self.halt_time, lambda : self.update(can))  
        
halt=lambda x: lambda: sleep(x)

