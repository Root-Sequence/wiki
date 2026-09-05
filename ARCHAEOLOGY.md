# Concept Archaeology

The wiki should preserve not only what an idea means now, but how it got here.

## Questions to answer

For a term, phrase, project, or motif:

1. What is the earliest known occurrence?
2. What wording did it use then?
3. Was the term already established elsewhere?
4. Which project first gave it a durable role?
5. What aliases or discarded names did it have?
6. Which later ideas changed its meaning?
7. Is the current definition canonical, provisional, contested, or merely convenient?

## Record format

```yaml
term: example
first_known: 2026-09-05
first_known_source: conversation | github | document | external-source
provenance: origin-unverified
provenance_confidence: low
former_names: []
projects: []
canonical: null
```

Then add a short chronology:

```text
2026-08 — first known fragment
2026-09 — gets a name
2026-10 — applied in another project
2027-01 — definition changes after contradiction / experiment / new source
```

## Rules

- **Earliest found is not automatically first ever.** Say "first known" unless the evidence supports more.
- **Do not backfill certainty.** If a term feels familiar but the source is missing, mark it uncertain.
- **Preserve discarded language.** Old names often explain why the current concept looks the way it does.
- **Keep contradictions.** A later revision should not erase the fact that the earlier version existed.
- **Separate external history from ecosystem history.** An established term can still have a distinct Root Sequence adoption date and evolution.
- **Link, do not duplicate.** If the evidence lives in a project repository, point to it rather than copying the entire source.

## Why bother?

Concepts mutate. Without archaeology, the latest wording can make an idea look more inevitable, coherent, or intentionally designed than it actually was. Preserving the messy path keeps the system honest and makes abandoned branches reusable.
