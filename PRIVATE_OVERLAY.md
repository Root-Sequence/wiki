# Private Overlay

The Root Sequence Wiki is one logical knowledge system with **public and private visibility layers**.

The public repository remains:

- `Root-Sequence/wiki`
- public-safe entities, project descriptions, provenance, references, and generated views
- the only source consumed by the public Pages workflow

The intended private companion is:

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

## Private repository layout

Recommended structure for `Root-Sequence/wiki-private`:

```text
README.md
entities/
  concept/
  phrase/
  motif/
  source/
  project/
overlays/
  concept/
  phrase/
  motif/
  source/
  project/
PRIVATE_PROJECTS.md        # optional private-only project register
SEEDS.md                   # private seeds / unresolved material
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
related_add:
  - concept:another-private-concept
canonical_private: null
status_private: working
---
```

The Markdown body can contain private notes, chronology, interpretations, or project-specific context.

## Overlay semantics

Private overlays are **additive by default**.

Safe additive fields:

- `projects_add`
- `aliases_add`
- `related_add`
- `canonical_private`
- `status_private`
- `first_known_private`
- private Markdown body

An overlay should not silently rewrite public provenance, authorship claims, or public definitions. If public information is wrong, fix the public entity itself rather than hiding the correction in the private layer.

## Build boundary

The public GitHub Pages workflow must never:

- check out `wiki-private`;
- query private repository contents;
- accept a private-repository token;
- generate public files from the private overlay;
- upload a combined graph as a Pages artifact.

A **private combined build** may read both repositories only when explicitly invoked in a trusted private environment.

Recommended local layout:

```text
Root-Sequence/
  wiki/
  wiki-private/
```

Then the combined builder can read the two repositories as siblings.

## Private combined view

The private view should eventually expose:

```text
public entities
+ private-only entities
+ private overlays
+ public project lenses
+ private project lenses
= one combined private graph
```

Public URLs should remain stable. Private-only entities do not need public placeholders unless their existence itself is intentionally public.

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

Publishing private material should be an explicit act:

1. identify the private entity or overlay fields intended for publication;
2. move or merge only those fields into `Root-Sequence/wiki`;
3. review provenance and canonical links;
4. remove redundant private additions only after the public version is confirmed.

### Public → private

Do not rely on Git history erasure as a privacy mechanism. If something sensitive is accidentally committed publicly, treat it as exposed and follow an appropriate remediation process.

## Security invariant

> **The public build is complete without the private repository. The private build may depend on the public repository, never the reverse.**

This asymmetric dependency is what keeps the visibility boundary understandable and auditable.
