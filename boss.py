from pico2d import *
import game_framework
import state_machine
import game_world

FRAMES_PER_ACTION = 16  # 한 동작당 프레임 수
ACTION_PER_TIME = 1.0 / 1.0  # 초당 동작 수

class Boss:
    def __init__(self, character):
        self.x, self.y = 1300, 177  # 보스의 초기 위치
        self.frame = 0
        self.timer = 0
        self.character = character  # 캐릭터 객체 참조
        self.dead = False
        self.hp = 3.0  # 보스의 HP (0.0 ~ 1.0)
        self.max_hp = 3.0  # 보스의 최대 HP
        self.speed = 100  # 보스의 이동 속도
        self.effect_frame = 0
        self.effect_active = False
        self.effect_timer = 0.0
        self.effect_image = load_image('boss1.png')
        self.image = load_image('boss1.png')  # 보스 이미지 로드
        self.state_machine = state_machine.StateMachine(self)  # 상태 머신 초기화
        self.state_machine.change_state(Idle)  # 초기 상태 설정

    def update(self):
        self.state_machine.update()  # 현재 상태 업데이트
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.state_machine.change_state(Dead)

    def draw(self):
        self.state_machine.draw()  # 현재 상태의 애니메이션 출력

    def get_bb(self):
        # 충돌 박스 반환 (x1, y1, x2, y2)
        if self.dead:
            return -1, -1, -1, -1
        return self.x - 70, self.y - 100, self.x + 70, self.y + 100

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def take_damage(self, damage):
        """보스가 피해를 입을 때"""
        if not self.dead:
            self.hp = max(0, self.hp - damage)  # HP 감소 (최소값은 0)
            print(f"Boss HP: {self.hp}")
            if self.hp <= 0:
                self.dead = True
                self.state_machine.change_state(Dead)  # HP가 0이 되면 Dead 상태로 전환


class Idle:
    ATTACK_INTERVAL = 5.0  # 공격 간격
    STOP_DISTANCE = 250  # 보스가 멈추는 거리

    @staticmethod
    def enter(boss, event=None):
        boss.frame = 0
        boss.timer = 0  # 타이머 초기화
        print("Boss entered Idle state")

    @staticmethod
    def exit(boss):
        print("Boss exited Idle state")

    @staticmethod
    def do(boss):
        """5초마다 공격 상태로 전환 및 캐릭터 쫓기"""
        boss.timer += game_framework.frame_time  # 타이머 업데이트

        # 5초가 경과하면 공격 상태로 전환
        if boss.timer >= Idle.ATTACK_INTERVAL:
            boss.timer = 0  # 타이머 초기화
            boss.state_machine.change_state(Attack1)
            return

        # 캐릭터와의 거리 계산
        dx = boss.character.x - boss.x  # X축 차이
        dy = boss.character.y - boss.y  # Y축 차이
        distance = (dx**2 + dy**2)**0.5  # 캐릭터와 보스 간 거리 계산

        if distance > Idle.STOP_DISTANCE:  # 250픽셀 이상이면 이동
            boss.x += (dx / distance) * boss.speed * game_framework.frame_time
            boss.y += (dy / distance) * boss.speed * game_framework.frame_time
        else:
            # 250픽셀 이내에서는 멈춤
            boss.x = boss.x
            boss.y = boss.y

        # 애니메이션 프레임 업데이트
        boss.frame = (boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(boss):
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

        col = int(boss.frame)
        x1, y1, x2, y2 = frame_coordinates[col]

        # 프레임 출력
        boss.image.clip_draw(x1, y1, x2 - x1, y2 - y1, boss.x, boss.y)





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
        boss.effect_frame = 0
        boss.effect_active = True

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

class AtaackEffect:

class Dead:
    frame_coordinates = [
        (0, 0, 211, 288),  # frame 1
        (211, 0, 427, 288),  # frame 2
        (427, 0, 635, 288),  # frame 3
        (635, 0, 849, 288),  # frame 4
        (854, 0, 1085, 288),  # frame 5
        (1085, 0, 1320, 288),  # frame 6
        (1325, 0, 1553, 288),  # frame 7
        (1363, 0, 1796, 288)  # frmae 8
    ]

    @staticmethod
    def enter(boss, event=None):
        boss.frame = 0
        boss.dead = True
        boss.frame_timer = 0
        boss.frame_delay = 0.2

    @staticmethod
    def exit(boss):
        pass

    def do(boss):
        boss.frame += (boss.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

        if boss.frame_timer >= boss.frame_delay:
            boss.frame_timer = 0
            boss.frame += 1

        if boss.frame >= len(Dead.frame_coordinates):
            game_world.remove_object(boss) #보스를 제거

    @staticmethod
    def draw(boss):
        col = int(boss.frame % len(Dead.frame_coordinates))
        x1, y1, x2, y2 = Dead.frame_coordinates[col]

        boss.image.clip_draw(x1, y1, x2 - x1, y2 - y1, boss.x, boss.y)






