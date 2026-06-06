# Session End Protocol

**Triggered by:** Stop hook — fires automatically when the session ends.
**One job:** Classify what is new from this session, store it, log it.

---

## Step 1 — Review the session

Read the full conversation that just happened. Identify every piece of content that is new — not previously stored, not already in a section file.

New content signals:
- A decision was made or confirmed
- A position moved from open to settled
- A contributor said something that changes the architecture
- A task status changed
- A new dependency appeared or an existing one resolved
- A new mechanic was defined

If nothing is new — write the log file with "No new content this session." Stop.

---

## Step 2 — Classify each new piece

For each new piece of content, run the Layer 2 classifier.
Read: `brain/layers/memory-layers/layer2-classification-prompt.md`

Classifier returns: role, section, confidence, flag.

- Confidence 70+ and flag none → proceed to Step 3
- Confidence below 70 → log as flagged for human review, do not store
- Flag ambiguous → log as flagged for human review, do not store
- Flag cross-topic → log as cross-topic, do not store in memory-layers

---

## Step 3 — Write to section files

For each classified piece:
1. Open the correct section file at `brain/layers/memory-layers/[section].md`
2. Add the content under the correct heading
3. Update `fill` in frontmatter — increment by 1 per entry added
4. Update `last-updated` in frontmatter to today's date

---

## Step 4 — Re-index updated sections in cortexgraph

For each section file that was updated:
1. Call `mcp__cortexgraph__save_memory` with the full updated section content
2. Write the new `memory_id` into the section file's `cortexgraph_id` frontmatter field

---

## Step 5 — Write the log file

Write one file to `projects/memory-layers/logs/YYYY-MM-DD-session-end.md`.

Use this structure:

```
# Session End Log
Date: YYYY-MM-DD

## Stored
- [section]: [one line description of what was stored]

## Flagged for human review
- [content]: [reason — low confidence / ambiguous]

## Cross-topic
- [content]: [which topic it belongs to]

## No changes
[if nothing was stored, state why]
```

---

## Constraint check

Before writing the log file — run C01 through C07 in `brain/constraints/constraints.md`. If any failure condition is met, rewrite the affected output before writing.

## Stop condition

Log file is written. Session ends.

If the log file does not exist after the session — the hook failed. Check `~/.claude/settings.json`.
