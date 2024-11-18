from pico2d import *
import game_framework
import game_world
from background import Background
from character import Character
from boss import Boss
from hp_bar import HPBarUI,HPBar, MPBar, ExpBar

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)  # 캐릭터에만 이벤트 전달


def init():
    global background, character, boss, hp_bar, mp_bar, exp_bar, hp_bar_ui

    background = Background()  # 배경 추가
    game_world.add_object(background, 0)  # 레이어 0

    character = Character()  # 플레이어 캐릭터 추가
    game_world.add_object(character, 1)  # 레이어 1

    boss = Boss()  # 보스 추가
    game_world.add_object(boss, 2)  # 레이어 2

    hp_bar_ui = HPBarUI()
    hp_bar = HPBar()
    mp_bar = MPBar()
    exp_bar = ExpBar()

def finish():
    game_world.clear()

def update():
    game_world.update()

    hp_bar.update(character.hp)
    mp_bar.update(character.mp)

def draw():
    clear_canvas()

    game_world.render()

    hp_bar_ui.draw()
    hp_bar.draw()
    mp_bar.draw()
    exp_bar.draw()

    update_canvas()

def pause():
    pass

def resume():
    pass
