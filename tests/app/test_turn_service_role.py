"""ROLE-SPECIFIC: the thief local service may only move (BAR-004 is police-only).

The capability is refused at the application boundary **before** any domain
effect. This is local API capability design, not network authorization: the
shared domain barrier verifier stays available for checking a declared
placement later.
"""

import inspect

import pytest

from mars777_thief.app import turn_service
from mars777_thief.app.turn_service import (
    ActionKind,
    BarrierAction,
    LocalTurnService,
    MoveAction,
    UnsupportedActionError,
)
from mars777_thief.domain.barriers import BarrierQuota, is_placeable, place_barrier
from mars777_thief.domain.board import Board, Position
from mars777_thief.domain.rules import Move
from mars777_thief.domain.terminal import TurnLimits
from mars777_thief.domain.truth import LocalTruth

GRID = 7
CENTRE = Position(3, 3)
LIMITS = TurnLimits(max_moves=35, survival_threshold=35)
QUOTA = BarrierQuota(max_barriers=14)


def _service() -> LocalTurnService:
    return LocalTurnService(limits=LIMITS, quota=QUOTA)


def _truth(board: Board | None = None) -> LocalTruth:
    return LocalTruth(board=board or Board(rows=GRID, cols=GRID), own_position=CENTRE)


def test_a_move_action_is_accepted() -> None:
    result = _service().apply(_truth(), MoveAction(Move.N))
    assert result.kind is ActionKind.MOVE
    assert result.truth.own_position == Position(2, 3)
    assert result.truth.completed_steps == 1


@pytest.mark.parametrize("target", [Position(3, 3), Position(2, 3), Position(3, 4)])
def test_a_barrier_action_can_never_be_executed_locally(target: Position) -> None:
    before = _truth()
    with pytest.raises(UnsupportedActionError):
        _service().apply(before, BarrierAction(target))
    assert before.board.blocked == frozenset()
    assert before.own_position == CENTRE
    assert before.completed_steps == 0


def test_the_rejection_happens_before_any_domain_effect() -> None:
    # An otherwise perfectly legal placement is still refused, so the refusal
    # cannot be a side effect of domain validation.
    before = _truth()
    assert is_placeable(before.board, CENTRE, Position(2, 3), QUOTA)
    with pytest.raises(UnsupportedActionError):
        _service().apply(before, BarrierAction(Position(2, 3)))
    assert before.board.blocked == frozenset()


def test_the_service_has_no_hidden_barrier_capability() -> None:
    source = inspect.getsource(turn_service)
    assert "place_barrier" not in source
    assert not hasattr(LocalTurnService, "place_barrier")
    for flag in ("role", "is_police", "as_cop", "allow_barrier"):
        assert flag not in LocalTurnService.__init__.__code__.co_varnames


def test_a_quota_cannot_unlock_the_capability() -> None:
    service = LocalTurnService(limits=LIMITS, quota=BarrierQuota(max_barriers=99))
    with pytest.raises(UnsupportedActionError):
        service.apply(_truth(), BarrierAction(CENTRE))


def test_the_shared_domain_barrier_verifier_is_still_available() -> None:
    # Needed later to verify a declared placement; it must not be deleted here.
    board = Board(rows=GRID, cols=GRID)
    assert is_placeable(board, CENTRE, Position(2, 3), QUOTA)
    assert place_barrier(board, CENTRE, Position(2, 3), QUOTA).is_blocked(Position(2, 3))
    assert board.blocked == frozenset()


def test_exhaustion_and_illegal_moves_still_apply() -> None:
    from mars777_thief.app.turn_service import ActionsExhaustedError, InvalidActionError

    service = _service()
    with pytest.raises(ActionsExhaustedError):
        service.apply(
            LocalTruth(
                board=Board(rows=GRID, cols=GRID),
                own_position=CENTRE,
                completed_steps=LIMITS.max_moves,
            ),
            MoveAction(Move.STAY),
        )
    edge = LocalTruth(board=Board(rows=GRID, cols=GRID), own_position=Position(0, 3))
    with pytest.raises(InvalidActionError):
        service.apply(edge, MoveAction(Move.N))


def test_the_local_state_carries_no_barrier_specific_field() -> None:
    truth = _truth()
    for forbidden in ("barriers_placed", "barriers_remaining", "can_place_barrier", "role"):
        assert not hasattr(truth, forbidden)
