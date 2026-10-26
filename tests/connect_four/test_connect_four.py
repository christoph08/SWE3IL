import pytest

from testing_course.connect_four.connect_four import InvalidMoveError
from testing_course.connect_four.connect_four_game import ConnectFourGame
from testing_course.connect_four.player import Player


@pytest.fixture
def sut() -> ConnectFourGame:
    return ConnectFourGame(Player.RED)

def test_initial_player_is_set() -> None:
    sut = ConnectFourGame(Player.YELLOW)
    assert sut.player_on_turn == Player.YELLOW

def test_initial_winner_is_none(sut: ConnectFourGame) -> None:
    assert sut.winner == Player.NONE

def test_initial_game_is_not_over(sut: ConnectFourGame) -> None:
    assert sut.is_game_over is False

def test_initial_board_is_empty(sut: ConnectFourGame) -> None:
    for row in range(6):
        for col in range(7):
            assert sut.get_player_at(row, col) == Player.NONE

@pytest.mark.parametrize("drop_col", range(7))
def test_drop_places_disc_at_bottom(sut: ConnectFourGame, drop_col: int) -> None:
    sut.drop(drop_col)
    assert sut.get_player_at(5, drop_col) == Player.RED

def test_player_switch_after_drop(sut: ConnectFourGame) -> None:
    sut.drop(0)
    assert sut.player_on_turn == Player.YELLOW

    sut.drop(1)
    assert sut.player_on_turn == Player.RED

@pytest.mark.parametrize("drop_col", range(7))
def test_drop_stacks_discs(sut: ConnectFourGame, drop_col: int) -> None:
    for _ in range(3):
        sut.drop(drop_col)
        
    assert sut.get_player_at(5, drop_col) == Player.RED
    assert sut.get_player_at(4, drop_col) == Player.YELLOW
    assert sut.get_player_at(3, drop_col) == Player.RED

@pytest.mark.parametrize(
    ("moves", "expected_winner"),
    [
        pytest.param(
            [0, 0, 1, 1, 2, 2, 3],
            Player.RED,
            id="horizontal-red",
        ),
        pytest.param(
            [5, 0, 0, 1, 1, 2, 2, 3],
            Player.YELLOW,
            id="horizontal-yellow",
        ),
        pytest.param(
            [0, 1, 0, 1, 0, 1, 0],
            Player.RED,
            id="vertical-red",
        ),
        pytest.param(
            [1, 0, 1, 0, 1, 0, 2, 0],
            Player.YELLOW,
            id="vertical-yellow",
        ),
        pytest.param(
            [0, 1, 1, 2, 3, 2, 2, 3, 4, 3, 3],
            Player.RED,
            id="diagonal-up-right-red",
        ),
        pytest.param(
            [3, 2, 2, 1, 0, 1, 1, 0, 4, 0, 0],
            Player.RED,
            id="diagonal-down-right-red",
        ),
    ],
)
def test_win(sut: ConnectFourGame,moves: list[int], expected_winner: Player) -> None:
    for col in moves:
        sut.drop(col)

    assert sut.is_game_over is True
    assert sut.winner == expected_winner

def test_game_over_when_board_is_full_without_winner(sut: ConnectFourGame) -> None:
    moves = [
        3, 4, 4, 2, 0, 1, 3,
        6, 2, 1, 5, 0, 1, 2,
        2, 4, 6, 5, 6, 6, 4,
        6, 2, 6, 5, 4, 4, 3,
        3, 5, 0, 3, 2, 1, 3,
        0, 1, 1, 5, 5, 0, 0,
    ]

    for col in moves:
        sut.drop(col)

    assert sut.is_game_over is True
    assert sut.winner == Player.NONE

@pytest.mark.parametrize("drop_col", range(7))
def test_drop_rais_invalidemove_error_when_column_full(sut: ConnectFourGame, drop_col: int) -> None:  # noqa: E501
    for _ in range(6):
        sut.drop(drop_col)

    with pytest.raises(InvalidMoveError):
        sut.drop(drop_col)

@pytest.mark.parametrize(
    ("row", "col"),
    [
        (-1, 0),
        (6, 0),
        (0, -1),
        (0, 7),
    ],
)
def test_get_player_at_raises_index_error_for_invalid_position(sut: ConnectFourGame, row: int, col: int) -> None:
    with pytest.raises(IndexError):
        sut.get_player_at(row, col)

def prepare_vertical_win(sut: ConnectFourGame) -> None:
    for _ in range(3):
        sut.drop(0)  # RED
        sut.drop(1)  # YELLOW

    sut.drop(0)  # RED wins

def test_drop_after_game_over_raises_error(sut: ConnectFourGame) -> None:
    prepare_vertical_win(sut)

    assert sut.is_game_over is True
    with pytest.raises(InvalidMoveError):
            sut.drop(0)

@pytest.mark.parametrize(
    "drop_col",
    [*range(-10, 0), *range(7, 17)],
)
def test_invalide_input_dose_not_change_player(sut: ConnectFourGame, drop_col: int) -> None:  # noqa: E501
  with pytest.raises(IndexError):
          sut.drop(drop_col)

  assert sut.player_on_turn == Player.RED

@pytest.mark.parametrize(
    "drop_col",
    [*range(-10, 0), *range(7, 17)],
)
def test_invalid_input_does_not_change_board(sut: ConnectFourGame, drop_col: int) -> None:  # noqa: E501
    with pytest.raises(IndexError):
        sut.drop(drop_col)

    for row in range(6):
        for col in range(7):
            assert sut.get_player_at(row, col) == Player.NONE

def test_reset_clears_board(sut: ConnectFourGame) -> None:
    prepare_vertical_win(sut)

    sut.reset(Player.RED)

    for row in range(6):
        for col in range(7):
            assert sut.get_player_at(row, col) == Player.NONE

def test_reset_sets_player_on_turn(sut: ConnectFourGame) -> None:
    prepare_vertical_win(sut)

    sut.reset(Player.YELLOW)

    assert sut.player_on_turn == Player.YELLOW

def test_reset_clears_winner(sut: ConnectFourGame) -> None:
    prepare_vertical_win(sut)

    sut.reset(Player.RED)

    assert sut.winner == Player.NONE
    assert sut.is_game_over is False

def test_reset_after_game_over_allows_playing(sut: ConnectFourGame) -> None:
    prepare_vertical_win(sut)

    sut.reset(Player.YELLOW)
    sut.drop(0)

    assert sut.get_player_at(5, 0) == Player.YELLOW



    




