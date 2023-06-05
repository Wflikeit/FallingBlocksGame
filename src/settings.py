import pygame


class Settings:
    def __init__(self) -> None:
        """initialing settings of the game"""
        self.bg_colour = (36, 51, 55)
        self.CLOCK = pygame.time.Clock()
        self.screen_width = 540
        self.screen_height = 840
        self.moving_x = self.moving_y = 5
        self.iterator = 0
        self.speed_play = 0.5
        self.points_increment = 1
        self.initial_points_counter = 1

        # physics
        self.g_force = 0.00001
        self.player_speed_x = 3.2
        self.player_jump_limit = 1
        self.player_speed_y = self.player_jump_limit
        self.player_jump_speed = 2
        self.falling_brick_speed = 4

