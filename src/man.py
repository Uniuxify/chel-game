import enum

from core.game_object import State, GameObject
from src.core.animation import AnimationEvents  # TODO: Not working without 'src.' for some reason. Investigate later. (Probably enum comparison problem)

from core.conv_types import tPoint
import core.loader as loader


class RunningState(State):
    def __init__(self, game_object):
        name = 'running'
        animation = loader.load_animation('chel', name)

        super().__init__(name, game_object, animation)


class StayingState(State):
    def __init__(self, game_object):
        name = 'staying'
        animation = loader.load_animation('chel', name)

        super().__init__(name, game_object, animation)


class DudkaState(State):
    def __init__(self, game_object):
        name = 'dudka'
        animation = loader.load_animation('chel', name)
        animation.event_manager.subscribe(AnimationEvents.animation_ended,
                                          lambda: game_object.change_state(Man.STATES.STAYING))

        super().__init__(name, game_object, animation)


class JumpingState(State):
    def __init__(self, game_object):
        name = 'jumping'
        animation = loader.load_animation('chel', name)

        # hit_box = create_hitbox(list_of_points(
        #     list_x=,
        #     list_y=
        # ))

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
        super().__init__(name='chel', pos=pos, states_dict=states_dict, curr_state=Man.STATES.STAYING)
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
