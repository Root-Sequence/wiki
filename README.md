# Root Sequence Wiki

A living index for the Root Sequence ecosystem: terms, projects, phrases, connections, provenance, and conceptual archaeology.

The wiki is a **navigation and context layer**, not a replacement for project repositories.

> **Canonical rule:** keep one canonical home for substantive work, then link to it from here. Do not create silent copies that drift apart.

## One Wiki, many views

The Wiki is organized as a shared knowledge graph rather than a collection of disconnected project wikis.

Each Root Sequence project can have a **generated project lens** that behaves like a sub-wiki: it gathers the terms, phrases, seeds, relationships, and canonical links relevant to that project without copying the underlying entries.

> **Entities are canonical once; views are generated many times.**

See [Wiki Architecture](ARCHITECTURE.md) for the full model.

## Start here

- [Lexicon](LEXICON.md) — recurring terms, adapted language, working concepts, and jokes that escaped containment.
- [Phrases & motifs](PHRASES.md) — lines worth preserving because they recur, clarify a project, or become conceptual tools.
- [Projects](PROJECTS.md) — what each project does and where its canonical work lives.
- [Live public repo registry](AUTO_PROJECTS.md) — machine-maintained discovery of public `Root-Sequence` repositories.
- [Wiki Architecture](ARCHITECTURE.md) — one graph, many project lenses, and the intelligence model.
- [Provenance](PROVENANCE.md) — how we record whether a term is established, adapted, Rae-coined, jointly coined, uncertain, or otherwise sourced.
- [Concept archaeology](ARCHAEOLOGY.md) — when an idea first appeared, what it used to be called, and how it changed.
- [Seeds](SEEDS.md) — fragments that are not mature enough for a canonical project home yet.
- [Automation](AUTOMATION.md) — what updates automatically, what remains curated, and the public/private boundary.
- [Page template](PAGE_TEMPLATE.md) — lightweight metadata for new entries.

## Website

The repository is configured to publish a searchable static Wiki with an automatically generated interactive knowledge graph, project lenses, and heuristic maintenance signals.

**Intended public URL:** `https://wiki.rootsequence.systems/`

Every push to `main` rebuilds the site.

The generated site includes:

- an interactive knowledge graph;
- project-specific lenses that act like sub-wikis without duplicate source files;
- a Wiki Signals view that surfaces orphaned entries, sparse project coverage, and other transparent maintenance cues;
- a machine-maintained public repository registry;
- ordinary search and navigation across the Wiki.

The graph and lenses are generated from explicit Wiki structure and references. Heuristic signals are shown as suggestions, not silently promoted into canonical relationships.

### One-time GitHub Pages setup

Repository administrators must enable **Settings → Pages → Build and deployment → Source: GitHub Actions** once. The workflow is already committed at `.github/workflows/pages.yml`.

After Pages is enabled, configure `wiki.rootsequence.systems` as the custom domain in GitHub Pages and point the `wiki` DNS CNAME at `root-sequence.github.io`.

## Automatic maintenance

Three complementary layers keep different kinds of knowledge current:

1. **GitHub-side automation** refreshes `AUTO_PROJECTS.md` daily from public repositories only and rebuilds the site on every Wiki change.
2. **Generated structure** creates project lenses, backlinks/graph relationships, and structural maintenance signals from the same canonical Wiki source.
3. **Conversation-side maintenance** reviews recent Root Sequence work for durable new terms, aliases, phrases, project relationships, or provenance evidence and updates the Wiki conservatively when warranted.

Definitions, originality claims, private/public boundaries, and canon are intentionally **not** delegated to blind automation. See [Automation](AUTOMATION.md).

## What belongs here

The wiki is useful when the question is:

- What do we call this?
- Where does this idea belong?
- Which projects use it?
- Is this an established term or something we developed?
- What did we call this before?
- How did this concept change over time?
- What connects these otherwise separate projects?
- Which parts of the project ecosystem are under-documented or disconnected?

If the question is instead "what is the full argument/design/canon?", follow the link to its canonical repository.

## Entry lifecycle

```text
capture → seed → working entry → linked concept → canonicalized / composted
```

Nothing needs to pretend to be finished. Uncertainty should be visible rather than papered over.

## Relationship to existing Root Sequence navigation

This layer complements, rather than replaces:

- [Ecosystem Map](https://github.com/Root-Sequence/root-sequence/blob/main/ECOSYSTEM.md) for organization-wide project relationships;
- [Idea Trails](https://github.com/Root-Sequence/root-sequence/blob/main/IDEA_TRAILS.md) and the [Idea Trail Browser](https://github.com/Root-Sequence/root-sequence/blob/main/IDEA_TRAIL_INDEX.md) for recurring cross-project questions and document trails;
- [Root Sequence concepts](https://github.com/Root-Sequence/root-sequence/tree/main/concepts) for canonical Root Sequence concept treatments;
- [Root Sequence repository map](https://github.com/Root-Sequence/root-sequence/blob/main/root_map.md) for the internal structure of the conceptual commons.

The wiki should make those systems easier to enter, not duplicate them.

## Canonical home

This repository is the canonical home of the Root Sequence Wiki. The earlier prototype under `Root-Sequence/root-sequence/wiki/` was migrated here on 2026-09-05.
