from random import choice, randint

import pygame
from pygame import display, event, locals
from pygame.image import load
from pygame.sprite import Group, GroupSingle
from pygame.time import Clock
from pygame.transform import scale

from src.constants import SCREEN_SIZE, TICK, Directions
from src.info import InfoBar
from src.matrix import Matrix
from src.pawn import Pawn

RUNNING = True


pygame.init()
clock = Clock()
screen = display.set_mode(SCREEN_SIZE)
display.set_caption('Dungeons')
background = scale(load('src/images/background.png'), SCREEN_SIZE)

matrix_group = Group()
pawn_group = GroupSingle()
enemies_group = Group()


matrix = Matrix(10, 6, matrix_group)


def create_pawn(x, y, matrix, group) -> Pawn:
    node = matrix[x][y]
    pawn = Pawn(node=node, direction=Directions.DOWN)
    group.add(pawn)
    return pawn


pawn = create_pawn(0, 0, matrix, pawn_group)
enemies = [
    create_pawn(x, y, matrix, enemies_group)
    for x, y in (
        (5, 1),
        (5, 2),
        (5, 3)
    )
]

info_bar_group = Group()
info_bar = InfoBar(pawn=pawn)
info_bar_group.add(info_bar)


def interate_pawn(pawn: Pawn):
    if pawn.node_target:
        if randint(1, 100) >= 20:
            pawn.step()
        else:
            pawn.rotate(choice((True, False)))
    else:
        pawn.rotate(choice((True, False)))


while RUNNING:
    clock.tick(TICK)

    screen.blit(background, (0, 0))

    matrix_group.draw(screen)
    pawn_group.draw(screen)
    info_bar_group.draw(screen)
    enemies_group.draw(screen)

    matrix_group.update()
    info_bar_group.update(screen)
    pawn_group.update()
    enemies_group.update()

    display.update()

    for e in event.get():

        if e.type == locals.QUIT:
            pygame.quit()
            RUNNING = False

        if e.type == pygame.KEYUP:
            pawn.register_action(event=e)

        if e.type == pygame.KEYUP and e.key == pygame.K_f:
            import pdb
            pdb.set_trace()
