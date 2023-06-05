import pygame.font
from pygame import Surface


class Scoreboard:
    """Class dedicated to display user's points"""

    def __init__(self):
        """Initializing score attributes"""

        # Settings of font for scores
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 88)

        # Preparing initial pictures with scores
        self.score_image = self.font.render("0", True, self.text_color)
        self.score_rect = self.score_image.get_rect()

    def prep_score(self, bg_color: tuple[int, int, int], screen: Surface, score: int) -> None:
        """Transform the score into a rendered image"""
        rounded_score = round(score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, bg_color)

        # Position the score image at the center top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = screen.get_rect().centerx
        self.score_rect.top = 20
    def show_score(self, bg_color: tuple[int, int, int], screen: Surface, score: int) -> None:
        """Display the score on the screen"""
        self.prep_score(bg_color, screen, score)

        screen.blit(self.score_image, self.score_rect)
