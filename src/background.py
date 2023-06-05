import pygame


class Background:

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """initializing background"""

        background_image_path = "../img/back.png"

        # uploading image of background
        self.image = pygame.image.load(background_image_path)
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()
