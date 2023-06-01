class GameStats:
    """
    Monitoring stats in game "Alien invasion
    """

    def __init__(self, fb_game) -> None:
        """Initializing data stats"""
        self.level = 0
        self.score = 0
        self.settings = fb_game.settings
        self.reset_stats()

        # Booting game in inactive mode
        self.game_active = False

    def reset_stats(self) -> None:
        """
        Initializing stats that can be changed during game
        """
        self.score = 0
        self.level = 1
