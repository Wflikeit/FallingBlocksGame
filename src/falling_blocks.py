import random
import sys

import pygame
from pygame.event import Event

from src.background import Background
from src.brick import Brick
from src.brick import FallingBrick
from src.button import Button
from src.game_stats import GameStats
from src.player import Player
from src.scoreboard import Scoreboard
from src.settings import Settings


class FallingBlocks:
    def __init__(self) -> None:
        """initialing of game"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Falling Blocks")
        self.game_stats = GameStats()
        self.scoreboard = Scoreboard()
        self.player = Player(self.settings.player_speed_x, self.settings.player_speed_y)
        self.bg = Background(self.settings.screen_width, self.settings.screen_height)
        self.play_button = Button(self.screen, "Play")

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.left_wall_bricks = pygame.sprite.Group()
        self.floor_bricks = pygame.sprite.Group()
        self.right_wall_bricks = pygame.sprite.Group()
        self.falling_bricks = pygame.sprite.Group()
        self.falling_brick = FallingBrick()

        self._create_bricks()

        self.brick_counter = 0
        self.level_counter = 0

    def run_game(self) -> None:
        """ Main loop for pygame"""
        while True:
            self._check_event()

            if self.game_stats.game_active:
                self._check_player_if_player_is_colliding()
                self.player.update()
                self.settings.iterator += self.settings.speed_play
                self._display_bg()
                self.falling_bricks.draw(self.screen)
                self._update_falling_bricks(self.brick_width)  # Pass brick_width as an argument
                self._check_level_completion()
                # self.scoreboard.prep_score(self.game_stats.score, self.screen_rect, self.settings.bg_colour)

            self._update_screen()
            # Displaying lastly modified screen.
            pygame.display.flip()
            self.settings.CLOCK.tick(70)

    def _display_bg(self) -> None:
        """Displaying moving background"""
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
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """Starting a new game, after pressing mouse button"""
        button_pressed = self.play_button.rect.collidepoint(mouse_pos)
        if button_pressed and not self.game_stats.game_active:
            # Resetting stats data
            self.game_stats.reset_stats()
            self.game_stats.game_active = True
            self._generate_falling_brick(self.brick_width)

            # hiding a mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_event(self, event: Event) -> None:
        """Reaction for pressing of keys"""
        if event.key == pygame.K_LEFT and not self.player.is_colliding_left and self.game_stats.game_active:
            self.player.orientation = "Left"
            self.player.animate(0)
            self.player.moving_left = True
        elif event.key == pygame.K_RIGHT and not self.player.is_colliding_right and self.game_stats.game_active:
            self.player.moving_right = True
            self.player.orientation = "Right"

            self.player.animate(1)
        elif event.key == pygame.K_SPACE and self.player.standing and self.game_stats.game_active:
            self.player.jumping = True
            if self.player.orientation == "Right":
                self.player.animate(3)
            if self.player.orientation == "Left":
                self.player.animate(2)

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
        self.player.blit_me_up(self.screen)
        self.left_wall_bricks.draw(self.screen)
        self.floor_bricks.draw(self.screen)
        self.right_wall_bricks.draw(self.screen)
        self.scoreboard.show_score(self.settings.bg_colour, self.screen, self.game_stats.score)

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

    def _create_brick(self, x: int, y: int, brick_group: pygame.sprite.Group) -> None:
        """Creating a single brick at the given coordinates and adding it to the given brick group"""
        brick = Brick()
        brick.rect.x = x
        brick.rect.y = y
        brick_group.add(brick)

    def _check_player_if_player_is_colliding(self) -> None:
        """Checks if player is standing, or hitting the edge"""
        if pygame.sprite.spritecollideany(self.player, self.left_wall_bricks):
            self.player.moving_left = False
        if pygame.sprite.spritecollideany(self.player, self.right_wall_bricks):
            self.player.moving_right = False

        if pygame.sprite.spritecollideany(self.player, self.floor_bricks):
            self.player.standing = True

    def _generate_falling_brick(self, brick_x: int) -> None:
        """Generating falling block"""
        x_cord_for_falling_brick = self._choose_coordinates_of_falling_bricks(brick_x)
        falling_brick = FallingBrick()  # Create an instance of Falling_Brick
        falling_brick.rect.x = x_cord_for_falling_brick
        falling_brick.rect.y = 0
        self.falling_bricks.add(falling_brick)
        self.brick_counter += 1

    def _update_falling_bricks(self, brick_width: int) -> None:
        """Update positions of falling blocks"""
        for block in self.falling_bricks:
            block.rect.y += self.falling_brick.falling_speed
            # Check for collision with the floor
            if pygame.sprite.spritecollideany(block, self.floor_bricks):
                self._handle_brick_floor_collision(block, brick_width)

            if block.rect.y >= 0 and self.brick_counter < 4:
                for _ in range(4):
                    self._generate_falling_brick(brick_width)
            # Check for collision with the player
            if pygame.sprite.spritecollideany(self.player, self.falling_bricks):
                self._handle_brick_player_collision()

    def _handle_brick_player_collision(self) -> None:
        """handles the collision of brick with player"""
        self._new_game()

    def _handle_brick_floor_collision(self, block: FallingBrick, brick_width: int) -> None:
        """handles the collision of block with floor blocks"""
        self.falling_bricks.remove(block)
        self._generate_falling_brick(brick_width)
        self.brick_counter -= 1
        self.level_counter += 1
        self.game_stats.score += self.settings.points_increment

    def _increment_difficulty_level(self) -> None:
        """Increasing the level of difficulty"""
        self.falling_brick.falling_speed += 0.2
        self.player.speed_x += 0.2
        self.settings.points_increment *= 1.2

    def _new_game(self) -> None:
        """Resetting stats"""
        pygame.sprite.Group.empty(self.falling_bricks)
        self.game_stats.game_active = False
        self.settings.points_increment = self.settings.initial_points_counter
        self.brick_counter = 0
        self.level_counter = 0
        self.falling_brick.falling_speed = self.settings.falling_brick_speed
        self.player.speed_x = self.settings.player_speed_x
        pygame.mouse.set_visible(True)

    @staticmethod
    def _choose_coordinates_of_falling_bricks(block_x: int) -> int:
        """Getting random starting coordinates for falling blocks"""
        n = random.randint(1, 7)
        x_cord_for_falling_brick = n * block_x
        return x_cord_for_falling_brick

    def _check_level_completion(self) -> None:
        """Checks if a level of difficulty should be increased"""
        if self.level_counter == 5:
            self._increment_difficulty_level()
            self.level_counter = 0
