from pico2d import *
import time

class Character: #Character 클래스 생성
    def __init__(self):
        #두 개의 스프라이트 시트 로드
        self.image1 = load_image('character1.png')
        self.image2 - load_image('character2.png')

        self.frame = 0.0 #프레임을 float로 관리
        self.action = 'Idle' #기본 상태는 Idle
        self.x, self.y = 400, 300 #초기 위치
        self.velocity = 0 # 이동속도
        self.frame_time = 0.1 #한 프레임당 유지 시간(초 단위)

        self.last_time = time.time()

        self.actions = { #각 스프라이트 시트에서 동작별 프레임 범위 정의
            'Idle': (self.image1,0,5),
            'Walk': (self.image1,6,13),
            'Run': (self.image1,14,21),
            'Jump': (self.image1,22,29),
            'Attack1': (self.image1,30,36),
            'Attack2': (self.image2,0,3),
            'Attack3': (self.image2,4,6),
            'Shield': (self.image2,7,8),
            'Hurt': (self.image2,9,10),
            'Dead': (self.image2,11,13)
        }
    def set_action(self, action):
        if action in self.actions:
            self.action = action
            self.frame = self.actions[action][1] #해당 액션의 첫번째 프레임으로 초기화

    def update(self):
        #현재 시간 가져오기
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        #현재 동작의 프레임 범위를 기준으로 프레임 업데이트
        image, start, end = self.actions[self.action]
        self.frame += (1 / self.frame_time) * delta_time #시간에 따라 프레임 증가

        # 끝 프레임을 넘으면 다시 시작 프레임으로 루프
        if self.frame > end:
            self.frame = start

        #캐릭터 이동 처리
        self.x += self.velocity * delta_time

    def draw(self):
        #현재 동작에 해당하는 스프라이트 시트를 기준으로 프레임 그리기
        image, start, end = self.actions[self.action]
        frame_width = image.w // (end+1) #각 프레임의 가로 크기
        frame_height = image.h #각 프레임의 세로 크기

        image.clip_draw(int(self.frame) * frame_width, 0, frame_width, frame_height, self.x, self.y)
            #