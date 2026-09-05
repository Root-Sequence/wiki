# Wiki Architecture

The Root Sequence Wiki should behave like **one knowledge system with many views**, not a pile of separate mini-wikis that slowly duplicate one another.

## Core model: one graph, many lenses

A project may have what feels like its own sub-wiki, but that sub-wiki is a **lens over shared entities**.

For example:

```text
Root Sequence Wiki
├── concepts
├── terms
├── phrases
├── projects
├── sources
├── people / influences
├── timelines / archaeology
└── relationships
     ├── used-by
     ├── related-to
     ├── evolved-from
     ├── canonical-home
     └── referenced-by
```

Then project views are generated from that same graph:

```text
Being Human(e) lens
  → terms used by Being Human(e)
  → phrases associated with it
  → relevant seeds
  → related projects
  → canonical repository

No One Noticed lens
  → concepts used in the story
  → motifs and phrases
  → Coherent World relationships
  → public-safe canon references
  → canonical story/world homes
```

The lens does not own copies of those entries. It points at the same underlying things.

## Source-of-truth rule

> **Entities are canonical once; views are generated many times.**

A durable concept, project, phrase, source, or artifact should have one canonical Wiki identity. Project lenses, indexes, graph views, timelines, search results, and related-item lists are projections of that identity.

Sub-wikis therefore should not require duplicate directory scaffolding such as:

```text
projects/being-humane/concepts/empathy.md
projects/no-one-noticed/concepts/empathy.md
projects/community-infrastructure/concepts/empathy.md
```

Instead there should eventually be one `empathy` entity with relationships to every project that uses or transforms it.

## Project repositories still own substance

The Wiki organizes **knowledge about the ecosystem**. It does not absorb every project's working documents.

- project repository → canonical argument, design, implementation, policy, canon, research, or archive record;
- Wiki entity → name, short orientation, provenance, aliases, relationships, history, canonical link;
- project lens → generated view of Wiki entities relevant to one project.

This keeps the Wiki useful without making it a second copy of the organization.

## Three layers of "intelligence"

The Wiki can feel increasingly intelligent without pretending a heuristic is understanding.

### Layer 1: deterministic structure

Safe to generate automatically:

- backlinks;
- project lenses;
- aliases;
- explicit `related` relationships;
- canonical-home links;
- timelines from dated provenance;
- orphan detection;
- missing metadata;
- public repository status.

### Layer 2: heuristic signals

Useful as **suggestions**, not facts:

- repeated co-occurrence across projects;
- concepts that appear to bridge otherwise separate projects;
- likely duplicates or aliases;
- unusually isolated entries;
- recurring phrases that may deserve promotion from a seed;
- projects sharing many explicit references.

These should be labeled as signals or candidates rather than silently converted into canonical relationships.

### Layer 3: agent-assisted synthesis

A maintenance agent can review conversations, GitHub changes, and existing Wiki structure to propose or make conservative updates.

It should:

- preserve provenance uncertainty;
- distinguish public from private material;
- prefer linking over copying;
- place immature ideas in Seeds;
- explain why a new relationship was added;
- never infer authorship merely from conversational appearance.

This is the closest layer to an "intelligent Wiki," but it remains accountable to explicit evidence and reversible edits.

## Generated project lenses

The website build creates project-specific lenses from the curated project index and explicit Wiki references.

They are generated into the temporary site source and are **not committed as duplicate Markdown pages**.

A lens may show:

- project role and canonical home;
- terms that explicitly reference the project;
- phrases and motifs that reference it;
- relevant Seeds;
- other projects that share those explicit references;
- maintenance signals about missing or sparse coverage.

This gives each project a sub-wiki-like experience while maintaining one underlying knowledge graph.

## Future entity model

As the Wiki matures, major entries should move from giant tables into individual entity files with lightweight front matter, for example:

```yaml
title: Discoherence Propagation
type: concept
status: working
provenance: origin-unverified
projects:
  - root-sequence
  - universal-coherence-framework
related:
  - coherence
  - cascading-failure
canonical: https://github.com/Root-Sequence/root-sequence/...
visibility: public
```

The same metadata can power navigation, backlinks, project lenses, timelines, search, and graph edges.

## Organizational goal

The Wiki should increasingly answer questions such as:

- What is this?
- Where does it live?
- What else uses it?
- What did it used to be called?
- Which projects overlap here?
- What has changed recently?
- What is underdeveloped or disconnected?
- Where should a new idea probably go?

The goal is not an omniscient database. It is a **self-indexing ecosystem that makes the next useful connection easier to see**.
