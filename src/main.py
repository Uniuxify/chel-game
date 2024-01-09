import pygame
import sys
import os
from os import path

pygame.init()
SCREEN = pygame.display.set_mode((1000, 800))
SCREEN.fill((255, 255, 255))
pygame.display.set_caption('Чел')
icon_img = pygame.image.load('../res/icon.png')
pygame.display.set_icon(icon_img)

FPS_CLOCK = pygame.time.Clock()
FPS = 5

SOUNDS = {
    'dudka-sound': pygame.mixer.Sound('../res/sounds/tuDU.wav')
}


class Game:
    def __init__(self):
        self.man = Man()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.man.change_state(ManStates.RUNNING)
                        self.man.change_dir(ManDir.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.man.change_state(ManStates.RUNNING)
                        self.man.change_dir(ManDir.RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.man.change_state(ManStates.JUMPING)
                    elif event.key == pygame.K_1:
                        self.man.change_state(ManStates.DUDKA)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.man.man_dir == ManDir.LEFT:
                        self.man.change_state(ManStates.STAYING)
                    elif event.key == pygame.K_RIGHT and self.man.man_dir == ManDir.RIGHT:
                        self.man.change_state(ManStates.STAYING)

            if self.man.curr_state == ManStates.RUNNING:
                self.man.move()

            self.draw_scene()
            self.man.play_sounds()
            self.man.auto_change_state()
            FPS_CLOCK.tick(FPS)

    def draw_scene(self):
        SCREEN.fill((255, 255, 255))
        self.man.draw(show_hitboxes=True)

        pygame.display.update()

    def terminate(self):
        pygame.quit()
        sys.exit()


class ManStates:
    STAYING = 0
    RUNNING = 1
    JUMPING = 2
    DUDKA = 3

    NAMES = {
        STAYING: 'staying',
        RUNNING: 'running',
        JUMPING: 'jumping',
        DUDKA: 'dudka'
    }

    @staticmethod
    def is_valid(state):
        if state in ManStates.as_list():
            return True
        return False

    @staticmethod
    def as_list():
        return [ManStates.STAYING, ManStates.RUNNING, ManStates.JUMPING, ManStates.DUDKA]

    @staticmethod
    def as_dict():
        return ManStates.NAMES


class ManDir:
    RIGHT = 0
    LEFT = 1

    @staticmethod
    def is_valid(man_dir):
        if man_dir in [ManDir.LEFT, ManDir.RIGHT]:
            return True
        return False


def scale_frames(frames, scale):  # TODO: Адаптировать для работы с pivots
    return list(
            map(lambda frame: pygame.transform.smoothscale(frame, (frame.get_size()[0] * scale, frame.get_size()[1] * scale)),
                frames))


def flip_frames(frames):  # TODO: Адаптировать для работы с pivots
    return list(map(lambda frame: pygame.transform.flip(frame, True, False), frames))


def create_hitbox(img, pivots):
    img = pygame.surfarray.array2d(img)
    hit_boxes = []
    for pivot in pivots:
        w = 4
        h = 4

        # Координаты левого верхнего угла
        x0 = pivot[0] - w // 2
        y0 = pivot[1] - h // 2

        ready = False
        while not ready:
            ready = True
            # Координаты нижнего правого угла
            x1 = x0 + w
            y1 = y0 + h

            if y0 <= 0 or x0 <= 0 or x1 >= 500 or y1 >= 500:
                break

            top_edge = img[x0:x1, y0]
            bottom_edge = img[x0:x1, y1]
            left_edge = img[x0, y0:y1]
            right_edge = img[x1, y0:y1]
            if list(top_edge).count(-1) in (0, 1):
                y0 -= 2
                h += 2
                ready = False
            if list(bottom_edge).count(-1) in (0, 1):
                h += 2
                ready = False
            if list(left_edge).count(-1) in (0, 1):
                x0 -= 2
                w += 2
                ready = False
            if list(right_edge).count(-1) in (0, 1):
                w += 2
                ready = False

        hitbox = pygame.Rect(x0, y0, w, h)
        hit_boxes.append(hitbox)

    return hit_boxes


class Man:
    def __init__(self):
        self.curr_state = ManStates.STAYING
        self.state_frames = dict()
        self.staying_hitboxes = []  # TODO: Распространить хитбоксы на все состояния

        self.state_nframes = dict()

        for state, state_name in ManStates.as_dict().items():  # TODO: пути к кадрам должны читаться из файла
            frames_dir = f'../res/frames/{state_name}'
            frames = [path.join(frames_dir, f) for f in os.listdir(frames_dir) if path.isfile(path.join(frames_dir, f))]
            n_frames = len(frames)
            self.state_frames[state] = [pygame.image.load(f"../res/frames/{state_name}/{state_name}{i}.png") for i in range(1, n_frames+1)]
            self.state_nframes[state] = n_frames

        # TODO: pivots должны читаться из файла
        pivots_x = [219, 217, 217, 216, 216, 216, 215, 213, 209, 193, 173, 157, 307, 307, 307, 308, 308, 307, 307, 307, 305, 289, 271, 254, 203, 190, 176, 166, 155, 147, 140, 139, 314, 330, 346, 358, 362, 359, 349, 338, 224, 216, 211, 204, 200, 199, 202, 208, 219, 235, 254, 276, 293, 305, 314, 316, 315, 312, 308, 303, 296, 290, 234, 252, 274, 292, 311, 327, 339, 349, 348, 339, 322, 298, 276, 253, 231, 209, 192, 182, 180, 188, 199, 216]
        pivots_y = [324, 341, 360, 379, 398, 420, 441, 461, 479, 485, 484, 485, 324, 344, 361, 381, 400, 418, 437, 459, 478, 484, 483, 484, 181, 190, 203, 218, 235, 253, 269, 286, 173, 171, 175, 183, 200, 214, 227, 236, 154, 169, 185, 207, 229, 249, 271, 291, 310, 322, 332, 334, 324, 305, 283, 260, 238, 218, 199, 180, 163, 147, 137, 136, 134, 130, 121, 112, 95, 75, 54, 35, 23, 17, 17, 19, 25, 34, 47, 65, 86, 107, 123, 133]
        pivots = list(zip(pivots_x, pivots_y))
        self.p = pivots

        for frame in self.state_frames[ManStates.STAYING]:
            self.staying_hitboxes.append(create_hitbox(frame, pivots))

        # scale = 0.33
        # for state, frames in self.state_frames.items():
        #     self.state_frames[state] = scale_frames(frames, scale)

        self.curr_frame = 0
        self.man_dir = ManDir.LEFT

        self.step = 30
        self.x = 100
        self.y = 200

    def draw(self, show_hitboxes=False):
        frames = self.state_frames[self.curr_state]
        SCREEN.blit(frames[self.curr_frame], (self.x, self.y))

        if show_hitboxes:
            if self.curr_state == ManStates.STAYING:  # TODO: Распространить хитбоксы на все состояния
                for hitbox in self.staying_hitboxes[self.curr_frame]:

                    pygame.draw.rect(SCREEN, (255, 0, 0), hitbox.move(self.x, self.y), 0)

        for piv in self.p:
            pygame.draw.circle(SCREEN, (0, 255, 0), (piv[0] + self.x, piv[1] + self.y), 1)
        self.curr_frame += 1
        self.curr_frame %= len(frames)

    def play_sounds(self):
        if self.curr_state == ManStates.DUDKA:
            if self.curr_frame == 6:
                SOUNDS['dudka-sound'].play()

    def change_state(self, state):
        if not ManStates.is_valid(state):
            raise AttributeError('State must be one of 0, 1, 2')

        if self.curr_state != state:
            self.curr_state = state
            self.curr_frame = 0

    def auto_change_state(self):

        if (self.curr_state == ManStates.DUDKA and self.state_nframes[self.curr_state] == self.curr_frame + 1) or \
                (self.curr_state == ManStates.JUMPING and self.state_nframes[self.curr_state] == self.curr_frame + 1):
            self.change_state(ManStates.STAYING)

    def change_dir(self, man_dir):
        if not ManDir.is_valid(man_dir):
            raise AttributeError('Direction must be one of 0, 1')
        if self.man_dir != man_dir:
            self.man_dir = man_dir
            for state, frames in self.state_frames.items():
                self.state_frames[state] = flip_frames(frames)

    def move(self):
        if self.man_dir == ManDir.RIGHT:
            self.x += self.step
        if self.man_dir == ManDir.LEFT:
            self.x -= self.step

    def can_change_state(self):
        pass


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
