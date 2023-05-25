import pygame
from pygame import Surface
import math


class Player:
    """Class made for managing player"""

    def __init__(self, speed_x: int, speed_y: int, brick_height: int) -> None:
        """initializing player and initial position"""
        self.speed_x = speed_x
        self.speed_y = speed_y

        # uploading image of jumping player
        self.image = pygame.image.load("images/Jump.png")
        self.image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.image.get_rect()

        # location of player is stored as floats
        self.x = 300.0
        self.y = 711.0
        self.rect.x = self.x
        self.rect.y = self.y

        # Flags indicating player's movement and collision status
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.falling = False
        self.jumping_counter1 = 13
        self.standing = False
        self.is_colliding_left = False
        self.is_colliding_right = False
        self.is_colliding_down = False
        self.brick_height = brick_height

    def update(self, screen: Surface) -> None:
        """Update player's location"""
        if self.moving_right and not self.is_colliding_right:
            self.x += self.speed_x
        if self.moving_left and not self.is_colliding_left:
            self.x -= self.speed_x
        if self.jumping:
            self.jump(13, -13)

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def blitme_up(self, screen: Surface) -> None:
        """Display jumping player at the current location"""
        screen.blit(self.image, self.rect)

    def jump(self, start: int = 13, end: int = -13) -> bool:
        """Calculate player's location with some physics"""
        if self.jumping_counter1 < end:
            self.jumping_counter1 = start
            self.jumping = False
            return True
        self.y -= self.jumping_counter1 ** 2 * 0.25 * math.copysign(1, self.jumping_counter1)
        self.jumping_counter1 -= 1
        return False
