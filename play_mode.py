from pico2d import *
import game_framework
import game_world
from background import Background
from character import Character
from boss import Boss, Dead
from hp_bar import HPBarUI,HPBar, MPBar, ExpBar, BossHPBar
from Tile import Tile

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
    global background, character, boss, hp_bar, mp_bar, exp_bar, hp_bar_ui, boss_hp_bar, tiles

    background = Background()  # 배경 추가
    game_world.add_object(background, 0)  # 레이어 0

    tiles = [
        Tile(400, 200, 269, 317, 90, 57)
    ]
    for tile in tiles:
        game_world.add_object(tile, 1)  # 타일은 레이어 1

    character = Character()  # 플레이어 캐릭터 추가
    game_world.add_object(character, 2)  # 레이어

    boss = Boss(character)  # 보스 추가
    game_world.add_object(boss, 3)  # 레이어

    hp_bar_ui = HPBarUI()

    hp_bar = HPBar()
    mp_bar = MPBar()
    exp_bar = ExpBar()

    boss_hp_bar = BossHPBar(boss)

def check_collision(box1, box2):
    """충돌 체크"""
    left1, bottom1, right1, top1 = box1
    left2, bottom2, right2, top2 = box2

    return not (right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1)

def finish():
    game_world.clear()

def update():
    current_time = get_time()
    game_world.update()

    hp_bar.update(character.hp)
    mp_bar.update(character.mp)

    if boss.hp<= 0 and boss.state_machine.current_state != Dead:
        boss.state_machine.change_state(Dead)
    else:
        boss_hp_bar.update(boss.hp)

    if check_collision(character.get_bb(), boss.get_bb()):
        if current_time - character.last_damage_time >= 1.0:  # 1초 딜레이
            knockback_dir = -1 if character.x < boss.x else 1  # 넉백 방향
            character.take_damage(0.1, knockback_dir)  # 데미지 적용
            character.last_damage_time = current_time  # 마지막 데미지 시간 업데이트
    else:
        character.last_damage_time = 0  # 충돌 해제 시 초기화

    attack_hitbox = character.get_attack_hitbox()
    if attack_hitbox and check_collision(attack_hitbox, boss.get_bb()):
        boss.take_damage(0.1)  # 보스 HP 감소
        delay(0.1)

    for tile in tiles:
        if check_collision(character.get_bb(), tile.get_bb()):
           character.y = tile.get_bb()[3] + 20  # 타일 위로 이동
           character.velocity_y = 0  # 점프 중단


def draw():
    clear_canvas()

    game_world.render()

    hp_bar_ui.draw()
    hp_bar.draw()
    mp_bar.draw()
    exp_bar.draw()
    boss_hp_bar.draw()
    #character.draw_bb()
    character.draw_attack_hitbox()
    #boss.draw_bb()

    update_canvas()

def pause():
    pass

def resume():
    pass
