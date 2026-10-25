from testing_course.connect_four.player import Player


class ConnectFourGame:
    def __init__(self, player_on_turn: Player) -> None:
        self._winner = Player.NONE

    def get_player_at(self, row: int, col: int) -> Player:
        raise NotImplementedError

    @property
    def player_on_turn(self) -> Player:
        raise NotImplementedError    

    @property
    def is_game_over(self) -> bool:
        raise NotImplementedError

    @property
    def winner(self) -> Player:
        return self._winner

    def reset(self, player_on_turn: Player) -> None:
        raise NotImplementedError

    def drop(self, col: int) -> None:
        raise NotImplementedError
