#!/usr/bin/env python3
"""Add Draw.io / PNG / SVG links to lab README files."""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LABS = REPO / "modules"

OLD_PATTERNS = [
    "> 📊 **[View Lab Diagram](diagram.md)**",
    "**[Architecture Diagram](diagram.md)**",
]

def link_block(lab_dir: Path) -> str:
    name = lab_dir.name
    rel = "../../../../docs/diagrams"
    return (
        f"> 📊 **Diagrams:** [Mermaid](diagram.md) · "
        f"[Draw.io ({name}.drawio)]({rel}/drawio/{name}.drawio) · "
        f"[PNG]({rel}/png/{name}.png) · "
        f"[SVG]({rel}/svg/{name}.svg)"
    )


def main() -> None:
    updated = 0
    for readme in sorted(LABS.glob("module-*/labs/*/README.md")):
        lab_dir = readme.parent
        text = readme.read_text()
        new_line = link_block(lab_dir)
        if new_line in text:
            continue
        replaced = False
        for old in OLD_PATTERNS:
            if old in text:
                text = text.replace(old, new_line, 1)
                replaced = True
                break
        if not replaced:
            print(f"SKIP (no pattern): {readme.relative_to(REPO)}")
            continue
        readme.write_text(text)
        updated += 1
        print(f"Updated {readme.relative_to(REPO)}")
    print(f"\n{updated} README files updated")


if __name__ == "__main__":
    main()
