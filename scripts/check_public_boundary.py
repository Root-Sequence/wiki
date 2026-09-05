#!/usr/bin/env python3
"""Fail public CI if the Pages workflow starts consuming private Wiki data."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"

FORBIDDEN = {
    "wiki-private": "public Pages must not reference the private companion repository",
    "WIKI_PRIVATE_DIR": "public Pages must not load a private overlay path",
    "PRIVATE_WIKI_TOKEN": "public Pages must not accept private Wiki credentials",
    "merge_private_overlay.py": "public Pages must not run the private merge builder",
}


def main() -> None:
    text = PAGES_WORKFLOW.read_text(encoding="utf-8")
    violations = [message for token, message in FORBIDDEN.items() if token in text]
    if violations:
        for violation in violations:
            print(f"privacy-boundary violation: {violation}")
        raise SystemExit(1)
    print("public/private Wiki build boundary: OK")


if __name__ == "__main__":
    main()
