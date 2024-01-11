from typing import Tuple


class Point:
    @classmethod
    def from_tuple(cls, xy: Tuple[float, float]):
        return cls(xy[0], xy[1])

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def as_tuple(self):
        return self.x, self.y

    def move(self, x, y):
        self.x += x
        self.y += y


def list_of_points(list_x: list[float, ...], list_y: list[float, ...]) -> list[Point]:
    return [Point.from_tuple(xy) for xy in zip(list_x, list_y)]

