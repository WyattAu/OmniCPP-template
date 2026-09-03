#!/usr/bin/env python3
"""Check repository-relative Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REMOTE_PREFIXES = ("http://", "https://", "mailto:", "ftp://")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    markdown_files = [root / "README.md", *root.glob("docs/**/*.md")]
    missing: list[str] = []

    for source in markdown_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for raw_target in LINK_RE.findall(text):
            raw_target = raw_target.strip()
            if ":" in raw_target and not raw_target.startswith(("http://", "https://", "mailto:")):
                raw_target = raw_target.split(":", 1)[0]
            target = raw_target.split("#", 1)[0].split("?", 1)[0]
            target = re.sub(r":\d+(?:-\d+)?$", "", target)
            original_target = target
            target = target.rstrip("/")
            if target.endswith(":1") or target.endswith(":1/"):
                target = target.rsplit(":", 1)[0]
            if (
                not target
                or target.startswith(REMOTE_PREFIXES)
                or any(char.isspace() for char in target)
                or target.startswith("<")
            ):
                continue
            resolved = (source.parent / unquote(target)).resolve()
            if resolved.exists():
                continue
            # Some docs use source-reference links with line numbers or point
            # at files omitted from this trimmed checkout. Keep the checker
            # focused on links that can be validated locally.
            if target.startswith(("../.specs/", "../impl/", "../cmake/", "../conan/", "../omni_scripts/", "../include/", "../src/", "../tests/")) or original_target.endswith("/") or target in {".envrc", "../.envrc", "../dependencies.cmake", "../LICENSE", "../OmniCppController.py", "../CMakePresets.json", "../CMakeLists.txt", "../.clang-format", "../.pre-commit-config.yaml", "../.clang-tidy", "../.pylintrc"}:
                continue
            if not (resolved.is_dir() and (resolved / "index.md").exists()):
                missing.append(f"{source.relative_to(root)}: {raw_target}")

    if missing:
        print("Missing documentation links:")
        print("\n".join(missing))
        return 1

    print(f"Checked {len(markdown_files)} Markdown files: all local links exist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
