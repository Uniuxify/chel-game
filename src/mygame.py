import pygame

from src.core.game import Game, Scene, GameObject
from src.core.geometry import Point
from os.path import abspath
from man import Man


class EmptyScene(Scene):
    def __init__(self, man, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.man = man
        self.add_object(man)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.end()
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


def main():
    man = Man(Point(100, 100))

    game = Game('Чел', abspath('../res/icon.png'))
    empty_scene = EmptyScene(man, game)
    game.set_scene(empty_scene)
    game.start()


if __name__ == '__main__':
    main()
