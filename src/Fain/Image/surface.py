from typing import Optional, Any
import cairo as c

class RenderSurface:
    def __init__(self, width:int, height:int, cnf:dict):
        self.width:int = width
        self.height:int = height
        self.cnf:dict = cnf
        self.surface:Any = self.build()

    def build(self) -> Any:
        raise NotImplementedError("Error")

    def on(self) -> Any:
        if self.surface:
            return self.surface



class PSurface(RenderSurface):
    def __init__(self, width, height):
        cnf = {"format": c.Format.RGB24}
        super().__init__(width, height, cnf)

    def build(self):
        return c.ImageSurface(self.cnf["format"], self.width, self.height)

