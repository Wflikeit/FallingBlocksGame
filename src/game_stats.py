class GameStats:
    """
    Monitoring stats in game "Alien invasion
    """

    def __init__(self, ai_game):
        """Initializing data stats"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Booting game Alien invasion in inactive mode
        self.game_active = False

    def reset_stats(self):
        """
        Initializing stats that can be changed during game
        """
        self.score = 0
        self.level = 1