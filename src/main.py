import pygame


def scale_frames(frames, scale):  # TODO: Адаптировать для работы с pivots
    return list(
            map(lambda frame: pygame.transform.smoothscale(frame, (frame.get_size()[0] * scale, frame.get_size()[1] * scale)),
                frames))


def main():
    pass


if __name__ == '__main__':
    main()
