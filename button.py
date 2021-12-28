import pygame


class Button:
    def __init__(self, ai_game, msg) -> None:
        """Initializes buttons atribues."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.WIDTH, self.HEIGHT = 200, 50
        self.BUTTON_COLOR = (0,255,0)
        self.TEXT_COLOR = (255,255,255)
        self.FONT = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0,0,self.WIDTH,self.HEIGHT)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turns msg into rendered image and center text on the button."""
        self.msg_image = self.FONT.render(msg, True, self.TEXT_COLOR, self.BUTTON_COLOR)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw(self):
        """Draws a blank button and then draws msg."""
        self.screen.fill(self.BUTTON_COLOR, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)