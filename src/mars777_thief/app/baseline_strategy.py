"""The thief baseline: keep room to run, and never step into a dead end.

Ch 6 §6.3.1 offers three equal tracks for movement policy and gives the choice
to the group; Ch 10 §10.3.3 places a **blind** module at this stage, *"blind in
the sense that there is not yet scent, natural language or deception"*. This is
that module, and the heuristic is **PROJECT-DERIVED**: the source mandates no
algorithm, only that the spatial decision stay algorithmic (§6.1, §6.6).

**What an evader can honestly optimise while knowing nothing.** Not distance
from the police - there is no believed police cell to be far from. What is
knowable is the shape of the board, and App E #47 names the way that shape
kills: *"a thief imprisoned without any legal move is likewise considered
captured"* (GAME-005). Barriers only ever accumulate (BAR-004 is irreversible),
so the standing danger is walking somewhere with nothing left to do. The policy
therefore prefers the destination with the larger reachable region, and among
equals the one with more onward legal moves.

**One measured limitation, stated rather than buried.** Every candidate
destination is either this actor's own cell or a cell orthogonally adjacent to
it, so whenever the actor stands somewhere traversable they all belong to the
*same* connected component - and the region term scores them identically. The
mobility term is what actually separates candidates in this stage. The region
term is still correct, still the right primary, and does separate genuinely
disconnected regions; it simply cannot be reached from here. `PRD03-FR-016`'s
escape-room preservation therefore needs its look-ahead form, which belongs to
the competitive stage along with the threat region it was designed to work with.

No corner or edge penalty is written by hand: an edge cell has fewer onward
moves and a corner fewer still, so mobility already says it, and a second rule
saying it again would be a rule that could disagree.
"""

from dataclasses import dataclass

from ..domain.actions import MoveAction
from ..domain.observation import Observation
from ..domain.reachability import reachable_from
from ..domain.rules import Move, destination_of, legal_moves
from .protocol_errors import LocalDefectError


@dataclass(frozen=True, slots=True)
class BaselineStrategy:
    """A stateless, deterministic, zero-token thief policy."""

    def choose_action(self, observation: Observation) -> MoveAction:
        """Return the legal move that leaves this side the most room to run.

        The return type is `MoveAction`, narrower than the port's
        `PhysicalAction`, and that narrowing is the point: BAR-004 gives
        placement to the police alone, so a thief that *could* return a
        `BarrierAction` would be a thief that could be asked why it did not.
        `LocalTurnService` refuses one as well - this makes it unconstructible.

        Candidates come from `legal_moves` and nowhere else. Ties fall to
        `MOVE_ORDER`, which `legal_moves` already preserves and `min` keeps.
        """
        candidates = legal_moves(observation.board, observation.own_position)
        if not candidates:
            raise LocalDefectError(
                f"no legal action from {observation.own_position}: an actor with"
                " none is a terminal the caller settles before asking a strategy",
            )
        return MoveAction(min(candidates, key=lambda move: self._risk(observation, move)))

    def _risk(self, observation: Observation, move: Move) -> tuple[int, int]:
        """How cornered *move* leaves this side: lower is safer.

        Both terms are negated sizes, so one `min` expresses "largest region,
        then most onward moves" without a second comparison rule. Integer
        throughout, so the ordering is exact on every platform.
        """
        landing = destination_of(observation.own_position, move)
        room = reachable_from(observation.board, landing)
        return (-len(room), -len(legal_moves(observation.board, landing)))
