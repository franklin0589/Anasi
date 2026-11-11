from abc import ABC, abstractmethod

class Shot(ABC):
    _shots:list["Shot"] = []

    def __init__(self, duration:int = 0):
        self.duration:int = duration # Duration of the shot in seconds
        self.fps:int = 24 # Frames per second

    def __init_subclass__(cls, **kwargs):
        Shot._shots.append(cls())
        super().__init_subclass__(**kwargs)

    @staticmethod
    def render():
        """Render all shots in the _shots list."""
        for shot in Shot._shots:
            for frame in shot.render_frame():
                yield frame

    def get_frame_count(self) -> int:
        """Calculate the total number of frames in the shot based on duration and fps."""
        return self.duration * self.fps

    def set_fps(self, fps:int):
        """Set the frames per second for the shot."""
        self.fps = fps

    @abstractmethod
    def build(self, frame_number:int):
        """Build the shot. This method should be implemented by subclasses."""
        pass

    def get_frame(self, frame_number:int):
        """Retrieve a specific frame from the shot based on the frame number."""
        if frame_number < 0 or frame_number >= self.get_frame_count():
            raise ValueError("Frame number out of range.")
        # Placeholder for actual frame retrieval logic
        return self.build(frame_number)
    
    def render_frame(self):
        """Render all frames of the shot."""
        for frame_number in range(self.get_frame_count()):
            yield self.get_frame(frame_number)