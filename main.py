from pico2d import open_canvas, close_canvas
import game_framework
import play_mode as start_mode

# 캔버스 크기 설정
open_canvas(1600, 600)

# 게임 프레임워크 실행
game_framework.run(start_mode)

# 종료 시 캔버스 닫기
close_canvas()
