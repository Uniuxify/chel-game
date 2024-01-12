from typing import Union
import src.core.geometry as geom
import pygame

tPoint = Union[tuple[float, float], geom.Point]
tSurface = Union[pygame.Surface, pygame.SurfaceType]
tSound = pygame.mixer.Sound


def to_point(point: tPoint) -> geom.Point:
    if isinstance(point, tuple):
        return geom.Point.from_tuple(point)
    if isinstance(point, geom.Point):
        return point
    raise TypeError()
