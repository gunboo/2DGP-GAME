import time
from pico2d import delay

running = True
stack = []  # 상태 스택 관리
frame_time = 0.0  # 각 프레임의 시간 차이

def run(start_state):
    global running, frame_time, stack
    running = True
    stack.append(start_state)
    start_state.init()

    current_time = time.time()

    while running:
        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time



        current_state = stack[-1]

        # 상태 처리
        current_state.handle_events()
        current_state.update()
        current_state.draw()

        delay(0.01)  # 프레임 속도 조정

    while stack:
        stack.pop().exit()

def change_state(state):
    global stack
    if stack:
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()

def push_state(state):
    global stack
    if stack:
        stack[-1].pause()
    stack.append(state)
    state.enter()

def pop_state():
    global stack
    if stack:
        stack[-1].exit()
        stack.pop()

    if stack:
        stack[-1].resume()

def quit():
    global running
    running = False
