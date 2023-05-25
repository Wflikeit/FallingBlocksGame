import pygame


class Scoreboard:
    """Class dedicated to display user's points"""

    def __init__(self, tf_game):
        """Initializing score atributes """
        self.screen = tf_game.screen
        self.settings = tf_game.settings
        self.screen_rect = tf_game.screen.get_rect()
        self.stats = tf_game.game_stats


        # settings of font for scores
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 88)

        # Preparing initial pictures with scores
        self.prep_score()

    def prep_score(self):
        """transforming scores for generated pic"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color,
                                            self.settings.bg_colour)

        # Displaying score in right top corner of screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.centerx

    def show_score(self):
        """Displaying score at the screen"""
        self.screen.blit(self.score_image, self.score_rect)
