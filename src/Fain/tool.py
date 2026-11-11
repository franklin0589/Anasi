from PIL import Image
from pathlib import Path


class SheetCuttingService:
    def __init__(self, image_path):
        self.path = Path(image_path)
        self.image = Image.open(image_path)
        
    def pull(self, x:int, y:int, w:int, h:int):
        return self.image.crop((x,y,x+w,y+h))
    def clip(self, box:tuple, save_path:str):
        region = self.image.crop(box)
        region.save(save_path)
        return region
    
    def pull_grid(self, dimwidth, dimheight):
        index = 0
        for x in range(0, self.image.width, dimwidth):
            for y in range(0, self.image.height, dimheight):
                index += 1
                cr = self.pull(x, y, dimwidth, dimheight)
                output_path = self.get_appendix(f"grid_{index}")
                cr.save(output_path)
    
    def get_appendix(self, appendix):
        t = Path(self.path.parent)
        stem = self.path.stem
        return t.joinpath(f"{stem}_{appendix}.png")
        
    
    def vhalf_clip(self, percentage = 0.5):
        width = self.image.width
        height = self.image.height
        self.clip((0,0,int(width*percentage), height), self.get_appendix("left"))
        self.clip((int(width*percentage), 0, width, height), self.get_appendix("right"))
    
class SpriteSheet:
    def __init__(self):
        self.image = ...
    

