"""The thief baseline: keep room to run, and never walk into a dead end.

App E #47 is the rule these tests are really about - a thief with no legal move
is captured - and barriers only ever accumulate, so the losing move is the one
that trades space for nothing. Two of the tests below deliberately pin a
*limitation* rather than a capability: every candidate destination shares one
connected region, so the region term always ties and mobility is what decides.
Asserting that keeps the boundary honest and makes any future look-ahead form
announce itself by breaking a test instead of passing quietly.
"""

import pytest
from strategy_builders import CENTRE, LIMITS, QUOTA, board, column, destination, seen

from mars777_thief.app.baseline_strategy import BaselineStrategy
from mars777_thief.app.protocol_errors import LocalDefectError
from mars777_thief.app.turn_service import LocalTurnService
from mars777_thief.domain.actions import BarrierAction, MoveAction
from mars777_thief.domain.board import Board, Position
from mars777_thief.domain.observation import Observation
from mars777_thief.domain.reachability import reachable_from
from mars777_thief.domain.rules import MOVE_ORDER, Move, legal_moves
from mars777_thief.domain.truth import LocalTruth

THIEF = BaselineStrategy()
DEAD_END = (Position(0, 2), Position(0, 4))


def _mobility(observation: Observation, move: Move) -> int:
    return len(legal_moves(observation.board, destination(observation, move)))


def _region(observation: Observation, move: Move) -> int:
    return len(reachable_from(observation.board, destination(observation, move)))


def test_it_returns_a_legal_move_on_an_open_board() -> None:
    action = THIEF.choose_action(seen(CENTRE))
    assert isinstance(action, MoveAction)
    assert action.move in legal_moves(board(), CENTRE)


def test_the_chosen_action_is_accepted_by_the_turn_service() -> None:
    truth = LocalTruth(board=board(), own_position=CENTRE)
    action = THIEF.choose_action(seen(CENTRE))
    assert LocalTurnService(limits=LIMITS, quota=QUOTA).apply(truth, action).completed_step == 1


def test_it_never_returns_a_barrier_anywhere_on_any_reachable_board() -> None:
    for row in range(7):
        for col in range(7):
            here = Position(row, col)
            observation = seen(here, Position(2, 2), Position(4, 4), Position(1, 5))
            if not legal_moves(observation.board, here):
                continue
            assert not isinstance(THIEF.choose_action(observation), BarrierAction)


def test_the_region_term_really_does_separate_disconnected_regions() -> None:
    wall = column(3, 0, 1, 2, 3, 4, 5, 6)
    walled = Board(rows=7, cols=7, blocked=frozenset(wall))
    assert len(reachable_from(walled, Position(3, 0))) == 21
    assert len(reachable_from(walled, Position(3, 6))) == 21
    assert len(reachable_from(Board(rows=7, cols=7), Position(3, 0))) == 49


def test_every_candidate_shares_one_region_so_mobility_is_what_decides() -> None:
    observation = seen(Position(1, 3), *DEAD_END)
    moves = legal_moves(observation.board, observation.own_position)
    assert len({_region(observation, move) for move in moves}) == 1
    assert len({_mobility(observation, move) for move in moves}) > 1


def test_it_refuses_a_dead_end_in_favour_of_the_open_board() -> None:
    observation = seen(Position(1, 3), *DEAD_END)
    assert _mobility(observation, Move.N) == 2
    chosen = THIEF.choose_action(observation)
    assert chosen != MoveAction(Move.N)
    assert _mobility(observation, chosen.move) == max(
        _mobility(observation, move)
        for move in legal_moves(observation.board, observation.own_position)
    )


def test_among_equal_regions_the_roomier_destination_wins() -> None:
    observation = seen(Position(3, 1), Position(2, 0), Position(4, 0))
    chosen = THIEF.choose_action(observation)
    assert _mobility(observation, Move.W) < _mobility(observation, chosen.move)


def test_a_tie_on_both_objectives_falls_to_the_existing_move_order() -> None:
    observation = seen(CENTRE)
    moves = legal_moves(observation.board, observation.own_position)
    scored = {(_region(observation, move), _mobility(observation, move)) for move in moves}
    assert len(scored) == 1
    assert THIEF.choose_action(observation) == MoveAction(MOVE_ORDER[0])


def test_it_stays_when_staying_is_the_only_legal_action() -> None:
    observation = seen(Position(0, 0), Position(0, 1), Position(1, 0))
    assert legal_moves(observation.board, observation.own_position) == (Move.STAY,)
    assert THIEF.choose_action(observation) == MoveAction(Move.STAY)


def test_the_same_observation_always_yields_the_same_action() -> None:
    observation = seen(Position(1, 5), Position(2, 2), Position(4, 4))
    first = THIEF.choose_action(observation)
    for _ in range(10):
        assert THIEF.choose_action(observation) == first


def test_a_barrier_changes_the_decision_it_would_otherwise_have_made() -> None:
    assert THIEF.choose_action(seen(Position(1, 3))) != THIEF.choose_action(
        seen(Position(1, 3), *DEAD_END, Position(2, 3))
    )


def test_it_refuses_rather_than_inventing_a_stay_when_there_is_no_legal_action() -> None:
    trapped = seen(Position(0, 0), Position(0, 0), Position(0, 1), Position(1, 0))
    assert legal_moves(trapped.board, trapped.own_position) == ()
    with pytest.raises(LocalDefectError, match="no legal action"):
        THIEF.choose_action(trapped)
