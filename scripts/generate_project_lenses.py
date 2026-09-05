#!/usr/bin/env python3
"""Generate project lenses and transparent Wiki maintenance signals.

Canonical entities use explicit project metadata. Legacy index-only terms,
phrases, and seeds may still use conservative textual matching until they are
migrated. Generated lenses are site views, never duplicate source homes.
"""

from __future__ import annotations

import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".site-src"
LENSES = OUT / "lenses"
ENTITY_DIR = ROOT / "entities"

ALIASES = {
    "Root Sequence": ["Root Sequence"],
    "Liberated Intelligence": ["Liberated Intelligence"],
    "Universal Coherence Framework": ["Universal Coherence Framework", "UCF"],
    "Being Human(e)": ["Being Human(e)", "Being Humane"],
    "Being Humane Atlas": ["Being Humane Atlas", "Being Human(e) Atlas", "BHIG"],
    "Liberation Mass": ["Liberation Mass"],
    "Community Infrastructure": ["Community Infrastructure"],
    "Coherent World": ["Coherent World"],
    "No One Noticed": ["No One Noticed"],
    "Museum of Ordinary Life": ["Museum of Ordinary Life", "MoOL"],
    "Root Sequence Discussions": ["Root Sequence Discussions"],
    "Root Sequence Wiki": ["Root Sequence Wiki", "Wiki"],
    "Good Chaos": ["Good Chaos"],
}


