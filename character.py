from pico2d import *
import game_framework
from state_machine import StateMachine, left_down, left_up, right_down, right_up, ctrl_down, shift_down, alt_down
from hp_bar import HPBar,HPBarUI, MPBar,ExpBar


FRAMES_PER_ACTION = 8
ACTION_PER_TIME = 1.0 / 1.0
RUN_SPEED_PPS = 200


class Character:
    def __init__(self):
        self.x, self.y = 400, 90
        self.hp = 1.0
        self.mp = 1.0
        self.hp_bar = HPBar()
        self.mp_bar = MPBar()
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {alt_down: Jump,right_down: Walk, left_down: Walk, ctrl_down: Attack1, shift_down: Attack2 },
                Walk: {right_up: Idle, left_up: Idle, ctrl_down: Attack1, shift_down: Attack2, alt_down:Jump},
                Attack1: {left_up: Idle, right_up: Idle},
                Attack2: {left_up: Idle, right_up: Idle},
                Jump: {},
            }
        )

    def take_damage(self, damage):
        """데미지를 입으면 HP 감소"""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0  # HP는 최소 0으로 유지
        self.hp_bar.update(self.hp)

    def use_mana(self,amount):
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



# 상태 정의
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
        print("Entering Walk State")
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
        print(f"Character position: {character.x}, {character.y}")  # 위치 디버깅

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
        character.frame = 0  # 공격 시작 시 첫 프레임 초기화
        character.mp -= 0.1
        character.mp = max(0, character.mp)

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        # 0~5 프레임 순환 (6프레임)
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        character.mp_bar.update(character.mp)
        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if character.frame >= 5:
            character.state_machine.change_state(Idle)

    @staticmethod
    def draw(character):
        frame_widths = [89, 89, 89, 110, 110, 110]  # 각 프레임의 실제 너비
        frame_adjustments = [0, 0, -35, -30, -30, -30]  # 오른쪽 확장을 위한 조정 값
        frame_coordinates = [
            (0, 689, 89, 776),  # Frame 1
            (89, 689, 178, 776),  # Frame 2
            (178, 689, 267, 776),  # Frame 3
            (267, 689, 377, 776),  # Frame 4
            (377, 689, 487, 776),  # Frame 5
            (487, 689, 597, 776)  # Frame 6
        ]

        col = int(character.frame)  # 현재 프레임 인덱스
        x1, y1, x2, y2 = frame_coordinates[col]
        adjustment = frame_adjustments[col]  # 오른쪽 확장을 위한 조정

        y_offset = 14  # Y축 보정값

        if character.face_dir == 1:  # 오른쪽 방향
            character.image.clip_composite_draw(
                x1, y1, (x2 - x1) + adjustment, y2 - y1,  # 오른쪽 확장
                0, 'h',  # 수평 반전
                character.x, character.y + y_offset,  # 출력 위치
                        (x2 - x1) + adjustment, y2 - y1  # 최종 출력 크기
            )
        else:  # 왼쪽 방향
            character.image.clip_draw(
                x1, y1, (x2 - x1) + adjustment, y2 - y1,  # 오른쪽 확장 적용
                character.x, character.y + y_offset  # 출력 위치
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

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        # y 위치 업데이트
        character.y += character.velocity_y * game_framework.frame_time
        character.velocity_y += character.gravity * game_framework.frame_time

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