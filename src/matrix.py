from pygame.image import load
from pygame.sprite import DirtySprite, Group
from pygame.transform import scale

from src.constants import (
    AVAILABLE_SCREEN_HEIGHT,
    BLOCK_SIZE,
    DIRECTIONS,
    SCREEN_WIDTH,
    Directions
)
from src.pawn import Pawn


class Node(DirtySprite):
    def __init__(self, x: int, y: int, margin_x=0, margin_y=0) -> None:
        super().__init__()
        self.image = scale(
            load('src/images/ground.png'),
            (BLOCK_SIZE, BLOCK_SIZE)
        )

        self.x = x
        self.y = y

        self.rect = self.image.get_rect()
        self.rect.x = self.x * BLOCK_SIZE + margin_x
        self.rect.y = self.y * BLOCK_SIZE + margin_y

        self.value: Pawn = None

        self.references = {direction: None for direction in DIRECTIONS}

    def __repr__(self) -> str:
        return f'Node: ({self.x}, {self.y})'


class Matrix:
    def __init__(self, width: int, height: int, group: Group):

        self._width = width
        self._height = height
        length_x = width * BLOCK_SIZE
        length_y = height * BLOCK_SIZE

        margin_x = (SCREEN_WIDTH - length_x) / 2
        margin_y = (AVAILABLE_SCREEN_HEIGHT - length_y) / 2

        grid = []
        for x in range(width):
            row = []
            for y in range(height):
                node = Node(x, y, margin_x=margin_x, margin_y=margin_y)
                group.add(node)
                row.append(node)
            grid.append(row)

        self.grid = grid

        self._populate_node_references()

    def __getitem__(self, index):
        return self.grid[index]

    def _populate_node_references(self):
        for x, row in enumerate(self.grid):
            for y, node in enumerate(row):
                if x == 0:
                    node.references[Directions.LEFT] = None
                    node.references[Directions.RIGHT] = self.grid[x + 1][y]
                elif x == (self._width - 1):
                    node.references[Directions.RIGHT] = None
                    node.references[Directions.LEFT] = self.grid[x - 1][y]
                else:
                    node.references[Directions.RIGHT] = self.grid[x + 1][y]
                    node.references[Directions.LEFT] = self.grid[x - 1][y]
                if y == 0:
                    node.references[Directions.UP] = None
                    node.references[Directions.DOWN] = row[y + 1]
                elif y == (self._height - 1):
                    node.references[Directions.DOWN] = None
                    node.references[Directions.UP] = row[y - 1]
                else:
                    node.references[Directions.DOWN] = row[y + 1]
                    node.references[Directions.UP] = row[y - 1]
