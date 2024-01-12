import pygame
import sys
from man import Man

pygame.init()
SCREEN = pygame.display.set_mode((1000, 800))
SCREEN.fill((255, 255, 255))
pygame.display.set_caption('Чел')
icon_img = pygame.image.load('../res/icon.png')
pygame.display.set_icon(icon_img)

FPS_CLOCK = pygame.time.Clock()
FPS = 5


class Game:
    def __init__(self):
        self.man = Man((200, 200))

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.man.change_state(Man.STATES.RUNNING)
                        self.man.change_facing('left')

                    elif event.key == pygame.K_RIGHT:
                        self.man.change_state(Man.STATES.RUNNING)
                        self.man.change_facing('right')

                    elif event.key == pygame.K_SPACE:
                        self.man.change_state(Man.STATES.JUMPING)
                    elif event.key == pygame.K_1:
                        self.man.change_state(Man.STATES.DUDKA)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.man.facing == 'left':
                        self.man.change_state(Man.STATES.STAYING)
                    elif event.key == pygame.K_RIGHT and self.man.facing == 'right':
                        self.man.change_state(Man.STATES.STAYING)

            if self.man.curr_state == Man.STATES.RUNNING:
                self.man.move()

            self.draw_scene()
            FPS_CLOCK.tick(FPS)

    def draw_scene(self):
        SCREEN.fill((255, 255, 255))
        self.man.render(SCREEN)

        pygame.display.update()

    def terminate(self):
        pygame.quit()
        sys.exit()


def scale_frames(frames, scale):  # TODO: Адаптировать для работы с pivots
    return list(
            map(lambda frame: pygame.transform.smoothscale(frame, (frame.get_size()[0] * scale, frame.get_size()[1] * scale)),
                frames))


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
