import pygame
from pygame.sprite import Sprite


class Brick(pygame.sprite.Sprite):

    def __init__(self) -> None:
        """initializing background"""
        super().__init__()
        # uploading the image of brick
        self.image = pygame.image.load("images/brick.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.y = 780
        self.rect.y = self.y
        self.falling_speed = 4  # Add the falling_speed attribute and set an appropriate value
        self.brick_width = self.rect.x

class Falling_Brick(Brick):
    def __init__(self):
        super().__init__()  # Call the parent class's __init__ method
        # uploading the image of brick
        self.image = pygame.image.load("images/slime-block.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        self.y = 780
        self.rect.y = self.y
        self.falling_speed = 4  # Add the falling_speed attribute and set an appropriate value
        self.brick_width = self.rect.x

