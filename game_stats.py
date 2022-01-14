import csv
import datetime



class GameStats:
    """Tracks stats for Alien Invasion."""

    def __init__(self, ai_game) -> None:
        """Initalizes statistics."""
        self.filename = 'high_score.csv'
        self.settings = ai_game.settings
        self.game_active = False
        self.high_score = self.read_high_score()
        self.reset_stats()


    def reset_stats(self):
        """Initializes stats that can change durring the game."""
        self.ships_left : int = self.settings.ship_limit
        self.score : int = 0
        self.level = 0


    def read_high_score(self) -> int:
        """Opens the high score file and returns the latest high score."""
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            all_lines = list(reader)
            line = [all_lines[-1]]
            score = line[-1]
            return int(score[1])
        

    def write_high_score(self):
        """Checks if new score is higher than the last score, then writes it to a new line in the high score file."""
        if self.score < self.high_score:
            return
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.datetime.now(),self.score])
        