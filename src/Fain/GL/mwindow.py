import moderngl
import glfw
import numpy as np
from abc import ABC, abstractmethod
import time
import imageio

class MWindow(ABC):
    def __init__(self, width=800, height=800, title="DefaultMwindow", output = "output.mp4"):
        # Uninitialized
        self.window = None
        self.ctx = None
        
        # Parameter Initialized
        self.title = title
        self.output_path = output
        self.width = width
        self.height = height
        self.delta_time = time.time()
        
        # Function Initialized
        self.last_time = 0
        self.keys = set()
        self._init_window()
        self._init_context()
        self._init_recorder()
        self.init()  # Subclass-specific setup

    def _init_window(self):
        if not glfw.init():
            raise RuntimeError("GLFW initialization failed")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)
        # Optional: set input callbacks
        glfw.set_key_callback(self.window, self._on_key)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos_callback(self.window, self._on_mouse_move)
        self.first_mouse = True
        self.last_x, self.last_y = self.width // 2, self.height // 2

    def _init_context(self):
        self.ctx = moderngl.create_context()
        self.ctx.viewport = (0, 0, self.width, self.height)

    def _on_resize(self, window, width, height):
        self.width = width
        self.height = height
        self.ctx.viewport = (0, 0, width, height)
        self.on_resize(width, height)

    def _on_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys.add(key)
        elif action == glfw.RELEASE:
            self.keys.discard(key)

    def _on_mouse_move(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # reversed: y goes down

        self.last_x = xpos
        self.last_y = ypos

        if hasattr(self, 'camera'):
            self.camera.process_mouse_movement(xoffset, yoffset)
    
    
    def run(self, duration_seconds=5):
        frame_count = int(duration_seconds * 60)

        for _ in range(frame_count):
            glfw.poll_events()
            capture_time = time.time()
            self.delta_time = capture_time - self.last_time
            self.last_time = capture_time
            if self.update() == -1:
                break
            self.render_frame()
            glfw.swap_buffers(self.window)

        self.writer.close()
        self.cleanup()
        glfw.terminate()
        print(f"Video saved to {self.output_path}")
    
    def _init_recorder(self):
        self.writer = imageio.get_writer(
            self.output_path,
            fps=60,
            codec='libx264',
            quality=8
        )
    def update(self):
        """Optional: override for per-frame logic."""
        pass

    @abstractmethod
    def init(self):
        """Override to initialize resources (shaders, buffers, etc.)."""
        pass

    @abstractmethod
    def render(self):
        """Override to draw per frame."""
        pass
    
    def render_frame(self):
        self.render()
        pixels = self.ctx.screen.read(components=3, alignment=1)
        image = np.frombuffer(pixels, dtype=np.uint8).reshape((self.height, self.width, 3))
        image = np.flipud(image)  # Flip vertically

        self.writer.append_data(image)

    def on_resize(self, width, height):
        """Optional: override for window resize handling."""
        pass

    def cleanup(self):
        """Optional: override for resource cleanup."""
        pass