import enum

from core.game_object import State, GameObject
from core.animation import Animation, Frame, AnimationEvents
from os import path
import pygame

from core.conv_types import tPoint


class RunningState(State):
    def __init__(self, game_object):
        name = 'running'

        frames_dir = '../res/animations/chel/running'
        frame_files = ['1.png', '2.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames)

        super().__init__(name, game_object, animation)


class StayingState(State):
    def __init__(self, game_object):
        name = 'staying'

        frames_dir = '../res/animations/chel/staying'
        frame_files = ['1.png', '2.png', '3.png', '4.png', '5.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames)

        super().__init__(name, game_object, animation)


class DudkaState(State):
    def __init__(self, game_object):
        name = 'dudka'

        frames_dir = r'..\res\animations\chel\dudka'
        frame_files = ['1.png', '2.png', '3.png', '4.png',
                       '5.png', '6.png', '7.png', '8.png',
                       '9.png', '10.png', '11.png', '12.png',
                       '13.png', '14.png', '15.png', '16.png']

        frames = tuple([Frame(pygame.image.load(path.join(frames_dir, file))) for file in frame_files])
        animation = Animation(frames,
                              loop=1)
        animation.add_sound(5, pygame.mixer.Sound('../res/sounds/tuDU.wav'))
        super().__init__(name, game_object, animation)
        self.animation.event_manager.subscribe(AnimationEvents.animation_ended,
                                               lambda: self.game_object.change_state(Man.STATES.STAYING))


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
        super().__init__(name, game_object, animation)
        self.animation.event_manager.subscribe(AnimationEvents.animation_ended,
                                               lambda: self.game_object.change_state(Man.STATES.STAYING))


class Man(GameObject):
    class STATES(enum.Enum):
        RUNNING = 0
        JUMPING = 1
        DUDKA = 2
        STAYING = 3

    def __init__(self, pos: tPoint):
        states_dict = {
            Man.STATES.RUNNING: RunningState(self),
            Man.STATES.JUMPING: JumpingState(self),
            Man.STATES.DUDKA: DudkaState(self),
            Man.STATES.STAYING: StayingState(self)
        }
        super().__init__(name='Man', pos=pos, states_dict=states_dict, curr_state=Man.STATES.STAYING)
        self.step = 30
        self.facing = 'left'

    def move(self):
        if self.facing == 'right':
            self.shift(x=self.step, y=0)
        if self.facing == 'left':
            self.shift(x=-self.step, y=0)

    def change_facing(self, direction):
        if self.facing != direction:
            self.facing = direction
            self.flip_horizontally()
