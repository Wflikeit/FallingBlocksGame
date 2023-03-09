import pygame


class Background:

    def __init__(self, tf_game) -> None:
        """initializing background"""
        self.screen = tf_game.screen
        self.settings = tf_game.settings
        self.screen_rect = tf_game.screen.get_rect()

        # uploading image of background
        self.image = pygame.image.load("images/back_v1.png")
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width, self.settings.screen_height))
        self.rect = self.image.get_rect()
