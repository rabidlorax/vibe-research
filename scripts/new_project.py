#!/usr/bin/env python3
"""Scaffold a research project: python scripts/new_project.py <domain> <slug> ["Title"]"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv):
    if len(argv) not in (3, 4):
        sys.exit(__doc__)
    domain, slug = argv[1], argv[2]
    title = argv[3] if len(argv) == 4 else slug.replace("-", " ").capitalize()
    domain_dir = ROOT / "domains" / domain
    if not (domain_dir / "README.md").is_file():
        names = sorted(p.name for p in (ROOT / "domains").iterdir() if p.is_dir())
        sys.exit(f"Unknown domain '{domain}'. Choose from:\n  " + "\n  ".join(names))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("Slug must be lowercase letters, digits and hyphens, e.g. cap-set-bounds")
    project = domain_dir / "projects" / slug
    if project.exists():
        sys.exit(f"{project.relative_to(ROOT)} already exists")
    for sub in ("src", "data", "results"):
        (project / sub).mkdir(parents=True)
        (project / sub / ".gitkeep").touch()
    text = (ROOT / "templates" / "project-README.md").read_text()
    today = datetime.date.today().isoformat()
    for key, value in (("TITLE", title), ("DOMAIN", domain), ("DATE", today)):
        text = text.replace("{{" + key + "}}", value)
    (project / "README.md").write_text(text)
    print(f"Created {project.relative_to(ROOT)}")
    print("Next: fill in the Question section, then run python scripts/check_repo.py --write-index")


if __name__ == "__main__":
    main(sys.argv)
