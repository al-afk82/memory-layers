# Task Assignment Proposal — Memory Layers Build

## What we're building

A layered memory architecture that solves context bloat and enables real-time classification and routing of information into the correct memory section as a conversation happens.

**Layer 1 — Segmentation:** Topics broken into sections like paragraphs. Load the section, not the whole topic.
**Layer 2 — Real-time routing:** Live classifier assigns incoming information to the correct section continuously.
**Layer 3 — Cup overflow protocol:** Fill monitor watches each section. Before capacity is reached, content transfers to a new section with a specific arrangement. A recognition layer reads what the user is referencing and pulls from the right cup. Nothing is lost. Transfer is proactive, not reactive.

Layer 3 breaks into three discrete tasks:

**Task A — Fill monitor** ✓ SETTLED
- Threshold: 85% of the active model's context window, calculated dynamically at session start — not a fixed token number
- Model-dependency: reads the active model's reported context limit and calculates 85% from that automatically
- Variable thresholds: 85% is the global default; sections that run alongside heavy conversation can override to 70% via section metadata
- Selection rule: when transfer triggers, move least recently accessed content first — not oldest by date, but least recently referenced

**Task B — Transfer protocol** — to be defined
- Moves content to a new section before overflow, with a specific arrangement that preserves findability
- Must write a pointer in the source section when content moves — so the recognition layer can follow the chain across cups
- Does not pour blindly — reads the section and sorts by variance as it transfers. Similar variances group together. Each distinct variance becomes its own layer.

**Task B1 — Variance detection** — to be defined
- Sits inside the transfer protocol. When a transfer is triggered, variance detection reads the section and identifies which entries are the same variance and which are distinct.
- Each distinct variance becomes its own new layer during transfer — the section splits with meaning, not just by volume.
- Uses the same classification logic as Layer 2 — variance detection is not a separate engine, it's Layer 2 applied to existing content rather than incoming content.
- When the user references something mid-conversation, the recognition layer uses variance detection to identify which specific variance is being referenced and loads only that — not the whole section.
- **Variance rule — SETTLED (David Vogel, 2026-05-28):** Two entries are the same variance if they share the same role. Different role = different variance = different layer. Roles are stable, they don't grow. The content within a role grows. Variance detection asks one question: what role does this entry play?

**Task C — Recognition layer** — to be defined
- Reads what the user is referencing right now and knows which cup to pull from
- Follows pointers across cups to reconstruct full threads when understanding spans multiple sections

**Known future problem — cross-cup thread reconstruction**
When a conversation thread is split across multiple cups, the recognition layer follows pointers to reconstruct it. At scale, chains can get long and expensive to follow. Not a blocker now — revisit when the system is live and the pattern emerges.

---

## What Claude does well — and where to use it

### 1. Classification
**What it is:** Given a piece of information, identify what topic and section it belongs to.
**Where to use it:** Layer 2 — the real-time routing protocol. Claude can read incoming content and assign it to the correct section with high accuracy.
**Task format:** "Here is a piece of conversation. What topic does it belong to? What section within that topic?"

---

### 2. Protocol design
**What it is:** Taking a concept or goal and designing a repeatable structured process for it.
**Where to use it:** Building the per-topic layer creation protocol. Claude can take a new subject area and draft the section structure for it.
**Task format:** "Here is a new topic: [X]. Design the sections this topic should be broken into and define what each section captures."

---

### 3. Schema design
**What it is:** Defining the structure of how information gets stored — what fields, what format, what relationships.
**Where to use it:** Designing the memory file format for each layer so that recall is precise and misfiling is minimised.
**Task format:** "Design a schema for storing [topic] memory in a way that supports section-level recall."

---

### 4. Misfiling detection
**What it is:** Reviewing classified memory and identifying items that were assigned to the wrong section or belong to multiple sections.
**Where to use it:** Quality layer on top of Layer 2 — periodic review of what got filed and whether it landed correctly.
**Task format:** "Review this memory section. Flag anything that is misfiled or ambiguous."

---

### 5. Recall
**What it is:** Given a current task or question, identify which memory section is relevant and surface only that.
**Where to use it:** Every session start — instead of loading everything, Claude loads the section relevant to the current task.
**Task format:** "The current task is [X]. Which memory sections are relevant? Load only those."

---

## Implementation mechanics — borrowed from Hermes (reference: data-room/scoped/)

These three decisions are borrowed from the Hermes architecture after a comparative scan. They are implementation details, not architectural changes. David's model stays intact.

**1. Inject retrieved context into the user message, not the system prompt**
Hermes injects memory context into the user message at API-call time. Reason: the system prompt is cached. Injecting there would invalidate the cache on every retrieval. Injecting into the user message preserves caching and keeps retrieval cost low.
When Task C (recognition layer) pulls from a cup and surfaces it, the output goes into the user message wrapped in fences.

**2. Context fencing**
Injected blocks must be wrapped in `<memory-context>` tags so the system knows what is retrieved context versus what is actual user input. A scrubber strips these tags from message history before re-processing — without it, injected blocks reappear in subsequent turns and pollute the conversation.
Both the fence tags and the scrubber need to exist before any injection goes live.

**3. Session routing**
Before anything is written to a layer, the system needs an explicit decision about which bucket this turn belongs to. Hermes solves this with four strategies (per-directory, per-session, per-repo, global). Memory-layers needs its own version of this — likely per-topic, determined by the Layer 2 classifier.
This decision must be made before Layer 1 is built for a topic, because the routing target must exist before the classifier can route to it.

---

## What Claude cannot do alone

| Gap | What's needed |
|-----|--------------|
| Persistent memory across sessions | A storage layer outside the context window — files, database, or a system like cortexgraph |
| Autonomous monitoring | A trigger mechanism — hooks, cron jobs, or session-start protocols that fire automatically |
| Self-classification without prompting | Either a hook that runs on every message, or Alec manually triggering classification at key moments |

---

## Immediate next steps

1. **Define Layer 1 for one topic** — pick one active topic (e.g. memory layers itself) and map out its sections together. This becomes the template.
2. **Build the classification prompt** — a single reusable prompt Claude can run on any piece of information to assign it to topic + section.
3. **Design the storage schema** — what does a memory section file look like? What fields does it need to support precise recall?
4. **Wire up a session-start protocol** — at the start of each session, Claude loads only the sections relevant to the current task rather than everything.

---

## The order matters

Layer 1 (segmentation) must exist before Layer 2 (routing) can work. You cannot route to sections that haven't been defined. Build the section structure first, then build the classifier that assigns to it.
