from typing import List, Literal
from src.core.conv_types import tSurface, tSound

import pygame

from src.core.geometry import Point
import enum

from collections import defaultdict


class Frame:
    def __init__(self, image: tSurface, sounds: List[tSound] = None, pivots: List[Point] = None):
        self.image = image
        self.pivots = pivots
        self.sounds = sounds if sounds is not None else []

        self.height = self.image.get_height()
        self.width = self.image.get_width()

    def render(self, screen, pos):
        screen.blit(self.image, pos)
        for sound in self.sounds:
            sound.play()

    def flip(self, flip_x=True, flip_y=True):
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)
        if self.pivots:
            new_pivots = [Point(self.width - pivot.x if flip_x else pivot.x,
                                self.height - pivot.x if flip_y else pivot.y)
                          for pivot in self.pivots]
            self.pivots = new_pivots

    def add_sound(self, sound: tSound):
        self.sounds.append(sound)


class FramesOrder(enum.Enum):
    reverse = 'reverse'
    default = 'default'
    back_and_forth = 'back-and-forth'
    forth_and_back = 'forth-and-back'

    @staticmethod
    def values():
        return tuple([e.value for e in FramesOrder])


class EventManager:
    def __init__(self):
        self.handlers = defaultdict(list)

    def subscribe(self, event_type, handler):
        self.handlers[event_type].append(handler)

    def unsubscribe(self, event_type, handler):
        self.handlers[event_type].remove(handler)

    def notify(self, event_type, *args, **kwargs):
        for handler in self.handlers[event_type]:
            handler(*args, **kwargs)


class AnimationEvents(enum.Enum):
    animation_ended = 0
    new_loop = 1


class Animation:
    def __init__(self, frames: tuple[Frame, ...],  # TODO: Добавить проверку того, что все кадры одинакового размер
                 on_animation_end=None,
                 frames_order: Literal['default', 'reverse', 'forth-and-back', 'back-and-forth'] = 'default',
                 # frames_order=FramesOrder.default,
                 loop: int = -1):

        if loop == 0:
            raise ValueError('loop cannot be zero')
        # if frames_order not in FramesOrder.values():
        #     raise ValueError(f'frames_order must be one of {FramesOrder.values()}, not {frames_order}')

        self.frames = frames

        self.frames_order = frames_order

        if self.frames_order in (FramesOrder.reverse.value, FramesOrder.back_and_forth.value):
            self.curr_frame = self.last_frame()
        else:
            self.curr_frame = 0

        self.loops_left = loop
        self.loop = loop
        self.paused = False

        self.step = 1 if frames_order in (FramesOrder.default.value, FramesOrder.forth_and_back.value) else -1

        self.on_animation_end = on_animation_end

        self.event_manager = EventManager()
        self.is_ended = False

    def __iter__(self):
        self.loops_left = self.loop
        if self.frames_order == FramesOrder.default.value:
            return iter(self.frames)
        elif self.frames_order == FramesOrder.reverse.value:
            return iter(reversed(self.frames))
        elif self.frames_order == FramesOrder.back_and_forth.value:
            return iter(tuple(reversed(self.frames)) + self.frames)
        elif self.frames_order == FramesOrder.forth_and_back.value:
            return iter(self.frames + tuple(reversed(self.frames)))

    def __next__(self) -> Frame:
        frame = self.frames[self.curr_frame]
        if self.paused or self.is_ended:
            return frame

        self.curr_frame += self.step
        if self.curr_frame == self.last_frame() + 1:
            if self.frames_order == FramesOrder.default.value or self.frames_order == FramesOrder.back_and_forth.value:
                self.curr_frame = 0
                self.loops_left -= 1
                self.event_manager.notify(AnimationEvents.new_loop)
            if self.frames_order == FramesOrder.forth_and_back.value or self.frames_order == FramesOrder.back_and_forth.value:
                self.step *= -1
                self.curr_frame += self.step

        elif self.curr_frame == -1:
            if self.frames_order == FramesOrder.reverse.value or self.frames_order == FramesOrder.forth_and_back.value:
                self.loops_left -= 1
                self.event_manager.notify(AnimationEvents.new_loop)
                self.curr_frame = self.last_frame()
            if self.frames_order == FramesOrder.back_and_forth.value or self.frames_order == FramesOrder.forth_and_back.value:
                self.step *= -1
                self.curr_frame += self.step

        if self.loops_left == 0:
            self.loops_left = self.loop
            self.is_ended = True
            self.event_manager.notify(AnimationEvents.animation_ended)
        return frame

    def next_frame(self) -> Frame:
        return next(self)

    def n_frames(self):
        return len(self.frames)

    def flip_frames(self, flip_x=True, flip_y=True):
        for frame in self.frames:
            frame.flip(flip_x, flip_y)

    def add_sound(self, i_frame, sound: tSound):
        self.frames[i_frame].add_sound(sound)

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def reset(self):
        self.unpause()
        self.is_ended = False
        self.loops_left = self.loop
        if self.frames_order in (FramesOrder.reverse.value, FramesOrder.back_and_forth.value):
            self.curr_frame = self.last_frame()
        else:
            self.curr_frame = 0

    def last_frame(self):
        return len(self.frames) - 1
