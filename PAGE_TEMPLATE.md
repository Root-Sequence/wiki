# Wiki Entity Template

Use this when an indexed term, phrase, motif, or other durable thing has enough identity or cross-project reuse to deserve a canonical entity file under `entities/`.

Not every Lexicon row needs one.

```yaml
---
id: concept:example
title: Example
slug: example
type: concept | phrase | motif | source | artifact | other
status: seed | working | established | retired | composted
provenance: origin-unverified
provenance_confidence: low
visibility: public
projects: []
aliases: []
related: []
evolved_from: []
canonical: null
first_known: "unknown"
first_known_source: unknown
---
```

Use quoted ISO strings for known dates, for example `first_known: "2026-09-05"`, so metadata remains portable across YAML/JSON tooling.

Before creating a public entity from material that originated privately, follow the [Visibility Policy](https://github.com/Root-Sequence/wiki/blob/main/VISIBILITY.md). Private-to-public movement is an explicit promotion decision; uncertain material stays private.

# Example

## Short definition

One or two sentences answering: **what does this mean here?**

## Why it matters

What problem does the entity solve, distinction does it preserve, or relationship does it make visible?

## Ecosystem use

- **Project A:** how it appears there.
- **Project B:** how that treatment differs.

Project labels should match `PROJECTS.md` exactly. Generated project lenses will use these relationships without copying the entity into project-specific folders.

## Provenance

What is currently known about the wording and its history? Link evidence where public evidence exists. Use **first known** rather than **first** unless authorship has actually been established.

## Evolution

Use dated metadata or concise chronology when useful:

```text
YYYY-MM — first known appearance
YYYY-MM — renamed / expanded / challenged
```

## Related

Put related **entity slugs** in front matter. The website generator creates related links and reverse backlinks automatically.

## Canonical substantive home

If a project repository owns the full argument, implementation, research, policy, or canon, put that public URL in `canonical`. The Wiki entity remains an orientation/relationship layer rather than a duplicate copy.

## Open questions

What remains unresolved, contested, or worth testing?
