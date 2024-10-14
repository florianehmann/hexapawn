"""Tests the functionality of the `Move` class"""

import pytest

from hexapawn import Move, Squares


class TestMove:
    """Bundles the tests for the Move class"""

    def test_instantiate(self):
        """Test if we can instantiate the class directly"""
        Move(from_square=Squares.A1, to_square=Squares.A2)

    @pytest.mark.parametrize("uci, reference", [
        ('a1a2', Move(from_square=Squares.A1, to_square=Squares.A2)),
        ('c2b3', Move(from_square=Squares.C2, to_square=Squares.B3)),
    ])
    def test_from_uci(self, uci: str, reference: Move):
        """Test UCI factory"""
        assert Move.from_uci(uci) == reference

    @pytest.mark.parametrize("uci", ['a3a4', 'c2d3'])
    def test_from_invalid_uci(self, uci: str):
        """Test if the UCI factory properly fails on invalid commands"""
        with pytest.raises(ValueError):
            Move.from_uci(uci)
