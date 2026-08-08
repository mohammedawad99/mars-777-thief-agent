# Project Plan - group MaRs-777 (THIEF)

> **Status: DRAFT.**
> **Purpose:** Sequence the work from foundation to a compliant, competitive
> THIEF agent.
> **Authoritative source:** book v3.0.0 (`.project-spec/police_thief_p2p.pdf`);
> Appendix E (rules/sanctions); Appendix F (numeric values).
> **To extract later:** the concrete milestones and acceptance criteria implied
> by the book once the full 160-page extraction is done.
> **Note:** No requirement is approved merely because this file exists.

## Phases (provisional)

- **Stage 0A - Environment audit.** Complete.
- **Stage 0B - Local foundation.** Complete (incl. 0B.1 evidence audit).
- **Stage 0C - Private remote, reviewed initial commit + push, CI verified.** Complete.
- **Stage 1 - Specification baseline.** **Adopted — REVIEWED / APPROVED / LOCKED.**
  The common Stage-1 baseline (extraction, Appendix-E/F corrections, requirement
  traceability, conflict resolutions, four JSON contracts, cryptographic-authentication
  distinctions, reporting contract) was **synchronized into this repository** from the
  Police locked source commit `691280dc3219452eeff462c997714fd5bcbd9e55` after
  supervising review — **not independently re-extracted here** (see `SOURCES.md` →
  *Synchronization provenance*, and `DECISIONS.md` D15). Lives in `docs/spec/`.
  **This synchronization is itself pending supervising review before it is committed.**
  Implementation: **NOT STARTED**.
- **Stage 2 onwards (PRD/architecture)** begins only **after** this synchronization is
  reviewed. No substantive PRD work has begun.
- **Stage 2A - Architecture freeze + PRD blueprints.** Complete (documentation only): 21 architecture documents in `docs/architecture/` (system topology, dependency layering, state ownership, state machine, error model, 18 ports, data/privacy flow, concurrency, config, artifacts, strategy seam, LLM boundary, observability, 12 test layers, security threat model, four quality gates, traceability, red-team, sync matrix) + seven PRD **blueprints**. All 91 requirements architecture-mapped; 11 blocking red-team findings resolved.
- **Stage 2A-R - Lecturer reference audit.** Complete: read-only audit of `rmisegal/Game-P2P-Cop-Chase` @ `960499fd` (v3.0.0). Its bundled book PDF hash matches ours exactly. Reference classified **NON-BINDING**; its unkeyed `SHA256(terms|nonce)` "signature" does **not** satisfy the book's keyed pre-supplied-key requirement (book wins). Chatbot question pack produced.
- **Stage 2A-R2 - Final reconciliation.** Complete: attachment evidence AE-01…AE-04 recorded as **secondary provenance**; all chatbot items closed (zero pending). Compatibility profiles defined (STRICT / REFERENCE / ATTACHMENT). One authorized Stage-1 **project-contract** correction: **JDEC-014** — the result **references** the declaration instead of duplicating static metadata (four-artifact-set self-containment), so the field matrix moved **77 → 75** (result 13 → 11). No requirement, Appendix E/F value, filename, or conflict changed.
- **Stage 2A-CLOSE - Consistency sweep + commit.** Stale-baseline sweep, non-self-referential `result_sha256` audit, symmetry re-verification, then commit + push + CI.
- **Stage 2B - PRD-01…04 authored in full.** Complete and reviewed (documentation only).
- **Stage 2C - PRD-05…07 authored in full.** Complete and reviewed; all 91 requirements given exactly one primary owner (PRD-01 15 / PRD-02 11 / PRD-03 3 / PRD-04 10 / PRD-05 2 / PRD-06 14 / PRD-07 24 / EXTERNAL-SUBMISSION 12).
- **Stage 2-CLOSE - PASS.** Resolved CLOSE-F1 (series convention is negotiated protocol metadata, **not** a declaration field — matrix stays **75**) and CLOSE-F2 (declared MCP endpoint is a **stable group-level ingress**, 1/team, static whole-series). **All seven PRDs are APPROVED — PHASE 2 LOCKED.** **Implementation: NOT STARTED.**
- **Phase 3 - Deterministic core implementation.** Next authorized phase; begins only after Phase-2 closure review.
- **Stage 2 - Game logic & movement legality.** Pending implementation (PRD-01, locked).
- **Stage 3 - Local FastMCP protocol.** Pending (PRD-02).
- **Stage 4 - Baseline strategy.** Pending (PRD-03).
- **Stage 5 - Language & scent.** Pending (PRD-04).
- **Stage 6 - Public network.** Pending (PRD-05).
- **Stage 7 - Security & cryptography.** Pending (PRD-06).
- **Stage 8 - Reporting, GUI, replay.** Pending (PRD-07).
- **Stage 9 - Submission delivery.** Pending.
