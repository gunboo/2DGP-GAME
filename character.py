from pico2d import *
import game_framework
from state_machine import StateMachine, left_down, left_up, right_down, right_up, ctrl_down, shift_down, alt_down
from hp_bar import HPBar,HPBarUI, MPBar,ExpBar
import boss
from Tile import Tile
import game_world
FRAMES_PER_ACTION = 8
ACTION_PER_TIME = 1.0 / 1.0
RUN_SPEED_PPS = 200
from boss import Boss
import play_mode

class Character:
    def __init__(self):
        self.x, self.y = 400, 90
        self.hp = 1.0
        self.mp = 1.0
        self.hp_bar = HPBar()
        self.mp_bar = MPBar()
        self.last_damage_time = 0  # 마지막으로 데미지를 받은 시간 (초)
        self.is_knocked_back = False  # 넉백 상태
        self.knockback_timer = 0  # 넉백 지속 시간
        self.attack_active = False  # 공격 상태 플래그
        self.attack_range = 50  # 공격 히트박스 범위
        self.gravity = -1000
        self.velocity_y = 0
        self.velocity_x = 0
        self.tile_underneath = None
        self.is_on_tile = False
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {alt_down: Jump, right_down: Walk, left_down: Walk, ctrl_down: Attack1, shift_down: Attack2},
                Walk: {right_up: Idle, left_up: Idle, ctrl_down: Attack1, shift_down: Attack2, alt_down: Jump},
                Attack1: {left_up: Idle, right_up: Idle},
                Attack2: {left_up: Idle, right_up: Idle},
                Jump: {},
            }
        )

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def take_damage(self, damage, knockback_dir):
        """피해를 입을 때 HP 감소 및 넉백"""
        if not self.is_knocked_back:  # 이미 넉백 중이면 중복 적용 안 함
            self.hp = max(0, self.hp - damage)
            self.hp_bar.update(self.hp)
            print(f"Character HP: {self.hp}")

            self.is_knocked_back = True
            self.knockback_timer = 0.5  # 넉백 지속 시간 (0.5초)
            self.knockback_dir = knockback_dir  # 넉백 방향 (-1: 왼쪽, 1: 오른쪽)
            self.state_machine.change_state(Hurt)

    def use_mana(self, amount):
        self.mp = max(0, self.mp - amount)
        self.mp_bar.update(self.mp)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(event)

    def draw(self):
        self.state_machine.draw()
        self.hp_bar.draw()
        self.mp_bar.draw()

    def handle_collision(self, other):
        if isinstance(other, boss.Boss):
            if self.state_machine.current_state != Hurt:  # 현재 Hurt 상태가 아니면
                self.state_machine.change_state(Hurt)  # Hurt 상태로 전환

    def attack(self, boss):
        if isinstance(boss, boss.Boss):
            boss.take_damage(0.01)  # 보스 HP를 0.1 감소
            print(f"Boss HP after attack: {boss.hp}")

    def get_attack_hitbox(self):
        if self.attack_active:
            if self.face_dir == 1:  # 오른쪽
                return self.x, self.y - 20, self.x + 50, self.y + 20
            else:  # 왼쪽
                return self.x - 50, self.y - 20, self.x, self.y + 20
        return None

    def draw_attack_hitbox(self):
         attack_hitbox = self.get_attack_hitbox()
         #if attack_hitbox:
             #draw_rectangle(*attack_hitbox)  # 사각형으로 히트박스 표시
