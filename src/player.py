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
        self.double_jumping = False
        self.jumping_counter1 = 13
        self.jumping_iterator = 0
        self.standing = False
        self.is_colliding_left = False
        self.is_colliding_right = False
        self.is_colliding_down = False
        self.is_colliding_up = False
        self.brick_height = brick_height
        self.double_jump_counter = 0
        self.first_jump_end = None

    def update(self, screen: Surface) -> None:
        """Updating location of player"""
        if self.moving_right and not self.is_colliding_right:
            self.x += self.speed_x
        if self.moving_left and not self.is_colliding_left:
            self.x -= self.speed_x
        # if self.jumping and self.jumping_iterator <2:
        #     self.jump()
        if self.double_jumping:
            self.double_jump()
        elif self.jumping:
            self.jump(13, -13)

        # if not self.standing:
        #     if self.falling:
        #         self.fall()
        # if self.standing:
        #     self.jumping_counter1 = 13
        # self.falling = False

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme_up(self, screen: Surface) -> None:
        """Displaying player while jumping at current location"""
        screen.blit(self.image, self.rect)

    # def blitme_down(self):
    #     """Displaying player while falling at current location"""
    #     self.screen.blit(self.image_down, self.rect)

    # def jump(self, floor_y) -> None:
    #     """Calculating location of player with creating some physics"""
    #     if self.jumping_counter < 0:
    #         self.jumping = False
    #         self.falling = True
    #         self.jumping_counter = 13
    #         while self.falling:
    #             self.fall()
    #         return
    #
    #     # if self.y >= floor_y:
    #     #     self.y = floor_y
    #     #     self.jumping = False
    #     #     self.jumping_counter = 0
    #     #     return
    #
    #     self.y -= self.jumping_counter ** 2 * 0.3
    #     self.jumping_counter -= 1
    #
    # def fall(self):
    #     """Calculating location of player with creating some physics"""
    #     if self.standing:
    #         self.jumping_counter = 13
    #         self.falling = False
    #         return False
    #
    #     self.y -= -self.jumping_counter ** 2 * 0.3
    #     self.jumping_counter -= 1
    def jump(self, start: int = 13, end: int = -13) -> bool:
        """Calculating location of player with creating some physics"""
        if self.jumping_counter1 < end:
            self.jumping_counter1 = start
            # self.falling = True
            self.jumping = False
            return True
        self.y -= self.jumping_counter1 ** 2 * 0.25 * math.copysign(1, self.jumping_counter1)
        self.jumping_counter1 -= 1
        return False

    # def double_jump(self):
    #     if self.double_jump_counter == 2:
    #         self.double_jumping = False
    #         self.double_jump_counter = 0
    #         return
    #     if self.double_jump_counter == 0:
    #         self.first_jump_end = self.jumping_counter1
    #         if self.jump():
    #             self.double_jump_counter = 1
    #     else:
    #         if self.jump(- self.first_jump_end, - 13):
    #             self.double_jump_counter = 2
    def double_jump(self):
        if self.double_jump_counter == 2:
            self.double_jumping = False
            self.double_jump_counter = 0
            return
        if self.double_jump_counter == 0:
            self.first_jump_end = self.jumping_counter1
            if self.jump():
                self.double_jump_counter = 1
        else:
            if self.jump(- self.first_jump_end, - 13):
                self.double_jump_counter = 2

    #
    # def jump(self) -> None:
    #     """Calculating location of player with creating some physics"""
    #     if self.jumping_counter1 < 0:
    #         self.jumping_counter1 = 13
    #         self.falling = True
    #         self.jumping = False
    #         return
    #     self.y -= self.jumping_counter1 ** 2 * 0.25
    #     self.jumping_counter1 -= 1

    # def jump(self) -> None:
    #      """Calculating location of player with creating some physics"""
    #      if self.jumping_counter == 1:
    #          self.jumping_counter += 13
    #          self.falling = True
    #          self.jumping = False
    #          self.jumping_iterator +=1
    #      if self.jumping_counter == 1 and self.jumping_iterator == 1:
    #          self.jumping_iterator = 2
    #          self.falling = True
    #          self.jumping = False
    #      # if self.jumping and self.jumping_iterator < 2:
    #      #     self.jumping_iterator += 1
    #      #     print("Double jumppppppppp")
    #      #     self.falling = False
    #      if self.jumping_iterator == 2:
    #          self.falling = True
    #          self.jumping = False
    #          # if self.standing:
    #          #     self.jumping_iterator = 0
    #      if self.jumping_iterator == 1:
    #          self.jumping_counter = 13
    #          self.falling = True
    #          print("skok nr2")
    #      # if self.jumping_iterator == 1:
    #      #     self.falling = True
    #      #     self.jumping_counter = 13
    #      #     print("skok nr2")
    #      """Jesli odkomentujemy to przy kazdym spadku bedzie delikatnie progresywnie nizej"""
    #      self.y -= self.jumping_counter ** 2 * 0.25
    #      self.jumping_counter -= 1

    # def jump(self) -> None:
    #     """Calculating location of player with creating some physics"""
    #     if self.jumping_counter < 0:
    #         self.jumping = False
    #         self.jumping_counter = 13
    #         self.falling = True
    #         self.fall()
    #         return
    #
    #     self.y -= self.jumping_counter ** 2 * 0.3
    #     self.jumping_counter -= 1

    # def fall(self) -> None:
    #     # if self.standing:
    #     #     self.jumping_counter = 13
    #     #     self.falling = False
    #     #     return
    #     self.y += self.jumping_counter1 ** 2 * 0.25
    #     self.jumping_counter1 -= 1
