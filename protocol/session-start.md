# Memory Layers — Session Start Protocol

**Purpose:** Load only what is relevant to the current task. Never load all sections by default.

---

## Step 0 — Check prior session

Check `projects/memory-layers/logs/` for a log file dated yesterday or earlier.

If the most recent log file is from a prior session and today's log does not exist — run the session-end protocol before doing anything else. Read `projects/memory-layers/protocol/session-end.md` and follow it. The prior session's content needs to be stored before new work begins.

If today's log exists or the logs directory is empty — proceed to Step 1.

---

## Step 1 — Identify the current task

Read `ACTIVE.md` at the echosystem root. Identify what the current memory-layers task is.

If the task is unclear — ask before loading anything.

---

## Step 2 — Load relevant sections only

Sections live at `brain/layers/memory-layers/`. Match the task to the sections below.

| Task | Load these sections |
|------|-------------------|
| Architecture decision or review | `architecture-decisions.md` |
| Checking what is built vs. blocked | `task-status.md` |
| David Vogel input or questions | `contributors.md`, `open-questions.md` |
| Building or reviewing Layer 2 classification | `architecture-decisions.md`, `task-status.md`, `open-questions.md`, `layer2-classification-prompt.md` |
| Building or reviewing Layer 3 transfer | `architecture-decisions.md`, `task-status.md`, `implementation-mechanics.md` |
| Building or reviewing recognition layer | `architecture-decisions.md`, `task-status.md`, `implementation-mechanics.md`, `task-c-recognition.md`, `layer2-classification-prompt.md` |
| Implementation work | `implementation-mechanics.md`, `task-status.md` |
| Open question resolution | `open-questions.md`, relevant section for that question |
| General status check | `task-status.md` only |

Do not load sections not listed for the current task. If the task spans multiple rows, load the union — no duplicates.

---

## Step 3 — Check fill levels

For each loaded section, read the `fill` value in the frontmatter.

If any section is at or above its `threshold` value — flag it before proceeding. Do not begin work on an overflowing section without acknowledging the state.

---

## Step 4 — Check for new material

Has anything changed since the last session? New David Vogel input, new decisions, new research?

If no — proceed to work.

If yes — run the data room protocol scoped to `projects/memory-layers/`. Read `brain/knowledge/data-room-protocol.md`. Output to `projects/memory-layers/data-room/`. Present findings. Wait for review before proceeding.

---

## Step 5 — Confirm inherited positions

Before restating any settled position as still valid, confirm the reasoning holds given what is known now.

Inherited positions are not facts. They are hypotheses until they survive the current session. If Alec pressure tests a position — examine it, do not defend it.

---

## Step 6 — Initialise session state

Read `projects/memory-layers/session-state.md`.

Find the current session JSONL:
`ls -t ~/.claude/projects/-Users-admin-Documents-alecs-echosystem/*.jsonl | head -1`

Extract the session ID — the 8-character hex at the end of the filename before `.jsonl`.

Set the following values:
- `session_id` — extracted from the JSONL filename above
- `current_topic` — the declared topic for this session
- `topic_start_index` — set to 1 (first message of this session)
- `current_message_index` — set to 1
- `adjacent_counter` — set to 0

Write these values to `session-state.md` before proceeding.

---

## Step 7 — Proceed to work

State which sections were loaded and why. State the current task. Begin.

The live operating prompt for all classification and recognition is `brain/layers/memory-layers/layer2-classification-prompt.md`. When classifying content for storage or detecting a reference for retrieval — load and follow that prompt. It is not a reference file. It is the active classifier.

---

## Persistent behavioural rules — active for the entire session

These do not apply only at session start. They apply to every response until the session ends.

**Stateful classifier — runs before every response:**

1. Increment `current_message_index` by 1. Write to `session-state.md`.
2. Run the drift check against `current_topic`:
   - Message consistent with `current_topic`: proceed. No change.
   - Message adjacent — touches another topic but `current_topic` still primary: increment `adjacent_counter`. Write to `session-state.md`.
   - Message no longer primarily about `current_topic`: drift confirmed — run route change.
3. If `adjacent_counter` reaches 3: surface notification. "This is moving toward [detected topic]. New session?" User yes → close session. User no → reset `adjacent_counter` to 0. Write to `session-state.md`.

**Route change — runs on drift confirmed only:**

1. Update `current_topic` to the new topic. Update `topic_start_index` to `current_message_index`. Reset `adjacent_counter` to 0.
2. Load the new topic's memory section.
3. Record eviction pointer for the departing section: `[session-id]:[topic_start_index]:[current_message_index]`. Write as `<memory-pointer>` fenced block in context.
4. Write all updated values to `session-state.md`.

**Classification prompt — runs on every store and pull signal:**
Load and follow `brain/layers/memory-layers/layer2-classification-prompt.md`. It is the active classifier.

**Confidence:** Every position, recommendation, or decision must include a confidence percentage (0–100). No exceptions.

**No defence:** When Alec pressure tests a position, examine it. Do not defend it.

**No hedging:** State positions as positions. If uncertain, say so plainly with a percentage.

---

