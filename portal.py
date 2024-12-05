from pico2d import *
import game_framework

class Portal:
    def __init__(self):
        self.x = 100  # 포탈의 X 좌표
        self.y = 90   # 포탈의 Y 좌표
        self.image = load_image('portal.png')  # 포탈 이미지 로드

    def update(self):
        pass  # 업데이트할 애니메이션 없음 (고정된 이미지)

    def draw(self):
        # 포탈 그리기
        self.image.draw(self.x, self.y)
        self.draw_bb()  # 충돌 박스 디버깅용

    def get_bb(self):
        # 포탈의 충돌 박스 반환
        return self.x - 30, self.y - 40, self.x + 30, self.y + 40

    def draw_bb(self):
        # 포탈의 충돌 박스를 시각적으로 표시 (디버깅용)
        left, bottom, right, top = self.get_bb()
        draw_rectangle(left, bottom, right, top)
