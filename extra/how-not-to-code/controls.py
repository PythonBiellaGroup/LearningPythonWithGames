from abc import ABC, abstractmethod
import pygame

class Controls(ABC):
    @abstractmethod
    def get_x_dir(self):
        pass

    @abstractmethod
    def get_y_dir(self):
        pass

class KeyboardControls(Controls):
    def get_x_dir(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return -1
        elif keys[pygame.K_RIGHT]:
            return 1
        else:
            return 0

    def get_y_dir(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return -1
        elif keys[pygame.K_DOWN]:
            return 1
        else:
            return 0

class JoystickControls(Controls):
    def __init__(self, joystick_id):
        self.joystick = pygame.joystick.Joystick(joystick_id)

    def get_axis_dir(self, axis_id):
        axis_value = self.joystick.get_axis(axis_id)
        if abs(axis_value) < 0.5:
            return 0
        else:
            return 1 if axis_value > 0 else -1

    def get_x_dir(self):
        return self.get_axis_dir(0)

    def get_y_dir(self):
        return self.get_axis_dir(1)
