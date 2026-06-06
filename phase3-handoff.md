# Phase 3 Handoff — Layer 3: Cup Overflow Protocol

> Scope: define and build the cup overflow system — transfer protocol (Task B + B1) and recognition layer (Task C).
> Last updated: 2026-05-29
> Status: skeleton — Task B, B1, and C require David Vogel input before acceptance criteria can be finalised.

---

## What is settled — do not re-litigate

**Task A — Fill monitor**
- Threshold: 85% of active model's context window, calculated dynamically at session start
- Variable threshold: 70% for sections running alongside heavy conversation — set via section metadata
- Selection rule on transfer trigger: move least recently accessed content first (not oldest by date)

**Variance rule (Task B1)**
- Two entries are the same variance if they share the same role
- Different role = different variance = different layer
- Roles are stable — they do not grow. Content within a role grows.
- Variance detection applies Layer 2 classification logic to existing content, not a separate engine

**Injection mechanics (from Hermes — already written into task-assignment-proposal.md)**
- Retrieved context injects into the user message, not the system prompt
- Injected blocks use `<memory-context>` fencing tags
- A scrubber strips these tags from message history before re-processing
- Both fence tags and scrubber must exist before any injection goes live

---

## Files in play

| File | Role |
|------|------|
| `task-assignment-proposal.md` | Live spec — source of truth for all settled decisions |
| `phase3-handoff.md` | This file — Phase 3 work order |
| `integrated-character-model.md` | Fixed base layer — read before any task redefines identity-adjacent behaviour |
| `protocol/session-start.md` | Selective loading protocol — must stay consistent with whatever Task C builds |

---

## Risks — read before starting any task

1. **Transfer mid-conversation** — overflow can trigger while the user is mid-thread. Transfer must not interrupt the current turn. Trigger must be async or deferred to turn boundary.

2. **Pointer chain length** — a section split many times produces a long pointer chain. Task C has to follow this chain to reconstruct a thread. At scale this gets expensive. Not a blocker now — but the pointer format Task B defines must be designed for chain traversal, not just single-hop lookups.

3. **Variance misclassification on transfer** — Task B1 uses the Layer 2 classifier on existing content. If Layer 2 has low confidence on an entry, B1 will inherit that error and split the section incorrectly. Need a confidence floor before B1 acts on a classification.

4. **Cross-topic bleed** — if Layer 1 section boundaries are loose, two distinct topics can accumulate in the same section. When B1 runs variance detection, it may surface this bleed as multiple variances rather than a segmentation error. B1 is not responsible for fixing segmentation — it must flag this as a boundary error, not silently split.

5. **Scrubber timing** — the `<memory-context>` scrubber must run before message history is re-submitted to the model. If it runs after, leaked tags reappear in subsequent turns. The scrubber's position in the request pipeline is not yet defined.

---

## Task B — Transfer protocol

**What it does:** Moves content from a full section to a new section before overflow, preserving findability and variance groupings.

**Acceptance criteria:**
- [ ] Transfer triggers at the Task A threshold (85% or override value)
- [ ] Content is read, variance-detected (via Task B1), and sorted by variance before writing
- [ ] Each distinct variance writes to its own destination section
- [ ] Source section retains a pointer to each destination section — format TBD (see open question)
- [ ] Transfer completes without interrupting the current conversation turn
- [ ] No content is lost — entry count before transfer equals entry count across all destination sections after

**Open questions — David Vogel input needed:**
- What is the pointer format? (inline link, metadata field, separate pointer file?)
- Does the source section retain the content after transfer, or does it become a pointer-only stub?
- When multiple variances transfer, do they all go to one new section or separate new sections per variance?

---

## Task B1 — Variance detection

**What it does:** Sits inside Task B. Before content moves, reads the section and identifies which entries share a role (same variance) and which do not. Groups the section by variance so Task B can split intelligently.

**Acceptance criteria:**
- [ ] For any section, produces a list of entries grouped by role
- [ ] Entries the classifier cannot assign with confidence above floor value are flagged, not silently assigned
- [ ] Entries that appear to belong to two roles are flagged as ambiguous, not split or duplicated
- [ ] Cross-topic bleed (two distinct topics in one section) is reported as a boundary error, not processed as a normal variance split
- [ ] Confidence floor value: TBD — David Vogel input needed

**Open questions — David Vogel input needed:**
- What confidence floor triggers a flag vs. a silent assignment?
- Ambiguous entries (two roles): defer, flag, or assign to the higher-confidence role?

---

## Task C — Recognition layer

**What it does:** Reads what the user is referencing mid-conversation and identifies which section (or chain of sections) holds the relevant content. Surfaces only that — nothing else.

**Acceptance criteria:**
- [ ] Given a user message, identifies the topic and section being referenced
- [ ] If the section has been transferred, follows the pointer chain to find current location
- [ ] Returns the relevant content fenced in `<memory-context>` tags, ready for injection
- [ ] Does not load entire topics — loads the minimum section that satisfies the reference
- [ ] Pointer chain traversal has a maximum depth limit — TBD (guards against infinite loops on corrupted chains)

**Open questions — David Vogel input needed:**
- How does the recognition layer handle ambiguous references (user message could reference two sections)?
- What triggers recognition — every turn, or only when a reference signal is detected?
- Maximum pointer chain depth: what is the hard limit before fallback behaviour?

---

## Stop condition

This phase is complete when:
1. Task B, B1, and C each pass their acceptance criteria in a test session
2. A section has been filled to threshold, transferred, and successfully recalled via Task C without data loss
3. Pointer chains have been traversed successfully across at least two hops
4. Scrubber has been confirmed functional — no `<memory-context>` tags appearing in message history after injection

Stop here. Do not begin storage schema design or session-start protocol updates in this phase. Those are Phase 4.

---

## What this file needs before it is executable

Two conversations with David Vogel — one per question cluster:

1. **Transfer protocol questions** (Task B open questions above)
2. **Confidence floor and ambiguity handling** (Task B1 and Task C open questions above)

When David answers, fill the open questions sections and mark each acceptance criterion with its final spec. The document becomes executable at that point.
