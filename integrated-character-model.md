# Integrated Character Model

Alec's term for the full package that defines who the AI is and how it behaves. The fixed layer that makes the AI behave consistently regardless of what the user throws at it.

## What it covers

- **Identity** — who the persona is, where its perspective comes from
- **Rules** — behavioral contract, what it always does and never does
- **Voice** — how it speaks, register, sentence structure
- **Context guidelines** — what loads, when, at what budget
- **Intake/outputs** — how user-specific knowledge flows in and out

## Why it matters

**Without the structure:** Claude loads context in whatever order seems relevant, identity and voice get compressed when the window gets tight, and by mid-session the outputs start drifting. Memory files get loaded but compete with everything else for influence.

**With the structure:** Identity loads first, in full, before anything else. It does not compress. So when memory files load — Jonathan, Delta, the pitch feedback, the no-hyphens rule — they land on top of a stable base. Claude already knows who Alec is before it reads what Alec has been doing.

The practical effect: memory recall stops being additive noise and starts being interpreted through a fixed lens. "Jonathan said the pitch is too complex" means something different when Claude already knows Alec is pre-revenue, solo, and the strategy is to find collaborators not investors. Without the identity loaded first, that memory is just a data point. With it, Claude knows what to do with it.

## Rule 0

Memory can be loaded correctly and still ignored if Claude drifts toward the easy response. Rule 0 is the check that forces recalled memory to actually influence the output, not just sit in context.

## Relationship to memory layers

Identity is the fixed base. Memory layers sit on top of it. The recognition layer doesn't just find relevant content — it finds relevant content and runs it through the identity lens before it influences output. The memory layers system only works correctly when identity loads first.
