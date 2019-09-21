import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image
from PyGE.Misc.AlarmClock import AlarmClock
import source.GlobalVariable as GlobalVariable
import PyGE.utils as utils


class Player(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)

        self.respawn_countdown = AlarmClock(5.0)
        self.respawn_countdown.start()
        self.isDead = False

        self.angle = 90
        self.velocity = 100

        self.number = self.get_mandatory_arguement("number", int)

        self.image = self.rotate_object(get_image("player{}".format(self.number)))

        self.w, self.h = self.image.get_size()

        self.shot_cool_down = AlarmClock(0.125)
        self.shot_cool_down.start()

    @property
    def bullet_y(self):
        return self.y + (self.h / 2)

    def draw(self):
        if(self.isDead == False):
            self.draw_to_screen(self.image)

    def update(self, pressed_keys):
        
        if(self.isDead == True and self.respawn_countdown.finished == True):
            GlobalVariable.gameOver = False
            self.isDead = False
            print("Respawn")

        if (pressed_keys[pygame.K_w] == 1 and self.number == 1) or (pressed_keys[pygame.K_UP] == 1 and self.number == 2) and self.isDead == False:
            self.time_move(0, self.velocity)
            self.boundary_check()

        if (pressed_keys[pygame.K_s] == 1 and self.number == 1) or (pressed_keys[pygame.K_DOWN] == 1 and self.number == 2) and self.isDead == False:
            self.time_move(0, -self.velocity)
            self.boundary_check()

        if self.shot_cool_down.finished and self.isDead == False:
            self.add_object("Bullet", {"angle": self.angle + 90}, x=self.x, y=self.bullet_y)
            self.shot_cool_down.restart()

    def boundary_check(self):
        if not utils.rect_a_in_b(self.rect, self.screen.get_rect()):
            self.undo_last_move()

    def onkeydown(self, unicode, key, modifier, scancode):
        if key == 27:
            self.change_room("menu")

    def oncollide(self, obj:'ObjectBase'):
        if(obj.object_type == 'Enemy'):
            if(self.isDead == False):
                self.die()

    def die(self):
        self.isDead = True
        # print("Player dead" + str(GlobalVariable.gameOver))
        if(GlobalVariable.gameOver == True):
            # Game Over
            print("Game over")
            self.parent.attempt_quit()
        else:
            self.respawn_countdown = AlarmClock(5.0)
            self.respawn_countdown.start()
            GlobalVariable.gameOver = True
