"""Python Hexapawn library for playing and move generation"""

from dataclasses import dataclass
from enum import Enum
from itertools import product
import re
from typing import Optional, TypeAlias, Self

Color: TypeAlias = bool
WHITE: Color = True
BLACK: Color = False


class Squares(Enum):
    """All squares of the board"""
    A1 = (0, 0)
    A2 = (0, 1)
    A3 = (0, 2)
    B1 = (1, 0)
    B2 = (1, 1)
    B3 = (1, 2)
    C1 = (2, 0)
    C2 = (2, 1)
    C3 = (2, 2)

    @staticmethod
    def _advance_rank(coords: tuple[int, int], player_color: Color) -> tuple[int, int] | None:
        # Gets the coordinate tuple of the square a pawn of `player_color` would advance to without capturing
        new_coords = (
            coords[0],
            coords[1] + (1 if player_color == WHITE else -1)
        )

        if new_coords[1] < 0 or new_coords[1] > 2:
            return None

        return new_coords

    @staticmethod
    def _change_file(coords: tuple[int, int], left: bool = True) -> tuple[int, int] | None:
        # Changes the file of a coordinate tuple according to the direction specified. Left means towards a file.
        new_coords = (
            coords[0] + (-1 if left else 1),
            coords[1]
        )

        if new_coords[0] < 0 or new_coords[0] > 2:
            return None

        return new_coords

    def capture_candidates(self, player_color: Color) -> set[Self]:
        """Gets the squares that a pawn could capture at, given its `player_color`,
        if there is an opponent pawn on the target square."""
        if (rank_advanced_coords := self._advance_rank(self.value, player_color)) is None:
            return set()

        candidate_coords = [coords for left in [True, False]
                            if (coords := self._change_file(rank_advanced_coords, left))]
        assert len(candidate_coords) > 0, "There is always at least a file to the left or right"

        return {self.__class__(coords) for coords in candidate_coords}


@dataclass
class Move:
    """Move of a pawn from a square to another square"""

    from_square: Squares
    """Source square of the move"""

    to_square: Squares
    """Target square of the move"""

    @classmethod
    def from_uci(cls, uci: str) -> Self:
        """Creates a move from a UCI string"""
        pattern = "([abc][1-3])([abc][1-3])"
        match = re.match(pattern, uci.lower().strip())

        if not match:
            raise ValueError(f"Invalid UCI string '{uci}'")

        from_uci = match.group(1)
        to_uci = match.group(2)

        return cls(
            from_square=Squares[from_uci.upper()],
            to_square=Squares[to_uci.upper()],
        )


class Board:
    """Describes the board state in a game of Hexapawn"""

    def __init__(self):

        # two-dimensional array representing the board
        # indexing of the squares is done according to the Square enum
        self._board: list[list[Optional[Color]]] = [[None for _ in range(3)] for _ in range(3)]

        self.turn: Color = WHITE
        """Indicates which player does the next move"""

        self.clear().reset()

    def clear(self) -> Self:
        """Removes all pieces from the board"""
        for i, j in product(range(len(self._board)), range(len(self._board[0]))):
            self._board[i][j] = None

        return self

    def reset(self) -> Self:
        """Restores the starting position"""
        for square in [Squares.A1, Squares.B1, Squares.C1]:
            file, rank = square.value
            self._board[file][rank] = WHITE

        for square in [Squares.A3, Squares.B3, Squares.C3]:
            file, rank = square.value
            self._board[file][rank] = BLACK

        self.turn = WHITE

        return self

    def legal_moves(self):
        """Legal moves from the current position and for the player whose turn it is."""

    def to_unicode(self) -> str:
        """Returns a Unicode symbol representation of the state of the board"""
        result = ""
        for rank in range(len(self._board[0])):
            for file in range(len(self._board)):  # pylint: disable=consider-using-enumerate
                entry = self._board[file][rank]
                if entry is not None:
                    result += "♙ " if entry == WHITE else "♟ "
                else:
                    result += "□ " if (file + rank) % 2 != 0 else "■ "
            result += "\n"
        result = result[:-1]
        return result

    def print(self) -> None:
        """Prints a Unicode representation if the state of the board"""
        print(self.to_unicode())
