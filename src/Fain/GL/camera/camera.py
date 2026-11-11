import numpy as np
from pyrr import Matrix44, Vector3


class Camera:
    def __init__(self, position=(0, 0, 10), target=(0, 0, 0), up=(0, 1, 0), fov=90, aspect=4/3, near=0.1, far=450.0):
        self.position = Vector3(position)
        self.front = Vector3([0, 0, -1])
        self.up = Vector3(up)
        self.right = Vector3([1, 0, 0])
        self.world_up = Vector3(up)

        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 120
        self.sensitivity = 0.1
        self.zoom = fov

        self.aspect = aspect
        self.near = near
        self.far = far

        self._update_vectors()

    def get_view_matrix(self):
        return Matrix44.look_at(self.position, self.position + self.front, self.up)

    def get_projection_matrix(self):
        return Matrix44.perspective_projection(self.zoom, self.aspect, self.near, self.far)

    def process_keyboard(self, direction, delta_time):
        velocity = self.speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            print(self.front*velocity)
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity
        print(self.position)
        
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            self.pitch = max(-89.0, min(89.0, self.pitch))

        self._update_vectors()

    def _update_vectors(self):
        front = Vector3([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
        ])
        self.front = front.normalized
        self.right = self.front.cross(self.world_up).normalized
        self.up = self.right.cross(self.front).normalized