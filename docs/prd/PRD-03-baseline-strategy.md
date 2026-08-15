# PRD-03 — Baseline Strategy — group MaRs-777 (THIEF)

## 1. Document Metadata

| Field | Value |
|---|---|
| PRD | PRD-03 — Baseline Strategy (**THIEF**) |
| Owns | The strategy plug-in behind `StrategyPort`; `app.strategy_api` contract usage |
| Architecture inputs | `STRATEGY_ARCHITECTURE.md`, `API_BOUNDARIES.md`, `DATA_FLOW.md` §3, `DEPENDENCY_RULES.md` §2 |
| Symmetry class | **ROLE-SPECIFIC** — the Police PRD-03 differs materially by design |

## 2. Status

**Implementation status: BASELINE IMPLEMENTED (Stage 6B).** Live in
`domain/observation.py`, `domain/reachability.py`, `app/strategy_api.py` and
`app/baseline_strategy.py`: a deterministic, LLM-free, belief-free, scent-free
thief baseline behind the documented `StrategyPort`, returning `MoveAction` and
structurally unable to return a `BarrierAction`. No dependency was added and no
existing module was modified. It is **not yet wired into a game owner** — that is
Stage 6C.

**Nothing here is deleted.** Requirements presupposing belief, plug-in loading,
seeded randomness, a decision time-box or a self-play benchmark are retained and
marked **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE**; they remain the
long-term contract and are simply not Stage-6B acceptance criteria.

**APPROVED — PHASE 2 LOCKED.** Approved after Stage 2-CLOSE supervising review.
**Implementation status: NOT STARTED.** No code. No dependency.

## 3. Purpose

Define (a) the **StrategyPort contract**, (b) a **legal deterministic zero-token thief
baseline**, (c) a **benchmarkable fallback**, and (d) the **extension seam** for the
later competitive-strategy phase. This PRD does **not** design our final league strategy.

## 4. Problem Statement

The thief must survive to the survival threshold without ever seeing the police's true
position, while barriers accumulate **irreversibly** and can trap it — including the
losing condition of having **no legal move at all** (GAME-005). A baseline that walks
into a corner loses; one entangled with networking or crypto cannot be replaced later.
Both must be designed out now.

## 5. Scope

Strategy plug-in decision policy · seeding and tie-breaking · time-boxing and fallback ·
diagnostics it emits · the plug-in selection mechanism.

## 6. Out of Scope

Movement **legality** (PRD-01 — the validator remains authoritative) · transport,
crypto, artifacts (structurally forbidden) · hint/bluff text generation and LLM
(PRD-04) · advanced competitive strategy (later phase, §13.6).

## 7. Actors

`app.turn_service` (calls the port) · `domain.observation` (builds the input) ·
`domain.rules` (validates the output) · `infra.metrics` (records diagnostics).

## 8. Definitions

**Observation** — the role-legal input record. **ProposedAction** — a *proposal*, not an
effect. **Mobility** — number of legal moves available from a cell. **Escape room** —
size of the barrier-aware reachable region. **Threat region** — believed police-reachable
cells within *k* steps. **Fallback** — deterministic legal action used when the primary
policy cannot decide in budget.

## 9. Locked Source Requirements

| ID | Modality | Requirement |
|---|---|---|
| STRAT-001 | MUST | Separate strategy module between incoming hint-decode and outgoing commit-pack; holds belief update, legal move choice, deception text |
| STRAT-002 | MUST | Keep the spatial/movement decision **fully algorithmic** in all policy modes |
| STRAT-003 | MAY | Movement policy may be heuristics (Bayes + Manhattan), own algorithm, or optionally RL |
| GAME-005 | MUST | A thief with **no legal move** is considered **captured** |
| GAME-008 | MUST | Step ceiling and survival threshold come from config (defaults 35, MINIMUM) |
| GAME-009 | MUST | Movement legality decided by deterministic code, never delegated to an LLM |
| LLM-001 | SHOULD | Do not hand the LLM the move decision itself |
| LLM-005 | MAY | LLM move tactic only by explicit documented mutual agreement; local code still enforces legality |
| GUI-001 | MUST | Local truth only (own position, sensed scent, received hints, belief heatmap) |
| GUI-002 | **MUST NOT** | Never display/expose the full objective board state |

## 10. Project / Architecture Decisions

