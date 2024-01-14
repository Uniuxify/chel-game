from random import randint


def random_color():
    return tuple([randint(0, 255) for _ in range(3)])
