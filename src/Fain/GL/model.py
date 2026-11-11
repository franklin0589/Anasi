import numpy as np
import trimesh
import base64
import struct
from Fain.GL.shaders.shader_loader import ShaderLoader


class GLTFModel:
    def __init__(self, path, ctx):
        self.ctx = ctx
        self.vbo = None
        self.vao = None
        self.program = None
        self.vertex_count = 0

        self.load(path)
        
    def load(self, path):
        scene = trimesh.load(path, force='scene')  # can also be .glb
        mesh = scene.dump(concatenate=True)

        # Prepare vertex and index data
        vertices = mesh.vertices.astype('f4')
        indices = mesh.faces.flatten().astype('i4')

        self.vbo = self.ctx.buffer(vertices.tobytes())
        ibo = self.ctx.buffer(indices.tobytes())

        self.program = ShaderLoader(self.ctx).load_from_files("src\\fain\\shaders\\vert.glsl", "src\\fain\\shaders\\frag.glsl")

        self.mvp = self.program.get("mvp", None)
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_position')],
            index_buffer=ibo
        )
    def render(self, mvp):
        if self.mvp:
            self.mvp.write(mvp.astype("f4").tobytes())
        self.vao.render()