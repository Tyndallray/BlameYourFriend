import pygame

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image
from PyGE.Misc.AlarmClock import AlarmClock
import source.GlobalVariable as GlobalVariable
import PyGE.utils as utils
import math


class Player(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)

        self.respawn_countdown = AlarmClock(5.0)
        self.respawn_countdown.start()
        self.isDead = False

        self.angle = 90
        self.velocity = 5

        self.number = self.get_mandatory_arguement("number", int)

        self.image = self.rotate_object(get_image("player{}".format(self.number)))

        self.w, self.h = self.image.get_size()

        self.shot_cool_down = AlarmClock(0.125)
        self.shot_cool_down.start()

        self.display_image = self.image
        self.angle = 0

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
            self.move_angle(-self.velocity,self.angle)
            self.boundary_check()

        if (pressed_keys[pygame.K_s] == 1 and self.number == 1) or (pressed_keys[pygame.K_DOWN] == 1 and self.number == 2) and self.isDead == False:
            self.move_angle(self.velocity,self.angle)
            self.boundary_check()

        if self.shot_cool_down.finished and self.isDead == False:
            self.add_object("Bullet", {"angle": self.angle + 90}, x=self.x, y=self.bullet_y)
            self.shot_cool_down.restart()
       
       

        if (pressed_keys[pygame.K_a] == 1 and self.number == 1) or (pressed_keys[pygame.K_LEFT] == 1 and self.number == 2):
            # self.time_move(self.velocity,0)
            self.angle += 1.5708
            self.display_image = self.rotate_object(self.image,self.angle)
            # slef.rotate_object(sel.image,)
            self.boundary_check()

        if (pressed_keys[pygame.K_d] == 1 and self.number == 1) or (pressed_keys[pygame.K_RIGHT] == 1 and self.number == 2):
            self.angle -= 1.5708
            self.display_image = self.rotate_object(self.image,self.angle)
            # slef.rotate_object(sel.image,)
            self.boundary_check()

        if self.shot_cool_down.finished:
            print("angle")
            print(self.angle)
            angleStore = self.angle
            temp = angleStore/360
            temp1 = math.floor(temp)
            print("temp1")
            print(temp1)
            if(temp1 < 0):
                temp1 = temp1 + 1
                print(temp1)
            temp2 = temp - temp1
            temp = 360*temp2
            print("temp")
            print(temp)
            if(temp<0):
                if(temp > -45 and temp <= 0):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y)
                elif(temp >= -90 and temp <= -45):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y-(self.h/2))
                elif(temp >= -135 and temp < -90):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+(self.w/2), y=self.bullet_y-(self.h/2))
                elif(temp >= -180 and temp < -135):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+self.w, y=self.bullet_y)
                elif(temp >= -225 and temp < -180):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+self.w, y=self.bullet_y+(self.h/2))
                elif(temp >= -270 and temp < -225):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+(self.w/2), y=self.bullet_y+(self.h/2))
                elif(temp >= -315 and temp < -270):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y+(self.h/2))
                elif(temp >= -360 and temp < -315):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y)
                self.shot_cool_down.restart()
            elif (temp>0):
                if(temp < 45 and temp >= 0):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y)
                elif(temp <= 90 and temp >= 45):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y+(self.h/2))
                elif(temp <= 135 and temp > 90):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+(self.w/2), y=self.bullet_y+(self.h/2))
                elif(temp <= 180 and temp > 135):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+self.w, y=self.bullet_y+(self.h/2))
                elif(temp <= 225 and temp > 180):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+self.w, y=self.bullet_y)
                elif(temp <= 270 and temp > 225):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x+(self.w/2), y=self.bullet_y-(self.h/2))
                elif(temp <= 315 and temp > 270):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y-(self.h/2))
                elif(temp <= 360 and temp > 315):
                    self.add_object("Bullet", {"angle": self.angle + 180}, x=self.x, y=self.bullet_y)
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
