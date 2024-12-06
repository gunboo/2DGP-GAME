from pico2d import *
import game_framework
import game_world
from background import Background
from character import Character
from boss import Boss, Dead
from hp_bar import HPBarUI, HPBar, MPBar, ExpBar, BossHPBar
from Tile import Tile
from portal import Portal
from next_map import NextMap
import next_map

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:  # 위키를 눌렀을 때
            if check_collision(character.get_bb(), portal.get_bb()):  # 포탈과 충돌했을 때
                game_framework.change_state(next_map.NextMap())  # 다음 맵으로 이동
                return
        else:
            character.handle_event(event)  # 캐릭터에 이벤트 전달


def init():
    global background, character, boss, hp_bar, mp_bar, exp_bar, hp_bar_ui, boss_hp_bar, tiles, portal,npcs

    # 배경 추가
    background = Background()
    game_world.add_object(background, 0)  # 레이어 0

    # 포탈 추가
    portal = Portal(100, 90)  # 포탈 위치
    game_world.add_object(portal, 1)  # 레이어 1

    # 타일 추가
    tiles = [
        Tile(400, 200, 269, 317, 90, 57),
        Tile(600, 300, 269, 317, 90, 57)  # 추가 타일 예시
    ]
    for tile in tiles:
        game_world.add_object(tile, 2)  # 타일은 레이어 2

    # 캐릭터 추가
    character = Character()
    game_world.add_object(character, 3)  # 레이어 3

    # 보스 추가
    boss = Boss(character)
    game_world.add_object(boss, 4)  # 레이어 4

    # HP/MP/EXP 바 및 UI 추가
    hp_bar_ui = HPBarUI()
    hp_bar = HPBar()
    mp_bar = MPBar()
    exp_bar = ExpBar()
    boss_hp_bar = BossHPBar(boss)


def check_collision(box1, box2):
    """충돌 체크"""
    if not box1 or not box2:
        return False

    left1, bottom1, right1, top1 = box1
    left2, bottom2, right2, top2 = box2

    return not (right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1)


def finish():
    game_world.clear()

def enter():
    """플레이 모드 초기화"""
    init()  # 초기화 함수 호출

def exit():
    """플레이 모드 종료"""
    finish()  # 리소스 정리
def update():
    current_time = get_time()
    game_world.update()

    # UI 업데이트
    hp_bar.update(character.hp)
    mp_bar.update(character.mp)


    # 보스의 상태 업데이트
    if boss.hp <= 0 and boss.state_machine.current_state != Dead:
        boss.state_machine.change_state(Dead)
    else:
        boss_hp_bar.update(boss.hp)

    # 캐릭터와 보스 충돌 체크
    if check_collision(character.get_bb(), boss.get_bb()):
        if current_time - character.last_damage_time >= 1.0:  # 1초 딜레이
            knockback_dir = -1 if character.x < boss.x else 1  # 넉백 방향
            character.take_damage(0.1, knockback_dir)  # 데미지 적용
            character.last_damage_time = current_time  # 마지막 데미지 시간 업데이트
    else:
        character.last_damage_time = 0  # 충돌 해제 시 초기화

    # 캐릭터 공격 히트박스와 보스 충돌 체크
    attack_hitbox = character.get_attack_hitbox()
    if attack_hitbox and check_collision(attack_hitbox, boss.get_bb()):
        boss.take_damage(0.0005)  # 보스 HP 감소
        delay(0.1)

    # 캐릭터와 타일 충돌 체크
    for tile in tiles:
        if check_collision(character.get_bb(), tile.get_bb()):
            character.y = tile.get_bb()[3] + 20  # 타일 위로 이동
            character.velocity_y = 0  # 점프 중단
            character.is_on_tile = True
            break
    else:
        character.is_on_tile = False  # 타일과 충돌하지 않은 경우

    if boss.effect_active:  # 보스가 공격 중일 때
        attack_hitbox = boss.get_attack_hitbox()
        if check_collision(attack_hitbox, character.get_bb()):
            if not boss.damage_dealt:  # 이미 데미지를 준 상태가 아니면
                character.take_damage(0.1, -1)  # 캐릭터 HP 감소
                boss.damage_dealt = True  # 데미지를 준 상태로 표시


def draw():
    clear_canvas()

    # 렌더링
    game_world.render()

    # UI 그리기
    hp_bar_ui.draw()
    hp_bar.draw()
    mp_bar.draw()
    exp_bar.draw()
    boss_hp_bar.draw()

    # 디버깅용 박스 그리기
    character.draw_attack_hitbox()
    portal.draw_bb()

    update_canvas()


def pause():
    pass


def resume():
    pass

def exit():
    game_world.clear()