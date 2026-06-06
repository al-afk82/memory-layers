# Memory Layers

## What this project is

R&D build. A layered memory architecture that solves context bloat — segmentation, real-time routing, cup overflow protocol, variance detection. The product that makes Echosystem work.

Collaborator: David Vogel (data scientist).

## What to load

| Task | Load these |
|------|-----------|
| Architecture decisions | `task-assignment-proposal.md` — live spec |
| Conceptual grounding | `integrated-character-model.md` — fixed base layer |
| Current state | `ACTIVE.md` at echosystem root |

## Files

| File | What it contains |
|------|-----------------|
| `task-assignment-proposal.md` | Full architecture spec — Tasks A (settled), B, B1 (variance rule settled), C (to define). Immediate next steps. |
| `integrated-character-model.md` | Defines the identity/rules/voice base that memory layers sit on top of. |

## Current state (as of 2026-05-28)

- Layer 1 segmentation: concept defined, not yet built for any topic
- Layer 2 real-time routing: design complete, not yet built
- Layer 3 cup overflow: Task A (fill monitor) settled. Task B (transfer protocol) and Task C (recognition layer) to be defined. Task B1 variance rule settled with David Vogel: same role = same variance.
- Storage schema: not yet designed

## Next action

Define Layer 1 for one topic. Build the classification prompt. This is the prerequisite for everything else.

## What does not exist yet

- Storage layer (files, database, or cortexgraph)
- Autonomous monitoring / hooks
- Session-start protocol for selective loading
- David Vogel input files — his contributions are in memory only, not in this repo
