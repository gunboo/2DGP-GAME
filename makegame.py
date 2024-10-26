from pico2d import *
import random

class Hero: #Hero 클래스 생성
    def __init__(self):
        self.x, self.y = 0 , 90
        self.frame = 0
        self.image = load_image('.png')

    def update(self):
        self.frame = (self.frame + 1) % ?
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*?,?,100,100, self.x, self.y)

class Monster: #Monser 클래스 생성
    def __init__(self):
        self.x, self.y =

    def update(self):
def reset_world(): 
    global running
    global hero
    global world

    running = True
    world = []

    hero = Hero()
    world.append(hero)
    world.append(monster)

def update_world(): #업데이트
    hero.update()
    for o in world:
        o.update()

def render_world(): #렌더링
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()