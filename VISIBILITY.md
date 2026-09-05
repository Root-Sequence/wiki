# Visibility Policy

The Root Sequence Wiki is one logical knowledge system with a **public base** and a **private overlay**. Visibility should be predictable enough that the system can grow without requiring a fresh privacy judgment for every link.

## Default rule

> **Inherit source visibility. Crossing from private to public requires an explicit promotion decision. When uncertain, keep it private.**

This is intentionally conservative. "Seems harmless" is not sufficient reason to publish something that originated in a private workspace, unpublished project, private conversation context, or private repository.

## Two separate questions

For any entity, project, source, or relationship, ask separately:

1. **May its contents be public?**
2. **May its existence or name be public?**

Those are different decisions.

A project can therefore have a deliberately public identity while keeping its internal substance private.

## Three supported visibility states

### 1. Public

The identity and its public-safe Wiki treatment live in `Root-Sequence/wiki`.

Use when the material is already public, was intentionally created for public use, or has been deliberately promoted.

```text
public entity
→ public graph
→ public project lenses
→ wiki.rootsequence.systems
```

### 2. Public identity + private depth

A minimal/public-safe entity lives in `Root-Sequence/wiki`. Additional private context lives in `Root-Sequence/wiki-private/overlays/` using the **same stable entity ID**.

```text
public entity
+ private overlay
= richer private combined entity
```

Use this for projects or concepts whose existence may be public while unpublished canon, internal plans, private relationships, detailed mechanisms, or working interpretations remain private.

### 3. Private-only

The entity exists only in `Root-Sequence/wiki-private/entities/`.

Use when even the entity's name, existence, relationship, or framing should not be exposed publicly.

A private-only entity should not receive an automatic public placeholder.

## Routing matrix

| Origin / condition | Default Wiki treatment |
| --- | --- |
| Already published in a public Root Sequence repository/site | Public |
| Explicitly intended for public communication | Public |
| Public concept with additional unpublished/private context | Public entity + private overlay |
| Originates in a private repository or unpublished workspace | Private |
| Unpublished fiction canon/worldbuilding | Private unless explicitly promoted |
| Internal planning, unresolved design, or speculative branch | Private |
| Personal or sensitive contextual information | Private |
| Security/infrastructure detail that could increase operational risk | Private |
| Visibility is ambiguous | Private |

## Public-stub rule

If the **existence** of a private project or concept is intentionally public but its substance is not, create a small public entity or project description containing only the facts intended for disclosure.

Do not copy private material and then try to redact it down automatically.

A good public stub answers only what is intentionally public, for example:

```text
Coherent World
Public: broad project role and intentionally disclosed relationships.
Private: unpublished designs, detailed mechanisms, internal branches, private canon links.
```

The private layer then extends that same identity.

## Repository visibility is evidence, not the entire policy

Repository visibility provides the default:

- public repo → material is eligible for public indexing;
- private repo → material remains private unless deliberately promoted.

But a public Wiki page can still reference the **existence** of a private repository/project if that disclosure is intentional.

Private repository names and URLs should never be added to the public Wiki merely because an authenticated agent can see them.

## Promotion: private → public

Publishing private material is an explicit operation:

1. identify exactly what is intended to become public;
2. review whether the entity's existence, name, relationships, and content can all be disclosed;
3. create/update the public entity with only those fields;
4. preserve the same stable ID when converting a private-only identity into a public identity;
5. convert remaining private-only context into an overlay where appropriate;
6. review provenance and canonical links before publishing.

Promotion should be reversible in the Wiki structure, but **publication itself is not reversible in a privacy sense**. Once material has been public, assume it may have been copied.

## Public → private

Moving or deleting something from the public repository does not make prior publication private again.

If sensitive information is accidentally published, treat it as exposed and handle remediation separately. Git history rewriting is not a privacy strategy.

## Automation rules

Automated/agent maintenance must:

- inherit source visibility;
- default ambiguous material to private;
- never publish private material as a substitute for a missing public description;
- never expose a private project's existence solely because the agent has access;
- never promote private → public without an explicit prior public disclosure or deliberate promotion decision;
- prefer a private Seed when placement or visibility is unresolved;
- report which visibility layer received an update.

The public Pages workflow consumes only `Root-Sequence/wiki` and is guarded against private-overlay dependencies.

## Audit question

For every public project/entity reference, periodically ask:

> **Are we intentionally publishing the identity, the contents, both, or neither?**

This is especially important for private repositories referenced by the curated public `PROJECTS.md`. Their names, descriptions, and repository URLs are themselves disclosures and should remain there only when intentional.

## Short version

> **Public by deliberate choice. Private by inheritance/default. Public stub + private overlay when existence can be public but depth should not be.**
