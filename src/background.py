import pygame


class Background:

    def __init__(self, fb_game) -> None:
        """initializing background"""
        self.screen = fb_game.screen
        self.settings = fb_game.settings
        self.screen_rect = fb_game.screen.get_rect()

        # uploading image of background
        self.image = pygame.image.load("../images/back.png")
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.image.get_rect()
