import random

import pygame
import sys
from pygame.event import Event

from player import Player
from settings import Settings
from background import Background
from brick import Brick
from brick import Falling_Brick
from Scoreboard import Scoreboard
from game_stats import GameStats
from button import Button


def _choose_coordinates_of_falling_blocks(block_x: int) -> int:
    """Getting random starting coordinates for falling blocks"""
    n = random.randint(1, 7)
    x_cord_for_falling_block = n * block_x
    return x_cord_for_falling_block


class TowerFly:
    def __init__(self) -> None:
        """initialing of game"""
        pygame.init()
        self.brick_counter = 0
        self.level_counter = 0
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg = Background(self)
        self.screen_rect = self.screen.get_rect()
        self.left_wall_bricks = pygame.sprite.Group()
        self.floor_bricks = pygame.sprite.Group()
        self.right_wall_bricks = pygame.sprite.Group()
        self.falling_bricks = pygame.sprite.Group()
        self.falling_brick = Falling_Brick()
        self._create_bricks()
        self.player = Player(self.settings.player_speed_x, self.settings.player_speed_y)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.game_stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.play_button = Button(self, "Play")

        # self.extra_point = extra_point()

        pygame.display.set_caption("Tower Fly")

    def run_game(self) -> None:
        """ Main loop for pygame"""
        while True:
            self._check_event()

            if self.game_stats.game_active:
                self._check_player_if_player_is_colliding()
                self.player.update(self.screen)
                self.settings.iterator += self.settings.speed_play
                self._display_bg()
                self.falling_bricks.draw(self.screen)
                self._update_falling_blocks(self.brick_width)  # Pass brick_width as an argument

            self._update_screen()

            # Displaying lastly modified screen.
            pygame.display.flip()
            self.settings.CLOCK.tick(90)

    def _display_bg(self) -> None:
        """Displaying moving background"""
        # print(f"{self.player.x}           {self.player.y}")
        self.screen.blit(self.bg.image, (0, self.settings.iterator))
        self.screen.blit(self.bg.image, (0, self.settings.iterator - self.settings.screen_height))

        if self.settings.iterator == self.settings.screen_height + 0.5:
            self.screen.blit(self.bg.image, (0, 0))
            self.settings.iterator = 0

    def _check_event(self) -> None:
        """Checking events of game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        """Starting a new game, after pressing mouse button"""
        button_pressed = self.play_button.rect.collidepoint(mouse_pos)
        if button_pressed and not self.game_stats.game_active:
            # Resetting stats data
            self.game_stats.reset_stats()
            self.game_stats.game_active = True
            self.scoreboard.prep_score()

            # hiding a mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_event(self, event: Event) -> None:
        """Reaction for pressing of keys"""
        if event.key == pygame.K_LEFT and not self.player.is_colliding_left:
            self.player.moving_left = True
        elif event.key == pygame.K_RIGHT and not self.player.is_colliding_right:
            self.player.moving_right = True
        elif event.key == pygame.K_SPACE and self.player.standing:
            self.player.jumping = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_event(self, event: Event) -> None:
        """Reaction for freeing of keys"""
        if event.key == pygame.K_LEFT:
            self.player.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.player.moving_right = False

    def _update_screen(self) -> None:
        """refreshing screen during each iteration"""
        self.player.blitme_up(self.screen)
        self.left_wall_bricks.draw(self.screen)
        self.floor_bricks.draw(self.screen)
        self.right_wall_bricks.draw(self.screen)
        self.scoreboard.show_score()

        if not self.game_stats.game_active:
            self.play_button.draw_button()

    def _create_bricks(self) -> None:
        """Creating a static block of bricks"""
        self.brick = Brick()
        self.brick_width, brick_height = self.brick.rect.size
        self.brick_height = self.settings.screen_height - brick_height
        available_space_x = self.settings.screen_width
        available_space_y = self.settings.screen_height
        number_of_bricks_x = available_space_x // self.brick_width
        number_of_bricks_y = available_space_y // self.brick_width + 1
        self.floor_y = self.settings.screen_height - brick_height
        # Creating the floor bricks
        for brick_number in range(0, number_of_bricks_x):
            self._create_brick(brick_number * self.brick_width - 60, self.settings.screen_height - brick_height,
                               self.floor_bricks)

        # Creating the left wall bricks
        for brick_number in range(0, number_of_bricks_y):
            self._create_brick(0, self.settings.screen_height - self.brick_width * brick_number, self.left_wall_bricks)

        # Creating the right wall bricks
        for brick_number in range(0, number_of_bricks_y):
            self._create_brick(self.settings.screen_width - self.brick_width,
                               self.settings.screen_height - self.brick_width * brick_number, self.right_wall_bricks)
        self._generate_falling_block(self.brick_width)

    def _create_brick(self, x: int, y: int, brick_group: pygame.sprite.Group) -> None:
        """Creating a single brick at the given coordinates and adding it to the given brick group"""
        self.brick = Brick()
        self.brick.rect = self.brick.image.get_rect()
        self.brick.rect.x = x
        self.brick.rect.y = y
        brick_group.add(self.brick)

    def _check_player_if_player_is_colliding(self) -> None:
        """Checks if player is standing, or hitting the edge"""
        if pygame.sprite.spritecollideany(self.player, self.left_wall_bricks):
            self.player.moving_left = False
        if pygame.sprite.spritecollideany(self.player, self.right_wall_bricks):
            self.player.moving_right = False

        if pygame.sprite.spritecollideany(self.player, self.floor_bricks):
            self.player.standing = True

    def _generate_falling_block(self, block_x: int) -> None:
        """Generating falling block"""
        x_cord_for_falling_block = _choose_coordinates_of_falling_blocks(block_x)
        falling_block = Falling_Brick()  # Create an instance of Falling_Brick
        falling_block.rect.x = x_cord_for_falling_block
        falling_block.rect.y = 0
        self.falling_bricks.add(falling_block)
        self.brick_counter += 1

    def _update_falling_blocks(self, brick_width: int) -> None:
        """Update positions of falling blocks"""
        for block in self.falling_bricks:
            block.rect.y += self.brick.falling_speed
            # Check for collision with the floor
            if pygame.sprite.spritecollideany(block, self.floor_bricks):
                # Handle collision with the floor
                self.falling_bricks.remove(block)
                self._generate_falling_block(brick_width)
                self.brick_counter -= 1
                self.level_counter += 1
                self.game_stats.score += self.settings.points_counter
                print(self.level_counter)

            if block.rect.y >= int(self.floor_y / 2) & self.brick_counter < 4:
                for _ in range(4):
                    self._generate_falling_block(brick_width)
            # Check for collision with the player
            if pygame.sprite.spritecollideany(self.player, self.falling_bricks):
                # Handle collision with the player (e.g., game over)
                print("Collision with player!")
                self._new_game()

        if self.level_counter == 5:
            self._increment_difficulty_level()
            self.level_counter = 0

    def _increment_difficulty_level(self) -> None:
        """Increasing the level of difficulty"""
        self.brick.falling_speed += 0.4
        self.player.speed_x += 0.2
        self.settings.points_counter *= 2

    def _new_game(self) -> None:
        """Resetting stats"""
        pygame.sprite.Group.empty(self.falling_bricks)
        self.game_stats.game_active = False
        self.brick_counter = 0
        self.level_counter = 0
        self.brick.falling_speed= self.settings.falling_brick_speed
        self.player.speed_x = self.settings.player_speed_x
        pygame.mouse.set_visible(True)
