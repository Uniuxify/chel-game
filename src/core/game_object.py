import pygame
from src.core.conv_types import tPoint, tSurface, to_point
from typing import Union
from src.core.animation import Animation, AnimationEvents
from src.core.geometry import Point


# Состоит из множества прямоугольников
class HitBox:
    def __init__(self, rectangles: list[pygame.Rect, ...], ):
        self.rectangles = rectangles

    def render(self, screen: tSurface):
        for rect in self.rectangles:
            pygame.draw.rect(screen, (255, 0, 0), rect, width=3)

    def is_collide(self, other):
        pass


def create_hitbox(img, pivots: list[Point, ...]):
    img = pygame.surfarray.array2d(img)
    hit_boxes = []
    for pivot in pivots:
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

        hitbox = pygame.Rect(x0, y0, w, h)
        hit_boxes.append(hitbox)

    return hit_boxes


class State:
    def __init__(self, game_object, animation: Animation, hit_boxes: Union[list[HitBox, ...], None] = None):
        if hit_boxes:
            if len(hit_boxes) != animation.n_frames():
                raise ValueError(f'hit_boxes and animation must have same length ({len(hit_boxes)} != {animation.n_frames()})')
        self.hit_boxes = hit_boxes
        self.animation = animation
        self.game_object = game_object


class GameObject:
    def __init__(self, state, name: str, pos: tPoint):
        self.name = name

        self.state = state

        self.pos = to_point(pos)

    def render(self, screen: tSurface, show_hit_boxes=False):
        screen.blit(next(self.state.animation).image, self.pos.as_tuple())
        if show_hit_boxes:
            for hit_box in self.state.hit_boxes:
                hit_box.render(screen)

    def change_state(self, state):
        print(f'state = {state}')
        self.state = state

    def shift(self, x, y):
        self.pos += Point(x, y)
