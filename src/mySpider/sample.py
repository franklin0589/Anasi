from mySpider.Shot import Shot
from mySpider.Engine import MP4Engine, Engine
from PIL import Image, ImageDraw
import time
import numpy as np

class IntroductionShot(Shot):
    def __init__(self):
        self.base_image = Image.new("RGB", (1920, 1080), color=(255, 255, 255))
        self.array = np.array(self.base_image) # Placeholder for actual frame content
        super().__init__(20)

    def build(self, frame_number:int):
        """Build the introduction shot."""
        # Implementation for building the introduction shot
        # image = self.base_image.copy()
        return self.array

if __name__ == "__main__":
    start = time.time()
    engine = Engine("test_engine")
    engine.run("output.mp4", format="mp4")
    print(f"Rendering completed in {time.time() - start:.2f} seconds.")
