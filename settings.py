import pygame
class Settings:
    """A class to store all settings for Alien Invasion."""
   
    def __init__(self):
        """Initailize the game's static settings."""
        #Screen Settings
        self.SCREEN_WIDTH : int = 1200
        self.SCREEN_HIGHT : int = 800
        self.BG_COLOR : int = (230,230,230)
        
        #Ship Settings
        self.ship_speed : int = 2
        self.ship_limit : int = 2

        #Bullet Settings
        self.BULLET_WIDTH : int   = 3
        self.BULLET_HEIGHT : int = 10
        self.BULLET_COLOR  : int = (60,60,60)
        self.bullet_speed  : int = 2
        self.bullets_allowed : int = 100

        #Alien Settigns
        self.alien_speed : int = 1
        self.fleet_drop_speed : int = 10
        self.fleet_direction : int = 1

        self.speedup_scale : float = 1.15
        self.score_scale : float = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Ship Settings
        self.ship_speed : int = 2
        
        # Bullet Settings
        self.bullet_speed : int = 2
       
        # Alien Settings
        self.alien_speed : int = 1
        self.alien_points : int = 50
        self.fleet_direction : int = 1

    def increase_speed(self):
        """Increase speed and point value settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        
        