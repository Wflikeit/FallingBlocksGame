import pygame
from pygame.sprite import Sprite


class Brick(Sprite):

    def __init__(self) -> None:
        """initializing background"""
        super().__init__()
        # uploading the image of brick
        self.image = pygame.image.load("images/brick.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.y = 780
        self.rect.y = self.y
        # self.rect.width = self.rect.width
        # self.rect.height = 13 * self.rect.height
        #
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height
