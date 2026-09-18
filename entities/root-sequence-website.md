---
id: artifact:root-sequence-website
title: Root Sequence Website
slug: root-sequence-website
type: artifact
status: established
provenance: origin-unverified
provenance_confidence: low
visibility: public
projects:
  - Root Sequence
aliases:
  - Root Sequence public site
  - Public Seed
  - rootsequence.systems
related: []
canonical: https://github.com/Root-Sequence/root-sequence/tree/main/site
first_known: unknown
first_known_source: "The public rootsequence.systems site predates the current repository source; the present canonical site source was established in Root-Sequence/root-sequence on 2026-09-18."
---

# Root Sequence Website

## Short definition

The reader-facing public website for Root Sequence at `rootsequence.systems`. Its canonical editorial and publishing source now lives under [`Root-Sequence/root-sequence/site/`](https://github.com/Root-Sequence/root-sequence/tree/main/site), while the research repository remains the substantive home of the full arguments and the Root Sequence Wiki remains the shared ecosystem reference.

## Current source and publication state

On September 18, 2026, the current single-page public seed was approved and `site/index.html` became the canonical editorial source. The publishing workflow builds an approved release from that source rather than publishing the repository tree directly.

GitHub Pages is configured as the intended website host and the generated release has been verified at the staged GitHub Pages origin. The custom domain is configured there, but the public web DNS cutover from Fastmail is still pending. Until that web-only cutover is complete, Fastmail remains the public website host; its DNS and mail service remain separate from the website migration.

This status distinction matters: a verified staged Pages deployment is not the same thing as a completed custom-domain cutover.

## Historical Public Seed

The earlier eleven-page **Public Seed v0.1** candidate is preserved under `site/legacy-public-seed-v0.1/` as project history. It is not a second canonical website source.

`Public Seed` remains a useful alias for the reader-facing Root Sequence website, but edition history belongs in the canonical `site/` records rather than being duplicated in the Wiki.

## Boundaries

The website introduces and routes into Root Sequence. It does not replace:

- the full research and conceptual work in `Root-Sequence/root-sequence`;
- shared identities, provenance and relationships in `Root-Sequence/wiki`;
- private Wiki overlays, unpublished fiction, or other private project material.

Publication approval is tied to the exact reviewed source and build rules. Changes to the canonical site source require a new review/approval cycle in the project repository.

## Canonical substantive home

Current source, approval state, validation records, deployment runbook, and edition history live in [`Root-Sequence/root-sequence/site/`](https://github.com/Root-Sequence/root-sequence/tree/main/site). The Wiki keeps only the stable artifact identity, aliases, project relationship, and high-level publication status.
