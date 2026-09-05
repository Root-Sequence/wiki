#!/usr/bin/env python3
"""Build a private combined entity view from public Wiki + private overlay.

This script is intentionally NOT used by the public GitHub Pages workflow.
It reads the public entity layer from this repository and a sibling/private
repository, then writes combined data only under `.private-build/`, which
should remain gitignored.

Expected layout by default:

    Root-Sequence/
      wiki/
      wiki-private/

Override the private repository path with WIKI_PRIVATE_DIR or --private-dir.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIVATE = ROOT.parent / "wiki-private"
PRIVATE_BUILD = ROOT / ".private-build"


class OverlayError(RuntimeError):
    pass


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise OverlayError(f"{path}: entity/overlay is missing YAML front matter")
    try:
        _, fm, body = text.split("---", 2)
    except ValueError as exc:
        raise OverlayError(f"{path}: malformed front matter") from exc
    data = yaml.safe_load(fm) or {}
    if not isinstance(data, dict):
        raise OverlayError(f"{path}: front matter must be a mapping")
    entity_id = data.get("id")
    if not isinstance(entity_id, str) or ":" not in entity_id:
        raise OverlayError(f"{path}: stable `id` is required")
    return data, body.strip()


def load_tree(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*.md")):
        meta, body = parse_frontmatter(path)
        entity_id = meta["id"]
        if entity_id in out:
            raise OverlayError(f"duplicate id {entity_id!r}: {path} and {out[entity_id]['_path']}")
        out[entity_id] = {
            **meta,
            "body": body,
            "_path": str(path),
        }
    return out


def merge_unique(base: Any, additions: Any) -> list[Any]:
    result: list[Any] = []
    for value in list(base or []) + list(additions or []):
        if value not in result:
            result.append(value)
    return result


def apply_overlay(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    entity_id = base["id"]
    if overlay.get("visibility") != "private":
        raise OverlayError(f"overlay {entity_id}: visibility must be `private`")
    if overlay.get("extends") not in (None, entity_id):
        raise OverlayError(
            f"overlay {entity_id}: `extends` must be omitted or equal the entity id"
        )

    merged = copy.deepcopy(base)
    merged["projects"] = merge_unique(base.get("projects"), overlay.get("projects_add"))
    merged["aliases"] = merge_unique(base.get("aliases"), overlay.get("aliases_add"))
    merged["related"] = merge_unique(base.get("related"), overlay.get("related_add"))
    merged["visibility_effective"] = "private-combined"

    private_meta: dict[str, Any] = {}
    for key in (
        "canonical_private",
        "status_private",
        "first_known_private",
        "provenance_notes_private",
    ):
        if key in overlay:
            private_meta[key] = overlay[key]

    if overlay.get("body"):
        private_meta["body"] = overlay["body"]

    if private_meta:
        merged["private"] = private_meta

    merged["_overlay_path"] = overlay.get("_path")
    return merged


def validate_public_entities(public: dict[str, dict[str, Any]]) -> None:
    for entity_id, entity in public.items():
        visibility = entity.get("visibility", "public")
        if visibility != "public":
            raise OverlayError(
                f"public repository entity {entity_id} has visibility={visibility!r}; "
                "private-only entities belong in wiki-private"
            )


def validate_private_only(private: dict[str, dict[str, Any]]) -> None:
    for entity_id, entity in private.items():
        if entity.get("visibility") != "private":
            raise OverlayError(
                f"private entity {entity_id} must declare visibility: private"
            )


def build_combined(private_dir: Path) -> dict[str, Any]:
    public = load_tree(ROOT / "entities")
    private_only = load_tree(private_dir / "entities")
    overlays = load_tree(private_dir / "overlays")

    validate_public_entities(public)
    validate_private_only(private_only)

    collisions = sorted(set(public) & set(private_only))
    if collisions:
        raise OverlayError(
            "private-only entity ids collide with public entities; use overlays instead: "
            + ", ".join(collisions)
        )

    combined: dict[str, dict[str, Any]] = {
        entity_id: copy.deepcopy(entity) for entity_id, entity in public.items()
    }
    for entity_id, entity in private_only.items():
        entity = copy.deepcopy(entity)
        entity["visibility_effective"] = "private"
        combined[entity_id] = entity

    for entity_id, overlay in overlays.items():
        if entity_id not in public:
            raise OverlayError(
                f"overlay {entity_id!r} has no matching public entity; "
                "use private entities/ for private-only identities"
            )
        combined[entity_id] = apply_overlay(public[entity_id], overlay)

    # Strip absolute working paths from the portable data, but preserve
    # repository-relative provenance paths for debugging.
    for entity in combined.values():
        for key in ("_path", "_overlay_path"):
            value = entity.get(key)
            if value:
                try:
                    entity[key] = str(Path(value).resolve().relative_to(ROOT.parent.resolve()))
                except ValueError:
                    entity[key] = Path(value).name

    return {
        "mode": "private-combined",
        "public_repository": "Root-Sequence/wiki",
        "private_repository": "Root-Sequence/wiki-private",
        "entity_count": len(combined),
        "public_entity_count": len(public),
        "private_only_entity_count": len(private_only),
        "overlay_count": len(overlays),
        "entities": [combined[key] for key in sorted(combined)],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--private-dir",
        type=Path,
        default=Path(os.environ.get("WIKI_PRIVATE_DIR", DEFAULT_PRIVATE)),
        help="path to the private companion repository",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PRIVATE_BUILD / "combined-entities.json",
        help="output path; must remain under .private-build/",
    )
    args = parser.parse_args()

    private_dir = args.private_dir.resolve()
    output = args.output.resolve()
    build_root = PRIVATE_BUILD.resolve()

    if not private_dir.exists():
        raise SystemExit(
            f"private overlay repository not found at {private_dir}. "
            "Create/clone Root-Sequence/wiki-private or pass --private-dir."
        )

    try:
        output.relative_to(build_root)
    except ValueError as exc:
        raise SystemExit("refusing to write private combined data outside .private-build/") from exc

    payload = build_combined(private_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"combined {payload['public_entity_count']} public entities, "
        f"{payload['private_only_entity_count']} private-only entities, and "
        f"{payload['overlay_count']} private overlays -> {output}"
    )


if __name__ == "__main__":
    main()
