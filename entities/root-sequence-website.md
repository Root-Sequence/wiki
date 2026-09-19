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

The reader-facing public website for Root Sequence at `rootsequence.systems`. Its canonical editorial and publishing source lives under [`Root-Sequence/root-sequence/site/`](https://github.com/Root-Sequence/root-sequence/tree/main/site), while the research repository remains the substantive home of the full arguments and the Root Sequence Wiki remains the shared ecosystem reference.

## Current source and publication state

On September 18, 2026, the current single-page public seed was approved and `site/index.html` became the canonical editorial source. The publishing workflow builds an approved release from that source rather than publishing the repository tree directly.

GitHub Pages is enabled with GitHub Actions as the publishing source, and the generated release was verified at the staged Pages origin before the custom domain was attached.

The **web-only DNS cutover was saved in Fastmail on September 18, 2026**. The four apex A records now point to GitHub Pages and `www` has an explicit CNAME to `root-sequence.github.io`. Google Public DNS and Cloudflare both returned the new records after the change. Fastmail still provides the domain's nameservers and email service; MX, SPF, DMARC, and DKIM records were intentionally left in place.

GitHub's custom-domain health check recognizes both the apex and `www` names as valid and served by Pages. Certificate issuance is still pending, so public HTTPS/browser verification and enabling **Enforce HTTPS** remain incomplete. The migration should therefore be described as **DNS-cut-over with certificate finalization pending**, not merely staged and not yet fully closed.

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
