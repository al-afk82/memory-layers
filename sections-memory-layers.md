# Section Definitions — Memory-layers

> One level below topic definitions. Defines what each section within the memory-layers topic captures.
> Good enough to surface valid errors — not final.

---

## Layer 1 — Segmentation

**Role**
Owns the structure of how topics are broken into sections. What sections exist, what they capture, how they are defined.

**Scope — belongs here**
- Topic definitions — role and scope per topic
- Section definitions — role and scope per section within a topic
- Classification prompts for routing to sections
- The topic list

**Scope — does not belong here**
- How routing happens in real time → Layer 2
- What happens when sections fill up → Layer 3
- Collaborator inputs → Collaborators

---

## Layer 2 — Routing

**Role**
Owns all real-time routing decisions and mechanisms. How incoming messages get classified and directed to the correct section while a session is live.

**Scope — belongs here**
- Stateful classifier — topic state, drift check, route change
- Session entry protocol — structured entry, declared topic
- Drift notification, adjacent counter
- Eviction trigger
- Save-before-evict, pointer design, session state file

**Scope — does not belong here**
- Section structure definitions → Layer 1
- What happens when a section reaches capacity → Layer 3
- Collaborator inputs → Collaborators

---

## Layer 3 — Overflow

**Role**
Owns what happens when a section approaches capacity. Proactive transfer, variance detection, recognition.

**Scope — belongs here**
- Fill monitor — threshold, model-dependency, selection rule
- Transfer protocol — how content moves, variance sorting
- Variance detection — variance rule, role-based variance
- Recognition layer — pointer following, thread reconstruction

**Scope — does not belong here**
- Real-time routing decisions → Layer 2
- Section structure definitions → Layer 1
- Collaborator inputs → Collaborators

---

## Collaborators

**Role**
Owns all external input that shaped memory-layers architecture. Not the decisions themselves — the inputs that informed them.

**Scope — belongs here**
- David Vogel — variance rule discussion, data science perspective
- Jake Van Clee — principles applied to memory-layers decisions
- Any other external contributor inputs

**Scope — does not belong here**
- The settled decisions → the relevant layer section
- Build progress or next steps → the relevant layer section