def slugify(value: str) -> str:
    value = re.sub(r"[*_`\"']", "", value).lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def clean_label(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    return value.replace("**", "").replace("`", "").strip()


def read(name: str) -> str:
    path = ROOT / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        data = {}
    return data, text[end + 5 :]


def load_entities() -> list[dict]:
    entities: list[dict] = []
    if not ENTITY_DIR.exists():
        return entities
    for path in sorted(ENTITY_DIR.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if meta.get("visibility", "public") != "public":
            continue
        entities.append(
            {
                "kind": "entity",
                "label": str(meta.get("title") or path.stem.replace("-", " ").title()),
                "slug": str(meta.get("slug") or path.stem),
                "text": body,
                "source": f"../entities/{meta.get('slug') or path.stem}.md",
                "projects": [str(p) for p in (meta.get("projects") or [])],
                "provenance": str(meta.get("provenance") or "origin-unverified"),
            }
        )
    return entities


def table_rows(text: str, header_fragment: str) -> list[list[str]]:
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if header_fragment.lower() in line.lower():
            start = i
            break
    rows: list[list[str]] = []
    header_seen = False
    for line in lines[start:]:
        if line.startswith("## ") and header_seen:
            break
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        if not header_seen:
            header_seen = True
            continue
        rows.append(cells)
    return rows


def heading_blocks(text: str, level: int = 3) -> list[dict]:
    prefix = "#" * level + " "
    lines = text.splitlines()
    out: list[dict] = []
    for i, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        title = line[len(prefix):].strip().strip('"')
        block: list[str] = []
        for nxt in lines[i + 1:]:
            if nxt.startswith(prefix) or nxt.startswith("## "):
                break
            block.append(nxt)
        out.append({"label": title, "text": "\n".join(block), "anchor": slugify(title)})
    return out


def parse_projects() -> list[dict]:
    rows = table_rows(read("PROJECTS.md"), "| Project |")
    projects = []
    for cells in rows:
        if len(cells) < 3:
            continue
        name = clean_label(cells[0])
        if not name:
            continue
        projects.append({
            "name": name,
            "role": cells[1],
            "home": cells[2],
            "slug": slugify(name),
            "aliases": ALIASES.get(name, [name]),
        })
    return projects


def parse_items() -> list[dict]:
    entities = load_entities()
    entity_slugs = {slugify(item["label"]) for item in entities} | {item["slug"] for item in entities}
    items: list[dict] = list(entities)

    for cells in table_rows(read("LEXICON.md"), "| Term |"):
        if len(cells) < 4:
            continue
        label = clean_label(cells[0])
        if slugify(label) in entity_slugs:
            continue
        items.append({
            "kind": "term",
            "label": label,
            "text": " | ".join(cells),
            "source": "../lexicon.md",
            "projects": [],
        })

    for item in heading_blocks(read("PHRASES.md")):
        if slugify(item["label"]) in entity_slugs:
            continue
        items.append({
            "kind": "phrase",
            "label": item["label"],
            "text": item["text"],
            "source": f"../phrases.md#{item['anchor']}",
            "projects": [],
        })

    for item in heading_blocks(read("SEEDS.md")):
        if item["label"].lower() == "name" or slugify(item["label"]) in entity_slugs:
            continue
        items.append({
            "kind": "seed",
            "label": item["label"],
            "text": item["text"],
            "source": f"../seeds.md#{item['anchor']}",
            "projects": [],
        })

    return items


def matches_project(text: str, project: dict) -> bool:
    lowered = text.lower()
    for alias in project["aliases"]:
        a = alias.lower().strip()
        if len(a) >= 3 and a in lowered:
            return True
    return False


def build_memberships(projects: list[dict], items: list[dict]) -> tuple[dict, dict]:
    by_project: dict[str, list[dict]] = defaultdict(list)
    by_item: dict[int, list[dict]] = defaultdict(list)
    project_lookup = {p["name"]: p for p in projects}

    for idx, item in enumerate(items):
        explicit = [project_lookup[p] for p in item.get("projects", []) if p in project_lookup]
        if item["kind"] == "entity":
            matches = explicit
        else:
            haystack = f"{item['label']}\n{item['text']}"
            matches = [p for p in projects if matches_project(haystack, p)]

        for project in matches:
            by_project[project["name"]].append(item)
            by_item[idx].append(project)

    return by_project, by_item


def write_lens(project: dict, related: list[dict], overlaps: Counter) -> None:
    path = LENSES / f"{project['slug']}.md"
    lines = [
        f"# {project['name']}",
        "",
        "> **Generated project lens.** This page is a view over shared Wiki entities, not a second canonical home for their content.",
        "",
        f"**Role:** {project['role']}  ",
        f"**Canonical home:** {project['home']}",
        "",
    ]

    grouped = {"entity": [], "term": [], "phrase": [], "seed": []}
    for item in related:
        grouped[item["kind"]].append(item)

    section_names = {
        "entity": "Canonical Wiki entities",
        "term": "Legacy indexed terms",
        "phrase": "Phrases & motifs",
        "seed": "Relevant seeds",
    }
    for kind in ("entity", "term", "phrase", "seed"):
        lines.append(f"## {section_names[kind]}")
        lines.append("")
        if grouped[kind]:
            for item in sorted(grouped[kind], key=lambda x: x["label"].lower()):
                lines.append(f"- [{item['label']}]({item['source']})")
        else:
            lines.append("No explicit public Wiki references yet.")
        lines.append("")

    lines += [
        "## Cross-project overlap signals",
        "",
        "These are navigation signals based on shared explicit references. They are **not** claims that the projects are equivalent or causally related.",
        "",
    ]
    if overlaps:
        for other, count in overlaps.most_common(8):
            lines.append(f"- [{other}]({slugify(other)}.md) — {count} shared reference{'s' if count != 1 else ''}")
    else:
        lines.append("No shared-reference signal yet.")
    lines += [
        "",
        "## Editing rule",
        "",
        "Do not edit this generated page to add substantive content. Update the canonical Wiki entity, the curated Project Index, or the project's canonical repository instead.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def generate() -> None:
    if not OUT.exists():
        raise SystemExit(".site-src does not exist; run scripts/prepare_site.py first")

    if LENSES.exists():
        shutil.rmtree(LENSES)
    LENSES.mkdir(parents=True)

    projects = parse_projects()
    items = parse_items()
    by_project, by_item = build_memberships(projects, items)

    overlap_map: dict[str, Counter] = {p["name"]: Counter() for p in projects}
    for plist in by_item.values():
        names = [p["name"] for p in plist]
        for source in names:
            for target in names:
                if source != target:
                    overlap_map[source][target] += 1

    for project in projects:
        write_lens(project, by_project.get(project["name"], []), overlap_map[project["name"]])

    index = [
        "# Project Lenses",
        "",
        "Each project lens is generated from the same shared Wiki entities and indexes. This creates sub-wiki-like views **without duplicating source content**.",
        "",
    ]
    for project in projects:
        count = len(by_project.get(project["name"], []))
        index.append(f"- [{project['name']}]({project['slug']}.md) — {count} explicit Wiki reference{'s' if count != 1 else ''}")
    (LENSES / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")

    item_projects = {idx: [p["name"] for p in by_item.get(idx, [])] for idx in range(len(items))}
    entity_orphans = [items[i] for i, names in item_projects.items() if not names and items[i]["kind"] == "entity"]
    heuristic_orphans = [items[i] for i, names in item_projects.items() if not names and items[i]["kind"] != "entity"]
    low_coverage = [
        (p["name"], len(by_project.get(p["name"], [])))
        for p in projects
        if len(by_project.get(p["name"], [])) < 2
    ]

    legacy_unknown = sum(
        1 for row in table_rows(read("LEXICON.md"), "| Term |")
        if len(row) >= 2 and "origin-unverified" in row[1]
    )
    entity_unknown = sum(
        1 for item in items
        if item["kind"] == "entity" and item.get("provenance") == "origin-unverified"
    )

    signal_lines = [
        "# Wiki Signals",
        "",
        "> **Maintenance view.** Deterministic metadata checks and transparent heuristics appear here as prompts, not automatic conclusions.",
        "",
        "## Current structural signals",
        "",
        f"- Canonical entities: **{sum(1 for i in items if i['kind'] == 'entity')}**",
        f"- Canonical entities with no project relationship: **{len(entity_orphans)}**",
        f"- Legacy/seed items with no heuristic project match: **{len(heuristic_orphans)}**",
        f"- Entity records marked `origin-unverified`: **{entity_unknown}**",
        f"- Legacy Lexicon rows marked `origin-unverified`: **{legacy_unknown}**",
        f"- Curated projects with fewer than two Wiki references: **{len(low_coverage)}**",
        "",
        "## Canonical entity orphans",
        "",
        "These are deterministic metadata gaps: the entity currently names no curated project.",
        "",
    ]
    if entity_orphans:
        for item in sorted(entity_orphans, key=lambda x: x["label"].lower()):
            signal_lines.append(f"- [{item['label']}]({item['source'].replace('../', '')})")
    else:
        signal_lines.append("No canonical entity orphans.")

    signal_lines += [
        "",
        "## Heuristic orphan candidates",
        "",
        "These legacy entries may be perfectly valid. This list only asks whether an explicit relationship or entity migration is worth reviewing.",
        "",
    ]
    if heuristic_orphans:
        for item in sorted(heuristic_orphans, key=lambda x: (x["kind"], x["label"].lower()))[:40]:
            signal_lines.append(f"- **{item['label']}** ({item['kind']})")
    else:
        signal_lines.append("No current heuristic orphan candidates.")

    signal_lines += ["", "## Sparse project lenses", ""]
    if low_coverage:
        for name, count in sorted(low_coverage, key=lambda x: (x[1], x[0].lower())):
            signal_lines.append(f"- [{name}](lenses/{slugify(name)}.md) — {count} explicit reference{'s' if count != 1 else ''}")
    else:
        signal_lines.append("All project lenses currently have at least two explicit references.")

    signal_lines += [
        "",
        "## How to use this page",
        "",
        "Treat signals as review prompts: add metadata when evidence supports it, migrate durable legacy entries into entities when useful, leave meaningful isolation alone, and place uncertain connections in Seeds. The generator never canonicalizes a heuristic relationship automatically.",
        "",
    ]
    (OUT / "signals.md").write_text("\n".join(signal_lines), encoding="utf-8")

    print(f"generated {len(projects)} project lenses from {len(items)} Wiki items")


if __name__ == "__main__":
    generate()
