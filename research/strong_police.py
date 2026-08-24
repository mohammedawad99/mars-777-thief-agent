"""Police evaluators strong enough to measure a Thief by.

**Why these exist.** The seven original families let the shipped Thief survive
98.93% of development scenarios, five of them at exactly 100%. A bank the
baseline never loses on cannot rank anything: every candidate scores 1.000 and
the harness reports a tie between policies that are not remotely equivalent.
Claiming the Thief is optimal against that would be claiming a measurement that
was never taken.

**Why the originals are weak, stated precisely.** `pursuit` ranks moves by scent
intensity - it follows the gradient of where the evader *has been*. A trail
leads to a vacated cell, so a policy that climbs it converges on history rather
than on the evader. None of the seven closes Manhattan distance on a believed
position, and none spends a barrier to remove somewhere the evader could go.
Those are the two mechanisms a capture actually needs.

**Authored from the game's own rules, not from anyone's code.** Each family
below is written from the movement, barrier and scent rules in the shared
contract. No opponent implementation was read, and none is imitated; these are
research instruments, and their only job is to be hard to survive.

**Legal on both sides of the measurement.** Every family reads only what an
actor may see at its own decision point - board, own position, quota, lawful
scent belief - and returns actions drawn from `legal_moves` and `is_placeable`.
A stress evaluator that cheated would flatter the Thief exactly where it should
be exposing it.
"""

from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Final

from mars777_thief.domain.actions import BarrierAction, MoveAction, PhysicalAction
from mars777_thief.domain.barriers import is_placeable
from mars777_thief.domain.board import Position
from mars777_thief.domain.observation import Observation
from mars777_thief.domain.reachability import reachable_from
from mars777_thief.domain.rules import Move, destination_of, legal_moves

STRONG_FAMILIES: Final[tuple[str, ...]] = (
    "closing_pursuit",
    "choke_control",
    "anticipating",
)
"""Three mechanisms the original seven never used: close, sever, and anticipate."""


def _distance(one: Position, other: Position) -> int:
    return abs(one.row - other.row) + abs(one.col - other.col)


def believed(observation: Observation) -> Position | None:
    """The strongest believed cell, or `None` when no evidence exists."""
    board = observation.board
    best: tuple[Decimal, int, int] | None = None
    found: Position | None = None
    for row in range(board.rows):
        for col in range(board.cols):
            cell = Position(row + board.start_index, col + board.start_index)
            weight = observation.scent.intensity_at(cell)
            key = (weight, -cell.row, -cell.col)
            if weight > Decimal(0) and (best is None or key > best):
                best, found = key, cell
    return found


def _severance(observation: Observation, target: Position, cell: Position) -> int:
    """How much of the evader's reachable region a placement at *cell* removes.

    The hypothetical board is built with `replace` rather than mutated: `Board`
    is frozen and revalidates its blocked set, so this asks the domain the
    question instead of assuming the answer.
    """
    board = observation.board
    before = reachable_from(board, target)
    after = reachable_from(replace(board, blocked=board.blocked | {cell}), target)
    return len(before) - len(after)


@dataclass(frozen=True, slots=True)
class StrongPolice:
    """One strong Police evaluator, named by the mechanism it uses."""

    family: str
    seed: int = 0

    def choose_action(self, observation: Observation) -> PhysicalAction:
        """Close, sever or anticipate - whichever this family is."""
        moves = legal_moves(observation.board, observation.own_position)
        if not moves:
            raise ValueError("a trapped actor is a terminal, not a decision")
        target = believed(observation)
        if target is None:
            return MoveAction(min(moves, key=lambda one: one.value))
        if self.family == "choke_control":
            placement = self._sever(observation, target)
            if placement is not None:
                return BarrierAction(placement)
        if self.family == "anticipating":
            return MoveAction(self._anticipate(observation, target, moves))
        return MoveAction(self._close(observation, target, moves))

    def _close(self, observation: Observation, target: Position, moves: tuple[Move, ...]) -> Move:
        """Minimise distance to the believed cell. The mechanism none of the seven had."""
        here = observation.own_position
        return min(moves, key=lambda one: (_distance(destination_of(here, one), target), one.value))

    def _anticipate(
        self, observation: Observation, target: Position, moves: tuple[Move, ...]
    ) -> Move:
        """Take the move whose worst case, after the evader's best reply, is best."""
        board, here = observation.board, observation.own_position
        options = [target, *(destination_of(target, one) for one in legal_moves(board, target))]
        return min(
            moves,
            key=lambda one: (
                max(_distance(destination_of(here, one), cell) for cell in options),
                _distance(destination_of(here, one), target),
                one.value,
            ),
        )

    def _sever(self, observation: Observation, target: Position) -> Position | None:
        """The lawful placement removing most of the evader's region, if any does."""
        here = observation.own_position
        candidates = [
            cell
            for cell in observation.board.orthogonal_neighbours(here)
            if is_placeable(observation.board, here, cell, observation.quota)
        ]
        severing = [
            (cell, _severance(observation, target, cell)) for cell in candidates if cell != target
        ]
        worthwhile = [(cell, cut) for cell, cut in severing if cut > 0]
        if not worthwhile:
            return next((cell for cell in candidates if cell == target), None)
        return max(worthwhile, key=lambda pair: (pair[1], -pair[0].row, -pair[0].col))[0]
