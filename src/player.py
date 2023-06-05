import math

import pygame
from pygame import Surface


class Player:
    """Class made for managing player"""

    def __init__(self, speed_x: int, speed_y: int) -> None:
        """initializing player and initial position"""
        self.speed_x = speed_x
        self.speed_y = speed_y
        player_image_size = (45, 70)

        # uploading paths of jumping player
        image_walking_left_path = "img/run_left.png"
        image_walking_right_path = "img/run_right.png"
        image_jumping_left_path = "img/jump_left.png"
        image_jumping_right_path = "img/jump_right.png"

        # uploading image of jumping player
        self.image_walking_left = pygame.image.load(image_walking_left_path)
        self.image_walking_right = pygame.image.load(image_walking_right_path)
        self.image_jumping_left = pygame.image.load(image_jumping_left_path)
        self.image_jumping_right = pygame.image.load(image_jumping_right_path)

        # Resize images to the desired dimensions
        self.image_walking_left = pygame.transform.scale(self.image_walking_left, player_image_size)
        self.image_walking_right = pygame.transform.scale(self.image_walking_right, player_image_size)
        self.image_jumping_left = pygame.transform.scale(self.image_jumping_left, player_image_size)
        self.image_jumping_right = pygame.transform.scale(self.image_jumping_right, player_image_size)

        self.player_images = [
            self.image_walking_left,
            self.image_walking_right,
            self.image_jumping_left,
            self.image_jumping_right
        ]
        self.image_index = 0
        self.image = self.player_images[self.image_index]
        self.orientation = "Left"

        # Other player attributes
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
        self.jumping_counter = 13
        self.standing = False
        self.is_colliding_left = False
        self.is_colliding_right = False

    def update(self) -> None:
        """Update player's location"""
        if self.moving_right:
            self.x += self.speed_x
        if self.moving_left:
            self.x -= self.speed_x
        if self.jumping:
            self._jump(13, -13)

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def blit_me_up(self, screen: Surface) -> None:
        """Display jumping player at the current location"""
        screen.blit(self.image, self.rect)

    def _jump(self, start: float = 13.0, end: float = -13.0) -> bool:
        """Calculate player's location with some physics"""
        if self.jumping_counter < end:
            self.jumping_counter = start

            self._check_for_direction()
            self.jumping = False
            return True

        self.y -= self.jumping_counter ** 2 * 0.25 * math.copysign(1, self.jumping_counter)
        self.jumping_counter -= 1.0
        return False

    def _check_for_direction(self):
        """Checks direction of player"""
        if self.orientation == "Right":
            self.animate(1)
        if self.orientation == "Left":
            self.animate(0)

    def animate(self, image_index: int) -> None:
        """Animate the player by changing the current image"""
        self.image = self.player_images[image_index]
