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

def check_collision(box1, box2):
    left1, bottom1, right1, top1 = box1
    left2, bottom2, right2, top2 = box2

    # 두 박스가 겹치면 충돌
    return not (right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1)

def finish():
    game_world.clear()

def update():
    current_time = get_time()
    game_world.update()

    hp_bar.update(character.hp)
    mp_bar.update(character.mp)

    if check_collision(character.get_bb(), boss.get_bb()):
        if current_time - character.last_damage_time >= 1.0:  # 1초 딜레이
            knockback_dir = -1 if character.x < boss.x else 1  # 넉백 방향
            character.take_damage(0.1, knockback_dir)  # 데미지 적용
            character.last_damage_time = current_time  # 마지막 데미지 시간 업데이트
    else:
        character.last_damage_time = 0  # 충돌 해제 시 초기화
def draw():
    clear_canvas()

    game_world.render()

    hp_bar_ui.draw()
    hp_bar.draw()
    mp_bar.draw()
    exp_bar.draw()

    character.draw_bb()
    boss.draw_bb()

    update_canvas()

def pause():
    pass

def resume():
    pass
