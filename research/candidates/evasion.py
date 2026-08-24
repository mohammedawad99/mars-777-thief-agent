"""Thief candidates aimed at the one mechanism that actually captures.

**What the evaluator established first.** Four independently authored strong
Police families were measured against the shipped Thief. `closing_pursuit` and
`anticipating` both left it surviving exactly 1.000 - movement-only pursuit
cannot catch a mobile evader when the only lawful evidence is a scent trail,
because a trail leads to a cell it has left. Only region denial captured
anything: `choke_control` took 3.1%, and spending the whole quota on it
reproduced that number exactly.

So there is one mechanism to defend against, and the shipped policy does not
model it. It maximises reachable region, then onward moves, then quiet - all
measured on the board *as it stands*. None of those terms anticipates a barrier.

**T-C, choke-aware.** Prefer a cell whose region survives the worst single
lawful placement the pursuer could make next. A cell with a large region reached
through one corridor is exactly what the shipped rule likes and what a barrier
punishes; this asks what the region would be *after* the placement that hurts
most, and keeps the current-region term as the tie-break so nothing already
working is discarded.

**T-D, escape lookahead.** The mirror of the pursuer's bounded search: for each
of our moves, assume the pursuer replies with whichever legal move brings it
closest, and take the move whose worst case leaves us furthest. One ply each
side, bounded by construction since both branching factors are at most five.

**Legality.** Both read only board, own position, quota and lawful scent belief.
Neither knows where the pursuer is except through the belief the game already
grants, neither remembers a trajectory, and neither can name an opponent. Both
return moves from `legal_moves`; a thief may not place a barrier and neither
tries to.
"""

from dataclasses import dataclass, field, replace
from decimal import Decimal
from typing import Final

from mars777_thief.app.baseline_strategy import BaselineStrategy
from mars777_thief.domain.actions import MoveAction
from mars777_thief.domain.board import Board, Position
from mars777_thief.domain.observation import Observation
from mars777_thief.domain.reachability import reachable_from
from mars777_thief.domain.rules import Move, destination_of, legal_moves

REVISION: Final[str] = "t-evasion-1"


def _believed(observation: Observation) -> Position | None:
    """The most-believed cell, which is our only lawful hint at the pursuer."""
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


def _blocked(board: Board, cell: Position) -> Board:
    """The board as it would stand with one more cell removed."""
    return replace(board, blocked=board.blocked | {cell})


def worst_region_after_one_barrier(observation: Observation, standing: Position) -> int:
    """The region left at *standing* after the most damaging single placement.

    Every cell adjacent to ours is a candidate, because a placement we cannot
    see coming is exactly the one that traps us. Excluded: our own cell, since
    the rules do not let a pursuer place where we stand; cells already blocked,
    which cannot be blocked twice; and cells off the board, which
    `orthogonal_neighbours` returns and the `Board` constructor rightly refuses.
    """
    board = observation.board
    worst = len(reachable_from(board, standing))
    for cell in board.orthogonal_neighbours(standing):
        if cell == standing or not board.contains(cell) or board.is_blocked(cell):
            continue
        worst = min(worst, len(reachable_from(_blocked(board, cell), standing)))
    return worst


@dataclass(frozen=True, slots=True)
class ChokeAwareStrategy:
    """Keep the region that survives the worst barrier, not the largest one now."""

    def choose_action(self, observation: Observation) -> MoveAction:
        """Rank landings by their post-barrier region, then by region now."""
        here = observation.own_position
        moves = legal_moves(observation.board, here)
        return MoveAction(
            min(
                moves,
                key=lambda one: (
                    -worst_region_after_one_barrier(observation, destination_of(here, one)),
                    -len(reachable_from(observation.board, destination_of(here, one))),
                    one.value,
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class EscapeLookaheadStrategy:
    """Take the move whose worst case, after the pursuer's best reply, is safest."""

    fallback: BaselineStrategy = field(default_factory=BaselineStrategy)

    def choose_action(self, observation: Observation) -> MoveAction:
        """Search one ply each side, or defer when there is nothing to search."""
        target = _believed(observation)
        if target is None:
            return self.fallback.choose_action(observation)
        board, here = observation.board, observation.own_position
        replies = [target, *(destination_of(target, one) for one in legal_moves(board, target))]

        def worst(move: Move) -> int:
            landing = destination_of(here, move)
            return min(
                abs(landing.row - cell.row) + abs(landing.col - cell.col) for cell in replies
            )

        return MoveAction(
            min(
                legal_moves(board, here),
                key=lambda one: (
                    -worst(one),
                    -len(reachable_from(board, destination_of(here, one))),
                    one.value,
                ),
            )
        )
