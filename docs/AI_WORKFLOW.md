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