| Decision | Type |
|---|---|
| Strategy receives `Observation`, returns `ProposedAction` | ARCHITECTURE-CONSTRAINT |
| Strategy imports only `app.strategy_api` + `domain` value types | ARCHITECTURE-CONSTRAINT (D3) |
| Deterministic **given a seed**; seed recorded as replay evidence | PROJECT-CONTRACT |
| Plug-in selected by dotted path in local settings | **REFERENCE-COMPATIBILITY** pattern (D-13) |
| Baseline is intentionally simple and **must not** be our competitive strategy | PROJECT-CONTRACT |

## 11. Inputs — the legal `Observation`

Own true position · own step / **remaining steps to the survival threshold** · locked
config values (grid, `move_set`, `max_moves`, `survival_threshold`, `max_barriers`,
scent parameters) · public barrier set · own scent readings · **belief** over police
location (explicitly typed, with uncertainty) · current scores · remaining decision
budget · validated opponent-public data (revealed police move, revealed hint + `intent`,
**declared barrier placements** — which are public and truthful by BAR-001/002).

**Forbidden inputs (the type has no field for them):** police true position · police
nonce · police pre-reveal move · any network/transport object · FastMCP client or server
· hashing/auth objects or key material · artifact writer · Gmail · GUI state ·
unrestricted filesystem access.

## 12. Outputs — `ProposedAction`

`move ∈ {N,S,E,W,STAY}` (the thief has **no** barrier action) · optional hint request
(text produced by PRD-04) with its `intent` classification — a hint **may legally be a
lie**, but its classification MUST be truthful · optional confidence/diagnostics.
**Every output is a proposal**; `domain.rules` validates before any effect.

## 13. Functional Requirements

### 13.1 Contract

| ID | Requirement | Traces to |
|---|---|---|
| **PRD03-FR-001** | The strategy is a replaceable plug-in satisfying `StrategyPort`; replacing it requires **no change** to networking, cryptography, persistence, GUI, or reporting. | STRAT-001; `STRATEGY_ARCHITECTURE.md` |
| **PRD03-FR-002** | It accepts only an `Observation` and returns only a proposed action. *Stage 6B: satisfied with a bare `MoveAction`, narrowing the port's `PhysicalAction`; `ProposedAction` reserved for PRD-04 (see §12).* | `API_BOUNDARIES.md` P1 |
| **PRD03-FR-003** | It MUST NOT send network messages, write artifacts, touch nonce/hash material, mutate authoritative state, or bypass validation. | `DEPENDENCY_RULES.md` §3 |
| **PRD03-FR-004** | The spatial/movement decision is **fully algorithmic** in all modes. | **STRAT-002**, GAME-009 |
| **PRD03-FR-005** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** The plug-in is selected by configuration (dotted path). *App F Table 22 declares itself "a reference table only — the choice is private to each peer and is not subject to negotiation", so this is a reference pattern, not a source mandate. One strategy exists; a loader with nothing to choose between waits for the second.* | REFERENCE-COMPATIBILITY (D-13) |
| **PRD03-FR-006** | The strategy MUST NOT propose a barrier action — barrier placement is police-only. | BAR-004 (police-only) |

### 13.2 Thief baseline policy

