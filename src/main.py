import pygame
import sys
import os
from os import path

pygame.init()
SCREEN = pygame.display.set_mode((500, 400))
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
        self.man.draw()

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


def scale_frames(frames, scale):
    return list(
            map(lambda frame: pygame.transform.smoothscale(frame, (frame.get_size()[0] * scale, frame.get_size()[1] * scale)),
                frames))


def flip_frames(frames):
    return list(map(lambda frame: pygame.transform.flip(frame, True, False), frames))


class Man:
    def __init__(self):
        self.curr_state = ManStates.STAYING
        self.state_frames = dict()
        self.state_nframes = dict()

        for state, state_name in ManStates.as_dict().items():
            frames_dir = f'../res/frames/{state_name}'
            frames = [path.join(frames_dir, f) for f in os.listdir(frames_dir) if path.isfile(path.join(frames_dir, f))]
            n_frames = len(frames)
            self.state_frames[state] = [pygame.image.load(f"../res/frames/{state_name}/{state_name}{i}.png") for i in range(1, n_frames+1)]
            self.state_nframes[state] = n_frames

        scale = 0.33
        for state, frames in self.state_frames.items():
            self.state_frames[state] = scale_frames(frames, scale)

        self.curr_frame = 0
        self.man_dir = ManDir.LEFT

        self.step = 30
        self.x = 100
        self.y = 200

    def draw(self):
        frames = self.state_frames[self.curr_state]
        SCREEN.blit(frames[self.curr_frame], (self.x, self.y))

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