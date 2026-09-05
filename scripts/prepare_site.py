#!/usr/bin/env python3
"""Prepare MkDocs source and generate a conservative knowledge graph.

The root Markdown files remain canonical. This script copies/relabels them into
.site-src/ for the website and derives graph nodes/edges only from explicit
wiki structure and textual project references.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".site-src"

PAGES = {
    "README.md": ("index.md", "Home"),
    "LEXICON.md": ("lexicon.md", "Lexicon"),
    "PHRASES.md": ("phrases.md", "Phrases & Motifs"),
    "PROJECTS.md": ("projects.md", "Projects"),
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


def parse_table_rows(text: str, heading_marker: str) -> list[list[str]]:
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if heading_marker.lower() in line.lower():
            start = i + 1
            break
    rows: list[list[str]] = []
    seen_header = False
    for line in lines[start:]:
        if line.startswith("## ") and seen_header:
            break
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        if not seen_header:
            seen_header = True
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


def build_graph() -> dict:
    nodes: dict[str, dict] = {}
    edges: set[tuple[str, str, str]] = set()

    def add_node(node_id: str, label: str, kind: str, url: str) -> None:
        nodes[node_id] = {"id": node_id, "label": label, "kind": kind, "url": url}

    def add_edge(source: str, target: str, relation: str) -> None:
        if source != target:
            edges.add((source, target, relation))

    document_nodes = {
        "doc:lexicon": ("Lexicon", "lexicon/"),
        "doc:phrases": ("Phrases & Motifs", "phrases/"),
        "doc:projects": ("Projects", "projects/"),
        "doc:provenance": ("Provenance", "provenance/"),
        "doc:archaeology": ("Concept Archaeology", "archaeology/"),
        "doc:seeds": ("Seeds", "seeds/"),
        "doc:automation": ("Automation", "automation/"),
    }
    for node_id, (label, url) in document_nodes.items():
        add_node(node_id, label, "document", url)

    projects = parse_projects()
    for project in projects:
        node_id = f"project:{slugify(project['label'])}"
        project["id"] = node_id
        add_node(node_id, project["label"], "project", "projects/")
        add_edge(node_id, "doc:projects", "indexed-in")

    terms = parse_lexicon()
    for term in terms:
        node_id = f"term:{slugify(term['label'])}"
        term["id"] = node_id
        add_node(node_id, term["label"], "term", "lexicon/")
        add_edge(node_id, "doc:lexicon", "indexed-in")

    phrases = parse_phrases()
    for phrase in phrases:
        node_id = f"phrase:{slugify(phrase['label'])}"
        phrase["id"] = node_id
        add_node(node_id, phrase["label"], "phrase", "phrases/")
        add_edge(node_id, "doc:phrases", "indexed-in")

    # Connect terms and phrases to projects only when the project name is
    # explicitly present in the corresponding wiki text.
    for item in terms + phrases:
        haystack = item["text"].lower()
        for project in projects:
            label = project["label"].lower()
            if len(label) >= 4 and label in haystack:
                add_edge(item["id"], project["id"], "mentions")

    # Explicit Markdown links among source documents become document edges.
    source_to_doc = {
        "LEXICON.md": "doc:lexicon",
        "PHRASES.md": "doc:phrases",
        "PROJECTS.md": "doc:projects",
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


def make_graph_page() -> str:
    return """# Knowledge Graph\n\nThis view is generated from explicit Wiki structure. It does **not** infer hidden equivalences or treat co-occurrence as proof.\n\n<div class=\"graph-controls\">\n  <label for=\"graph-search\">Find a node</label>\n  <input id=\"graph-search\" type=\"search\" placeholder=\"term, phrase, project…\" autocomplete=\"off\">\n  <button id=\"graph-reset\" type=\"button\">Reset view</button>\n</div>\n\n<div id=\"knowledge-graph\" aria-label=\"Interactive Root Sequence knowledge graph\"></div>\n\n<div id=\"graph-detail\" class=\"graph-detail\">Select a node to see its type and relationships.</div>\n\n## How the graph is built\n\n- terms come from the Lexicon;\n- phrases come from Phrases & Motifs;\n- projects come from the curated Project Index;\n- links are created from explicit Markdown links and explicit project-name mentions;\n- no private repository contents are harvested into the graph.\n\nAs entries become individual pages with richer metadata, this graph can become more precise without changing the public URL.\n"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)

    for src, (dest, _) in PAGES.items():
        source = ROOT / src
        if source.exists():
            (OUT / dest).write_text(rewrite_links(source.read_text(encoding="utf-8")), encoding="utf-8")

    # Ensure navigation always has an auto-project page even before the first sync.
    auto_page = OUT / "auto-projects.md"
    if not auto_page.exists():
        auto_page.write_text(
            "# Live Public Repository Registry\n\nThe first automatic registry sync has not run yet.\n",
            encoding="utf-8",
        )

    (OUT / "graph.md").write_text(make_graph_page(), encoding="utf-8")
    (OUT / "graph.json").write_text(json.dumps(build_graph(), indent=2), encoding="utf-8")

    for asset in ("wiki.css", "graph.js"):
        shutil.copy2(ROOT / "assets" / asset, OUT / "assets" / asset)

    print(f"prepared site source at {OUT}")


if __name__ == "__main__":
    main()
