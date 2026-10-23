class Game:
    def __init__(self) -> None:
        self._rolls: list[int] = [] 

    def roll(self, *pins: int) -> None:
        self._rolls.extend(pins)

    def score(self) -> int:
        score = 0
        roll_index = 0

        for _ in range(10):
            if self._rolls[roll_index] == 10:
                score += 10 + self._rolls[roll_index + 1] + self._rolls[roll_index + 2]
                roll_index += 1
            elif self._rolls[roll_index] + self._rolls[roll_index + 1] == 10:
                score += 10 + self._rolls[roll_index + 2]
                roll_index += 2
            else:
                score += self._rolls[roll_index] + self._rolls[roll_index + 1]
                roll_index += 2

        return score




    
