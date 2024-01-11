from core.game_object import State, create_hitbox, GameObject
from core.animation import Animation, Frame, AnimationEvents
from core.geometry import list_of_points
from os import path
import pygame

from core.conv_types import tPoint


class RunningState(State):
    def __init__(self, game_object):
        frames_dir = '../res/animations/chel/running'
        frame_files = ['1.png', '2.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames)

        super().__init__(game_object, animation)


class StayingState(State):
    def __init__(self, game_object):
        frames_dir = '../res/animations/chel/staying'
        frame_files = ['1.png', '2.png', '3.png', '4.png', '5.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames)

        super().__init__(game_object, animation)


class DudkaState(State):
    def __init__(self, game_object):
        frames_dir = r'..\res\animations\chel\dudka'
        frame_files = ['1.png', '2.png', '3.png', '4.png',
                       '5.png', '6.png', '7.png', '8.png',
                       '9.png', '10.png', '11.png', '12.png',
                       '13.png', '14.png', '15.png', '16.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames,
                              loop=1)
        super().__init__(game_object, animation)
        self.animation.event_manager.subscribe(AnimationEvents.animation_ended,
                                               lambda: self.game_object.change_state(StayingState(game_object)))


class JumpingState(State):
    def __init__(self, game_object):
        name = 'jumping'

        frames_dir = '../res/animations/chel/jumping'
        frame_files = ['1.png', '2.png', '3.png', '4.png']

        # hit_box = create_hitbox(list_of_points(
        #     list_x=,
        #     list_y=
        # ))

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames,
                              frames_order='forth-and-back',
                              loop=1)
        super().__init__(game_object, animation)
        self.animation.event_manager.subscribe(AnimationEvents.animation_ended,
                                               lambda: self.game_object.change_state(StayingState(game_object)))


class Man(GameObject):
    def __init__(self, pos: tPoint):
        super().__init__(state=StayingState(self), name='Man', pos=pos)
        self.step = 30
        self.facing = 'right'

    def move(self):
        if self.facing == 'right':
            self.shift(x=self.step, y=0)
        if self.facing == 'left':
            self.shift(x=-self.step, y=0)