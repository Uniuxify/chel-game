import json
import pygame
from src.core.animation import Animation, Frame
from os import path

ANIMATION_JSON = r'..\res\Animations.json'
ROOT_PATH = r'../'
pygame.init()


def load_animation(entity_name: str, state_name: str):
    with open(ANIMATION_JSON) as f:
        animation_json = json.load(f)['Animations']

    for entity in animation_json:
        if entity['name'] == entity_name:
            for state in entity["states"]:

                if state['name'] == state_name:
                    state_anim = state['animation']
                    frames = []
                    for frame_json in state_anim['frames']:
                        img = pygame.image.load(path.join(ROOT_PATH, state_anim['frames_directory'], frame_json['file_name']))
                        frame = Frame(img)
                        for sound_fp in frame_json['sound_files']:
                            frame.add_sound(pygame.mixer.Sound(path.join(ROOT_PATH, sound_fp)))
                        frames.append(frame)

                    return Animation(frames, frames_order=state_anim['frames_order'], loop=state_anim['loop'])


if __name__ == '__main__':
    ANIMATION_JSON = r'../../res/Animations.json'
    ROOT_PATH = r'../../'
    print(load_animation('chel', 'dudka'))
