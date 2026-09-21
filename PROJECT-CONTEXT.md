---
context_format: root-sequence-project-context/v1
project_id: wiki
repository: Root-Sequence/wiki
visibility: public
status: active-public-knowledge-graph
---

# Project Context — Root Sequence Wiki

## Purpose and scope

The Wiki is the public vocabulary, identity, provenance, relationship, archaeology, and navigation layer for Root Sequence. It helps answer what something is called, where it belongs, how it connects, how it changed, and where its substantive canonical work lives.

It is not a second conceptual commons, implementation repository, fiction canon, or automatic publication surface for private material.

## Source-of-truth map

| Question | Canonical source |
| --- | --- |
| Wiki purpose and reader orientation | [`README.md`](README.md) |
| One-Wiki/many-views architecture | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Automation and review boundaries | [`AUTOMATION.md`](AUTOMATION.md) |
| Curated project meaning | [`PROJECTS.md`](PROJECTS.md) |
| Live public repository discovery | [`AUTO_PROJECTS.md`](AUTO_PROJECTS.md) |
| Public/private layer contract | [`PRIVATE_OVERLAY.md`](PRIVATE_OVERLAY.md) |
| Provenance rules | [`PROVENANCE.md`](PROVENANCE.md) |

## Current reality

The repository contains public entities, indexes, a generated site/knowledge graph, project lenses, automation, validation, and a daily public-repository registry. Generated overlap and maintenance signals are review cues, not facts. Private context exists in a separate overlay and is never required by the public build.

## Repository structure

`entities/` contains canonical public identities. Root indexes cover projects, terms, phrases, provenance, archaeology, and seeds. `scripts/` validates and generates the site and project lenses. `.site-src/` and private combined output are generated rather than canonical.

## Ecosystem connections

Every project owns its arguments, designs, implementations, policies, practices, archives, and canon. The Wiki owns findability, naming, explicit relationships, and history. `wiki-private` extends stable identities privately; public never depends on private.

## Working rules

- Use one stable identity and generate multiple views.
- Link to canonical substance rather than reproducing it.
- Record provenance and uncertainty; do not infer equivalence from similar language.
- Keep public builds independent of all private repositories.
- Treat heuristic graph signals as invitations to review.

## Update contract

Review when schema, public/private architecture, generation, project-lens behavior, provenance, visibility, or canonical project relationships change.
