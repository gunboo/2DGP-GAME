from pico2d import *
import game_framework
import game_world
from background import Background
from character import Character
from boss import Boss

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for obj in game_world.all_objects():
                obj.handle_event(event)


def init():
    global background, character, boss

    background = Background() #배경 오브젝트
    game_world.add_object(background,0) #레이어 0

    character = Character()
    game_world.add_object(character, 1) #레이어 1

    boss = Boss()
    game_world.add_object(boss,2) #레이어 2

def finish():
    game_world.clear() #모든 오브젝트 제거

def update():
    game_world.update() #모든 오브젝트의 update호출

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

