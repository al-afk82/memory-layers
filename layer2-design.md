# Layer 2 — Real-time Routing Design

> Live spec. Updated as decisions are settled.
> All decisions in this file are interception — harness instructions, not automation.

---

## What Layer 2 does

Real-time routing. As a conversation happens, incoming messages are classified and routed to the correct topic section. Nothing is loaded blindly. Nothing accumulates.

---

## The stateful classifier

The core mechanism. Three blocks.

**TOPIC STATE**
At session start: read the declared topic. Record it as `[current topic]`. Carry it forward. Do not re-derive it each turn.

**DRIFT CHECK — runs before every response**
Compare the incoming message against `[current topic]`.
- Message is consistent with `[current topic]`: proceed. No change.
- Message is adjacent — touches another topic but `[current topic]` still primary: increment adjacent counter. No route change.
- Message's primary subject is no longer `[current topic]`: drift confirmed.

**ROUTE CHANGE — runs on drift confirmed only**
1. Update `[current topic]` to the new topic.
2. Load that topic's memory section.
3. Eviction fires on the departing section (see below).

---

## Topic identification — adjacent signals

When a message is adjacent, the drift check must name the emerging topic — not just flag that something is off.

The classifier compares the adjacent message against the topic list. Each topic has a defined role and scope. The message must satisfy role AND fall within scope to match. The comparison returns the closest match.

If no topic matches clearly: return "outside known set." Do not force a weak match.

Topic definitions live in `topic-definitions.md`.

---

## Drift notification

Fires when the adjacent counter hits threshold N.

Claude surfaces: "This is moving toward [detected topic]. New session?"

- User says yes → session closes, new session opens with [detected topic] declared
- User says no → counter resets, current topic holds

The user's response is the declaration. Claude does not route silently.

Threshold N is a tuning decision — not a design decision. Pick a number, test it, adjust it.

---

## Session entry protocol

**Structured entry only — version 1.**

- Topic is always declared explicitly at session start
- One declared topic per session start
- Blank openers are not valid entry points
- If two topics are named at once, the first is accepted; the second enters through the drift mechanism

Unstructured opener support is version 2.

---

## Eviction trigger — SETTLED

**One role: confirmed topic exit.**

When the classifier confirms a topic shift (route change fires), the departing topic's section is evicted from context.

- Eviction is coupled to the classifier by design
- If the user does not declare a topic exit, the section stays loaded — this is a protocol violation, not a system failure
- The system is not responsible for user discipline failures

Fill monitor pressure (approaching context capacity) is handled by Layer 3 — the overflow protocol. Not by the eviction trigger. One mechanism, one role.

---

## Save-before-evict — SETTLED

The JSONL transcript already writes continuously. Every exchange is captured in real time. The save step is a reference operation, not a write operation.

**Sequence:**
1. Topic exit confirmed → eviction fires
2. Record JSONL path + message range (start index when topic became active, end index at eviction)
3. Leave pointer in context
4. Section removed from context

Nothing is rewritten. The content already exists in the file.

---

## Pointer design — SETTLED

**Format:** `[session-id]:[start-message-index]:[end-message-index]`

Example: `00acf61b:42:87`

**Form in context** — fenced block, consistent with existing architecture:

```
<memory-pointer>
topic: [topic name]
session: [session-id]
range: [start]:[end]
</memory-pointer>
```

**Creation:** Assembled at eviction from session state file (see below).

**Reading:** Task C resolves session ID → file path, slices JSONL by message range, surfaces full content. Task C is not yet designed — pointer format is forward compatible.

---

## Session state file — SETTLED

All classifier state lives in a file. Updated every turn. Context compression cannot touch it.

**File:** `session-state.md` (in project folder)

```
current_topic: [topic name]
topic_start_index: [n]
current_message_index: [n]
adjacent_counter: [n]
```

The classifier reads from this file each turn, not from context memory. This closes both the pointer counter persistence risk and the adjacency counter persistence crack.

---

## Open questions

| # | Question | Status |
|---|----------|--------|
| 1 | Routing granularity — topic-first vs direct-to-section | Settled — stateful classifier with structured entry |
| 2 | Eviction trigger — every turn vs on pressure vs on topic exit | Settled — confirmed topic exit only |
| 3 | Pointer format — minimum vs extended | Settled — session-id:start:end, fenced block |
| — | Save-before-evict step | Settled — reference operation, JSONL path + message range |
| — | Counter persistence | Settled — session state file, updated every turn |
