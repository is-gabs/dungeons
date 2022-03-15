
from pygame import font
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale

from src.constants import AVAILABLE_SCREEN_HEIGHT, BAR_HEIGHT, BAR_WIDTH
from src.pawn import Pawn

font.init()
Font = font.SysFont(None,  30)
white = (255, 255, 255)


class InfoBar(Sprite):
    def __init__(self, pawn: Pawn) -> None:
        super().__init__()

        self.image = scale(
            load('src/images/bar.png'),
            (BAR_WIDTH, BAR_HEIGHT)
        )

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = AVAILABLE_SCREEN_HEIGHT

        self.pawn = pawn

    def update(self, screen):
        hp_info = Font.render(
            f'HP: {self.pawn.current_hp}/{self.pawn.max_hp}', True, white
        )
        hp_info_rect = hp_info.get_rect()
        hp_info_rect.x = self.rect.x + 10
        hp_info_rect.y = self.rect.y + 10

        screen.blit(hp_info, hp_info_rect)

        attack_info = Font.render(
            f'Attack: {self.pawn.attack_points}', True, white
        )

        attack_info_rect = attack_info.get_rect()
        attack_info_rect.x = self.rect.x + 10
        attack_info_rect.y = self.rect.y + 40

        screen.blit(attack_info, attack_info_rect)

        defence_info = Font.render(
            f'Defense: {self.pawn.defense_points}', True, white
        )
        defense_info_rect = defence_info.get_rect()
        defense_info_rect.x = self.rect.x + 10
        defense_info_rect.y = self.rect.y + 70

        screen.blit(defence_info, defense_info_rect)

        actions = [str(action) for action in self.pawn.actions]
        actions_info = Font.render(
            f'Actions queue: {", ".join(actions)}', True, white
        )

        actions_info_rect = actions_info.get_rect()
        actions_info_rect.x = self.rect.x + 100
        actions_info_rect.y = self.rect.y + 10

        screen.blit(actions_info, actions_info_rect)
