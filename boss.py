from pico2d import *
import game_framework

FRAMES_PER_ACTION = 16  # 한 동작당 프레임 수
ACTION_PER_TIME = 1.0 / 1.0  # 초당 동작 수

class Boss:
    def __init__(self):
        self.x, self.y = 1300, 150  # 보스의 초기 위치
        self.frame = 0
        self.image = load_image('boss_sprite.png')  # 보스 이미지 로드
        self.state = Idle  # 기본 상태는 Idle
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

    @staticmethod
    def exit(boss):
        pass

    @staticmethod
    def do(boss):
        boss.frame = (boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16  # 16프레임 순환

    @staticmethod
    def draw(self):
        frame_coordinates = [
            (0, 2163, 261, 2379),  # Frame 1
            (261, 2163, 500, 2379),  # Frame 2
            (500, 2163, 755, 2379),  # Frame 3
            (755, 2163, 1000, 2379),  # Frame 4
            (1000, 2163, 1260, 2379),  # Frame 5
            (1260, 2163, 1520, 2379),  # Frame 6
            (1520, 2163, 1786, 2379),  # Frame 7
            (1800, 2163, 2094, 2379),  # Frame 8
            (2094, 2163, 2356, 2379),  # Frame 9
            (2356, 2163, 2600, 2379),  # Frame 10
            (2600, 2163, 2860, 2379),  # Frame 11
            (2860, 2163, 3120, 2379),  # Frame 12
            (3121, 2163, 3383, 2379),  # Frame 13
            (3370, 2163, 3630, 2379),  # Frame 14
            (3630, 2163, 3910, 2379),  # Frame 15
            (3900, 2163, 4189, 2379)  # Frame 16
        ]

        col = int(self.frame)
        x1, y1, x2, y2 = frame_coordinates[col]

        # 프레임 출력
        self.image.clip_draw(x1, y1, x2 - x1, y2 - y1, self.x, self.y)