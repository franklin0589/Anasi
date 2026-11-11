from PIL import Image

class VideoOut:
    def __init__(self, output_path:str):
        self.output_path = output_path
        self.out_count = 0
   
    def save(self, frames:list[Image.Image]):
        """Save the list of frames as a video file."""
        ...

class GifOut(VideoOut):
    def save(self, frames:list[Image.Image]):
        """Save the list of frames as a GIF file."""
        if not frames:
            raise ValueError("No frames to save.")
        self.out_count += 1

        out_name = self.output_path.split(".")[0] + str(self.out_count) + ".gif"
        frames[0].save(out_name, save_all=True, append_images=frames[1:], loop=0, duration=1000/24)  # Assuming 24 fps
