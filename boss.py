from pico2d import *
import game_framework

FRAMES_PER_ACTION = 16  # 한 동작당 프레임 수
ACTION_PER_TIME = 1.0 / 1.0  # 초당 동작 수

class Boss:
    def __init__(self):
        self.x, self.y = 1300, 177 # 보스의 초기 위치
        self.frame = 0
        self.image = load_image('boss1.png')  # 보스 이미지 로드
        self.state = Attack1  # 기본 상태는 Idle
        self.state.enter(self)  # 상태 진입

    def update(self):
        self.state.do(self)  # 현재 상태의 로직 업데이트

    def draw(self):
        self.state.draw(self)  # 현재 상태의 애니메이션 출력


    def change_state(self, new_state):
        self.state.exit(self)  # 현재 상태 종료
        self.state = new_state  # 새로운 상태로 변경
        self.state.enter(self)  # 새로운 상태 진입

class Idle:
    @staticmethod
    def enter(boss):
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
        (0, 215, 215, 430),  # Frame 1
        (215, 215, 430, 430),  # Frame 2
        (447, 215, 682, 430),  # Frame 3
        (706, 215, 953, 430),  # Frame 4
        (977, 215, 1222, 430),  # Frame 5
        (1222, 215, 1466, 430),  # Frame 6
        (1469, 215, 1716, 430),  # Frame 7
        (1716, 215, 1945, 430),  # Frame 8
        (1845, 215, 2170, 430),  # Frame 9
        (2170, 215, 2387, 430),  # Frame 10
        (2390, 215, 2633, 430),  # Frame 11
        (2633, 215, 2882, 430),  # Frame 12
        (2882, 215, 3155, 430),  # Frame 13
        (3156, 215, 3448, 430),  # Frame 14
        (3450, 215, 3753, 430),  # Frame 15
        (3751, 215, 4070, 430),  # Frame 16
        (4070, 215, 4376, 430),  # Frame 17
        (4376, 215, 4687, 430),  # Frame 18
        (4687, 215, 4993, 430),  # Frame 19
        (5000, 215, 5264, 430),  # Frame 20
        (5269, 215, 5504, 430)   # Frame 21
    ]

    @staticmethod
    def enter(boss):
        boss.frame = 0  # Attack1 상태 진입 시 첫 프레임 초기화

    @staticmethod
    def exit(boss):
        pass

    @staticmethod
    def do(boss):
        boss.frame += 1

        # 공격 애니메이션이 끝나면 Idle 상태로 전환
        if boss.frame >= len(Attack1.frame_coordinates):
            boss.state_machine.change_state(Idle)

    @staticmethod
    def draw(boss):
        # 현재 프레임 좌표 가져오기
        x1, y1, x2, y2 = Attack1.frame_coordinates[boss.frame % len(Attack1.frame_coordinates)]

        # 보스 이미지를 좌표에 맞게 출력
        boss.image.clip_draw(x1, y1, x2 - x1, y2 - y1, boss.x, boss.y)
