# Topic Definitions

> Layer 1 build reference. Each topic has a role and scope. Role = what it is responsible for. Scope = what belongs, and what explicitly does not.
> The classifier compares incoming messages against these definitions. A message must satisfy role AND fall within scope to route here. If it fits none, return "outside known set."

---

## Memory-layers

**Role**
Owns all design and architecture decisions for the layered memory system. Responsible for how memory is segmented, routed, overflowed, and stored. Nothing else.

**Scope — belongs here**
- Classifier design, structure, pressure testing
- Topic list definitions — role and scope of each topic
- Layer 1 segmentation — classification prompts, topic definitions
- Layer 2 routing — stateful classifier, drift detection, notification mechanism, adjacent counter
- Layer 3 overflow — fill monitor, transfer protocol, recognition layer, variance rule
- Storage schema decisions
- David Vogel architecture inputs
- Build order and next steps within memory-layers

**Scope — does not belong here**
- Echosystem as a product — server, API, thin client, hosting, execution layer → Echosystem
- Outreach, pipeline, client work → Outreach
- Berlin, Delta Campus, collaborator conversations → Echosystem
- Fantom Foiling, Johannes → Fantom
- Brain files — identity, voice, constraints → Brain

---

## Echosystem

**Role**
Owns all product and architecture decisions for Echosystem as a deployable system. Responsible for what Echosystem is, how it is built, and how it reaches users. Not the memory architecture inside it — that belongs to Memory-layers.

**Scope — belongs here**
- Product architecture — server, API, thin client
- Hosting decisions and costs
- Execution layer — what runs when Alec is not present
- Collaborator conversations — Ari, Delta Campus, potential build partners
- Distribution strategy — Paperclip as future surface, other channels
- Echosystem as a pitch or positioning problem
- Jonathan Teklu — investor relationship, stage 2 selling

**Scope — does not belong here**
- Memory classifier design, routing logic, overflow → Memory-layers
- Outreach pipeline, client work, Malec Systems → Outreach
- Fantom Foiling → Fantom
- Brain files — identity, voice, constraints → Brain

---

## Topics to define

The following topics have been identified but not yet defined. Define before the classifier can route to them.

- Outreach
- Brain
- Fantom
