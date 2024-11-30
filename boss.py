from pico2d import *
import game_framework
import state_machine

FRAMES_PER_ACTION = 16  # 한 동작당 프레임 수
ACTION_PER_TIME = 1.0 / 1.0  # 초당 동작 수

class Boss:
    def __init__(self):
        self.x, self.y = 1300, 177 # 보스의 초기 위치
        self.frame = 0
        self.timer = 0

        self.image = load_image('boss1.png')  # 보스 이미지 로드
        self.state_machine = state_machine.StateMachine(self)  # 기본 상태는 Idle
        self.state_machine.change_state(Idle)

    def update(self):
        self.state_machine.update()  # 현재 상태의 로직 업데이트

    def draw(self):
        self.state_machine.draw()  # 현재 상태의 애니메이션 출력

    def get_bb(self):
        # 충돌 박스 반환 (x1, y1, x2, y2)
        return self.x - 70, self.y - 100, self.x + 70, self.y + 100

    def draw_bb(self):
        # 디버깅용: 충돌 박스 그리기
        draw_rectangle(*self.get_bb())

    def take_damage(self, danage):
        """보스가 피해를 입을 때 HP 감소"""
        self.hp = max(0, self.hp - damage)  # HP 감소
        self.hp_bar.update(self.hp)  # HP 바 상태 업데이트

class Idle:
    @staticmethod
    def enter(boss, event=None):
        boss.frame = 0  # Idle 상태 시작 시 첫 프레임 초기화
        boss.timer = 0

    @staticmethod
    def exit(boss):
        pass

    @staticmethod
    def do(boss):
        boss.timer += game_framework.frame_time
        boss.frame = (boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if boss.timer > 5.0:
            boss.state_machine.change_state(Attack1)
    @staticmethod
    def draw(self):
        frame_coordinates = [
            (0, 2369, 210, 2661),  # Frame 1
            (223, 2369, 442, 2661),  # Frame 2
            (442, 2369, 663, 2661),  # Frame 3
            (663, 2369, 879, 2661),  # Frame 4
            (879, 2369, 1103, 2661),  # Frame 5
            (1103, 2369, 1334, 2661),  # Frame 6
            (1338, 2369, 1576, 2661),  # Frame 7
            (1576, 2369, 1809, 2661)  # Frame 8

        ]

        col = int(self.frame)
        x1, y1, x2, y2 = frame_coordinates[col]

        # 프레임 출력
        self.image.clip_draw(x1, y1, x2 - x1, y2 - y1, self.x, self.y)
class Attack1:
    frame_coordinates = [
        (0, 1490, 215, 1780),  # Frame 1
        (215, 1493, 430, 1818),  # Frame 2
        (447, 1493, 700, 1818),  # Frame 3
        (716, 1493, 938, 1818),  # Frame 4
        (977, 1493, 1222, 1818),  # Frame 5
        (1222, 1493, 1466, 1818),  # Frame 6
        (1469, 1493, 1716, 1818),  # Frame 7
        (1746, 1493, 1932, 1818),  # Frame 8
        (1932, 1493, 2169, 1818),  # Frame 9
        (2169, 1493, 2376, 1818),  # Frame 10
        (2390, 1493, 2633, 1818),  # Frame 11
        (2633, 1493, 2882, 1818),  # Frame 12
        (2882, 1493, 3155, 1818),  # Frame 13
        (3156, 1493, 3448, 1818),  # Frame 14
        (3450, 1493, 3753, 1818),  # Frame 15
        (3751, 1493, 4070, 1818),  # Frame 16
        (4070, 1493, 4376, 1818),  # Frame 17
        (4376, 1493, 4687, 1818),  # Frame 18
        (4687, 1493, 4993, 1818),  # Frame 19
        (5000, 1493, 5264, 1818),  # Frame 20
        (5269, 1493, 5504, 1818)  # Frame 21
    ]

    @staticmethod
    def enter(boss, event=None):
        boss.frame = 0  # Attack1 상태 진입 시 첫 프레임 초기화

    @staticmethod
    def exit(boss):
        pass

    @staticmethod
    def do(boss):
        boss.timer += game_framework.frame_time
        boss.frame = (boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 21

        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if int(boss.frame) > len(Attack1.frame_coordinates) - 2:
            boss.state_machine.change_state(Idle)

    @staticmethod
    def draw(boss):
        x1, y1, x2, y2 = Attack1.frame_coordinates[int(boss.frame) % len(Attack1.frame_coordinates)]

        # 보스 이미지를 좌표에 맞게 출력
        boss.image.clip_draw(x1, y1, x2 - x1, y2 - y1, boss.x, boss.y + 50)