class Idle:

    @staticmethod
    def enter(character, event=None):
        if character.dir != 0:
            character.face_dir = character.dir
        character.frame = 0
        if event and right_down(event):
            character.dir = 1  # 오른쪽으로 이동
        elif event and left_down(event):
            character.dir = -1  # 왼쪽으로 이동
        character.action = 1  # Walk 액션 설정
    @staticmethod
    def exit(character):
        character.face_dir = character.dir

    @staticmethod
    def do(character):
        # frame_time 기반 애니메이션 업데이트
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

    @staticmethod
    def draw(character):
        frame_width = 84
        frame_height = 80

        col = int(character.frame)
        y_position = character.image.h - 80  # 첫 줄의 Idle 모션

        if character.face_dir == 1:  # 오른쪽 바라보기
            character.image.clip_composite_draw(
                col * frame_width,
                y_position,
                frame_width,
                frame_height,
                0,  # 회전 각도
                'h',  # 수평 반전
                character.x,
                character.y,
                frame_width,
                frame_height
            )
        else:  # 왼쪽 바라보기
            character.image.clip_draw(
                col * frame_width,
                y_position,
                frame_width,
                frame_height,
                character.x,
                character.y
            )

class Walk:
    @staticmethod
    def enter(character, event=None):
        if event and right_down(event):
            character.dir = 1  # 오른쪽 이동
        elif event and left_down(event):
            character.dir = -1  # 왼쪽 이동

        character.action = 1  # Walk 액션 설정

        character.frame = 0  # Walk 상태 진입 시 첫 프레임으로 초기화

    @staticmethod
    def exit(character):
        if character.dir != 0:
            character.face_dir = character.dir

    @staticmethod
    def do(character):
        # 0~3 프레임 순환 (4프레임)
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time  # 캐릭터 이동


    @staticmethod
    def draw(character):
        frame_width = 84  # 프레임 너비
        frame_height = 80  # 프레임 높이
        col = int(character.frame)  # 현재 열 번호 (0~3)
        row = 2  # 걷는 모션이 3번째 줄(2번째 행)

        # Y 위치 조정 (캐릭터의 y축을 약간 위로 이동)
        y_position = character.image.h - (row + 1) * frame_height - 40  # 10px 위로 보정

        if character.dir == 1:
            character.image.clip_composite_draw(
                col * frame_width,  # 스프라이트의 열 시작 위치
                y_position,  # Y 위치
                frame_width,  # 프레임 너비
                frame_height,  # 프레임 높이
                0,  # 회전 각도
                'h',  # 수평 반전
                character.x,  # 출력 X 위치 (화면상의 위치)
                character.y,  # 출력 Y 위치 (화면상의 위치)
                frame_width,  # 실제 그릴 너비
                frame_height
            )
        else:
            character.image.clip_draw(
                col * frame_width + 5,  # 열에 따른 X 위치
                y_position,  # 보정된 Y 위치
                frame_width,  # 프레임 너비
                frame_height,  # 프레임 높이
                character.x,  # 출력 X 위치
                character.y  # 출력 Y 위치
        )

class Attack1:
    @staticmethod
    def enter(character, event=None):
        character.attack_active = True
        character.frame = 0  # 공격 시작 시 첫 프레임 초기화
        character.mp = max(0, character.mp - 0.1)
        character.has_hit = False  # 데미지를 준 상태인지 체크

    @staticmethod
    def exit(character):
        character.attack_active = False
        character.has_hit = False  # 상태 초기화

    @staticmethod
    def do(character):
        # 애니메이션 프레임 업데이트
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        character.mp_bar.update(character.mp)

        # 공격 범위 내에서 보스와 충돌 체크
        if not character.has_hit:  # 이미 데미지를 줬으면 더 이상 체크하지 않음
            for obj in game_world.all_objects():
                if isinstance(obj, Boss) and play_mode.check_collision(character.get_attack_hitbox(), obj.get_bb()):
                    obj.take_damage(0.000001)  # 보스에게 딱 한 번만 데미지 적용
                    print(f"Boss HP: {obj.hp}")
                    character.has_hit = True  # 데미지 적용 여부 기록

        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if character.frame >= 5:
            character.state_machine.change_state(Idle)

    @staticmethod
    def draw(character):
        frame_coordinates = [
            (15, 689, 76, 776),  # Frame 1
            (100, 689, 168, 776),  # Frame 2
            (171, 689, 249, 776),  # Frame 3
            (252, 689, 351, 787),  # Frame 4
            (354, 689, 454, 787),  # Frame 5
            (454, 689, 558, 787)  # Frame 6
        ]

        col = int(character.frame)
        x1, y1, x2, y2 = frame_coordinates[col]

        y_offset = 14  # Y축 보정값

        if character.face_dir == 1:  # 오른쪽 방향
            character.image.clip_composite_draw(
                x1, y1, (x2 - x1), y2 - y1,
                0, 'h',
                character.x, character.y + y_offset,
                (x2 - x1), y2 - y1
            )
        else:  # 왼쪽 방향
            character.image.clip_draw(
                x1, y1, (x2 - x1), y2 - y1,
                character.x, character.y + y_offset
            )



