# Wiki Entities

This directory contains canonical Wiki identities for durable concepts, terms, motifs, and other cross-project entities.

The entity layer is intentionally **hybrid** while the Wiki evolves:

- `LEXICON.md`, `PHRASES.md`, and other indexes remain useful compact discovery surfaces;
- selected entries graduate into individual entity files here;
- the index may keep a one-line summary, but the entity file owns identity, metadata, relationships, provenance, and Wiki-level orientation;
- project lenses, backlinks, graph edges, timelines, and maintenance signals are generated from entity metadata rather than copied into project-specific folders.

> **One entity, many views.**

## Minimum metadata

```yaml
---
id: concept:example
title: Example
slug: example
type: concept
status: working
provenance: origin-unverified
provenance_confidence: low
visibility: public
projects: []
aliases: []
related: []
canonical: null
first_known: unknown
first_known_source: unknown
---
```

Project names in `projects` should match the curated names in `PROJECTS.md`. Values in `related` are entity slugs, not copied page paths.

## Source-of-truth boundary

An entity page describes what something **is in the Root Sequence ecosystem** and where its substantive work lives. It does not replace a project's full argument, implementation, private canon, policy, or research record.
