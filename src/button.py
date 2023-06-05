import pygame.font
from pygame import Surface


class Button:
    def __init__(self, screen: Surface, msg: str) -> None:
        """Initializing attributes of button"""
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.screen = screen

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.center = self.screen.get_rect().center

        # message displayed after pressing the button
        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """ Putting a message in generated picture and centering text on the button """
        # transforming str to picture
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        """ Drawing a button rect"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)  # displaying on screen