> **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE:** `PRD03-FR-011`,
> `PRD03-FR-012`, `PRD03-FR-013`, `PRD03-FR-014`, `PRD03-FR-018`,
> `PRD03-FR-019`. Each needs a believed police cell or the threat region derived
> from one, and belief's evidence — scent and hints — arrives at PRD-04. Ch 10
> §10.3.3 puts a **blind** strategy at this stage.
>
> **In force at Stage 6B.** `FR-006` **implemented and strengthened**: the
> baseline's return type is `MoveAction`, so a placement is not merely refused
> but unconstructible. `FR-010` implemented — candidates come from `legal_moves`
> alone. `FR-015` (mobility guard) **implemented**, and it is the operative
> discriminator: the thief takes the destination with the larger barrier-aware
> reachable region and, among equals, more onward legal moves. `FR-020` holds —
> no outcome is asserted.
>
> **`FR-016` (escape-room preservation) is implemented but measurably inert, and
> that is recorded rather than glossed.** Every candidate destination is either
> this actor's own cell or one orthogonally adjacent to it, so whenever the
> actor stands somewhere traversable all candidates belong to the **same**
> connected component and the region term scores them identically — verified
> across 3,209 randomly generated candidate sets at Stage 6B, in which the term
> differed **zero** times. The term is correct and does separate genuinely
> disconnected regions; it simply cannot be reached from a single actor's own
> move set. Making it bite needs the *look-ahead* form — the survivable region
> still available after **threat-conditioned or likely** opponent replies — which
> belongs with the threat region it was designed to work alongside. **Deferred
> with the belief group** by supervising decision at Stage 6B-C, which kept the
> Stage-6B implementation unchanged rather than swapping the objective during a
> closure. Two things that refinement will **not** do: it will not read the
> police's true position, and it will not gain one — it conditions on *belief*
> and on the threat region derived from legally available evidence, exactly as
> `FR-012` requires. **No claim is made that escape-room optimisation is already
> competitive**; in Stage 6B it is present in baseline form only.
>
> **`FR-017` (corner/edge penalty) is deliberately not implemented as a separate
> rule.** An edge cell has fewer onward moves and a corner fewer still, so the
> mobility term already expresses it; a second rule saying the same thing is a
> rule that can disagree with the first. Revisit only if measurement shows
> mobility alone is insufficient.

| ID | Requirement | Traces to |
|---|---|---|
| **PRD03-FR-010** | Build the **candidate set** = all legal moves at this step, using the same deterministic rules as the validator (no private legality logic). | GAME-003/004; PRD-01 |
| **PRD03-FR-011** | Maintain a **belief** over candidate police cells from legally available evidence only: own scent readings, revealed police moves, revealed hints (unreliable — `intent` may be a lie), and **publicly declared barrier placements**, which reveal where the police recently was (BAR-004 restricts placement to its own or an adjacent cell). | STRAT-001; BAR-001/004 |
| **PRD03-FR-012** | Belief MUST NOT use the police's true position; it remains a distribution, never a certainty unless legitimately revealed. | GUI-002; PRD01-FR-021/022 |
| **PRD03-FR-013** | Compute a **threat region**: cells the believed police could reach within *k* steps (barrier-aware BFS), where *k* is a small configured horizon (baseline default 2). | STRAT-003 |
| **PRD03-FR-014** | **Escape rule:** prefer the legal move that **maximises barrier-aware distance to the belief mode** while not entering the threat region, subject to the mobility guard below. | STRAT-003 |
| **PRD03-FR-015** | **Mobility guard (dead-end avoidance):** never choose a move whose destination has **mobility ≤ 1** (only the cell it came from) when an alternative legal move with higher mobility exists. This directly defends against GAME-005 (no legal move ⇒ captured). | **GAME-005** |
| **PRD03-FR-016** | **Escape-room preservation:** among moves surviving the mobility guard, prefer the one whose destination has the **larger barrier-aware reachable region** (flood-fill size, capped for cost). This preserves future options as barriers accumulate irreversibly. | BAR-004 (irreversible) |
| **PRD03-FR-017** | **Corner/edge penalty:** destinations on the board edge, and especially corners, receive a deterministic penalty; they are chosen only when they strictly dominate on distance-and-mobility. | GAME-005 defence |
| **PRD03-FR-018** | **Survival awareness:** as `remaining steps to survival_threshold` becomes small, the policy weights *not being captured this turn* above increasing separation — it never trades a safe cell for a marginally more distant but lower-mobility cell in the final steps. | **GAME-008**; GAME-006 (survival scoring) |
| **PRD03-FR-019** | **Anti-passivity:** `STAY` is chosen only when it is the sole legal move, or when every move strictly reduces mobility **and** STAY does not enter the threat region. | quality requirement |
| **PRD03-FR-020** | The strategy never asserts an outcome (survival/capture); terminals are **detected by the domain**. | PRD01-FR-055 |

### 13.3 Determinism and tie-breaking

