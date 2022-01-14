import pygame

class Ship(pygame.sprite.Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initalize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.WIDTH, self.HEIGHT = self.rect.size

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ships position based on the moment flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0 : 
            self.rect.x -= self.settings.ship_speed
        self.x = self.rect.x
  

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


    def center(self):
        """Centers ship in the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)