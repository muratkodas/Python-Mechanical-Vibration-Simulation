class GameStats:
    """ Track statistics for Alien Invasion."""
    
    def __init__(self, game):
        """ Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()
        
        # Start the game in an passive state.
        self.game_active = False
        
        # High score should never be reset
        self.high_score = 0
        
    def reset_stats(self):
        """ Initialize statistics that can change during the game."""
        self.score = 0
        self.level = 1