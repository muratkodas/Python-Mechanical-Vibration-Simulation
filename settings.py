# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:05:52 2019

@author: murat
"""

class Settings:
    """A class to store all settings for Allien Invasion."""
    
    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        
        self.screen_width  = 640
        self.screen_height = 480
        # Set the background color.
        self.bg_color = (230, 230, 230)
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game."""
        pass
    
    def increase_speed(self):
        """ Increase speed settings and alien point values."""
        pass
        