| ID | Requirement | Traces to |
|---|---|---|
| **PRD03-FR-030** | Given identical strategy profile, seed and `Observation`, the returned `ProposedAction` is identical on Linux and Windows. | cross-OS |
| **PRD03-FR-031** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE** (constraint retained, not yet exercised). Randomness, if any, comes **only** from a seeded RNG owned by the strategy. *The Stage-6B baseline draws no randomness at all, so no RNG owner exists to seed.* | determinism |
| **PRD03-FR-032** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** The seed is supplied via local settings and **recorded as replay evidence**. *No seed exists while the policy is deterministic.* | REPLAY-001/002 |
| **PRD03-FR-033** | **Tie-break order (total and deterministic):** (1) larger barrier-aware reachable region; (2) higher destination mobility; (3) the existing `domain.rules.MOVE_ORDER`, which is **`N, S, E, W, STAY`**. *Corrected at Stage 6B on two counts: the action order previously read `N, E, S, W, STAY`, which never matched the implemented, unit-tested `MOVE_ORDER` — production wins; and region now precedes mobility, per the Stage-6A ruling. The two orderings are behaviourally identical while the region term ties (see §13.2). The belief-mode distance and corner/edge terms are deferred with their groups.* The order is total because candidates are a subset of the five `Move` values, each occurring once. | determinism; `PRD-01` §19 |
| **PRD03-FR-034** | No decision may depend on Python hash randomization, set iteration order, or dict insertion order; collections are canonically sorted before iteration. | cross-OS |

### 13.4 Time-boxing, fallback and failure

