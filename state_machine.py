from pico2d import SDL_KEYDOWN, SDLK_LEFT, SDL_KEYUP, SDLK_RIGHT, SDLK_LCTRL, SDLK_LSHIFT
from sdl2 import SDLK_LALT

FRAMES_PER_ACTION = 8  # 한 동작당 프레임 수
ACTION_PER_TIME = 1.0 / 1.0  # 초당 동작 수
RUN_SPEED_PPS = 200  # 초당 픽셀 이동 속도

# 이벤트 조건 정의
def left_down(e): return e.type == SDL_KEYDOWN and e.key == SDLK_LEFT
def left_up(e): return e.type == SDL_KEYUP and e.key == SDLK_LEFT
def right_down(e): return e.type == SDL_KEYDOWN and e.key == SDLK_RIGHT
def right_up(e): return e.type == SDL_KEYUP and e.key == SDLK_RIGHT
def ctrl_down(e): return e.type == SDL_KEYDOWN and e.key == SDLK_LCTRL
def shift_down(e): return e.type == SDL_KEYDOWN and e.key == SDLK_LSHIFT
def alt_down(e): return e.type == SDL_KEYDOWN and e.key == SDLK_LALT

class StateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.current_state = None
        self.transitions = {}

    def start(self, initial_state):
        self.change_state(initial_state)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, event):
        if self.current_state in self.transitions:
            for condition, next_state in self.transitions[self.current_state].items():
                if callable(condition) and condition(event):
                    self.change_state(next_state, event)
                    return

    def change_state(self, new_state, event=None):
        if self.current_state:
            self.current_state.exit(self.owner)
        self.current_state = new_state
        self.current_state.enter(self.owner,event)  # 이벤트 전달


    def update(self):
        if self.current_state:
            self.current_state.do(self.owner)

    def draw(self):
        if self.current_state:
            self.current_state.draw(self.owner)
