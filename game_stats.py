


class GameStats:
    """Tracks stats for Alien Invasion."""

    def __init__(self, ai_game) -> None:
        """Initalizes statistics."""
        self.settings = ai_game.settings
        self.game_active = False
        self.high_score : int = 0
        self.reset_stats()


    def reset_stats(self):
        """Initializes stats that can change durring the game."""
        self.ships_left : int = self.settings.ship_limit
        self.score : int = 0
        self.level = 0