# simulation with 1 spring
import sys
from time import sleep

import pygame
import operator
import numpy as np

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button



WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (240,240,0)
LT_BLUE = (230,230,255)


class Game:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.fps = 120
        
        """
        ###For Fullscreen
        self.screen = pygame.display.set_mode((0, 0 ), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """
        ###For Low resolation
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        
        pygame.display.set_caption("Game")
        
        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        # Make the Play button.
        self.play_button = Button(self, "Play")
        
        self.offset = (int(self.settings.screen_width//2), int(self.settings.screen_height//2))
        
    def run_game(self, simulation_size, particles):
        self.simulation_size = simulation_size
        self.particles = particles
        
        for p in self.particles:
            p.visual(self.screen, self.offset)
        
        """Start the main loop for the game."""
        self.i= 0
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            
            if self.stats.game_active:
                pass
                
            self._uptade_screen()
            self.clock.tick(self.fps)
            if self.i < self.simulation_size - 1:
                self.i += 1
            else:
                self.i = 0
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.display.quit():
                        sys.exit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)                                            
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                    self._check_play_button(button_clicked)
                
    
    def _check_play_button(self, button_clicked):
        """ Start a new game when the player clicks Play."""        
        if  button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
           
            
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            
                        
    def _check_keydown_events(self, event):
        """ Respond to keypresses."""
        if event.key == pygame.K_q:
            if event.type == pygame.display.quit():
                sys.exit()
            sys.exit()
        elif event.key == pygame.K_p:
            button_clicked = True
            self._check_play_button(button_clicked)
        elif event.key == pygame.K_SPACE:
            pass
        
    
    def _check_keyup_events(self, event):
        """ Respond to keypresses."""
        pass

        
        
        
    def _uptade_screen(self):
        """Uptade images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)
        else:
            #self.update_points()
            for part in self.particles:
                part.draw(self.i)
        
            # Draw the score information.
            #self.sb.show_score()
            
        # Make the most recently dwn screen visible.
        pygame.display.flip()
"""
if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()"""
