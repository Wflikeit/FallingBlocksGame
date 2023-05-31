import pygame
class Scoreboard:
    """Class dedicated to display user's points"""

    def __init__(self, tf_game):
        """Initializing score attributes"""
        self.screen = tf_game.screen
        self.settings = tf_game.settings
        self.screen_rect = tf_game.screen.get_rect()
        self.stats = tf_game.game_stats

        # Settings of font for scores
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 88)

        # Preparing initial pictures with scores
        self.score_image = None
        self.score_rect = None

    def prep_score(self):
        """Transforming scores into a generated image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_colour)

        # Position the score image at the center top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.screen_rect.top

    def show_score(self):
        """Display the score on the screen"""
        self.prep_score()
        self.screen.blit(self.score_image, self.score_rect)
