import pygame.font


class Button:
    def __init__(self, tf_game, msg):
        """Initializing attributes of button"""
        self.screen = tf_game.screen
        self.screen_rect = self.screen.get_rect()

        # defining dimensions and properties of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # creating a button and centring it
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.center = self.screen_rect.center

        # message displayed after pressing the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Putting a message in generated picture and centering text on the button
        """
        # transforming str to picture
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Displaying blank button, subsequently displaying a message on it
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)  # displaying on screen
