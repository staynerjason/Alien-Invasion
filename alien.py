import pygame 


class Alien(pygame.sprite.Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initializes the alien class."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load the alien image and set its rect atrbute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top of the screen.
        self.rect.x, self.rect.y = self.rect.size

        #Store the aliens exact horisonal position.
        self.x = float(self.rect.x)

        #Stores its size.
        self.WIDTH, self.HEIGHT = self.rect.size
    
    
    def check_edges(self):
        """Returns True if the alien is at the edge of the screen."""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0: 
            return True
   
   
    def update(self):
        """Moves alien around the screen."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)        
        self.rect.x = self.x

