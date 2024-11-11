from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.x, self.y = 800,300

    def update(self):
        pass #배경 동적 업데이트 아직 필요 X

    def draw(self):
        self.image.draw(self.x, self.y)