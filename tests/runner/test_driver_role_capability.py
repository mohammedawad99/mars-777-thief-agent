"""What this repository's driver structurally cannot do, and why that is right.

BAR-004 gives barrier placement to the police alone. `LocalTurnService` here has
no code path for one at all, so a strategy that returned a `BarrierAction` would
be refused before any emission was projected or any commitment sealed - the
driver never gets the chance to place one. The police repository proves the
placement half of the same contract, because only there can a placement execute.
"""

import asyncio

import pytest
from driver_builders import facing

from mars777_thief.app.turn_service import UnsupportedActionError
from mars777_thief.domain.actions import BarrierAction, MoveAction
from mars777_thief.domain.board import Position
from mars777_thief.domain.observation import Observation
from mars777_thief.domain.rules import Move


class Fixed:
    """A strategy that always returns the one action it was built with."""

    def __init__(self, action: object) -> None:
        self.action = action

    def choose_action(self, observation: Observation) -> object:
        return self.action


def test_a_barrier_choice_is_refused_before_anything_is_sealed() -> None:
    a, _ = facing(Fixed(BarrierAction(Position(0, 1))), Fixed(MoveAction(Move.S)))
    with pytest.raises(UnsupportedActionError, match="cannot execute"):
        asyncio.run(a.driver.play_round())
    assert a.driver.truth.completed_steps == 0
    assert a.producer.records == ()


def test_nothing_reached_the_peer_when_the_choice_was_refused() -> None:
    a, b = facing(Fixed(BarrierAction(Position(0, 1))), Fixed(MoveAction(Move.S)))
    with pytest.raises(UnsupportedActionError):
        asyncio.run(a.driver.play_round())
    assert b.context.current_turn().peer_commitment is None
