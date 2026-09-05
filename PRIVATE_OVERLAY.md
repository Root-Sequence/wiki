# Private Overlay

The Root Sequence Wiki is one logical knowledge system with **public and private visibility layers**.

The public repository is:

- `Root-Sequence/wiki`
- public-safe entities, project descriptions, provenance, references, and generated views
- the only source consumed by the public Pages workflow

The private companion is:

- `Root-Sequence/wiki-private`
- a **private** repository
- private-only entities and additive overlays for public entities
- unpublished canon, internal project relationships, private archaeology, working notes, and other material that must not enter the public build

## Core rule

> **Same identity, additional private context.**

A concept should not become a second unrelated entity merely because some of its context is private.

For a public entity such as:

```text
concept:bounded-structure
```

`wiki-private` may contain an overlay with that same `id`. The private combined view merges the public entity with the private additions while the public view continues to use only the public entity.

## Active private repository layout

`Root-Sequence/wiki-private` uses:

```text
README.md
PRIVATE_PROJECTS.md
SEEDS.md
entities/                 # private-only identities
overlays/                 # private additions to public entity IDs
templates/
  private-entity.md
  overlay.md
.github/workflows/
  validate.yml            # validates private schema against current public IDs
```

### `entities/`

Use for entities that should exist **only** in the private graph.

Example:

```yaml
---
id: concept:unpublished-example
title: Unpublished Example
type: concept
status: working
provenance: origin-unverified
provenance_confidence: low
visibility: private
projects:
  - Coherent World
aliases: []
related: []
canonical: null
---
```

A private-only entity must not reuse the ID of a public entity.

### `overlays/`

Use when the entity already exists publicly and the private layer needs additional context.

Example:

```yaml
---
id: concept:bounded-structure
visibility: private
extends: concept:bounded-structure
projects_add:
  - Coherent World
aliases_add: []
related_add: []
canonical_private: null
status_private: working
---
```

The Markdown body can contain private notes, chronology, interpretations, or project-specific context.

## Overlay semantics

Private overlays are **additive by default**.

Supported private additions include:

- `projects_add`
- `aliases_add`
- `related_add`
- `canonical_private`
- `status_private`
- `first_known_private`
- `provenance_notes_private`
- private Markdown body

An overlay should not silently rewrite public provenance, authorship claims, or public definitions. If public information is wrong, fix the public entity itself rather than hiding the correction in the private layer.

## Build boundary

The public GitHub Pages workflow must never:

- check out `wiki-private`;
- query private repository contents;
- accept a private-repository token;
- generate public files from the private overlay;
- upload a combined graph as a Pages artifact.

Public CI includes a boundary guard that fails if the Pages workflow begins referencing private-overlay inputs or tooling.

A **private combined build** may read both repositories only when explicitly invoked in a trusted private environment.

Recommended local layout:

```text
Root-Sequence/
  wiki/
  wiki-private/
```

From `wiki/`:

```bash
python scripts/merge_private_overlay.py
```

The combined output is restricted to the gitignored `.private-build/` directory.

## Private validation

`wiki-private/.github/workflows/validate.yml` checks out the public Wiki contract and runs the same merge validator against the private repository.

It validates that:

- private-only entities declare `visibility: private`;
- private-only IDs do not collide with public IDs;
- overlay IDs correspond to real public entities;
- `extends` matches the overlay ID;
- an ID is not simultaneously a private-only entity and an overlay;
- documentation README files are ignored as schema data.

The combined validation data remains ephemeral on the GitHub runner and is not uploaded or deployed.

## Private combined view

The private view can contain:

```text
public entities
+ private-only entities
+ private overlays
+ public project lenses
+ private project context
= one combined private graph
```

Public URLs remain stable. Private-only entities do not need public placeholders unless their existence itself is intentionally public.

## Public-safe stubs

A private project may have a public-safe Wiki entity or project lens that reveals only intentionally public facts.

For example:

```text
Coherent World
public: broad role, relationship to No One Noticed, public-safe description
private: unpublished systemic designs, detailed canon relationships, internal notes
```

The private overlay extends the public identity rather than duplicating the project.

## Promotion and demotion

### Private → public

Publishing private material is an explicit act:

1. identify the private entity or overlay fields intended for publication;
2. move or merge only those fields into `Root-Sequence/wiki`;
3. review provenance and canonical links;
4. remove redundant private additions only after the public version is confirmed.

### Public → private

Do not rely on Git history erasure as a privacy mechanism. If something sensitive is accidentally committed publicly, treat it as exposed and follow an appropriate remediation process.

## Security invariant

> **The public build is complete without the private repository. The private build may depend on the public repository, never the reverse.**

This asymmetric dependency is what keeps the visibility boundary understandable and auditable.
