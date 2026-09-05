#!/usr/bin/env python3
"""Generate AUTO_PROJECTS.md from public Root-Sequence repositories only."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

ORG = "Root-Sequence"
OUT = Path("AUTO_PROJECTS.md")
API = f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&sort=full_name"


def fetch_repos() -> list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "root-sequence-wiki-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos: list[dict] = []
    page = 1
    while True:
        req = urllib.request.Request(f"{API}&page={page}", headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            batch = json.load(response)
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def esc(text: str | None) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render(repos: list[dict]) -> str:
    repos = sorted(repos, key=lambda r: r["name"].lower())
    lines = [
        "# Live Public Repository Registry",
        "",
        "> **Machine-maintained.** This page is generated from public repositories in the `Root-Sequence` GitHub organization. It is a discovery surface, not a semantic description of the ecosystem. See [`PROJECTS.md`](PROJECTS.md) for the curated project map.",
        "",
        "Private repositories are intentionally excluded from this automatic registry.",
        "",
        "| Repository | Description | State | Default branch |",
        "| --- | --- | --- | --- |",
    ]
    for repo in repos:
        name = esc(repo.get("name"))
        url = repo.get("html_url") or f"https://github.com/{ORG}/{name}"
        desc = esc(repo.get("description")) or "—"
        state = "archived" if repo.get("archived") else "active"
        branch = esc(repo.get("default_branch")) or "—"
        lines.append(f"| [{name}]({url}) | {desc} | {state} | `{branch}` |")

    lines += [
        "",
        "## Why this is separate from the curated project map",
        "",
        "A GitHub repository can appear, disappear, be renamed, or change technical state automatically. Its *meaning* inside Root Sequence is interpretive and should remain curated. This file keeps repository discovery current without letting repository metadata silently redefine the ecosystem.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    content = render(fetch_repos())
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
        OUT.write_text(content, encoding="utf-8")
        print(f"updated {OUT}")
    else:
        print(f"{OUT} already current")


if __name__ == "__main__":
    main()
