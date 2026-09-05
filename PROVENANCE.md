# Provenance

The wiki should distinguish **using a term** from **inventing a term**.

## Provenance tags

Use one of these when reasonably known:

- `established-term` — already used outside this ecosystem in substantially the same sense.
- `adapted-term` — established language given a more specific Root Sequence meaning or role.
- `rae-coined` — first known wording came from Rae.
- `jointly-coined` — wording emerged through back-and-forth development between Rae and ChatGPT.
- `project-origin` — coined inside a project, but individual authorship is not important or not yet established.
- `working-term` — temporary language still being tested.
- `joke-escaped-containment` — started as a joke and became useful enough to keep.
- `origin-unverified` — provenance has not yet been checked closely enough to claim authorship.

These tags are descriptive, not prestige rankings.

## Confidence

When provenance is reconstructed later, add a confidence field:

- `high` — directly supported by a dated source or first-known record.
- `medium` — strongly indicated by available records but not conclusively first use.
- `low` — remembered association or incomplete archaeology.

If uncertain, use `origin-unverified`. It is better than accidentally claiming someone else's language.

## Suggested metadata

```yaml
type: concept | phrase | project | motif | seed
status: seed | working | established | retired | composted
provenance: origin-unverified
provenance_confidence: low
first_known: unknown
projects: []
aliases: []
related: []
canonical: null
```

## Special note on ordinary language

A phrase can be independently rediscovered. Common combinations such as "environmental memory", "machine culture", or "radical empathy" should not be treated as original merely because they appeared naturally in conversation. Record the ecosystem-specific interpretation separately from the history of the phrase itself.
