import pygame
from pygame import Surface
import math


class Player:
    """Class made for managing player"""

    def __init__(self, speed_x: int, speed_y: int, brick_height: int) -> None:
        """initialing of player and initial position"""
        # self.screen = tf_game.screen
        # self.settings = tf_game.settings
        # self.screen_rect = tf_game.screen.get_rect()

        self.speed_x = speed_x
        self.speed_y = speed_y

        # uploading image of jumping player
        self.image = pygame.image.load("images/Jump.png")
        self.image = pygame.transform.scale(self.image, (80, 70))
        self.rect = self.image.get_rect()

        # location of player is stored in float type
        self.x = 300
        self.y = 711
        self.rect.x = self.x
        self.rect.y = self.y

        # Options indicating that the player is moving
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.falling = False
        self.jumping_counter1 = 13
        self.standing = False
        self.is_colliding_left = False
        self.is_colliding_right = False
        self.is_colliding_down = False
        self.is_colliding_up = False
        self.brick_height = brick_height

    def update(self, screen: Surface) -> None:
        """Updating location of player"""
        if self.moving_right and not self.is_colliding_right:
            self.x += self.speed_x
        if self.moving_left and not self.is_colliding_left:
            self.x -= self.speed_x
        if self.jumping:
            self.jump(13, -13)

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme_up(self, screen: Surface) -> None:
        """Displaying player while jumping at current location"""
        screen.blit(self.image, self.rect)

    def jump(self, start: int = 13, end: int = -13) -> bool:
        """Calculating location of player with creating some physics"""
        if self.jumping_counter1 < end:
            self.jumping_counter1 = start
            self.jumping = False
            return True
        self.y -= self.jumping_counter1 ** 2 * 0.25 * math.copysign(1, self.jumping_counter1)
        self.jumping_counter1 -= 1
        return False
