#!/usr/bin/env python3
"""Prepare MkDocs source and generate a conservative knowledge graph.

Root Markdown indexes remain useful discovery surfaces. Durable entries may
also have one canonical Wiki identity under entities/. Generated site views,
backlinks, project lenses, and graph edges are projections of that identity.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".site-src"
ENTITY_DIR = ROOT / "entities"

PAGES = {
    "README.md": ("index.md", "Home"),
    "LEXICON.md": ("lexicon.md", "Lexicon"),
    "PHRASES.md": ("phrases.md", "Phrases & Motifs"),
    "PROJECTS.md": ("projects.md", "Projects"),
    "ARCHITECTURE.md": ("architecture.md", "Architecture"),
    "PROVENANCE.md": ("provenance.md", "Provenance"),
    "ARCHAEOLOGY.md": ("archaeology.md", "Concept Archaeology"),
    "SEEDS.md": ("seeds.md", "Seeds"),
    "AUTOMATION.md": ("automation.md", "Automation"),
    "AUTO_PROJECTS.md": ("auto-projects.md", "Live Public Repo Registry"),
    "PAGE_TEMPLATE.md": ("page-template.md", "Entry Template"),
}

LINK_REWRITES = {src: dest for src, (dest, _) in PAGES.items()}


def slugify(value: str) -> str:
    value = re.sub(r"[*_`\"']", "", value).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def clean_markdown_label(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("**", "").replace("`", "").strip()
    return html.unescape(value)


def rewrite_links(text: str) -> str:
    for src, dest in LINK_REWRITES.items():
        text = text.replace(f"]({src})", f"]({dest})")
    return text


def read(name: str) -> str:
    path = ROOT / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


def load_entities() -> list[dict]:
    entities: list[dict] = []
    if not ENTITY_DIR.exists():
        return entities
    for path in sorted(ENTITY_DIR.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        if meta.get("visibility", "public") != "public":
            continue
        title = str(meta.get("title") or path.stem.replace("-", " ").title())
        slug = str(meta.get("slug") or path.stem)
        entity_id = str(meta.get("id") or f"entity:{slug}")
        entities.append(
            {
                "id": entity_id,
                "title": title,
                "slug": slug,
                "type": str(meta.get("type") or "entity"),
                "status": str(meta.get("status") or "working"),
                "provenance": str(meta.get("provenance") or "origin-unverified"),
                "projects": list(meta.get("projects") or []),
                "aliases": list(meta.get("aliases") or []),
                "related": list(meta.get("related") or []),
                "evolved_from": list(meta.get("evolved_from") or []),
                "canonical": meta.get("canonical"),
                "first_known": meta.get("first_known"),
                "source_path": path,
                "body": body.rstrip() + "\n",
            }
        )
    return entities


def parse_table_rows(text: str, heading_marker: str) -> list[list[str]]:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if heading_marker.lower() in line.lower():
            start = i + 1
            break
    if start is None:
        return []

    rows: list[list[str]] = []
    for line in lines[start:]:
        if line.startswith("## ") and rows:
            break
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    return rows


def parse_lexicon() -> list[dict]:
    rows = parse_table_rows(read("LEXICON.md"), "| Term |")
    items = []
    for cells in rows:
        if len(cells) < 4:
            continue
        label = clean_markdown_label(cells[0])
        items.append({"label": label, "text": " | ".join(cells), "kind": "term"})
    return items


def parse_projects() -> list[dict]:
    rows = parse_table_rows(read("PROJECTS.md"), "| Project |")
    items = []
    for cells in rows:
        if len(cells) < 3:
            continue
        label = clean_markdown_label(cells[0])
        if not label:
            continue
        items.append({"label": label, "text": " | ".join(cells), "kind": "project"})
    return items


def parse_phrases() -> list[dict]:
    text = read("PHRASES.md")
    lines = text.splitlines()
    items: list[dict] = []
    for i, line in enumerate(lines):
        if not line.startswith("### "):
            continue
        label = line[4:].strip().strip('"')
        block: list[str] = []
        for nxt in lines[i + 1 :]:
            if nxt.startswith("### ") or nxt.startswith("## "):
                break
            block.append(nxt)
        items.append({"label": label, "text": "\n".join(block), "kind": "phrase"})
    return items


def build_graph(entities: list[dict]) -> dict:
    nodes: dict[str, dict] = {}
    edges: set[tuple[str, str, str]] = set()

    def add_node(node_id: str, label: str, kind: str, url: str, **extra) -> None:
        node = {"id": node_id, "label": label, "kind": kind, "url": url}
        node.update({k: v for k, v in extra.items() if v not in (None, [], "")})
        nodes[node_id] = node

    def add_edge(source: str, target: str, relation: str) -> None:
        if source != target:
            edges.add((source, target, relation))

    document_nodes = {
        "doc:lexicon": ("Lexicon", "lexicon/"),
        "doc:phrases": ("Phrases & Motifs", "phrases/"),
        "doc:projects": ("Projects", "projects/"),
        "doc:architecture": ("Architecture", "architecture/"),
        "doc:provenance": ("Provenance", "provenance/"),
        "doc:archaeology": ("Concept Archaeology", "archaeology/"),
        "doc:seeds": ("Seeds", "seeds/"),
        "doc:automation": ("Automation", "automation/"),
    }
    for node_id, (label, url) in document_nodes.items():
        add_node(node_id, label, "document", url)

    projects = parse_projects()
    project_by_slug: dict[str, dict] = {}
    for project in projects:
        pslug = slugify(project["label"])
        node_id = f"project:{pslug}"
        project["id"] = node_id
        project_by_slug[pslug] = project
        add_node(node_id, project["label"], "project", f"lenses/{pslug}/")
        add_edge(node_id, "doc:projects", "indexed-in")

    entity_by_slug = {entity["slug"]: entity for entity in entities}
    entity_by_title_slug = {slugify(entity["title"]): entity for entity in entities}

    for entity in entities:
        add_node(
            entity["id"],
            entity["title"],
            entity["type"],
            f"entities/{entity['slug']}/",
            status=entity["status"],
            provenance=entity["provenance"],
            aliases=entity["aliases"],
        )
        for project_name in entity["projects"]:
            project = project_by_slug.get(slugify(str(project_name)))
            if project:
                add_edge(entity["id"], project["id"], "used-by")
        for related_slug in entity["related"]:
            related = entity_by_slug.get(str(related_slug))
            if related:
                add_edge(entity["id"], related["id"], "related-to")
        for older_slug in entity["evolved_from"]:
            older = entity_by_slug.get(str(older_slug))
            if older:
                add_edge(entity["id"], older["id"], "evolved-from")

    terms = parse_lexicon()
    for term in terms:
        tslug = slugify(term["label"])
        entity = entity_by_slug.get(tslug) or entity_by_title_slug.get(tslug)
        if entity:
            term["id"] = entity["id"]
            add_edge(entity["id"], "doc:lexicon", "indexed-in")
            continue
        node_id = f"term:{tslug}"
        term["id"] = node_id
        add_node(node_id, term["label"], "term", "lexicon/")
        add_edge(node_id, "doc:lexicon", "indexed-in")

    phrases = parse_phrases()
    for phrase in phrases:
        pslug = slugify(phrase["label"])
        entity = entity_by_slug.get(pslug) or entity_by_title_slug.get(pslug)
        if entity:
            phrase["id"] = entity["id"]
            add_edge(entity["id"], "doc:phrases", "indexed-in")
            continue
        node_id = f"phrase:{pslug}"
        phrase["id"] = node_id
        add_node(node_id, phrase["label"], "phrase", "phrases/")
        add_edge(node_id, "doc:phrases", "indexed-in")

    # Legacy index entries without entity metadata still receive conservative
    # project connections only when a project name is explicitly present.
    for item in terms + phrases:
        haystack = item["text"].lower()
        for project in projects:
            label = project["label"].lower()
            if len(label) >= 4 and label in haystack:
                add_edge(item["id"], project["id"], "mentions")

    source_to_doc = {
        "LEXICON.md": "doc:lexicon",
        "PHRASES.md": "doc:phrases",
        "PROJECTS.md": "doc:projects",
        "ARCHITECTURE.md": "doc:architecture",
        "PROVENANCE.md": "doc:provenance",
        "ARCHAEOLOGY.md": "doc:archaeology",
        "SEEDS.md": "doc:seeds",
        "AUTOMATION.md": "doc:automation",
    }
    for source_name, source_id in source_to_doc.items():
        text = read(source_name)
        for target_name, target_id in source_to_doc.items():
            if target_name != source_name and f"]({target_name})" in text:
                add_edge(source_id, target_id, "links-to")

    return {
        "nodes": list(nodes.values()),
        "edges": [
            {"source": s, "target": t, "relation": r}
            for s, t, r in sorted(edges)
        ],
    }


def write_entity_pages(entities: list[dict]) -> None:
    target = OUT / "entities"
    target.mkdir(parents=True, exist_ok=True)
    entity_by_slug = {e["slug"]: e for e in entities}
    backlinks: dict[str, list[dict]] = defaultdict(list)
    for entity in entities:
        for related_slug in entity["related"]:
            if related_slug in entity_by_slug:
                backlinks[str(related_slug)].append(entity)

    index = [
        "# Entities",
        "",
        "Canonical Wiki identities. Indexes and project lenses point here rather than creating project-specific copies.",
        "",
    ]

    for entity in sorted(entities, key=lambda e: e["title"].lower()):
        slug = entity["slug"]
        index.append(f"- [{entity['title']}]({slug}.md) — {entity['type']} · {entity['status']}")

        lines = [entity["body"].rstrip(), "", "## Wiki connections", ""]
        if entity["projects"]:
            lines.append("**Project lenses**")
            lines.append("")
            for project_name in entity["projects"]:
                pslug = slugify(str(project_name))
                lines.append(f"- [{project_name}](../lenses/{pslug}.md)")
            lines.append("")

        if entity["related"]:
            lines.append("**Related entities**")
            lines.append("")
            for related_slug in entity["related"]:
                related = entity_by_slug.get(str(related_slug))
                if related:
                    lines.append(f"- [{related['title']}]({related['slug']}.md)")
            lines.append("")

        incoming = backlinks.get(slug, [])
        if incoming:
            lines.append("**Referenced by entities**")
            lines.append("")
            for source in sorted(incoming, key=lambda e: e["title"].lower()):
                lines.append(f"- [{source['title']}]({source['slug']}.md)")
            lines.append("")

        if entity["canonical"]:
            lines += ["**Canonical substantive home**", "", f"- {entity['canonical']}", ""]

        (target / f"{slug}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    (target / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def make_graph_page() -> str:
    return """# Knowledge Graph\n\nThis view is generated from explicit Wiki structure. It does **not** infer hidden equivalences or treat co-occurrence as proof.\n\n<div class=\"graph-controls\">\n  <label for=\"graph-search\">Find a node</label>\n  <input id=\"graph-search\" type=\"search\" placeholder=\"term, entity, phrase, project…\" autocomplete=\"off\">\n  <button id=\"graph-reset\" type=\"button\">Reset view</button>\n</div>\n\n<div id=\"knowledge-graph\" data-graph-url=\"../graph.json\" aria-label=\"Interactive Root Sequence knowledge graph\"></div>\n\n<div id=\"graph-detail\" class=\"graph-detail\">Select a node to see its type and relationships.</div>\n\n## How the graph is built\n\n- canonical entities come from explicit metadata under `entities/`;\n- legacy terms come from the Lexicon until they graduate into entities;\n- phrases come from Phrases & Motifs unless they have a canonical entity identity;\n- projects come from the curated Project Index;\n- entity relationships come from explicit metadata;\n- legacy project links require explicit textual project-name mentions;\n- no private repository contents are harvested into the graph.\n\nThe graph therefore becomes richer as entries gain metadata without duplicating their identity across project views.\n"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)

    for src, (dest, _) in PAGES.items():
        source = ROOT / src
        if source.exists():
            (OUT / dest).write_text(rewrite_links(source.read_text(encoding="utf-8")), encoding="utf-8")

    auto_page = OUT / "auto-projects.md"
    if not auto_page.exists():
        auto_page.write_text(
            "# Live Public Repository Registry\n\nThe first automatic registry sync has not run yet.\n",
            encoding="utf-8",
        )

    entities = load_entities()
    write_entity_pages(entities)
    (OUT / "graph.md").write_text(make_graph_page(), encoding="utf-8")
    (OUT / "graph.json").write_text(json.dumps(build_graph(entities), indent=2), encoding="utf-8")

    for asset in ("wiki.css", "graph.js"):
        shutil.copy2(ROOT / "assets" / asset, OUT / "assets" / asset)

    print(f"prepared site source at {OUT} with {len(entities)} canonical entities")


if __name__ == "__main__":
    main()
