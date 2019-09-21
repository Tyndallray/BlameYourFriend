import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room

class Bullet(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)
        self.angle = self.get_mandatory_arguement("angle", float)
        self.velocity = self.get_optional_arguement("velocity", 200, float)
        self.radius = 1

        self.w = self.radius * 2
        self.h = self.radius * 2

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)

    def update(self, pressed_keys):
        self.move_angle_time(self.velocity)

    def onscreenleave(self):
        self.delete(self)