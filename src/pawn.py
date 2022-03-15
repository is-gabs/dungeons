from typing import List

import pygame
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import rotate, scale

from src.constants import CHAR_MARGIN, CHAR_SIZE, DIRECTIONS, Directions


class Action:
    def __init__(self, func, **params):
        self.func = func
        self.params = params

    def __repr__(self) -> str:
        dictionary = {
            'attack': 'A',
            'protect': 'P',
            'step': 'W',
            'rotate': 'R'
        }

        return dictionary[self.func.__name__]

    def run(self):
        self.func(**self.params)


class Pawn(Sprite):
    def __init__(self, node=None, direction=Directions.RIGHT) -> None:
        super().__init__()

        self.image = rotate(
            scale(
                load('src/images/arrow.png'),
                (CHAR_SIZE, CHAR_SIZE)
            ), direction.value
        )
        self.direction = direction

        self.attack_points = 1
        self.max_hp = 5
        self.current_hp = 5
        self._base_defense_points = 1

        self._is_protected = False

        self.rect = self.image.get_rect()

        self._is_running = False
        self.actions: List[Action] = []

        if node:
            self.register_node(node)
            self.node = node

    def rotate(self, horaire: bool = False):
        degrees = 270 if horaire else 90
        print(f'rotating {degrees} degrees')
        self.image = rotate(self.image, degrees)

        directions = DIRECTIONS[::] if horaire else DIRECTIONS[::-1]

        index = directions.index(self.direction)

        if directions[-1] == self.direction:
            self.direction = directions[0]
        else:
            self.direction = directions[index + 1]

    def _set_coordinates(self, node):
        self.rect.x = node.rect.x + CHAR_MARGIN
        self.rect.y = node.rect.y + CHAR_MARGIN
        self.node = node

    @property
    def node_target(self):
        target = self.node.references[self.direction]
        if target:
            return target

    @property
    def available_node_target(self):
        target = self.node_target
        if target and not target.value:
            return target

    def step(self, **params):
        print('step')
        target = self.available_node_target
        if target:
            self.node.value, target.value = target.value, self.node.value
            self._set_coordinates(target)

    def register_node(self, node):
        self.rect.x = node.rect.x + CHAR_MARGIN
        self.rect.y = node.rect.y + CHAR_MARGIN
        node.value = self

    def update(self):
        if self.actions and self._is_running:
            self.actions.pop().run()
            if not self.actions:
                self._is_running = False

        if self.actions:
            print(self.actions)

    @property
    def defense_points(self):
        if self._is_protected:
            return self._base_defense_points * 2
        return self._base_defense_points

    def protect(self):
        self._is_protected = True

    def attack(self):
        self._is_protected = False
        target = self.node_target
        if target:
            enemy = target.value
            if enemy:
                if self.direction == enemy.direction:
                    print('Advantage attack!')
                    attack = self.attack_points * 2
                elif (
                    (self.direction.value - enemy.direction.value) == 180
                ) or (
                    (enemy.direction.value - self.direction.value) == 180
                ):
                    print('Not good attack!')
                    attack = self.attack_points / 2
                else:
                    print('Side attack!')
                    attack = self.attack_points
                attack -= enemy.defense_points
                enemy.current_hp -= attack if attack > 0 else 0
                print(f'Attack: {enemy.current_hp}/{enemy.max_hp}')
                if enemy.current_hp <= 0:
                    enemy.kill()
                    target.value = None
            else:
                print('Empty attack')
        else:
            print('Punching the wall')

    def register_action(self, event):
        if not self._is_running:
            if event.key == pygame.K_UP:
                self.actions.insert(0, Action(self.step))
            elif event.key == pygame.K_LEFT:
                self.actions.insert(0, Action(self.rotate, horaire=False))
            elif event.key == pygame.K_RIGHT:
                self.actions.insert(0, Action(self.rotate, horaire=True))
            elif event.key == pygame.K_z:
                self.actions.insert(0, Action(self.attack))
            elif event.key == pygame.K_x:
                self.actions.insert(0, Action(self.protect))
            elif event.key == pygame.K_SPACE:
                if self.actions:
                    self._is_running = True
