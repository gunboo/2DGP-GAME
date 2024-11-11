from pico2d import *
from pymsgbox import password


class Boss:
    def __init__(self):
        self.image = load_image('boss_sprite.png')
        self.x, self.y = 1200,300
        self.frame = 0

    def update(self):
        self.frame =

    def draw(self):
        self.image.clip_draw()

    def handle_event(self,event):
        pass #음...