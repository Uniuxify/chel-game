import pygame
from src.core.conv_types import tPoint, tSurface, to_point
from typing import Union
from src.core.animation import Animation, Frame
from src.core.geometry import Point


# Состоит из множества прямоугольников
class HitBox:
    @classmethod
    def from_frame(cls, frame: Frame):
        img = pygame.surfarray.array2d(frame.image)

        rectangles = []
        for pivot in frame.pivots:
            w = 4
            h = 4

            # Координаты левого верхнего угла
            x0 = pivot.x - w // 2
            y0 = pivot.y - h // 2

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

            rect = pygame.Rect(x0, y0, w, h)
            rectangles.append(rect)

        return cls(frame.image.get_width(), frame.image.get_height(), rectangles)

    def __init__(self, orig_width, orig_height, rectangles: list[pygame.Rect, ...], ):
        self.rectangles = rectangles
        self.orig_width = orig_width
        self.orig_height = orig_height

    def render(self, screen: tSurface):
        for rect in self.rectangles:
            pygame.draw.rect(screen, (255, 0, 0), rect, width=3)

    def flip(self, flip_x=True, flip_y=True):
        flipped = []
        for rect in self.rectangles:
            new_x = self.orig_width - rect.x - rect.width if flip_x else rect.x
            new_y = self.orig_height - rect.y - rect.height if flip_y else rect.y
            flipped.append(pygame.Rect(new_x, new_y, rect.width, rect.height))
        self.rectangles = flipped

    def is_collide(self, other):
        pass


class State:
    def __init__(self, name, game_object, animation: Animation, hit_boxes: Union[list[HitBox, ...], None] = None):
        if hit_boxes:
            if len(hit_boxes) != animation.n_frames():
                raise ValueError(f'hit_boxes and animation must have same length ({len(hit_boxes)} != {animation.n_frames()})')
        self.hit_boxes = hit_boxes
        self.animation = animation
        self.game_object = game_object
        self.name = name


class GameObject:
    def __init__(self, name: str, pos: tPoint, states_dict, curr_state):
        self.name = name
        self.states_dict = states_dict
        self.state = states_dict[curr_state]

        self.pos = to_point(pos)

    def render(self, screen: tSurface, show_hit_boxes=False):
        self.state.animation.next_frame().render(screen, self.pos.as_tuple())
        if show_hit_boxes:
            for hit_box in self.state.hit_boxes:
                hit_box.render(screen)

    def change_state(self, man_state):

        self.state = self.states_dict[man_state]
        self.state.animation.reset()

    def shift(self, x, y):
        self.pos += Point(x, y)

    def flip(self, flip_x=True, flip_y=True):
        for state in self.states_dict.values():
            state.animation.flip_frames(flip_x, flip_y)
            if state.hit_boxes:
                for hit_box in state.hit_boxes:
                    hit_box.flip(flip_x, flip_y)

    def flip_horizontally(self):
        self.flip(flip_x=True, flip_y=False)

    def flip_vertically(self):
        self.flip(flip_x=False, flip_y=True)
