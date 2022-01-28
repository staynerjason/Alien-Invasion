#!/usr/bin/env python
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import time

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import ScoreBoard
from ship import Ship
from settings import Settings



class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game and creates game resources."""
        pygame.init()
        self._init_joysticks()
        self.settings = Settings()
        self.windowed()
        
        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        pygame.display.set_caption("Alien Invasion")
        self.play_button = Button(self, "Play")

        
    def run_game(self):
        """Start the main loop for game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self._update_ship()
                self._update_bullets()
                self._update_alien()
            self._update_screen()


    def _check_events(self):
        """Responds to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            if event.type == pygame.JOYAXISMOTION:
                self._check_joy_axis_events()
            if event.type == pygame.JOYBUTTONDOWN:
                self._check_joy_button_down_events()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_play_button(self, mouse_pos):
        """Starts a new game when the play button is pressed."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            self.stats.game_active = True
    

    def _check_joy_button_down_events(self):
        """Handles joystick button press events."""
        if self.joystick_0.get_button(0):
            self.fire_bullet()     
        
    
    def _check_joy_axis_events(self):
        """Handles joystick axis events."""
        if self.joystick_0.get_axis(0) > .2:
            self.ship.moving_right = True
        elif self.joystick_0.get_axis(0) < -.2:
            self.ship.moving_left = True
        else:
            self.ship.moving_right = False 
            self.ship.moving_left = False
    
    
    def _check_keydown_events(self, event):
        """Reponds to key press events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        

    def _check_keyup_events(self, event):
        """Reponds to key release events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
    
    def fire_bullet(self):
        """Creates new bullet instance."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Updates position of the bullets and remooves the old ones."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_bullet_collisions()
    

    def _check_bullet_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()


    def _create_alien(self, alien_number, row_number):    
        """Creates an alien and places it in a row."""
        alien = Alien(self)
        alien.x = alien.WIDTH + 2 * alien.WIDTH * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.HEIGHT + 2 * alien.HEIGHT * row_number
        self.aliens.add(alien)

    
    def _update_alien(self):
        """Updates all the aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    
    def _create_fleet(self):
        """Create the alien fleet."""
        alien = Alien(self)
        avilable_space_x = self.settings.SCREEN_WIDTH - (2 * alien.WIDTH)
        number_aliens_x = avilable_space_x // (2 * alien.WIDTH)
        availible_space_y = (self.settings.SCREEN_HIGHT - (3 * alien.WIDTH) - self.ship.HEIGHT)
        number_rows = availible_space_y // (2 * alien.HEIGHT)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    
    def _check_fleet_edges(self):
        """Responds appropriately if any of the aliens have reached the edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop entire fleet and change the fleets direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_aliens_bottom(self):
        """Check if any aliens have made it to the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _update_ship(self):
        """Updates the ship."""
        self.ship.update()        

    
    def _ship_hit(self):
        """Handles a ship collision."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center()
            time.sleep(1)
        else:
            self.stats.write_high_score()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def windowed(self):
        """Initailizes a windowed version of the game"""
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HIGHT))


    def full_screen(self):
        """Initailizes a fullscreen version of the game."""
        self.screen = pygame.display.set_mode((0,0), pygame.constants.FULLSCREEN)
        self.settings.SCREEN_WIDTH = self.screen.get_rect().width
        self.settings.SCREEN_HIGHT = self.screen.get_rect().height


    def _update_screen(self):
        """Updates images on the screen, and flip to new screen."""
        self.screen.fill(self.settings.BG_COLOR)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.draw()
        if not self.stats.game_active:
            self.play_button.draw()
        pygame.display.flip()


    def _init_joysticks(self):
            pygame.joystick.init()
            if  pygame.joystick.get_count() > 0:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
                self.joystick_0 = joysticks[0]



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()