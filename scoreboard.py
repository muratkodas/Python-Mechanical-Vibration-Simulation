import pygame.font
from pygame.sprite import Group


class Scoreboard:
    """ A class to report scroring information."""
    
    def __init__(self, game):
        """ Initialize scorekeeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        
        # Font settings for scoring informartion.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        
        
    def prep_score(self):
        """ Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, 0)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
        
        
    def prep_high_score(self):
        """ Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, 0)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def check_high_score(self):
        """ Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
        
    def show_score(self):
        """ Draw score and hight score to the screen."""
        self.prep_score()
        self.screen.blit(self.score_image, self.score_rect)
        self.prep_high_score()
        self.screen.blit(self.high_score_image, self.high_score_rect)