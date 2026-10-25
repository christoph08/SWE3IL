from testing_course.connect_four.connect_four import InvalidMoveError
from testing_course.connect_four.player import Player
    # Spielfeld: 6 Zeilen (rows) x 7 Spalten (cols), Zugriff mit board[row][col]
    #
    #            col 0  col 1  col 2  col 3  col 4  col 5  col 6
    #           +------+------+------+------+------+------+------+
    #   row 0   |      |      |      |      |      |      |      |   <- oben
    #           +------+------+------+------+------+------+------+
    #   row 1   |      |      |      |      |      |      |      |
    #           +------+------+------+------+------+------+------+
    #   row 2   |      |      |      |      |      |      |      |
    #           +------+------+------+------+------+------+------+
    #   row 3   |      |      |      |      |      |      |      |
    #           +------+------+------+------+------+------+------+
    #   row 4   |      |      |      |      |      |      |      |
    #           +------+------+------+------+------+------+------+
    #   row 5   |      |      |      |      |      |      |      |   <- unten
    #           +------+------+------+------+------+------+------+
    #
    # drop(col): der Stein faellt nach unten -> von row 5 aufwaerts
    #            das erste freie Feld (Player.NONE) suchen.

class ConnectFourGame:
    ROWS = 6 # 6 Zeilen (bleiben immer gleich)
    COLS = 7 # 7 Spalten (bleiben immer gleich)


    def __init__(self, player_on_turn: Player) -> None:
        # Beim Erzeugen des Spiels wird reset aufgerufen.
        # So steht der Code für den Anfangszustand nur an einer Stelle (DRY).
        self.reset(player_on_turn)


    def get_player_at(self, row: int, col: int) -> Player: 
        # Gibt den Spieler zurück der auf der 
        # angegebenen Position sitzt.
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            raise IndexError(f"Position ({row}, {col}) liegt außerhalb des Spielfelds")
        return self._board[row][col]


    @property
    def player_on_turn(self) -> Player: # gibt den Spieler zurück, der am Zug ist
        return self._player_on_turn

    @property
    def is_game_over(self) -> bool: 
        # Ist das Spiel vorbei? 
        # zwei Möglichkeiten: Entweder es gibt einen Gewinner oder das Spielfeld ist voll.
        
        # 1 Möglichkeit self._winner ist nichtmehr None, dann gibt es einen Gewinner
        if self._winner != Player.NONE:
            return True
        else:
            # 2 Möglichkeit: Das Spielfeld ist voll
            for row in self._board:
                if Player.NONE in row:
                    return False
            return True

    @property
    def winner(self) -> Player:
        return self._winner

    def reset(self, player_on_turn: Player) -> None:
        # Setzt das Spiel auf den Anfangszustand zurück.
        # Wird beim Erzeugen (__init__) und bei einem Neustart ("r" in der main) aufgerufen.
        self._winner = Player.NONE # Hier wird der Gewinner auf NONE gesetzt.
        self._player_on_turn = player_on_turn # Hier wird der Spieler, der am Zug ist, gesetzt.

        self._board = [[Player.NONE] * self.COLS for _ in range(self.ROWS)]
        # Liste mit 6 Zeilen und 7 Spalten, die alle auf Player.NONE gesetzt sind.
        # Spielfeld fertig initialisiert. 
        
    def drop(self, col: int) -> None:
        # Lässt einen Stein des Spielers, der am Zug ist, in die Spalte col fallen.

        # 1. Prüfen, ob der Zug erlaubt ist.
        if self.is_game_over:
            raise InvalidMoveError("Das Spiel ist bereits vorbei")
        if not (0 <= col < self.COLS):
            raise IndexError(f"Spalte {col} liegt außerhalb des Spielfelds")
        if self._board[0][col] != Player.NONE: # oberstes Feld belegt -> Spalte voll
            raise InvalidMoveError(f"Spalte {col} ist voll")

        # 2. Von unten (row 5) nach oben das erste freie Feld suchen.
        row = self.ROWS - 1
        while self._board[row][col] != Player.NONE:
            row -= 1

        # 3. Hier wird der Stein gesetzt.
        self._board[row][col] = self._player_on_turn

        # 4. Gewonnen? Dann Gewinner setzen, sonst Spieler wechseln.
        if self._is_winning_move(row, col):
            self._winner = self._player_on_turn
        elif self._player_on_turn == Player.RED:
            self._player_on_turn = Player.YELLOW
        else:
            self._player_on_turn = Player.RED

    
    def _is_winning_move(self, row: int, col: int) -> bool:
        # Prüft, ob der Stein auf (row, col) vier (oder mehr) in einer Reihe ergibt.
        player = self._board[row][col]

        # Die 4 Richtungen als Tuple (Zeilenschritt, Spaltenschritt):
        # waagrecht, senkrecht, diagonal \, diagonal /
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for d_row, d_col in directions:
            count = 1 # der gerade gesetzte Stein zählt schon mit

            # In beide Richtungen zählen (z. B. nach links UND nach rechts).
            for sign in (1, -1):
                r = row + sign * d_row
                c = col + sign * d_col
                # Weiterlaufen, solange wir im Feld sind und der Stein dem gleichen Spieler gehört.
                while 0 <= r < self.ROWS and 0 <= c < self.COLS and self._board[r][c] == player:
                    count += 1
                    r += sign * d_row
                    c += sign * d_col

            if count >= 4:
                return True # Vier in einer Reihe gefunden.

        return False # In keiner Richtung vier in einer Reihe.

    def __str__(self) -> str:
        # Gibt das Spielfeld als Text zurück, damit print(game) in der main etwas anzeigt.
        symbols = {Player.NONE: ".", Player.RED: "R", Player.YELLOW: "Y"} # Hier wird jedem Spieler ein Zeichen zugeordnet.

        lines = [" 1 2 3 4 5 6 7"] # Spaltennummern wie in der main (1 .. 7)
        for row in self._board: # von row 0 (oben) bis row 5 (unten)
            lines.append(" " + " ".join(symbols[player] for player in row))

        lines.append(f"Am Zug: {self._player_on_turn.name}")
        return "\n".join(lines)
