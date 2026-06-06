# Classification Prompt — Memory-layers

> Run this prompt on any incoming message to assign it to the correct section within the memory-layers topic.
> Version 1 — good enough to surface valid errors.

---

## Prompt

You are a classifier for the memory-layers topic. Your job is to read an incoming message and assign it to exactly one section.

**The four sections are:**

**Layer 1 — Segmentation**
Role: owns the structure of how topics are broken into sections.
Belongs here: topic definitions, section definitions, classification prompts, the topic list.
Does not belong here: real-time routing decisions, overflow handling, collaborator inputs.

**Layer 2 — Routing**
Role: owns all real-time routing decisions and mechanisms during a live session.
Belongs here: stateful classifier, session entry protocol, drift notification, adjacent counter, eviction trigger, save-before-evict, pointer design, session state file.
Does not belong here: section structure definitions, overflow handling, collaborator inputs.

**Layer 3 — Overflow**
Role: owns what happens when a section approaches capacity.
Belongs here: fill monitor, transfer protocol, variance detection, recognition layer, thread reconstruction.
Does not belong here: real-time routing decisions, section structure definitions, collaborator inputs.

**Collaborators**
Role: owns external input that shaped the architecture — not the decisions, the inputs.
Belongs here: David Vogel inputs, Jake Van Clee principles applied here, other external contributor inputs.
Does not belong here: settled decisions, build progress, next steps.

---

**Rules:**

1. A message must satisfy the section's role AND fall within its scope to be assigned there.
2. If a message clearly fits one section: assign it there.
3. If a message fits two sections: assign it to the section whose role it primarily serves.
4. If a message fits no section clearly: return "outside known set." Do not force a weak match.

---

**Output format:**

```
Section: [section name]
Reason: [one sentence — why this section, not another]
```

If outside known set:
```
Section: outside known set
Reason: [one sentence — what the message is about and why it fits no defined section]
```

---

## Test cases

Run these to verify the prompt before using it in a live session.

| Message | Expected section |
|---------|-----------------|
| "How does the stateful classifier handle slow drift?" | Layer 2 — Routing |
| "What sections does the memory-layers topic break into?" | Layer 1 — Segmentation |
| "What happens when a section hits 85% capacity?" | Layer 3 — Overflow |
| "What did David Vogel say about the variance rule?" | Collaborators |
| "What is the next step for the build?" | outside known set |
