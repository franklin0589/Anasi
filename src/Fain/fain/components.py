from .whiteboard import *

class Art:
    def __init__(self, eqs):
        self.equations = eqs
    
    def draw(self, whiteboard):
        Shape(self.equations).draw(whiteboard)

class Guide:
    def __init__(self, eqs):
        self.equations = eqs 
        self.visibility = False
    def draw(self, whiteboard):
        Shape(self.equations).draw(whiteboard)
    


class Bone(Art):
    def __init__(self, x, y, x2, y2):
        self.origin = (x, y)
        self.end = (x2,y2)
        
        bone_instructs = [
            line(*self.origin, *self.end, 360),
            circle(20, *self.origin),
            circle(20, *self.end),
        ]
        super().__init__(bone_instructs)
    def draw(self, whiteboard):
        Shape(self.equations, 360).draw(whiteboard)
        


class Joint:
    def __init__(self, origin, radius, length):
        self.rotation = radius
        self.length = length
        self.origin = origin
        
    def update_final_position(self):
        self.new_distance = vec_add(self.origin, polar_cast(self.length, self.rotation))
        return self.new_distance
    def draw_bone(self, w):
        bone = Bone(*self.origin, *self.update_final_position() )
        bone.draw(w)
        
    def detect_joint(self):
        ...
    def rotate(self, delta:float):
        ...

#     def draw(self, canvas:PCanvas):
#             canvas.draw_circle(self.origin.x, self.origin.y, 10, fill='blue')


