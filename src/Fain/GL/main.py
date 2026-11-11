import moderngl
import numpy as np
from Fain.GL.mwindow import MWindow
from Fain.GL.shaders.shader_loader import ShaderLoader
from pyrr import Matrix44
from Fain.GL.model import GLTFModel
from Fain.GL.camera.camera import Camera
import glfw
import trimesh

class Starter(MWindow):
    def init(self):

        self.model = GLTFModel("rock.gltf", self.ctx)
        self.camera = Camera(aspect=self.width / self.height)

        # Model matrix (identity here)
        # self.model = Matrix44.identity()

    def update(self):
        if glfw.KEY_W in self.keys:
            self.camera.process_keyboard("FORWARD", self.delta_time)
        if glfw.KEY_S in self.keys:
            self.camera.process_keyboard("BACKWARD", self.delta_time)
        if glfw.KEY_A in self.keys:
            self.camera.process_keyboard("LEFT", self.delta_time)
        if glfw.KEY_D in self.keys:
            self.camera.process_keyboard("RIGHT", self.delta_time)
        if glfw.KEY_ESCAPE in self.keys:
            return -1
    
    def render(self):
    
        projection = trimesh.transformations.projection_matrix(fovy=np.radians(60.0), aspect=self.camera.aspect, znear=0.1, zfar=100.0)
        model = trimesh.transformations.translation_matrix([0, 0, -3])
        self.model.program['projection'].write(projection)
        self.model.program['model'].write(model.tobytes())
        
        self.ctx.clear(0.1, 0.1, 0.1)
        self.model.render()


if __name__ == "__main__":
    Starter().run(duration_seconds=30)