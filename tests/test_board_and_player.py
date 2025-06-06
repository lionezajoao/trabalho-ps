import pytest
from app.src.board import Board
from app.src.player import Player

def test_create_players_and_board():
    board = Board()
    player_names = ["Alice", "Bob"]
    players = []
    for name in player_names:
        player = Player(name, board.get_city("Atlanta"))
        players.append(player)
        board.players.append(player)
    assert len(players) == 2
    assert all(player.location.name == "Atlanta" for player in players)
    assert board.players == players