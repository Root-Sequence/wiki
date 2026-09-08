# Publishing & Deployment

The public Wiki is published at [wiki.rootsequence.systems](https://wiki.rootsequence.systems/) with GitHub Pages.

## Public build

Every push to `main` starts `.github/workflows/pages.yml`. The workflow:

1. checks the public/private boundary;
2. prepares the generated site source;
3. generates project lenses and Wiki signals;
4. runs a strict MkDocs build;
5. uploads and deploys the Pages artifact.

The public workflow reads only this public repository. It does not check out, query, or merge `Root-Sequence/wiki-private`.

## GitHub Pages configuration

Repository administrators configure **Settings → Pages → Build and deployment → Source** as **GitHub Actions**.

The custom domain is `wiki.rootsequence.systems`, with the `wiki` DNS CNAME pointing to `root-sequence.github.io`. HTTPS should remain enforced once GitHub has provisioned the certificate.

## Local verification

Use the same sequence as CI before publishing a structural or presentation change:

```bash
python scripts/check_public_boundary.py
python scripts/prepare_site.py
python scripts/generate_project_lenses.py
mkdocs build --strict --site-dir _site
```

Generated `.site-src/` and `_site/` directories are build outputs and are not canonical Wiki content.

## Maintenance automation

The separate daily repository sync is described in [Wiki Automation](AUTOMATION.md). The public/private repository contract and private validation boundary are described in [Public + Private Layers](PRIVATE_OVERLAY.md).
