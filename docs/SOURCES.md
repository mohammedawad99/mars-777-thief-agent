# Sources & Source-of-Truth - group MaRs-777

**Status: DRAFT (foundation).**

## Authoritative document

- **Title:** Distributed Police-Thief Peer-to-Peer - Project Book
- **Version:** 3.0.0
- **Pages:** 160
- **Expected SHA-256:** `7c9e1d7527582c3aef9afd71709981cea50ea60b8fabefe85efccab0a5fdd02e`
- **Local (git-ignored) copy:** `.project-spec/police_thief_p2p.pdf`
- **Parent source:** `../references/police_thief_p2p.pdf`

The local copy under `.project-spec/` must have the **same SHA-256** as the
parent source. It is a static, ignored, read-only reference - never runtime
state, never committed.

## Source hierarchy

1. Book v3.0.0.
2. Appendix E - mandatory rules, prohibitions, sanctions, recommendations.
3. Appendix F - mandatory numeric parameters and status definitions.
4. Moodle instructions from the lecturer.
5. Professional software-submission guidelines.
6. Example simulator - non-binding reference only.

## Warning

**No rule, numeric value, status, or JSON schema may be reconstructed from
memory.** Every such element is extracted from the book with a page/section
citation.

## Synchronization provenance (Stage 1-SYNC)

The reviewed **common** Stage-1 specification baseline in `docs/spec/` was **not
independently extracted by this repository**. It was **synchronized into this THIEF
repository** from the counterpart Police repository after supervising review:

| Item | Value |
|---|---|
| Source repository | `mohammedawad99/mars-777-police-agent` |
| Locked source commit | `691280dc3219452eeff462c997714fd5bcbd9e55` |
| Source commit subject | `docs: mark stage 1 specification locked` |
| Direction | Police (read-only source) → Thief (destination). One-way; no shared state. |
| Scope | Documentation only — no code, runtime, dependency, CI, or Git history was copied. |

**Authority:** the **project book remains the authoritative source**. The Police
commit is the *reviewed project extraction/contract baseline*, **not** a replacement
for the book. Where this documentation and the book disagree, the **book governs**
and the conflict must be recorded in `CONFLICT_REGISTER.md`.

**Note on the later Police metadata commit.** After this synchronization was
prepared, Police received a **metadata-only** correction commit
(`7563e09f65671bbe3901229f3769a46e2a45c74b`) that fixed a stale requirement-count
statement in its own `SOURCES.md` (79 → the correct **91**) and updated its
`DECISIONS.md` D12 Git-transport wording to SSH. That commit **did not alter any
locked specification semantics**, so the common specification content in `docs/spec/`
here remains sourced from — and byte-identical to — commit `691280dc…`. The
specification was **not** re-synchronized from the newer metadata commit.

Stages 1A–1D.1 (extraction, cross-audit, JSON contracts, cryptographic/reporting
corrections) were executed in the Police repository and reviewed there; this
repository **adopted** the reviewed result. The two repositories remain fully
independent (separate Git history, package namespace, runtime, and strategy).

## Extraction status (common baseline, adopted)

The full 160-page extraction (specification-only, no implementation) lives under
`docs/spec/`:

- `AUTHORITY_RULES.md` - reading conventions, hierarchy, citation format.
- `PAGE_COVERAGE.md` - all 160 PDF pages accounted for.
- `REQUIREMENT_CATALOG.md` - **91** source-cited requirements across 18 domains
  (MUST 76 · MUST NOT 9 · SHOULD 4 · MAY 2), verified by row count.
- `APPENDIX_E_CROSSWALK.md` - all 55 mandatory entries mapped.
- `APPENDIX_F_NUMERIC_INVENTORY.md` - every binding numeric value.
- `HIGH_RISK_REQUIREMENTS.md` - compliance-risk audit.
- `JSON_SOURCE_MAP.md` - sources for the four JSON docs (no schema yet; Stage 1C).

Plus `CONFLICT_REGISTER.md` and `REQUIREMENTS_TRACEABILITY.md` (in `docs/`).
All of it was independently cross-audited (Stage 1B) and **accepted by supervising
review (PASS)** as the approved specification baseline. Numeric values are governed
by **Appendix F**; the four JSON contracts were built and reviewed in
**Stage 1C/1D/1D.1** (now **LOCKED**) with their field/key/nesting details resolved.
