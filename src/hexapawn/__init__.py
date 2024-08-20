"""Python Hexapawn library for playing and move generation"""

from enum import Enum
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

    def capture_candidates(self, player_color: Color) -> list[Self]:
        """Gets the squares that a pawn could capture at, given its `player_color`,
        if there is an opponent pawn on the target square."""
        if (rank_advanced_coords := self._advance_rank(self.value, player_color)) is None:
            return []

        candidate_coords = [coords for left in [True, False]
                            if (coords := self._change_file(rank_advanced_coords, left))]
        assert len(candidate_coords) > 0, "There is always at least a file to the left or right"

        return [self.__class__(coords) for coords in candidate_coords]


class Board:
    """Describes the board state in a game of Hexapawn"""

    def __init__(self):

        # two-dimensional array representing the board
        # indexing of the squares is done according to the Square enum
        self._board: list[list[Optional[Color]]] = [[None for _ in range(3)] for _ in range(3)]

        self.turn: Color = WHITE
        """Indicates which player does the next move"""

    def reset(self) -> None:
        """Restores the starting position"""
        self._board = [[WHITE, None, BLACK] for _ in range(3)]
        self.turn = WHITE

    def legal_moves(self):
        pass
