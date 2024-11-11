import time
from pico2d import *

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# 각 프레임의 크기
FRAME_WIDTH = 182
FRAME_HEIGHT = 169

# 일정한 속도 값 설정
TIME_PER_ACTION = 0.5  # 한 사이클당 시간 (0.5초에 한 번 날갯짓 사이클 완료)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 초당 사이클 수
FRAMES_PER_ACTION = 8  #

# 새의 이동 속도를 초당 185픽셀로 설정
FLY_SPEED_PPS = 200

# 전역 변수
frame_time = 0.0  # 프레임 시간

# 새떼 속성 정의
class BirdFlock:
    def __init__(self):
        self.image = load_image('bird_animation.png')
        self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.frame = 0
        self.direction = 1
        self.total_frames = 14

    def update(self):
        global frame_time
        # 날갯짓 애니메이션 프레임 업데이트
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time) % self.total_frames

        # 새떼 이동
        self.x += self.direction * FLY_SPEED_PPS * frame_time
        # 화면 끝에서 방향 전환
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.direction *= -1  # 방향 반전

    def draw(self):

        row = int(self.frame) // 5  # 5열로 구성
        col = int(self.frame) % 5   # 현재 열 위치


        if row == 2 and col >= 4:
            col = 3


        if self.direction == 1:
            self.image.clip_draw(col * FRAME_WIDTH, (2 - row) * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
        else:
            self.image.clip_composite_draw(col * FRAME_WIDTH, (2 - row) * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT, 0, 'h', self.x, self.y, FRAME_WIDTH, FRAME_HEIGHT)

    def handle_events(self):
        pass

    def finish(self):
        pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            quit()


def quit():
    global running
    running = False


def run(start_mode):
    global running, frame_time
    running = True
    stack = [start_mode]
    start_mode.init()

    # 초기 frame_time 설정
    current_time = time.time()

    while running:
        handle_events()
        stack[-1].update()
        stack[-1].draw()


        new_time = time.time()
        frame_time = new_time - current_time
        current_time = new_time



    # 모든 모드 종료
    while stack:
        stack[-1].finish()
        stack.pop()


class GameMode:
    def init(self):
        self.bird_flock = BirdFlock()

    def update(self):
        self.bird_flock.update()

    def draw(self):
        clear_canvas()
        self.bird_flock.draw()
        update_canvas()

    def handle_events(self):
        handle_events()

    def finish(self):
        pass


# 실행 부분
if __name__ == '__main__':
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    start_mode = GameMode()
    run(start_mode)
    close_canvas()
