from pico2d import *

class HPBarUI:
    def __init__(self):
        self.image = load_image('hp_bar.png')  # 첨부된 HP바 틀 이미지
        self.x, self.y = 110, 560  # UI 위치

    def draw(self):
        self.image.draw(self.x, self.y)  # UI 틀 그리기

class HPBar:
    def __init__(self):
        self.image = load_image('hp.png')  # 'hp.png' 파일
        self.max_width = self.image.w
        self.height = self.image.h
        self.x, self.y = 120, 578  # HP 바 위치 (조정 필요)
        self.current_hp = 1.0  # 기본 HP 100%

    def update(self, hp_ratio):
        self.current_hp = hp_ratio

    def draw(self):
        # 바 확대 및 위치 조정
        scale_x = 10.3 # 확대 배율 (가로)
        scale_y = 12.3 # 확대 배율 (세로)
        self.image.clip_composite_draw(
            0, 0,
            int(self.max_width * self.current_hp), self.height,
            0, '',  # 회전, 반전 없음
            self.x, self.y,  # 위치
            int(self.max_width * scale_x * self.current_hp), self.height * scale_y  # 확대된 크기
        )


class MPBar:
    def __init__(self):
        self.image = load_image('mp.png')
        self.max_width = self.image.w
        self.height = self.image.h
        self.x, self.y = 120, 560  # MP 바 위치 (조정 필요)
        self.current_mp = 1.0

    def update(self, mp_ratio):
        self.current_mp = mp_ratio

    def draw(self):
        scale_x = 10.3  # 가로 확대 비율
        scale_y = 12.3  # 세로 확대 비율
        clip_width = int(self.max_width * self.current_mp)  # 현재 MP 비율에 따른 실제 너비

        # MP 바가 왼쪽에서 오른쪽으로 감소하도록 설정
        self.image.clip_draw(
            0, 0,  # 이미지의 시작 좌표
            clip_width, self.height,  # 현재 MP 비율에 따른 너비와 높이
            self.x - (self.max_width * scale_x - clip_width * scale_x) / 2,  # X 위치 보정
            self.y,  # Y 위치
            clip_width * scale_x,  # 확대된 가로 크기
            self.height * scale_y  # 확대된 세로 크기
        )


class ExpBar:
    def __init__(self):
        self.image = load_image('exp.png')
        self.max_width = self.image.w
        self.height = self.image.h
        self.x, self.y = 120, 535  # EXP 바 위치 (조정 필요)
        self.current_exp = 0.5  # 임의로 EXP 50%로 설정

    def update(self, exp_ratio):
        self.current_exp = exp_ratio

    def draw(self):
        scale_x = 38.0
        scale_y = 5.0
        self.image.clip_composite_draw(
            0, 0,
            int(self.max_width * self.current_exp), self.height,
            0, '',
            self.x, self.y,
            int(self.max_width * scale_x * self.current_exp), self.height * scale_y
        )
