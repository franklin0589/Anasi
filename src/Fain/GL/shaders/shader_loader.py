class ShaderLoader:
    def __init__(self, ctx):
        self.ctx = ctx

    def load_from_files(self, vertex_path: str, fragment_path: str, geometry_path: str = None):
        with open(vertex_path, 'r') as f:
            vertex_src = f.read()

        with open(fragment_path, 'r') as f:
            fragment_src = f.read()

        geometry_src = None
        if geometry_path:
            with open(geometry_path, 'r') as f:
                geometry_src = f.read()

        return self._create_program(vertex_src, fragment_src, geometry_src)

    def _create_program(self, vertex_src, fragment_src, geometry_src=None):
        kwargs = {
            "vertex_shader": vertex_src,
            "fragment_shader": fragment_src,
        }
        if geometry_src:
            kwargs["geometry_shader"] = geometry_src

        try:
            return self.ctx.program(**kwargs)
        except Exception as e:
            print("Shader compilation error:", e)
            raise e
