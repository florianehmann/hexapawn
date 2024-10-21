"""Tests the functionality of the `Squares` enum"""

import pytest

from hexapawn import Color, BLACK, WHITE
from hexapawn import Squares


# pylint: disable=protected-access
class TestSquares:
    """Bundles the tests for the Squares enum"""

    def test_corners_present(self):
        """Test if the corner squares are present in the enum"""
        _ = Squares.A1
        _ = Squares.C1
        _ = Squares.C3
        _ = Squares.A3

    @pytest.mark.parametrize("source_square, destination_square, player_color", [
        (Squares.A1, Squares.A2, WHITE),
        (Squares.B1, Squares.B2, WHITE),
        (Squares.C1, Squares.C2, WHITE),
        (Squares.A2, Squares.A3, WHITE),
        (Squares.B2, Squares.B3, WHITE),
        (Squares.C2, Squares.C3, WHITE),
        (Squares.A3, Squares.A2, BLACK),
        (Squares.B3, Squares.B2, BLACK),
        (Squares.C3, Squares.C2, BLACK),
        (Squares.A2, Squares.A1, BLACK),
        (Squares.B2, Squares.B1, BLACK),
        (Squares.C2, Squares.C1, BLACK),
    ])
    def test_advance_rank(self, source_square: Squares, destination_square: Squares, player_color: Color):
        """Tests if the index arithmetic in `_advance_rank` produces correct results"""
        assert Squares._advance_rank(source_square.value, player_color) == destination_square.value

    @pytest.mark.parametrize("source_square, player_color", [
        (Squares.A3, WHITE),
        (Squares.B3, WHITE),
        (Squares.C3, WHITE),
        (Squares.A1, BLACK),
        (Squares.B1, BLACK),
        (Squares.C1, BLACK)
    ])
    def test_advance_rank_edge(self, source_square: Squares, player_color: Color):
        """Test if we get None if we try to advance off the board's edge"""
        assert Squares._advance_rank(source_square.value, player_color) is None

    @pytest.mark.parametrize("player_color, source_square, target_square, expected", (
        (WHITE, Squares.B1, Squares.B2, True),
        (WHITE, Squares.B1, Squares.C2, False),
        (WHITE, Squares.B1, Squares.C1, False),
        (WHITE, Squares.B2, Squares.B3, True),
        (BLACK, Squares.B3, Squares.B2, True),
        (BLACK, Squares.B3, Squares.C2, False),
        (BLACK, Squares.B3, Squares.C3, False),
        (BLACK, Squares.B2, Squares.B1, True)
    ))
    def test_can_advance_to(self, player_color: Color, source_square: Squares, target_square: Squares, expected: bool):
        """Checks if `Squares` properly determines which moves are regular advances."""
        assert source_square.can_advance_to(target_square, player_color) == expected

    @pytest.mark.parametrize("player_color, starting_square, candidates", [
        (WHITE, Squares.A1, {Squares.B2}),
        (WHITE, Squares.A2, {Squares.B3}),
        (WHITE, Squares.A3, set()),
        (WHITE, Squares.B1, {Squares.A2, Squares.C2}),
        (WHITE, Squares.B2, {Squares.A3, Squares.C3}),
        (WHITE, Squares.B3, set()),
        (WHITE, Squares.C1, {Squares.B2}),
        (WHITE, Squares.C2, {Squares.B3}),
        (WHITE, Squares.C3, set()),
        (BLACK, Squares.A1, set()),
        (BLACK, Squares.A2, {Squares.B1}),
        (BLACK, Squares.A3, {Squares.B2}),
        (BLACK, Squares.B1, set()),
        (BLACK, Squares.B2, {Squares.A1, Squares.C1}),
        (BLACK, Squares.B3, {Squares.A2, Squares.C2}),
        (BLACK, Squares.C1, set()),
        (BLACK, Squares.C2, {Squares.B1}),
        (BLACK, Squares.C3, {Squares.B2}),
    ])
    def test_capture_candidates(self, player_color: Color, starting_square: Squares, candidates: set[Squares]):
        """Test if we get the right capture candidates"""
        assert starting_square.capture_candidates(player_color) == candidates
