# TODO - group MaRs-777 (THIEF)

> **Status: DRAFT.**
> **Purpose:** Track outstanding foundation and project tasks.
> **Authoritative source:** book v3.0.0.
> **Note:** No requirement is approved merely because this file exists.

## Done
- [x] Stage 0A - environment / tooling / Git / GitHub preflight audit.
- [x] Stage 0B - local repository foundation.
- [x] Stage 0B.1 - final evidence audit (exact future-commit validation).
- [x] Stage 0C - private GitHub repository created under mohammedawad99; **SSH** origin configured; reviewed initial commit pushed to origin/main.
- [x] Stage 0C - first GitHub Actions CI run green (ubuntu-latest + windows-latest).
- [x] Stage 1-SYNC - reviewed COMMON Stage-1 specification baseline **synchronized** from Police locked commit `691280dc…` into `docs/spec/` (documentation only; adopted, not re-extracted here). See `SOURCES.md`, `DECISIONS.md` D15.

- [x] Stage 2A - architecture freeze: 21 architecture docs + 7 PRD blueprints; 91/91 requirements architecture-mapped; red-team blocking findings resolved.
- [x] Stage 2A-R - read-only lecturer reference audit (`rmisegal/Game-P2P-Cop-Chase` @ `960499fd`); reference classified NON-BINDING; book wins on keyed Step-0 auth.
- [x] Stage 2A-R2 - attachment/chatbot reconciliation (AE-01…AE-04, secondary provenance); compatibility profiles; **JDEC-014** result→declaration reference; field matrix **77 → 75** (result 13 → 11). Zero chatbot questions pending.
- [x] Stage 2A-CLOSE - stale-baseline sweep + `result_sha256` audit; architecture/compatibility baseline committed and pushed; CI green (Ubuntu + Windows).
- [x] Stage 2B - PRD-01…04 authored in full (reviewed).
- [x] Stage 2C - PRD-05…07 authored in full (reviewed); 91/91 requirements have exactly one primary owner.
- [x] Stage 2-CLOSE - **PASS**; CLOSE-F1 (series convention = negotiated metadata, **not** a declaration field) and CLOSE-F2 (declared MCP endpoint = stable group-level ingress) resolved with **no artifact-contract change** (matrix stays **75**); all 7 PRDs **APPROVED — PHASE 2 LOCKED**; implementation **NOT STARTED**.

### Phase 3 — Deterministic Core Implementation (started)
- [x] Stage 3A - deterministic domain **foundation** (tests-first): immutable `GridConfig` (project grid minimum enforced here), immutable `Position`, immutable policy-free `Board` geometry with blocked cells, `Move` = N/S/E/W/STAY, stable `MOVE_ORDER`, destination calculation, bounds/blocked legality, deterministic `legal_moves`, typed `apply_move` failure. Role-neutral, no opponent truth, no I/O. **Supervising review PASS.**
- [x] Stage 3A-CLOSE - final audits, narrow tracking update, commit + push + CI.
- [x] Stage 3B - deterministic **game semantics** (tests-first): barrier placement, the three capture routes, terminal/survival evaluation, role-keyed scoring and bounded scent physics. **Supervising review PASS.**
- [x] Stage 3B-FIX1 - supervising correction: **JDEC-015** terminal threshold admissibility (`survival_threshold <= max_moves`) + radial scent-kernel contract hardened; `UnspecifiedTerminalError` removed.
- [x] Stage 3B-FIX2 - supervising ruling: **C-10** scent state bound vs additive update resolved as the saturating recurrence `min(0.9, max(0, (1-rho)*tau + delta))`.
- [x] Stage 3B-CLOSE - final audits, tracking finalization, commit + push + CI.
- [x] Stage 3C - local application / turn orchestration **foundation** (tests-first): `LocalTruth` (board, own position, completed steps), typed `MoveAction`/`BarrierAction`, role-specific `LocalTurnService` (police move **or** barrier; thief move only), atomic local effect application, local step accounting and max-moves exhaustion. **Supervising review PASS.**
- [x] Stage 3C-FIX1 - state-ownership correction: removed the duplicated `barriers_placed` counter from `LocalTruth`; barrier usage now has **one** authoritative representation (the public board plus the validated `BarrierQuota`), so no local count can drift.
- [x] Stage 3C-CLOSE - final audits, PRD-02 status alignment, commit + push + CI.

