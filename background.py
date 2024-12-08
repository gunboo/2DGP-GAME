from pico2d import *
from Tile import Tile

class Background:
    def __init__(self):
        # 업로드한 배경 이미지 로드
        self.image = load_image('background1.png')
        self.x, self.y = 800, 220  # 배경 이미지의 중심 좌표 설정 (1600x600 크기에 맞게)
        self.bgm = load_music('background_sound.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        pass  # 배경은 움직이지 않으므로 업데이트는 필요 없음

    def draw(self):
        self.image.draw(self.x, self.y)  # 배경 이미지 중앙 출력


