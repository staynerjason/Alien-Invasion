import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A Class to manage the Bullets behavor."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.BULLET_COLOR

        # Creates a Bullet Rect
        self.rect = pygame.Rect(0, 0, self.settings.BULLET_WIDTH, self.settings.BULLET_HEIGHT)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullets position as a decimal.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.settings.bullet_speed

        #Update Position
        self.rect.y = self.y


    def draw_bullet(self):
        """Draws the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
