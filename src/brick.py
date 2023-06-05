import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self) -> None:
        """initializing brick"""
        self.brick_size = (60, 60)
        super().__init__()
        # uploading the image of brick
        brick_image_path = "../img/brick.png"
        self.image = pygame.image.load(brick_image_path)
        self.image = pygame.transform.scale(self.image, self.brick_size)
        self.rect = self.image.get_rect()


class FallingBrick(Brick):
    def __init__(self) -> None:
        """initializing falling brick"""

        super().__init__()
        # uploading the image of falling block
        falling_block_image = "../img/falling_block.png"
        self.image = pygame.image.load(falling_block_image)
        self.image = pygame.transform.scale(self.image, self.brick_size)
        self.rect = self.image.get_rect()

        # initial_falling_speed = 4
        self.falling_speed = 4
        self.brick_width = self.rect.x
