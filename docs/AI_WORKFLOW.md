# AI Workflow - group MaRs-777

> **Status: DRAFT.**

## Roles

- The **human** receives a prompt from the supervising reviewer.
- **Claude Code** performs repository and terminal work inside a single repository.
- Claude returns an **evidence report** (exact commands + results).
- Work is **reviewed** before any commit or push.

## Principles

- No implementation before an approved plan.
- No commit/push without explicit instruction.
- Exact command/result reporting; explicit statement of what was not verified.
- Stage prompt texts (e.g., Stage 0A through Stage 0C) may be recorded or
  referenced in `docs/PROMPTS.md` **without** including any secrets.
- Stage 0C established the two private GitHub remotes (owner mohammedawad99) and
  the `origin` configuration (**SSH** transport); commits and pushes happen only
  under explicit reviewer approval, and no authentication output or secret is
  ever recorded here.
- **Stage 1-SYNC** adopted the reviewed **common** Stage-1 specification baseline by
  **one-way synchronization** from the Police repository's locked commit
  `691280dc3219452eeff462c997714fd5bcbd9e55` (documentation only). The specification
  stages 1A–1D.1 were executed and reviewed **in the Police repository**; this
  repository did **not** perform that extraction and does not claim to have. The two
  repositories keep separate Git history, package namespaces (`mars777_thief` here),
  runtime state, and future strategy. See `SOURCES.md` and `DECISIONS.md` D15.
- **Phase 2 (Stages 2A → 2-CLOSE)** froze the architecture and authored all seven PRDs.
  Stage 2-CLOSE resolved the two final cross-contract issues **without changing any locked
  contract**: the series convention is negotiated protocol metadata (not a declaration field)
  and the declared MCP endpoint is a stable group-level ingress. **PRD-01…07 are
  APPROVED — PHASE 2 LOCKED; implementation has NOT started.**
- **Phase 3 (Stage 3A →)** is the first implementation phase. Stage 3A was driven
  **tests-first**: every domain test was written and observed failing in both repositories
  before any production module existed. It delivers only the deterministic, role-neutral
  foundation - grid configuration, coordinates, board geometry with blocked cells, the
  five-token move set, movement legality and safe move application. The project grid
  minimum is enforced by `GridConfig`, deliberately **not** by the policy-free `Board`
  geometry, per the frozen domain-layer boundary. **PRD-01…07 remain APPROVED — PHASE 2
  LOCKED**; the deterministic core is **not** complete and no protocol, networking,
  cryptography, strategy, GUI or reporting code exists.
- **Stage 3B** completed the deterministic game-rule layer tests-first: barriers,
  capture, terminal/survival, scoring and bounded scent physics. Two supervising
  corrections were applied. **JDEC-015** records a source *gap* — Appendix F fixes two
  independent MINIMUM-35 step limits but Ch 3 Table 2 defines no outcome when the
  ceiling precedes the survival threshold, so `survival_threshold <= max_moves` became
  an admissibility condition instead of an invented terminal. **C-10** records a source
  *contradiction* — Ch 4 §4.3 defines tau in [0, 0.9] yet writes the update with a lower
  clamp only, so the state domain wins and the recurrence saturates. Registers are now
  **JDEC-001…015** and **C-01…C-10**; every authoritative count is unchanged. Turn
  orchestration, protocol, networking, cryptography, strategy, GUI and reporting remain
  **not implemented**; PRD-01 stays **IN PROGRESS** and PRD-02…07 **NOT STARTED**.
- **Stage 3C** opened the application layer with the **local** turn-execution step,
  tests-first. Supervising review accepted it except for one state-ownership defect:
  `LocalTruth` carried a `barriers_placed` counter that duplicated the public board's
  barrier facts and could drift from them, and it was police-only state sitting in a
  role-neutral object. **Stage 3C-FIX1** removed it; remaining budget is derived from
  `max_barriers - len(board.blocked)`, and `STATE_OWNERSHIP.md` anti-duplication rule 2
  is satisfied. No architecture document was changed. **PRD-02 is now IN PROGRESS**
  for this one slice; the state machine, orchestrator, ports, FastMCP, networking and
  cryptography remain **not implemented**, and PRD-03…07 stay **NOT STARTED**.
- **Stage 4A** added the local protocol phase machine, tests-first, pinning the frozen
  graph literally rather than against the implementation: an exhaustive 324-pair sweep
  makes a hidden or missing edge impossible. Supervising review then found a genuine
  contradiction inside the frozen table itself - TECHNICAL_LOSS was absorbing although
  the same table makes "technical loss" an entry condition of SUBGAME_COMPLETE, tells
  the phase to "proceed per series rules", and excludes it from rule R5. **Stage
  4A-FIX1** added the single edge `TECHNICAL_LOSS -> SUBGAME_COMPLETE` and recorded the
  reasoning in `STATE_MACHINE.md` §4 as an implementation-discovered architecture
  correction - not a lecturer rule, not a source conflict, no register increment.
  Primary source agrees: Ch 3 Table 2 lists technical loss as a **sub-game** end event
  scored 0/0 beside capture and survival. TAMPERED keeps its severe, non-repairable
  status. PRD-06 remains **NOT STARTED** despite the crypto-named phases.
