from pico2d import *

class Tile:
    def __init__(self, x, y, frame_x, frame_y, frame_width, frame_height):
        self.image = load_image('tile.png')
        self.x, self.y = x, y
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_bb(self):
        # 충돌 박스 설정
        return self.x - self.frame_width // 2, self.y - self.frame_height // 2, self.x + self.frame_width // 2, self.y + self.frame_height // 2

    def draw_bb(self):
        # 충돌 박스 시각화 (디버깅용)
        draw_rectangle(*self.get_bb())

    def draw(self):
        # 이미지의 특정 영역을 clip_draw로 출력
        self.image.clip_draw(
            self.frame_x, self.frame_y,  # 타일 시작 좌표
            self.frame_width, self.frame_height,  # 타일 너비와 높이
            self.x, self.y  # 화면상의 출력 위치
        )

    def update(self):
        pass