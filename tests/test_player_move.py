import pytest
from app.src.board import Board
from app.src.player import Player


def test_player_move():
    board = Board()
    atlanta = board.get_city("Atlanta")
    chicago = board.get_city("Chicago")
    player = Player("Alice", atlanta)
    board.players.append(player)
    # Move só deve funcionar se as cidades estiverem conectadas
    if chicago in atlanta.connections:
        player.move(chicago)
        assert player.location == chicago
        assert player.actions_left == 3
    else:
        player.move(chicago)
        assert player.location == atlanta  # Não deve mover
        assert player.actions_left == 4


def test_reset_actions():
    board = Board()
    atlanta = board.get_city("Atlanta")
    player = Player("Bob", atlanta)
    player.actions_left = 1
    player.reset_actions()
    assert player.actions_left == 4


def test_add_and_remove_card():
    board = Board()
    atlanta = board.get_city("Atlanta")
    player = Player("Carol", atlanta)
    player.add_card("Chicago")
    assert "Chicago" in player.hand
    player.remove_card("Chicago")
    assert "Chicago" not in player.hand