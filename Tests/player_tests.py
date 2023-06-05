import math

import pygame
import pytest

from player import Player


@pytest.fixture
def player():
    """Create an instance of the Player class for testing"""
    pygame.init()
    player = Player(speed_x=5, speed_y=10)
    yield player
    pygame.quit()


def test_player_initialization(player):
    """Test if the player is initialized correctly"""
    assert player.speed_x == 5
    assert player.speed_y == 10
    assert len(player.player_images) == 4
    assert player.image_index == 0
    assert player.image == player.player_images[0]
    assert player.orientation == "Left"
    assert player.rect.x == 300
    assert player.rect.y == 711
    assert not player.moving_right
    assert not player.moving_left
    assert not player.jumping
    assert player.jumping_counter == 13
    assert not player.standing
    assert not player.is_colliding_left
    assert not player.is_colliding_right


#
# def test_player_update(player):
#     """Test if the player's location is updated correctly"""
#     player.moving_right = True
#     player.update(screen=Surface((800, 600)))
#     assert player.x == 305  # Initial position + speed_x
#     assert player.rect.x == 305  # Rounded x position
#
#     player.moving_left = True
#     player.update(screen=Surface((800, 600)))
#     assert player.x == 300  # Previous position - speed_x
#     assert player.rect.x == 300  # Rounded x position
#
#     player.jumping = True
#     player.update(screen=Surface((800, 600)))
#     assert player.y < 711  # Player's y position should be lower due to jumping
#     assert player.rect.y < 711  # Rounded y position should also be lower

def test_player_jump(player):
    """Test if the player's jump function works correctly"""
    player.jumping = True
    player._jump()
    assert player.y < 711.0  # Player's y position should be lower due to jumping
    assert math.isclose(player.jumping_counter, 12.0, rel_tol=1e-9)  # Counter should decrease by 1.0


def test_player_animate(player):
    """Test if the player's animate function changes the image correctly"""
    player.animate(1)  # Change to image at index 1 (image_walking_right)
    assert player.image == player.player_images[1]  # Player's image should be updated

    player.animate(0)  # Change to image at index 0 (image_walking_left)
    assert player.image == player.player_images[0]  # Player's image should be updated