### Phase 4 — Protocol Foundation (started)
- [x] Stage 4A - local protocol **state machine** foundation (tests-first): the frozen 18-phase graph (15 normal + 3 fault) with **31** legal directed edges, exhaustively verified over all 324 ordered pairs; `ProtocolMachine` owns **only** the current phase; normal bootstrap via `ProtocolMachine.start()` at BOOT. **Supervising review PASS.**
- [x] Stage 4A-FIX1 - **TECHNICAL_LOSS lifecycle correction**: the frozen table made "technical loss" an entry condition of SUBGAME_COMPLETE and told the phase to "proceed per series rules", while R5 names only TAMPERED and FAILED as never returning to play - yet it listed no successor. One edge added, `TECHNICAL_LOSS -> SUBGAME_COMPLETE`, recorded in `STATE_MACHINE.md` §4 as an implementation-discovered architecture correction. TAMPERED and FAILED stay absorbing.
- [x] Stage 4A-CLOSE - final graph/ownership audit, bootstrap guard, tracking, commit + push + CI.
- [x] Stage 4B - protocol event / **transition evidence** foundation (tests-first): every successful `advance()` now returns one immutable `TransitionResult` carrying a `TransitionEvidence` of exactly `source_phase` + `target_phase`, per R7 and `PROTOCOL_TIMELINE.md` event 10 (transmitted "phase transition", persisted "—", hashed "—"). No transition-signal vocabulary is frozen anywhere, so **no event enum was invented**; there is no evidence-less transition path and no compatibility shim. **Supervising review PASS.**
- [x] Stage 4B-FIX1 - supervising corrections: (a) `TransitionEvidence` is now **valid by construction** - the pair must be an edge of the single `_ALLOWED` graph, so a record of a step R1/R5 forbid (e.g. `COMMIT_SENT -> REVEAL`, `TAMPERED -> SUBGAME_COMPLETE`) cannot be built; 31 legal pairs constructible, 293 illegal pairs and all 18 self-loops rejected. The replay corruption boundary moved forward to the constructor and negative replay coverage was **extended** (duplicated record, out-of-position record) rather than weakened. (b) A reported "153-line" file was reconciled as a **cross-repo semantic-diff count**, not physical LOC; the repository-wide audit proves max **150** and **0** files over the limit.
- [x] Stage 4B-CLOSE - final evidence/graph invariant audit, repository-wide LOC proof, tracking finalization, commit + push + CI.

## In progress
**Phase 2 — PRD and architecture — is fully complete.** **Phases 3 and 4 are under
way:** the deterministic game-rule layer (3A/3B), the local turn-execution step
(3C), the local protocol phase machine (4A) and its transition evidence (4B)
exist and are tested. The phase machine enforces order only — the phases named
COMMIT_SENT, ACKNOWLEDGED, REVEAL and FINAL_AUDIT carry no cryptography, message
bodies or transport, and the machine never applies a local effect. Transition
evidence is **structurally valid, not authenticated**: it supports ordered
**phase-path** replay only, never game-state, movement, barrier, score, scent,
commitment, nonce, network-message, official-artifact or complete-game replay.
**Not implemented:** orchestrator, application ports, FastMCP, networking,
cryptography, logger/replay persistence, JSON artifacts, strategy, belief, GUI
and reporting. PRD-01 and PRD-02 remain **IN PROGRESS**; the next stage is
tracked once, under Pending.
## Pending
- [ ] Branch protection / rulesets - **blocked**: unavailable on the current GitHub
      plan for private repos (Stage 0D). Needs Pro upgrade, org, or public-at-submission.
- [ ] Example-simulator review (non-binding).
- [x] PRD-01 game logic - authored and locked; implementation **IN PROGRESS** (Stage 3A foundation only; barriers, capture, terminal/survival, scoring and scent still pending).
- [x] PRD-02 local FastMCP - authored and locked; implementation **IN PROGRESS** (Stage 3C local turn foundation only; state machine, orchestrator, ports, FastMCP and runtime composition still pending).
- [x] PRD-03 baseline strategy (**THIEF** role-specific) - authored and locked; implementation not started.
- [x] PRD-04 language & scent - authored and locked; implementation not started.
- [x] PRD-05 public network - authored and locked; implementation not started.
- [x] PRD-06 security & cryptography - authored and locked; implementation not started.
- [x] PRD-07 reporting, GUI, replay - authored and locked; implementation not started.
- [x] **Phase 3 — Deterministic Core Implementation** — **STARTED** (Stage 3A closed; the phase itself is **not** complete).
- [x] **Stage 3B — Deterministic Game Semantics** — **CLOSED** (barriers, capture, terminal/survival, scoring, bounded scent physics).
- [x] **Stage 3C — Local Application / Turn Orchestration Foundation** — **CLOSED.**
- [x] **Stage 4A — Local Protocol State Machine Foundation** — **CLOSED.**
- [x] **Stage 4B — Protocol Event / Transition Evidence Foundation** — **CLOSED** (deterministic per-transition evidence, valid by construction against the single frozen graph; phase-path replay only). No event enum was invented: no transition-signal vocabulary is frozen in any source or architecture document.
- [ ] **Stage 4C — Local Orchestrator / Protocol Guard Foundation** — **NEXT AUTHORIZED; NOT STARTED.** Planned: introduce the frozen `app.orchestrator` responsibility; own the sub-game index/cursor where the architecture assigns it; consume `TransitionResult`/evidence; coordinate caller-supplied branch/guard facts without duplicating their authoritative subsystem state; establish deterministic series/sub-game control flow; prepare the seam for `LocalTurnService` and later protocol adapters. **Not** in 4C unless separately authorized: FastMCP/network I/O, commitment hashing, nonce generation, signatures/HMAC, canonical sealed payloads, official artifact persistence, strategy, GUI/replay/reporting.
- [ ] Collaborator (Rawey7) access - pending explicit instruction.

_Phases 1 and 2 are specification and requirements only; all seven PRDs remain
APPROVED — PHASE 2 LOCKED. Phase 3 implementation has begun with the Stage-3A
domain foundation (grid config, coordinates, board geometry, move vocabulary,
movement legality). No JSON schema, protocol, networking, cryptography,
strategy, GUI or reporting code has been implemented._
