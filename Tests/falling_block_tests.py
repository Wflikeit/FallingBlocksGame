import pygame
import pytest

from falling_blocks import TowerFly


@pytest.fixture
def tower_fly():
    """Create an instance of the TowerFly game for testing"""
    pygame.init()
    game = TowerFly()
    yield game
    pygame.quit()


def test_create_bricks(tower_fly):
    """Test if the bricks are created properly"""
    assert len(tower_fly.floor_bricks) > 0
    assert len(tower_fly.left_wall_bricks) > 0
    assert len(tower_fly.right_wall_bricks) > 0


def test_generate_falling_block(tower_fly):
    """Test if a falling block is generated"""
    brick_counter_before = tower_fly.brick_counter
    tower_fly._generate_falling_block(tower_fly.brick_width)
    assert tower_fly.brick_counter == brick_counter_before + 1
    assert len(tower_fly.falling_bricks) > 0


def test_update_falling_blocks(tower_fly):
    """Test if falling blocks are updated properly"""
    tower_fly._update_falling_blocks(tower_fly.brick_width)
    assert tower_fly.level_counter == 0  # Level counter should start at 0
    assert tower_fly.brick_counter >= 0
    assert len(tower_fly.falling_bricks) >= 0


def test_increment_difficulty_level(tower_fly):
    """Test if the difficulty level is incremented"""
    falling_speed_before = tower_fly.brick.falling_speed
    player_speed_x_before = tower_fly.player.speed_x
    points_counter_before = tower_fly.settings.points_counter
    tower_fly._increment_difficulty_level()
    assert tower_fly.brick.falling_speed > falling_speed_before
    assert tower_fly.player.speed_x > player_speed_x_before
    assert tower_fly.settings.points_counter > points_counter_before


def test_new_game(tower_fly):
    """Test if the game is reset properly"""
    tower_fly.brick_counter = 5
    tower_fly.level_counter = 3
    tower_fly.brick.falling_speed = 2.0
    tower_fly.player.speed_x = 1.5
    tower_fly._new_game()
    assert tower_fly.game_stats.game_active is False
    assert tower_fly.brick_counter == 0
    assert tower_fly.level_counter == 0
    assert tower_fly.brick.falling_speed == tower_fly.settings.falling_brick_speed
    assert tower_fly.player.speed_x == tower_fly.settings.player_speed_x
