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
        self.bricks1 = pygame.sprite.Group()
        self.bricks2 = pygame.sprite.Group()
        self.falling_bricks = pygame.sprite.Group()
        self.falling_brick = Falling_Brick()
        self._create_bricks()
        self.player = Player(self.settings.player_speed_x, self.settings.player_speed_y, self.brick.rect.y)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.game_stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.play_button = Button(self, "Play")

        pygame.display.set_caption("Tower Fly")

    def run_game(self) -> None:
        """ Main loop for pygame"""
        while True:
            self.check_event()
            if self.game_stats.game_active:
                self._check_player_if_player_is_colliding()
                self.player.update(self.screen)
                self.settings.iterator += self.settings.speed_play
                self.display_bg()
                self.falling_bricks.draw(self.screen)
                self._update_falling_blocks(self.brick_width)  # Pass brick_width as an argument

            self._update_screen()

            # Displaying lastly modified screen.
            pygame.display.flip()
            self.settings.CLOCK.tick(60)

    def display_bg(self) -> None:
        """Displaying moving background"""
        # print(f"{self.player.x}           {self.player.y}")
        self.screen.blit(self.bg.image, (0, self.settings.iterator))
        self.screen.blit(self.bg.image, (0, self.settings.iterator - self.settings.screen_height))

        if self.settings.iterator == self.settings.screen_height + 0.5:
            self.screen.blit(self.bg.image, (0, 0))
            self.settings.iterator = 0

    def check_event(self) -> None:
        """Checking events of game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game_stats.game_active = True
                self._update_falling_blocks(self.brick_width)

    def check_keydown_event(self, event: Event) -> None:
        """Reaction for pressing of keys"""
        if event.key == pygame.K_LEFT and not self.player.is_colliding_left:
            self.player.moving_left = True
        elif event.key == pygame.K_RIGHT and not self.player.is_colliding_right:
            self.player.moving_right = True
        elif event.key == pygame.K_SPACE and self.player.standing:
            self.player.jumping = True
            print("skokkkkkkkkkkkkkk")
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_event(self, event: Event) -> None:
        """Reaction for freeing of keys"""
        if event.key == pygame.K_LEFT:
            self.player.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.player.moving_right = False

    def _update_screen(self) -> None:
        """refreshing screen during each iteration"""
        self.player.blitme_up(self.screen)
        self.bricks1.draw(self.screen)
        self.bricks2.draw(self.screen)
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
                               self.bricks2)

        # Creating the left wall bricks
        for brick_number in range(0, number_of_bricks_y):
            self._create_brick(0, self.settings.screen_height - self.brick_width * brick_number, self.bricks1)

        # Creating the right wall bricks
        for brick_number in range(0, number_of_bricks_y):
            self._create_brick(self.settings.screen_width - self.brick_width,
                               self.settings.screen_height - self.brick_width * brick_number, self.bricks1)
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
        if self.player.rect.left < 50:
            self.player.is_colliding_left = True
            self.player.moving_left = False
        elif self.player.moving_right and self.player.is_colliding_left:
            self.player.is_colliding_left = False

        if self.player.rect.right > 500:
            self.player.is_colliding_right = True
            self.player.moving_right = False
        elif self.player.moving_left and self.player.is_colliding_right:
            self.player.is_colliding_right = False
        self.player.standing = pygame.sprite.spritecollideany(self.player, self.bricks2)

        # print(
        #     f"{self.}")

    def _generate_falling_block(self, block_x: int) -> None:
        """Generating falling block"""
        x_cord_for_falling_block = self._choose_coordinates_of_falling_blocks(block_x)
        falling_block = Falling_Brick()  # Create an instance of Falling_Brick
        falling_block.rect.x = x_cord_for_falling_block
        falling_block.rect.y = 0
        self.falling_bricks.add(falling_block)
        self.brick_counter += 1

    def _choose_coordinates_of_falling_blocks(self, block_x: int) -> int:
        """Getting random starting coordinates for falling blocks"""
        n = random.randint(1, 7)
        x_cord_for_falling_block = n * block_x
        return x_cord_for_falling_block

    def _update_falling_blocks(self, brick_width: int) -> None:
        """Update positions of falling blocks"""
        for block in self.falling_bricks:
            block.rect.y += self.brick.falling_speed
            # Check for collision with the floor
            if pygame.sprite.spritecollideany(block, self.bricks2):
                # Handle collision with the floor (e.g., remove the block)
                self.falling_bricks.remove(block)
                self._generate_falling_block(brick_width)
                self.brick_counter -= 1
                self.level_counter += 1
                self.game_stats.score += self.settings.points_counter
            if block.rect.y >= int(self.floor_y / 2) & self.brick_counter < 4:
                self._generate_falling_block(brick_width)
                self._generate_falling_block(brick_width)
                self._generate_falling_block(brick_width)
                self._generate_falling_block(brick_width)
            # Check for collision with the player
            if pygame.sprite.spritecollide(self.player, self.falling_bricks, False):
                # Handle collision with the player (e.g., game over)
                print("Collision with player!")
                pygame.sprite.Group.empty(self.falling_bricks)
                self.game_stats.game_active = False

        if self.level_counter == 10:
            self.brick.falling_speed += 1
            self.settings.player_speed_x += 1
            self.settings.points_counter *= 2
            self.level_counter = 0