| ID | Requirement | Traces to |
|---|---|---|
| **PRD03-FR-040** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** The decision is time-boxed strictly inside `response_timeout_sec`. *App F T16 #6's 30 s is a timeout "for each network request", not a decision budget; the source defines none. Measured Stage-6B p95 is ~0.5 ms.* | STATE-004; PRD-02 |
| **PRD03-FR-041** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** The fallback ladder. *Every rung presupposes a fallible strategy. The Stage-6B baseline is total and deterministic, selecting only from `legal_moves`, so its only failure mode is an empty candidate set — a **terminal** the caller settles first (App E #47, and `FR-045` below). Unreachable rungs are untestable dead code. Its action order must be corrected to `MOVE_ORDER` when it lands.* | measurable ordering |
| **PRD03-FR-042** | A strategy failure MUST degrade to a deterministic legal fallback and MUST NOT bypass the validator. | GAME-009 |
| **PRD03-FR-043** | A strategy failure MUST NOT mutate authoritative domain state. | `DEPENDENCY_RULES.md` |
| **PRD03-FR-044** | If the optional LLM (PRD-04) is unavailable or unusable, movement is unaffected. | LLM-001; T0 viability |
| **PRD03-FR-045** | **IMPLEMENTED.** If the candidate set is empty the strategy returns no action and the **domain** declares the GAME-005 terminal; the strategy never self-declares capture. *Stage 6B raises the frozen `E-LOCAL-DEFECT` identity (`LocalDefectError`) rather than inventing a `STAY`: being asked at all means the caller skipped a terminal check it owns. No new error identity was registered.* | **GAME-005** |
| **PRD03-FR-046** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** Every fallback activation is recorded with its reason. *Deferred with `FR-041`: there is no fallback to record.* | `OBSERVABILITY.md` |

### 13.5 Zero-token operation

| ID | Requirement | Traces to |
|---|---|---|
| **PRD03-FR-050** | The baseline operates fully at **T0** (no LLM, no tokens) and can complete an entire six-sub-game series. | `LLM_BOUNDARY.md`; PERF-003 |

### 13.6 Future competitive extension (explicitly deferred)

| ID | Requirement |
|---|---|
| **PRD03-FR-060** | The seam MUST allow a later competitive strategy to add, **without contract change**: police trajectory prediction, trap/enclosure modelling over the barrier network, deception optimisation (coordinated hint/`intent` policy), adaptive opponent modelling across the series, and multi-turn search. |
| **PRD03-FR-061** | **None of these is claimed or required for the baseline**, which is a simple, competent, deterministic survival policy. |

## 14. Non-Functional Requirements

| ID | Requirement |
|---|---|
| **PRD03-NFR-001** | Decision latency p95 **< 50 ms** at 7×7 with a full barrier set (flood-fill capped), measurable. |
| **PRD03-NFR-002** | Zero imports of transport, crypto, artifact, GUI or LLM modules (dependency test). |
| **PRD03-NFR-003** | Every strategy file ≤ **150 lines**; belief, mobility/escape-room, and policy are separate modules. |
| **PRD03-NFR-004** | **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE.** A strictly higher survival rate than a uniform-random legal policy over ≥ 200 seeded self-play sub-games. *Self-play needs both agents in one process; App E #1/#2 keep them separate with no shared memory, so this needs a SIMULATION harness that does not exist. Not a Stage-6B acceptance criterion.* |

## 15. State / Lifecycle Responsibilities

Owns only internal policy state (belief working copy, seeded RNG, cached mobility/
escape-room results for the current step). Owns no authoritative state.

## 16. Validation Rules

The strategy pre-checks candidate legality with the shared rules, but the **validator
remains authoritative**; every proposal is re-validated before effect. A rejected
proposal triggers `E-LOCAL-VALIDATION` and the fallback ladder.

## 17. Error / Failure Behaviour

Timeout → fallback · invalid proposal → `E-LOCAL-VALIDATION` → fallback · **empty
candidate set → domain declares GAME-005 capture** (strategy asserts nothing) · internal
exception → logged, fallback · LLM unavailable → `E-LLM-UNAVAILABLE`, non-fatal.

## 18. Security / Privacy Constraints

Cannot access opponent truth · cannot reach nonce/key material · cannot emit network
traffic · receives only sanitized validated opponent-public data · diagnostics contain
no forbidden data or secrets · a hint may be a lie, but its `intent` classification is
always truthful (C-08 semantics; enforced in PRD-04).

## 19. Determinism / Reproducibility

Same profile + seed + observation ⇒ same action on both OSes; total tie-break order;
no wall-clock/unseeded randomness; canonical iteration. Seed recorded for replay.

## 20. Performance / Deadline Constraints

Budget strictly inside `response_timeout_sec` (config-sourced). Flood-fill and BFS are
bounded by the grid size and capped so the p95 latency target holds. Anytime behaviour:
a legal "best so far" is always available at budget expiry.

## 21. Cross-Platform Constraints

Identical decisions on Linux and Windows; integer arithmetic; sorted collections; no
locale/platform-dependent behaviour.

## 22. Observability / Evidence

Decision latency, fallback rate + reason, validator-rejection rate, candidate-set size,
destination mobility, escape-room size, threat-region size, belief mode margin, action
chosen, seed, steps remaining to survival. **Belief quality is measured only post-hoc at
replay time**, never live.

## 23. Acceptance Criteria

**Common**

| ID | Criterion |
|---|---|
| **PRD03-AC-001** | The `Observation` type exposes no opponent true position; contract test fails if such a field is added. |
| **PRD03-AC-002** | Static check: strategy imports no transport, crypto, artifact, reporting or GUI module. |
| **PRD03-AC-003** | Same seed + same observation ⇒ identical action, on Linux and Windows. |
| **PRD03-AC-004** | Decision always returns within the budget, or the fallback ladder produces a legal action. |
| **PRD03-AC-005** | A deliberately illegal proposal is rejected by the validator and the fallback is used; no state change. |
| **PRD03-AC-006** | A complete six-sub-game series runs at **T0** with zero tokens. |

**Thief-specific**

> **DEFERRED — BELIEF / COMPETITIVE STRATEGY STAGE:** `PRD03-AC-020`,
> `PRD03-AC-022`, `PRD03-AC-025`, `PRD03-AC-026`, `PRD03-AC-028`. `AC-020`,
> `AC-025` and `AC-026` name a belief mode or a threat region; `AC-022` needs
> the look-ahead escape-room form (see §13.2); `AC-028` is deferred with
> `NFR-004`. **`AC-021`, `AC-023`, `AC-024` and `AC-027` are met** — dead-end
> avoidance, barrier-sensitive decisions, `MOVE_ORDER` tie-breaking, and a
> baseline that cannot emit a barrier placement at all.

| ID | Criterion |
|---|---|
| **PRD03-AC-020** | *Simple escape:* with belief concentrated near the thief on an open board, each turn does not decrease barrier-aware distance to the belief mode unless the mobility guard forces it. |
| **PRD03-AC-021** | *Dead-end avoidance:* offered a move into a cell with mobility 1 and an alternative with higher mobility, the baseline never chooses the dead end. |
| **PRD03-AC-022** | *Trap resistance:* in a corridor scenario where a greedy "maximise distance" policy would enter a pocket that barriers can seal, the baseline chooses the higher-escape-room cell instead. |
| **PRD03-AC-023** | *Barrier-aware mobility:* declared barrier placements immediately reduce computed mobility/escape-room and change the chosen move accordingly. |
| **PRD03-AC-024** | *Deterministic equal-choice:* two equally scored moves resolve via the documented tie-break order, identically every run. |
| **PRD03-AC-025** | *Survival awareness:* in the final steps before `survival_threshold`, the policy prefers the safe higher-mobility cell over a marginally more distant lower-mobility cell. |
| **PRD03-AC-026** | *Anti-passivity:* STAY is not chosen when a legal move preserves mobility and avoids the threat region. |
| **PRD03-AC-027** | *No barrier action:* the thief baseline never emits a barrier placement. |
| **PRD03-AC-028** | *Benchmark:* survival rate over ≥ 200 seeded sub-games strictly exceeds a uniform-random legal policy. |

## 24. Planned Tests

| ID | Test | Layer |
|---|---|---|
| **PRD03-T-001** | Observation privacy contract | CONTRACT |
| **PRD03-T-002** | Forbidden-import scan | CONTRACT |
| **PRD03-T-003** | Seeded determinism | PROPERTY |
| **PRD03-T-004** | Cross-OS determinism | PROPERTY / CROSS-PROCESS |
| **PRD03-T-005** | Time-box + fallback ladder (each rung) | UNIT |
| **PRD03-T-006** | Validator authority over a bad proposal | INTEGRATION |
| **PRD03-T-007** | Mobility guard / dead-end avoidance | UNIT |
| **PRD03-T-008** | Escape-room preservation in a corridor | UNIT |
| **PRD03-T-009** | Threat-region avoidance | UNIT |
| **PRD03-T-010** | Barrier declaration updates mobility | UNIT |
| **PRD03-T-011** | Tie-break total order | PROPERTY |
| **PRD03-T-012** | Survival-awareness weighting near threshold | UNIT |
| **PRD03-T-013** | Never proposes a barrier | CONTRACT |
| **PRD03-T-014** | Empty candidate set ⇒ domain GAME-005 terminal (strategy silent) | INTEGRATION |
| **PRD03-T-015** | Zero-token full series | INTEGRATION |
| **PRD03-T-016** | Baseline vs random benchmark (≥200 seeded runs) | SIMULATION |

## 25. Requirement Traceability

**Directly owned:** STRAT-001, STRAT-002, STRAT-003. **Constrained by:** GAME-005,
GAME-008, GAME-009, LLM-001, LLM-005, GUI-001/002, GAME-003/004; BAR-001/004 consumed as
*public evidence*. **Consumes:** PRD-01 validator + `Observation`; PRD-02 budget;
PRD-04 hint/`intent`.

## 26. Dependencies on Other PRDs

PRD-01 (legality, mobility/distance primitives, belief type) · PRD-02 (invocation,
budget, seed plumbing) · PRD-04 (hint/`intent`, including legal deception) · PRD-07
(metrics, replay-time belief analysis).

## 27. Open Design Decisions

Belief representation (shared with PRD-01) · threat-horizon *k* default and its config
home · escape-room flood-fill cap · corner/edge penalty weights · survival-awareness
switch point · benchmark harness shape.

## 28. Explicit Non-Goals

Not the competitive league strategy · no trajectory prediction, trap modelling,
deception optimisation, opponent modelling or multi-turn search in the baseline · no LLM
movement · no legality logic of its own · no barrier actions.

## 29. Implementation Readiness Checklist

- [x] Port contract, legal inputs and forbidden inputs enumerated
- [x] Baseline policy fully specified (escape, mobility guard, escape-room, survival awareness)
- [x] GAME-005 dead-end risk explicitly designed against
- [x] Total deterministic tie-break order defined
- [x] Fallback ladder defined with measurable ordering
- [x] Advanced techniques explicitly deferred, not claimed
- [x] Supervising review — **complete**. Reviewed at Stage 2-CLOSE and again at
  the Stage-6A contract & design lock, whose rulings are applied above. *This box
  previously contradicted §2, which already recorded the review as done; the
  Stage-6A audit found the contradiction and Stage 6B resolves it in favour of
  §2, the reviews being a matter of record.*
- [x] Baseline implementation — **complete (Stage 6B)**, TDD, 100% statement and
  branch coverage on all four new modules, both repositories
- [ ] Wiring into an autonomous game owner — **not started (Stage 6C)**
- [ ] Belief / competitive strategy — **not started**, everything marked
  DEFERRED above
