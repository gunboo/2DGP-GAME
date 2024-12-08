from pico2d import *
import game_framework
import game_world
from character import Character
from portal import Portal
import play_mode  # 이전 맵


class NPC:
    def __init__(self, x, y):
        self.x, self.y = x, y + 20
        self.image = load_image('npc.png')  # NPC 이미지 로드
        self.image2 = load_image('0.png')
        self.dialogue = "마뇽을 물리치고 저를 구해주세요"
        self.is_talking = False
        self.font = load_font('light.otf', 20)
        self.interaction_sound = load_wav('npc_interaction.wav')  # 충돌 시 재생할 효과음
        self.interaction_sound.set_volume(30)  # 효과음 볼륨 설정

    def draw(self):
        self.image.draw(self.x, self.y)
        self.image2.draw(self.x, self.y + 100)
        if self.is_talking:
            self.font.draw(self.x - 140, self.y + 70, self.dialogue, (255, 255, 255))

    def update(self):
        pass

    def get_bb(self):
        """충돌 박스 반환"""
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50

    def draw_bb(self):
        """충돌 박스 시각화"""
        pass

    def play_sound(self):
        """NPC 효과음 재생"""
        self.interaction_sound.play()


class NextMap:
    def __init__(self):
        self.background = None
        self.character = None
        self.portal_back = None  # 이전 맵으로 돌아가는 포탈
        self.npc = None  # NPC 추가

    def enter(self):
        """NextMap 상태로 진입할 때 호출"""
        self.background = load_image('next_map_background.png')  # 배경 이미지 로드
        print("Entered NextMap")

        # 캐릭터 추가
        if not self.character:  # 캐릭터가 없으면 새로 생성
            self.character = Character()
            self.character.x, self.character.y = 1400, 90  # 초기 위치
            game_world.add_object(self.character, 2)  # 캐릭터 추가
        else:  # 기존 캐릭터 유지
            self.character.x, self.character.y = 100, 90

        # 이전 맵으로 이동하는 포탈 추가
        self.portal_back = Portal(1500, 90)
        game_world.add_object(self.portal_back, 1)

        # NPC 추가
        self.npc = NPC(800, 90)  # NPC 위치 지정
        game_world.add_object(self.npc, 2)

    def exit(self):
        """NextMap 상태를 나갈 때 호출"""
        print("Exiting NextMap")
        game_world.clear()

    def update(self):
        """NextMap 상태에서 업데이트 처리"""
        game_world.update()

        # 포탈과 캐릭터 충돌 검사
        if self.portal_back and check_collision(self.character.get_bb(), self.portal_back.get_bb()):
            game_framework.change_state(play_mode)  # 이전 맵으로 이동

        # NPC와 캐릭터 충돌 검사
        if self.npc and check_collision(self.character.get_bb(), self.npc.get_bb()):
            if not self.npc.is_talking:  # 처음 충돌 시에만 사운드 재생
                self.npc.play_sound()  # 효과음 재생
            self.npc.is_talking = True  # 캐릭터가 NPC와 충돌 중
        else:
            self.npc.is_talking = False  # 캐릭터와 NPC가 충돌하지 않음

    def draw(self):
        """다음 맵 배경 및 기타 요소를 화면에 그림"""
        clear_canvas()
        if self.background:
            self.background.draw(800, 300)  # 배경 출력
        game_world.render()  # 게임 월드의 객체들 렌더링

        # NPC 충돌 박스 시각화 (디버깅용)
        if self.npc:
            self.npc.draw_bb()

        update_canvas()

    def handle_events(self):
        """이벤트 처리"""
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.pop_state()  # 이전 상태로 돌아감
            else:
                if self.character:
                    self.character.handle_event(event)  # 캐릭터 이벤트 처리



def check_collision(box1, box2):
    """충돌 체크"""
    left1, bottom1, right1, top1 = box1
    left2, bottom2, right2, top2 = box2

    return not (right1 < left2 or right2 < left1 or top1 < bottom2 or top2 < bottom1)
