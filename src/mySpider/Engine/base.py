import os
from itertools import chain
from mySpider.Shot import Shot
from mySpider.Engine.outTypes import GifOut
import av

class Engine:
    def __init__(self, name:str):
        self.name = name
        os.makedirs(f"export/{name}", exist_ok=True)
        self.outtype = "gif"  # Default output type

    def get_output_class(self, format:str):
        """Get the appropriate output class based on the format."""
        if format == "gif":
            return GifOut
        else:
            raise ValueError(f"Unsupported format: {format}")

    def run(self, output_path:str, format:str = "mp4"):
        """Run the engine to render all shots."""
        full_output_path = f"export/{self.name}/{output_path}"
        frames = iter(Shot.render())
        first_frame = next(frames, None)
        if first_frame is None:
            raise ValueError("No frames were rendered.")

        height, width = first_frame.shape[:2]
        with av.open(full_output_path, mode="w", hwaccel='cuda') as container:
            stream = container.add_stream(
                "libx264",
                rate=30,
                options={"preset": "ultrafast", "crf": "23"},
            )
            stream.width = width
            stream.height = height
            stream.pix_fmt = "yuv420p"

            for frame in chain((first_frame,), frames):
                video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
                for packet in stream.encode(video_frame):
                    container.mux(packet)

            for packet in stream.encode():
                container.mux(packet)

class MP4Engine(Engine):
    def __init__(self, name:str):
        super().__init__(name)
        self.outtype = "mp4"  # Set output type to mp4
        self.container = av.open(f"export/{name}.mp4", mode="w")


    def run(self, output_path:str, format:str = "mp4"):

        stream = self.container.add_stream("mpeg4", rate=24)
        stream.width = 1080
        stream.height =720
        stream.pix_fmt = "bgrp"

        for frame_i in Shot.render():
            frame = av.VideoFrame.from_ndarray(frame_i, format="rgb24")
            for packet in stream.encode(frame):
                self.container.mux(packet)
        # Flush stream
        for packet in stream.encode():
            self.container.mux(packet)

        # Close the file
        self.container.close()