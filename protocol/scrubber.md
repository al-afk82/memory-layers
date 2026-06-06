# Scrubber Protocol

**When it runs:** Immediately before message history is re-submitted to the model. Every turn without exception.

**One job:** Strip all injected memory context from message history so it does not reappear in subsequent turns.

---

## What to strip

Remove any block matching this pattern from message history:

```
<memory-context section="[any value]">
[any content]
</memory-context>
```

Remove the opening tag, all content between the tags, and the closing tag. Leave everything else in the message intact.

If a message contains multiple memory-context blocks, remove all of them.

If a message contains no memory-context blocks, do nothing.

---

## What not to strip

- The user's actual message content
- Any other XML-style tags not named `memory-context`
- References to memory-context in plain text (e.g. "the memory-context block said...")
- The current turn's injected content — only strip from prior turns in history, not the content being injected right now

---

## Why this exists

When the recognition layer injects a section into context, it wraps it in `<memory-context>` tags. Without the scrubber, those tags and their content accumulate in message history. On the next turn the model sees them again — as if they were part of the original conversation. After several turns, the history becomes bloated with duplicate injected content that was never said by anyone.

The scrubber keeps history clean. Injected content is available for the current turn only. It does not persist.

---

## Failure mode

If the scrubber does not run, injected blocks accumulate. Symptoms:
- Responses begin referencing content that was not mentioned in the current turn
- History grows faster than conversation volume explains
- The model appears to "remember" things from earlier sessions that were not in the loaded sections

If any of these appear — check whether the scrubber ran before the last submission.
