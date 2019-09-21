import pygame
import random
import math

from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Objects.Text import Text
from PyGE.Screens.Room import Room
from PyGE.Globals.Cache import get_image
from PyGE.Misc.AlarmClock import AlarmClock
import PyGE.utils as utils
import source.GlobalVariable as GlobalVariable
from source.Objects.Player import Player



class EnemyHandler(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        args["@x"], args["@y"] = (-10, -10)
        ObjectBase.__init__(self, screen, args, parent)

        self.spawn_countdown = AlarmClock(0.2)
        self.spawn_countdown.start()

    def oncreate(self):
        GlobalVariable.score = 0

    def update(self, pressed_keys):
        if self.spawn_countdown.finished:
            self.spawn_countdown.restart()
            self.add_object("Enemy", {},  random.randint(0, self.screen_w ),-31)


class Enemy(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        ObjectBase.__init__(self, screen, args, parent)

        self.image = get_image("enemy")
        self.drawable = self.image

        self.w, self.h = self.image.get_size()

        self.angle = -90

        self.drawable = self.rotate_object(self.image, self.angle - 90)
        self.curAngle = self.angle -90
        self.velocity = 100

        self.scoreboard = self.get_all_type("Text")[0]     # type: Text

        self.screen_c_w, self.screen_c_h = utils.get_surface_center(self.screen)
        self.tPlayer = None

        self.PlayerList = [None,None]
        self.realAngle =0
        for obj in self.siblings:
            if(obj.object_type == "Player"):
                print(obj.get_num())
                if(obj.get_num()==1):
                    self.PlayerList[0] = obj
                    self.tPlayer = obj    
                    
                else:
                    self.PlayerList[1] = obj
        self.tPlayer = self.PlayerList[random.randint(0,1)]


    def update(self, pressed_keys):
        self.updateAngle()
        self.move_angle_time(self.velocity,self.realAngle)
        
        
    # for keep changing angle
    def updateAngle(self):
        if(self.tPlayer != None):
            if(Player.get_y(self.tPlayer) == self.y):
                
                print( self.tPlayer )
            else:
                self.curAngle =  math.degrees( math.atan((Player.get_x(self.tPlayer)  - self.x)/(Player.get_y(self.tPlayer)  - self.y)))
                self.realAngle = self.angle + self.curAngle
                if(self.realAngle > 180 ): self.realAngle -= 360
                elif (self.realAngle < -180): self.realAngle += 360
                self.drawable = self.rotate_object(self.image, self.realAngle)
    

    def oncollide(self, obj:'ObjectBase'):
        if obj.object_type == "Bullet":
            self.delete(self)
            self.delete(obj)

            self.change_score(100)

    def onscreenleave(self):
        self.delete(self)
        self.change_score(-50)

    def draw(self):
        self.draw_to_screen(item=self.drawable)

    def change_score(self, delta:int):
        GlobalVariable.score += delta
        self.scoreboard.set_text("Score: {}".format(GlobalVariable.score))
