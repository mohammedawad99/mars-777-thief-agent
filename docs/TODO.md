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

## In progress
**Phase 2 — PRD and architecture — is fully complete.** **Phase 3 is under way:**
Stages 3A and 3B are closed, so the deterministic game-rule layer — movement,
barriers, capture, terminal/survival, scoring and bounded scent physics — is
implemented locally and tested. Two implementation-discovered source anomalies
carry explicit provenance: **JDEC-015** (terminal source gap) and **C-10**
(scent source conflict). **Not implemented:** turn orchestration, state machine,
local application service, protocol, networking, cryptography, strategy, belief,
GUI, replay and reporting. The deterministic core is **not** complete and PRD-01
remains **IN PROGRESS**. The next stage is tracked once, under Pending.
## Pending
- [ ] Branch protection / rulesets - **blocked**: unavailable on the current GitHub
      plan for private repos (Stage 0D). Needs Pro upgrade, org, or public-at-submission.
- [ ] Example-simulator review (non-binding).
- [x] PRD-01 game logic - authored and locked; implementation **IN PROGRESS** (Stage 3A foundation only; barriers, capture, terminal/survival, scoring and scent still pending).
- [x] PRD-02 local FastMCP - authored and locked; implementation not started.
- [x] PRD-03 baseline strategy (**THIEF** role-specific) - authored and locked; implementation not started.
- [x] PRD-04 language & scent - authored and locked; implementation not started.
- [x] PRD-05 public network - authored and locked; implementation not started.
- [x] PRD-06 security & cryptography - authored and locked; implementation not started.
- [x] PRD-07 reporting, GUI, replay - authored and locked; implementation not started.
- [x] **Phase 3 — Deterministic Core Implementation** — **STARTED** (Stage 3A closed; the phase itself is **not** complete).
- [x] **Stage 3B — Deterministic Game Semantics** — **CLOSED** (barriers, capture, terminal/survival, scoring, bounded scent physics).
- [ ] **Stage 3C — Local Application / Turn Orchestration Foundation** — **NEXT AUTHORIZED; NOT STARTED.** Planned: consume the validated domain primitives; a local turn command/application service; explicit action choice (move **or** barrier); local state ownership; deterministic transition/result objects. **No** public networking and **no** cryptography.
- [ ] Collaborator (Rawey7) access - pending explicit instruction.

_Phases 1 and 2 are specification and requirements only; all seven PRDs remain
APPROVED — PHASE 2 LOCKED. Phase 3 implementation has begun with the Stage-3A
domain foundation (grid config, coordinates, board geometry, move vocabulary,
movement legality). No JSON schema, protocol, networking, cryptography,
strategy, GUI or reporting code has been implemented._
