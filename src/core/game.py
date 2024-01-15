import pygame
import sys

from src.core.conv_types import tPoint, tSurface, to_point
from src.core.animation import Animation, Frame
from src.core.geometry import Point
from src.core.utils import random_color


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
            _break = False
            while not ready:
                ready = True
                # Координаты нижнего правого угла
                x1 = x0 + w
                y1 = y0 + h

                if y0 < 0 or x0 < 0 or x1 >= 500 or y1 >= 500:
                    break

                top_edge = img[x0:x1, y0]
                bottom_edge = img[x0:x1, y1]
                left_edge = img[x0, y0:y1]
                right_edge = img[x1, y0:y1]
                if list(top_edge).count(0) in (0, 1) and list(top_edge).count(16777215) in (0, 1):
                    y0 -= 2
                    h += 2
                    ready = False
                if list(bottom_edge).count(0) in (0, 1) and list(bottom_edge).count(16777215) in (0, 1):
                    h += 2
                    ready = False
                if list(left_edge).count(0) in (0, 1) and list(left_edge).count(16777215) in (0, 1):
                    x0 -= 2
                    w += 2
                    ready = False
                if list(right_edge).count(0) in (0, 1) and list(right_edge).count(16777215) in (0, 1):
                    w += 2
                    ready = False

            rect = pygame.Rect(x0, y0, w, h)
            rectangles.append(rect)
        return cls(frame.image.get_width(), frame.image.get_height(), rectangles)

    @classmethod
    def from_rect(cls, rect: pygame.Rect):
        return cls(rect.width, rect.height, [rect])

    @staticmethod
    def from_frames(frames: list[Frame]):
        hit_boxes = []
        for frame in frames:
            hit_boxes.append(HitBox.from_frame(frame))
        return hit_boxes

    def __init__(self, orig_width, orig_height, rectangles: list[pygame.Rect], ):
        self.rectangles = rectangles
        self.orig_width = orig_width
        self.orig_height = orig_height
        self.mime_box = None
        self._update_mime_box()

    def _update_mime_box(self):
        if self.rectangles:
            first_rect = self.rectangles[0]
            min_x = first_rect.x
            min_y = first_rect.y
            max_x = first_rect.x + first_rect.width
            max_y = first_rect.y + first_rect.height
            for rect in self.rectangles:
                min_x = min(min_x, rect.x)
                min_y = min(min_y, rect.y)

                max_x = max(max_x, rect.x + rect.width)
                max_y = max(max_y, rect.y + rect.height)
            x, y = min_x, min_y
            w, h = max_x - x, max_y - y
            self.mime_box = pygame.Rect(x, y, w, h)

    def render(self, screen: tSurface, pos: Point):
        for rect in self.rectangles:
            pygame.draw.rect(screen, random_color(), rect.move(pos.x, pos.y), width=3)

        if self.mime_box:
            pygame.draw.rect(screen, (255, 0, 0), self.mime_box.move(pos.x, pos.y), width=3)

    def flip(self, flip_x=True, flip_y=True):
        flipped = []
        for rect in self.rectangles:
            new_x = self.orig_width - rect.x - rect.width if flip_x else rect.x
            new_y = self.orig_height - rect.y - rect.height if flip_y else rect.y
            flipped.append(pygame.Rect(new_x, new_y, rect.width, rect.height))
        self.rectangles = flipped

    def scale(self, scale):
        self.orig_width *= scale
        self.orig_height *= scale
        for rect in self.rectangles:
            rect.update(rect.x * scale, rect.y * scale, rect.w * scale, rect.h * scale)
        self._update_mime_box()

    def is_collide(self, other):
        pass


class State:
    def __init__(self, name, game_object, animation: Animation):

        hit_boxes = HitBox.from_frames(animation.frames)

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
        self.curr_state = curr_state
        self.state = states_dict[self.curr_state]

        self.pos = to_point(pos)

    def render(self, screen: tSurface, show_hit_boxes=False, show_pivots=False):
        # TODO: Эта строчка нужна, т.к. состояние может измениться в процессе получения кадра (AnimationEvents.animation_ended).
        #  Это плохо, надо потом исправить. Анимация заканчивается не после получения последнего кадра, а после его отрисовки
        state = self.state
        frame_ind, frame_to_draw = self.state.animation.next_frame()
        frame_to_draw.render(screen, self.pos.as_tuple(), show_pivots=show_pivots)
        if show_hit_boxes:
            state.hit_boxes[frame_ind].render(screen, self.pos)

    def change_state(self, state):
        self.curr_state = state
        self.state = self.states_dict[self.curr_state]
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

    def scale(self, scale):
        for state in self.states_dict.values():
            state.animation.scale_frames(scale)
            if state.hit_boxes:
                for hit_box in state.hit_boxes:
                    hit_box.scale(scale)


class Scene:
    def __init__(self, game):
        self.game_objects = []
        self.game = game

    def update(self):
        """Updates inner state of all objects on scene"""
        pass

    def render(self, screen, show_hit_boxes=False):
        """Renders all objects on scene"""
        screen.fill((255, 255, 255))
        for obj in self.game_objects:
            obj.render(screen, show_hit_boxes)

    def add_object(self, obj: GameObject):
        self.game_objects.append(obj)


class Game:
    def __init__(self, game_name: str, icon_fp: str):
        self.scene = None
        self.game_name = game_name
        self.fps_clock = pygame.time.Clock()
        self.fps = 5

        pygame.init()
        pygame.display.set_caption(self.game_name)

        icon_img = pygame.image.load(icon_fp)
        pygame.display.set_icon(icon_img)

        self.screen = pygame.display.set_mode((1000, 800))
        self.screen.fill((255, 255, 255))

    def set_scene(self, scene: Scene):
        self.scene = scene

    def start(self):
        """Starts game loop"""
        while True:
            self.scene.update()
            self.scene.render(self.screen, show_hit_boxes=True)

            self.fps_clock.tick(self.fps)
            pygame.display.update()

    def end(self):
        pygame.quit()
        sys.exit()




