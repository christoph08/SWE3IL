import pytest

from testing_course.bowling.game import Game


@pytest.fixture
def sut() -> Game:
    return Game()

def roll_many(game: Game, n: int, pins: int) -> None:
    for _ in range(n):
        game.roll(pins)

def test_gutter_game(sut: Game):
    roll_many(sut, 20, 0)
    assert sut.score() == 0

def test_all_ones(sut: Game):
    roll_many(sut, 20, 1)
    assert sut.score() == 20

def test_one_spare(sut: Game):
    sut.roll(5, 5, 3)
    roll_many(sut, 17, 0)
    assert sut.score() == 16

def test_one_strike(sut: Game):
    sut.roll(10, 5, 3)
    roll_many(sut, 16, 0)
    assert sut.score() == 26

def test_perfect_game(sut: Game):
    roll_many(sut, 12, 10)
    assert sut.score() == 300

def test_acceptance_test(sut: Game):
    sut.roll(1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6)

    assert sut.score() == 133