class Attack2:
    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 84, 3 * 80, 84, 80, character.x, character.y)

class Jump:
    @staticmethod
    def enter(character, event=None):
        character.velocity_y =  380# 초기 점프 속도 (위로 상승)
        character.gravity = -1000 # 중력 값
        character.jump_origin_y = character.y  # 점프 시작 높이 기록
        character.frame = 0  # 점프 애니메이션 초기화
        character.dir = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        # y 위치 업데이트
        character.y += character.velocity_y * game_framework.frame_time
        character.velocity_y += character.gravity * game_framework.frame_time

        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time

        # 지면에 도달하면 점프 종료
        if character.y <= character.jump_origin_y:
            character.y = character.jump_origin_y  # 지면에서 멈춤
            character.state_machine.change_state(Idle)

        # 점프 애니메이션
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(character):
        # 3번째 줄, 고정된 프레임으로 출력
        frame_width = 45
        frame_height = 90
        x1 = 570 # 해당 프레임의 시작 X좌표
        row = 2  # 3번째 줄에 위치한 프레임이므로 (2번째 행)
        y_offset = 0

        if character.face_dir == -1:  #
            character.image.clip_draw(
                x1, character.image.h - (row + 1) * frame_height, frame_width, frame_height,
                character.x, character.y + y_offset
            )
        else:  # 왼쪽 방향
            character.image.clip_composite_draw(
                x1, character.image.h - (row + 1) * frame_height, frame_width, frame_height,
                0, 'h',
                character.x, character.y + y_offset,
                frame_width, frame_height
            )
    @staticmethod
    def handle_event(character, event):
        if right_down(event):
            character.dir = 1
        elif left_down(event):
            character.dir = -1
        elif right_up(event) or left_up(event):
            character.dir = 0
class Hurt:
    @staticmethod
    def enter(character, event = None):
        character.frame = 0
        character.knockback_timer = 0.5  # 넉백 유지 시간
        character.knockback_dir = -1 if character.face_dir == 1 else 1  # 넉백 방향 설정
        print("Entered Hurt State")  # 디버깅 메시지

    @staticmethod
    def exit(character):
        character.knockback_timer = 0

    @staticmethod
    def do(character):
        character.knockback_timer -= game_framework.frame_time
        if character.knockback_timer > 0:
            character.x += character.knockback_dir * 300 * game_framework.frame_time  # 넉백 이동
        else:
            character.is_knocked_back = False  # 넉백 상태 해제
            character.state_machine.change_state(Idle)  # 넉백이 끝나면 Idle 상태로 전환

    @staticmethod
    def draw(character):
        # Hurt 상태 프레임 그리기
        frame_width = 84  # 프레임 너비
        frame_height = 80  # 프레임 높이
        row = 6  # Hurt 모션이 7번째 행
        col = int(character.frame)
        y_position = character.image.h - (row + 1) * frame_height

        character.image.clip_draw(
            col * frame_width, y_position, frame_width, frame_height,
            character.x, character.y
        )
