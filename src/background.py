import pygame


class Background:

    def __init__(self, screen_width, screen_height) -> None:
        """initializing background"""

        # uploading image of background
        self.image = pygame.image.load("../images/back.png")
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
