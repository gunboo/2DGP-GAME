from pico2d import *
import game_framework
import game_world
from character import Character  # 캐릭터 재활용
from background import Background  # 배경 재활용

class NextMap:
    def __init__(self):
        self.background = Background('next_map_background.png')  # 새로운 맵 배경
        self.character = Character()  # 캐릭터 재활용
        self.character.x, self.character.y = 100, 100  # 캐릭터의 초기 위치
        game_world.add_object(self.background, 0)  # 배경을 레이어 0에 추가
        game_world.add_object(self.character, 1)  # 캐릭터를 레이어 1에 추가

    def update(self):
        game_world.update()

    def draw(self):
        clear_canvas()
        game_world.render()
        update_canvas()

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                self.character.handle_event(event)

    def exit(self):
        game_world.clear()

def enter():
    global next_map
    next_map = NextMap()

def exit():
    next_map.exit()

def update():
    next_map.update()

def draw():
    next_map.draw()

def handle_events():
    next_map.handle_events()
