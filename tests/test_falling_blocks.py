import pygame
import pygame.event as pygame_event
import pytest
from pygame.event import Event
from pygame.rect import Rect

from src.brick import Brick
from src.falling_blocks import FallingBlocks
from src.player import Player
from src.settings import Settings


@pytest.fixture
def falling_blocks():
    return FallingBlocks()


def test_falling_blocks_init(falling_blocks):
    assert isinstance(falling_blocks.settings, Settings)
    assert isinstance(falling_blocks.player, Player)
    assert isinstance(falling_blocks.brick, Brick)
    assert isinstance(falling_blocks.left_wall_bricks, pygame.sprite.Group)
    assert isinstance(falling_blocks.floor_bricks, pygame.sprite.Group)
    assert isinstance(falling_blocks.right_wall_bricks, pygame.sprite.Group)
    assert isinstance(falling_blocks.falling_bricks, pygame.sprite.Group)


def test_falling_blocks_check_keydown_event(falling_blocks):
    falling_blocks.game_stats.game_active = True
    falling_blocks.player.is_colliding_left = False
    event_left = pygame_event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    falling_blocks._check_keydown_event(event_left)
    assert falling_blocks.player.moving_left
    assert falling_blocks.player.orientation == "Left"

    falling_blocks.player.is_colliding_right = False
    event_right = pygame_event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
    falling_blocks._check_keydown_event(event_right)
    assert falling_blocks.player.moving_right
    assert falling_blocks.player.orientation == "Right"

    event_space = pygame_event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
    falling_blocks.player.standing = True
    falling_blocks._check_keydown_event(event_space)
    assert falling_blocks.player.jumping

    event_q = pygame_event.Event(pygame.KEYDOWN, {'key': pygame.K_q})
    with pytest.raises(SystemExit):
        falling_blocks._check_keydown_event(event_q)


def test_falling_blocks_check_keyup_event(falling_blocks):
    event_left = Event(pygame.KEYUP, {'key': pygame.K_LEFT})
    falling_blocks.player.moving_left = True
    falling_blocks._check_keyup_event(event_left)
    assert not falling_blocks.player.moving_left

    event_right = Event(pygame.KEYUP, {'key': pygame.K_RIGHT})
    falling_blocks.player.moving_right = True
    falling_blocks._check_keyup_event(event_right)
    assert not falling_blocks.player.moving_right


def test_falling_blocks_check_play_button(falling_blocks):
    falling_blocks.game_stats.game_active = False
    mouse_pos = (100, 100)
    falling_blocks.play_button.rect = Rect(90, 90, 20, 20)
    falling_blocks._check_play_button(mouse_pos)
    assert falling_blocks.game_stats.game_active

    falling_blocks.game_stats.game_active = True
    falling_blocks._check_play_button(mouse_pos)
    assert falling_blocks.game_stats.game_active


def test_falling_blocks_create_bricks(falling_blocks):
    falling_blocks._create_bricks()
    assert len(falling_blocks.left_wall_bricks) > 0
    assert len(falling_blocks.floor_bricks) > 0
    assert len(falling_blocks.right_wall_bricks) > 0


def test_falling_blocks_check_player_if_player_is_colliding(falling_blocks):
    falling_blocks = FallingBlocks()

    # Mock the left wall bricks
    left_wall_brick = pygame.sprite.Sprite()
    left_wall_brick.rect = pygame.Rect(0, 0, 10, 10)
    falling_blocks.left_wall_bricks.add(left_wall_brick)

    # Mock the right wall bricks
    right_wall_brick = pygame.sprite.Sprite()
    right_wall_brick.rect = pygame.Rect(20, 0, 10, 10)
    falling_blocks.right_wall_bricks.add(right_wall_brick)

    # Mock the floor bricks
    floor_brick = pygame.sprite.Sprite()
    floor_brick.rect = pygame.Rect(0, 15, 10, 10)
    falling_blocks.floor_bricks.add(floor_brick)

    # Set player position
    falling_blocks.player.rect = pygame.Rect(5, 5, 10, 11)

    # Call the method to test
    falling_blocks._check_player_if_player_is_colliding()

    # Assertions
    assert not falling_blocks.player.moving_left
    assert not falling_blocks.player.moving_right
    assert falling_blocks.player.standing

    # Clean up
    falling_blocks.left_wall_bricks.empty()
    falling_blocks.right_wall_bricks.empty()
    falling_blocks.floor_bricks.empty()


def test_update_falling_bricks():
    falling_blocks = FallingBlocks()
    falling_brick = falling_blocks.falling_brick
    falling_brick.rect = pygame.Rect(0, 0, 10, 10)
    falling_blocks.falling_brick.falling_speed = 1
    falling_blocks.falling_bricks.add(falling_brick)

    falling_blocks._update_falling_bricks(10)

    assert falling_brick.rect.y == 1  # Falling brick should move down by 1 pixel
