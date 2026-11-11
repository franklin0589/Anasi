from .maths import *
from .drawing import *

class Object:
    def __init__(self, world_position, orientation, points, indices):
        self.position = world_position
        self.orientation = orientation
        self.points = points
        self.indices = indices
    def get_points(self):
        points = []
        for point in self.points:
            # new_point = mat3D_rotate(point, *u_hvec(self.position))
            new_point = mat3D_translate(h_vec3(point), *uvec(self.position))
            points += [new_point]
        return points

class World:
    def __init__(self):
        # self.locations = {
        #     "origin":Object(Vector3D(0,0,0), Vector3D(0,0,0)),
        #     "screen":Object(Vector3D(0,0,10), Vector3D(0,0,0))
        # }
        ...

    def add_object(self, object, position = Vector3D(0,0,0)):
        self.locations[object] = position

    def move(self, object, x=0, y=0, z=0):
        for i, offset in enumerate([x,y,z]):
            origin = self.locations[object].position[i]
            self.locations[object].position[i] = origin + offset

class Screen:
    def __init__(self, width, height):
        self.dimensions = (width, height)
        self.focal_length = 40

    def project(self, points):
        screen_points = []
        for point in points:
            scale = perspective(self.focal_length, point[2])
            screen_points.append(Vector2D(point[0]*scale, point[1]*scale))        
        return screen_points

    def draw_polyline(self, context, screen_points, indices):
        context.move_to(*screen_points[indices[0]])
        for i in indices[1:]:
            context.line_to(*screen_points[i])
        context.stroke()

    def draw_object(self, context, object, indices):
        context.save()
        context.set_line_width(0.3)
        context.set_source_rgba(*(0, 0.8, 0, 1))
        screen_points = self.project(object) 
        for index in indices:
            self.draw_polyline(context, screen_points, index)

class StageManager():
    def __init__(self):
        self.world = World()
        self.objects = []
        
    def new_object(self, world_position, orientation, points, indices):
        self.objects += [Object(world_position, orientation, points, indices)]
    
    def render(self, context):
        new_screen = Screen(400,400)

        for object in self.objects:
            new_screen.draw_object(context, object.get_points(), object.indices)
        ...
